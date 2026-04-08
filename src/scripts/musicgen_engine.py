import logging as log
import torch
import math
import numpy as np
from transformers import MusicgenForConditionalGeneration, AutoProcessor


class MusicGenEngine:
    def __init__(self, model_size="medium"):
        self.model_name = f"facebook/musicgen-{model_size}"

        log.info(f'[MusicGenEngine] Loading model: {self.model_name}')

        log.info(f"torch version: {torch.__version__}")
        log.info(f"CUDA available: {torch.cuda.is_available()}")
        log.info(f"CUDA device count: {torch.cuda.device_count()}")

        if torch.cuda.is_available():
            self.device = torch.device('cuda')
            log.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            self.device = torch.device('cpu')
            log.error("CUDA NÃO está funcionando. Usando CPU.")

        self.processor = AutoProcessor.from_pretrained(self.model_name)

        self.model = MusicgenForConditionalGeneration.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device.type == "cuda" else torch.float32
        )

        self.model = self.model.to(self.device)
        self.model.eval()

        print(f"[MusicGenEngine] Device: {self.device}")

    def _crossfade(self, a, b, overlap):
        """Faz transição suave entre dois áudios"""
        fade_out = torch.linspace(1, 0, overlap)
        fade_in = torch.linspace(0, 1, overlap)

        return (a[-overlap:] * fade_out + b[:overlap] * fade_in)

    def generate(self, prompt, duration):
        print(f"\n[LOFI GEN] Prompt: {prompt}")

        # 🔧 CONFIGURAÇÃO
        sample_rate = 32000
        chunk_duration = 60
        overlap_sec = 5

        overlap = int(sample_rate * overlap_sec)

        num_chunks = math.ceil(duration / chunk_duration)
        total_audio = []

        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            for i in range(num_chunks):

                print(f"[LOFI GEN] Chunk {i+1}/{num_chunks}")

                current_duration = min(chunk_duration, duration - i * chunk_duration)

                max_tokens = int(current_duration * 50)

                chunk = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    do_sample=True,
                    top_k=250,
                    top_p=0.95,
                    temperature=1.0
                )

                chunk = chunk.squeeze(0).detach().cpu()

                # 🔗 PRIMEIRO CHUNK
                if i == 0:
                    total_audio.append(chunk)
                else:
                    prev = total_audio[-1]

                    # garante tamanho suficiente
                    if len(prev) > overlap and len(chunk) > overlap:

                        mixed = self._crossfade(prev, chunk, overlap)

                        merged = torch.cat([
                            prev[:-overlap],
                            mixed,
                            chunk[overlap:]
                        ])

                        total_audio[-1] = merged
                    else:
                        total_audio.append(chunk)

        # 🔥 junta tudo
        audio = torch.cat(total_audio, dim=0)

        return audio, sample_rate