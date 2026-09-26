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
| `yue2_anison_jrock_v2.json` | Varian J-rock orisinal kedua (E minor, BPM 168, twin harmonized guitar, double-kick, slap bass), lirik Jepang orisinal. |
| `yue2_anison_jpop.json` | Anison J-pop / electro (BPM 183, verse D minor → chorus **modulasi +1 semitone ke E♭ minor**, power-chord gitar + supersaw trance synth arpeggio). Lirik orisinal; output prefix `audio/anison_jpop`. |
| `yue2_anison_jrock_instrumental.json` | Versi instrumental (best-effort; lirik = tag seksi + style "instrumental, no vocals"). |
| `yue2_bgm_epic_battle.json` | BGM instrumental dark-fantasy battle (violin/strings + female choir lead, gitar/drum penggerak), `max_duration` = durasi klip (mis. 45.28). Prefix `audio/bgm_epic_battle`. |
| `yue2_bgm_forest_duel.json` | BGM duel hutan (pedang vs tombak), taiko + shakuhachi + staccato strings + low brass. **51s** via skor ABC suplai sendiri (34 bar @160 BPM; bar akhir `"Dm"D16` + `z16`; voice `Vocal` = rests), blok negasi 6 tag. Prefix `audio/bgm_forest_duel`. |
| `yue2_bgm_pose_30s.json` | BGM 30s upbeat kawaii electro-pop / J-pop dance (BPM 144, bright synth + punchy bass), dibuat mengikuti profil referensi "Pose! Pose! Pose! seedance2.5". Prefix `audio/bgm_pose_30s`. |

Catatan: genre/vibe saja yang meniru gaya era itu — **melodi & lirik orisinal**, bukan salinan lagu berhak cipta manapun. Untuk melodi kustom orisinal, suplai skor ABC ke input `abc` di node `YuE2 Generate Music`.

**Penting soal `style` prompt:** YuE2 dilatih dengan **tag pendek** (contoh asli: `"violin with girl singing jpop anime"`). Prompt panjang/analitis sebagian diabaikan (tempo/karakter tidak diikuti). Tulis instrument di depan, singkat, comma-separated. Contoh yang jalan (dipakai di `yue2_anison_jpop.json`):
`anison digital J-rock, distorted electric guitar power chords, bright supersaw trance synth arpeggios, fast electronic rock drums, driving synth bass, powerful female lead vocal, urgent energetic futuristic, BPM 183, D minor verse to E-flat minor chorus`

### Catatan

- ComfyUI nge-warn frontend `1.51.10` < rekomendasi `1.52.7` (tidak blocking).
- Jalur "direct" (tanpa ABC, `cot=off`) sudah diverifikasi; template default pakai ABC planning (`cot=full`).
- Revert ComfyUI: `git -C E:\AI\ComfyUI checkout 856a922b` lalu restart.

---

## Video Export (gambar cover + audio → YouTube)

Menggabungkan cover PNG + audio jadi video. **Konvensi: pakai lossless untuk master.**

Tools: `E:\AI\sound-plan\tools\ffmpeg-shared\ffmpeg-master-latest-win64-gpl-shared\bin\` (`ffmpeg.exe`, `ffprobe.exe`).

### Master lossless (arsip / putar lokal) — AUDIO BIT-PERFECT

Audio FLAC di-**copy** (`-c:a copy`), bukan re-encode. Output **MKV** (MP4 tak menerima FLAC secara standar/Youtube).

```powershell
$ff = "E:\AI\sound-plan\tools\ffmpeg-shared\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"
$vf = "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,format=yuv420p[v]"
& $ff -y -loop 1 -framerate 2 -i "cover.png" -i "song.flac" -filter_complex $vf `
  -map "[v]" -map 1:a -c:v libx264 -preset medium -crf 18 -tune stillimage `
  -c:a copy -r 2 -t <durasi_audio_detik> -movflags +faststart "out_lossless.mkv"
```

### Upload YouTube — tetap lossy (master tetap lossless)

YouTube **tidak** menerima MKV/FLAC; dia transcoding sendiri. Render MP4 dari master lossless (jangan dari yang sudah lossy):

```powershell
& $ff -y -loop 1 -framerate 2 -i "cover.png" -i "song.flac" -filter_complex $vf `
  -map "[v]" -map 1:a -c:v libx264 -preset medium -crf 18 -tune stillimage `
  -c:a aac -b:a 320k -ar 48000 -r 2 -t <durasi_audio_detik> -movflags +faststart "out_youtube.mp4"
```

### Aturan & verifikasi

- **Selalu `-t <durasi_audio>`** agar tidak ada ekor hening/senjata di akhir (gambar still loop tak berujung).
- Gambar ~16:9 → scale+pad cukup. Gambar persegi → blur background + `overlay` cover di tengah.
- **Audio FLAC (~950 kbps) jauh lebih besar dari AAC 256k** — file MP4 lebih kecil itu **normal**, bukan kehilangan bagian.
- Kalau ada "ada yang turun/jelek", cek dulu **apakah ada di FLAC sumber** (bukan asumsi encoding). Bukti bit-perfect:
  ```powershell
  # decode kedua file ke PCM, bandingkan hash
  & $ff -v error -i "out_lossless.mkv" -f s16le -ac 2 -ar 48000 a.pcm -y
  & $ff -v error -i "song.flac"          -f s16le -ac 2 -ar 48000 b.pcm -y
  Get-FileHash a.pcm,b.pcm -Algorithm SHA256
  ```
  Hash sama = combine tidak mengubah apa pun.
- **Loudness identik** dicek dgn: `-af loudnorm=print_format=summary` (atau `ebur128`).
- Kalau terasa lebih kecil **hanya di player**, curigai normalisasi/ReplayGain player (bukan file). Putar raw FLAC vs MKV di player & volume yang sama untuk membuktikan.
- Cacat yang **ada di FLAC sumber** (mis. drop volume ~1s) tidak bisa dihilangkan oleh combine apa pun; harus di-patch atau regenerate.

### Lokasi kerja (folder lagu + cover)

- `E:\Sanctury Music\Yue Trial\` — batch pertama (`anison_original_*`)
- `E:\Sanctury Music\Yue Trial S2\` — `anison_jpop_00004`
- `E:\Sanctury Music\Yue Trial S3\` — `anison_jpop_00001` (catatan: ada drop ~81.7s di FLAC sumbernya)

---

## BGM untuk video klip (khusus kebutuhan scoring video)

> **SCOPE — penting.** Seluruh seksi ini **hanya untuk BGM instrumental berdurasi terbatas** (mis. 30 / 45 / 51s untuk scoring klip).
> **TIDAK berlaku untuk song ber-lirik.** Song punya perilaku berbeda: ia bisa menulis **end-token** dan berhenti
> sendiri di panjang yang **tidak bulat** (terukur: `164.72 / 169.72 / 148.76 / 152.04 / 204.64 / 191.32 / 235.68s`
> dengan cap 360s). Jangan pakai resep "suplai ABC + voice Vocal = rests" di bawah untuk song — song justru butuh voice vokal.

Konteks: membuat **BGM instrumental** lalu memasangnya ke klip video berdurasi tetap, supaya **timing pas dan ending tidak gantung**. Template: `yue2_bgm_epic_battle.json`, `yue2_bgm_pose_30s.json`, dan `yue2_bgm_forest_duel.json` (`E:\AI\eikei-plan\custom\workflows\music\` + `E:\AI\ComfyUI\user\default\workflows\music\`).

### Kenapa ending "gantung" — mekanisme di ComfyUI

Dari `comfy_extras/nodes_yue2.py`:

```python
max_tokens = max(1, round(max_duration * FRAMES_PER_SECOND))   # FRAMES_PER_SECOND = 25
```

- `max_duration` **bukan durasi pasti**, tapi **batas token**. Tooltip resmi: *"Maximum duration in seconds. Automatically reduced for long prompts; generation can stop earlier."*
- **Temuan terukur (17 Sep)**: untuk prompt **tag-only / instrumental**, YuE2 **selalu menghabiskan seluruh budget** — output = cap persis. Cap 60/45/90s → output 60.00/45.00/90.00s. Tidak ada end-token, jadi tidak ada ending natural. **Set `max_duration` = durasi video** (mis. `45.28`), lalu fade singkat di post bila perlu.
- Untuk lagu **berlirik**, dua kemungkinan akhir: (1) model menulis **end-token** → ending natural tapi panjang < `max_duration`; (2) **budget habis** → terpotong mid-frase → **gantung**. Tanda pasti di konsol: `YuE2 music reached its token budget before the end token.`
- Output `seconds` = frame yang **benar-benar** di-generate (bukan cap).

### Instrumental sejati: blok negasi 6 tag (WAJIB untuk BGM)

Temuan terukur (23 Sep) — **cukup via prompt, tanpa LoRA**:

| Output | Stem vokal (Demucs) | Hasil |
|---|---|---|
| `bgm_epic_battle_00006` | **0.0%** (RMS 0.00158) | benar-benar instrumental ✅ |
| `bgm_forest_duel_00005` | **22.7%** (RMS 0.05152) | ada nyanyi ❌ (profil: aktif 0–25s, hening 25–40s, **nyanyi 40–51s** lalu terpotong) |

Beda satu-satunya: **style**. Yang jalan memuat blok negasi lengkap, kata per kata:

```
instrumental only, no vocals, no singing, no lyrics, no lead voice, wordless
```

`no vocals` **satu tag saja tidak cukup**. Taruh blok itu di bagian awal style (setelah genre), dan ingat konvensi tag pendek (lihat §Template) — style 300-an karakter masih bekerja, tapi tag di ujung paling rawan diabaikan.

### BGM panjang terbatas: suplai skor ABC sendiri (kontrol panjang penuh)

Masalah: dengan `cot=full`, **planner ABC internal menulis form yang bisa lebih panjang dari cap** → selalu ada seksi baru yang mulai sekitar detik 40 lalu terpotong; planner juga **selalu menulis voice melodi vokal**.

Solusi deterministik — dari `comfy/text_encoders/yue2.py:246-250`, kalau input `abc` **diisi**, skornya dipakai apa adanya (`abc_ids` di-append ke prefix, tidak digenerate):

1. **Lepas link `abc`** di node *YuE2 Generate Music* (`input.link = None`) + hapus link-nya dari daftar `links`, supaya widget `abc` yang dipakai (bukan output node ABC).
2. **Tulis skor sendiri** ke widget `abc`. Format (contoh resmi repo YuE):
   ```
   X:1
   T:Forest Duel
   M:4/4
   L:1/16
   Q:1/4=160
   V: Vocal clef=treble name="Vocal Melody" snm="Vocal"
   V: Ins clef=treble name="Ins Melody" snm="Inst."
   K:Dm
   % intro
   V: Ins
   "Dm"D8A,8|"Dm"D8A,8|"Bb"B,8F8|"C"C8G8|
   ...
   V: Vocal
   z16|z16|...            <- voice vokal = istirahat (instrumental)
   ```
3. **Hitung durasi:** `durasi = jumlah_bar × 4 × 60 / BPM`. Contoh dipakai: **34 bar @160 BPM = 51.0s persis**.
4. **Akhiri dengan ending asli:** bar terakhir `"Dm"D16` (hantaman nada penuh 1 bar) lalu `z16` (istirahat 1 bar) → budget `max_duration` berakhir **bersamaan** dengan akhir skor, jadi **tidak ada potong paksa**.
5. **Voice `Vocal Melody` = rests untuk semua bar** → tidak ada garis vokal untuk dinyanyikan (pelengkap blok negasi di style).
6. Set `max_duration` = durasi skor (mis. `51`; `51 × 25 = 1275` frame, kelipatan pas 0.04). Set BPM di style agar cocok dengan `Q:1/4=`.

Skor bisa diedit langsung di widget untuk mengubah form/panjang/ending.

### Verifikasi hasil BGM

1. **Stem vokal** (target < ~1% energi). `torchaudio`/`torchcodec` **rusak di venv ini** (`OSError: libtorchcodec_core*.dll`) → panggil Demucs lewat API sambil memuat audio dengan `soundfile`:
   ```python
   import soundfile as sf, torch
   from demucs.pretrained import get_model
   from demucs.apply import apply_model
   model = get_model("htdemucs").cuda().eval()
   wav, sr = sf.read(path, dtype="float32", always_2d=True)   # butuh 44.1 kHz stereo
   x = torch.from_numpy(wav.T)
   ref = x.mean(0); x = (x - ref.mean()) / (ref.std() + 1e-8)
   sources = apply_model(model, x[None], device="cuda", shifts=1, split=True, overlap=0.25)[0]
   ```
   Lalu bandingkan RMS `vocals` vs total. Skrip kerja: `%TEMP%\opencode\run_demucs.py`.
2. **Ekor** — ukur RMS 2.5s terakhir vs rata-rata (`tail/avg`) dan 1s terakhir vs 1s sebelumnya:

   | Output | tail/avg | 1s/prev | Verdict |
   |---|---|---|---|
   | `bgm_epic_battle_00004/5/6` | 0.80 / 0.77 / 0.59 | 0.70 / 0.69 / 0.73 | ada penurunan (ending layak) |
   | `bgm_forest_duel_00001` | 1.11 | 1.25 | menanjak → stop keras |
   | `bgm_forest_duel_00002` | 0.67 | **1.42** | hantaman final terpotong |
   | `..._fade45` (post) | 0.34 | 0.51 | turun mulus |
   | `..._stinger45` (post) | 0.25 | 0.00 | hening total |

### Kalau masih terpotong: fallback post (2 pilihan)

```powershell
$ff = "E:\AI\sound-plan\tools\ffmpeg-shared\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"
# A. fade mulus, berakhir tepat di durasi
& $ff -y -i "bgm.flac" -af "afade=t=out:st=49.2:d=1.8" "bgm_fade.flac"
# B. berhenti di hantaman + hening (idiom cue pertarungan): potong di onset kuat terakhir, sisanya sunyi
```
Pasang ke video: `-c:v copy -c:a aac -b:a 320k -t <durasi>` (video tidak di-re-encode).

### Riset lanjutan (belum dikerjakan)

- **Instrumental LoRA** untuk jaminan tanpa vokal: `Mothersuperior/YuE2-instrumental-cot-full-loras` — file ComfyUI `ar_lora_inst_v3abc_comfyui.safetensors` (~203 MiB), di-load di slot **CLIP** (AR planner), `mode=full` + ABC node. Belum diinstal. **Status: sekarang OPSIONAL** — blok negasi 6 tag (§Instrumental sejati) sudah cukup (terukur 0.0% vokal), dan voice `Vocal` = rests pada skor ABC memberi jaminan tambahan.

### Resep BGM durasi terbatas (ringkas)

1. **Style**: genre + **blok negasi 6 tag** + instrumen + `BPM …` (lihat §Instrumental sejati).
2. **Skor ABC** disuplai sendiri (link `abc` dilepas), panjang = durasi target, diakhiri hit final + `z16`; voice `Vocal` = rests (lihat §BGM panjang terbatas).
3. **`max_duration`** = durasi skor/video persis; harus kelipatan `0.04` (frame = `s × 25`). Mis. `51` → 1275 frame.
4. **Verifikasi**: stem vokal < ~1% (Demucs) + ekor `tail/avg` < 0.85 (lihat §Verifikasi hasil BGM).
5. **Fade/stinger di post hanya bila perlu** (cadangan, lihat §Kalau masih terpotong).

Catatan: untuk prompt instrumental output akan = cap (selalu penuh), jadi panjang ditentukan oleh cap/skor — bukan sesuatu yang bisa "berhenti sendiri".

### (Dihapus) `scripts/fit-video-bgm.ps1`

Dibuat lalu **dihapus** (17 Sep): ternyata tidak perlu, karena set `max_duration` = durasi video langsung di ComfyUI sudah menghasilkan durasi pas. Skrip itu hanya berguna untuk kasus langka (audio jauh lebih panjang / perlu loop), dan bisa diganti perintah ffmpeg satu baris.

Diuji dengan klip 45.28s: cap 45 → output `45.00s`, cap 90 → `90.00s` (membuktikan output = cap).

### BGM mengikuti referensi audio (contoh: 30s "Pose! Pose! Pose!")

Referensi: `C:\Users\Paimon\Downloads\…seedance2.5.m4a` (30.09s). Profil diukur dengan `librosa` (di `.venv`) — decode dulu ke mono 22.05 kHz via ffmpeg:

| Fitur | Referensi | Hasil `bgm_pose_30s_00001` |
|---|---|---|
| Durasi | 30.09s | **30.00s** |
| Tempo | tempogram peak 95.7 & 143.6 BPM (rasio 2:3 → feel bouncy/triplet) | 143.6 BPM |
| Key (Krumhansl) | F mayor | E mayor (model geser) |
| Centroid / rolloff85 | 2106 Hz / 4.85 kHz | 3634 Hz / 7.85 kHz (lebih terang) |
| Band energy | bass 60–250: 26.6%, highmid 2–5k: 21.1%, high 5–10k: 15.4% | 11.6% / 22.3% / 30.1% (**bass lebih tipis, high lebih tajam**) |
| Harmonic/percussive | 2.99 | 2.64 |

Prosedur:

1. **Analisis** referensi (bukan transkripsi melodi — hanya profil gaya: tempo, key, centroid, band energy, HPSS). Skrip: `%TEMP%\opencode\analyze_ref.py`.
2. **Terjemahkan ke tag pendek** (instrument di depan), isi `style`: mis. `upbeat kawaii electro-pop, cute energetic J-pop dance, bright sparkling synth lead, punchy bass, four-on-the-floor dance beat, claps and snaps, … BPM 144, F major`.
3. **Set `max_duration`** = durasi target (30 → output 30.00s persis).
4. **Queue via API** (ComfyUI harus jalan) — `POST /prompt` dengan format API (`{class_type, inputs}` per node id), bukan format UI. Node `PrimitiveNode`/`PreviewAny`/`Note` **tidak** ikut; style/lyrics di-inline, `abc` = `["<node ABC>", 0]`. Node `YuE2GenerateABC` **wajib** diberi parameter advanced (`temperature 0.7`, `top_p 0.9`, `top_k 30`, `repetition_penalty 1.005`, `penalty_window 100`) atau validasi gagal.
5. Iterasi bila perlu: bass kurang → tambah `deep warm sub bass, fat kick`; treble terlalu tajam → kurangi `sparkling`.

Contoh job API: `%TEMP%\opencode\job_pose.json`.

Catatan: model **tidak selalu mengikuti key** yang diminta, dan hasil tag-only cenderung lebih terang/lebih tipis bass daripada referensi. 

---

## Referensi

- Model doc: `04-audio-generation/models/yue2.md`
- audio.cpp: <https://github.com/0xShug0/audio.cpp>
- GGUF: <https://huggingface.co/audio-cpp/Yue2-3B-GGUF>
- Diskusi VRAM: <https://github.com/multimodal-art-projection/YuE/issues/163>
