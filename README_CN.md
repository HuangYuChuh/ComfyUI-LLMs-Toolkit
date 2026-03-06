<div align="center">

# ComfyUI-LLMs-Toolkit

![Banner](asset/banner.png)

**语言**

[![简体中文](https://img.shields.io/badge/README-简体中文-red?style=for-the-badge)](README_CN.md)
[![English](https://img.shields.io/badge/README-English-blue?style=for-the-badge)](README.md)

---

[![GitHub Stars](https://img.shields.io/github/stars/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&logo=github&color=yellow)](https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&logo=github&color=green)](https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit/network)
[![GitHub Issues](https://img.shields.io/github/issues/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&logo=github&color=red)](https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit/issues)
[![License](https://img.shields.io/github/license/HuangYuChuh/ComfyUI-LLMs-Toolkit?style=flat-square&color=blue)](LICENSE)

**在 ComfyUI 中轻松调用各种大语言模型 — 无需 GPU，API 即用。**

</div>

---

## 这是什么？

ComfyUI-LLMs-Toolkit 让你可以在 ComfyUI 工作流中，通过简单的 API 调用直接使用 DeepSeek、通义千问、GPT、Moonshot 等主流大语言模型。

不管你是想生成文本、翻译内容、用视觉模型处理图片，还是构建结构化 JSON 数据，这个工具包都能帮到你。

### 主要特色

- **内置模型管理面板** — 在 ComfyUI 菜单栏中可视化管理所有 API 供应商，无需手动编辑配置文件
- **12 家服务商预配置** — 通义千问、DeepSeek、智谱清言、豆包、星火、月之暗面、百川、MiniMax、阶跃星辰、日日新、心流、魔搭
- **智能模型联动** — 选择供应商后，模型下拉框只显示该供应商的模型
- **视觉多模态** — 通过 Image Preprocessor 节点把图片发给支持视觉的大模型
- **不会崩溃** — API 调用失败时返回可读错误信息，工作流不会中断
- **多轮对话记忆** — 开启 Memory 模式即可进行连续对话

---

## 安装

### 方式一：ComfyUI Manager（推荐）

1. 打开 **ComfyUI Manager**
2. 搜索 `ComfyUI-LLMs-Toolkit`
3. 点击 **安装** → **重启 ComfyUI**

### 方式二：手动安装

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit.git
cd ComfyUI-LLMs-Toolkit
pip install -r requirements.txt
```

安装完成后重启 ComfyUI 即可。

---

## 快速上手

### 第一步：打开管理面板

安装完成后，你会在 ComfyUI 顶部菜单栏看到一个 **`LLMs_Manager`** 按钮，点击打开设置面板。

### 第二步：配置你的服务商

1. 从左侧选择一个 **服务商**（比如 DeepSeek）
2. 填入你的 **API Key**（从服务商官网申请）
3. 点击 **Check API** 验证连接 ✅
4. 添加或编辑你想用的 **模型名称**
5. 点击 **Save**，并把 **Enable in Nodes** 开关打开

### 第三步：在工作流中使用

1. 右键 → `Add Node` → `🚦ComfyUI_LLMs_Toolkit`
2. 添加一个 **OpenAI Compatible Adapter** 节点
3. 在下拉框中选择你配置好的服务商和模型
4. 输入 Prompt，连接输出，点击 **执行**！

### API Key 获取指南

| 服务商 | 官网 | 免费额度 |
|--------|------|----------|
| **DeepSeek** | [platform.deepseek.com](https://platform.deepseek.com/) | ¥500 |
| **通义千问** | [dashscope.aliyun.com](https://dashscope.aliyun.com/) | 每月 100 万 tokens |
| **智谱清言** | [open.bigmodel.cn](https://open.bigmodel.cn/) | 每月 500 万 tokens |
| **月之暗面** | [platform.moonshot.cn](https://platform.moonshot.cn/) | 免费试用 |
| **OpenAI** | [platform.openai.com](https://platform.openai.com/) | $5 |

---

## 节点一览

### 大模型节点

| 节点 | 用途 |
|------|------|
| **OpenAI Compatible Adapter** | 核心节点 — 向任意 OpenAI 兼容大模型发送 Prompt，获得文本回复。支持 System Prompt、多轮记忆、图片输入。 |
| **LLMs Loader** | 辅助配置节点，输出供应商配置供高级场景使用。 |
| **LLM Translator** | 快速翻译节点，一步完成文本翻译。 |

### 视觉节点

| 节点 | 用途 |
|------|------|
| **Image Preprocessor** | 将 ComfyUI 图片转换为大模型可读的格式。连接到 Adapter 节点的 `prep_img` 输入即可。 |

### JSON 工具节点

| 节点 | 用途 |
|------|------|
| **JSON Builder** (Simple / Medium / Large) | 构建包含 1、5 或 10 个键值对的结构化 JSON。 |
| **JSON Combine** | 合并多个 JSON 对象。 |
| **JSON Extractor** | 从 JSON 字符串中按路径提取值。 |
| **JSON Fixer** | 自动修复大模型有时输出的格式错误的 JSON。 |

### 文本工具节点

| 节点 | 用途 |
|------|------|
| **String Template** | 用变量填充模板字符串，如 `"你好 {name}！"` → `"你好 Alice！"` |

---

## 常见问题

<details>
<summary><strong>提示 "API Key is missing" 怎么办？</strong></summary>

请确认：
1. 打开了 **LLMs_Manager** 面板
2. 选择了对应服务商并填入了 API Key
3. 点击了 **Save**
4. 将 **Enable in Nodes** 开关打开

</details>

<details>
<summary><strong>可以用 Ollama 等本地模型吗？</strong></summary>

可以！在 LLMs_Manager 中点击 **+ Custom Provider**，将 Base URL 设为本地地址（如 `http://localhost:11434/v1`），添加模型名称即可。任何 OpenAI 兼容的 API 都可以使用。

</details>

<details>
<summary><strong>模型下拉框显示不对</strong></summary>

在 Provider Manager 中修改配置后，请 **刷新浏览器**（Cmd+R / Ctrl+R）。模型列表会根据选择的服务商自动更新。

</details>

<details>
<summary><strong>排障文档在哪里？</strong></summary>

请查看 [`docs/troubleshooting.md`](docs/troubleshooting.md)，包含依赖冲突、模型下拉异常、本地端点配置等常见问题。

</details>

---

## 安全提醒

你的 API Key 以明文形式保存在本地的 `config/providers.json` 文件中。该文件默认已被 `.gitignore` 排除，所以推送代码时不会泄漏。但请注意不要手动将此文件分享给他人。

---

## 更新日志

### v1.2.1 — 2026-03-07
- 同步包版本号与当前发布版本线（`pyproject.toml`）
- 新增 `docs/troubleshooting.md`，集中说明依赖/供应商配置常见问题

### v1.2.0 — 2026-03-02
- 内置 **Provider Manager** 可视化管理面板
- 模型下拉框按供应商动态过滤
- 自定义弹窗替代浏览器原生 prompt
- 精简节点接口（移除冗余输入输出参数）

### v1.1.0 — 2026-03-01
- DeepSeek 深度思考过程提取
- o1/o3 模型角色兼容
- 统一 API 客户端（智能重试机制）
- 优雅降级（不再崩溃工作流）
- 修复多轮记忆和 Token 显示 Bug

---

## 开源协议

[GNU Affero General Public License v3.0 (AGPL-3.0)](LICENSE) — 免费使用、修改和分发。如果你修改或在网络服务中使用了本代码，必须基于相同协议开源你的完整源代码。

---

<div align="center">

### 觉得有用？给个 Star 吧！

[![Star History Chart](https://api.star-history.com/svg?repos=HuangYuChuh/ComfyUI-LLMs-Toolkit&type=Date)](https://star-history.com/#HuangYuChuh/ComfyUI-LLMs-Toolkit&Date)

[![GitHub](https://img.shields.io/badge/GitHub-@HuangYuChuh-181717?style=flat-square&logo=github)](https://github.com/HuangYuChuh)

**Made with ❤️ for the ComfyUI community**

</div>
