# LLM Translator 使用指南

## 一句话介绍

最简单的LLM翻译节点 - 输入文本，选择目标语言，完成。

## 快速开始

### 基础用法

```
[LLMs Loader] → [LLM Translator] → [输出]
```

只需填写3个参数：
1. **text** - 要翻译的文本
2. **target_language** - 目标语言（如：English, 中文, 日本語）
3. **llm_config** - 来自 LLMs Loader

就这么简单。

## 参数说明

### 必填参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `llm_config` | LLM配置 | 来自 LLMs Loader |
| `text` | 待翻译文本 | "你好世界" |
| `target_language` | 目标语言 | "English" |

### 可选参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `source_language` | "auto" | 源语言（auto=自动检测） |
| `glossary` | "" | 术语对照表 |
| `temperature` | 0.3 | 翻译稳定性（越低越稳定） |

## 使用示例

### 示例1：最简单的翻译

```
text: "人工智能正在改变世界"
target_language: "English"
```

输出：`"Artificial intelligence is changing the world"`

### 示例2：带术语表的专业翻译

```
text: "LLM可以进行多模态推理"
target_language: "English"
glossary: "LLM = Large Language Model
          多模态 = multimodal"
```

输出：`"Large Language Model can perform multimodal reasoning"`

### 示例3：指定源语言

```
text: "Hello world"
source_language: "English"
target_language: "日本語"
```

输出：`"こんにちは世界"`

## 术语表格式

每行一个术语对，用 `=` 分隔：

```
AI = 人工智能
API = 应用程序接口
ComfyUI = ComfyUI（保持不译）
```

## 设计理念

### 为什么这么简单？

1. **自动语言检测** - 不需要手动指定源语言
2. **单一策略** - 不需要选择翻译策略
3. **智能默认值** - temperature=0.3 适合99%的场景
4. **专注核心** - 只做翻译，做好翻译

### 技术细节

- 使用低温度参数（0.3）确保翻译稳定
- 自动处理格式和换行
- 支持超长文本（最多4096 tokens输出）
- 完全复用现有的 LLM 基础设施

## 常见问题

### Q: 如何提高翻译质量？

A: 三个方法：
1. 使用更强的模型（如 GPT-4, Claude）
2. 添加术语表
3. 降低 temperature 到 0.1

### Q: 支持哪些语言？

A: 取决于你使用的 LLM 模型。主流模型都支持：
- 中文、英文、日文、韩文
- 法语、德语、西班牙语
- 以及更多...

### Q: 可以批量翻译吗？

A: 可以。在 ComfyUI 中使用循环节点配合使用。

### Q: 翻译很慢怎么办？

A: 检查：
1. 网络连接
2. 使用更快的模型
3. 减少文本长度

## 与其他节点配合

### 工作流1：内容生成+翻译

```
[LLMs Loader] → [OpenAI Compatible Adapter] → [LLM Translator]
                         ↓                            ↓
                    生成中文内容                  翻译成英文
```

### 工作流2：多语言输出

```
                    → [LLM Translator (English)]
[LLMs Loader] →    → [LLM Translator (日本語)]
                    → [LLM Translator (한국어)]
```

## 总结

LLM Translator 的设计哲学：

✅ **极简** - 3个必填参数
✅ **智能** - 自动检测源语言
✅ **可靠** - 低温度确保稳定
✅ **专业** - 支持术语表

不需要复杂的配置，不需要选择策略，只需要告诉它"翻译成什么语言"。
