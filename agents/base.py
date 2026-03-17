from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Optional


@dataclass
class AgentResult:
    """
    Output of an agent analysis step.

    - directives: short instructions to the main LLM about how to respond
    - tool_hints: suggested tools (names) + brief why
    - memory_ops: optional structured memory/graph actions to apply
    """

    agent: str
    directives: list[str] = field(default_factory=list)
    tool_hints: list[str] = field(default_factory=list)
    memory_ops: list[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.5


class BaseNovaAgent:
    name: str = "base"

    def match(self, text: str, ctx: Optional[Dict[str, Any]] = None) -> float:
        """Return confidence [0..1] this agent should handle the message."""
        return 0.0

    def run(self, text: str, ctx: Optional[Dict[str, Any]] = None) -> AgentResult:
        """Return analysis/directives. Must be fast and side-effect free."""
        return AgentResult(agent=self.name, confidence=0.0)

    async def start_passive(self, runtime: Any) -> None:
        """
        Optional: start passive background monitors.

        runtime provides:
        - session: LiveKit AgentSession (or None)
        - log: ActivityLogger
        - memory_graph: MemoryGraph
        - config: dict
        """

    def merge(self, results: Iterable[AgentResult]) -> AgentResult:
        """Optional: agent-specific merging; default is no-op."""
        return AgentResult(agent=self.name, confidence=0.0)

