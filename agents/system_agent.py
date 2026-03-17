from __future__ import annotations

import asyncio
import psutil
from typing import Any

from .base import AgentResult, BaseNovaAgent


class SystemAgent(BaseNovaAgent):
    name = "system_agent"

    def match(self, text: str, ctx=None) -> float:
        t = (text or "").lower()
        keywords = ["ram", "cpu", "battery", "slow", "performance", "storage", "disk", "heat"]
        return 0.65 if any(k in t for k in keywords) else 0.0

    def run(self, text: str, ctx=None) -> AgentResult:
        res = AgentResult(agent=self.name, confidence=self.match(text, ctx))
        if res.confidence <= 0:
            return res
        res.directives.append("Be proactive about system health: suggest low-risk steps first and use system tools when asked.")
        res.tool_hints.append("Use get_system_info_deep for diagnostics; consider system_power_action for power tweaks only on request.")
        return res

    async def start_passive(self, runtime: Any) -> None:
        # Passive monitoring: RAM spikes + battery drain.
        session = getattr(runtime, "session", None)
        log = getattr(runtime, "log", None)
        cfg = getattr(runtime, "config", {}) or {}

        interval_s = int(cfg.get("system_check_interval_s", 20))
        ram_spike_pct = float(cfg.get("ram_spike_pct", 90))
        battery_drain_warn_pct_per_min = float(cfg.get("battery_drain_warn_pct_per_min", 2.0))

        last_batt = None
        last_batt_ts = None

        while True:
            await asyncio.sleep(interval_s)

            try:
                vm = psutil.virtual_memory()
                if vm.percent >= ram_spike_pct and session:
                    if log:
                        log.log("system", "RAM spike detected", {"ram_percent": vm.percent})
                    await session.generate_reply(
                        instructions=(
                            f"System Agent: RAM usage is {vm.percent:.0f}%. "
                            "Want me to identify heavy apps and suggest quick fixes?"
                        )
                    )
            except Exception:
                pass

            try:
                batt = psutil.sensors_battery()
                if not batt or batt.percent is None:
                    continue
                now = psutil.time.time() if hasattr(psutil, "time") else None
                # Fallback: use asyncio loop time
                if now is None:
                    now = asyncio.get_running_loop().time()

                if last_batt is not None and last_batt_ts is not None and not batt.power_plugged:
                    dt_min = max(0.001, (now - last_batt_ts) / 60.0)
                    drain = (last_batt - batt.percent) / dt_min
                    if drain >= battery_drain_warn_pct_per_min and session:
                        if log:
                            log.log(
                                "system",
                                "Battery drain detected",
                                {"drain_pct_per_min": drain, "battery_percent": batt.percent},
                            )
                        await session.generate_reply(
                            instructions=(
                                f"System Agent: battery is draining fast (~{drain:.1f}%/min). "
                                "I can suggest actions (brightness, background apps, power mode)."
                            )
                        )

                last_batt = batt.percent
                last_batt_ts = now
            except Exception:
                pass

