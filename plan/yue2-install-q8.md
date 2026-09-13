# YuE2 — Install Plan (Q8 GGUF / audio.cpp, RTX 5070 12 GB)

- **Status**: done (installed & tested 2026-09-13)
- **Added**: 2026-09-13
- **Model**: YuE2-3B (M-A-P) — detail di `04-audio-generation/models/yue2.md`

---

## Kenapa Q8, bukan rute resmi BF16

Rute resmi YuE2 (PyTorch) minta **24 GB VRAM**, peak terukur **11.18 GiB** (normal) sampai **14.08 GiB** (max-context). Di RTX 5070 12 GB itu **rawan OOM**.

Rute kuantisasi via **audio.cpp** (C++ / ggml, tanpa Python):

| Combo | Peak VRAM (audio.cpp, RTX 5090) | RTF | Keputusan |
|-------|:-------------------------------:|:---:|-----------|
| BF16 + F32 VAE | 12,535 MiB | 0.2688 | ❌ terlalu besar utk 12 GB |
| **Q8_0 + F16 VAE** | **8,867 MiB** | 0.1992 | ✅ **dipilih** |
| Q4_0 + F16 VAE | 7,755 MiB | 0.1997 | ⚠️ cadangan (degradasi) |

## Hardware (terverifikasi)

| Item | Nilai mesin ini | Syarat | Status |
|------|-----------------|--------|:------:|
| GPU | RTX 5070 12 GB (12,227 MiB) | Q8 ~8.9 GB | ✅ |
| RAM | 32 GB | ~24 GB host RAM | ✅ |
| Driver | 610.47 | dukung CUDA 13.3 | ✅ |
| Disk E: | 91.8 GB free | ~6 GB | ✅ |
| CPU | Ryzen 7 5700X | — | ✅ |

## Hasil Test (2026-09-13)

| Metric | Hasil |
|--------|-------|
| Model | YuE2-3B Q8_0 + VAE F16 |
| Task | `gen`, `cot=off`, 8 inference steps |
| Output | **48 kHz stereo, 31.8s, PCM_16** (`first-song.wav`, 5.83 MB) |
| **Peak VRAM** | **5,921 MiB (5.78 GiB)** |
| Waktu generate | 18.6s (lagu 31.8s) |
| Backend | CUDA (RTX 5070, compute 12.0) |

Catatan: peak 5.78 GiB ini untuk lagu pendek (~32s). Lagu panjang (~3 menit) diperkirakan naik mendekati ~8.9 GiB (angka audio.cpp di RTX 5090), masih di bawah 12 GB.

## Storage

| Komponen | Size |
|----------|-----:|
| `bin/` (audio.cpp CUDA 13.3 + cudart) | 1,034 MB |
| `models/yue2/` (Q8 GGUF + VAE F16 + sidecars) | 4,322 MB |
| `outputs/` | ~6 MB |
| **Total** | **≈ 5.24 GB** |

## Layout (terpasang)

```
E:\AI\audio.cpp\
  bin\                     ← audiocpp_cli.exe, audiocpp_server.exe, ggml-cuda.dll, cudart DLL, model_specs\
  models\yue2\
    yue2-3b-q8_0.gguf      ← 3.97 GiB
    yue2-vae-f16.gguf      ← 247 MiB
    sidecars\              ← yue2-qwen.tiktoken, model/generation/vae config
  outputs\                 ← first-song.wav
```

## Sumber

- **Runtime**: audio.cpp — repo `0xShug0/audio.cpp`, **dev branch** (Yue2 belum masuk release stabil v0.7.4 per 2026-09-13).
  - Prebuilt Windows CUDA 13.3 dari GitHub Actions run `34642627647` (commit `fbe3e`, 2026-09-11): artifact `audio-v0.7.2-dev.fbe3e-bin-windows-x64-cuda13.3` + `-cudart-windows-x64-cuda13.3`.
  - Build ini terverifikasi mendukung `yue2` (ada `bin/model_specs/yue2.json`, loader `yue2`, `tools/community_models/yue2/convert_yue2_gguf.py`).
- **Model**: HF `audio-cpp/Yue2-3B-GGUF` (konversi dari `m-a-p/YuE2-3B`).

## Cara Pakai

```powershell
cd E:\AI\audio.cpp\bin
.\audiocpp_cli.exe --task gen --family yue2 --model "E:\AI\audio.cpp\models\yue2" `
  --backend cuda --threads 8 `
  --text "[Verse]`nSoft morning light is touching the window.`n[Chorus]`nStay with the rhythm." `
  --request-option "style=English, indie pop, bright acoustic guitar, soft drums, warm lead vocal" `
  --request-option cot=off --request-option seed=20260920 --request-option num_inference_steps=8 `
  --out "E:\AI\audio.cpp\outputs\song.wav" --log
```

- `cot=off` → langsung dari lirik+style. `cot=melody`/`full` → symbolic ABC planning (lebih lambat).
- Ganti file: `--session-option yue2.model_gguf=yue2-3b-q4_0.gguf` (bila ada).
- Semua default sudah cocok (Q8 + VAE F16), jadi `--session-option` tidak wajib.

## Risiko / Catatan

- **Dev branch**: belum stabil; release stabil v0.7.4 belum memuat Yue2.
- **Lisensi bobot**: **CC BY-NC 4.0** — personal/riset boleh, komersial tidak.
- **Download**: Actions artifact Azure blob di jaringan ini di-throttle (~6-10 KB/s/koneksi). Solusi: unduh paralel banyak koneksi (script chunked), atau tunggu release stabil (CDN GitHub Releases cepat, ~8 MB/s).
- **Cover/edit**: butuh SheetSage2 (sudah ada di dev audio.cpp: artifact `-sheetsage2`) — belum diinstal.

## Opsi 2 — ComfyUI Native (checkpoint INT8) — TERVERIFIKASI

Selain audio.cpp, YuE2 juga jalan lewat **support native ComfyUI** (PR [#16250](https://github.com/Comfy-Org/ComfyUI/pull/16250), merged 11 Sep 2026 + fix #16293). Cocok kalau mau UI/workflow visual.

| Item | Detail |
|------|--------|
| ComfyUI | diupdate dari detached `v0.35.1` → `master 02d39c8c` (24 commit) |
| Node | `YuE2GenerateMusic`, `YuE2GenerateABC`, `EmptyYuE2LatentAudio` (+ `VAEDecodeAudioTiled`, `AudioEncoderLoader`, `SheetSage2AudioToABC`) |
| Checkpoint | `E:\AI\ComfyUI\models\checkpoints\yue2_3b_int8_convrot.safetensors` (3.69 GB, **INT8**) |
| Encoder cover | `E:\AI\ComfyUI\models\audio_encoders\sheetsage2_bf16.safetensors` (1.29 GB) |
| Sumber | HF `Comfy-Org/YuE2` |
| **Peak VRAM (uji)** | **5.84 GiB** |
| Waktu | lagu 40s → **~13.4s** execution (termasuk load model) |
| Output | `E:\AI\ComfyUI\output\audio\YuE2_test_00001.flac` (48 kHz stereo) |

Alternatif checkpoint: `yue2_3b_bf16.safetensors` (7.26 GB) — lebih berat, rawan OOM di 12 GB.

### Template

Semua di `E:\AI\eikei-plan\custom\workflows\music\` (source) dan `E:\AI\ComfyUI\user\default\workflows\music\` (aktif di menu **Workflows**):

| File | Isi |
|------|-----|
| `yue2_int8_text_to_song.json` | Dasar: text-to-song 48 kHz, checkpoint INT8, jalur ABC (`cot=full`). |
| `yue2_anison_jrock.json` | Anison/J-rock opening (vokal female, gitar distorsi, BPM 152, D major), lirik Jepang **orisinal**. |
| `yue2_anison_jrock_instrumental.json` | Versi instrumental (best-effort; lirik = tag seksi + style "instrumental, no vocals"). |

Catatan: genre/vibe saja yang meniru gaya era itu — **melodi & lirik orisinal**, bukan salinan lagu berhak cipta manapun. Untuk melodi kustom orisinal, suplai skor ABC ke input `abc` di node `YuE2 Generate Music`.

### Catatan

- ComfyUI nge-warn frontend `1.51.10` < rekomendasi `1.52.7` (tidak blocking).
- Jalur "direct" (tanpa ABC, `cot=off`) sudah diverifikasi; template default pakai ABC planning (`cot=full`).
- Revert ComfyUI: `git -C E:\AI\ComfyUI checkout 856a922b` lalu restart.

---

## Referensi

- Model doc: `04-audio-generation/models/yue2.md`
- audio.cpp: <https://github.com/0xShug0/audio.cpp>
- GGUF: <https://huggingface.co/audio-cpp/Yue2-3B-GGUF>
- Diskusi VRAM: <https://github.com/multimodal-art-projection/YuE/issues/163>
