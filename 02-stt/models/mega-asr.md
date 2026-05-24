# Mega-ASR

- **Paper**: [arXiv 2605.19833](https://arxiv.org/abs/2605.19833) (May 19, 2026)
- **Repo**: <https://github.com/xzf-thu/Mega-ASR>
- **Model**: <https://huggingface.co/zhifeixie/Mega-ASR>
- **License**: Apache 2.0
- **Status**: todo
- **Added**: 2026-05-24

---

## Overview

Mega-ASR is a robust ASR system specialized for **severely degraded audio** — noisy, reverberant, clipped, overlapping speech where standard ASR (Whisper, Qwen3-ASR) often produces empty output, omissions, or hallucinations.

Built on Qwen3-ASR-1.7B backbone with:

- **Voices-in-the-Wild-2M** dataset: 7 acoustic phenomena, 54 compound scenarios
- **Acoustic-to-Semantic Progressive SFT**: trained on progressively harder examples
- **Dual-Granularity WER-Gated Policy Optimization**
- **Audio Quality Router**: auto-decides whether to use robust or clean path

## Benchmarks

| Benchmark | Prior SOTA | Mega-ASR |
|-----------|:--------:|:------:|
| VOiCES R4-B-F (noise) | 54.01% | **45.69%** |
| NOIZEUS Sta-0 (noise) | 29.34% | **21.49%** |
| Compound acoustic scenarios | baseline | **30%+ relative WER reduction** |

## Key Difference vs Whisper

| | Whisper | Mega-ASR |
|---|:---:|:---:|
| Clean audio | ✅ Best | ✅ Comparable (via router) |
| Noisy/degraded audio | ❌ Hallucinates | ✅ Designed for this |
| Languages | 99+ | Depends on Qwen3 ASR backbone |
| Auto-routing | ❌ | ✅ Built-in quality router |

## TODO

- [ ] Deep dive into architecture details
- [ ] Test with Indonesian audio samples
- [ ] Compare vs Whisper turbo on real-world YouTube audio
- [ ] Check if router quality threshold can be tuned
- [ ] Integrate into training data transcription pipeline
