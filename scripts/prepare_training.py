"""Full pipeline: split + transcribe + JSONL + config for training"""
import json
import numpy as np
import soundfile as sf
import whisper
from pathlib import Path

NAME = "training-news"
DATADIR = Path(f"E:/AI/sound-plan/data/{NAME}")
SEGDIR = DATADIR / "segments"
SEGDIR.mkdir(exist_ok=True)

print("[1/4] Loading audio...")
audio, sr = sf.read(str(DATADIR / "raw.wav"))
audio = audio.astype("float32")
if audio.ndim > 1:
    audio = audio.mean(axis=1)

total_s = len(audio) / sr
print(f"  {total_s:.0f}s @ {sr}Hz mono")

# Split into 25s segments, skip < 3s
print(f"\n[2/4] Splitting into 25s segments...")
SEG_S = 25
records = []
seg_count = 0

for i, start in enumerate(range(0, len(audio), SEG_S * sr)):
    end = min(start + SEG_S * sr, len(audio))
    chunk = audio[start:end]
    if len(chunk) < sr * 3:
        continue
    seg_path = SEGDIR / f"seg_{i:03d}.wav"
    sf.write(str(seg_path), chunk, sr)
    records.append({"path": str(seg_path.resolve().as_posix()), "audio": chunk.copy(), "idx": i})
    seg_count += 1

print(f"  {seg_count} segments saved")

# Transcribe
print(f"\n[3/4] Transcribing with Whisper turbo...")
model = whisper.load_model("turbo")

jsonl_records = []
for r in records:
    result = model.transcribe(r["audio"], language="id", fp16=True, verbose=False)
    text = result["text"].strip()
    jsonl_records.append({
        "audio_path": r["path"],
        "text": text,
        "language": "id"
    })
    preview = text[:80].encode("ascii", "replace").decode()
    print(f"  seg_{r['idx']:03d}.wav: \"{preview}...\"")

# Write JSONL
jsonl_path = DATADIR / "train.jsonl"
with open(jsonl_path, "w", encoding="utf-8") as f:
    for r in jsonl_records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"\n  JSONL: {jsonl_path} ({len(jsonl_records)} records)")

# Create config YAML
print(f"\n[4/4] Creating config YAML...")
config = f"""pretrained_path: E:/AI/sound-plan/models/voxcpm2/
train_manifest: E:/AI/sound-plan/data/training-news/train.jsonl
val_manifest: null
sample_rate: 16000
out_sample_rate: 48000
batch_size: 2
grad_accum_steps: 8
num_workers: 4
num_iters: 1000
log_interval: 10
valid_interval: 500
save_interval: 500
learning_rate: 0.0001
weight_decay: 0.01
warmup_steps: 100
max_steps: 1000
max_batch_tokens: 8192
max_grad_norm: 1.0
save_path: E:/AI/sound-plan/models/voxcpm2-ft-{NAME}
tensorboard: E:/AI/sound-plan/logs/{NAME}
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
cfg_path = DATADIR / "config.yaml"
cfg_path.write_text(config)
print(f"  Config: {cfg_path}")

print(f"\nDone! Ready to train:")
print(f"  Data: {DATADIR}")
print(f"  Segments: {seg_count}")
print(f"  Total audio: {total_s:.0f}s")
