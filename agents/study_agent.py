from __future__ import annotations

from .base import AgentResult, BaseNovaAgent


class StudyAgent(BaseNovaAgent):
    name = "study_agent"

    def match(self, text: str, ctx=None) -> float:
        t = (text or "").lower()
        keywords = ["study", "learn", "physics", "math", "exam", "notes", "revision", "topic", "weak"]
        return 0.7 if any(k in t for k in keywords) else 0.0

    def run(self, text: str, ctx=None) -> AgentResult:
        res = AgentResult(agent=self.name, confidence=self.match(text, ctx))
        if res.confidence <= 0:
            return res
        res.directives.append("Act like a study coach: break into concepts, diagnose weak areas, and propose a short plan + practice questions.")
        res.tool_hints.append("If notes/files are involved, suggest using universal_file_opener or process_document_query.")
        # Example memory-graph linking hints (applied by controller when requested)
        return res

