# ACE-Step 1.5 — Install Plan

- **Status**: in-progress
- **Added**: 2026-05-24

---

## Overview

ACE-Step 1.5 — **10.4K★ MIT**, full song generation (vocal + music) dari text prompt + lirik.

## Model Variants

### DiT Models (music generation)

| Model | Size (disk) | Steps | Quality | Fit RTX 5070? |
|-------|:---------:|:-----:|:-------:|:------------:|
| `acestep-v15-turbo` (2B) | ~4.7 GB | 8 | Very High | ✅ Auto (no offload) |
| `acestep-v15-sft` (2B) | ~4.7 GB | 50 | High | ✅ |
| `acestep-v15-xl-turbo` (4B) | **18.8 GB** | 8 | Very High | ⚠️ Offload+INT8 |
| `acestep-v15-xl-sft` (4B) | 18.8 GB | 50 | Very High | ❌ 20GB+ |

### LM Models (lyrics understanding, CoT planner)

| Model | VRAM | Kualitas |
|-------|:----:|---------|
| `acestep-5Hz-lm-0.6B` | ~0.5 GB | Basic |
| `acestep-5Hz-lm-1.7B` | ~1.5 GB | Good (recommended) |
| `acestep-5Hz-lm-4B` | ~4 GB | Best |

### Rekomendasi untuk RTX 5070 (12 GB, Tier 5):

| Komponen | Pilihan | Alasan |
|----------|---------|--------|
| DiT | `acestep-v15-turbo` (2B) | 8 steps, Very High quality, no offload |
| LM | `acestep-5Hz-lm-1.7B` | Best fit for 12 GB |
| Backend | `vllm` | Auto-selected |

**XL (4B) bisa dicoba dengan offload+INT8** — works on 12 GB tapi performance lebih lambat.

---

## Storage Requirements

| Skenario | Komponen | Download | + Venv | Total |
|----------|----------|:------:|:-----:|:----:|
| **Minimal** (2B turbo) | Main bundle | ~8 GB | 3 GB | **~11 GB** |
| **Recommended** (2B + 1.7B LM) | Main + LM | ~8 GB | 4 GB | **~12 GB** |
| **Full XL** (4B + 4B LM) | XL bundle | ~27 GB | 5 GB | **~32 GB** |

**Main bundle** includes: VAE, Qwen3-embedding (0.6B), acestep-v15-turbo (2B), acestep-5Hz-lm-1.7B.

---

## Installation

### Windows (easiest)

```powershell
# 1. Install uv package manager
irm https://astral.sh/uv/install.ps1 | iex

# 2. Clone & install
git clone https://github.com/ACE-Step/ACE-Step-1.5.git "E:\AI\ACE-Step-1.5"
cd E:\AI\ACE-Step-1.5
uv sync

# 3. Launch (models auto-download first run ~8 GB)
uv run acestep
# → http://localhost:7860
```

### Or portable package

Download `ACE-Step-1.5.7z` → extract → run `start_gradio_ui.bat`.

---

## What You Can Do

| Feature | How |
|---------|-----|
| **Full song from prompt** | Text description → complete song with vocals |
| **Lyric-to-song** | [Verse] [Chorus] [Bridge] tags |
| **Cover/remix** | Upload song → change style |
| **Repaint** | Fix specific section of a track |
| **Instrumental only** | `[Instrumental]` tag in lyrics |
| **Batch generate** | 4-8 variasi sekaligus, pilih terbaik |
| **LoRA personalization** | Train with few songs for custom style |

### Example prompt

```yaml
Caption: "J-pop idol song, energetic, female vocal, 140 BPM"
Lyrics:
  [Verse 1]
  朝日が昇る街角で
  新しい一日が始まる

  [Chorus]
  走り出せ！今すぐに！
  夢を追いかけて！
```

---

## Indonesian Support

ACE-Step claims 50+ languages via lyrics. **Indonesia tidak di top 19**, tapi mungkin berfungsi — perlu di-test. Cara: generate 5-10x dengan lirik Indo, pilih yang paling bagus.

---

## Decision

| Opsi | Quality | VRAM | Install Size |
|------|:------:|:----:|:----------:|
| **A: 2B turbo** (auto-fit) | Between Suno v4.5-v5 | <4 GB | **~11 GB** |
| **B: XL turbo BF16** (offload) | Above Suno v5 | 12 GB | **~27 GB** |

**Rekomendasi**: Start dengan opsi A (2B turbo, ~11 GB). Kalau suka, upgrade ke XL later.
