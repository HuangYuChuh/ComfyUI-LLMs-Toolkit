import time
import random
import json as json_lib
import urllib.request
import urllib.error
from typing import Optional, List, Dict, Tuple, Any, Union
from dataclasses import dataclass


@dataclass
class ProviderConfig:
    """LLM provider endpoint configuration"""
    name: str
    base_url: str
    requires_string_content: bool = False


class ProviderRegistry:
    """Centralized registry for LLM API providers"""
    
    PROVIDERS = {
        "Qwen/通义千问": ProviderConfig(
            "Qwen", 
            "https://dashscope.aliyuncs.com/compatible-mode/v1"
        ),
        "DeepSeek/深度求索": ProviderConfig(
            "DeepSeek", 
            "https://api.deepseek.com/v1/"
        ),
        "DouBao/豆包": ProviderConfig(
            "DouBao", 
            "https://ark.cn-beijing.volces.com/api/v3/"
        ),
        "Spark/星火": ProviderConfig(
            "Spark", 
            "https://spark-api-open.xf-yun.com/v1/",
            requires_string_content=True
        ),
        "GLM/智谱清言": ProviderConfig(
            "GLM", 
            "https://open.bigmodel.cn/api/paas/v4/"
        ),
        "Moonshot/月之暗面": ProviderConfig(
            "Moonshot", 
            "https://api.moonshot.cn/v1"
        ),
        "Baichuan/百川": ProviderConfig(
            "Baichuan", 
            "https://api.baichuan-ai.com/v1/",
            requires_string_content=True
        ),
        "MiniMax/MiniMax": ProviderConfig(
            "MiniMax", 
            "https://api.minimax.chat/v1/"
        ),
        "StepFun/阶跃星辰": ProviderConfig(
            "StepFun", 
            "https://api.stepfun.com/v1/"
        ),
        "SenseChat/日日新": ProviderConfig(
            "SenseChat", 
            "https://api.sensenova.cn/compatible-mode/v1",
            requires_string_content=True
        ),
    }
    
    @classmethod
    def get_provider(cls, provider_key: str) -> ProviderConfig:
        """Get provider config or treat key as custom URL"""
        return cls.PROVIDERS.get(provider_key.strip(), 
                                 ProviderConfig("Custom", provider_key.strip()))


class MessageBuilder:
    """Builds chat messages with support for multimodal content"""
    
    @staticmethod
    def build_content(prompt: str, image_url: Optional[Union[str, List[str]]] = None) -> List[Dict[str, Any]]:
        """Build content array for user message"""
        content = []
        
        if image_url:
            if isinstance(image_url, list):
                 for url in image_url:
                     if isinstance(url, str) and url.startswith("data:image"):
                         content.append({
                             "type": "image_url",
                             "image_url": {"url": url}
                         })
            elif isinstance(image_url, str):
                if not image_url.startswith("data:image"):
                    raise ValueError("Image must be a valid base64 data URL")
                content.append({
                    "type": "image_url",
                    "image_url": {"url": image_url}
                })
        
        if prompt.strip():
            content.append({
                "type": "text",
                "text": prompt
            })
        
        if not content:
            raise ValueError("Content cannot be empty")
        
        return content
    
    @staticmethod
    def build_messages(
        content: List[Dict[str, Any]],
        system_prompt: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Build complete message array"""
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": content
        })
        
        return messages
    
    @staticmethod
    def adapt_for_provider(
        messages: List[Dict[str, Any]],
        provider: ProviderConfig,
        prompt: str
    ) -> List[Dict[str, Any]]:
        """Adapt messages for provider-specific requirements"""
        if provider.requires_string_content:
            # Some providers require string content, not structured arrays
            adapted = []
            for msg in messages:
                if msg["role"] == "system":
                    adapted.append(msg)
                elif msg["role"] == "user":
                    adapted.append({
                        "role": "user",
                        "content": prompt if isinstance(prompt, str) else prompt
                    })
            return adapted
        return messages


class TokenEstimator:
    """Estimates token usage for billing/logging purposes"""
    
    @staticmethod
    def estimate_input_tokens(
        prompt: str,
        system_prompt: Optional[str] = None,
        image_url: Optional[Union[str, List[str]]] = None
    ) -> int:
        """Simple character-based token estimation"""
        tokens = len(prompt)
        
        if system_prompt:
            tokens += len(system_prompt)
        
        if image_url:
            if isinstance(image_url, list):
                for url in image_url:
                    if isinstance(url, str):
                         tokens += len(url) // 1000
            elif isinstance(image_url, str):
                # Rough estimate: base64 image ~= length/1000 tokens
                tokens += len(image_url) // 1000
        
        return tokens


class OpenAICompatibleLoader:
    """
    OpenAI-compatible API adapter for ComfyUI
    
    Supports multiple LLM providers with unified interface.
    Designed for extensibility and clean architecture.
    """
    
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
                    "default": 512,
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
    
    RETURN_TYPES = ("STRING", "INT", "INT")
    RETURN_NAMES = ("text", "input_tokens", "output_tokens")
    FUNCTION = "generate"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/Generate"
    
    def __init__(self):
        self._conversation_history: List[Dict[str, Any]] = []
        self._request_start_time: float = 0.0
    
    def _log_request_start(
        self,
        provider: ProviderConfig,
        model: str,
        system_prompt: Optional[str],
        prompt: str,
        image_input: Optional[Union[str, List[str]]]
    ) -> None:
        """Geek-style request logging with timing"""
        self._request_start_time = time.time()
        ts = time.strftime('%H:%M:%S')
        
        # Build context flags
        flags = []
        if system_prompt:
            flags.append('sys')
            
        img_count = 0
        if image_input:
            if isinstance(image_input, list):
                img_count = len(image_input)
            else:
                img_count = 1
            flags.append(f'img(x{img_count})')
        
        flag_str = f"[{' '.join(flags)}]" if flags else ""
        
        # Compact header
        print(f"[LLMs_Toolkit] {ts} → {provider.name}/{model or 'default'} {flag_str}")
        
        # Content preview (indented)
        if system_prompt:
            sys_preview = system_prompt[:60].replace('\n', ' ')
            print(f"   sys│ {sys_preview}...")
        
        prompt_preview = prompt[:80].replace('\n', ' ')
        print(f"   in │ {prompt_preview}...")
    
    def _log_request_complete(
        self,
        response: str,
        input_tokens: int,
        output_tokens: int
    ) -> None:
        """Geek-style completion logging with metrics"""
        # Calculate elapsed time
        elapsed_ms = int((time.time() - self._request_start_time) * 1000)
        
        # Format token counts (k suffix for thousands)
        in_tok = f"{input_tokens/1000:.1f}k" if input_tokens >= 1000 else str(input_tokens)
        out_tok = f"{output_tokens/1000:.1f}k" if output_tokens >= 1000 else str(output_tokens)
        
        # Response preview
        preview = response[:80].replace('\n', ' ')
        
        print(f"   out│ {preview}...")
        print(f"[LLMs_Toolkit] {time.strftime('%H:%M:%S')} ← {in_tok}/{out_tok}t ({elapsed_ms}ms)\n")
    
    def _log_error(
        self,
        error: Exception,
        provider: 'ProviderConfig',
        model: str
    ) -> None:
        """Structured error logging with diagnostics and actionable hints"""
        elapsed_ms = int((time.time() - self._request_start_time) * 1000)
        ts = time.strftime('%H:%M:%S')
        
        # Classify error and extract details
        error_str = str(error)
        error_type = "UNKNOWN"
        cause = error_str
        hint = "检查终端完整日志获取更多信息"
        
        if "HTTP 401" in error_str or "invalid_api_key" in error_str or "Unauthorized" in error_str:
            error_type = "AUTH"
            cause = "API Key 无效或已过期"
            hint = f"请检查 {provider.name} 的 API Key 是否正确配置"
        elif "HTTP 429" in error_str or "rate_limit" in error_str:
            error_type = "RATE_LIMIT"
            cause = "请求频率超限"
            hint = "请等待片刻后重试，或升级 API 套餐"
        elif "HTTP 400" in error_str or "invalid_request" in error_str:
            error_type = "BAD_REQUEST"
            cause = "请求参数有误"
            hint = f"请检查模型名称 '{model}' 是否正确"
        elif "HTTP 404" in error_str or "model_not_found" in error_str:
            error_type = "MODEL"
            cause = f"模型 '{model}' 不存在"
            hint = f"请确认 {provider.name} 支持该模型名称"
        elif "HTTP 5" in error_str:
            error_type = "SERVER"
            cause = "API 服务端错误"
            hint = f"{provider.name} 服务可能暂时不可用，请稍后重试"
        elif "TimeoutError" in type(error).__name__ or "timed out" in error_str.lower():
            error_type = "TIMEOUT"
            cause = f"请求超时 ({elapsed_ms}ms)"
            hint = "网络连接缓慢或 API 响应时间过长"
        elif "URLError" in type(error).__name__ or "connection" in error_str.lower():
            error_type = "NETWORK"
            cause = "无法连接到 API 服务器"
            hint = "请检查网络连接和代理设置"
        elif "missing 'choices'" in error_str:
            error_type = "RESPONSE"
            cause = "API 返回了非标准格式"
            hint = "API 可能返回了错误信息而非正常结果"
        
        # Parse API error message if present
        api_message = ""
        if '"message"' in error_str:
            try:
                # Try to extract JSON error message
                import re
                msg_match = re.search(r'"message"\s*:\s*"([^"]+)"', error_str)
                if msg_match:
                    api_message = msg_match.group(1)
            except Exception:
                pass
        
        # Print structured error block
        print(f"")
        print(f"[LLMs_Toolkit] {ts} ✗ {error_type} ERROR ({elapsed_ms}ms)")
        print(f"   ┌──────────────────────────────────────────────")
        print(f"   │ 服务商  {provider.name}")
        print(f"   │ 模型    {model or 'default'}")
        print(f"   │ 原因    {cause}")
        if api_message:
            print(f"   │ API消息 {api_message[:120]}")
        print(f"   │ 建议    {hint}")
        print(f"   └──────────────────────────────────────────────")
        print(f"")
    
    def _sync_api_call(
        self,
        endpoint: str,
        payload: Dict[str, Any],
        api_key: str
    ) -> Tuple[str, Dict[str, Any]]:
        """Synchronous API call using urllib (avoids asyncio event loop conflicts)"""
        url = f"{endpoint}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data_bytes = json_lib.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                response_body = response.read().decode("utf-8")
                data = json_lib.loads(response_body)
                
                if "choices" not in data or len(data["choices"]) == 0:
                    raise ValueError(f"API response missing 'choices'. Full response: {data}")
                
                content = data["choices"][0]["message"]["content"]
                return content, data
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            raise Exception(f"HTTP {e.code} | {error_body}")
        except urllib.error.URLError as e:
            raise Exception(f"URLError | {str(e.reason)}")
        except TimeoutError:
            raise Exception(f"TimeoutError | 请求超过 120 秒未响应")
    
    def _build_payload(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Build API request payload"""
        return {
            "model": model or "glm-4",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "request_id": f"req-{int(time.time() * 1000)}-{random.randint(1000, 9999)}",
            "timestamp": int(time.time() * 1000),
            "seed": random.randint(1, 1000000)
        }
    
    def _manage_conversation_history(
        self,
        messages: List[Dict[str, Any]],
        enable_memory: bool
    ) -> List[Dict[str, Any]]:
        """Manage conversation history with memory support"""
        if not enable_memory:
            self._conversation_history = []
            return messages
        
        # Append to history and return full context
        for msg in messages:
            if not any(
                h["role"] == msg["role"] and h["content"] == msg["content"]
                for h in self._conversation_history
            ):
                self._conversation_history.append(msg)
        
        return self._conversation_history
    
    def generate(
        self,
        llm_config: Dict[str, Any],
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 512,
        system_prompt: Optional[str] = None,
        prep_img: Optional[str] = None,
        enable_memory: bool = False,
        seed: int = 0
    ) -> Tuple[str, int, int]:
        """Main generation entry point"""

        # Extract config parameters
        base_url = llm_config.get("base_url", "")
        model = llm_config.get("model", "")
        api_key = llm_config.get("api_key", "")
        provider = llm_config.get("provider", "Custom")

        # Log using config
        print(f"[LLMs_Toolkit] 使用配置: {provider} / {model}")

        # Handle prep_img: parse JSON list if applicable
        image_input = None
        if prep_img:
            if prep_img.strip().startswith("["):
                try:
                    image_input = json_lib.loads(prep_img)
                except Exception:
                    # Fallback: treat as single string
                    image_input = prep_img
            else:
                image_input = prep_img
        
        # Get provider configuration
        provider = ProviderRegistry.get_provider(base_url)
        
        # Log request details
        self._log_request_start(
            provider=provider,
            model=model,
            system_prompt=system_prompt,
            prompt=prompt,
            image_input=image_input
        )
        
        # Build message content
        content = MessageBuilder.build_content(prompt, image_input)
        
        # Build messages with system prompt
        messages = MessageBuilder.build_messages(content, system_prompt)
        
        # Apply provider-specific adaptations
        messages = MessageBuilder.adapt_for_provider(messages, provider, prompt)
        
        # Manage conversation history
        messages = self._manage_conversation_history(messages, enable_memory)
        
        # Build request payload
        payload = self._build_payload(model, messages, temperature, max_tokens)
        
        # Estimate input tokens
        input_tokens = TokenEstimator.estimate_input_tokens(
            prompt, system_prompt, image_input
        )
        
        try:
            # Synchronous call to avoid asyncio event loop conflicts
            response_content, data = self._sync_api_call(
                provider.base_url, payload, api_key
            )
            
            # Extract actual token usage from response
            output_tokens = data.get("usage", {}).get("completion_tokens", 0)
            
            # Log completion
            self._log_request_complete(response_content, input_tokens, output_tokens)
            
            return (response_content, int(input_tokens), int(output_tokens))
            
        except Exception as e:
            self._log_error(e, provider, model)
            raise


# ComfyUI node registration
NODE_CLASS_MAPPINGS = {"OpenAICompatibleLoader": OpenAICompatibleLoader}
NODE_DISPLAY_NAME_MAPPINGS = {"OpenAICompatibleLoader": "OpenAI Compatible Adapter"}

WEB_DIRECTORY = "./web"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
