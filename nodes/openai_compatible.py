import time
import re
import json as json_lib
import urllib.request
import urllib.error
import ssl
import os
import threading
from typing import Dict, Any, List, Union, Optional
import base64
from io import BytesIO
from PIL import Image
import torch

try:
    from .api_client import LLMClient, classify_error, log_error
except ImportError:
    from api_client import LLMClient, classify_error, log_error


# Load Providers from JSON config
_CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "config")
_PROVIDERS_FILE = os.path.join(_CONFIG_DIR, "providers.json")

_PROVIDER_CACHE = {"mtime": 0, "data": []}
_USAGE_LOCK = threading.Lock()
_USAGE_MAX_LINES = 5000

def _get_providers() -> List[Dict[str, Any]]:
    try:
        if os.path.exists(_PROVIDERS_FILE):
            mtime = os.path.getmtime(_PROVIDERS_FILE)
            if mtime != _PROVIDER_CACHE["mtime"]:
                with open(_PROVIDERS_FILE, "r", encoding="utf-8") as f:
                    data = json_lib.load(f)
                    providers = data.get("providers", [])
                    _PROVIDER_CACHE["data"] = [p for p in providers if p.get("enabled", True)]
                    _PROVIDER_CACHE["mtime"] = mtime
            return _PROVIDER_CACHE["data"]
    except Exception as e:
        print(f"[LLMs_Toolkit] Failed to load providers.json: {e}")
    return []


# ─── Message Building ────────────────────────────────────────────────────────

# Providers that require plain string content instead of structured arrays
_STRING_CONTENT_PROVIDERS = frozenset({
    "spark", "baichuan", "sensechat"
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
        providers = _get_providers()
        
        # Only include enabled providers in the dropdown
        enabled_providers = [p for p in providers if p.get("enabled", True)]
        
        provider_names = [p['name'] for p in enabled_providers]
        provider_names.append("LLM_CONFIG (from input)")
        
        # Collect all models from enabled providers for the dropdown
        all_models = ["Custom Input", "LLM_CONFIG (from input)"]
        for p in enabled_providers:
            for m in p.get("models", []):
                if m not in all_models:
                    all_models.append(m)
                    
        return {
            "required": {
                "provider": (provider_names, {"default": provider_names[0] if provider_names else "LLM_CONFIG (from input)"}),
                "model": (all_models, {"default": all_models[1] if len(all_models) > 1 else "Custom Input"}),
                "system_prompt": ("STRING", {"default": "You are an AI assistant", "multiline": True}),
                "prompt": ("STRING", {"multiline": True, "default": "hello"}),
            },
            "optional": {
                "llm_config": ("LLM_CONFIG",),  # Keep for backward compatibility
                "prep_img": ("STRING", {"default": "", "forceInput": True}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0}),
                "max_tokens": ("INT", {"default": 2048, "min": 1, "max": 4096}),
                "enable_memory": ("BOOLEAN", {"default": False, "label": "Enable Memory"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
            },
            "hidden": {"unique_id": "UNIQUE_ID"}
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("response", "reasoning")
    FUNCTION = "generate"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/LLM"

    _MEMORY_STORE = {}

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

    @staticmethod
    def _log_usage(provider_name: str, model: str, in_tok: int, out_tok: int,
                   start: float, status: str = "ok") -> None:
        """Append usage stats to config/usage.jsonl (thread-safe, auto-rotated)."""
        try:
            usage_file = os.path.join(_CONFIG_DIR, "usage.jsonl")
            elapsed_ms = int((time.time() - start) * 1000)
            record = {
                "timestamp": int(time.time()),
                "provider": provider_name,
                "model": model,
                "input_tokens": in_tok,
                "output_tokens": out_tok,
                "total_tokens": in_tok + out_tok,
                "elapsed_ms": elapsed_ms,
                "status": status
            }
            line = json_lib.dumps(record, ensure_ascii=False) + "\n"

            with _USAGE_LOCK:
                # Auto-rotate: if file exceeds max lines, keep the last half
                if os.path.exists(usage_file):
                    try:
                        with open(usage_file, "r", encoding="utf-8") as f:
                            lines = f.readlines()
                        if len(lines) >= _USAGE_MAX_LINES:
                            keep = lines[len(lines) // 2:]
                            with open(usage_file, "w", encoding="utf-8") as f:
                                f.writelines(keep)
                            print(f"[LLMs_Toolkit] Usage log rotated: {len(lines)} -> {len(keep)} entries")
                    except Exception:
                        pass  # rotation failure is non-critical

                with open(usage_file, "a", encoding="utf-8") as f:
                    f.write(line)
        except Exception as e:
            print(f"[LLMs_Toolkit] Failed to write usage log: {e}")

    # ── Memory ───────────────────────────────────────────────────────────

    def _apply_memory(
        self, messages: List[Dict[str, Any]], enable: bool, unique_id: str
    ) -> List[Dict[str, Any]]:
        """Manage conversation history per node instance."""
        if not enable:
            if unique_id in self._MEMORY_STORE:
                del self._MEMORY_STORE[unique_id]
            return messages

        history = self._MEMORY_STORE.setdefault(unique_id, [])

        for msg in messages:
            if not any(
                h["role"] == msg["role"] and h["content"] == msg["content"]
                for h in history
            ):
                history.append(msg)
                
        # Limit history to prevent unbounded growth
        if len(history) > 40:
            history = history[-40:]
            self._MEMORY_STORE[unique_id] = history

        return list(history)

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

    def _get_provider_config(self, provider_choice: str) -> Optional[Dict[str, Any]]:
        """Find the provider config by its dropdown label."""
            
        providers = _get_providers()
        for p in providers:
            label = p['name']
            if label == provider_choice:
                return p
        return None

    # ── Main entry ───────────────────────────────────────────────────────

    def generate(
        self,
        provider: str = "",
        model: str = "",
        prompt: str = "",
        system_prompt: Optional[str] = None,
        llm_config: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        prep_img: Optional[str] = None,
        enable_memory: bool = False,
        seed: int = 0,
        unique_id: str = ""
    ) -> dict:
        """Main generation entry point with graceful degradation."""

        # ── Configuration Resolution ──────────────────────────────────
        _FROM_INPUT = "LLM_CONFIG (from input)"

        api_key = ""
        base_url = ""
        actual_model = "" if model in ("Custom Input", "Custom/手动输入", _FROM_INPUT, "") else model
        provider_id = "custom"
        provider_name = "Custom Endpoint"

        if provider == _FROM_INPUT:
            # Mode 1: All config comes from LLM_CONFIG input node
            if not llm_config:
                return self._error_result(
                    'Provider is set to "LLM_CONFIG (from input)" but no LLM_CONFIG node is connected. '
                    'Please connect a LLMs Loader node or select a different provider.'
                )
            api_key = llm_config.get("api_key", "")
            base_url = llm_config.get("base_url", "")
            actual_model = llm_config.get("model", "") or actual_model
            provider_id = llm_config.get("provider", "custom")
            provider_name = provider_id
        else:
            # Mode 2: Config from Provider Manager (providers.json)
            p_config = self._get_provider_config(provider)
            if p_config:
                provider_id = p_config["id"]
                provider_name = p_config["name"]
                api_key = p_config.get("apiKey", "") or api_key
                base_url = p_config.get("apiHost", "") or base_url

        # ── Input validation (fail fast, don't waste API quota) ──────
        if not prompt or not prompt.strip():
            return self._error_result("Prompt is empty. Please enter content to generate.")
        if not api_key or not api_key.strip():
            return self._error_result(
                "API Key is missing. Please configure it in the [⚙️ LLMs] settings "
                "or provide a Custom API Key."
            )
        if not base_url or not base_url.strip():
            return self._error_result(
                "Base URL is missing. Please configure it in the settings."
            )
        if not actual_model or not actual_model.strip():
            return self._error_result(
                "No Model selected. Please select a model or provide a Custom Model."
            )

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
        print(f"{self.TAG} Using config: {provider_name} / {actual_model}")
        start = self._log_start(
            provider_name, actual_model, system_prompt, prompt, image_input
        )

        # ── Build messages ───────────────────────────────────────────
        content = _build_content(prompt, image_input)
        messages = _build_messages(content, system_prompt, provider_name)
        messages = self._apply_memory(messages, enable_memory, unique_id)

        # ── o1/o3 System Role Downgrade (Compatibility) ──────────────
        if re.search(r'\bo[1-3](?:-mini|-preview)?\b', actual_model):
            for i, msg in enumerate(messages):
                if msg["role"] == "system":
                    messages[i] = {"role": "user", "content": msg["content"]}
                    messages.insert(i + 1, {"role": "assistant", "content": "Understood, I will follow your instructions."})
                    break

        # ── Build payload (clean, standard fields) ────────────
        payload = {
            "model": actual_model,
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
                print(f"[LLMs_Toolkit] 🧠 Reasoning content captured ({len(reasoning_content)} chars): \n{reasoning_content[:150]}...\n")

            # Extract real token usage from API response (prefer actual over estimate)
            usage = data.get("usage", {})
            input_tokens = usage.get("prompt_tokens", 0) or len(prompt)
            output_tokens = usage.get("completion_tokens", 0)

            self._log_done(response_content, input_tokens, output_tokens, start)
            self._log_usage(provider_name, actual_model, input_tokens, output_tokens, start)
            
            # Save assistant response to memory if enabled
            if enable_memory and unique_id:
                history = self._MEMORY_STORE.get(unique_id, [])
                history.append({"role": "assistant", "content": response_content})
                
            return self._success(response_content, reasoning_content, input_tokens, output_tokens)

        except Exception as e:
            elapsed_ms = int((time.time() - start) * 1000)
            err = classify_error(e, provider_name, actual_model, request_size_mb, elapsed_ms)
            log_error(err, provider_name, actual_model, request_size_mb, elapsed_ms)
            self._log_usage(provider_name, actual_model, 0, 0, start, status="error")

            # Graceful degradation: return error text instead of crashing
            return self._error_result(err.user_message())


# ComfyUI node registration
NODE_CLASS_MAPPINGS = {"OpenAICompatibleLoader": OpenAICompatibleLoader}
NODE_DISPLAY_NAME_MAPPINGS = {"OpenAICompatibleLoader": "OpenAI Compatible Adapter"}
