# VoxCPM2 Gradio Web UI

- **Status**: done
- **Added**: 2026-05-23

---

## Quick Start

```powershell
# Activate venv & run
& "E:\AI\sound-plan\.venv\Scripts\python.exe" "E:\AI\sound-plan\apps\voxcpm2-gradio\app.py"
```

Buka **http://localhost:7860**

---

## Features

| Feature | Description |
|---------|-------------|
| **Text-to-Speech** | 30 languages, auto-detect |
| **Voice Clone** | Upload reference audio 3-10 detik |
| **Voice Design** | Generate suara dari deskripsi teks |
| **Parameter control** | Timesteps (quality), CFG (prompt adherence) |
| **Examples** | Indonesian & Japanese built-in |

---

## Hardware

| Component | Requirement |
|-----------|-------------|
| GPU VRAM | 8 GB minimum |
| RAM | 16 GB+ |
| Disk | ~5 GB model + 1.4 GB venv |
| Python | 3.10+ (venv included) |

**Tested**: RTX 5070 12GB, Ryzen 7 5700X, 32GB RAM, Windows 11

---

## Architecture

```
apps/voxcpm2-gradio/
  app.py           ← Single-file Gradio app
  README.md        ← This file

models/voxcpm2/    ← Model weights (4.7 GB, not in git)
  model.safetensors  (4.3 GB)
  audiovae.pth       (359 MB)
  tokenizer.json     (4 MB)
  config.json
```

---

## Performance

| Metric | Value |
|--------|-------|
| Model load time | ~17s (cold) |
| RTF (Indonesian) | 1.75 (without Triton) |
| RTF (Japanese) | 1.75 (without Triton) |
| Output | 48kHz mono WAV |

Optimization pending: `pip install triton` → torch.compile → estimasi RTF ~0.6

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| CUDA not available | `pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128` |
| Low VRAM | Turunkan `inference_timesteps` ke 5 |
| Triton not installed | `pip install triton` untuk 2-3x speedup |
