import logging
import os
import re
import torch
import soundfile as sf
import numpy as np
import time
from datetime import datetime

# Importes corrigidos de acordo com sua estrutura
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

    def generate(self, config: dict):
        prompt = config.get("prompt", "lofi music")
        duration = int(config.get("duration", 180))
        name = config.get("name")
        
        final_prompt = self.pipeline.build(
            prompt=prompt,
            duration=duration,
            style=self._build_style(
                config.get("bpm_min", 60),
                config.get("bpm_max", 80),
                config.get("vibe", "calm"),
                config.get("instruments", []),
                config.get("constraints", [])
            )
        )

        self.logger.info("[LOFI GEN] Iniciando geração...")
        start_time = time.time()

        # Chama o Engine corrigido
        wav, sr = self.engine.generate(final_prompt, duration)

        # Processamento Final
        wav = self._to_numpy(wav)
        wav = self._normalize(wav)

        self._print_time_results(start_time, time.time())
        return self.save_audio(wav, sr, prompt, name)

    def _build_style(self, bpm_min, bpm_max, vibe, instruments, constraints):
        instruments_text = ", ".join(instruments) if instruments else "lo-fi instrumentation"
        constraints_text = ". ".join(constraints) if constraints else "smooth transitions"
        return f"{bpm_min}-{bpm_max} BPM, {vibe}, {instruments_text}, {constraints_text}"

    def _to_numpy(self, wav):
        if torch.is_tensor(wav):
            wav = wav.detach().cpu().numpy()
        return np.array(wav).astype(np.float32)

    def _normalize(self, wav):
        wav = np.nan_to_num(wav)
        peak = np.max(np.abs(wav))
        if peak > 0:
            wav = wav / peak
        return wav

    def _print_time_results(self, start, end):
        total = int(end - start)
        print(f"[LOFI GEN] Tempo total: {total//60:02d}:{total%60:02d}")

    def save_audio(self, wav, sample_rate, prompt, name=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_base = sanitize_filename(name) if name else f"lofi_{timestamp}"
        
        os.makedirs(self.output_dir, exist_ok=True)
        file_path = os.path.join(self.output_dir, f"{file_base}.wav")
        
        sf.write(file_path, wav, sample_rate, subtype="PCM_16")
        return file_path