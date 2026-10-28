"""Backward-compatible names for the original Alibaba adapter."""
from .openai_compatible import Credentials, ModelAPIError, OpenAICompatibleModelClient, tool_definitions


class BailianModelClient(OpenAICompatibleModelClient):
    def __init__(self, credentials, model="qwen3.8-flash", timeout=30, transport=None):
        super().__init__(credentials, model, timeout, transport, extra_body={"enable_thinking": False}, provider="aliyun_bailian")
