# VoxCPM2 — Deployment Guide

- **Status**: reviewed
- **Added**: 2026-05-23

---

## Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.10+ | 3.12 |
| PyTorch | 2.5.0+ | 2.8.0+ |
| CUDA | 12.0+ | 12.8 |
| GPU VRAM | 8 GB (bf16) | RTX 4090 (24 GB) |
| CPU (via VoxCPM.cpp) | 8 cores | Strix Halo / Apple M4 |

---

## Installation

```bash
conda create -n voxcpm python=3.12 -y
conda activate voxcpm

pip install torch==2.8.0+cu128 torchaudio==2.8.0+cu128 --extra-index-url https://download.pytorch.org/whl/cu128
pip install voxcpm
```

---

## Inference Modes

### 1. Basic Text-to-Speech

```python
from voxcpm import VoxCPM
model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)
wav = model.generate(text="Hello world.", cfg_value=2.0, inference_timesteps=10)
```

### 2. Voice Cloning (Zero-shot)

```python
wav = model.generate(
    text="This is a cloned voice.",
    reference_wav_path="speaker.wav",
)
```

### 3. Voice Design (from text, no audio)

```python
wav = model.generate(
    text="(A warm, authoritative male voice)Welcome to VoxCPM2.",
    cfg_value=2.0,
    inference_timesteps=10,
)
```

### 4. Controllable Cloning (clone + style)

```python
wav = model.generate(
    text="(slightly faster, cheerful tone)Cloned with style control.",
    reference_wav_path="speaker.wav",
    cfg_value=2.0,
    inference_timesteps=10,
)
```

### 5. Ultimate Cloning (reference + transcript)

```python
wav = model.generate(
    text="Ultimate cloning demo.",
    prompt_wav_path="speaker.wav",
    prompt_text="Transcript of the reference.",
    reference_wav_path="speaker.wav",
)
```

### 6. Streaming

```python
import numpy as np

chunks = []
for chunk in model.generate_streaming(text="Streaming demo."):
    chunks.append(chunk)
wav = np.concatenate(chunks)
```

---

## Performance Tuning

| Parameter | Impact |
|-----------|--------|
| `cfg_value` (1.0-3.0) | Higher = better prompt adherence, may reduce quality |
| `inference_timesteps` (5-20) | Higher = better quality, slower. 5 = fast, 10 = balanced |
| `temperature` (0.5-1.5) | Higher = more variation |
| `normalize=True` | Enable external text normalization |
| `denoise=True` | Enable external denoiser |
| `retry_badcase=True` | Auto-retry on bad generations |

---

## CPU Deployment (VoxCPM.cpp)

For English/Chinese only, VoxCPM1.5 via GGUF quantized:

```bash
git clone https://github.com/OpenBMB/VoxCPM.cpp
cd VoxCPM.cpp
python convert.py --model openbmb/VoxCPM2  # or VoxCPM1.5
```

Performance on Strix Halo CPU (no GPU):
- VoxCPM1.5 Q8_0: RTF 1.23, ~1GB RAM
- VoxCPM2 Python 5 timesteps: RTF 1.06-1.25, ~2.5GB RAM

---

## Fine-tuning

### LoRA (5-10 min audio)

```bash
python scripts/train_voxcpm_finetune.py \
    --config_path conf/voxcpm_v2/voxcpm_finetune_lora.yaml
```

### Full SFT

```bash
python scripts/train_voxcpm_finetune.py \
    --config_path conf/voxcpm_v2/voxcpm_finetune_all.yaml
```

---

## Nano-VLLM Acceleration

2x speedup on NVIDIA GPUs:

```python
# Install Nano-VLLM first
# RTF drops from ~0.30 → ~0.13 on RTX 4090
```

---

## Serving (vLLM-omni)

Production serving with continuous batching, paged KV cache:

```bash
# See: https://github.com/vllm-project/vllm-omni
# Supports: voice_clone, default_voice, voice_design tasks
# Benchmarked on H20-3e 141GB
```

---

## Known Limitations

- Voice design: 1-3 tries recommended for desired output
- Performance varies by language (better on high-resource)
- Occasional instability on very long (>2000 chars) or expressive inputs
- AudioVAE V2 accepts 16kHz reference only
- No official zero-shot voice cloning on CPU build (VoxCPM.cpp uses v1.5)
