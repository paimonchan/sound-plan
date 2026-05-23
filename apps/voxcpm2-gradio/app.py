"""
VoxCPM2 Gradio Web UI
Local model path, no internet needed after first download.
Run: python app.py
"""
import gradio as gr
from voxcpm import VoxCPM
import numpy as np

MODEL_PATH = "E:/AI/sound-plan/models/voxcpm2"
LANGUAGES = {
    "Auto": None,
    "Indonesian": "id",
    "Japanese": "ja", "Chinese": "zh", "English": "en",
    "Korean": "ko", "Arabic": "ar", "Dutch": "nl",
    "French": "fr", "German": "de", "Greek": "el",
    "Hindi": "hi", "Italian": "it", "Malay": "ms",
    "Polish": "pl", "Portuguese": "pt", "Russian": "ru",
    "Spanish": "es", "Swedish": "sv", "Thai": "th",
    "Turkish": "tr", "Vietnamese": "vi",
}

model = None
model = VoxCPM.from_pretrained(MODEL_PATH, load_denoiser=False)

def generate_tts(text, ref_audio, voice_design, timesteps, cfg):
    if not text.strip():
        return None, "Masukkan teks terlebih dahulu"
    try:
        if voice_design.strip():
            full_text = f"({voice_design}){text}"
            wav = model.generate(text=full_text, cfg_value=cfg, inference_timesteps=int(timesteps))
        elif ref_audio:
            wav = model.generate(text=text, reference_wav_path=ref_audio, cfg_value=cfg, inference_timesteps=int(timesteps))
        else:
            wav = model.generate(text=text, cfg_value=cfg, inference_timesteps=int(timesteps))

        sr = model.tts_model.sample_rate
        wav = wav.astype("float32")

        if wav.max() > 1.0 or wav.min() < -1.0:
            wav = wav / max(abs(wav.max()), abs(wav.min()))

        duration = len(wav) / sr
        return (sr, wav), f"OK {duration:.1f}s | RTX 5070 | VoxCPM2"
    except Exception as e:
        return None, f"Error: {e}"

def clear_fields():
    return "", None, "", 10, 2.0, None, ""

with gr.Blocks(title="VoxCPM2 TTS", theme=gr.themes.Soft()) as app:
    gr.Markdown("# VoxCPM2 Text-to-Speech")
    gr.Markdown(f"Model: `{MODEL_PATH}` | 30 languages | GPU: RTX 5070 12GB")

    with gr.Row():
        with gr.Column(scale=2):
            text = gr.Textbox(label="Text", placeholder="Ketik teks di sini...", lines=4)
            with gr.Row():
                ref_audio = gr.Audio(label="Reference audio (voice clone)", type="filepath", sources=["upload"])
                voice_design = gr.Textbox(label="Voice design (teks → suara)", placeholder="contoh: young woman, cheerful voice")
            with gr.Row():
                timesteps = gr.Slider(5, 20, value=10, step=1, label="Timesteps (lebih tinggi = kualitas)")
                cfg = gr.Slider(1.0, 3.0, value=2.0, step=0.1, label="CFG (prompt adherence)")

        with gr.Column(scale=1):
            generate_btn = gr.Button("Generate", variant="primary", size="lg")
            audio_out = gr.Audio(label="Output", type="numpy")
            status = gr.Textbox(label="Status", interactive=False)
            gr.Examples([
                ["Halo semuanya! Selamat datang di demo VoxCPM2.", None, "", 10, 2.0],
                ["こんにちは、皆さん。VoxCPM2の日本語デモへようこそ。", None, "", 10, 2.0],
            ], [text, ref_audio, voice_design, timesteps, cfg], label="Contoh")

    generate_btn.click(fn=generate_tts, inputs=[text, ref_audio, voice_design, timesteps, cfg], outputs=[audio_out, status])
    gr.ClearButton([text, ref_audio, voice_design, timesteps, cfg, audio_out, status])

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)
