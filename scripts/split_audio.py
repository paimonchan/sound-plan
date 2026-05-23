import soundfile as sf
from pathlib import Path

SRC = Path("E:/AI/sound-plan/data/clean.wav/vocals.wav")
OUTDIR = Path("E:/AI/sound-plan/data/training-vrkt")
OUTDIR.mkdir(parents=True, exist_ok=True)

audio, sr = sf.read(str(SRC))
print(f"Source: {len(audio)/sr:.0f}s @ {sr}Hz, {audio.shape}")

SEG_S = 25  # seconds per segment
total = len(audio)

count = 0
for i, start in enumerate(range(0, total, SEG_S * sr)):
    end = min(start + SEG_S * sr, total)
    chunk = audio[start:end]
    if len(chunk) < sr * 3:
        continue
    name = OUTDIR / f"seg_{i:03d}.wav"
    sf.write(str(name), chunk, sr)
    print(f"  {name.name}: {len(chunk)/sr:.1f}s")
    count += 1

print(f"\nSaved {count} segments to {OUTDIR}")
