# AI Song Creation — Complete Guide (May 2026)

- **Status**: reviewed
- **Added**: 2026-05-24

---

## 3 Cara Bikin Lagu Baru dari Nol

### A. Full Song Generation (paling gampang) 🏆

**Tools: ACE-Step 1.5** (MIT, 10.4K★)

Ketik lirik + deskripsi style → 1 lagu lengkap (vocal+music) dalam hitungan detik.

```
Caption: "Upbeat J-pop, female vocal, energetic, 140 BPM"
Lyrics:
[Verse 1]
朝日が昇る街角で
新しい一日が始まる

[Chorus]
走り出せ！今すぐに！
夢を追いかけて！

[Bridge]
[Instrumental]

[Chorus]
走り出せ！今すぐに！
```

**Kelebihan**: Cepat, gratis, <4GB VRAM, 50+ bahasa, bisa bikin instrumental aja
**Kekurangan**: Vocal quality belum selevel Suno v5, kadang hasilnya random (generate 2-3x)

### B. Singing Voice Synthesis (kontrol penuh)

**Tools: DiffSinger** (Apache 2.0, 3K★) + instrumental terpisah

1. Bikin melodi di MIDI editor / DAW
2. Tulis lirik + MIDI notes → DiffSinger → vocal track
3. Gabungin dengan instrumental (ACE-Step atau produksi sendiri)

**Kelebihan**: Kontrol penuh pitch, timing, vibrato. Kualitas produksi.
**Kekurangan**: Perlu dataset training (~5 jam audio), butuh MIDI skill, workflow panjang

### C. Singing Voice Conversion (pakai suara sendiri)

**Tools: RVC / GPT-SoVITS** (MIT, 56K★)

1. Rekam diri sendiri nyanyi (atau render dari TTS manapun)
2. RVC convert → suara karakter target
3. Melodi & lirik preserved dari rekaman asli

**Kelebihan**: 10 menit training data, real-time capable, bahasa apapun
**Kekurangan**: Bukan bikin lagu dari nol, hanya mengubah suara

---

## Perbandingan

| | ACE-Step 1.5 | DiffSinger | RVC/GPT-SoVITS |
|---|:---:|:---:|:---:|
| **Bikin lagu dari nol** | ✅ Ya | ✅ Ya | ❌ (konversi aja) |
| **Butuh skill musik** | ❌ Gak perlu | ⚠️ MIDI | ❌ Gak perlu |
| **Kontrol pitch/timing** | Prompt aja | Full via MIDI | Ikut source |
| **Waktu setup** | 30 menit | Beberapa hari | 1-2 jam |
| **Kualitas vocal** | Good | Excellent | Very Good |
| **VRAM (RTX 5070)** | <4 GB | ~8 GB | ~6 GB |
| **Bahasa** | 50+ (incl Indo?) | Dataset dependent | Language agnostic |
| **Lisensi** | MIT | Apache 2.0 | MIT |

---

## Rekomendasi berdasarkan tujuan

| Tujuan | Tools | Kenapa |
|--------|-------|-------|
| **Coba bikin lagu sekarang** | ACE-Step 1.5 | 1 command, langsung jadi |
| **Karakter anime nyanyi** | RVC + ACE-Step | Rekam → convert suara |
| **Produksi profesional** | DiffSinger + DAW | Kontrol penuh, export ke OpenUTAU |
| **Vocal aja, music sendiri** | DiffSinger | Paling akurat, MIDI-based |
| **Bikin banyak lagu cepet** | ACE-Step 1.5 batch | Generate 4-8 sekaligus, pilih yang bagus |

---

## Workflow ACE-Step 1.5 (rekomendasi untuk pemula)

```powershell
# Install
git clone https://github.com/ace-step/ACE-Step-1.5.git
cd ACE-Step-1.5
pip install -r requirements.txt

# Download model
python scripts/download_model.py

# Generate lagu
python -c "
from acestep import ACEInference
model = ACEInference.from_pretrained('ace-step/ace-step-1.5')
result = model.generate(
    prompt='Upbeat pop song, female vocal, 120 BPM, C major',
    lyrics='[Verse]\nWalking through the rain\nThinking of your smile\n\n[Chorus]\nWe rise together\nInto the light\n',
    duration_seconds=120
)
result.save('my_song.wav')
"
```

### Prompt structure untuk ACE-Step:

```yaml
Caption (style):
  "Genre, mood, instruments, BPM, key, vocal gender"
  Contoh: "J-pop idol song, energetic, female vocal, 140 BPM, D major"

Lyrics (structure + words):
  [Intro] - optional instrumental intro
  [Verse 1] - verse lyrics (6-10 syllables per line)
  [Chorus] - chorus lyrics
  [Bridge] - bridge section
  [Instrumental] - solos/breaks
  [Outro] - ending

Tips:
  - Generate 3-4 variations, pilih yang paling bagus
  - Gunakan Repaint untuk fix bagian tertentu
  - Gunakan Cover untuk restyle lagu existing
```

---

## Untuk Lagu Bahasa Indonesia

ACE-Step 1.5 claims 50+ languages. Perlu di-test apakah Indonesian berfungsi dengan baik. Alternatif jika ACE-Step gak cocok:

1. **RVC path**: Rekam suara nyanyi Indo → convert ke karakter target
2. **DiffSinger path**: Train dataset nyanyi Indo → synthesis dengan lirik Indo
3. **ACE-Step path**: Coba generate dengan lirik Indo, iterate prompt

---

## Next untuk project ini

1. **Install ACE-Step 1.5** — full song generation, test lirik Indo
2. **Install GPT-SoVITS/RVC** — singing voice conversion, test suara karakter
3. **DiffSinger research** — jika butuh kontrol profesional
