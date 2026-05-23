# AI Song & Singing Voice — Deep Dive 2026

- **Status**: in-progress
- **Added**: 2026-05-23

---

## Singing Voice Synthesis (SVS)

### 1. SoulX-Singer ⭐ 578 — RECOMMENDED

- **Repo**: `Soul-AILab/SoulX-Singer` | **Feb 2026**
- **Paper**: arXiv 2602.07803
- **License**: Apache 2.0
- **VRAM**: ~8-12 GB

| Feature | Detail |
|---------|--------|
| Zero-shot singing | ✅ No fine-tuning |
| Control modes | F0 melody + MIDI score |
| Languages | Mandarin, English, Cantonese |
| Dataset | 42,000+ hours aligned vocals+lyrics+notes |
| Timbre cloning | ✅ Across languages |
| Singing voice conversion (SVC) | ✅ Audio-to-audio, no transcription needed |
| HuggingFace demo | ✅ Live Space |

### 2. YingMusic-Singer-Plus ⭐ 39

- **Repo**: `ASLP-lab/YingMusic-Singer-Plus` | **Mar 2026**
- **License**: CC BY 4.0
- **Architecture**: Diffusion-based (F5-TTS backbone + Stable Audio 2 VAE)

| Feature | Detail |
|---------|--------|
| Lyric editing | 6 modes: change, insert, delete, translate (CN↔EN), code-switch |
| Melody from audio | No MIDI alignment needed |
| Output | 44.1 kHz stereo |
| Params | ~727M |
| HuggingFace demo | ✅ Live Space |

### 3. SongEcho (ICLR 2026) ⭐ 53

- **Repo**: `lsfhuihuiff/SongEcho_ICLR2026` | **Feb 2026**
- **Paper**: arXiv 2602.19976 (ICLR 2026)
- **License**: -

Cover song generation: preserves original melody, changes style/vocalist/accompaniment via text prompt.

### 4. DiffSinger (OpenVPI) ⭐ 3,000 — Community standard

- **Repo**: `openvpi/DiffSinger` | **Ongoing**
- **License**: Apache 2.0
- **Output**: 44.1 kHz

Production-ready SVS with OpenUTAU integration. De facto standard untuk komunitas synthesis di China/Japan.

---

## Full Song Generation (Music + Vocals)

### 5. SongGeneration v2 / LeVo 2 (Tencent) ⭐ 340+ — RECOMMENDED

- **Repo**: `tencent-ailab/SongGeneration` | **Mar 2026**
- **License**: Open-source (check repo)
- **VRAM**: 22-28 GB (v2-large)

| Feature | Detail |
|---------|--------|
| Max length | 4 min 30 sec |
| Languages | zh, en, es, ja, etc. (v2) |
| PER | **8.55%** — beats Suno v5 (12.4%), Mureka v8 (9.96%) |
| Quality | Rivals top closed-source (MiniMax 2.5) per 20 music pros |
| Modes | Full song, pure music, vocal-only, dual-track |
| GPU (H20) | RTF 0.82 |

### 6. Khala ⭐ 8 — New

- **Repo**: `Khala-Music-AI/Khala` | **Apr 2026**
- **Paper**: arXiv (May 2026)
- **License**: CC BY-NC 4.0
- **VRAM**: 24 GB+ (RTX 4090 recommended)

Unified acoustic-token, 64-layer RVQ. Full stack: frontend + FastAPI + worker. Too new, not production ready yet.

---

## Commercial (Closed Source)

| Service | Launched | PER | Key Edge |
|---------|:--------:|:---:|----------|
| **ElevenLabs Music** | Aug 2025 | - | Commercial licensed, Kobalt/Merlin deals |
| **Suno v5** | ~2025 | 12.4% | Biggest community, 397K Discord |
| **Udio** | ~2024 | - | Remixing + exploration focus |
| **Mureka v8** | ~2025 | 9.96% | Web-based, fast generation |
| **MiniMax Music 2.5** | Jan 2026 | - | Professional-grade, 14 structural tags |

---

## All-in-one Suites

| Tool | Stars | License | Key Feature |
|------|:-----:|---------|-------------|
| **HeartMuLa Studio** | 527 | MIT | Suno-like UI, React+FastAPI, LoRA training planned |
| **SlunderStudio** | 2 | MIT | ACE-Step + DiffSinger + RVC + Demucs, full offline |

---

## Benchmark Comparison

| Model | PER↓ | Quality | Open Weights | Best For |
|-------|:----:|:------:|:-----------:|----------|
| SongGeneration v2 | **8.55%** | Commercial-grade | ✅ | Full song, all languages |
| SoulX-Singer | - | High | ✅ Apache 2.0 | Singing voice, zero-shot |
| YingMusic-Singer | - | High | ✅ | Lyric editing, melody preserve |
| Suno v5 | 12.4% | Good | ❌ | Creative exploration |
| Mureka v8 | 9.96% | Good | ❌ | Fast web generation |

---

## Recommendation by Use Case

| Use case | #1 Pick | #2 Pick |
|----------|---------|---------|
| **Generate full song (vocal+music)** | SongGeneration v2 | HeartMuLa Studio |
| **Singing voice from text** | SoulX-Singer | DiffSinger |
| **Singing voice conversion (audio→audio)** | SoulX-Singer-SVC | RVC v2 |
| **Edit lyrics while keeping melody** | YingMusic-Singer | - |
| **Cover song (different style)** | SongEcho | SoulX-Singer |
| **All offline, local** | SlunderStudio | HeartMuLa Studio |

---

## What Works with Your RTX 5070 (12 GB)

| Model | VRAM | Status |
|-------|:----:|:------:|
| SoulX-Singer | 8-12 GB | ✅ Feasible |
| DiffSinger | ~4 GB | ✅ Easy |
| SongGeneration v2-medium | 12-18 GB | ⚠️ Tight (coming soon) |
| SongGeneration v2-large | 22-28 GB | ❌ Too big |
| YingMusic-Singer | 8-12 GB | ✅ Feasible |

---

## Next Steps

1. **SoulX-Singer** — most promising. Apache 2.0, 578 stars, zero-shot, SVC mode, HuggingFace demo live.
2. **SongGeneration v2-medium** — wait for release (12-18 GB VRAM target fits RTX 5070).
3. **DiffSinger** — if you want OpenUTAU integration for vocal synth workflow.
