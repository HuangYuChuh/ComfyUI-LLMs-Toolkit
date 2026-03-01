"""
OpenAI-compatible LLM adapter for ComfyUI.

Unified interface for multiple LLM providers with graceful degradation.
API calls are handled by the shared LLMClient (api_client.py).
"""

import time
import re
import json as json_lib
from typing import Optional, List, Dict, Tuple, Any, Union

try:
    from .api_client import LLMClient, classify_error, log_error
except ImportError:
    from api_client import LLMClient, classify_error, log_error


# ─── Message Building ────────────────────────────────────────────────────────

# Providers that require plain string content instead of structured arrays
_STRING_CONTENT_PROVIDERS = frozenset({
    "Spark/星火", "Baichuan/百川", "SenseChat/日日新"
})


def _build_content(
    prompt: str,
    image_url: Optional[Union[str, List[str]]] = None
) -> Union[str, List[Dict[str, Any]]]:
    """Build user message content (multimodal or text-only)."""
    # Fast path: no image → just return the string
    if not image_url:
        return prompt

    content: List[Dict[str, Any]] = []

    # Normalize to list
    urls = image_url if isinstance(image_url, list) else [image_url]
    for url in urls:
        if isinstance(url, str) and url.startswith("data:image"):
            content.append({
                "type": "image_url",
                "image_url": {"url": url}
            })

    if prompt.strip():
        content.append({"type": "text", "text": prompt})

    return content if content else prompt


def _build_messages(
    content: Union[str, List[Dict[str, Any]]],
    system_prompt: Optional[str] = None,
    provider: str = ""
) -> List[Dict[str, Any]]:
    """Build complete message array, adapting for provider quirks."""
    messages: List[Dict[str, Any]] = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    # Some providers require plain string content
    if provider in _STRING_CONTENT_PROVIDERS and isinstance(content, list):
        # Extract text from structured content
        text_parts = [c["text"] for c in content if c.get("type") == "text"]
        user_content = " ".join(text_parts) if text_parts else ""
    else:
        user_content = content

    messages.append({"role": "user", "content": user_content})
    return messages


# ─── ComfyUI Node ────────────────────────────────────────────────────────────

class OpenAICompatibleLoader:
    """
    OpenAI-compatible API adapter for ComfyUI.

    Supports multiple LLM providers with unified interface.
    Features graceful degradation — errors return readable text
    instead of crashing the workflow.
    """

    TAG = "[LLMs_Toolkit]"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "llm_config": ("LLM_CONFIG",),
                "system_prompt": ("STRING", {
                    "default": "你是一个AI大模型",
                    "multiline": True
                }),
                "prompt": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "prep_img": ("STRING", {"default": "", "forceInput": True}),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 2.0
                }),
                "max_tokens": ("INT", {
                    "default": 2048,
                    "min": 1,
                    "max": 4096
                }),
                "enable_memory": ("BOOLEAN", {
                    "default": False,
                    "label": "Enable Memory"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff
                })
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text", "reasoning")
    FUNCTION = "generate"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/Generate"
    OUTPUT_NODE = True

    def __init__(self):
        self._conversation_history: List[Dict[str, Any]] = []

    # ── Logging ──────────────────────────────────────────────────────────

    @staticmethod
    def _log_start(provider_name: str, model: str,
                   system_prompt: Optional[str], prompt: str,
                   image_input: Optional[Union[str, List[str]]]) -> float:
        """Log request start, return start time."""
        start = time.time()
        ts = time.strftime('%H:%M:%S')

        flags = []
        if system_prompt:
            flags.append('sys')
        if image_input:
            n = len(image_input) if isinstance(image_input, list) else 1
            flags.append(f'img(x{n})')
        flag_str = f"[{' '.join(flags)}]" if flags else ""

        print(f"[LLMs_Toolkit] {ts} → {provider_name}/{model or 'default'} {flag_str}")
        if system_prompt:
            print(f"   sys│ {system_prompt[:60].replace(chr(10), ' ')}...")
        print(f"   in │ {prompt[:80].replace(chr(10), ' ')}...")

        return start

    @staticmethod
    def _log_done(response: str, in_tok: int, out_tok: int, start: float) -> None:
        """Log completed request."""
        ms = int((time.time() - start) * 1000)
        fmt = lambda t: f"{t/1000:.1f}k" if t >= 1000 else str(t)
        print(f"   out│ {response[:80].replace(chr(10), ' ')}...")
        print(f"[LLMs_Toolkit] {time.strftime('%H:%M:%S')} ← {fmt(in_tok)}/{fmt(out_tok)}t ({ms}ms)\n")

    # ── Memory ───────────────────────────────────────────────────────────

    def _apply_memory(
        self, messages: List[Dict[str, Any]], enable: bool
    ) -> List[Dict[str, Any]]:
        """Manage conversation history."""
        if not enable:
            self._conversation_history = []
            return messages

        for msg in messages:
            if not any(
                h["role"] == msg["role"] and h["content"] == msg["content"]
                for h in self._conversation_history
            ):
                self._conversation_history.append(msg)

        return list(self._conversation_history)

    # ── Result helpers ───────────────────────────────────────────────────

    @staticmethod
    def _success(text: str, reasoning: str, in_tok: int, out_tok: int) -> dict:
        return {
            "ui": {
                "text": [f"Token Usage:\nInput: {in_tok}\nOutput: {out_tok}"]
            },
            "result": (text, reasoning)
        }

    @staticmethod
    def _error_result(error_msg: str) -> dict:
        """Return a graceful error result instead of crashing."""
        return {
            "ui": {
                "text": [f"⚠ Error:\n{error_msg}"]
            },
            "result": (f"[Error] {error_msg}", "")
        }

    # ── Main entry ───────────────────────────────────────────────────────

    def generate(
        self,
        llm_config: Dict[str, Any],
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        system_prompt: Optional[str] = None,
        prep_img: Optional[str] = None,
        enable_memory: bool = False,
        seed: int = 0
    ) -> dict:
        """Main generation entry point with graceful degradation."""

        # ── Extract config ───────────────────────────────────────────
        base_url = llm_config.get("base_url", "")
        model = llm_config.get("model", "")
        api_key = llm_config.get("api_key", "")
        provider_name = llm_config.get("provider", "Custom")

        # ── Input validation (fail fast, don't waste API quota) ──────
        if not prompt or not prompt.strip():
            return self._error_result("输入的 Prompt 为空，请填写内容后重试")
        if not api_key or not api_key.strip():
            return self._error_result("API Key 为空，请在 LLMs Loader 节点中配置")
        if not base_url or not base_url.strip():
            return self._error_result("Base URL 为空，请检查服务商配置")
        if not model or not model.strip():
            return self._error_result("模型名称为空，请在 LLMs Loader 节点中填写")

        # ── Parse image input ────────────────────────────────────────
        image_input = None
        if prep_img and prep_img.strip():
            stripped = prep_img.strip()
            if stripped.startswith("["):
                try:
                    image_input = json_lib.loads(stripped)
                except Exception:
                    image_input = stripped
            else:
                image_input = stripped

        # ── Logging ──────────────────────────────────────────────────
        print(f"{self.TAG} 使用配置: {provider_name} / {model}")
        start = self._log_start(
            provider_name, model, system_prompt, prompt, image_input
        )

        # ── Build messages ───────────────────────────────────────────
        content = _build_content(prompt, image_input)
        messages = _build_messages(content, system_prompt, provider_name)
        messages = self._apply_memory(messages, enable_memory)

        # ── o1/o3 System Role Downgrade (Compatibility) ──────────────
        if re.search(r'o[1-3]', model):
            for i, msg in enumerate(messages):
                if msg["role"] == "system":
                    messages[i] = {"role": "user", "content": msg["content"]}
                    messages.insert(i + 1, {"role": "assistant", "content": "好的，我会按照你的指示来操作"})
                    break

        # ── Build payload (clean, standard fields) ────────────
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        # Seed enables ComfyUI to bypass cache when changed (e.g., set to 'random')
        # However, we DO NOT inject it into the API payload to comply with CONTRIBUTING.md
        # and prevent 400 Bad Request errors from strict APIs (like qwen3).

        # Calculate request size for diagnostics
        payload_bytes = json_lib.dumps(payload).encode("utf-8")
        request_size_mb = len(payload_bytes) / (1024 * 1024)

        # ── Make API call ────────────────────────────────────────────
        try:
            client = LLMClient(base_url, api_key)
            response_content, data = client.chat(payload)

            # Extract reasoning content (DeepSeek/R1)
            reasoning_content = ""
            if "choices" in data and len(data["choices"]) > 0:
                msg_dict = data["choices"][0].get("message", {})
                if "reasoning_content" in msg_dict and msg_dict["reasoning_content"]:
                    reasoning_content = msg_dict["reasoning_content"]

            # Fallback: Extract <think> tags from text if no native field
            if not reasoning_content:
                pattern = r'<think>(.*?)</think>'
                match = re.search(pattern, response_content, re.DOTALL)
                if match:
                    reasoning_content = match.group(1).strip()
                    response_content = response_content.replace(match.group(0), "").strip()

            if reasoning_content:
                print(f"[LLMs_Toolkit] 🧠 思考过程已捕获 ({len(reasoning_content)} 字): \n{reasoning_content[:150]}...\n")

            # Extract real token usage from API response (prefer actual over estimate)
            usage = data.get("usage", {})
            input_tokens = usage.get("prompt_tokens", 0) or len(prompt)
            output_tokens = usage.get("completion_tokens", 0)

            self._log_done(response_content, input_tokens, output_tokens, start)
            
            # Save assistant response to memory if enabled
            if enable_memory:
                self._conversation_history.append({"role": "assistant", "content": response_content})
                
            return self._success(response_content, reasoning_content, input_tokens, output_tokens)

        except Exception as e:
            elapsed_ms = int((time.time() - start) * 1000)
            err = classify_error(e, provider_name, model, request_size_mb, elapsed_ms)
            log_error(err, provider_name, model, request_size_mb, elapsed_ms)

            # Graceful degradation: return error text instead of crashing
            return self._error_result(err.user_message())


# ComfyUI node registration
NODE_CLASS_MAPPINGS = {"OpenAICompatibleLoader": OpenAICompatibleLoader}
NODE_DISPLAY_NAME_MAPPINGS = {"OpenAICompatibleLoader": "OpenAI Compatible Adapter"}
