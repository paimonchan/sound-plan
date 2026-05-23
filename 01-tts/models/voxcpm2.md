# VoxCPM2

- **Paper VoxCPM v1**: [arXiv 2509.24650](https://arxiv.org/abs/2509.24650)
- **Paper VoxCPM2**: Coming soon (cited as GitHub only)
- **Repo**: <https://github.com/OpenBMB/VoxCPM>
- **Model Weights**: <https://huggingface.co/openbmb/VoxCPM2>
- **Demo Page**: <https://openbmb.github.io/voxcpm2-demopage/>
- **Status**: reviewed
- **Added**: 2026-05-23

---

## Overview

VoxCPM2 is a **tokenizer-free**, diffusion autoregressive TTS model by OpenBMB (Tsinghua/BAAI).
2B parameters, 30 languages, 48kHz output, trained on 2M+ hours multilingual speech.
Bypasses discrete tokenization entirely — operates directly on continuous speech representations.

## Architecture

```
LocEnc → TSLM → RALM → LocDiT
```

- **Backbone**: MiniCPM-4, 2B parameters
- **Audio VAE**: AudioVAE V2 (asymmetric encode/decode, 16kHz in → 48kHz out)
- **LM Token Rate**: 6.25 Hz
- **Max Sequence Length**: 8192 tokens
- **dtype**: bfloat16

## Features

| Feature | Description |
|---------|-------------|
| 30-Language Multilingual | No language tag needed; input text directly |
| Voice Design | Generate voice from text description — no reference audio needed |
| Controllable Cloning | Clone voice + optional style guidance (emotion, pace, expression) |
| Ultimate Cloning | Reference audio + transcript → every vocal nuance preserved |
| 48kHz Output | 16kHz input → 48kHz via built-in AudioVAE V2 super-resolution |
| Context-Aware | Auto-infers prosody and expressiveness from text |
| Streaming | RTF ~0.30 on RTX 4090, ~0.13 with Nano-VLLM |
| Fine-tuning | LoRA with 5-10 min audio; full SFT also supported |

## Supported Languages (30)

Arabic, Burmese, Chinese, Danish, Dutch, English, Finnish, French, German, Greek, Hebrew,
Hindi, **Indonesian**, Italian, **Japanese**, Khmer, Korean, Lao, Malay, Norwegian, Polish,
Portuguese, Russian, Spanish, Swahili, Swedish, Tagalog, Thai, Turkish, Vietnamese

Chinese Dialects: 四川话, 粤语, 吴语, 东北话, 河南话, 陕西话, 山东话, 天津话, 闽南话

## Quickstart

```bash
pip install voxcpm
```

```python
from voxcpm import VoxCPM
import soundfile as sf

model = VoxCPM.from_pretrained("openbmb/VoxCPM2")

# Basic TTS
wav = model.generate(text="Hello, this is VoxCPM2.", cfg_value=2.0, inference_timesteps=10)

# Voice Design (no reference needed)
wav = model.generate(text="(A young woman, gentle voice)Hello!", cfg_value=2.0, inference_timesteps=10)

# Voice Cloning
wav = model.generate(text="Cloned voice.", reference_wav_path="speaker.wav")

sf.write("output.wav", wav, model.tts_model.sample_rate)
```

## Hardware Requirements

| Metric | Value |
|--------|-------|
| VRAM | ~8 GB (bf16) |
| RTF (RTX 4090) | ~0.30 (standard) / ~0.13 (Nano-VLLM) |
| RTF (CPU, Strix Halo, 5 timesteps) | ~1.06-1.25 |
| Python | ≥ 3.10 |
| PyTorch | ≥ 2.5.0 |
| CUDA | ≥ 12.0 |

## Pros & Cons

**+ Strengths**
- SIM #1 for Indonesian (80.0%) and Japanese (82.8%)
- Tokenizer-free architecture avoids discrete bottleneck
- Voice design from text — no reference audio needed
- 48kHz studio-quality output
- Apache 2.0 — fully commercial
- LoRA fine-tuning with 5-10 min of audio
- Runs on CPU via VoxCPM.cpp (GGUF quantized)

**- Weaknesses**
- Paper for VoxCPM2 still "coming soon" (GitHub citation only)
- Voice design results vary — recommended 1-3 tries
- Performance varies across languages based on training data
- Occasional instability on very long or highly expressive inputs
- ~8GB VRAM needed for full quality (not edge-friendly without quantization)
