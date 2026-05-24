# Project Inventory — Installed Tools & Libraries

- **Updated**: 2026-05-24

---

## Python Virtual Environment

| Location | Python | Size |
|----------|:------:|:----:|
| `E:\AI\sound-plan\.venv` | 3.10.6 | 5.1 GB |

### Core AI Packages

| Package | Version | Purpose |
|---------|---------|---------|
| `torch` | 2.11.0+cu128 | GPU compute |
| `torchaudio` | 2.11.0+cu128 | Audio I/O |
| `voxcpm` | 2.0.3 | VoxCPM2 TTS |
| `gradio` | 6.14.0 | Web UI |
| `transformers` | 5.9.0 | HuggingFace models |
| `safetensors` | 0.7.0 | Safe model format |
| `huggingface-hub` | 1.16.1 | HF model download |

### Audio Processing

| Package | Version | Purpose |
|---------|---------|---------|
| `demucs` | 4.0.1 | Source separation (BGM removal) |
| `openai-whisper` | 20250625 | Speech-to-text transcription |
| `soundfile` | 0.13.1 | Audio file I/O |
| `librosa` | 0.11.0 | Audio DSP |
| `funasr` | 1.3.1 | Chinese ASR (VoxCPM dep) |
| `DeepFilterNet` | 0.5.6 | Noise reduction (Python, may not work) |

### Download/Utility

| Package | Version | Purpose |
|---------|---------|---------|
| `yt-dlp` | 2026.3.17 | YouTube audio download |
| `modelscope` | 1.37.1 | Chinese model hub |

---

## Standalone Binaries (in `tools/`)

| Tool | File | Size | Purpose |
|------|------|:----:|---------|
| **deep-filter** | `tools/deep-filter.exe` | 25.7 MB | Noise reduction (CLI, standalone) |
| **ffmpeg** (shared) | `tools/ffmpeg-shared/` | 1.2 GB | Audio/video conversion |

---

## Whisper Model Cache

| Model | Location | Size |
|-------|----------|:----:|
| `large-v3-turbo` | `~/.cache/whisper/` | 1.5 GB |
| `tiny` | `~/.cache/whisper/` | 72 MB |

---

## Downloaded Models (in `models/`)

| Model | Size | Purpose |
|-------|:----:|---------|
| VoxCPM2 (base) | 4.7 GB | TTS inference |
| VoxCPM2 LoRA (Sakura Miko) | 69 MB | Custom Japanese voice |

---

## Cloned Repos (in `repos/`)

| Repo | Stars | Purpose |
|------|:-----:|---------|
| `OpenBMB/VoxCPM` | 19.6K | Training tools + official demo |

---

## Scripts (in `scripts/`)

| Script | Function |
|--------|----------|
| `clean_audio.bat` | One-click audio cleaning (drag & drop) |
| `train_pipeline.py` | YouTube → split → transcribe → train (1 command) |
| `split_audio.py` | Split audio into segments |
| `transcribe_segments.py` | Transcribe audio segments with Whisper |
| `test_voxcpm2.py` | VoxCPM2 inference test |
| `check_audio.py` | Quick audio content check |

---

## Web Apps (in `apps/`)

| App | Port | How to run |
|-----|:----:|-----------|
| VoxCPM2 Gradio (TTS) | 7860 | `run.bat` |
| VoxCPM2 Training (LoRA) | 7860 | `run_train.bat` |

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
| `models/voxcpm2/` | VoxCPM2 weights |
| `models/voxcpm2-ft-training-news/latest/` | LoRA checkpoint |
| `repos/VoxCPM/scripts/train_voxcpm_finetune.py` | Training script |

## ACE-Step 1.5 (in E:\AI\ACE-Step-1.5\)

| Item | Detail |
|------|--------|
| Location | E:\AI\ACE-Step-1.5\ |
| Venv | Python 3.12.13, uv-managed, 6 GB |
| Models | 9.4 GB (turbo DiT + 1.7B LM + VAE + Qwen3-Emb) |
| Total | 15.5 GB |
| Launch | 'uv run acestep' -> http://localhost:7860 |
| GPU | RTX 5070, Tier 4 (11.94 GB) |
| License | MIT |
