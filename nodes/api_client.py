"""
LLMClient — Robust HTTP client for OpenAI-compatible LLM APIs.

Single source of truth for all API calls in ComfyUI-LLMs-Toolkit.
Features:
  - Smart retry with Retry-After header respect + exponential backoff + jitter
  - Structured error diagnostics with actionable hints
  - SSL compatibility for Chinese API providers
  - Request size logging
"""

import time
import random
import json
import ssl
import re
import urllib.request
import urllib.error
from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass, field


# ─── Error Classification ────────────────────────────────────────────────────

@dataclass
class APIError:
    """Structured API error with diagnostics"""
    error_type: str
    cause: str
    hint: str
    details: list = field(default_factory=list)
    api_message: str = ""

    def user_message(self) -> str:
        """Format a user-friendly error message (for graceful degradation)"""
        parts = [f"[{self.error_type}] {self.cause}"]
        if self.api_message:
            parts.append(f"API: {self.api_message[:120]}")
        parts.append(f"建议: {self.hint}")
        return "\n".join(parts)


def classify_error(
    error: Exception,
    provider_name: str,
    model: str,
    request_size_mb: float = 0.0,
    elapsed_ms: int = 0
) -> APIError:
    """Classify an exception into a structured APIError with diagnostics."""
    error_str = str(error)
    err = APIError(
        error_type="UNKNOWN",
        cause=error_str[:200],
        hint="检查终端完整日志获取更多信息"
    )

    if "HTTP 401" in error_str or "invalid_api_key" in error_str or "Unauthorized" in error_str:
        err.error_type = "AUTH"
        err.cause = "API Key 无效或已过期"
        err.hint = f"请检查 {provider_name} 的 API Key 是否正确配置"
        err.details.append("验证失败,请确认 API Key 有效且未过期")

    elif "HTTP 429" in error_str or "rate_limit" in error_str:
        err.error_type = "RATE_LIMIT"
        err.cause = "请求频率超限 (已自动重试后仍失败)"
        err.hint = "请等待片刻后重试，或升级 API 套餐"
        err.details.append("触发了速率限制")

    elif "HTTP 413" in error_str or "Payload Too Large" in error_str:
        err.error_type = "PAYLOAD_TOO_LARGE"
        err.cause = f"请求体过大 ({request_size_mb:.2f}MB)"
        err.hint = "请压缩图片或减少输入内容"
        err.details.append("建议: 压缩图片到 1024x1024 以下,或降低图片质量")

    elif "HTTP 400" in error_str or "invalid_request" in error_str:
        err.error_type = "BAD_REQUEST"
        err.cause = "请求参数有误"
        err.hint = f"请检查模型名称 '{model}' 是否正确"
        if request_size_mb > 10:
            err.details.append(f"请求体较大 ({request_size_mb:.2f}MB),可能超过服务器限制")

    elif "HTTP 404" in error_str or "model_not_found" in error_str:
        err.error_type = "MODEL"
        err.cause = f"模型 '{model}' 不存在"
        err.hint = f"请确认 {provider_name} 支持该模型名称"

    elif "HTTP 5" in error_str:
        err.error_type = "SERVER"
        err.cause = "API 服务端错误 (已自动重试后仍失败)"
        err.hint = f"{provider_name} 服务可能暂时不可用，请稍后重试"

    elif "Broken pipe" in error_str:
        err.error_type = "BROKEN_PIPE"
        err.cause = "连接在传输数据时被服务器关闭"
        err.hint = "可能是请求体过大或服务器超时"
        if request_size_mb > 5:
            err.details.append(f"请求体很大 ({request_size_mb:.2f}MB),建议压缩图片")

    elif "timed out" in error_str.lower() or "timeout" in error_str.lower():
        err.error_type = "TIMEOUT"
        err.cause = f"请求超时 ({elapsed_ms / 1000:.1f}秒)"
        err.hint = "网络连接缓慢或 API 响应时间过长"

    elif "connection" in error_str.lower() or "URLError" in type(error).__name__:
        err.error_type = "NETWORK"
        err.cause = "无法连接到 API 服务器"
        err.hint = "请检查网络连接和代理设置"
        err.details.append("可能原因: 网络断开 / 防火墙阻止 / 代理配置错误")

    elif "missing 'choices'" in error_str:
        err.error_type = "RESPONSE"
        err.cause = "API 返回了非标准格式"
        err.hint = "API 可能返回了错误信息而非正常结果"

    # Extract API error message from JSON
    msg_match = re.search(r'"message"\s*:\s*"([^"]+)"', error_str)
    if msg_match:
        err.api_message = msg_match.group(1)

    return err


def log_error(err: APIError, provider_name: str, model: str,
              request_size_mb: float, elapsed_ms: int) -> None:
    """Print structured error block to terminal."""
    ts = time.strftime('%H:%M:%S')
    print(f"")
    print(f"[LLMs_Toolkit] {ts} ✗ {err.error_type} ERROR ({elapsed_ms}ms)")
    print(f"   ┌──────────────────────────────────────────────")
    print(f"   │ 服务商  {provider_name}")
    print(f"   │ 模型    {model or 'default'}")
    if request_size_mb > 0:
        print(f"   │ 请求大小 {request_size_mb:.2f} MB")
    print(f"   │ 原因    {err.cause}")
    if err.api_message:
        print(f"   │ API消息 {err.api_message[:120]}")
    print(f"   │ 建议    {err.hint}")
    if err.details:
        print(f"   │")
        for i, detail in enumerate(err.details, 1):
            print(f"   │   {i}. {detail}")
    print(f"   └──────────────────────────────────────────────")
    print(f"")


# ─── HTTP Client ─────────────────────────────────────────────────────────────

# Shared SSL context (created once, reused across all calls)
_ssl_context = None

def _get_ssl_context() -> ssl.SSLContext:
    """Get or create a lenient SSL context for Chinese API providers."""
    global _ssl_context
    if _ssl_context is None:
        _ssl_context = ssl.create_default_context()
        _ssl_context.check_hostname = False
        _ssl_context.verify_mode = ssl.CERT_NONE
        _ssl_context.set_ciphers("DEFAULT")
        _ssl_context.options |= getattr(ssl, "OP_LEGACY_SERVER_CONNECT", 0)
    return _ssl_context


def _normalize_url(base_url: str, path: str = "/chat/completions") -> str:
    """Normalize base URL and append path, avoiding double slashes."""
    return base_url.rstrip("/") + path


def _parse_retry_after(headers) -> Optional[float]:
    """Extract Retry-After value from response headers (seconds)."""
    retry_after = headers.get("Retry-After")
    if retry_after:
        try:
            return float(retry_after)
        except ValueError:
            pass
    return None


def _is_retryable(code: int) -> bool:
    """Check if an HTTP status code warrants a retry."""
    return code == 429 or (500 <= code < 600)


class LLMClient:
    """
    Robust HTTP client for OpenAI-compatible chat completions API.

    Usage:
        client = LLMClient(base_url, api_key)
        content, data = client.chat(payload)
    """

    TAG = "[LLMs_Toolkit]"

    def __init__(
        self,
        base_url: str,
        api_key: str,
        max_retries: int = 3,
        timeout: int = 180,
    ):
        self.url = _normalize_url(base_url)
        self.api_key = api_key
        self.max_retries = max_retries
        self.timeout = timeout
        self._ctx = _get_ssl_context()

    def chat(self, payload: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Send a chat completion request.

        Returns:
            Tuple of (response_content, full_response_data)

        Raises:
            Exception with structured error message if all retries fail.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/event-stream",
            "Connection": "keep-alive"
        }

        data_bytes = json.dumps(payload).encode("utf-8")
        data_size_mb = len(data_bytes) / (1024 * 1024)
        if data_size_mb > 1:
            print(f"{self.TAG} 请求体大小: {data_size_mb:.2f} MB")

        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                req = urllib.request.Request(
                    self.url, data=data_bytes, headers=headers, method="POST"
                )
                with urllib.request.urlopen(
                    req, timeout=self.timeout, context=self._ctx
                ) as resp:
                    body = resp.read().decode("utf-8")
                    data = json.loads(body)

                    if "choices" not in data or len(data["choices"]) == 0:
                        raise ValueError(
                            f"API response missing 'choices'. Response: {json.dumps(data)[:300]}"
                        )

                    content = data["choices"][0]["message"]["content"]
                    return content, data

            except urllib.error.HTTPError as e:
                error_body = e.read().decode("utf-8", errors="replace")

                if _is_retryable(e.code) and attempt < self.max_retries:
                    # Respect Retry-After header if present
                    wait = _parse_retry_after(e.headers) or self._backoff(attempt, is_rate_limit=(e.code == 429))
                    print(
                        f"{self.TAG} HTTP {e.code} 错误, "
                        f"重试 {attempt + 1}/{self.max_retries} "
                        f"(等待 {wait:.1f}s)..."
                    )
                    time.sleep(wait)
                    continue

                raise Exception(f"HTTP {e.code} | {error_body}")

            except urllib.error.URLError as e:
                last_error = e
                error_msg = str(e.reason)

                if self._is_connection_error(error_msg) and attempt < self.max_retries:
                    wait = self._backoff(attempt)
                    print(f"{self.TAG} 连接错误, 重试 {attempt + 1}/{self.max_retries} (等待 {wait:.1f}s)...")
                    time.sleep(wait)
                    continue

                raise Exception(f"URLError | {error_msg}")

            except (TimeoutError, OSError) as e:
                last_error = e
                if attempt < self.max_retries:
                    wait = self._backoff(attempt)
                    print(f"{self.TAG} 超时/IO错误, 重试 {attempt + 1}/{self.max_retries} (等待 {wait:.1f}s)...")
                    time.sleep(wait)
                    continue
                raise Exception(f"TimeoutError | 请求超过 {self.timeout} 秒未响应")

        # All retries exhausted
        if last_error:
            raise Exception(
                f"URLError | {str(getattr(last_error, 'reason', last_error))} "
                f"(重试 {self.max_retries} 次后仍失败)"
            )
        raise Exception("Unknown error occurred")

    @staticmethod
    def _backoff(attempt: int, is_rate_limit: bool = False) -> float:
        """Calculate wait time with exponential backoff + jitter."""
        base = 2 ** attempt
        if is_rate_limit:
            base = max(5, base * 3)  # Much longer for rate limits
        jitter = random.uniform(0, base * 0.3)
        return base + jitter

    @staticmethod
    def _is_connection_error(msg: str) -> bool:
        """Check if error message indicates a retryable connection issue."""
        keywords = ("Broken pipe", "Connection", "EOF", "reset by peer", "ECONNRESET")
        return any(kw.lower() in msg.lower() for kw in keywords)
