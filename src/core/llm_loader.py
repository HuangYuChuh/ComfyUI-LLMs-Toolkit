import comfy
import folder_paths
import nodes
import aiohttp
import json
import asyncio
from typing import Optional
from aiohttp import ClientSession, ClientError


class LLM_Loader:
    """
    Custom node for loading LLM models via a base URL and model name
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_url": ([
                    "Qwen/通义千问",
                    "DeepSeek/深度求索",
                    "DouBao/豆包",
                    "Spark/星火",
                    "GLM/智谱清言",
                    "Moonshot/月之暗面",
                    "Baichuan/百川",
                    "MiniMax/MiniMax",
                    "StepFun/阶跃星辰",
                    "SenseChat/日日新"
                ], {}),
                "model": ("STRING", {
                    "default": "",
                    "label": "模型名称",
                    "allow_edit": True
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("base_url", "model")
    FUNCTION = "generate"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/Loader"

    def generate(self, base_url: str, model: str):
        # 定义 base_url 映射表
        base_url_mapping = {
            "Qwen/通义千问": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "DeepSeek/深度求索": "https://api.deepseek.com/v1",
            "DouBao/豆包": "https://ark.cn-beijing.volces.com/api/v3",
            "Spark/星火": "https://spark-api-open.xf-yun.com/v1",
            "GLM/智谱清言": "https://open.bigmodel.cn/api/paas/v4/",
            "Moonshot/月之暗面": "https://api.moonshot.cn/v1",
            "Baichuan/百川": "https://api.baichuan-ai.com/v1",
            "MiniMax/MiniMax": "https://api.minimax.chat/v1",
            "StepFun/阶跃星辰": "https://api.stepfun.com/v1",
            "SenseChat/日日新": "https://api.sensenova.cn/compatible-mode/v1"
        }
        
        # 获取实际的 base_url
        actual_base_url = base_url_mapping.get(base_url, base_url)
        
        # 返回 base_url 和 model 参数
        return (actual_base_url, model)

# 注册节点
NODE_CLASS_MAPPINGS = {"LLM_Loader": LLM_Loader}
NODE_DISPLAY_NAME_MAPPINGS = {"LLM_Loader": "LLMs Loader"}

WEB_DIRECTORY = "./web"
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
