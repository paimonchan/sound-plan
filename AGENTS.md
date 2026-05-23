# AI Sound Plan — Knowledge Base

Knowledge base untuk riset & tracking project AI suara. Berisi dokumentasi model, benchmark, deployment guide, dan aplikasi TTS.

---

## Quick Start

### VoxCPM2 TTS (Gradio Web UI)

```powershell
# Double-click this file:
E:\AI\sound-plan\apps\voxcpm2-gradio\run.bat

# Or from terminal:
& "E:\AI\sound-plan\.venv\Scripts\python.exe" "E:\AI\sound-plan\apps\voxcpm2-gradio\app.py"
# Buka http://localhost:7860
```

### Project Structure

```
E:\AI\sound-plan\
  AGENTS.md                  ← AI context (auto-loaded)
  apps/                      ← Runnable applications
    voxcpm2-gradio/          ← VoxCPM2 Gradio Web UI
      app.py                 ← TTS inference (custom)
      run.bat                ← Launch TTS (double-click)
      run_train.bat          ← Launch Training (double-click)
  repos/                     ← Cloned source repos (not in git)
    VoxCPM/                  ← OpenBMB/VoxCPM (19.6K stars)
      app.py                 ← Official Gradio demo
      lora_ft_webui.py       ← Training Web UI
  models/                    ← Downloaded model weights (~5GB)
    voxcpm2/                 ← VoxCPM2 (self-contained)
  configs/                   ← Training config YAML files
  data/                      ← Training datasets (not in git)
  logs/                      ← Training logs / TensorBoard
  .venv/                     ← Python virtual environment (Python 3.10)
  01-tts/ ... 21-*/          ← Research documentation per category
  plan/                      ← Implementation plans
  scripts/                   ← Utility & test scripts
```

---

## Peta Kategori (21 domain)

| # | Folder | Domain | Fokus Utama |
|---|--------|--------|-------------|
| 01 | `01-tts/` | Text-to-Speech | Sintesis suara, voice cloning, prosody control, streaming |
| 02 | `02-stt/` | Speech-to-Text | Transkripsi, diarization, VAD, keyword spotting, alignment |
| 03 | `03-voice-conversion/` | Voice Conversion | Timbre transfer, zero-shot conversion |
| 04 | `04-audio-generation/` | Audio Generation | Music generation, sound effects, controllable audio |
| 05 | `05-audio-processing/` | Audio Processing | Noise reduction, upscaling, source separation, dereverberation |
| 06 | `06-voice-assistant/` | Voice Assistant | LLM+TTS+STT pipeline, voice agents, frameworks |
| 07 | `07-audio-analysis/` | Audio Analysis | Classification, emotion detection, MIR, captioning, bioacoustics |
| 08 | `08-voice-biometrics/` | Voice Biometrics | Speaker verification, anti-spoofing, deepfake detection |
| 09 | `09-neural-codec/` | Neural Codec | AI audio compression (EnCodec, SoundStream, etc.) |
| 10 | `10-lip-sync/` | Lip Sync | Audio-driven facial animation, video dubbing |
| 11 | `11-singing-voice/` | Singing Voice | AI singing synthesis, synth integration |
| 12 | `12-speech-translation/` | Speech Translation | Speech-to-speech, cascade vs E2E, code-switching |
| 13 | `13-spatial-audio/` | Spatial Audio | Binaural, ambisonics, head-tracking, 3D audio |
| 14 | `14-audio-captioning/` | Audio Captioning | Deskripsi konten audio ke teks |
| 15 | `15-keyword-vad/` | Keyword & VAD | Wake word detection, voice activity detection, on-device |
| 16 | `16-audio-editing/` | Audio Editing | Inpainting, text-based audio editing |
| 17 | `17-realtime-streaming/` | Realtime Streaming | WebRTC, low-latency streaming, edge streaming |
| 18 | `18-multimodal-audio-visual/` | Multimodal AV | AV-ASR, AV-diarization, AV-generation |
| 19 | `19-accessibility/` | Accessibility | Assistive listening, speech-to-sign, audio description |
| 20 | `20-gaming-audio/` | Gaming Audio | Procedural audio, adaptive music, voice chat DSP |
| 21 | `21-audio-forensics/` | Audio Forensics | Tampering detection, authentication, enhancement |
| — | `_resources/` | Lintas Domain | Papers, courses, competitions, conferences, tools, VST plugins, glossary |

---

## Konvensi Sub-Folder

Tiap kategori bisa punya kombinasi sub-folder berikut:

| Sub-folder | Isi |
|------------|-----|
| `models/` | Informasi model: paper, repo, checkpoint, arsitektur |
| `datasets/` | Informasi dataset: link download, statistik, lisensi |
| `papers/` | Paper PDF + notes + highlight |
| `benchmarks/` | Hasil benchmark, leaderboard, metrik (MOS, WER, EER, etc.) |
| `notebooks/` | Link Colab / Jupyter notebook, eksperimen |
| `open-source/` | List proyek open-source GitHub (nama, link, deskripsi) |
| `commercial-apis/` | Layanan API berbayar: pricing, fitur, link |
| `deployment/` | Strategi deployment: ONNX, TensorRT, edge, cloud |
| `evaluation/` | Metrik evaluasi, tools pengujian spesifik domain |

**Tidak semua sub-folder wajib ada** — hanya yang relevan dengan domain-nya.

---

## Aturan Konten

- **Format**: Semua konten dalam file `.md`
- **Metadata wajib di tiap file**: `# Judul` + tanggal akses + status (`todo`, `in-progress`, `done`)
- **Link**: Gunakan permalink (commit hash) untuk GitHub, DOI untuk paper
  
### Contoh format file di `models/`:

```markdown
# XTTS-v2
- Paper: https://arxiv.org/abs/2406.04904
- Repo: https://github.com/coqui-ai/TTS
- Status: reviewed
- Added: 2026-05-23
- Notes: Multilingual TTS, voice cloning 6 detik, latency rendah
```

---

## Cara Nambah Kategori Baru

1. Pastikan tidak overlap dengan 21 kategori existing
2. Buat folder `XX-nama-kategori/` dengan sub-folder sesuai relevansi
3. Update file ini — tambah di tabel peta kategori
4. Isi konten minimal: 1 file `README.md` di dalam folder baru

---

## Current Landscape — TTS Models (Last updated: 2026-05-23)

Berdasarkan riset HuggingFace trending + benchmark publik + paper:

### Top Open-Source TTS (ranked by quality + license)

| # | Model | WER EN | SIM EN | Languages | License | Key Edge |
|---|-------|:------:|:------:|:---------:|:------:|-----------|
| 1 | **Qwen3-TTS 1.7B** | 1.24 | 71.7 | 10 | Apache 2.0 | Streaming 97ms, 5M hrs training |
| 2 | **VoxCPM2** 2B | 1.84 | 75.3 | 30 | Apache 2.0 | Tokenizer-free, SIM #2, voice design |
| 3 | **OmniVoice** 0.6B | 1.30 | 72.9 | 600+ | Apache 2.0 | Most languages, fastest RTF 0.025 |
| 4 | **MOSS-TTS** 1.7B | 1.93 | 73.3 | 20 | Apache 2.0 | Ecosystem (dialogue+SFX+realtime+Nano) |
| 5 | **FishAudio S2 Pro** 4B | 0.99 | unpub. | 80+ | Research | Best WER, complex license |
| 6 | **Chatterbox** 0.5B | unpub. | unpub. | 23 | MIT | Emotion exaggeration, easiest to use |
| 7 | **Supertone-3** 99M | unpub. | unpub. | 31 | OpenRAIL | CPU-only, on-device deployment |

Model-model di atas SUDAH di-riset dan diverifikasi. Data detail tersedia di `01-tts/models/`.

### Notable Omissions (why they're not in top list)

| Model | Downloads | Reason excluded |
|-------|:--------:|-----------------|
| **XTTS-v2** | 8.91M | CPML license (non-commercial), no Indonesian, Dec 2023 (stale) |
| **Kokoro-82M** | 11M | No Indonesian, no voice cloning, style presets only |
| **CSM-1B** | 231K | English only, no voice cloning, needs external LLM |
| **Dia-1.6B** | 10K | English only, 10GB VRAM |
| **VibeVoice-1.5B** | 182K | English+Chinese only, research-only (audible disclaimer) |

### For Indonesian + Japanese (current priority)

| # | Model | SIM ID↑ | SIM JP↑ | WER ID↓ | CER JP↓ | License |
|---|-------|:------:|:------:|:------:|:------:|:------:|
| 1 | **VoxCPM2** | 80.0% | 82.8% | 1.36% | 2.40% | Apache 2.0 |
| 2 | **OmniVoice** | 80.5% | 82.8% | 1.97% | 4.03% | Apache 2.0 |
| 3 | Fish S2 Pro | 76.3% | 79.6% | 1.68% | 1.82% | Research |
| 4 | Supertone-3 | ❌ | ❌ | ❌ | ❌ | OpenRAIL |

**→ VoxCPM2 is the top pick: #1 SIM in both languages, Apache 2.0, free voice cloning + voice design.**

### Also Significant

- **STT**: Cohere Transcribe #1 Open ASR Leaderboard, NVIDIA Parakeet v3, Qwen3-ASR
- **Music/SFX**: Stable Audio 3.0 (May 20, 2026), AudioX (ICLR 2026), Sony Woosh
- **Voice Agents**: GPT-Realtime-2 (May 7), TML-Interaction-Small (0.4s full-duplex)

---

## Tips Navigasi Cepat

- **Mau bandingin TTS?** → `01-tts/models/` + `01-tts/benchmarks/`
- **Mau bikin voice bot?** → `06-voice-assistant/pipelines/` + `02-stt/` + `01-tts/`
- **Mau riset paper terbaru?** → `_resources/papers/` atau `XX-kategori/papers/`
- **Mau belajar dari awal?** → `_resources/courses/` + `_resources/tutorials/`
- **Mau deploy di edge?** → `_resources/edge-deployment/` + `XX-kategori/deployment/`
- **Cari TTS untuk bahasa Indonesia/Jepang?** → `01-tts/models/voxcpm2.md`
