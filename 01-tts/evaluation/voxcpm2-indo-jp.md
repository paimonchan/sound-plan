# VoxCPM2 — Indonesia & Japanese Evaluation

- **Status**: reviewed
- **Added**: 2026-05-23

---

## Summary

VoxCPM2 adalah TTS open-source terbaik untuk bahasa Indonesia dan Jepang saat ini.
Menang di speaker similarity di kedua bahasa, dengan lisensi Apache 2.0.

---

## Indonesian — Detailed Breakdown

### Intelligibility (WER↓, makin rendah makin jelas)

| Model | WER | License |
|-------|:---:|---------|
| ElevenLabs (commercial) | 1.06% | Commercial |
| MiniMax (commercial) | 1.24% | Commercial |
| **VoxCPM2** | **1.36%** | Apache 2.0 |
| Fish S2 Pro | 1.68% | Research |
| OmniVoice | 1.97% | Apache 2.0 |

### Speaker Similarity (SIM↑, makin tinggi makin mirip)

| Model | SIM | License |
|-------|:---:|---------|
| **VoxCPM2** | **80.0%** 🥇 | Apache 2.0 |
| OmniVoice | 80.5% 🥇 | Apache 2.0 |
| Fish S2 Pro | 76.3% | Research |
| MiniMax | 72.9% | Commercial |
| ElevenLabs | 66.0% | Commercial |

**Verdict**: VoxCPM2 SIM #1 (tie dengan OmniVoice). WER competitive (kalah tipis dari ElevenLabs proprietary). Apache 2.0 = komersial bebas.

---

## Japanese — Detailed Breakdown

### Intelligibility (CER↓, makin rendah makin jelas)

| Model | CER | License |
|-------|:---:|---------|
| **Fish S2 Pro** | **1.82%** 🥇 | Research |
| VoxCPM2 | 2.40% | Apache 2.0 |
| MiniMax | 3.52% | Commercial |
| OmniVoice | 4.03% | Apache 2.0 |
| ElevenLabs | 10.65% | Commercial |

### Speaker Similarity (SIM↑)

| Model | SIM | License |
|-------|:---:|---------|
| **VoxCPM2** | **82.8%** 🥇 | Apache 2.0 |
| OmniVoice | 82.8% 🥇 | Apache 2.0 |
| Fish S2 Pro | 79.6% | Research |
| MiniMax | 77.6% | Commercial |
| ElevenLabs | 73.8% | Commercial |

**Verdict**: VoxCPM2 SIM #1 (tie). CER #2 after Fish S2 Pro. Fish lebih akurat baca Jepang tapi lisensi proprietary — kalo butuh komersial, VoxCPM2 pilihan terbaik.

---

## Cross-lingual Voice Cloning

VoxCPM2 mendukung cross-lingual cloning — referensi suara dari bahasa A, output di bahasa B.
Contoh: cloning suara Indonesia → output bahasa Jepang (atau sebaliknya).

Dari demo page VoxCPM2, sample cross-lingual Jepang tersedia:
- Voice transfer ke berbagai bahasa termasuk Jepang
- Style control dalam cross-lingual: (slightly faster, cheerful tone) + Japanese text

---

## Sample Demo (dari VoxCPM2 Demo Page)

### Indonesian

> "Sumpah deh, bos gue tuh toxic banget! Masa disuruh ngerjain laporan mepet deadline, padahal dia yang lupa ngasih tau dari kemarin. Gaji UMR tapi kerjaan kayak CEO, capek banget gue."

### Japanese

> "次はー、新宿ー、新宿です。お出口は右側です。中央線、埼京線、湘南新宿ライン、地下鉄各線はお乗り換えです。ドア付近のお客様、閉まるドアにご注意ください。"

### Cross-lingual Japanese

> "皆さん、こんにちは。VoxCPM2の音声合成デモへようこそ。今日は異なる言語でクロスリンガル音声変換の効果をお見せします。"

Samples available at: <https://openbmb.github.io/voxcpm2-demopage/>

---

## Use Case Recommendations

| Use Case | Recommendation | Reason |
|----------|---------------|--------|
| Voice cloning komersial Indo+Jepang | VoxCPM2 | SIM #1, Apache 2.0, gratis |
| Akurasi baca Jepang tertinggi | Fish S2 Pro | CER 1.82% tapi proprietary |
| Cakupan bahasa terbanyak | OmniVoice | 600+ bahasa, competitive SIM |
| On-device / no GPU | Supertone-3 | CPU-only, tapi cloning bayar |
| Budget nol + kualitas oke | VoxCPM2 | Gratis total, Apache 2.0 |

---

## Fine-tuning Recommendations

Untuk hasil terbaik di bahasa Indonesia/Jepang:

1. **Siapkan dataset**: 5-10 menit audio berkualitas + transkrip
2. **LoRA fine-tune**: `conf/voxcpm_v2/voxcpm_finetune_lora.yaml`
3. **Evaluasi**: WER/CER dengan Whisper ASR, SIM dengan ECAPA-TDNN
4. **Iterasi**: adjust `cfg_value` 1.0-2.0, `inference_timesteps` 5-15
