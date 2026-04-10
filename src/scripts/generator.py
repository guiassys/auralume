import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

import numpy as np
import soundfile as sf

from scripts.musicgen_pipeline import MusicPipeline
from src.scripts.musicgen_engine import MusicGenEngine


class AudioProcessor:
    def merge_sections(self, sections: List[np.ndarray]) -> np.ndarray:
        merged = sections[0]

        for nxt in sections[1:]:
            overlap = 20000

            fade_out = np.linspace(1, 0, overlap)
            fade_in = np.linspace(0, 1, overlap)

            cross = merged[-overlap:] * fade_out + nxt[:overlap] * fade_in

            merged = np.concatenate([
                merged[:-overlap],
                cross,
                nxt[overlap:]
            ])

        return merged

    def normalize(self, audio: np.ndarray) -> np.ndarray:
        peak = np.max(np.abs(audio))
        return audio / peak if peak > 0 else audio


class AudioSaver:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def save(self, audio: np.ndarray, sr: int, name: Optional[str]) -> str:
        os.makedirs(self.output_dir, exist_ok=True)

        filename = name or datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.output_dir, f"{filename}.wav")

        sf.write(path, audio, sr)

        return path


class LofiGenerator:
    def __init__(
        self,
        output_dir: str = "outputs",
        engine: Optional[MusicGenEngine] = None,
        pipeline: Optional[MusicPipeline] = None,
        processor: Optional[AudioProcessor] = None,
        saver: Optional[AudioSaver] = None,
    ):
        if saver and output_dir:
            # Optional safeguard (can remove if you prefer flexibility)
            pass

        self.engine = engine or MusicGenEngine()
        self.pipeline = pipeline or MusicPipeline()
        self.processor = processor or AudioProcessor()
        self.saver = saver or AudioSaver(output_dir=output_dir)

        self.logger = logging.getLogger(__name__)

    def generate(self, config: Dict[str, Any]) -> str:
        prompt = config.get("prompt", "lofi music")
        duration = int(config.get("duration", 180))
        name = config.get("name")
        style = config.get("style", "lofi chill")

        self.logger.info("[GENERATOR] Running pipeline")

        plan = self.pipeline.build(prompt, duration, style)

        sections_audio, sample_rate = self._generate_sections(plan)

        final_audio = self.processor.merge_sections(sections_audio)
        final_audio = self.processor.normalize(final_audio)

        path = self.saver.save(final_audio, sample_rate, name)

        self.logger.info(f"[GENERATOR] Saved: {path}")

        return path

    def generate_section(self, prompt: str, duration: int):
        return self.engine.generate_section(prompt, duration)

    def _generate_sections(self, plan: Dict[str, Any]) -> Tuple[List[np.ndarray], int]:
        full_audio = []
        sample_rate = None

        for section in plan["sections"]:
            self.logger.info(f"[GENERATOR] Section: {section['name']}")

            audio, sr = self.generate_section(
                section["prompt"],
                section["duration"]
            )

            sample_rate = sr
            full_audio.append(audio.numpy())

        return full_audio, sample_rate