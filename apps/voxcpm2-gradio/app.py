"""
VoxCPM2 Gradio Web UI with LoRA support
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
    """Find all LoRA checkpoints, return [(label, path), ...]"""
    found = [("None (base model)", None)]
    for lora_dir in sorted(LORA_DIR.glob("voxcpm2-ft-*/latest"), reverse=True):
        if (lora_dir / "lora_weights.safetensors").exists():
            parent = lora_dir.parent.name
            found.append((parent, lora_dir))
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
load_model(None)

def generate_tts(text, lora_label, cfg, timesteps):
    if not text.strip():
        return None, "Masukkan teks"
    try:
        lora_path = None
        for label, path in loras:
            if label == lora_label:
                lora_path = path
                break
        load_model(lora_path)
        wav = model.generate(text=text, cfg_value=cfg, inference_timesteps=int(timesteps))
        sr = model.tts_model.sample_rate
        wav = wav.astype("float32")
        if wav.max() > 1.0 or wav.min() < -1.0:
            wav = wav / max(abs(wav.max()), abs(wav.min()))
        duration = len(wav) / sr
        tag = "LoRA" if lora_path else "Base"
        return (sr, wav), f"OK {duration:.1f}s | {tag} | RTX 5070"
    except Exception as e:
        return None, f"Error: {e}"

lora_names = [l[0] for l in loras]

with gr.Blocks(title="VoxCPM2 TTS", theme=gr.themes.Soft()) as app:
    gr.Markdown("# VoxCPM2 Text-to-Speech")
    gr.Markdown(f"`{MODEL_PATH}` | RTX 5070 12GB | {len(loras)-1} LoRA(s)")

    with gr.Row():
        with gr.Column(scale=2):
            text = gr.Textbox(label="Text", placeholder="Ketik teks...", lines=4)
            lora_dropdown = gr.Dropdown(choices=lora_names, value=lora_names[0], label="Voice (LoRA)")
            timesteps = gr.Slider(5, 20, value=10, step=1, label="Timesteps")
            cfg = gr.Slider(1.0, 3.0, value=2.0, step=0.1, label="CFG")
        with gr.Column(scale=1):
            generate_btn = gr.Button("Generate", variant="primary", size="lg")
            audio_out = gr.Audio(label="Output", type="numpy")
            status = gr.Textbox(label="Status", interactive=False)

    generate_btn.click(fn=generate_tts, inputs=[text, lora_dropdown, cfg, timesteps], outputs=[audio_out, status])

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)
