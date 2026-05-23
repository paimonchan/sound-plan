# Audio Cleaning — untuk Training Data TTS

- **Status**: done (installed & tested)
- **Added**: 2026-05-23
- **Updated**: 2026-05-23 (verified tools, final setup)

---

## Tools Installed (Semua di E:\)

| Tool | Size | Status | Cara pakai |
|------|:----:|:------:|-----------|
| **yt-dlp** | ~3 MB | ✅ `yt-dlp` (venv) | Download audio dari YouTube/website |
| **Demucs v4.0.1** | ~370 MB | ✅ `demucs` (venv CLI) | Hapus BGM/instrumental |
| **DeepFilterNet** | 25.7 MB | ✅ `tools\deep-filter.exe` (standalone) | Hapus noise/hiss/static |

---

## Quick Start

### 1 baris: bersihin audio sekaligus

```powershell
# Hapus BGM (vocals only)
E:\AI\sound-plan\.venv\Scripts\demucs.exe --two-stems=vocals "input.wav"

# Hapus noise dari hasil vokal
E:\AI\sound-plan\tools\deep-filter.exe "separated\htdemucs\input\vocals.wav" -o "clean.wav"
```

---

## Workflow Lengkap

```
Audio Kotor (BGM + noise)
    │
    ├─ Step 1: demucs → hapus BGM, ambil vokal
    │     Output: separated/htdemucs/{nama}/vocals.wav
    │
    ├─ Step 2: deep-filter → hapus noise/hiss
    │     Output: clean.wav
    │
    └─ Step 3: Potong segmen 5-30 detik (Audacity / script)
           Siap training VoxCPM2
```

---

## Contoh Nyata

### Dari video YouTube → training data bersih

```powershell
# Step 0: Download audio dari YouTube (16kHz mono, siap training)
yt-dlp -x --audio-format wav --audio-quality 0 ^
  --postprocessor-args "ffmpeg:-ar 16000 -ac 1" ^
  "https://youtube.com/watch?v=xxx" -o "raw.wav"

# Step 1: Pisah vokal dari BGM (~35 detik di RTX 5070)
E:\AI\sound-plan\.venv\Scripts\demucs.exe --two-stems=vocals raw.wav

# Step 2: Bersihin noise (< 1 detik)
E:\AI\sound-plan\tools\deep-filter.exe separated/htdemucs/raw/vocals.wav -o clean.wav

# Hasil: clean.wav (16kHz mono) — siap langsung training VoxCPM2
```

---

## yt-dlp — Download Audio

### Basic download

```powershell
# Download audio only, kualitas terbaik
yt-dlp -x --audio-format wav "URL" -o "output.wav"
```

### Langsung format training (16kHz mono)

```powershell
yt-dlp -x --audio-format wav --audio-quality 0 ^
  --postprocessor-args "ffmpeg:-ar 16000 -ac 1" ^
  "URL" -o "output.wav"
```

### Opsi penting yt-dlp

| Opsi | Fungsi |
|------|--------|
| `-x` | Extract audio only (no video) |
| `--audio-format wav` | Output WAV |
| `--audio-quality 0` | Kualitas terbaik |
| `-ar 16000` | Resample ke 16kHz |
| `-ac 1` | Convert ke mono |
| `--playlist-items 1-5` | Download 5 video pertama dari playlist |
| `--cookies-from-browser chrome` | Untuk video yang butuh login |

> **Note**: ffmpeg harus terinstall untuk post-processing. Download: <https://ffmpeg.org/download.html>

---

## Demucs — Detail

### Basic (vocals only)

```powershell
E:\AI\sound-plan\.venv\Scripts\demucs.exe --two-stems=vocals "lagu.wav"
# Output: separated/htdemucs/lagu/vocals.wav
#         separated/htdemucs/lagu/no_vocals.wav
```

### Full stems (vocal, drum, bass, other)

```powershell
E:\AI\sound-plan\.venv\Scripts\demucs.exe "lagu.wav"
# Output: 4 file (vocals, drums, bass, other)
```

### Opsi penting

| Opsi | Fungsi |
|------|--------|
| `-n htdemucs_ft` | Model terbaik (fine-tuned) |
| `--two-stems=vocals` | Hanya pisah vokal vs instrumental |
| `--device cuda` | Gunakan GPU (default auto) |
| `--mp3` | Output MP3, lebih kecil |
| `--mp3-bitrate 320` | Bitrate MP3 |

---

## DeepFilterNet — Detail

### CLI

```powershell
E:\AI\sound-plan\tools\deep-filter.exe input.wav -o output.wav
```

### Opsi

| Opsi | Fungsi |
|------|--------|
| `-o output.wav` | Path output |
| `--pf` | Post-filter (agresif, hasil lebih bersih) |
| `-D` | Compensate delay (align dengan input) |

---

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Demucs "out of memory" | Tambah `--device cpu` atau kecilkan segment |
| Hasil vokal masih ada noise | Jalankan deep-filter --pf |
| Hasil vokal ada echo | DeepFilterNet handle light reverb, heavy reverb butuh tool lain |
| deep-filter.exe "not found" | Path: `E:\AI\sound-plan\tools\deep-filter.exe` |

---

## Install Ulang (kalau venv reset)

```powershell
E:\AI\sound-plan\.venv\Scripts\pip.exe install demucs
# deep-filter.exe sudah standalone (25.7 MB, no install needed)
```
