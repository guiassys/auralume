from src.musicgen_engine import MusicGenEngine
from src.prompts import LOFI_PROMPTS
import random
import soundfile as sf
import numpy as np
import time


class LofiGenerator:
    def __init__(self):
        self.engine = MusicGenEngine(model_size="medium")

    def generate(self, prompt=None, duration=None):
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

        return self.save_audio(wav, sr, prompt)

    def save_audio(self, wav, sample_rate, prompt):
        print("\n[LOFI GEN] Salvando áudio...")

        # corrige formato do tensor
        if isinstance(wav, list):
            wav = wav[0]

        wav = np.array(wav).squeeze()

        if wav.ndim > 1:
            wav = wav.reshape(-1)

        path = f"output_lofi_{abs(hash(prompt)) % 10000}.wav"

        sf.write(path, wav, sample_rate)

        print(f"[FINAL] Arquivo gerado: {path}")

        return path