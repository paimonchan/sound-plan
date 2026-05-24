import os
os.environ["HF_HOME"] = "E:/AI/sound-plan/.hf_cache"
os.environ["HF_HUB_CACHE"] = "E:/AI/sound-plan/.hf_cache"

import torch
import soundfile as sf
import time

print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0)}")
print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
print()

from voxcpm import VoxCPM

print("Loading VoxCPM2...")
start = time.time()
model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)
print(f"Model loaded in {time.time() - start:.1f}s")
print()

test_cases = [
    ("id", "Indonesian", "Halo semuanya! Selamat datang di demo VoxCPM2 untuk bahasa Indonesia. Hari ini cuaca sangat cerah dan saya sangat senang bisa mencoba teknologi text-to-speech terbaru ini."),
    ("ja", "Japanese", "こんにちは、皆さん。VoxCPM2の日本語デモへようこそ。今日はとてもいい天気で、最新の音声合成技術を試すことができて嬉しいです。"),
]

for lang, name, text in test_cases:
    print(f"[{name}] Generating...")
    start = time.time()
    wav = model.generate(
        text=text,
        cfg_value=2.0,
        inference_timesteps=10,
    )
    elapsed = time.time() - start
    duration = len(wav) / model.tts_model.sample_rate
    rtf = elapsed / duration
    output_path = f"E:/AI/sound-plan/test_output_{lang}.wav"
    sf.write(output_path, wav, model.tts_model.sample_rate)
    print(f"  -> {output_path}")
    print(f"  -> Duration: {duration:.1f}s, Generation: {elapsed:.1f}s, RTF: {rtf:.2f}")
    print()

print("Done!")
