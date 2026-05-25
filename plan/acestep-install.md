# ACE-Step 1.5 — Install Plan (12 GB / RTX 5070)

- **Status**: done
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
| Backend | `pt` | ⚠️ vllm tidak support Windows, fallback ke pt |

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

---

## 🆕 Rencana Install untuk RTX 5070 12 GB

### Yang dipilih: 2B turbo + 1.7B LM (~12 GB total)

### Changelog
| Tanggal | Update |
|---------|--------|
| 2026-05-24 | **Installed!** ACE-Step 1.5 di `E:\AI\ACE-Step-1.5\`. |
| 2026-05-24 | Research selesai. Ready to install. |

### Langkah install

1. Clone & install 
2. Pastikan di E drive
3. Tes generasi lirik Jepang
4. Tes generasi lirik Indonesia
5. Update doc dengan hasil

### Pertanyaan yang perlu dijawab

| # | Pertanyaan | Status |
|---|-----------|--------|
| 1 | Berapa actual size setelah install? | Belum |
| 2 | Indonesian lyrics berfungsi? | Belum |
| 3 | Kualitas vocal vs Suno? | Belum |
| 4 | Speed generation di RTX 5070? | Belum |
| 5 | Bisa pake venv existing sound-plan? | Cek nanti |

### Catatan

- Install ke `E:\AI\ACE-Step-1.5\` (bukan di dalam sound-plan)
- Model auto-download ke `checkpoints/` di folder project
- GPU auto-detect, Tier 4 (11.94 GB, CPU offload otomatis)
- LM 1.7B via pt backend (vllm tidak support Windows)
- Batch generation: 4 sekaligus
- Max duration: 8 menit (LM) / 10 menit (DiT only)
- **ffmpeg wajib di PATH** untuk export MP3

---

## Installation Result (2026-05-24)

| Item | Detail |
|------|--------|
| Location | E:\AI\ACE-Step-1.5\ |
| Python | 3.12.13 (uv-managed venv, 6 GB) |
| GPU detected | RTX 5070, 11.94 GB, Tier 4 (CPU offload auto) |
| DiT Model | acestep-v15-turbo (4.5 GB) |
| LM Model | acestep-5Hz-lm-1.7B (3.5 GB) |
| VAE | 0.3 GB |
| Qwen3-Embedding | 1.1 GB |
| **Total install** | **15.5 GB** |

### Launch

```powershell
# Double-click:
E:\AI\sound-plan\apps\acestep-gradio\run.bat

# Or from terminal:
cd E:\AI\ACE-Step-1.5
uv run acestep --port 7860 --debug
# → http://localhost:7860
```

Or gunakan shortcut di `apps/acestep-gradio/run.bat` — otomatis kill port 7860 + set PATH ffmpeg.

### Required: `.env` Configuration

Buat `E:\AI\ACE-Step-1.5\.env` dengan isi:

```env
ACESTEP_CONFIG_PATH=acestep-v15-turbo
ACESTEP_LM_MODEL_PATH=acestep-5Hz-lm-1.7B
ACESTEP_LM_BACKEND=pt
ACESTEP_DEVICE=auto
ACESTEP_INIT_LLM=auto
```

**PENTING**: `ACESTEP_LM_BACKEND=pt` — karena vllm tidak support Windows. Tanpa ini, generation error.

### Prerequisites: ffmpeg

ffmpeg harus ada di PATH. Sudah tersedia di:
- `E:\AI\ComfyUI\ffmpeg-8.1-essentials_build\bin\ffmpeg.exe`
- Atau `E:\AI\GPT-SoVITS\ffmpeg.exe`

`run.bat` sudah otomatis set PATH ke ffmpeg ComfyUI.

### Test Results

| Test | Status | Notes |
|------|:------:|-------|
| Japanese lyrics | ⏳ Todo | UI sudah running, model loading OK |
| Indonesian lyrics | ⏳ Todo | Perlu test |
| Speed benchmark | ⏳ Todo | - |
| Sound quality vs Suno | ⏳ Todo | - |

### Known Issues

| Issue | Workaround |
|-------|-----------|
| vllm tidak support Windows | Set `ACESTEP_LM_BACKEND=pt` di .env |
| ffmpeg required for MP3 | Tambah PATH ke run.bat atau global |
| CPU offload otomatis (VRAM <20GB) | Tidak bisa di-disable di Tier 4, generation lebih lambat |
| LM model list show `0.6B` tapi kita punya `1.7B` | Minor, GPU config list hardcoded; .env sudah benar |
