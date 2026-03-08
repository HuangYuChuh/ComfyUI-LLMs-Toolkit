"""
LLM Translator — Unix-philosophy translation node.

Do One Thing and Do It Well: translate text via LLM API.
Reuses the shared LLMClient for robustness.
"""

import os
import time
import json
from typing import Dict, Any, Tuple

try:
    from .api_client import LLMClient
except ImportError:
    from api_client import LLMClient


def get_providers_data():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "providers.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f).get("providers", [])
    except Exception as e:
        print(f"[LLMs_Toolkit] Error reading providers.json: {e}")
        return []

def get_enabled_providers():
    providers = get_providers_data()
    enabled = [p["name"] for p in providers if p.get("enabled", False)]
    return enabled if enabled else ["None"]

def get_all_models():
    providers = get_providers_data()
    models = []
    for p in providers:
        if p.get("enabled", False):
            models.extend(p.get("models", []))
    # Deduplicate and keep order
    return list(dict.fromkeys(models)) if models else ["None"]


class LLMTranslator:
    """
    LLM驱动的极简翻译节点 - Unix哲学设计
    Do One Thing and Do It Well.
    """

    @classmethod
    def INPUT_TYPES(cls):
        providers = get_enabled_providers()
        models = get_all_models()
        
        return {
            "required": {
                "provider": (providers,),
                "model": (models,),
                "text": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "✏️ Paste the text you want to translate here.\nSupports plain text, prompts, subtitles, or any multi-line content.\nLeave empty to skip."
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
                "llm_config": ("LLM_CONFIG",),
                "glossary": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "📖 Optional: Define domain-specific terms to ensure consistent translation.\nFormat — one entry per line:\n  LoRA = LoRA\n  Checkpoint = 检查点\n  Workflow = 工作流\nThe LLM will strictly follow these mappings."
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("translated_text",)
    FUNCTION = "translate"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/Utility"

    def translate(
        self,
        provider: str,
        model: str,
        text: str,
        target_language: str,
        llm_config: Dict[str, Any] = None,
        glossary: str = ""
    ) -> Tuple[str]:
        """Execute translation. Returns error text on failure instead of crashing."""
        if not text.strip():
            return ("",)

        start_time = time.time()
        
        # Build configuration (Use provided llm_config if connected, otherwise lookup from providers.json)
        if llm_config is None:
            providers_data = get_providers_data()
            selected_provider = next((p for p in providers_data if p["name"] == provider), None)
            
            if not selected_provider:
                return (f"[Translation Error] Provider '{provider}' not found in configuration.",)
                
            api_key = selected_provider.get("apiKey", "")
            base_url = selected_provider.get("apiHost", "")
            
            if not api_key:
                return (f"[Translation Error] API Key is missing for provider '{provider}'.",)
                
            config = {
                "base_url": base_url,
                "api_key": api_key,
                "model": model
            }
        else:
            config = llm_config

        # Build system instruction
        system_instruction = (
            f"You are a professional translator. Translate the following text into {target_language}. "
            "Maintain the original tone, style, and formatting. "
            "Output ONLY the translated text, no explanations."
        )
        if glossary.strip():
            system_instruction += f"\n\nGlossary (Strictly follow):\n{glossary}"

        # Build payload
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": text}
        ]
        payload = {
            "model": config.get("model", ""),
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 4096
        }

        # Call API via shared client
        try:
            client = LLMClient(
                base_url=config.get("base_url", ""),
                api_key=config.get("api_key", ""),
                max_retries=3,
                timeout=60,
            )
            translated_text, _ = client.chat(payload)

            elapsed = int((time.time() - start_time) * 1000)
            print(f"[LLM Translator] {len(text)} chars -> {target_language} ({elapsed}ms)")

            return (translated_text.strip(),)

        except Exception as e:
            elapsed = int((time.time() - start_time) * 1000)
            print(f"[LLM Translator] ✗ Translation failed ({elapsed}ms): {e}")
            return (f"[Translation Error] {str(e)[:200]}",)


# ComfyUI Node Registration
NODE_CLASS_MAPPINGS = {"LLMTranslator": LLMTranslator}
NODE_DISPLAY_NAME_MAPPINGS = {"LLMTranslator": "LLM Translator"}
