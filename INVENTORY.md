# Project Inventory — Installed Tools & Libraries

- **Updated**: 2026-09-13

> **Status**: Tidak ada model/app AI yang terinstall saat ini. **VoxCPM2** (TTS) dan **ACE-Step 1.5** (song generation) sudah di-remove dari disk beserta model weights, repo, dan package `voxcpm`. Lihat bagian [Removed](#removed) di bawah.

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
