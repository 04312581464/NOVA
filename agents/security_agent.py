from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any, Iterable, Set

import psutil

from .base import AgentResult, BaseNovaAgent


def _home() -> Path:
    return Path(os.path.expanduser("~"))


SUSPICIOUS_EXTS = {
    ".exe",
    ".msi",
    ".bat",
    ".cmd",
    ".ps1",
    ".vbs",
    ".js",
    ".scr",
    ".jar",
    ".lnk",
}


class SecurityAgent(BaseNovaAgent):
    name = "security_agent"

    def match(self, text: str, ctx=None) -> float:
        t = (text or "").lower()
        keywords = ["security", "virus", "malware", "scan", "suspicious", "hack", "phishing", "usb"]
        return 0.75 if any(k in t for k in keywords) else 0.0

    def run(self, text: str, ctx=None) -> AgentResult:
        res = AgentResult(agent=self.name, confidence=self.match(text, ctx))
        if res.confidence <= 0:
            return res
        res.directives.append("Be cautious and security-first. Prefer alerting + asking before destructive actions. Use lockdown tools only when needed.")
        res.tool_hints.append("Use scan_system_for_viruses or lockdown_mode_on/off if the user requests security actions.")
        return res

    async def start_passive(self, runtime: Any) -> None:
        session = getattr(runtime, "session", None)
        log = getattr(runtime, "log", None)
        cfg = getattr(runtime, "config", {}) or {}

        interval_s = int(cfg.get("security_check_interval_s", 15))
        watch_dirs = [
            _home() / "Downloads",
            _home() / "Desktop",
        ]
        watch_dirs = [d for d in watch_dirs if d.exists()]

        # Track known files and known drives for "new" detection
        known_files: Set[str] = set()
        for d in watch_dirs:
            for p in d.glob("*"):
                if p.is_file():
                    known_files.add(str(p))

        known_drives = self._current_drive_set()

        while True:
            await asyncio.sleep(interval_s)

            # USB / new drive detection
            try:
                cur = self._current_drive_set()
                added = sorted(cur - known_drives)
                if added and session:
                    for drv in added:
                        if log:
                            log.log("security", "USB/drive detected", {"drive": drv})
                        await session.generate_reply(
                            instructions=f"Security Agent: new drive detected ({drv}). Scanning automatically now."
                        )
                        try:
                            from Tools.scan_system_for_viruses import scan_system_for_viruses

                            scan_result = await scan_system_for_viruses()
                            if log:
                                log.log("security", "Auto-scan completed", {"drive": drv})
                            await session.generate_reply(
                                instructions=f"Security Agent: auto-scan finished.\n\n{scan_result}"
                            )
                        except Exception as e:
                            if log:
                                log.log("security", "Auto-scan failed", {"error": str(e)})
                            await session.generate_reply(
                                instructions=f"Security Agent: auto-scan failed: {e}"
                            )
                known_drives = cur
            except Exception:
                pass

            # Suspicious file detection (polling)
            try:
                new_suspicious = list(self._find_new_suspicious_files(watch_dirs, known_files))
                if new_suspicious and session:
                    for fp in new_suspicious[:5]:
                        if log:
                            log.log("security", "Suspicious file detected", {"path": fp})
                        await session.generate_reply(
                            instructions=(
                                "Security Agent: suspicious file detected:\n"
                                f"- {fp}\n\n"
                                "Want me to scan your system or enable lockdown mode?"
                            )
                        )
                for fp in new_suspicious:
                    known_files.add(fp)
            except Exception:
                pass

    def _current_drive_set(self) -> Set[str]:
        drives: Set[str] = set()
        try:
            for p in psutil.disk_partitions(all=False):
                # Heuristic: removable drives often have 'removable' or are not system drive
                drives.add(p.device)
        except Exception:
            pass
        return drives

    def _find_new_suspicious_files(self, watch_dirs: Iterable[Path], known_files: Set[str]) -> Iterable[str]:
        for d in watch_dirs:
            for p in d.glob("*"):
                if not p.is_file():
                    continue
                sp = str(p)
                if sp in known_files:
                    continue
                if p.suffix.lower() in SUSPICIOUS_EXTS:
                    yield sp

