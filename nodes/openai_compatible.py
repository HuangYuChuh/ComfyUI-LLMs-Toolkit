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
    
    RETURN_TYPES = ("STRING", "INT", "INT")
    RETURN_NAMES = ("text", "input_tokens", "output_tokens")
    FUNCTION = "generate"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/Generate"
    OUTPUT_NODE = True
    
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
        model: str,
        request_size_mb: float = 0.0
    ) -> None:
        """Structured error logging with diagnostics and actionable hints"""
        elapsed_ms = int((time.time() - self._request_start_time) * 1000)
        ts = time.strftime('%H:%M:%S')

        # Classify error and extract details
        error_str = str(error)
        error_type = "UNKNOWN"
        cause = error_str
        hint = "检查终端完整日志获取更多信息"
        details = []  # Additional diagnostic details
        
        if "HTTP 401" in error_str or "invalid_api_key" in error_str or "Unauthorized" in error_str:
            error_type = "AUTH"
            cause = "API Key 无效或已过期"
            hint = f"请检查 {provider.name} 的 API Key 是否正确配置"
            details.append("验证失败,请确认 API Key 有效且未过期")

        elif "HTTP 429" in error_str or "rate_limit" in error_str:
            error_type = "RATE_LIMIT"
            cause = "请求频率超限"
            hint = "请等待片刻后重试，或升级 API 套餐"
            details.append("触发了速率限制,建议降低请求频率")

        elif "HTTP 413" in error_str or "Payload Too Large" in error_str:
            error_type = "PAYLOAD_TOO_LARGE"
            cause = f"请求体过大 ({request_size_mb:.2f}MB)"
            hint = "请压缩图片或减少输入内容"
            details.append("服务器拒绝接收过大的请求")
            details.append("建议: 压缩图片到 1024x1024 以下,或降低图片质量")

        elif "HTTP 400" in error_str or "invalid_request" in error_str:
            error_type = "BAD_REQUEST"
            cause = "请求参数有误"
            hint = f"请检查模型名称 '{model}' 是否正确"
            if request_size_mb > 10:
                details.append(f"请求体较大 ({request_size_mb:.2f}MB),可能超过服务器限制")
            details.append("检查所有参数是否符合 API 要求")

        elif "HTTP 404" in error_str or "model_not_found" in error_str:
            error_type = "MODEL"
            cause = f"模型 '{model}' 不存在"
            hint = f"请确认 {provider.name} 支持该模型名称"
            details.append("模型名称可能拼写错误或该服务商不支持此模型")

        elif "HTTP 5" in error_str:
            error_type = "SERVER"
            cause = "API 服务端错误"
            hint = f"{provider.name} 服务可能暂时不可用，请稍后重试"
            details.append("这是服务器端的问题,不是客户端配置错误")

        elif "Broken pipe" in error_str:
            error_type = "BROKEN_PIPE"
            cause = "连接在传输数据时被服务器关闭"
            hint = "可能是请求体过大或服务器超时"
            if request_size_mb > 5:
                details.append(f"请求体很大 ({request_size_mb:.2f}MB),建议压缩图片")
            if elapsed_ms > 60000:
                details.append(f"传输时间过长 ({elapsed_ms/1000:.1f}秒),可能触发服务器超时")
            details.append("建议: 1) 压缩图片 2) 检查网络上传速度 3) 使用更快的网络")

        elif "TimeoutError" in type(error).__name__ or "timed out" in error_str.lower():
            error_type = "TIMEOUT"
            cause = f"请求超时 ({elapsed_ms/1000:.1f}秒)"
            hint = "网络连接缓慢或 API 响应时间过长"
            if request_size_mb > 5:
                details.append(f"请求体较大 ({request_size_mb:.2f}MB),传输需要更长时间")
            details.append("建议: 检查网络连接速度")

        elif "URLError" in type(error).__name__ or "connection" in error_str.lower():
            error_type = "NETWORK"
            cause = "无法连接到 API 服务器"
            hint = "请检查网络连接和代理设置"
            details.append("可能原因: 1) 网络断开 2) 防火墙阻止 3) 代理配置错误")

        elif "missing 'choices'" in error_str:
            error_type = "RESPONSE"
            cause = "API 返回了非标准格式"
            hint = "API 可能返回了错误信息而非正常结果"
            details.append("服务器返回的响应格式不符合预期")
        
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
        if request_size_mb > 0:
            print(f"   │ 请求大小 {request_size_mb:.2f} MB")
        print(f"   │ 原因    {cause}")
        if api_message:
            print(f"   │ API消息 {api_message[:120]}")
        print(f"   │ 建议    {hint}")

        # Print additional diagnostic details
        if details:
            print(f"   │")
            print(f"   │ 详细诊断:")
            for i, detail in enumerate(details, 1):
                print(f"   │   {i}. {detail}")

        print(f"   └──────────────────────────────────────────────")
        print(f"")
    
    def _sync_api_call(
        self,
        endpoint: str,
        payload: Dict[str, Any],
        api_key: str,
        max_retries: int = 2
    ) -> Tuple[str, Dict[str, Any]]:
        """Synchronous API call using urllib (avoids asyncio event loop conflicts)"""
        url = f"{endpoint}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        data_bytes = json_lib.dumps(payload).encode("utf-8")

        # Log request size for debugging
        data_size_mb = len(data_bytes) / (1024 * 1024)
        if data_size_mb > 1:
            print(f"[LLMs_Toolkit] 图片请求体大小: {data_size_mb:.2f} MB")

        last_error = None
        for attempt in range(max_retries + 1):
            try:
                req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")

                with urllib.request.urlopen(req, timeout=180) as response:
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
                last_error = e
                error_msg = str(e.reason)

                # Check if it's a broken pipe or connection error
                if "Broken pipe" in error_msg or "Connection" in error_msg:
                    if attempt < max_retries:
                        print(f"[LLMs_Toolkit] 连接错误,重试 {attempt + 1}/{max_retries}...")
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue

                raise Exception(f"URLError | {error_msg}")
            except TimeoutError:
                raise Exception(f"TimeoutError | 请求超过 180 秒未响应")

        # If all retries failed
        if last_error:
            raise Exception(f"URLError | {str(last_error.reason)} (重试 {max_retries} 次后仍失败)")

        raise Exception("Unknown error occurred")
    
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
        max_tokens: int = 2048,
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
        provider_name = llm_config.get("provider", "Custom")

        # Log using config
        print(f"[LLMs_Toolkit] 使用配置: {provider_name} / {model}")

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
        provider = ProviderRegistry.get_provider(provider_name)
        
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

        # Calculate request size for error logging
        payload_bytes = json_lib.dumps(payload).encode("utf-8")
        request_size_mb = len(payload_bytes) / (1024 * 1024)

        # Estimate input tokens
        input_tokens = TokenEstimator.estimate_input_tokens(
            prompt, system_prompt, image_input
        )

        try:
            # Synchronous call to avoid asyncio event loop conflicts
            response_content, data = self._sync_api_call(
                base_url, payload, api_key
            )

            # Extract actual token usage from response
            output_tokens = data.get("usage", {}).get("completion_tokens", 0)

            # Log completion
            self._log_request_complete(response_content, input_tokens, output_tokens)

            return {
                "ui": {
                    "text": [f"Token Usage:\nInput: {int(input_tokens)}\nOutput: {int(output_tokens)}"]
                },
                "result": (response_content, int(input_tokens), int(output_tokens))
            }

        except Exception as e:
            self._log_error(e, provider, model, request_size_mb)
            raise


# ComfyUI node registration
NODE_CLASS_MAPPINGS = {"OpenAICompatibleLoader": OpenAICompatibleLoader}
NODE_DISPLAY_NAME_MAPPINGS = {"OpenAICompatibleLoader": "OpenAI Compatible Adapter"}

