import logging
import os
import numpy as np
import soundfile as sf
from datetime import datetime
from typing import Dict, Any, Optional

from scripts.musicgen_pipeline import MusicPipeline
from src.scripts.musicgen_engine import MusicGenEngine


class LofiGenerator:

    def __init__(self, output_dir="outputs"):
        self.engine = MusicGenEngine()
        self.pipeline = MusicPipeline()
        self.output_dir = output_dir

        self.logger = logging.getLogger(__name__)

    def generate(self, config: Dict[str, Any]) -> str:

        prompt = config.get("prompt", "lofi music")
        duration = int(config.get("duration", 180))
        name = config.get("name")

        style = config.get("style", "lofi chill")

        self.logger.info("[GENERATOR] Running pipeline")

        plan = self.pipeline.build(prompt, duration, style)

        full_audio = []
        sample_rate = None

        for section in plan["sections"]:
            self.logger.info(f"[GENERATOR] Section: {section['name']}")

            audio, sr = self.engine.generate_section(
                section["prompt"],
                section["duration"]
            )

            sample_rate = sr

            audio_np = audio.numpy()

            full_audio.append(audio_np)

        final_audio = self._merge_sections(full_audio)

        final_audio = self._normalize(final_audio)

        return self._save(final_audio, sample_rate, name)

    # -----------------------------
    # AUDIO ENGINEERING
    # -----------------------------
    def _merge_sections(self, sections):

        self.logger.info("[POST] Merging sections with transitions")

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

    def _normalize(self, audio):

        peak = np.max(np.abs(audio))
        return audio / peak if peak > 0 else audio

    def _save(self, audio, sr, name: Optional[str]):

        os.makedirs(self.output_dir, exist_ok=True)

        filename = name or datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.output_dir, f"{filename}.wav")

        sf.write(path, audio, sr)

        self.logger.info(f"[GENERATOR] Saved: {path}")

        return path