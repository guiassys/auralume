import logging
import os
import random
import re
import soundfile as sf
import numpy as np
import time
from datetime import datetime

from src.scripts.music_pipeline import MusicPipeline
from src.scripts.musicgen_engine import MusicGenEngine
from src.scripts.prompts import LOFI_PROMPTS


def sanitize_filename(name: str) -> str:
    name = re.sub(r"[^\w\- ]+", "", name)
    return name.strip().replace(" ", "_")


class LofiGenerator:
    def __init__(self, output_dir: str = "."):
        self.engine = MusicGenEngine(model_size="medium")
        self.pipeline = MusicPipeline()
        self.logger = logging.getLogger(__name__)
        self.output_dir = output_dir

    def generate(self, prompt=None, duration=None, name=None):
        if duration is None:
            try:
                duration = int(input("Digite a duração da música em segundos (padrão 180): ") or 180)
            except ValueError:
                duration = 180
                print("Valor inválido, usando 180 segundos.")

        if prompt is None:
            prompt = random.choice(LOFI_PROMPTS)

        final_prompt = self.pipeline.build(prompt=prompt, duration=duration, style=prompt)
        self.logger.info("[LOFI GEN] Prompt de geração final: %s", final_prompt)

        start_time = time.time()
        wav, sr = self.engine.generate(final_prompt, duration)
        end_time = time.time()

        print(f"\n[LOFI GEN] Tempo total de geração: {end_time - start_time:.2f} segundos")

        return self.save_audio(wav, sr, final_prompt, name, self.output_dir)

    def save_audio(self, wav, sample_rate, prompt, name=None, output_dir: str = "."):
        print("\n[LOFI GEN] Salvando áudio...")

        # 🔹 Caso venha como lista
        if isinstance(wav, list):
            wav = wav[0]

        # 🔥 CORREÇÃO PRINCIPAL (CUDA → CPU → NumPy)
        if hasattr(wav, "detach"):
            wav = wav.detach().cpu().numpy()

        # Garante formato correto
        if wav.dtype == np.float16:
            wav = wav.astype(np.float32)

        if wav.ndim > 1:
            wav = wav.reshape(-1)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if name:
            file_base = sanitize_filename(name)
            if not file_base:
                file_base = f"lofi_{timestamp}"
        else:
            file_base = f"lofi_{abs(hash(prompt)) % 10000}_{timestamp}"

        # Garante que o diretório existe
        os.makedirs(output_dir, exist_ok=True)

        # Caminho final
        file_path = os.path.join(output_dir, f"{file_base}.wav")

        # Salva o áudio
        sf.write(file_path, wav, sample_rate)

        print(f"[FINAL] Arquivo gerado: {file_path}")

        return file_path