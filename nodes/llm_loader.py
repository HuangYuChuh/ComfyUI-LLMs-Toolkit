from typing import Optional

# Provider URL mapping (self-contained to avoid cross-module import issues with ComfyUI)
_BASE_URL_MAPPING = {
    "Qwen/通义千问": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "DeepSeek/深度求索": "https://api.deepseek.com/v1",
    "DouBao/豆包": "https://ark.cn-beijing.volces.com/api/v3",
    "Spark/星火": "https://spark-api-open.xf-yun.com/v1",
    "GLM/智谱清言": "https://open.bigmodel.cn/api/paas/v4/",
    "Moonshot/月之暗面": "https://api.moonshot.cn/v1",
    "Baichuan/百川": "https://api.baichuan-ai.com/v1",
    "MiniMax/MiniMax": "https://api.minimax.chat/v1",
    "StepFun/阶跃星辰": "https://api.stepfun.com/v1",
    "SenseChat/日日新": "https://api.sensenova.cn/compatible-mode/v1",
    "iFlow/心流": "https://apis.iflow.cn/v1",
    "ModelScope/魔搭": "https://api-inference.modelscope.cn/v1",
}


class LLM_Loader:
    """
    Custom node for loading LLM models via a base URL and model name
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "provider": ([
                    "Qwen/通义千问",
                    "DeepSeek/深度求索",
                    "DouBao/豆包",
                    "Spark/星火",
                    "GLM/智谱清言",
                    "Moonshot/月之暗面",
                    "Baichuan/百川",
                    "MiniMax/MiniMax",
                    "StepFun/阶跃星辰",
                    "SenseChat/日日新",
                    "iFlow/心流",
                    "ModelScope/魔搭",
                    "Custom/自定义"
                ], {
                    "default": "Qwen/通义千问"
                }),
                "model": ("STRING", {
                    "default": "",
                    "label": "模型名称"
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "label": "API Key"
                }),
            },
            "optional": {
                "custom_base_url": ("STRING", {
                    "default": "",
                    "label": "自定义 Base URL",
                    "placeholder": "https://api.example.com/v1"
                }),
            }
        }

    @classmethod
    def VALIDATE_INPUTS(cls, provider, model, api_key, custom_base_url=""):
        """Validate inputs"""
        if provider == "Custom/自定义" and (not custom_base_url or not custom_base_url.strip()):
            return "选择自定义时,必须填写自定义 Base URL"
        if not model or not model.strip():
            return "Model name cannot be empty"
        if not api_key or not api_key.strip():
            return "API Key cannot be empty"
        return True

    RETURN_TYPES = ("LLM_CONFIG",)
    RETURN_NAMES = ("llm_config",)
    FUNCTION = "generate"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/Loader"

    def generate(self, provider: str, model: str, api_key: str, custom_base_url: str = ""):
        if provider == "Custom/自定义":
            actual_base_url = custom_base_url.strip()
            print(f"[LLMs_Toolkit] 配置加载: Custom URL ({actual_base_url}) / {model}")
        else:
            actual_base_url = _BASE_URL_MAPPING.get(provider, "")
            print(f"[LLMs_Toolkit] 配置加载: {provider} / {model}")

        config = {
            "provider": provider,
            "base_url": actual_base_url,
            "model": model,
            "api_key": api_key
        }

        return (config,)

# 注册节点
NODE_CLASS_MAPPINGS = {"LLM_Loader": LLM_Loader}
NODE_DISPLAY_NAME_MAPPINGS = {"LLM_Loader": "LLMs Loader"}

