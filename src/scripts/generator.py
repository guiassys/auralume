import logging
import os
import random
import re
import soundfile as sf
import numpy as np
import time
from datetime import datetime

from scripts.musicgen_pipeline import MusicPipeline
from src.scripts.musicgen_engine import MusicGenEngine


def sanitize_filename(name: str) -> str:
    name = re.sub(r"[^\w\- ]+", "", name or "")
    return name.strip().replace(" ", "_")


class LofiGenerator:

    def __init__(self, output_dir: str = "."):
        self.engine = MusicGenEngine(model_size="medium")
        self.pipeline = MusicPipeline()
        self.logger = logging.getLogger(__name__)
        self.output_dir = output_dir

    # -----------------------------
    # MAIN GENERATION (SINGLE PASS)
    # -----------------------------
    def generate(self, config: dict):
        prompt = config.get("prompt", "lofi music")
        duration = int(config.get("duration", 180))
        name = config.get("name")
        bpm_min = config.get("bpm_min", 60)
        bpm_max = config.get("bpm_max", 80)
        vibe = config.get("vibe", "calm")
        instruments = config.get("instruments", [])
        constraints = config.get("constraints", [])

        # 🎯 SINGLE COHERENT PROMPT
        final_prompt = self.pipeline.build(
            prompt=prompt,
            duration=duration,
            style=self._build_style(
                bpm_min,
                bpm_max,
                vibe,
                instruments,
                constraints
            )
        )

        self.logger.info("[LOFI GEN] Generating full track (single pass)")

        start_time = time.time()

        # 🔥 ONLY ONE GENERATION (CRITICAL FIX)
        wav, sr = self.engine.generate(final_prompt, duration)

        wav = self._to_numpy(wav)
        wav = self._to_mono_safe(wav)
        wav = self._normalize(wav)

        end_time = time.time()
        self._print_time_results(start_time, end_time)

        return self.save_audio(wav, sr, prompt, name)

    # -----------------------------
    # STYLE BUILDER
    # -----------------------------
    def _build_style(self, bpm_min, bpm_max, vibe, instruments, constraints):

        instruments_text = ", ".join(instruments) if instruments else "lo-fi instrumentation"
        constraints_text = ". ".join(constraints) if constraints else "smooth transitions, stable groove"

        return (
            f"{bpm_min}-{bpm_max} BPM,"
            f"{vibe}, "
            f"{instruments_text},"
            f"{constraints_text},"
        )

    # -----------------------------
    # UTILITIES
    # -----------------------------
    def _to_numpy(self, wav):
        if hasattr(wav, "detach"):
            wav = wav.detach().cpu().numpy()

        if isinstance(wav, list):
            wav = wav[0]

        return np.array(wav)

    def _to_mono_safe(self, x):
        x = np.array(x)

        if x.ndim == 2:
            x = x.mean(axis=1) if x.shape[0] > x.shape[1] else x.mean(axis=0)

        return x

    def _normalize(self, wav):
        wav = np.nan_to_num(wav)
        peak = np.max(np.abs(wav))
        if peak > 0:
            wav = wav / peak
        return wav.astype(np.float32)

    def _print_time_results(self, start, end):
        total = int(end - start)
        print(f"\n[LOFI GEN] Tempo total: {total//3600:02d}:{(total%3600)//60:02d}:{total%60:02d}")

    # -----------------------------
    # SAVE
    # -----------------------------
    def save_audio(self, wav, sample_rate, prompt, name=None):

        print("\n[LOFI GEN] Salvando áudio...")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_base = (
            sanitize_filename(name)
            if name
            else f"lofi_{abs(hash(prompt)) % 10000}_{timestamp}"
        )

        os.makedirs(self.output_dir, exist_ok=True)

        file_path = os.path.join(self.output_dir, f"{file_base}.wav")

        sf.write(file_path, wav, sample_rate, subtype="PCM_16")

        print(f"[FINAL] Arquivo gerado: {file_path}")

        return file_path