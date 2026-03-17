from __future__ import annotations

from livekit.agents import function_tool


# This is set by agent.py at runtime
NOVA_CONTROLLER = None


def set_controller(controller) -> None:
    global NOVA_CONTROLLER
    NOVA_CONTROLLER = controller


@function_tool()
async def show_what_you_did_today() -> str:
    """
    Shows NOVA's transparency log for today (Stealth/Passive actions).
    """
    if NOVA_CONTROLLER is None:
        return "Transparency log is not available yet (controller not initialized)."
    return NOVA_CONTROLLER.show_what_i_did_today()

