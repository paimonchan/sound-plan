# VoxCPM2 — Benchmarks

- **Source**: <https://github.com/OpenBMB/VoxCPM>
- **Status**: reviewed
- **Added**: 2026-05-23

---

## Seed-TTS-eval

Standard zero-shot TTS benchmark. Lower WER = better intelligibility, higher SIM = better speaker similarity.

| Model | Params | Open | test-EN WER↓ | test-EN SIM↑ | test-ZH WER/CER↓ | test-ZH SIM↑ | test-Hard CER↓ | test-Hard SIM↑ |
|-------|:------:|:----:|:----------:|:----------:|:--------------:|:----------:|:------------:|:------------:|
| **VoxCPM2** | 2B | ✅ | **1.84** | **75.3** | **0.97** | **79.5** | 8.13 | 75.3 |
| FishAudio S2 | 4B | ✅ | 0.99 | - | 0.54 | - | 5.99 | - |
| LongCat-Audio-DiT | 3.5B | ✅ | 1.50 | 78.6 | 1.09 | 81.8 | 6.04 | 79.7 |
| Qwen3-TTS | 1.7B | ✅ | 1.23 | 71.7 | 1.22 | 77.0 | 6.76 | 74.8 |
| MOSS-TTS | 1.7B | ✅ | 1.93 | 73.3 | 1.20 | 78.8 | - | - |
| CosyVoice3 | 0.5B | ❌ | 2.02 | 71.8 | 1.16 | 78.0 | 6.08 | 75.8 |
| MiniMax-Speech | - | ❌ | 1.65 | 69.2 | 0.83 | 78.3 | - | - |
| Seed-TTS | - | ❌ | 2.25 | 76.2 | 1.12 | 79.6 | 7.59 | 77.6 |
| F5-TTS | 0.3B | ✅ | 2.00 | 67.0 | 1.53 | 76.0 | 8.67 | 71.3 |
| IndexTTS2 | 1.5B | ✅ | 2.23 | 70.6 | 1.03 | 76.5 | 7.12 | 75.5 |
| SparkTTS | 0.5B | ✅ | 3.14 | 57.3 | 1.54 | 66.0 | - | - |

**Key takeaway**: VoxCPM2 EN SIM = 75.3 (#2 among open-source, behind LongCat's 78.6).
WER competitive at 1.84, better than almost everything except Qwen3-TTS (1.23) and Fish S2 (0.99).

---

## MiniMax Multilingual Test (24 languages)

### Intelligibility (WER↓)

| Language | MiniMax | ElevenLabs | Qwen3-TTS | Fish S2 | **VoxCPM2** |
|----------|:------:|:--------:|:--------:|:------:|:----------:|
| Chinese | 2.25 | 16.03 | 0.93 | **0.73** | 1.14 |
| **Indonesian** | **1.24** | 1.06 | - | 1.46 | 1.08 |
| **Japanese** | 3.52 | 10.65 | - | **2.76** | 4.63 |
| Korean | 1.75 | 1.87 | - | **1.37** | 1.09 |
| English | 2.16 | 2.34 | **0.93** | 1.62 | 2.29 |
| Arabic | **1.67** | 1.67 | - | 3.50 | 13.05 |

### Speaker Similarity (SIM↑)

| Language | MiniMax | ElevenLabs | Qwen3-TTS | Fish S2 | **VoxCPM2** |
|----------|:------:|:--------:|:--------:|:------:|:----------:|
| Chinese | 78.0 | 67.7 | 79.9 | 81.6 | **82.5** |
| **Indonesian** | 72.9 | 66.0 | - | 76.3 | **80.0** |
| **Japanese** | 77.6 | 73.8 | - | 79.6 | **82.8** |
| Korean | 77.1 | 69.2 | - | 78.6 | **83.8** |
| English | 75.6 | 61.3 | 77.5 | 79.7 | **85.4** |
| French | 62.8 | 53.5 | 62.8 | 69.8 | **73.5** |
| German | 73.3 | 61.4 | 77.5 | 76.7 | **80.3** |
| Dutch | 73.8 | 68.0 | - | 73.0 | **80.8** |
| Finnish | 83.5 | 75.9 | - | 81.9 | **89.0** |

**Key takeaway**: VoxCPM2 SIM **#1** in nearly every language tested. Beats ElevenLabs by massive margins (e.g., English 85.4 vs 61.3).

---

## Internal 30-Language Benchmark (vs Fish S2 Pro)

Evaluated using Gemini 3.1 Flash Lite ASR, 500 samples per language.

| Language | Metric | VoxCPM2 | Fish S2 Pro |
|----------|--------|:------:|:----------:|
| en | WER | **0.42%** | 1.03% |
| **id (Indonesian)** | WER | **1.36%** | 1.68% |
| **ja (Japanese)** | CER | 2.40% | **1.82%** |
| zh (Chinese) | CER | **0.92%** | 1.02% |
| ko (Korean) | CER | 0.95% | **0.29%** |
| th (Thai) | CER | **0.94%** | 1.92% |
| vi (Vietnamese) | WER | **1.56%** | 5.56% |
| he (Hebrew) | CER | **2.98%** | 15.27% |
| km (Khmer) | CER | **2.05%** | 75.15% |
| my (Burmese) | CER | **1.42%** | 85.27% |
| Average (30 lang.) | | **~1.68%** | - |

**Key takeaway**: VoxCPM2 consistently better on low/mid-resource languages. Fish S2 struggles badly on Khmer, Burmese, Lao, Hebrew, Vietnamese — possible training data gaps.

---

## InstructTTSEval (Voice Design)

| Model | APS↑ (ZH) | DSD↑ (ZH) | RP↑ (ZH) | APS↑ (EN) | DSD↑ (EN) | RP↑ (EN) |
|-------|:------:|:------:|:------:|:------:|:------:|:------:|
| **VoxCPM2** | **85.2** | 71.5 | 60.8 | **84.2** | **83.2** | **71.4** |
| Qwen3-TTS | 83.0 | 77.8 | 61.2 | 77.3 | 77.1 | 63.7 |
| GPT-4o-mini-tts | 54.9 | 52.3 | 46.0 | 76.4 | 74.3 | 54.8 |
| Gemini-pro | 89.0 | 90.1 | 75.5 | 87.6 | 86.0 | 67.2 |

**Key takeaway**: VoxCPM2 leads on English voice design (APS 84.2, RP 71.4), competitive with Gemini on Chinese.

---

## Indonesian + Japanese Head-to-Head

### Indonesian

| Model | WER↓ | SIM↑ | License |
|-------|:----:|:----:|---------|
| **VoxCPM2** | 1.36% | **80.0%** 🥇 | Apache 2.0 |
| OmniVoice | 1.97% | 80.5% 🥈 | Apache 2.0 |
| Fish S2 Pro | 1.68% | 76.3% | Research |
| ElevenLabs | 1.06% | 66.0% | Commercial |
| MiniMax | 1.24% | 72.9% | Commercial |

### Japanese

| Model | CER↓ | SIM↑ | License |
|-------|:----:|:----:|---------|
| **VoxCPM2** | 2.40% | **82.8%** 🥇 | Apache 2.0 |
| OmniVoice | 4.03% | 82.8% 🥇 | Apache 2.0 |
| Fish S2 Pro | **1.82%** 🥇 | 79.6% | Research |
| ElevenLabs | 10.65% | 73.8% | Commercial |
| MiniMax | 3.52% | 77.6% | Commercial |

### Best Picks

| Criteria | Model |
|----------|-------|
| SIM Indonesia #1 | VoxCPM2 (80.0%) |
| SIM Jepang #1 | VoxCPM2 & OmniVoice (tie 82.8%) |
| WER Indonesia #1 | Minimax (1.24%) — but proprietary |
| CER Jepang #1 | Fish S2 Pro (1.82%) — but Research License |
| **Best overall Indo+JP open-source** | **VoxCPM2** |

---

## Hardware Benchmark (Strix Halo CPU, no GPU)

| Config | RTF | Output Rate | VRAM |
|--------|:---:|:-----------:|:----:|
| VoxCPM2 Python, 5 timesteps | 1.06-1.25 | 48kHz | ~2.5GB |
| VoxCPM2 Python, 10 timesteps | 1.58-1.93 | 48kHz | ~2.5GB |
| VoxCPM.cpp (VoxCPM1.5 Q8_0) | 1.23 | 44.1kHz | ~1GB |
| OmniVoice, 8 steps, voice design | 0.56 | 16kHz | ~3GB |
| OmniVoice, 8 steps, voice clone | 1.52 | 16kHz | ~3GB |

Source: [sleepingrobots.com](https://sleepingrobots.com/dreams/voxcpm-strix-halo/)
