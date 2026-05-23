# VoxCPM2 — Training Guide (LoRA Fine-tuning)

- **Status**: reviewed
- **Added**: 2026-05-23

---

## Reference vs Training

| | Reference (Voice Cloning) | Training (Fine-tuning) |
|---|:---:|:---:|
| Audio dibutuhkan | 3-10 detik | 5-10 menit |
| Waktu proses | Instan (zero-shot) | 30-60 menit |
| Kualitas | Good | Excellent |
| Konsistensi | Bisa bervariasi | Stabil |
| Biaya | Gratis | Gratis (GPU listrik) |
| Cocok untuk | Testing, eksperimen | Production, brand voice |

---

## Overview

Dua metode training:

| Metode | Waktu | GPU | Kualitas | Kapan dipake |
|--------|:-----:|:---:|:--------:|-------------|
| **LoRA** (recommended) | ~30-60 menit | 8GB+ | Good | Custom voice, 5-10 menit audio |
| **Full SFT** | ~1-3 jam | 12GB+ | Best | Dataset besar, 1+ jam audio |

---

## Prerequisites

```
✅ VoxCPM2 model downloaded (models/voxcpm2/)
✅ Python 3.10 venv (E:\AI\sound-plan\.venv)
✅ Audio recording: 5-10 menit (LoRA) / 1+ jam (Full)
✅ GPU RTX 5070 12GB (cukup untuk LoRA)
```

---

## Step 1: Siapkan Dataset

Buat file `train.jsonl` — satu line per sample:

```jsonl
{"audio_path": "E:/AI/sound-plan/data/my_voice/recording_01.wav", "text": "Halo semuanya, selamat datang di pelatihan suara.", "language": "id"}
{"audio_path": "E:/AI/sound-plan/data/my_voice/recording_02.wav", "text": "Hari ini kita akan belajar cara membuat model suara custom.", "language": "id"}
{"audio_path": "E:/AI/sound-plan/data/my_voice/recording_03.wav", "text": "Suara ini nantinya bisa digunakan untuk berbagai keperluan.", "language": "id"}
```

### Tips dataset
- **Format audio**: WAV 16kHz mono (direkomendasikan)
- **Durasi per file**: 5-30 detik — hindari yang terlalu pendek/panjang
- **Total audio**: 5-10 menit untuk LoRA (sekitar 20-40 sample)
- **Kualitas rekaman**: Bersih, minim noise, konsisten mic & volume
- **Transkripsi**: Akurat, tanpa typo, sesuai yang diucapkan
- **Variasi**: Sertakan berbagai tone & ekspresi

---

## Step 2: Buat Config YAML

File: `E:\AI\sound-plan\configs\voxcpm2_lora.yaml`

```yaml
pretrained_path: E:/AI/sound-plan/models/voxcpm2/
train_manifest: E:/AI/sound-plan/data/my_voice/train.jsonl
val_manifest: null
sample_rate: 16000
out_sample_rate: 48000
batch_size: 2
grad_accum_steps: 8
num_workers: 4
num_iters: 1000
log_interval: 10
valid_interval: 500
save_interval: 500
learning_rate: 0.0001
weight_decay: 0.01
warmup_steps: 100
max_steps: 1000
max_batch_tokens: 8192
max_grad_norm: 1.0
save_path: E:/AI/sound-plan/models/voxcpm2-ft-lora
tensorboard: E:/AI/sound-plan/logs/finetune_lora
lambdas:
  loss/diff: 1.0
  loss/stop: 1.0
lora:
  enable_lm: true
  enable_dit: true
  enable_proj: false
  r: 32
  alpha: 32
  dropout: 0.0
```

---

## Step 3: Jalankan Training

### CLI

```powershell
cd E:\AI\sound-plan
.venv\Scripts\python.exe repos\VoxCPM\scripts\train_voxcpm_finetune.py `
    --config_path configs\voxcpm2_lora.yaml
```

### Atau via Web UI (lebih mudah)

```powershell
# Double-click file ini:
E:\AI\sound-plan\apps\voxcpm2-gradio\run_train.bat
```

Web UI akan:
1. Load model
2. Tampilkan form upload dataset
3. Konfig training parameters
4. Monitor progress real-time (loss graph)
5. Download checkpoint hasil training

---

## Step 4: Gunakan Model Hasil Training

```python
from voxcpm import VoxCPM

model = VoxCPM.from_pretrained(
    "E:/AI/sound-plan/models/voxcpm2",
    lora_path="E:/AI/sound-plan/models/voxcpm2-ft-lora/checkpoint_1000"
)

wav = model.generate(text="Halo, ini suara custom hasil training.")
```

---

## Parameter Tuning

| Parameter | Default | Rekomendasi |
|-----------|:------:|-------------|
| `learning_rate` | 1e-4 (LoRA) | Turunkan ke 5e-5 jika loss naik-turun |
| `r` (LoRA rank) | 32 | 16 untuk dataset kecil, 64 untuk dataset besar |
| `batch_size × grad_accum` | 16 | Sesuaikan VRAM; VRAM habis → kecilkan |
| `max_steps` | 1000 | Monitor loss; stop kalau overfit |
| `warmup_steps` | 100 | 10% dari total steps |

---

## Web UI Training — Fitur

| Fitur | Keterangan |
|-------|-----------|
| Upload dataset | JSONL via UI |
| Real-time loss graph | TensorBoard-style di browser |
| Audio preview | Dengerin sample hasil tiap N step |
| Download checkpoint | Ambil .pth hasil training |
| Resume training | Dari checkpoint terakhir |
| Multi-language support | EN + ZH UI |

---

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Out of memory (OOM) | Turunkan `batch_size` ke 1, `max_batch_tokens` ke 4096 |
| Suara tidak mirip | Tambah dataset (10-20 menit), cek kualitas rekaman |
| Suara pecah / noise | Turunkan `learning_rate`, cek audio bersih dari noise |
| Training terlalu lambat | Install Triton (`pip install triton`) untuk torch.compile |
| Loss NaN | Restart dari awal, turunkan LR, cek data tidak korup |
| Port 7860 sudah dipakai | Tutup app TTS (run.bat) dulu, baru run training |
