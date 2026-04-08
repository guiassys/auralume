import logging
from typing import Any
from langchain_core.runnables import RunnableLambda

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MusicPipeline:

    def __init__(self):
        self.pipeline = RunnableLambda(self._final_stage)

    def build(self, prompt: str, duration: float, style: str = "lo-fi") -> str:

        logger.info("[PIPELINE] Building stable prompt")

        return self.pipeline.invoke({
            "prompt": prompt,
            "duration": duration,
            "style": style
        })["final_prompt"]

    # -----------------------------
    # SINGLE STAGE (FIXED DESIGN)
    # -----------------------------
    def _final_stage(self, inputs: dict[str, Any]) -> dict[str, Any]:

        prompt = inputs["prompt"]
        duration = int(inputs["duration"])
        style = inputs["style"]

        final_prompt = (
            f"{prompt}. "
            f"Style: {style}. "
            f"Duration: {duration} seconds."
)

        return {
            "final_prompt": final_prompt
        }