import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

import numpy as np
import soundfile as sf

from scripts.musicgen_pipeline import MusicPipeline
from src.scripts.musicgen_engine import MusicGenEngine
from src.web.log_stream import LogStream


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
            pass

        self.engine = engine or MusicGenEngine()
        self.pipeline = pipeline or MusicPipeline()
        self.processor = processor or AudioProcessor()
        self.saver = saver or AudioSaver(output_dir=output_dir)

        self.logger = logging.getLogger(__name__)

    def generate(self, config: Dict[str, Any], log_stream: Optional[LogStream] = None) -> str:
        prompt = config.get("prompt", "lofi music")
        duration = int(config.get("duration", 180))
        name = config.get("name")
        style = config.get("style", "lofi chill")

        def _log(message: str):
            self.logger.info(f"[GENERATOR] {message}")
            if log_stream:
                log_stream.log(message)

        _log("Running music generation pipeline...")

        plan = self.pipeline.build(prompt, duration, style)
        _log(f"Pipeline built. Plan includes {len(plan['sections'])} sections.")

        sections_audio, sample_rate = self._generate_sections(plan, log_stream)
        _log("All audio sections generated successfully.")

        _log("Merging sections with crossfade...")
        final_audio = self.processor.merge_sections(sections_audio)
        _log("Audio sections merged.")

        _log("Normalizing final audio...")
        final_audio = self.processor.normalize(final_audio)
        _log("Audio normalized.")

        _log("Saving final audio file...")
        path = self.saver.save(final_audio, sample_rate, name)
        _log(f"Audio saved successfully to: {os.path.basename(path)}")

        return path

    def generate_section(self, prompt: str, duration: int):
        return self.engine.generate_section(prompt, duration)

    def _generate_sections(self, plan: Dict[str, Any], log_stream: Optional[LogStream] = None) -> Tuple[List[np.ndarray], int]:
        full_audio = []
        sample_rate = None
        total_sections = len(plan["sections"])

        def _log(message: str):
            self.logger.info(f"[GENERATOR] {message}")
            if log_stream:
                log_stream.log(message)

        for i, section in enumerate(plan["sections"]):
            _log(f"Generating chunk {i + 1}/{total_sections}: {section['name']} ({section['duration']}s)")

            audio, sr = self.generate_section(
                section["prompt"],
                section["duration"]
            )

            sample_rate = sr
            full_audio.append(audio.numpy())
            _log(f"Chunk {i + 1}/{total_sections} finished.")

        return full_audio, sample_rate