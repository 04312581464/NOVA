from __future__ import annotations

from typing import Literal, Optional

from livekit.agents import function_tool

from dream_module import DreamModule, DreamRequest


# Set by agent.py at runtime
NOVA_CONTROLLER = None


def set_controller(controller) -> None:
    global NOVA_CONTROLLER
    NOVA_CONTROLLER = controller


@function_tool()
async def dream_generate_visual(
    user_input: str,
    mode: Optional[Literal["A", "B", "C", "D"]] = None,
    quality: str = "balanced",
    width: int = 1024,
    height: int = 1024,
) -> str:
    """
    NOVA Dream Module (MVP): generate a visual (image) from user input.

    Modes:
    - A: FutureSight (goal-based future visual)
    - B: Outcome Simulator (best vs worst consequences)
    - C: Concept Vision (academic/technical concept visualization)
    - D: WorldForge (simple exploratory what-if scene)
    """
    dream = DreamModule()
    if NOVA_CONTROLLER is not None:
        ctx = NOVA_CONTROLLER._dream_context_summary()
        profile = NOVA_CONTROLLER.behavior.profile.__dict__
    else:
        ctx = ""
        profile = {}

    m = mode or dream.classify(user_input)
    prompt = dream.build_prompt(DreamRequest(user_input=user_input, mode=m, context_summary=ctx), user_profile=profile)

    from Tools.generate_ai_image import generate_ai_image

    # Save into json/visuals for organization
    output_path = f"json/visuals/dream_{m}"
    return await generate_ai_image(prompt=prompt, output_path=output_path, quality=quality, width=width, height=height)

