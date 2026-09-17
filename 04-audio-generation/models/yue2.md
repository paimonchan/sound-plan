# YuE2

- **Paper (YuE v1)**: [arXiv 2503.08638](https://arxiv.org/abs/2503.08638) (Mar 11, 2025)
- **Paper (YuE2)**: Coming soon
- **Repo**: <https://github.com/multimodal-art-projection/YuE> (YuE v1 di branch `YuE-v1`)
- **Model Weights**: <https://huggingface.co/m-a-p/YuE2-3B>
- **Project Page**: <https://map-yue2.github.io/>
- **Demo / Benchmark**: <https://huggingface.co/datasets/m-a-p/WildSongBench>
- **Status**: reviewed
- **Added**: 2026-09-13

---

## Overview

YuE2 (乐2) adalah open music generation model dari **M-A-P (Multimodal Art Projection)** — kolaborasi dengan HKUST, Tokenwave.AI, MBZUAI, ACE Studio, NYU, Stanford, NOIZ. Dirilis **10 Sep 2026**.

Fitur pembeda: **symbolic planning** — model menulis **skor ABC notation dulu** (melodi + chord yang bisa dibaca/diedit), baru dirender jadi lagu penuh (vokal + instrumen) 48 kHz stereo. Menyaingi Suno v5/v6 pada WildSongBench.

Tiga kemampuan dari satu checkpoint:
- **Create** — lyrics + style prompt → skor → full song
- **Cover (zero-shot)** — transkripsi rekaman sumber via SheetSage2 → aransemen/interpretasi baru
- **Agentic editing** — feedback musikal → revisi skor/style/lyric → render ulang

## Architecture

- **Params**: ~3.59B, 28 layer
- **Backbone**: AR–NAR Mixture-of-Transformers (AR & NAR expert berbagi attention, terpisah di normalization/projection/MLP)
- **Pipeline**: skor ABC → semantic music tokens (25 Hz) → acoustic latents via **flow matching** → VAE decoder → 48 kHz stereo
- **Staged Python API**: `plan()` → `generate_semantic()` → `synthesize()` → `decode()`

## Generation Modes

| Setting | Behavior |
|---------|----------|
| `cot="full"` | Melody + chord plan (default, lagu baru) |
| `cot="melody"` | Melody-only plan, accompaniment bebas — direkomendasikan untuk cover |
| `cot="off"` | Langsung dari lyrics + style, tanpa symbolic plan |
| `abc=...` | Pakai skor sendiri (full/melody mode) |
| `cfg_scale=1.2` | Text guidance lebih kuat |

## Benchmarks — WildSongBench (192 prompt, 12 Sep 2026)

| System | SongBench Avg ↑ | AudioBox PQ ↑ | MuLan ↑ | PER ↓ |
|--------|:--------------:|:-------------:|:-------:|:-----:|
| **YuE2 (best-of-8)** † | **6.9632** | 8.2714 | 0.5051 | 9.79% |
| Mureka 9 | 6.9377 | 8.0226 | 0.4394 | 11.69% |
| Suno v5 | 6.8721 | 8.1698 | **0.5428** | 8.10% |
| **YuE2** † | 6.7316 | 8.2598 | 0.5068 | 8.44% |
| Suno v5.5 | 6.7150 | 8.1955 | 0.5089 | 5.96% |
| Suno v4.5 | 6.6995 | 8.2541 | 0.5022 | **5.80%** |
| Suno v6 | 6.5562 | 8.1296 | 0.4916 | 7.58% |
| LeVo 2 (SongGeneration) † | 6.3247 | **8.3966** | 0.3542 | 26.12% |
| MiniMax Music 2.6 | 6.3222 | 8.1711 | 0.4251 | 24.55% |
| HeartMuLa † | 6.2483 | 8.2933 | 0.3823 | 10.71% |
| Muse † | 6.0349 | 8.0517 | 0.3937 | 33.42% |
| **ACE-Step 1.5** † | 6.0118 | 8.0518 | 0.4372 | 7.46% |
| DiffRhythm 2 † | 5.2428 | 7.9782 | 0.3782 | 18.41% |
| YuE 1 † | 4.9165 | 7.8683 | 0.2623 | 36.38% |

† = public weights. YuE2 standard pilih 2 kandidat; best-of-8 pilih 8. Benchmark pakai decoder `YuE2-Vae-legacy`.

**Zero-shot cover**: **0.647 CLEWS mAP** pada 948 karya (vs 0.006 tanpa skor) — tanpa fine-tuning cover-specific.

## Companion Models

| Resource | Purpose |
|----------|---------|
| [YuE2-3B](https://huggingface.co/m-a-p/YuE2-3B) | Song generation, planning, cover, editing (7.3 GB) |
| [YuE2-Vae](https://huggingface.co/m-a-p/YuE2-Vae) | Decoder default (perceptual quality lebih baik) |
| [YuE2-Vae-legacy](https://huggingface.co/m-a-p/YuE2-Vae-legacy) | Decoder reproduksi benchmark |
| [SheetSage2](https://huggingface.co/m-a-p/SheetSage2) | Audio-to-score transcription (encoder MERT2) |
| [MERT-v2-FullSong](https://huggingface.co/m-a-p/MERT-v2-FullSong) | Full-song music representations |
| [MERT-v2-30s](https://huggingface.co/m-a-p/MERT-v2-30s) | Short-recording representations |

- **MERT2**: SOTA 14/15 metrik MARBLE, 91.72% genre accuracy GTZAN
- **SheetSage2**: SOTA 10/13 metrik, 82.51% vocal melody pitch-class F1 RWC-Pop
- **Agent skill**: `skills/yue2-music/SKILL.md` (generate, cover, edit ABC, cek invariant musikal)

## Quickstart

Prasyarat resmi: **Linux · Python 3.12 · NVIDIA GPU BF16 24 GB**. Output 48 kHz stereo tanpa kuantisasi.

```bash
git clone https://github.com/multimodal-art-projection/YuE.git
cd YuE
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
python examples/generate.py --output outputs/first-song
```

```python
import json
from pathlib import Path
from yue2 import YuE2Pipeline

request = json.loads(Path("examples/song.json").read_text(encoding="utf-8"))
with YuE2Pipeline.from_pretrained("m-a-p/YuE2-3B", device="cuda") as pipe:
    song = pipe(**request)
    song.save_artifacts("outputs/my-song")
```

## Hardware

| Metric | Value |
|--------|-------|
| VRAM resmi | 24 GB (BF16) |
| Peak terukur (RTX 4090) | ~11–14 GiB |
| Speed (RTX 4090) | 214.85s lagu dalam 71.04s |
| Output | 48 kHz stereo |
| OS | Linux (quickstart resmi) |
| RTX 5070 12 GB | ⚠️ Tight — peak 4090 ~11-14 GiB, belum tentu muat tanpa offload |

## Pros & Cons

**+ Strengths**
- Kualitas frontier — menyaingi Suno v5/v6; **SongBench Avg tertinggi** (best-of-8)
- **White-box**: skor ABC bisa dibaca, diedit, dan dipakai sebagai kontrol
- Zero-shot cover (0.647 CLEWS mAP) + agentic editing dalam satu checkpoint
- 48 kHz stereo tanpa kuantisasi; ekosistem lengkap (MERT2, SheetSage2, benchmark)
- Agent skill siap pakai

**- Weaknesses**
- **Lisensi bobot CC BY-NC 4.0 (non-komersial)** — beda dari YuE v1 yang Apache 2.0
- Laporan teknis YuE2 "coming soon"
- Quickstart resmi Linux (Windows belum didukung)
- Butuh 24 GB VRAM resmi; di 12 GB kemungkinan perlu offload/kuantisasi
- Editing menghasilkan rekaman baru (bukan waveform-preserving)

## Fine-tuning / LoRA (komunitas, 16 Sep 2026)

M-A-P **belum merilis training code YuE2** (yang ada di repo hanya `finetune/` untuk YuE v1). Komunitas menutup celah ini: user `Mothersuperior` (Reddit `thatisnotmychapstick`) merilis **encoder audio→semantic-token** yang tidak diship M-A-P, plus LoRA NAR + script training. Trik: YuE2 "mengajari dirinya sendiri" — tiap lagu hasil generate membawa token persisnya (data berlabel gratis), lalu decoder YuE2 dipakai menilai encoder pada audio nyata.

| Repo | Isi |
|------|-----|
| [yue2-mothersuperior-realaudio-tokenizer-v4](https://huggingface.co/Mothersuperior/yue2-mothersuperior-realaudio-tokenizer-v4) | Encoder head (MERT-v2-FullSong layer-20 → 32.768 kode YuE2, 25 Hz) + NAR LoRA + scripts (v4 → v5 → v8/v9) |
| [YuE2-instrumental-cot-full-loras](https://huggingface.co/Mothersuperior/YuE2-instrumental-cot-full-loras) | LoRA **instrumental** (~2.700 track, 100+ genre, ABC ber-chord; pakai `cot=full`) |
| [YuE2-hum-to-song](https://huggingface.co/Mothersuperior/YuE2-hum-to-song) | Adapter hum → full song |
| [yue2-minted-corpus](https://huggingface.co/datasets/Mothersuperior/yue2-minted-corpus) | Regularizer pack (~4.732 lagu YuE2) — **wajib** untuk AR training |
| [YuE2-Vae-merge-0.666](https://huggingface.co/Mothersuperior/YuE2-Vae-merge-0.666) | Merge decoder Vae(0.666)/legacy(0.334) |

### Ukuran file (yang relevan)

| File | Size |
|------|-----:|
| `tokenizer_head_joint_v9.bf16.safetensors` | 81.7 MiB |
| `tokenizer_head_joint_v9.safetensors` (fp32) | 163.3 MiB |
| `nar_lora_joint_v9.bf16.safetensors` | 67.0 MiB |
| `nar_lora_joint_v9.safetensors` (fp32) | 134.0 MiB |
| `nar_lora_joint_v9_comfyui.safetensors` | 102.5 MiB |
| `regularizer/minted_regularizer_pack.pt` | 97.2 MiB |
| `ar_lora_inst_v3abc_comfyui.safetensors` | 203.0 MiB |
| `ar_lora_inst_v3abc.bf16.safetensors` | 133.0 MiB |
| `humsong_yue2_adapter_v1_comfy.safetensors` | 307.6 MiB |

**Minimum untuk train artist LoRA**: head (81.7 MiB bf16) + NAR LoRA (67.0 MiB bf16) + regularizer pack (97.2 MiB) ≈ **~246 MiB**, plus base model (YuE2-3B 7.3 GB, YuE2-Vae, MERT-v2-FullSong) yang di-download otomatis.
**Untuk ComfyUI saja** (pakai LoRA jadi, tanpa training): cukup file `*_comfyui.safetensors` — mis. instrumental LoRA 203 MiB.

### Keamanan

- ✅ **`.safetensors`** aman (tensor-only, tidak bisa eksekusi kode). Varian `_comfyui.safetensors` juga aman.
- ⚠️ **`.pt`** berbasis **pickle** → `torch.load` bisa menjalankan kode arbitrer. Hindari `.pt` dari sumber tak dipercaya; utamakan `.safetensors` (isi bobotnya bit-identik fp32). Catatan: `minted_regularizer_pack.pt` juga `.pt`.
- ⚠️ **`scripts/`** = Python biasa — baca dulu sebelum jalankan; mengunduh model Demucs/MMS, path-nya hard-coded ke layout pod penulis (harus diedit).
- Sampai sekarang **tidak ada laporan malware**; rilis komunitas baru (126 likes), reproduce dalam hitungan jam. Tetap: jalankan di venv terpisah, jangan as-admin, scan Defender.
- Lisensi tetap **CC BY-NC 4.0** (turunan YuE2-3B) → LoRA hasil training pun non-komersial.

### Training — VRAM & waktu

- **VRAM**: README menyatakan **24 GB cukup untuk semua tahap**; terukur **14–18 GB** dengan gradient checkpointing. → **RTX 5070 12 GB kita kemungkinan OOM** (training lokal tidak realistis tanpa trik).
- **Jumlah step** (bukan waktu): joint head+NAR adapt **3.000 step**; **AR LoRA artist 1.600 step** (jangan > ~1.500–2.000 → mulai menghafal lagu); head v5 retrain **30.000 step** pada 14.547 track.
- **Wall-clock tidak dipublikasikan.** Skala jam di GPU 24 GB (bukan menit). Perlu diukur sendiri.
- Alur: `prep_real.py` → `cursor_prep.py` → (opsional) `joint.py 3000` → `ar_prep.py` → `ar_lora_cursor.py` (rank-64) → `ladder.sh` (pilih checkpoint by ear). Butuh Demucs + MMS alignment + MERT + VAE latents.
- Per lagu: `.flac` + `.lyrics.txt` (lirik lengkap bertag seksi) + `.txt` (caption style dengan trigger phrase).

### ComfyUI

- Konversi `drbaph` + node pack komunitas **`ComfyUI-YuE2-Trainer`** (masih eksperimental, 1 orang).
- `nar_lora_joint_v*_comfyui.safetensors` → load via **LoraLoader** di output **MODEL** (strength 1.0).
- `ar_lora_inst_v3abc_comfyui.safetensors` → load di output **CLIP** (AR planner ada di slot CLIP); wajib `mode=full` + ABC node terhubung.

## Related in this KB

- `plan/song-generation-2026.md`
- `plan/song-creation-guide.md`
