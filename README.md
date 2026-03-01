# ComfyUI-LLMs-Toolkit

<div align="center">

**Language / 语言切换**

[![English](https://img.shields.io/badge/README-English-blue?style=for-the-badge)](readme_en.md)
[![简体中文](https://img.shields.io/badge/README-简体中文-red?style=for-the-badge)](../README.md)

---

[![GitHub Stars](https://img.shields.io/github/stars/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&logo=github&color=yellow)](https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&logo=github&color=green)](https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit/network)
[![GitHub Issues](https://img.shields.io/github/issues/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&logo=github&color=red)](https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit/issues)
[![License](https://img.shields.io/github/license/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&color=blue)](../LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&color=orange)](https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit/commits)

**Inject powerful Large Language Models into your ComfyUI workflows!**

*A professional-grade ComfyUI custom node suite supporting world-leading Large Language Models*

</div>

---

## Project Overview

ComfyUI-LLMs-Toolkit is a high-performance ComfyUI extension designed for AI creators. Through a lightweight API-driven approach, you can easily integrate world-class Large Language Models like DeepSeek, Qwen, GPT, etc., even with limited computational resources, democratizing AI creation.

### Why Choose Us?

- **Zero Hardware Barrier**: No high-end GPU required, enjoy cutting-edge AI capabilities with just APIs
- **Global Model Support**: Integrated mainstream LLMs worldwide, one-stop solution
- **High-Performance Architecture**: Optimized concurrent processing, dramatically improving workflow efficiency
- **Developer Friendly**: Environment variable configuration, Docker support, developer-first approach

---

## Core Features

### Powerful LLM Ecosystem

| Category | Supported Models | Key Capabilities |
|----------|------------------|------------------|
| **Chinese Leaders** | DeepSeek-V3, Qwen-Max, GLM-4 | Chinese understanding, code generation, mathematical reasoning |
| **International Giants** | GPT-4, Claude-3, Gemini | Multimodal processing, creative writing, complex reasoning |
| **Professional Vertical** | Doubao, Spark, Moonshot | Dialogue generation, long text, role-playing |

### Technical Highlights

- **Lightning Deployment**: One-click installation, get started in 5 minutes
- **Concurrency Optimization**: Multi-threading processing, supports batch requests
- **Security First**: Environment variable configuration, secure API key management
- **Hot Reload**: Dynamic configuration updates, no need to restart ComfyUI
- **Smart Caching**: Response caching mechanism, reducing API call costs
- **Containerized**: Docker support, consistent deployment environment

---

## Quick Start

### System Requirements

- **Python**: `>= 3.8`
- **ComfyUI**: Latest version
- **Memory**: `>= 4GB RAM`
- **Network**: Stable internet connection

### Lightning Installation

```bash
# Method 1: Git Clone (Recommended)
cd ComfyUI/custom_nodes/
git clone https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit.git
cd ComfyUI-LLMs-Toolkit

# Install Dependencies
pip install -r requirements.txt
```

```bash
# Method 2: Docker Deployment
docker pull your-dockerhub/comfyui-llms-toolkit:latest
docker run -d --name comfyui-llms -p 8188:8188 your-dockerhub/comfyui-llms-toolkit
```

### Environment Configuration

#### 1. Create Configuration File

```bash
# Copy environment variable template
cp config/env.example .env
```

#### 2. Configure API Keys

Edit the `.env` file and select the models you want to use:

```bash
# DeepSeek (Recommended for beginners)
DEEPSEEK_API_KEY=sk-your_deepseek_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL_NAME=deepseek-chat

# Qwen (Chinese optimized)
QWEN_API_KEY=your_qwen_key_here
QWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1
QWEN_MODEL_NAME=qwen-max

# OpenAI GPT (International standard)
OPENAI_API_KEY=sk-your_openai_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4o-mini

# More configurations see config/env.example
```

#### 3. API Key Acquisition Guide

| Provider | Get Address | Free Credits | Rating |
|-------------|----------------|-----------------|-----------|
| **DeepSeek** | [platform.deepseek.com](https://platform.deepseek.com/) | ¥500 free credits | ⭐⭐⭐⭐⭐ |
| **Qwen** | [dashscope.aliyun.com](https://dashscope.aliyun.com/) | 1M tokens/month | ⭐⭐⭐⭐ |
| **OpenAI** | [platform.openai.com](https://platform.openai.com/) | $5 trial credits | ⭐⭐⭐⭐⭐ |
| **GLM** | [open.bigmodel.cn](https://open.bigmodel.cn/) | 5M tokens/month | ⭐⭐⭐⭐ |

### First Run

1. **Restart ComfyUI**:
   ```bash
   # Restart ComfyUI to load new nodes
   cd /path/to/ComfyUI
   python main.py
   ```

2. **Find Nodes**:
   - Right-click in ComfyUI interface
   - Navigate to `Add Node` -> `LLMs Toolkit`
   - Select the node type you need

3. **Start Creating**:
   - Drag in LLM nodes
   - Configure model parameters
   - Connect inputs and outputs
   - Enjoy your AI creation journey!

---

## Supported Model Matrix

### Chinese AI Champions

| Model | Provider | Core Advantages | Price Level | Config Prefix |
|-------|----------|-----------------|-------------|---------------|
| **DeepSeek-V3** | DeepSeek | Mathematical reasoning, Code generation | Ultra-low | `DEEPSEEK_` |
| **Qwen-Max** | Alibaba | Multimodal, Chinese optimization | Medium | `QWEN_` |
| **GLM-4** | Zhipu AI | Logical reasoning, Knowledge Q&A | Low | `GLM_` |
| **Doubao-Pro** | ByteDance | Dialogue generation, Creative writing | Medium | `DOUBAO_` |
| **Spark-Max** | iFLYTEK | Language understanding, Text analysis | Low | `SPARK_` |
| **Moonshot-V1** | Moonshot AI | Long text, Deep understanding | Medium | `MOONSHOT_` |

### International AI Giants

| Model | Provider | Core Advantages | Price Level | Config Prefix |
|-------|----------|-----------------|-------------|---------------|
| **GPT-4o** | OpenAI | General intelligence, Multimodal | High | `OPENAI_` |
| **Claude-3.5** | Anthropic | Safe dialogue, Long text | High | `CLAUDE_` |
| **Gemini-Pro** | Google | Search enhanced, Multilingual | Medium | `GEMINI_` |

---

## FAQ

<details>
<summary><strong>Q: How to get API keys?</strong></summary>

**A**: All major vendors provide free trial credits:
- **DeepSeek**: Register and get ¥500 credits, suitable for beginners
- **Qwen**: Large quota available after Alibaba Cloud account verification
- **OpenAI**: New users get $5 free credits, requires international payment method

</details>

<details>
<summary><strong>Q: Does it support local models?</strong></summary>

**A**: Currently mainly supports API calls, local model support is on the development roadmap:
- **v2.0**: Planned support for Ollama local models
- **v2.1**: Support for GGUF format models
- **v3.0**: Support for custom model fine-tuning

</details>

<details>
<summary><strong>Q: What to do when encountering connection errors?</strong></summary>

**A**: Common solutions:
1. **Check network**: Ensure access to corresponding API services
2. **Verify keys**: Confirm API keys are correct and have balance
3. **Check configuration**: Confirm BASE_URL format is correct
4. **View logs**: Check ComfyUI console output

</details>

---

## 📅 Changelog

### [1.1.0] - 2026-03-01

#### ✨ Added
- **DeepSeek Reasoning Support**: Supported extracting deep thinking processes (`reasoning_content`) from DeepSeek R1 models, exposing it to a dedicated `reasoning` output pin in the generic node.
- **o1/o3 Model System Role Compatibility**: Integrated a downgrade workaround for strict 'o1/o3' models by spoofing an `assistant` acceptance response.

#### 🛠 Changed
- **Shared API Client Refactor**: Extracted HTTP request logic to `api_client.py` for smarter retrying equipped with Exponential Backoff & Jitter.
- **Graceful Error Degradation**: The API node now outputs readable text error traces instead of throwing Python Exceptions, preventing ComfyUI workflows from halting abruptly.
- **User-Agent Masquerade**: Added browser-standard `User-Agent` headers to successfully bypass HTTP 403 (Cloudflare Error 1010) on proxy platforms.

#### 🐛 Fixed
- **Multi-turn Memory Fix**: Fixed `openai_compatible.py` to properly store `assistant` responses when `enable_memory` is toggled on.
- **Node Parameter Deserialization Bug UI**: Switched from dynamic widgets to naive `<canvas>` element drawings to fix the notorious parameter shift bug caused by `token_usage_display`.

---

## Open Source License

This project is licensed under **[GNU General Public License v2.0](../LICENSE)**.

**This means:**
- **Free to use**: Both personal and commercial use
- **Free to modify**: You can modify the source code
- **Free to distribute**: You can distribute original or modified versions
- **Open source obligation**: Modified versions must be open source

---

<div align="center">

### If this project helps you, please give us a Star!

[![Star History Chart](https://api.star-history.com/svg?repos=HuangYuChuh/ComfyUI-LLMs-Toolkit&type=Date)](https://star-history.com/#HuangYuChuh/ComfyUI-LLMs-Toolkit&Date)

**Contact Us**

[![GitHub](https://img.shields.io/badge/GitHub-@HuangYuChuh-181717?style=flat-square&logo=github)](https://github.com/HuangYuChuh)
[![Email](https://img.shields.io/badge/Email-Contact-red?style=flat-square&logo=gmail)](mailto:your-email@example.com)

---

**Made with love for the ComfyUI community**

*Making AI creation simpler, making technology more humane*

</div>
