import time
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Tuple


class LLMTranslator:
    """
    LLM驱动的极简翻译节点 - Unix哲学设计
    Do One Thing and Do It Well.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "llm_config": ("LLM_CONFIG",),
                "text": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Input text here..."
                }),
                "target_language": ([
                    "English",
                    "Chinese (Simplified)",
                    "Chinese (Traditional)",
                    "Japanese",
                    "Korean",
                    "French",
                    "German",
                    "Spanish",
                    "Russian",
                    "Italian",
                    "Portuguese",
                    "Dutch",
                    "Arabic"
                ], {
                    "default": "English"
                }),
            },
            "optional": {
                "glossary": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Optional glossary (Term = Translation)"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("translated_text",)
    FUNCTION = "translate"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/Translation"

    def __init__(self):
        pass

    def _call_api(
        self,
        llm_config: Dict[str, Any],
        messages: list,
        temperature: float = 0.3
    ) -> str:
        """调用LLM API - 核心通信逻辑"""
        base_url = llm_config.get("base_url", "").rstrip("/")
        model = llm_config.get("model", "")
        api_key = llm_config.get("api_key", "")

        url = f"{base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 4096
        }

        try:
            req = urllib.request.Request(
                url, 
                data=json.dumps(payload).encode("utf-8"), 
                headers=headers, 
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
                
                if "choices" not in data or not data["choices"]:
                    raise ValueError("Empty response from API")
                    
                return data["choices"][0]["message"]["content"].strip()

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="ignore")
            raise Exception(f"HTTP Error {e.code}: {error_body}")
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")

    def translate(
        self,
        llm_config: Dict[str, Any],
        text: str,
        target_language: str,
        glossary: str = ""
    ) -> Tuple[str]:
        """
        执行翻译任务
        Unix Philosophy: Clean input, clean output.
        """
        if not text.strip():
            return ("",)

        start_time = time.time()
        
        # 1. 构建系统指令 (System Prompt)
        system_instruction = (
            f"You are a professional translator. Translate the following text into {target_language}. "
            "Maintain the original tone, style, and formatting. "
            "Output ONLY the translated text, no explanations."
        )

        if glossary.strip():
            system_instruction += f"\n\nGlossary (Strictly follow):\n{glossary}"

        # 2. 构建消息体
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": text}
        ]

        # 3. 调用API (Opinionated defaults: temperature=0.3 for stability)
        translated_text = self._call_api(llm_config, messages, temperature=0.3)

        # 4. 简单日志
        elapsed = int((time.time() - start_time) * 1000)
        print(f"[LLM Translator] {len(text)} chars -> {target_language} ({elapsed}ms)")

        return (translated_text,)

# ComfyUI Node Registration
NODE_CLASS_MAPPINGS = {"LLMTranslator": LLMTranslator}
NODE_DISPLAY_NAME_MAPPINGS = {"LLMTranslator": "LLM Translator (Simple)"}
