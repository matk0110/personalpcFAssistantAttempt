from __future__ import annotations
from typing import List

class LLMAdapter:
    def complete(self, messages: List[dict]) -> str:
        raise NotImplementedError

class MockLLMAdapter(LLMAdapter):
    def complete(self, messages: List[dict]) -> str:
        # echo last user message for determinism
        last_user = next((m for m in reversed(messages) if m.get("role") == "user"), None)
        if not last_user:
            return "Hello."
        content = last_user.get("content", "")
        return f"(mock echo) {content}"