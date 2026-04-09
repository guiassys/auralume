import logging
import os
import re
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import soundfile as sf
import torch

# Importes existentes (mantidos)
from scripts.musicgen_pipeline import MusicPipeline
from src.scripts.musicgen_engine import MusicGenEngine


def sanitize_filename(name: Optional[str]) -> str:
    """Remove caracteres inválidos e normaliza nome de arquivo."""
    name = re.sub(r"[^\w\- ]+", "", name or "")
    return name.strip().replace(" ", "_")


class LofiGenerator:
    def __init__(
        self,
        output_dir: str = ".",
        engine: Optional[MusicGenEngine] = None
    ):
        self.engine = engine or MusicGenEngine(model_size="medium")
        self.pipeline = MusicPipeline()
        self.output_dir = output_dir

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def generate(self, config: Dict[str, Any]) -> str:
        """Gera música com base na configuração."""
        prompt = config.get("prompt", "lofi music")
        duration = self._safe_int(config.get("duration", 180), default=180)
        name = config.get("name")

        style = self._build_style(
            bpm_min=config.get("bpm_min", 60),
            bpm_max=config.get("bpm_max", 80),
            vibe=config.get("vibe", "calm"),
            instruments=config.get("instruments", []),
            constraints=config.get("constraints", [])
        )

        final_prompt = self.pipeline.build(
            prompt=prompt,
            duration=duration,
            style=style
        )

        self.logger.info("[AURALITH GEN] Starting generation...")
        start_time = time.time()

        wav, sr = self.engine.generate(final_prompt, duration)

        wav = self._to_numpy(wav)
        wav = self._normalize(wav)

        self._log_time(start_time, time.time())

        return self.save_audio(wav, sr, prompt, name)

    # --------------------------
    # Helpers internos
    # --------------------------

    def _build_style(
        self,
        bpm_min: int,
        bpm_max: int,
        vibe: str,
        instruments: List[str],
        constraints: List[str]
    ) -> str:
        instruments_text = ", ".join(instruments) if instruments else "lo-fi instrumentation"
        constraints_text = ". ".join(constraints) if constraints else "smooth transitions"

        return f"{bpm_min}-{bpm_max} Beats Per Minute (BPM), {vibe}, {instruments_text}, {constraints_text}"

    def _to_numpy(self, wav: Any) -> np.ndarray:
        if torch.is_tensor(wav):
            wav = wav.detach().cpu().numpy()

        return np.asarray(wav, dtype=np.float32)

    def _normalize(self, wav: np.ndarray) -> np.ndarray:
        if wav.size == 0:
            self.logger.warning("[AURALITH GEN] Empty audio received.")
            return wav

        wav = np.nan_to_num(wav)

        peak = np.max(np.abs(wav))
        if peak > 0:
            wav = wav / peak

        return wav

    def _safe_int(self, value: Any, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            self.logger.warning(f"[AURALITH GEN] Invalid value for integer: {value}, using {default}")
            return default

    def _log_time(self, start: float, end: float) -> None:
        total = int(end - start)
        self.logger.info(f"[AURALITH GEN] Total time: {total // 60:02d}:{total % 60:02d}")

    # --------------------------
    # Persistência
    # --------------------------

    def save_audio(
        self,
        wav: np.ndarray,
        sample_rate: int,
        prompt: str,
        name: Optional[str] = None
    ) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_base = sanitize_filename(name) if name else f"lofi_{timestamp}"

        os.makedirs(self.output_dir, exist_ok=True)
        file_path = os.path.join(self.output_dir, f"{file_base}.wav")

        sf.write(file_path, wav, sample_rate, subtype="PCM_16")

        self.logger.info(f"[AURALITH GEN] File saved in: {file_path}")

        return file_path