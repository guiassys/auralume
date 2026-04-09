import logging as log
import torch
import math
import numpy as np
from transformers import MusicgenForConditionalGeneration, AutoProcessor

class MusicGenEngine:
    def __init__(self, model_size="medium"):
        self.model_name = f"facebook/musicgen-{model_size}"

        log.info(f'[MusicGenEngine] Loading model: {self.model_name}')

        if torch.cuda.is_available():
            self.device = torch.device('cuda')
            log.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            self.device = torch.device('cpu')
            log.error("CUDA is not working. Using CPU. Performance will be very slow.")

        self.processor = AutoProcessor.from_pretrained(self.model_name)
        self.model = MusicgenForConditionalGeneration.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device.type == "cuda" else torch.float32
        )

        self.model = self.model.to(self.device)
        self.model.eval()

    def _crossfade(self, a, b, overlap):
        """Faz transição suave entre dois áudios"""
        fade_out = torch.linspace(1, 0, overlap)
        fade_in = torch.linspace(0, 1, overlap)
        # Garante que os fades estejam no mesmo dispositivo que os chunks
        return (a[-overlap:] * fade_out + b[:overlap] * fade_in)

    def generate(self, prompt, duration):
        print(f"\n[AURALITH GEN] Prompt: {prompt}")

        # 🔧 CONFIGURAÇÃO SEGURA
        sample_rate = 32000
        chunk_duration = 30  # LIMITE DO MODELO (1500 tokens)
        overlap_sec = 10
        overlap = int(sample_rate * overlap_sec)

        # Cálculo de chunks considerando que cada novo chunk sobrepõe o anterior
        effective_chunk_time = chunk_duration - overlap_sec
        num_chunks = math.ceil(duration / effective_chunk_time)
        
        total_audio = []

        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            for i in range(num_chunks):
                print(f"[AURALITH GEN] Chunk {i+1}/{num_chunks}")

                # 1500 tokens é o limite para MusicGen
                max_tokens = 1500 

                chunk = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    do_sample=True,
                    top_k=250,
                    top_p=0.95,
                    temperature=1.0
                )

                # Limpeza de dimensões: de [1, 1, samples] para [samples]
                chunk = chunk.detach().cpu().squeeze()

                if i == 0:
                    total_audio.append(chunk)
                else:
                    prev = total_audio[-1]
                    
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

        # Concatena e corta para a duração exata pedida
        audio = torch.cat(total_audio, dim=0)
        target_length = int(duration * sample_rate)
        audio = audio[:target_length]

        return audio, sample_rate