# VoxCPM2 Gradio Web UI

- **Status**: done
- **Added**: 2026-05-23

---

## Quick Start

### Inference (TTS)

```powershell
# Double-click:
E:\AI\sound-plan\apps\voxcpm2-gradio\run.bat
# → http://localhost:7860
```

### Training (Voice Fine-tuning)

```powershell
# Double-click:
E:\AI\sound-plan\apps\voxcpm2-gradio\run_train.bat
# → http://localhost:7860
```

---

## Features

| Tab | Description |
|-----|-------------|
| **TTS** | Text-to-Speech, 30 languages |
| **Voice Clone** | Upload reference audio 3-10 detik, zero-shot |
| **Voice Design** | Generate suara dari deskripsi teks |
| **Training** (separate app) | Fine-tune suara custom dengan LoRA (5-10 menit audio) |

---

## Training Steps

Lihat: [`01-tts/training/voxcpm2-training.md`](../../01-tts/training/voxcpm2-training.md)

1. Siapkan 5-10 menit audio + transkrip (JSONL)
2. Buat config YAML di `configs/`
3. Jalankan `run_train.bat` atau CLI
4. Load checkpoint via `lora_path`

---

## Project Structure

```
E:\AI\sound-plan\
  models/voxcpm2/            ← Model weights (4.7 GB, not in git)
  repos/VoxCPM/              ← Official source (training tools, not in git)
  apps/voxcpm2-gradio/
    run.bat                  ← Launch TTS Web UI
    run_train.bat            ← Launch Training Web UI
    app.py                   ← TTS Gradio app
    README.md
  .venv/                     ← Shared Python 3.10 venv
```

---

## Hardware

| Component | Requirement |
|-----------|-------------|
| GPU VRAM | 8 GB minimum |
| RAM | 16 GB+ |
| Disk | ~5 GB model + 1.4 GB venv + ~50 MB repo |
| Python | 3.10+ (venv included) |

**Tested**: RTX 5070 12GB, Ryzen 7 5700X, 32GB RAM, Windows 11
