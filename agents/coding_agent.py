from __future__ import annotations

from .base import AgentResult, BaseNovaAgent


class CodingAgent(BaseNovaAgent):
    name = "coding_agent"

    def match(self, text: str, ctx=None) -> float:
        t = (text or "").lower()
        keywords = ["code", "bug", "error", "traceback", "python", "javascript", "typescript", "fix", "refactor"]
        return 0.75 if any(k in t for k in keywords) else 0.0

    def run(self, text: str, ctx=None) -> AgentResult:
        res = AgentResult(agent=self.name, confidence=self.match(text, ctx))
        if res.confidence <= 0:
            return res
        res.directives.append("Act like a focused coding assistant: ask for the file/path and error details if missing, propose minimal safe changes, and use existing tools when appropriate.")
        res.tool_hints.append("Consider using code tools (generate_and_type_code, fix_code_error, run_file_in_vscode) if the user asks to write/run code.")
        return res

