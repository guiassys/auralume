import logging
import random
from typing import Any

from langchain_core.runnables import RunnableLambda

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


class MusicPipeline:
    """Pipeline modular de composição musical usando LangChain Core.

    O pipeline divide a composição em etapas independentes:
    - melodia musical
    - base rítmica
    - faixa instrumental
    - mixagem

    Cada etapa é um RunnableLangChain que pode ser estendida ou paralelizada.
    """

    def __init__(self):
        self.pipeline = (
            {
                "melody": RunnableLambda(self._melody_stage),
                "rhythm": RunnableLambda(self._rhythm_stage),
            }
            | RunnableLambda(self._combine_stage)
            | RunnableLambda(self._instrument_stage)
            | RunnableLambda(self._mix_stage)
        )

    def build(self, prompt: str, duration: float, style: str = "lo-fi") -> str:
        prompt = prompt or style
        duration = float(duration)
        style = style or "lo-fi"

        logger.info("[PIPELINE] Iniciando pipeline de geração musical")

        pipeline_input = {
            "prompt": prompt,
            "duration": duration,
            "style": style,
        }

        result = self.pipeline.invoke(pipeline_input)

        logger.info("[PIPELINE] Prompt final gerado com sucesso")
        logger.debug("[PIPELINE] Resultado da etapa final: %s", result)

        return result["final_prompt"]

    def _melody_stage(self, inputs: dict[str, Any]) -> dict[str, Any]:
        prompt = inputs["prompt"]
        style = inputs["style"]

        melody = (
            f"Melodia base com frases suaves, arpejos leves e progressões acolhedoras. "
            f"A estrutura deve ser fluida e emocional, inspirada no estilo {style}."
        )

        return {
            "prompt": prompt,
            "duration": inputs["duration"],
            "style": style,
            "melody": melody,
        }

    def _rhythm_stage(self, inputs: dict[str, Any]) -> dict[str, Any]:
        duration = inputs["duration"]
        style = inputs["style"]

        bpm = self._choose_bpm(style)
        rhythm = (
            f"Ritmo definido por um groove moderado ({bpm} BPM), batidas quentes e balanço suave. "
            f"A base rítmica deve manter a música envolvente por {int(duration)} segundos."
        )

        return {
            "prompt": inputs["prompt"],
            "duration": duration,
            "style": style,
            "rhythm": rhythm,
        }

    def _combine_stage(self, inputs: dict[str, Any]) -> dict[str, Any]:
        melody_outputs = inputs["melody"]
        rhythm_outputs = inputs["rhythm"]

        return {
            "prompt": melody_outputs["prompt"],
            "duration": melody_outputs["duration"],
            "style": melody_outputs["style"],
            "melody": melody_outputs["melody"],
            "rhythm": rhythm_outputs["rhythm"],
        }

    def _instrument_stage(self, inputs: dict[str, Any]) -> dict[str, Any]:
        style = inputs["style"]
        melody = inputs["melody"]
        rhythm = inputs["rhythm"]

        instrumentation = self._describe_instruments(style, melody, rhythm)

        return {
            "prompt": inputs["prompt"],
            "duration": inputs["duration"],
            "style": style,
            "melody": melody,
            "rhythm": rhythm,
            "instrumentation": instrumentation,
        }

    def _mix_stage(self, inputs: dict[str, Any]) -> dict[str, Any]:
        prompt = inputs["prompt"]
        style = inputs["style"]
        duration = inputs["duration"]
        melody = inputs["melody"]
        rhythm = inputs["rhythm"]
        instrumentation = inputs["instrumentation"]

        final_prompt = (
            f"{prompt}. {style}. "
            f"Elementos principais: {melody} {rhythm} {instrumentation} "
            f"Finalize com uma mixagem limpa, ambiência suave e característica analógica. "
            f"Duração aproximada: {int(duration)} segundos."
        )

        return {
            "prompt": prompt,
            "duration": duration,
            "style": style,
            "melody": melody,
            "rhythm": rhythm,
            "instrumentation": instrumentation,
            "final_prompt": final_prompt,
        }

    def _choose_bpm(self, style: str) -> int:
        style = style.lower()
        if "hip hop" in style:
            return random.choice([70, 75, 80])
        if "rock" in style:
            return random.choice([90, 100, 110])
        if "jazz" in style:
            return random.choice([80, 90, 100])
        return random.choice([60, 70, 80])

    def _describe_instruments(self, style: str, melody: str, rhythm: str) -> str:
        style = style.lower()
        if "hip hop" in style:
            return (
                "Tons de baixo elétrico, piano suave, pads atmosféricos e percussões em "
                "pulseira com groove laidback."
            )
        if "rock" in style:
            return (
                "Guitarras limpas, baixos graves e bateria orgânica com sutis texturas de synth."
            )
        return (
            "Piano elétrico, baixos profundos e pads suaves com textura de fita vintage, "
            "misturados a percussões discretas e ambiente relaxante."
        )
