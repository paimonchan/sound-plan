import json, numpy as np
from voxcpm import VoxCPM
from voxcpm.model.voxcpm import LoRAConfig

print("Loading base model...")
m_base = VoxCPM.from_pretrained("E:/AI/sound-plan/models/voxcpm2", load_denoiser=False)

print("Loading LoRA model...")
cfg = json.load(open("E:/AI/sound-plan/models/voxcpm2-ft-training-news/latest/lora_config.json"))
m_lora = VoxCPM.from_pretrained("E:/AI/sound-plan/models/voxcpm2",
    lora_config=LoRAConfig(**cfg["lora_config"]),
    lora_weights_path="E:/AI/sound-plan/models/voxcpm2-ft-training-news/latest",
    load_denoiser=False)

print(f"LoRA enabled: {m_lora.lora_enabled}")
print(f"LoRA params: {len(m_lora.get_lora_state_dict())}")

print("Generating base...")
w1 = m_base.generate(text="こんにちは", cfg_value=2.0, inference_timesteps=10)
print("Generating LoRA...")
w2 = m_lora.generate(text="こんにちは", cfg_value=2.0, inference_timesteps=10)

diff = np.abs(w1 - w2).mean()
same = np.allclose(w1, w2)
print(f"Diff: {diff:.6f}")
print(f"Different: {'YES' if not same else 'NO - BUG! LoRA not applied!'}")
print(f"Base duration: {len(w1)/m_base.tts_model.sample_rate:.1f}s")
print(f"LoRA duration: {len(w2)/m_lora.tts_model.sample_rate:.1f}s")
