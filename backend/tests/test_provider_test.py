"""Unit tests: provider connectivity test sanitization."""

from app.services import provider_test as provider_test_module


class _Chunk:
    """Simple streaming chunk test double."""

    def __init__(self, content):
        self.content = content


class _RaisingChatOpenAI:
    """Test double that simulates a streaming-capable chat model."""

    error_message = "boom"
    stream_chunks = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def stream(self, _messages):
        if self.error_message is not None:
            raise RuntimeError(self.error_message)
        for chunk in self.stream_chunks:
            yield chunk


class TestProviderConnectivityStreaming:
    def test_test_config_connectivity_succeeds_on_first_meaningful_stream_chunk(self, monkeypatch):
        _RaisingChatOpenAI.error_message = None
        _RaisingChatOpenAI.stream_chunks = [_Chunk(""), _Chunk("hello")]
        monkeypatch.setattr(provider_test_module, "ChatOpenAI", _RaisingChatOpenAI)

        result = provider_test_module.test_config_connectivity(
            {
                "api_key": "sk-stream-ok-123",
                "base_url": "https://open.bigmodel.cn/api/paas/v4",
                "model": "glm-5",
            }
        )

        assert result.success is True
        assert result.message == "连接成功"
        assert result.latency_ms is not None

    def test_test_config_connectivity_fails_when_stream_has_no_meaningful_chunks(self, monkeypatch):
        _RaisingChatOpenAI.error_message = None
        _RaisingChatOpenAI.stream_chunks = [_Chunk(""), _Chunk(None), _Chunk([])]
        monkeypatch.setattr(provider_test_module, "ChatOpenAI", _RaisingChatOpenAI)

        result = provider_test_module.test_config_connectivity(
            {
                "api_key": "sk-stream-empty-456",
                "base_url": "https://open.bigmodel.cn/api/paas/v4",
                "model": "glm-5",
            }
        )

        assert result.success is False
        assert result.latency_ms is None
        assert result.message == "流式连接已建立，但未收到有效响应内容"


class TestProviderConnectivityErrors:
    def test_test_config_connectivity_redacts_auth_error_details(self, monkeypatch):
        secret = "sk-secret-auth-123"
        _RaisingChatOpenAI.error_message = (
            f"401 Unauthorized Authorization: Bearer {secret} "
            "Incorrect API key provided"
        )
        _RaisingChatOpenAI.stream_chunks = []
        monkeypatch.setattr(provider_test_module, "ChatOpenAI", _RaisingChatOpenAI)

        result = provider_test_module.test_config_connectivity(
            {
                "api_key": secret,
                "base_url": "https://internal.example/v1",
                "model": "gpt-4o-mini",
            }
        )

        assert result.success is False
        assert result.latency_ms is None
        assert result.message == "认证失败，请检查 API Key 是否正确"
        assert secret not in result.message
        assert "Authorization" not in result.message
        assert "internal.example" not in result.message

    def test_test_config_connectivity_redacts_network_error_details(self, monkeypatch):
        secret = "sk-secret-network-456"
        _RaisingChatOpenAI.error_message = (
            f"Connection timeout while reaching https://internal.example/v1 "
            f"with Authorization: Bearer {secret}"
        )
        _RaisingChatOpenAI.stream_chunks = []
        monkeypatch.setattr(provider_test_module, "ChatOpenAI", _RaisingChatOpenAI)

        result = provider_test_module.test_config_connectivity(
            {
                "api_key": secret,
                "base_url": "https://internal.example/v1",
            }
        )

        assert result.success is False
        assert result.latency_ms is None
        assert result.message == "连接失败，请检查 Base URL 或网络后重试"
        assert secret not in result.message
        assert "Authorization" not in result.message
        assert "internal.example" not in result.message

    def test_test_config_connectivity_identifies_non_openai_compatible_provider(self, monkeypatch):
        _RaisingChatOpenAI.error_message = (
            "404 Not Found for url: https://api.anthropic.com/v1/chat/completions"
        )
        _RaisingChatOpenAI.stream_chunks = []
        monkeypatch.setattr(provider_test_module, "ChatOpenAI", _RaisingChatOpenAI)

        result = provider_test_module.test_config_connectivity(
            {
                "api_key": "sk-secret-provider-789",
                "base_url": "https://api.anthropic.com/v1",
                "model": "claude-3-7-sonnet",
            }
        )

        assert result.success is False
        assert result.latency_ms is None
        assert result.message == "当前测试仅支持 OpenAI-compatible Chat Completions 接口"
        assert "anthropic.com" not in result.message

    def test_test_config_connectivity_identifies_model_or_parameter_errors(self, monkeypatch):
        _RaisingChatOpenAI.error_message = (
            "400 Bad Request: model `gpt-4.1-mini` does not exist for this account"
        )
        _RaisingChatOpenAI.stream_chunks = []
        monkeypatch.setattr(provider_test_module, "ChatOpenAI", _RaisingChatOpenAI)

        result = provider_test_module.test_config_connectivity(
            {
                "api_key": "sk-secret-model-321",
                "base_url": "https://api.openai.com/v1",
                "model": "gpt-4.1-mini",
            }
        )

        assert result.success is False
        assert result.latency_ms is None
        assert result.message == "模型或请求参数不兼容，请检查模型名和供应商兼容性"
        assert "gpt-4.1-mini" not in result.message
