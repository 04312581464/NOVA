from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from agents import CodingAgent, FileAgent, SecurityAgent, StudyAgent, SystemAgent
from focus_mode import focus_manager
from memory_graph import MemoryGraph
from nova_activity_log import ActivityLogger
from stealth_automation import StealthAutomation


@dataclass
class NovaRuntime:
    session: Any
    log: ActivityLogger
    memory_graph: MemoryGraph
    config: Dict[str, Any]


class NovaAgentsController:
    """
    Central multi-agent controller:
    - intent detection (rule-based)
    - agent selection
    - directive/response merging (into one injected developer/system message)
    - starts passive + stealth tasks when session is available
    """

    def __init__(self, *, base_dir: Path):
        self.base_dir = base_dir
        self.log = ActivityLogger(base_dir / "json" / "nova_activity_log.jsonl")
        self.memory_graph = MemoryGraph(base_dir / "json" / "memory_graph.json")
        self.config: Dict[str, Any] = {
            "system_check_interval_s": 20,
            "ram_spike_pct": 90,
            "battery_drain_warn_pct_per_min": 2.0,
            "security_check_interval_s": 15,
        }

        self.coding_agent = CodingAgent()
        self.study_agent = StudyAgent()
        self.system_agent = SystemAgent()
        self.security_agent = SecurityAgent()
        self.file_agent = FileAgent()

        self._agents = [
            self.security_agent,
            self.system_agent,
            self.file_agent,
            self.coding_agent,
            self.study_agent,
        ]

        self._runtime: Optional[NovaRuntime] = None
        self._passive_tasks: List[asyncio.Task] = []
        self._stealth: Optional[StealthAutomation] = None

    def attach_session(self, session: Any) -> None:
        runtime = NovaRuntime(session=session, log=self.log, memory_graph=self.memory_graph, config=self.config)
        self._runtime = runtime
        focus_manager.set_session(session)
        self.log.log("system", "NOVA session attached", {})

    async def start_background(self) -> None:
        """
        Start Passive Mode + Stealth Automation Mode.
        Called once after session attach.
        """
        if not self._runtime or not self._runtime.session:
            return

        # Focus mode doomscroll interrupts
        await focus_manager.start()

        # Stealth automation
        if self._stealth is None:
            self._stealth = StealthAutomation(self.file_agent, self.log, enabled=True)
        await self._stealth.start()

        # Passive monitors from agents
        if not self._passive_tasks:
            for a in (self.security_agent, self.system_agent):
                self._passive_tasks.append(asyncio.create_task(a.start_passive(self._runtime)))

    def show_what_i_did_today(self) -> str:
        events = self.log.get_today()
        if not events:
            return "No actions logged today."
        lines = ["Here’s what I did today (transparency log):"]
        for e in events[-30:]:
            lines.append(f"- [{e.kind}] {e.message}")
        return "\n".join(lines)

    def detect_intents(self, text: str) -> List[str]:
        t = (text or "").lower()
        intents: List[str] = []
        if any(k in t for k in ["show what you did", "what did you do today", "today log", "transparency log"]):
            intents.append("show_log")
        if any(k in t for k in ["focus mode", "doomscroll", "scrolling too much"]):
            intents.append("focus_mode")
        if any(k in t for k in ["memory graph", "relationships", "link this", "connect this"]):
            intents.append("memory_graph")
        if any(k in t for k in ["organize", "downloads", "cleanup", "clear junk", "rename"]):
            intents.append("file_ops")
        if any(k in t for k in ["usb", "virus", "scan", "suspicious", "security", "malware"]):
            intents.append("security")
        if any(k in t for k in ["ram", "cpu", "battery", "slow", "performance"]):
            intents.append("system")
        if any(k in t for k in ["study", "learn", "physics", "math", "exam", "revision", "topic"]):
            intents.append("study")
        if any(k in t for k in ["code", "bug", "error", "traceback", "refactor", "python"]):
            intents.append("coding")
        return intents

    def select_agents(self, text: str) -> List[Any]:
        scored = [(a.match(text, None), a) for a in self._agents]
        scored.sort(key=lambda x: x[0], reverse=True)
        selected = [a for s, a in scored if s > 0]
        return selected[:3]  # keep it small and fast

    def merged_directives(self, text: str) -> str:
        intents = self.detect_intents(text)
        selected = self.select_agents(text)
        results = [a.run(text, None) for a in selected]

        lines: List[str] = []
        lines.append("Multi-Agent Controller:")
        if intents:
            lines.append(f"- Detected intents: {', '.join(intents)}")
        if selected:
            lines.append(f"- Selected agents: {', '.join(a.name for a in selected)}")

        for r in results:
            if r.directives:
                lines.append(f"\n[{r.agent}] directives:")
                for d in r.directives:
                    lines.append(f"- {d}")
            if r.tool_hints:
                lines.append(f"[{r.agent}] tool hints:")
                for h in r.tool_hints:
                    lines.append(f"- {h}")

        # Built-in behaviors
        if "show_log" in intents:
            lines.append("\nController action: respond with today's transparency log.")

        return "\n".join(lines)

