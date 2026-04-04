from src.musicgen_engine import MusicGenEngine
from src.prompts import LOFI_PROMPTS
import random
import re
import soundfile as sf
import numpy as np
import time
from datetime import datetime


def sanitize_filename(name: str) -> str:
    name = re.sub(r"[^\w\- ]+", "", name)
    return name.strip().replace(" ", "_")


class LofiGenerator:
    def __init__(self):
        self.engine = MusicGenEngine(model_size="medium")

    def generate(self, prompt=None, duration=None, name=None):
        if duration is None:
            try:
                duration = int(input("Digite a duração da música em segundos (padrão 180): ") or 180)
            except ValueError:
                duration = 180
                print("Valor inválido, usando 180 segundos.")

        if prompt is None:
            prompt = random.choice(LOFI_PROMPTS)

        start_time = time.time()
        wav, sr = self.engine.generate(prompt, duration)
        end_time = time.time()

        print(f"\n[LOFI GEN] Tempo total de geração: {end_time - start_time:.2f} segundos")

        return self.save_audio(wav, sr, prompt, name)

    def save_audio(self, wav, sample_rate, prompt, name=None):
        print("\n[LOFI GEN] Salvando áudio...")

        # corrige formato do tensor
        if isinstance(wav, list):
            wav = wav[0]

        wav = np.array(wav).squeeze()

        if wav.ndim > 1:
            wav = wav.reshape(-1)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if name:
            file_base = sanitize_filename(name)
            if not file_base:
                file_base = f"lofi_{timestamp}"
        else:
            file_base = f"lofi_{abs(hash(prompt)) % 10000}_{timestamp}"

        path = f"{file_base}.wav"

        sf.write(path, wav, sample_rate)

        print(f"[FINAL] Arquivo gerado: {path}")

        return path