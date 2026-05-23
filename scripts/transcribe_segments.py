"""Transcribe audio segments using Whisper and create training JSONL."""
import json
import numpy as np
import librosa
import soundfile as sf
import whisper
from pathlib import Path

SEG_DIR = Path("E:/AI/sound-plan/data/training-vrkt")
OUT_DIR = SEG_DIR / "16k"
OUT_DIR.mkdir(exist_ok=True)

print("Loading Whisper large-v3...")
model = whisper.load_model("turbo")  # faster than large-v3, good accuracy

segments = sorted(SEG_DIR.glob("seg_*.wav"))
print(f"Transcribing {len(segments)} segments...")

records = []
for seg in segments:
    audio, sr = sf.read(str(seg))

    # Convert stereo to mono if needed
    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    # Resample to 16kHz if needed
    if sr != 16000:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
    audio = audio.astype("float32")

    # Save 16kHz mono version
    mono_path = OUT_DIR / seg.name
    sf.write(str(mono_path), audio, 16000)

    # Transcribe
    result = model.transcribe(audio, language="id", fp16=True)
    text = result["text"].strip()

    records.append({
        "audio_path": str(mono_path.resolve().as_posix()),
        "text": text,
        "language": "id"
    })
    print(f"  {seg.name}: \"{text[:80]}...\"")

# Write JSONL
jsonl_path = SEG_DIR / "train.jsonl"
with open(jsonl_path, "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"\nSaved {len(records)} records to {jsonl_path}")
