# Changelog

All notable changes to the **ComfyUI-LLMs-Toolkit** extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased] - YYYY-MM-DD
*( 这里存放正在开发中、还未打上特定版本号的改动 )*

---

## [1.1.0] - 2026-03-01

### Added (新增)
- **DeepSeek Reasoning Support**: 新增了针对 DeepSeek R1 模型的思考过程（Reasoning Content）截取功能。现在，它会将官方 `reasoning_content` 或 `<think>` 标签包裹的内容无损分离，并暴露给 `openai_compatible` 节点的专属 `reasoning` 输出引脚，完美保持文本干净！
- **o1/o3 Model Compatibility**: 对 `o1`、`o3` 思考类型的模型提供了降级兼容层。在发包前自动强制将不支持的 `system` 角色转为 `user`，防止服务商报错 HTTP 400。

### Changed (变更)
- **API Client Architecture Refactor**: 彻底重构了底层网路请求模块，提取出了高内聚的 `LLMClient` (`api_client.py`)，供不同 LLM Nodes 共同复用。
- **Graceful Degradation**: `openai_compatible.py` 现在采用**优雅降级**的设计。任何 API 错误仅返回红色结构化错误文本而不再主动抛出 Python 异常，这样可以完美保证 ComfyUI 工作流在批量运算时不会被中断爆炸。
- **Intelligent Retry**: HTTP 客户端增加了指数退避重试功能（Exponential Backoff & Jitter），并学会了尊重 `Retry-After` 头，在面对 HTTP 429 频率限制时能自动从容等待再发包。
- **User-Agent Masquerade**: 为纯 API 代码加装了标准浏览器的 `User-Agent` 与通用 HTTP 头，成功绕过了中转 API 平台上恶心的 Cloudflare 1010 拦截。

### Fixed (修复)
- **Multi-turn Memory Bug**: 修复了开启 `enable_memory` 时系统没有完整存储 Assistant（机器人自己）对话历史的恶性 Bug。现在节点具备真正可追溯的多轮上下文能力了。
- **Node Parameter Misalignment**: 修复了 UI 层因为动态增加 `token_usage_display` 组件导致的参数反序列化偏移问题，采用原生 `<canvas>` 的 `onDrawForeground` 完美解决。
- **Strict Payload Cleaner**: 去除了在 `_build_payload` 中随意发送 `seed`、`timestamp` 等非标准字段的坏习惯，避免了在要求极高的接口上导致 400 失败。

---

## [1.0.0] - Initial Release
- The birth of ComfyUI-LLMs-Toolkit.
