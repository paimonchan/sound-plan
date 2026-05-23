"""
VoxCPM2 Gradio Web UI — Voice Clone + LoRA
Run: python app.py or double-click run.bat
"""
import json
import gradio as gr
import numpy as np
from pathlib import Path
from voxcpm import VoxCPM
from voxcpm.model.voxcpm import LoRAConfig

MODEL_PATH = "E:/AI/sound-plan/models/voxcpm2"
LORA_DIR = Path("E:/AI/sound-plan/models")
model = None
current_lora = None

def find_loras():
    found = [("None (base model)", None)]
    for lora_dir in sorted(LORA_DIR.glob("voxcpm2-ft-*/latest"), reverse=True):
        if (lora_dir / "lora_weights.safetensors").exists():
            found.append((lora_dir.parent.name, lora_dir))
    return found

def load_model(lora_path=None):
    global model, current_lora
    if lora_path == current_lora:
        return
    current_lora = lora_path
    kwargs = {"load_denoiser": False}
    if lora_path:
        cfg_file = lora_path / "lora_config.json"
        if cfg_file.exists():
            cfg_data = json.loads(cfg_file.read_text())
            kwargs["lora_config"] = LoRAConfig(**cfg_data["lora_config"])
        kwargs["lora_weights_path"] = str(lora_path)
    model = VoxCPM.from_pretrained(MODEL_PATH, **kwargs)

loras = find_loras()
lora_names = [l[0] for l in loras]
load_model(None)

def generate_tts(text, mode, lora_label, ref_audio, voice_design, cfg, timesteps):
    if not text.strip():
        return None, "Masukkan teks"
    try:
        # Load LoRA if selected
        lora_path = None
        if mode == "LoRA (trained)" and lora_label != "None (base model)":
            for label, path in loras:
                if label == lora_label:
                    lora_path = path
                    break
        load_model(lora_path)

        # Generate based on mode
        if mode == "Voice Design (teks)" and voice_design.strip():
            full_text = f"({voice_design}){text}"
            wav = model.generate(text=full_text, cfg_value=cfg, inference_timesteps=int(timesteps))
        elif mode == "Voice Clone (ref)" and ref_audio:
            wav = model.generate(text=text, reference_wav_path=ref_audio, cfg_value=cfg, inference_timesteps=int(timesteps))
        else:
            wav = model.generate(text=text, cfg_value=cfg, inference_timesteps=int(timesteps))

        sr = model.tts_model.sample_rate
        wav = wav.astype("float32")
        if wav.max() > 1.0 or wav.min() < -1.0:
            wav = wav / max(abs(wav.max()), abs(wav.min()))
        duration = len(wav) / sr
        tags = []
        if lora_path: tags.append("LoRA")
        if ref_audio: tags.append("Clone")
        if voice_design.strip(): tags.append("Design")
        tag = "+".join(tags) if tags else "Base"
        return (sr, wav), f"OK {duration:.1f}s | {tag} | RTX 5070"
    except Exception as e:
        return None, f"Error: {e}"

with gr.Blocks(title="VoxCPM2 TTS", theme=gr.themes.Soft()) as app:
    gr.Markdown("# VoxCPM2 Text-to-Speech")
    gr.Markdown(f"`{MODEL_PATH}` | RTX 5070 12GB | {len(loras)-1} LoRA(s)")

    with gr.Row():
        with gr.Column(scale=2):
            text = gr.Textbox(label="Text", placeholder="Ketik teks di sini...", lines=4)

            mode = gr.Radio(
                choices=["Base (no voice)", "Voice Clone (ref)", "Voice Design (teks)", "LoRA (trained)"],
                value="Base (no voice)", label="Mode"
            )

            with gr.Column(visible=False) as clone_col:
                ref_audio = gr.Audio(label="Reference audio (3-10 detik)", type="filepath")

            with gr.Column(visible=False) as design_col:
                voice_design = gr.Textbox(label="Voice design", placeholder="contoh: young woman, cheerful, high pitch")

            with gr.Column(visible=True) as lora_col:
                lora_dropdown = gr.Dropdown(choices=lora_names, value=lora_names[0], label="LoRA checkpoint")

            timesteps = gr.Slider(5, 20, value=10, step=1, label="Timesteps")
            cfg = gr.Slider(1.0, 3.0, value=2.0, step=0.1, label="CFG")

        with gr.Column(scale=1):
            generate_btn = gr.Button("Generate", variant="primary", size="lg")
            audio_out = gr.Audio(label="Output", type="numpy")
            status = gr.Textbox(label="Status", interactive=False)

    # Show/hide panels based on mode
    def toggle_mode(m):
        return (
            gr.update(visible=(m == "Voice Clone (ref)")),
            gr.update(visible=(m == "Voice Design (teks)")),
            gr.update(visible=(m == "LoRA (trained)"))
        )
    mode.change(toggle_mode, mode, [clone_col, design_col, lora_col])

    generate_btn.click(
        fn=generate_tts,
        inputs=[text, mode, lora_dropdown, ref_audio, voice_design, cfg, timesteps],
        outputs=[audio_out, status]
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)
