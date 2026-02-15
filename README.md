# ComfyUI-LLMs-Toolkit

<div align="center">

**Language / 语言切换**

[![English](https://img.shields.io/badge/README-English-blue?style=for-the-badge)](README.md)
[![简体中文](https://img.shields.io/badge/README-简体中文-red?style=for-the-badge)](README_CN.md)

---

[![GitHub Stars](https://img.shields.io/github/stars/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&logo=github&color=yellow)](https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&logo=github&color=green)](https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit/network)
[![GitHub Issues](https://img.shields.io/github/issues/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&logo=github&color=red)](https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit/issues)
[![License](https://img.shields.io/github/license/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&color=blue)](LICENSE)

**A Lightweight LLM Integration Suite for ComfyUI**

</div>

---

## 📖 Introduction

ComfyUI-LLMs-Toolkit is a streamlined extension for ComfyUI that enables seamless integration with major Large Language Models (LLMs) like GPT-4o, Claude 3.5, DeepSeek, and Qwen via API calls. No local GPU resources required.

### ✨ Key Features

- **Zero Hardware Requirement** — Runs purely on APIs, no local GPU memory usage.
- **Multi-Model Support** — Integrated with top-tier providers (OpenAI, Anthropic, DeepSeek, Alibaba, etc.).
- **Secure & Flexible** — Environment variable-based configuration for safety and convenience.
- **Plug & Play** — One-click installation, ready to use in minutes.

---

## 🤖 Supported Models

### International Models

| Model | Provider | Key Strengths | Config Prefix |
|-------|----------|---------------|---------------|
| GPT-4o | OpenAI | Universal Intelligence, Multimodal | `OPENAI_` |
| Claude-3.5 | Anthropic | Coding, Nuanced Writing, Long Context | `CLAUDE_` |
| Gemini-Pro | Google | Multilingual, Search Grounding | `GEMINI_` |

### Domestic Models (CN)

| Model | Provider | Key Strengths | Config Prefix |
|-------|----------|---------------|---------------|
| DeepSeek-V3 | DeepSeek | Math, Coding, Cost-Effective | `DEEPSEEK_` |
| Qwen-Max | Alibaba | Multimodal, Chinese Proficiency | `QWEN_` |
| GLM-4 | Zhipu AI | Reasoning, Knowledge Retrieval | `GLM_` |
| Doubao-Pro | ByteDance | Creative Writing, Chat | `DOUBAO_` |
| Spark-Max | iFLYTEK | Language Understanding | `SPARK_` |
| Moonshot-V1 | Moonshot | Long Context Understanding | `MOONSHOT_` |

---

## 🚀 Quick Start

### Prerequisites

- Python >= 3.8
- Latest ComfyUI
- >= 4GB RAM
- Stable Internet Connection

### Installation

#### Option 1: ComfyUI Manager (Recommended)

1. Open **Manager** in ComfyUI.
2. Search for `ComfyUI-LLMs-Toolkit`.
3. Install and restart ComfyUI.

#### Option 2: Manual Installation

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit.git
cd ComfyUI-LLMs-Toolkit
pip install -r requirements.txt
```

### Configuration

1. Copy the environment template:

```bash
cp config/env.example .env
```

2. Edit `.env` and add your API keys:

```ini
# DeepSeek
DEEPSEEK_API_KEY=sk-your_deepseek_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL_NAME=deepseek-chat

# Qwen
QWEN_API_KEY=your_qwen_key_here
QWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1
QWEN_MODEL_NAME=qwen-max

# OpenAI
OPENAI_API_KEY=sk-your_openai_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4o-mini
```

### Getting API Keys

- **DeepSeek**: [platform.deepseek.com](https://platform.deepseek.com/) (Free credits for new users)
- **Qwen**: [dashscope.aliyun.com](https://dashscope.aliyun.com/)
- **OpenAI**: [platform.openai.com](https://platform.openai.com/)
- **Zhipu AI**: [open.bigmodel.cn](https://open.bigmodel.cn/)

### Usage

1. Restart ComfyUI.
2. Right-click > **Add Node** > **LLMs Toolkit**.
3. Select your desired node, configure, and connect!

---

## ❓ FAQ

<details>
<summary><strong>How do I get an API Key?</strong></summary>

Most providers offer free tiers or trials:
- **DeepSeek**: Generous initial credits.
- **OpenAI**: $5 free credit for new accounts.
- **Qwen**: High token limits for free tier.

</details>

<details>
<summary><strong>I'm getting connection errors.</strong></summary>

Common fixes:
1. Check your internet connection (and proxy/VPN if needed).
2. Verify your API Key and `BASE_URL`.
3. Check ComfyUI console logs for detailed error messages.

</details>

---

<div align="center">

**If you find this project helpful, please give it a Star! ⭐️**

[![GitHub](https://img.shields.io/badge/GitHub-@HuangYuChuh-181717?style=flat-square&logo=github)](https://github.com/HuangYuChuh)

</div>
