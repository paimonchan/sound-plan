# Qwen3-TTS

- **Paper**: [arXiv 2601.15621](https://arxiv.org/abs/2601.15621)
- **Repo**: <https://github.com/QwenLM/Qwen3-TTS>
- **HuggingFace**: <https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base>
- **License**: Apache 2.0
- **Status**: reviewed
- **Added**: 2026-05-24

---

## Overview

Qwen3-TTS dari Alibaba (Qwen team). **WER terendah di Seed-TTS benchmark** (1.24 EN, 0.77 ZH). 5M jam training data. 10 bahasa. Streaming 97ms.

## Model Variants

| Model | Size | Fitur |
|-------|:----:|-------|
| 12Hz-1.7B-Base | 1.7B | Voice clone 3 detik, fine-tuning |
| 12Hz-1.7B-CustomVoice | 1.7B | 9 preset voices + instruction control |
| 12Hz-1.7B-VoiceDesign | 1.7B | Voice design dari teks deskripsi |
| 12Hz-0.6B-Base | 0.6B | Lebih ringan, voice clone |
| 12Hz-0.6B-CustomVoice | 0.6B | 9 preset voices, lightweight |

## Benchmark (Seed-TTS)

| Model | test-EN WER↓ | test-ZH WER↓ |
|-------|:----------:|:----------:|
| **Qwen3-TTS 1.7B Base** | **1.24** | **0.77** |
| CosyVoice 3 | 1.45 | 0.71 |
| MiniMax-Speech | 1.65 | 0.83 |
| F5-TTS | 1.83 | 1.56 |
| Seed-TTS | 2.25 | 1.12 |

**WER terendah di semua benchmark open-source.**

## Languages

Chinese, English, **Japanese**, Korean, German, French, Russian, Portuguese, Spanish, Italian. + Chinese dialects.

## Key Features

- **Streaming 97ms** — first-packet latency terendah
- **Voice clone 3 detik** — zero-shot
- **Voice design** — text description → suara baru
- **Cross-lingual** — voice clone antar bahasa
- **Long-form** — 10+ menit stabil

## Pros/Cons

**+** WER terendah industri, Apache 2.0, streaming tercepat
**-** Tidak support Indonesia, 10 bahasa aja (banding: OmniVoice 600+), VRAM ~8 GB

## Fit for Indo+Japanese?

- **Indonesia**: ❌ Tidak didukung
- **Japanese**: ✅ Didukung (dengan preset speaker Ono_Anna)
