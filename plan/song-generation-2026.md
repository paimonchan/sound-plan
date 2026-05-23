# AI Song & Singing Voice — Deep Dive 2026

- **Status**: reviewed (updated May 24)
- **Added**: 2026-05-23

---

## What People Actually Use (May 2026)

### Closed-source heavyweights (dominating mainstream)

| Platform | Users | Valuation | Best For | Price |
|----------|:-----:|:---------:|----------|:-----:|
| **Suno v4.5/v5** | ~100M | $2.4B | Full songs, fastest, viral trend | $10/mo |
| **Udio** | ~400K community | - | Best audio quality, producer tools | $10/mo |
| **ElevenLabs Music** | 11B parent | - | Commercial license-safe, API | $5-30/mo |
| **Mureka v8** | - | - | Fast web generation | Web |
| **MiniMax Music 2.5** | - | - | Professional vocals, 14 tags | API |

### Viral moments (2026)

- **April 2026**: TikTok "Texts to Song" trend — 8.6M views on first video, Suno used
- **May 2026**: "Puerto Rico Song" — 46K+ TikTok posts, Suno, called "song of the summer"
- **May 2026**: Spotify + UMG deal — AI covers/remixes for Premium subscribers
- **May 2026**: World Cup AI fan anthems — millions of plays
- **May 2026**: Deep Dream Generator AI track — compared to Beatles quality

### How people compare them

| | Suno v5 | Udio | ElevenLabs Music |
|---|:---:|:---:|:---:|
| **Vocals** | Best natural | Good (characteristic "shimmer") | Best realism, multilingual |
| **Instrumentals** | Great | **Best** — 48kHz, clean separation | Good, newer |
| **Speed** | **~40s** | Slower | Medium |
| **Editing** | Studio (timeline, stems) | **Best**: inpainting, extend | Section-level |
| **License safety** | Settled (WMG Nov 2025) | Settled (UMG) | **Cleanest** (licensed from start) |
| **Best genre** | Pop/Rock/Electronic | Jazz/Acoustic/Orchestral | Vocal-focused/Agency |

### Suno dominance explanation

Multiple independent reviewers tested all platforms in 2026. Key findings:
- **Suno v5 leads in overall quality (ELO 1293)** — most consistent across genres
- **People prefer their own Suno songs over Spotify artists** — a real behavioral shift
- **v5.5 quality regression**: users report "one-voice" collapse in April 2026
- Suno has massive community (397K Discord) driving iteration speed

## Open-Source Full Song Generation (Vocal + Music)

### 1. ACE-Step 1.5 ⭐ 10,400 — RECOMMENDED 🏆 #1

- **Repo**: `ace-step/ACE-Step-1.5`
- **Released**: Jan 28, 2026 | Latest: v0.1.7 (Apr 24, 2026)
- **License**: MIT
- **VRAM**: <4 GB (2B turbo), 7.5 GB (XL turbo BF16), 12-20 GB (XL 4B)

**Paper benchmarks — ACE-Step 1.5 XL BEATS Suno v5:**
| Metric | ACE-Step 1.5 | ACE-Step XL | Suno v5 |
|--------|:----------:|:---------:|:-----:|
| AudioBox PQ | 8.35 | **8.42** | 8.29 |
| AudioBox CU | 8.09 | 8.12 | 7.87 |
| Coherence | **4.72** | **4.79** | 4.72 |
| StyleAlign | 39.1 | **47.9** | 46.8 |
| LyricAlign | 26.3 | **35.8** | 34.2 |
| Human A/B | v4.5-v5 | **>v5** | v5 |

| Feature | Detail |
|---------|--------|
| Full song | ✅ Up to 10 min (600s) |
| Speed | **<10s on RTX 3090**, <2s on A100 |
| Languages | Any (lyrics in any language) |
| Modes | Full song, vocal-only, instrumental-only, dual-track |
| Personalization | LoRA from few songs |
| Hardware | CUDA, MPS (Mac), ROCm (AMD), Intel XPU, CPU |
| Studio app | ACE-Step-Studio (portable, one-click) |

**Best open-source Suno alternative.** MIT license. 70 contributors.

### 2. HeartMuLa ⭐ 3,500 — Apache 2.0

- **Repo**: `HeartMuLa/heartlib` | **Jan 2026**
- **License**: Apache 2.0
- **VRAM**: ~8-12 GB (3B)

| Feature | Detail |
|---------|--------|
| Claim | "Comparable performance with Suno" |
| Languages | Almost all languages |
| Lyrics | Best controllability among open-source |
| Model | 3B (7B planned) |
| Speed | RTF ~1.0 (realtime) |

### 3. YuE ⭐ 6,200 — Apache 2.0

- **Repo**: `multimodal-art-projection/YuE` | **Jan 2025**
- **License**: Apache 2.0

First open-source Suno-like model. 6.2K stars. Full song with vocals+accompaniment. Multiple genres, languages, vocal techniques. Needs 24GB+ VRAM for full song.

### 4. DiffRhythm ⭐ 2,300 — Apache 2.0

- **Repo**: `ASLP-lab/DiffRhythm` | **Mar 2025**
- **License**: Apache 2.0

First diffusion-based full song generator. 4m45s full-length. Text-to-music + instrumental mode. 8GB VRAM minimum.

### 5. SongGeneration v2 (LeVo 2) ⭐ 1,600

- **Repo**: `tencent-ailab/SongGeneration` | **Mar 2026**
- **PER**: 8.55% (beats Suno v5 12.4%)

Best lyric accuracy among all. 4B params. 22-28 GB VRAM. v2-medium (12-18 GB) coming soon.

### 6. Khala ⭐ 8 — CC BY-NC

- **Repo**: `Khala-Music-AI/Khala` | **Apr 2026**
- Too new, Docker-only, 24GB+ VRAM

### 7. Muse ⭐ 105 — MIT

- **Repo**: `yuhui1038/Muse` | **Jan 2026**
- Full dataset (116k songs) open-sourced. MIT license.

## Singing Voice (vocals only)

| Model | Stars | License | VRAM |
|-------|:-----:|---------|:----:|
| **SoulX-Singer** | 578 | Apache 2.0 | 8-12 GB |
| DiffSinger (OpenVPI) | 3,000 | Apache 2.0 | ~4 GB |
| SongEcho (ICLR 2026) | 53 | - | TBD |
| YingMusic-Singer | 39 | CC BY 4.0 | 8-12 GB |

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
| **ACE-Step-Studio** | - | MIT | Portable, one-click, Suno-at-home, 3 XL models |
| **HeartMuLa Studio** | 527 | MIT | Suno-like UI, React+FastAPI, LoRA training |
| **SlunderStudio** | 2 | MIT | ACE-Step + DiffSinger + RVC + Demucs |

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

| Model | VRAM | Status | Type |
|-------|:----:|:------:|------|
| **ACE-Step 1.5** (2B turbo) | <4 GB | ✅ Perfect fit | Full song |
| **ACE-Step 1.5** (XL turbo BF16) | 7.5 GB | ✅ | Full song |
| **HeartMuLa 3B** | ~10 GB | ✅ | Full song |
| **DiffRhythm** | 8 GB | ✅ | Full song |
| **YuE** | 24 GB rec. | ⚠️ Tight (exllamav2 helps) | Full song |
| SoulX-Singer | 8-12 GB | ✅ | Singing voice |
| DiffSinger | ~4 GB | ✅ | Singing voice |
| SongGeneration v2-large | 22-28 GB | ❌ | Full song |

---

## Recommendation — Open Source Full Song

| Use case | #1 Pick | #2 |
|----------|---------|-----|
| **Fastest, easiest** | **ACE-Step 1.5** (MIT, <10s, 10.4K★) | ACE-Step-Studio |
| **Best quality** | HeartMuLa (Apache 2.0, Suno-level) | SongGeneration v2 |
| **Lyric accuracy** | SongGeneration v2 (PER 8.55%) | HeartMuLa |
| **Low VRAM** | ACE-Step 1.5 2B (<4 GB) | DiffRhythm (8 GB) |
| **Singing voice only** | SoulX-Singer (Apache 2.0) | DiffSinger |

---

## Timeline — Key Releases 2025-2026

| Date | Model | Type | Impact |
|------|-------|------|--------|
| Jan 2025 | **YuE** | Full song | First open-source Suno-like (6.2K★) |
| Feb 2025 | **SongGen** | Full song | ICML 2025, single-stage (309★) |
| Mar 2025 | **DiffRhythm** | Full song | First diffusion full song (2.3K★) |
| Jun 2025 | **SongGeneration** | Full song | Tencent LeVo v1 (1.6K★) |
| Sep 2025 | **Suno v5** | Cloud | Major quality jump (100M users) |
| Jan 7 2026 | **Muse** | Full song | 116K songs open dataset (MIT) |
| Jan 14 2026 | **HeartMuLa** | Full song | "Comparable to Suno" (Apache 2.0) |
| **Jan 28 2026** | **ACE-Step 1.5** | Full song | **Game changer (MIT, 10.4K★)** |
| Feb 2 2026 | **SongEcho** | Cover | ICLR 2026 |
| Feb 6 2026 | **SoulX-Singer** | Singing | Zero-shot SVS (Apache 2.0) |
| Mar 1 2026 | **SongGeneration v2** | Full song | PER beats Suno (8.55%) |
| Mar 10 2026 | **YingMusic-Singer** | Lyric edit | GRPO alignment |
| Apr 20 2026 | **Khala** | Full song | Acoustic-token approach |
| Apr 24 2026 | **ACE-Step 1.5 v0.1.7** | Full song | Latest stable release |
| May 20 2026 | **Stable Audio 3.0** | Music/SFX | Stability AI open weights |
| May 21 2026 | **Spotify + UMG deal** | Industry | AI remix for Premium subscribers |
