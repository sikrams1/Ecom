"""Universal AI assistant starter framework.

This module demonstrates a simple architecture you can expand into a
production-grade assistant.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class Intent(str, Enum):
    SUPPORT = "support"
    PLANNING = "planning"
    DRAFTING = "drafting"
    TROUBLESHOOTING = "troubleshooting"
    GENERAL = "general"


@dataclass
class Request:
    user_id: str
    text: str


@dataclass
class Response:
    intent: Intent
    confidence: float
    content: str
    escalated: bool = False


class SafetyPolicy:
    """Lightweight policy checks.

    Replace with a robust moderation and policy layer in production.
    """

    blocked_terms = {"exploit", "self-harm instructions", "steal credentials"}

    def is_blocked(self, text: str) -> bool:
        lowered = text.lower()
        return any(term in lowered for term in self.blocked_terms)


class IntentRouter:
    """Heuristic intent router.

    Replace with model-based classification and confidence calibration.
    """

    def route(self, text: str) -> tuple[Intent, float]:
        lowered = text.lower()
        if any(k in lowered for k in ["error", "broken", "not working", "bug"]):
            return Intent.TROUBLESHOOTING, 0.82
        if any(k in lowered for k in ["plan", "roadmap", "strategy"]):
            return Intent.PLANNING, 0.80
        if any(k in lowered for k in ["write", "draft", "email", "message"]):
            return Intent.DRAFTING, 0.78
        if any(k in lowered for k in ["refund", "order", "account", "support"]):
            return Intent.SUPPORT, 0.79
        return Intent.GENERAL, 0.60


class ToolRegistry:
    """Stub tool layer.

    Register real integrations (CRM, docs, code execution, search APIs, etc.).
    """

    def available_tools(self, intent: Intent) -> List[str]:
        mapping = {
            Intent.SUPPORT: ["knowledge_base_search", "ticketing"],
            Intent.PLANNING: ["task_planner", "calendar"],
            Intent.DRAFTING: ["document_writer", "style_reviewer"],
            Intent.TROUBLESHOOTING: ["log_search", "runbook_lookup"],
            Intent.GENERAL: ["web_search"],
        }
        return mapping[intent]


class Assistant:
    def __init__(self) -> None:
        self.policy = SafetyPolicy()
        self.router = IntentRouter()
        self.tools = ToolRegistry()

    def handle(self, request: Request) -> Response:
        if self.policy.is_blocked(request.text):
            return Response(
                intent=Intent.GENERAL,
                confidence=1.0,
                content="I can't help with that request, but I can offer a safe alternative.",
                escalated=True,
            )

        intent, confidence = self.router.route(request.text)

        if confidence < 0.70:
            return Response(
                intent=intent,
                confidence=confidence,
                content=(
                    "I want to make sure I get this right. Could you share a bit more detail "
                    "about your goal and constraints?"
                ),
                escalated=False,
            )

        tool_list = ", ".join(self.tools.available_tools(intent))
        return Response(
            intent=intent,
            confidence=confidence,
            content=(
                f"Understood. I classified this as '{intent.value}'. "
                f"Next, I would use: {tool_list}."
            ),
            escalated=False,
        )
