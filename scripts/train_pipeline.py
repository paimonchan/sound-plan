"""
One-command training pipeline: YouTube URL -> split -> transcribe -> train

Usage:
  python train_pipeline.py "https://youtube.com/watch?v=xxx" --name my_voice --lang ja

What it does:
  1. Download audio from YouTube (yt-dlp + ffmpeg)
  2. Split into 25s segments
  3. Transcribe with Whisper
  4. Create train.jsonl + config.yaml
  5. Run LoRA training
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import whisper

ROOT = Path("E:/AI/sound-plan")
VENV_PYTHON = ROOT / ".venv/Scripts/python.exe"
VENV_BIN = ROOT / ".venv/Scripts"
FFMPEG_BIN = ROOT / "tools/ffmpeg-shared/ffmpeg-master-latest-win64-gpl-shared/bin"
TRAIN_SCRIPT = ROOT / "repos/VoxCPM/scripts/train_voxcpm_finetune.py"

def main():
    parser = argparse.ArgumentParser(description="VoxCPM2 Training Pipeline")
    parser.add_argument("url", help="YouTube URL")
    parser.add_argument("--name", default="my-voice", help="Dataset name")
    parser.add_argument("--lang", default="ja", help="Language code (ja, id, en, etc.)")
    parser.add_argument("--model", default="turbo", help="Whisper model (tiny/turbo)")
    parser.add_argument("--seg", type=int, default=25, help="Segment duration in seconds")
    parser.add_argument("--steps", type=int, default=1000, help="Training steps")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--skip-download", action="store_true", help="Skip YouTube download")
    parser.add_argument("--skip-train", action="store_true", help="Skip training (only prep data)")
    args = parser.parse_args()

    datadir = ROOT / f"data/{args.name}"
    datadir.mkdir(parents=True, exist_ok=True)
    raw_path = datadir / "raw.wav"

    # Step 1: Download
    if not args.skip_download:
        print(f"[1/5] Downloading from YouTube...")
        env = {"PATH": f"{FFMPEG_BIN};{Path.home()}"}
        subprocess.run([
            str(VENV_BIN / "yt-dlp.exe"), "-x", "--audio-format", "wav",
            "--audio-quality", "0", "--postprocessor-args",
            "ffmpeg:-ar 16000 -ac 1", "--ffmpeg-location",
            str(FFMPEG_BIN / "ffmpeg.exe"), args.url, "-o", str(raw_path)
        ], check=True, env=env, cwd=str(ROOT))
        print(f"  -> {raw_path}")
    else:
        print(f"[1/5] Using existing: {raw_path}")

    # Step 2: Load & split
    print(f"[2/5] Loading & splitting audio...")
    audio, sr = sf.read(str(raw_path))
    audio = audio.astype("float32")
    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    segdir = datadir / "segments"
    segdir.mkdir(exist_ok=True)
    seg_paths = []
    count = 0
    for i, start in enumerate(range(0, len(audio), args.seg * sr)):
        end = min(start + args.seg * sr, len(audio))
        chunk = audio[start:end]
        if len(chunk) < sr * 3:
            continue
        sp = segdir / f"seg_{i:03d}.wav"
        sf.write(str(sp), chunk, sr)
        seg_paths.append(sp)
        count += 1

    print(f"  {count} segments ({len(audio)/sr:.0f}s total)")

    # Step 3: Transcribe
    print(f"[3/5] Transcribing with Whisper {args.model} (lang={args.lang})...")
    model = whisper.load_model(args.model)
    records = []

    for sp in seg_paths:
        a, _ = sf.read(str(sp))
        a = a.astype("float32")
        if a.ndim > 1:
            a = a.mean(axis=1)
        r = model.transcribe(a, language=args.lang, fp16=True, verbose=False)
        text = r["text"].strip()
        records.append({"audio": str(sp.resolve().as_posix()), "text": text, "language": args.lang})
        preview = text[:80].encode("ascii", "replace").decode()
        print(f"  {sp.name}: {preview}")

    # Step 4: Write JSONL + config
    print(f"[4/5] Creating JSONL & config...")
    jsonl = datadir / "train.jsonl"
    with open(jsonl, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    config = f"""pretrained_path: {ROOT.as_posix()}/models/voxcpm2/
train_manifest: {datadir.as_posix()}/train.jsonl
val_manifest: null
sample_rate: 16000
out_sample_rate: 48000
batch_size: 2
grad_accum_steps: 8
num_workers: 4
num_iters: {args.steps}
log_interval: 10
valid_interval: 500
save_interval: 500
learning_rate: {args.lr}
weight_decay: 0.01
warmup_steps: 100
max_steps: {args.steps}
max_batch_tokens: 8192
max_grad_norm: 1.0
save_path: {ROOT.as_posix()}/models/voxcpm2-ft-{args.name}
tensorboard: {ROOT.as_posix()}/logs/{args.name}
lambdas:
  loss/diff: 1.0
  loss/stop: 1.0
lora:
  enable_lm: true
  enable_dit: true
  enable_proj: false
  r: 32
  alpha: 32
  dropout: 0.0
"""
    cfg = datadir / "config.yaml"
    cfg.write_text(config)
    print(f"  JSONL: {jsonl} ({len(records)} samples)")
    print(f"  Config: {cfg}")

    # Step 5: Train
    if args.skip_train:
        print(f"\n[5/5] Skipped. Run manually:")
        print(f"  python repos/VoxCPM/scripts/train_voxcpm_finetune.py --config_path {cfg}")
        return

    print(f"\n[5/5] Training ({args.steps} steps, LoRA)...")
    print(f"  This may take 15-30 minutes. Checkpoints -> models/voxcpm2-ft-{args.name}/")
    print(f"  Logs -> logs/{args.name}/\n")

    env = {"PYTHONPATH": str(ROOT / "repos/VoxCPM/src"), "PATH": f"{VENV_BIN};{Path.home()}"}
    subprocess.run([
        str(VENV_PYTHON), str(TRAIN_SCRIPT), "--config_path", str(cfg)
    ], check=True, env=env, cwd=str(ROOT))

    print(f"\nDone! Checkpoint: models/voxcpm2-ft-{args.name}/")


if __name__ == "__main__":
    main()
