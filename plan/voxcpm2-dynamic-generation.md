# VoxCPM2 — Dynamic Generation Plan

- **Status**: in-progress
- **Added**: 2026-05-23

---

## Goal

Membuat sistem TTS yang bisa dipanggil secara dinamis — dari script, CLI, atau ComfyUI node — untuk bahasa Indonesia dan Jepang (extensible ke 30 bahasa).

Context: VoxCPM2 sudah terinstall dan ter-test di `E:\AI\sound-plan\.venv`, GPU RTX 5070 12GB ready.

---

## Architecture Overview

```
[Input Text] → [CLI / API / ComfyUI Node] → [VoxCPM2 Generator] → [.wav output]
```

3 lapis akses:
1. **Core script** — pure Python, reusable di mana aja
2. **CLI tool** — dari terminal
3. **ComfyUI custom node** — integrasi ke workflow visual

---

## Phase 1: Core Generator Script

File: `E:\AI\sound-plan\scripts\tts_generator.py`

### Features
- Auto-detect bahasa dari teks (atau explicit `--lang`)
- Voice cloning dari reference audio
- Voice design dari text description
- Caching model (load sekali, generate berkali-kali)
- Batch generation dari file teks / JSON

### Usage
```bash
# Single generation
python tts_generator.py --text "Halo dunia" --output output.wav

# Voice cloning
python tts_generator.py --text "Halo dunia" --ref-audio suara.wav --output clone.wav

# Voice design
python tts_generator.py --text "Hello" --voice-design "young woman, cheerful" --output design.wav

# Batch from JSON
python tts_generator.py --batch input.json --output-dir ./output/
```

### JSON batch format
```json
[
  {"id": "1", "text": "Halo dunia", "lang": "id"},
  {"id": "2", "text": "こんにちは", "lang": "ja", "ref_audio": "voice.wav"}
]
```

---

## Phase 2: ComfyUI Custom Node

Folder: `E:\AI\ComfyUI\custom_nodes\ComfyUI-VoxCPM2\`

### Node types

| Node | Input | Output |
|------|-------|--------|
| `VoxCPM2 Loader` | model_path | VOXCPM_MODEL |
| `VoxCPM2 TTS` | model, text, lang | AUDIO |
| `VoxCPM2 Voice Clone` | model, text, ref_audio | AUDIO |
| `VoxCPM2 Voice Design` | model, text, description | AUDIO |

### Workflow example
```
[Load VoxCPM2] → [TTS: "Halo dunia", lang=id] → [Audio Preview / Save]
```

### Directory structure
```
ComfyUI/
  custom_nodes/
    ComfyUI-VoxCPM2/
      __init__.py
      nodes.py           # ComfyUI node definitions
      requirements.txt   # voxcpm, torch >= 2.11
      README.md
```

### Integration approach
- Node pakai subprocess atau shared venv dari sound-plan
- Model cached di `E:\AI\sound-plan\.hf_cache` — reuse, gak download ulang
- Model loader node: load model sekali, cached di ComfyUI workflow

---

## Phase 3: Optimization

| Item | Current | Target |
|------|---------|--------|
| RTF | 1.75 | <1.0 (near-realtime) |
| Speedup options | - | Install Triton (+triton), Nano-VLLM, torch.compile |
| Model quantization | bf16 ~8GB VRAM | INT8/INT4 via GGUF |
| Loading time | 17 detik (cold) | <5 detik (warm/streaming) |

### Triton install
```bash
pip install triton
```
Akan enable `torch.compile` → estimasi 2-3x speedup → RTF ~0.6-0.9

### Nano-VLLM
```bash
pip install nano-vllm
```
Published RTF ~0.13 on RTX 4090 → estimasi ~0.2-0.3 on RTX 5070

---

## Phase 4: Extend to Other TTS Models

Setelah VoxCPM2 beres, bisa extend ke model lain:

| Model | Priority | Use case |
|-------|----------|----------|
| OmniVoice | High | 600+ bahasa, fastest inference |
| Supertone-3 | High | CPU-only deployment |
| Qwen3-TTS | Medium | Streaming 97ms |
| Kokoro-82M | Low | Ultra-lightweight |

---

## Implementation Order

1. **Core generator script** — `scripts/tts_generator.py` (cukup 1 file)
2. **CLI wrapper** — via `argparse`
3. **ComfyUI node** — 4 nodes (loader, tts, clone, design)
4. **Optimization** — Triton + torch.compile
5. **Batch pipeline** — JSON input → multi-file output

---

## Dependencies needed

```bash
# Already installed
pip install voxcpm torch torchaudio soundfile

# Need to add for optimization
pip install triton  # torch.compile speedup

# For ComfyUI node
# Just voxcpm + torch (already in shared venv or specify path)
```

---

## File Plan

```
E:/AI/sound-plan/
  scripts/
    tts_generator.py        # Core reusable generator
    tts_batch.py            # Batch processing
    requirements.txt        # Dependencies manifest

E:/AI/ComfyUI/
  custom_nodes/
    ComfyUI-VoxCPM2/
      __init__.py
      nodes.py              # 4 custom nodes
      config.yaml           # Model path, cache path
      README.md
```
