# LLM 配置解耦使用指南

## 概述

通过 **LLMs Loader** 节点,你可以将 LLM 的配置参数(provider、base_url、model、api_key)集中管理,然后在多个节点中复用。

## 核心特性

- ✅ **统一配置**: 所有 LLM 参数集中在 LLMs Loader 节点
- ✅ **一线连接**: 只需一根连接线,简洁清晰
- ✅ **强制解耦**: OpenAI Compatible Adapter 必须使用配置节点,确保配置统一
- ✅ **灵活选择**: 支持预设提供商和自定义 URL

## 使用方式

配置一次,全局使用:

```
[LLMs Loader] ──llm_config──> [OpenAI Compatible Adapter]
                                  ↓ prompt: "你的提示词"
                                  ↓ temperature: 0.7
                                  ↓ max_tokens: 512
```

**步骤:**

1. 添加 `LLMs Loader` 节点
2. 配置:
   - **provider**: 从下拉菜单选择提供商
     - 预设提供商: "Qwen/通义千问"、"DeepSeek/深度求索" 等
     - 自定义: 选择 "Custom/自定义"
   - **model**: 输入模型名称(如 "qwen-max")
   - **api_key**: 输入你的 API Key
   - **custom_base_url** (可选): 当选择 "Custom/自定义" 时,填写完整的 API 端点

3. 将 Loader 的 `llm_config` 输出连接到 `OpenAI Compatible Adapter` 的 `llm_config` 输入
4. 在 Adapter 中配置 prompt 和其他参数(temperature、max_tokens 等)

## 使用示例

### 示例 1: 基础使用

```
[LLMs Loader]
  provider: Qwen/通义千问
  model: qwen-max
  api_key: sk-xxx
     ↓ llm_config
[OpenAI Compatible Adapter]
  prompt: "写一首关于春天的诗"
  temperature: 0.8
  max_tokens: 512
```

### 示例 2: 多个节点共享配置

```
                         ──llm_config──> [Adapter 1] prompt: "翻译成英文"
                         |
[LLMs Loader]            |
  provider: DeepSeek     |
  model: deepseek-chat   |
  api_key: sk-xxx        |
                         ──llm_config──> [Adapter 2] prompt: "总结要点"
```

一个 Loader 可以连接到多个 Adapter,实现配置复用。

### 示例 3: 使用第三方代理商 URL

```
[LLMs Loader]
  provider: Custom/自定义
  custom_base_url: https://api.your-proxy.com/v1
  model: gpt-4
  api_key: sk-proxy-xxx
     ↓ llm_config
[OpenAI Compatible Adapter]
  prompt: "你的提示词"
```

选择 "Custom/自定义" 后,填写自定义 URL,支持任何兼容 OpenAI API 格式的第三方服务。

### 示例 4: 不同模型处理不同任务

```
[Loader 1: Qwen] ──llm_config──> [Adapter 1] 翻译任务
[Loader 2: DeepSeek] ──llm_config──> [Adapter 2] 代码生成任务
```

为不同的任务使用不同的模型配置。

## 优势

1. **配置集中**: API Key 等敏感信息只需配置一次
2. **易于维护**: 切换模型时只需修改 Loader 节点
3. **复用性强**: 一个配置可以被多个节点使用
4. **灵活性高**: 可以混合使用 Loader 和直接配置

## 注意事项

- 如果同时使用 Loader 和直接配置,Loader 的输出会覆盖直接配置的值
- 确保 api_key 和 model 参数不为空,否则会报错
- Loader 节点的输出可以连接到任何支持这些参数的节点

## 支持的提供商

### 预设提供商

直接输入以下名称,会自动转换为对应的 API 端点:

- **Qwen/通义千问** → https://dashscope.aliyuncs.com/compatible-mode/v1
- **DeepSeek/深度求索** → https://api.deepseek.com/v1
- **DouBao/豆包** → https://ark.cn-beijing.volces.com/api/v3
- **Spark/星火** → https://spark-api-open.xf-yun.com/v1
- **GLM/智谱清言** → https://open.bigmodel.cn/api/paas/v4/
- **Moonshot/月之暗面** → https://api.moonshot.cn/v1
- **Baichuan/百川** → https://api.baichuan-ai.com/v1
- **MiniMax/MiniMax** → https://api.minimax.chat/v1
- **StepFun/阶跃星辰** → https://api.stepfun.com/v1
- **SenseChat/日日新** → https://api.sensenova.cn/compatible-mode/v1

### 自定义 URL

你也可以直接输入任何兼容 OpenAI API 格式的 URL:

- 第三方代理商: `https://api.your-proxy.com/v1`
- 本地部署: `http://localhost:8000/v1`
- 其他兼容服务: 任何支持 OpenAI API 格式的端点

**注意**: 自定义 URL 必须是完整的端点地址,包括协议(http/https)和路径。
