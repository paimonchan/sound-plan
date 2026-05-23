# Audio Cleaning — untuk Training Data TTS

- **Status**: reviewed
- **Added**: 2026-05-23

---

## Pipeline Audio Bersih

```
Audio Kotor (noise/BGM/echo)
  → 1. Source Separation (hapus BGM)
  → 2. Noise Reduction (hapus noise/hiss)
  → 3. Final (audio bersih, siap training)
```

---

## 1. Source Separation — Hapus Background Music

| Tool | Kualitas | Speed | Cara install |
|------|:----:|:---:|-------------|
| **Demucs v4 (htdemucs_ft)** | ⭐⭐⭐⭐ | Medium | `pip install demucs` |
| **UVR (Ultimate Vocal Remover)** | ⭐⭐⭐⭐⭐ | Lambat | GUI app atau `uvr-headless-runner` |
| **vsep** | ⭐⭐⭐⭐⭐ | Fast | `pip install vsep` |
| **audio-separator** | ⭐⭐⭐⭐ | Medium | `pip install audio-separator` |

### Rekomendasi: Demucs

```bash
pip install demucs

# Vocals only (hapus BGM, ambil suara doang)
demucs --two-stems=vocals "lagu_ada_bgm.wav"
# Output: separated/htdemucs/lagu_ada_bgm/vocals.wav
#         separated/htdemucs/lagu_ada_bgm/no_vocals.wav
```

| Opsi | Fungsi |
|------|--------|
| `--two-stems=vocals` | Hanya pisah vokal vs instrumental |
| `-n htdemucs_ft` | Model terbaik untuk vokal |
| `--mp3` | Output MP3 (lebih kecil) |
| `--device cuda` | GPU inference |

### Kalau butuh kualitas maksimal: UVR

```bash
pip install uvr-headless-runner

# Roformer — kualitas vokal terbaik (SDR 12.98)
uvr mdx -m model_bs_roformer_ep_317_sdr_12.9755.ckpt -i audio.wav -o clean/ --gpu

# Demucs via UVR — 4 stems (vocal, drum, bass, other)
uvr demucs -m htdemucs_ft -i audio.wav -o clean/ --gpu
```

---

## 2. Noise Reduction — Hapus Static/Hiss/Noise

| Tool | Kualitas | Speed | Real-time | Install |
|------|:----:|:---:|:---:|---------|
| **DeepFilterNet3** | ⭐⭐⭐⭐⭐ | Fast | ✅ | `pip install deepfilternet` |
| **RNNoise** | ⭐⭐⭐ | Very Fast | ✅ | `pip install pyrnnoise` |
| **noisereduce** | ⭐⭐⭐ | Medium | ❌ | `pip install noisereduce` |

### Rekomendasi: DeepFilterNet3

```bash
pip install deepfilternet

# CLI
deep-filter noisy_audio.wav -o clean_audio.wav

# Python
from deepfilternet import enhance
enhance("noisy_audio.wav", "clean_audio.wav")
```

Kelebihan:
- 48kHz full-band
- Deep learning, hasil natural
- Ada mode low-latency (real-time)
- Pre-compiled binary (no Python needed)

### Kalau cuma perlu simpel: noisereduce

```python
import noisereduce as nr
import librosa

audio, sr = librosa.load("noisy.wav", sr=16000)
clean = nr.reduce_noise(y=audio, sr=sr, stationary=True)
sf.write("clean.wav", clean, sr)
```

---

## 3. Dereverberation — Hapus Echo

| Tool | Install |
|------|---------|
| **DeepFilterNet** (built-in reverb reduction) | `pip install deepfilternet` |
| **HiFi-GAN denoiser** | (via voxcpm denoiser path) |

DeepFilterNet sudah handle light reverb. Untuk heavy reverb, butuh tool spesifik.

---

## Workflow Lengkap (dari video YouTube/karaoke → training data)

```bash
# Step 1: Download audio (optional)
yt-dlp -x --audio-format wav "https://youtube.com/..." -o raw.wav

# Step 2: Hapus BGM → ambil vokal
demucs --two-stems=vocals raw.wav
# Output: separated/htdemucs/raw/vocals.wav

# Step 3: Hapus noise
deep-filter separated/htdemucs/raw/vocals.wav -o clean_final.wav

# Step 4: Potong jadi segmen 5-30 detik untuk training
# (manual di Audacity atau script Python)
```

---

## Untuk insta11 (paling cepet & gampang)

```bash
pip install demucs deepfilternet

# 1 command pipeline:
demucs --two-stems=vocals input.wav && deep-filter separated/htdemucs/input/vocals.wav -o clean.wav
```
