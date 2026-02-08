# ComfyUI-LLMs-Toolkit

<div align="center">

**Language / 语言切换**

[![简体中文](https://img.shields.io/badge/README-简体中文-red?style=for-the-badge)](README.md)
[![English](https://img.shields.io/badge/README-English-blue?style=for-the-badge)](docs/readme_en.md)

---

[![GitHub Stars](https://img.shields.io/github/stars/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&logo=github&color=yellow)](https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&logo=github&color=green)](https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit/network)
[![GitHub Issues](https://img.shields.io/github/issues/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&logo=github&color=red)](https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit/issues)
[![License](https://img.shields.io/github/license/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&color=blue)](LICENSE)

**为 ComfyUI 接入主流大语言模型的轻量级节点套件**

</div>

---

## 项目简介

ComfyUI-LLMs-Toolkit 是一个轻量级的 ComfyUI 扩展，通过 API 调用的方式，让用户无需本地部署即可在工作流中使用 DeepSeek、通义千问、GPT 等主流大语言模型。

### 核心优势

- **零硬件门槛** — 无需 GPU，仅需 API 密钥即可使用
- **多模型支持** — 集成国内外主流 LLM 服务商
- **配置灵活** — 环境变量管理，安全便捷
- **开箱即用** — 一键安装，五分钟上手

---

## 支持的模型

### 国内模型

| 模型 | 提供商 | 核心优势 | 配置前缀 |
|------|--------|----------|----------|
| DeepSeek-V3 | DeepSeek | 数学推理、代码生成 | `DEEPSEEK_` |
| Qwen-Max | 阿里巴巴 | 多模态、中文优化 | `QWEN_` |
| GLM-4 | 智谱AI | 逻辑推理、知识问答 | `GLM_` |
| Doubao-Pro | 字节跳动 | 对话生成、创意写作 | `DOUBAO_` |
| Spark-Max | 科大讯飞 | 语言理解、文本分析 | `SPARK_` |
| Moonshot-V1 | 月之暗面 | 长文本、深度理解 | `MOONSHOT_` |

### 国际模型

| 模型 | 提供商 | 核心优势 | 配置前缀 |
|------|--------|----------|----------|
| GPT-4o | OpenAI | 通用智能、多模态 | `OPENAI_` |
| Claude-3.5 | Anthropic | 安全对话、长文本 | `CLAUDE_` |
| Gemini-Pro | Google | 搜索增强、多语言 | `GEMINI_` |

---

## 快速开始

### 系统要求

- Python >= 3.8
- ComfyUI 最新版本
- 内存 >= 4GB RAM
- 稳定的网络连接

### 安装

#### 方法一：ComfyUI Manager（推荐）

1. 在 ComfyUI 中打开 Manager 面板
2. 搜索 `ComfyUI-LLMs-Toolkit`
3. 点击安装并重启 ComfyUI

#### 方法二：手动安装

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit.git
cd ComfyUI-LLMs-Toolkit
pip install -r requirements.txt
```

### 配置

1. 复制环境变量模板：

```bash
cp config/env.example .env
```

2. 编辑 `.env` 文件，配置你需要的 API 密钥：

```bash
# DeepSeek
DEEPSEEK_API_KEY=sk-your_deepseek_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL_NAME=deepseek-chat

# 通义千问
QWEN_API_KEY=your_qwen_key_here
QWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1
QWEN_MODEL_NAME=qwen-max

# OpenAI
OPENAI_API_KEY=sk-your_openai_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4o-mini
```

### API 密钥获取

| 提供商 | 获取地址 | 免费额度 |
|--------|----------|----------|
| DeepSeek | [platform.deepseek.com](https://platform.deepseek.com/) | ¥500 |
| 通义千问 | [dashscope.aliyun.com](https://dashscope.aliyun.com/) | 每月 100 万 tokens |
| OpenAI | [platform.openai.com](https://platform.openai.com/) | $5 |
| 智谱清言 | [open.bigmodel.cn](https://open.bigmodel.cn/) | 每月 500 万 tokens |

### 使用

1. 重启 ComfyUI
2. 右键添加节点，导航至 `Add Node` → `LLMs Toolkit`
3. 选择需要的节点，配置参数，连接工作流

---

## 常见问题

<details>
<summary><strong>如何获取 API 密钥？</strong></summary>

各厂商都提供免费试用额度：
- DeepSeek：注册即送 ¥500 额度
- 通义千问：阿里云账号认证后可获得大额度
- OpenAI：新用户有 $5 免费额度

</details>

<details>
<summary><strong>遇到连接错误怎么办？</strong></summary>

常见解决方案：
1. 检查网络是否能访问对应 API 服务
2. 确认 API 密钥正确且有余额
3. 确认 BASE_URL 格式正确
4. 查看 ComfyUI 控制台日志

</details>

---

<div align="center">

**如果这个项目对你有帮助，欢迎 Star**

[![GitHub](https://img.shields.io/badge/GitHub-@HuangYuChuh-181717?style=flat-square&logo=github)](https://github.com/HuangYuChuh)

</div>
