# VoxCPM Ecosystem

- **Repo**: <https://github.com/OpenBMB/VoxCPM>
- **Pinned version**: [main branch](https://github.com/OpenBMB/VoxCPM)
- **Status**: reviewed
- **Added**: 2026-05-23

---

## Repository Stats

| Metric | Value |
|--------|-------|
| Stars | ~7,400+ |
| Forks | ~1,500+ |
| Watchers | ~39 |
| License | Apache 2.0 |
| Primary Language | Python |
| Organization | [OpenBMB](https://github.com/OpenBMB) (Tsinghua University / BAAI) |
| Last Release | VoxCPM2 (Apr 16, 2026) |

---

## Model Variants

| Variant | Params | Languages | Key Feature |
|----------|:------:|:---------:|-------------|
| **VoxCPM2** | 2B | 30 | Full multilingual, voice design, 48kHz |
| VoxCPM2-Light | ~600M | 10 | Lightweight edge deployment |
| VoxCPM1.5 | 0.8B | 2 (zh, en) | GGUF quantized (VoxCPM.cpp), CPU-friendly |
| VoxCPM-0.5B | 0.6B | 2 (zh, en) | Smallest, ~5GB VRAM |

---

## HuggingFace Ecosystem

| Resource | Count |
|----------|:-----:|
| Spaces using VoxCPM2 | 49 |
| Finetunes | 10 |
| Quantizations | 6 |
| Downloads (VoxCPM2) | 199K/month |

---

## Related Projects

| Project | Description |
|---------|-------------|
| [VoxCPM.cpp](https://github.com/OpenBMB/VoxCPM.cpp) | GGUF quantized inference for CPU (VoxCPM1.5) |
| [Nano-VLLM](https://github.com/OpenBMB/Nano-VLLM) | Accelerated inference engine — 2x speedup on VoxCPM2 |
| [vLLM-omni](https://github.com/vllm-project/vllm-omni) | Official vLLM integration, includes benchmarks |

---

## Community

- Active spaces on HuggingFace for custom voice cloning, upscaling, API wrappers
- LoRA adapters for specific voices/styles
- Chinese + English Discord/WeChat community (via OpenBMB)
- Regular updates: last push Mar 2026

---

## License

Apache 2.0 — code and weights both free for commercial use.
VoxCPM also used at ICLR 2026 (VoxCPM v1 paper accepted).
