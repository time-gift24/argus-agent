"""Provider connectivity test service using langchain-openai."""

from __future__ import annotations

import json
import time

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from app.core.config import settings
from app.core.crypto import decrypt
from app.models.user import Provider
from app.schemas.user import ProviderTestResult

_AUTH_ERROR_HINTS = (
    "401",
    "unauthorized",
    "authentication",
    "incorrect api key",
    "invalid api key",
    "api key provided",
)

_NETWORK_ERROR_HINTS = (
    "timeout",
    "timed out",
    "connection",
    "refused",
    "dns",
    "unreachable",
    "failed to resolve",
)

_RATE_LIMIT_ERROR_HINTS = (
    "429",
    "rate limit",
    "too many requests",
    "quota",
    "insufficient_quota",
)

_MODEL_ERROR_HINTS = (
    "model_not_found",
    "invalid model",
    "does not exist",
    "unsupported parameter",
    "unsupported value",
    "unrecognized request argument",
)

_SERVER_ERROR_HINTS = (
    "500",
    "502",
    "503",
    "504",
    "bad gateway",
    "service unavailable",
    "internal server error",
)

_NON_OPENAI_BASE_URL_HINTS = (
    "api.anthropic.com",
    "anthropic.com",
    "generativelanguage.googleapis.com",
    "googleapis.com",
    "aiplatform.googleapis.com",
)


def _build_kwargs(config: dict) -> dict:
    """Build ChatOpenAI kwargs from a config dict."""
    kwargs: dict = {
        "api_key": config["api_key"],
        "request_timeout": 10,
        "max_tokens": 5,
        "streaming": True,
    }
    if config.get("base_url"):
        kwargs["base_url"] = config["base_url"]
    if config.get("model"):
        kwargs["model"] = config["model"]
    return kwargs


def _looks_non_openai_compatible(base_url: str | None) -> bool:
    """Best-effort detection for providers that do not expose OpenAI chat endpoints."""
    text = (base_url or "").lower()
    return any(hint in text for hint in _NON_OPENAI_BASE_URL_HINTS)


def _normalize_probe_error(error: Exception, kwargs: dict) -> str:
    """Map upstream exceptions to safe user-facing messages."""
    text = str(error).lower()
    if any(hint in text for hint in _AUTH_ERROR_HINTS):
        return "认证失败，请检查 API Key 是否正确"
    if any(hint in text for hint in _RATE_LIMIT_ERROR_HINTS):
        return "请求过于频繁或额度不足，请稍后重试"
    if any(hint in text for hint in _NETWORK_ERROR_HINTS):
        return "连接失败，请检查 Base URL 或网络后重试"
    if (
        _looks_non_openai_compatible(kwargs.get("base_url"))
        and ("chat/completions" in text or "404" in text or "not found" in text)
    ):
        return "当前测试仅支持 OpenAI-compatible Chat Completions 接口"
    if any(hint in text for hint in _MODEL_ERROR_HINTS):
        return "模型或请求参数不兼容，请检查模型名和供应商兼容性"
    if any(hint in text for hint in _SERVER_ERROR_HINTS):
        return "供应商服务暂时不可用，请稍后重试"
    return "连接测试失败，请确认供应商兼容 OpenAI-compatible Chat Completions 接口，并检查模型与配置"


def _has_meaningful_content(content) -> bool:
    """Return True when a streamed chunk contains actual user-visible content."""
    if isinstance(content, str):
        return bool(content.strip())
    if isinstance(content, list):
        return any(_has_meaningful_content(item) for item in content)
    if isinstance(content, dict):
        for key in ("text", "content", "value"):
            if key in content and _has_meaningful_content(content[key]):
                return True
        return any(_has_meaningful_content(value) for value in content.values())
    return bool(content)


def _probe(kwargs: dict) -> ProviderTestResult:
    """Open a stream and succeed after the first meaningful chunk arrives."""
    start = time.monotonic()
    try:
        llm = ChatOpenAI(**kwargs)
        for chunk in llm.stream([HumanMessage(content="Hi")]):
            if _has_meaningful_content(getattr(chunk, "content", None)):
                elapsed_ms = int((time.monotonic() - start) * 1000)
                return ProviderTestResult(success=True, message="连接成功", latency_ms=elapsed_ms)
        return ProviderTestResult(success=False, message="流式连接已建立，但未收到有效响应内容")
    except Exception as e:
        return ProviderTestResult(success=False, message=_normalize_probe_error(e, kwargs))


def test_provider_connectivity(provider: Provider) -> ProviderTestResult:
    """Test if a persisted provider's LLM config is reachable."""
    if not provider.config:
        return ProviderTestResult(success=False, message="内部提供商不支持测试")

    try:
        config_json = decrypt(provider.config, settings.aes_key_bytes)
        config = json.loads(config_json)
    except Exception as e:
        return ProviderTestResult(success=False, message=f"配置解密失败: {e}")

    if not config.get("api_key"):
        return ProviderTestResult(success=False, message="API Key 未配置")

    return _probe(_build_kwargs(config))


def test_config_connectivity(config: dict) -> ProviderTestResult:
    """Test connectivity with raw config (no Provider ORM object needed)."""
    if not config.get("api_key"):
        return ProviderTestResult(success=False, message="API Key 未配置")
    return _probe(_build_kwargs(config))
