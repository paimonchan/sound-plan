"""Re-transcribe with Japanese language and regenerate JSONL"""
import json
import numpy as np
import soundfile as sf
import whisper
from pathlib import Path

DATADIR = Path("E:/AI/sound-plan/data/training-news")
SEGDIR = DATADIR / "segments"

seg_files = sorted(SEGDIR.glob("seg_*.wav"))
print(f"Re-transcribing {len(seg_files)} segments with Japanese...")

model = whisper.load_model("turbo")
records = []

for seg in seg_files:
    audio, sr = sf.read(str(seg))
    audio = audio.astype("float32")
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    
    result = model.transcribe(audio, language="ja", fp16=True, verbose=False)
    text = result["text"].strip()
    
    records.append({
        "audio_path": str(seg.resolve().as_posix()),
        "text": text,
        "language": "ja"
    })
    
    preview = text[:100].encode("ascii", "replace").decode()
    print(f"  {seg.name}: \"{preview}...\"")

# Write JSONL
jsonl_path = DATADIR / "train.jsonl"
with open(jsonl_path, "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"\nDone! {len(records)} records saved to {jsonl_path}")
print("Ready to train:")
print(f"  python repos/VoxCPM/scripts/train_voxcpm_finetune.py --config_path data/training-news/config.yaml")
