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


def _build_kwargs(config: dict) -> dict:
    """Build ChatOpenAI kwargs from a config dict."""
    kwargs: dict = {
        "api_key": config["api_key"],
        "request_timeout": 10,
        "max_tokens": 5,
    }
    if config.get("base_url"):
        kwargs["base_url"] = config["base_url"]
    if config.get("model"):
        kwargs["model"] = config["model"]
    return kwargs


def _probe(kwargs: dict) -> ProviderTestResult:
    """Send a test message and return the result."""
    start = time.monotonic()
    try:
        llm = ChatOpenAI(**kwargs)
        llm.invoke([HumanMessage(content="Hi")])
        elapsed_ms = int((time.monotonic() - start) * 1000)
        return ProviderTestResult(success=True, message="连接成功", latency_ms=elapsed_ms)
    except Exception as e:
        return ProviderTestResult(success=False, message=str(e)[:200])


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
