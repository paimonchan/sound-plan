import numpy as np
import soundfile as sf
import whisper

audio, sr = sf.read("E:/AI/sound-plan/data/training-news/raw.wav")
audio = audio.astype("float32")
if audio.ndim > 1:
    audio = audio.mean(axis=1)

m = whisper.load_model("tiny")
r = m.transcribe(audio, language="id", fp16=True, verbose=False)
text = r["text"][:300].encode("ascii", "replace").decode()
print(f"Content preview: {text}")
print(f"Size: {len(audio)/sr:.0f}s, Segments: {len(audio)/(sr*25):.0f}")
