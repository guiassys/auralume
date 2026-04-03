from src.ai_music.musicgen_engine import MusicGenEngine
from src.ai_music.prompts import LOFI_PROMPTS
import random
import soundfile as sf
import numpy as np


class LofiGenerator:
    def __init__(self):
        self.engine = MusicGenEngine(model_size="medium")

    def generate(self, prompt=None, duration=30):
        if prompt is None:
            prompt = random.choice(LOFI_PROMPTS)

        wav, sr = self.engine.generate(prompt, duration)

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