# Project Inventory — Installed Tools & Libraries

- **Updated**: 2026-09-13

> **Status**: Terinstall lokal: **YuE2** (music generation) dalam 2 rute — **audio.cpp Q8** (`E:\AI\audio.cpp\`) dan **ComfyUI native INT8** (`E:\AI\ComfyUI\models\`). **VoxCPM2** (TTS) dan **ACE-Step 1.5** sudah di-remove (lihat [Removed](#removed)).

---

## Local AI App — YuE2 (audio.cpp) — E:\AI\audio.cpp\

| Item | Detail |
|------|--------|
| App | **YuE2-3B** music generation (M-A-P) |
| Runtime | audio.cpp dev build, Windows CUDA 13.3 (C++/ggml, tanpa Python) |
| Venv/model dir | `E:\AI\audio.cpp\bin\` + `models\yue2\` |
| Size | **5.24 GB** (bin 1.03 GB + models 4.32 GB) |
| Model | `yue2-3b-q8_0.gguf` (3.97 GiB) + `yue2-vae-f16.gguf` (247 MiB) + sidecars |
| Launch | `bin\audiocpp_cli.exe --task gen --family yue2 --model models\yue2 --backend cuda ...` |
| Peak VRAM | **5.78 GiB** (lagu 31.8s, cot=off) |
| Output | 48 kHz stereo PCM_16 |
| License | weights **CC BY-NC 4.0** (non-komersial) |
| Plan/detail | `plan/yue2-install-q8.md`, `04-audio-generation/models/yue2.md` |

### YuE2 via ComfyUI native (INT8) — E:\AI\ComfyUI\

| Item | Detail |
|------|--------|
| ComfyUI | diupdate v0.35.1 → `master 02d39c8c` (native YuE2, PR #16250) |
| Checkpoint | `models\checkpoints\yue2_3b_int8_convrot.safetensors` (3.69 GB, INT8) |
| Encoder cover | `models\audio_encoders\sheetsage2_bf16.safetensors` (1.29 GB) |
| Peak VRAM | **5.84 GiB** (lagu 40s) |
| Waktu | ~13.4s execution |
| Template | `yue2_int8_text_to_song.json`, `yue2_anison_jrock.json`, `yue2_anison_jrock_instrumental.json` — di `E:\AI\eikei-plan\custom\workflows\music\` + aktif di `E:\AI\ComfyUI\user\default\workflows\music\` |
| Catatan | ComfyUI pernah di-restart; revert: `git -C E:\AI\ComfyUI checkout 856a922b` |

---

## Python Virtual Environment

| Location | Python | Size |
|----------|:------:|:----:|
| `E:\AI\sound-plan\.venv` | 3.10.6 | 5.1 GB |

Package `voxcpm` sudah di-uninstall. Environment masih menyimpan tool audio umum (Whisper, Demucs, dll).

### Core AI Packages

| Package | Version | Purpose |
|---------|---------|---------|
| `torch` | 2.11.0+cu128 | GPU compute |
| `torchaudio` | 2.11.0+cu128 | Audio I/O |
| `transformers` | 5.9.0 | HuggingFace models |
| `safetensors` | 0.7.0 | Safe model format |
| `huggingface-hub` | 1.16.1 | HF model download |
| `gradio` | 6.14.0 | Web UI |

### Audio Processing

| Package | Version | Purpose |
|---------|---------|---------|
| `demucs` | 4.0.1 | Source separation (BGM removal) |
| `openai-whisper` | 20250625 | Speech-to-text transcription |
| `soundfile` | 0.13.1 | Audio file I/O |
| `librosa` | 0.11.0 | Audio DSP |
| `funasr` | 1.3.1 | Chinese ASR (sisa dep VoxCPM) |
| `DeepFilterNet` | 0.5.6 | Noise reduction (Python, may not work) |

### Download/Utility

| Package | Version | Purpose |
|---------|---------|---------|
| `yt-dlp` | 2026.3.17 | YouTube audio download |
| `modelscope` | 1.37.1 | Chinese model hub |

---

## Standalone Binaries (in `tools/`)

| Tool | File | Purpose |
|------|------|---------|
| **deep-filter** | `tools/deep-filter.exe` | Noise reduction (CLI, standalone) |
| **ffmpeg** (shared) | `tools/ffmpeg-shared/` | Audio/video conversion |
| **ffmpeg** | `tools/ffmpeg/` | Audio/video conversion |

---

## Whisper Model Cache

| Model | Location | Size |
|-------|----------|:----:|
| `tiny` | `~/.cache/whisper/` | 72 MB |

---

## Downloaded Models (in `models/`)

Kosong. (VoxCPM2 + LoRA sudah dihapus.)

---

## Cloned Repos (in `repos/`)

Kosong. (OpenBMB/VoxCPM sudah dihapus.)

---

## Scripts (in `scripts/`)

| Script | Function |
|--------|----------|
| `clean_audio.bat` | One-click audio cleaning (drag & drop) |
| `split_audio.py` | Split audio into segments |
| `transcribe_segments.py` | Transcribe audio segments with Whisper |

---

## Web Apps (in `apps/`)

Kosong.

---

## Key Paths

| Path | Content |
|------|---------|
| `.venv/Scripts/python.exe` | Python interpreter |
| `.venv/Scripts/pip.exe` | Package manager |
| `.venv/Scripts/demucs.exe` | Demucs CLI |
| `.venv/Scripts/yt-dlp.exe` | YouTube downloader |
| `tools/deep-filter.exe` | Noise reduction CLI |
| `tools/ffmpeg-shared/.../bin/ffmpeg.exe` | FFmpeg |

---

## Removed

| Item | Detail | Date |
|------|--------|------|
| VoxCPM2 (TTS) | `models/voxcpm2` (4.7 GB) + LoRA (207 MB), `repos/VoxCPM`, `apps/voxcpm2-gradio`, package `voxcpm` 2.0.3 | 2026-09-13 |
| ACE-Step 1.5 (song gen) | `E:\AI\ACE-Step-1.5\` (15.5 GB), `apps/acestep-gradio` | ~2026-09 |
