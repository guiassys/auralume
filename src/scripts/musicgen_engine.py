import logging as log
import torch
import math
from typing import Optional
from transformers import MusicgenForConditionalGeneration, AutoProcessor


class MusicGenEngine:
    _instance = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MusicGenEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self, model_size="medium"):
        if hasattr(self, "_initialized"):
            return

        self.model_name = f"facebook/musicgen-{model_size}"
        log.info(f"[MusicGenEngine] Loading model: {self.model_name}")

        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            log.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            self.device = torch.device("cpu")
            log.error("CUDA not available. Using CPU.")

        self.processor = AutoProcessor.from_pretrained(self.model_name)
        self.model = MusicgenForConditionalGeneration.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device.type == "cuda" else torch.float32
        ).to(self.device)

        self.model.eval()
        self._initialized = True

    def generate_section(self, prompt: str, duration: int):
        """Generate a single structured section"""
        log.info(f"[ENGINE] Generating section: {prompt[:60]}...")

        sample_rate = 32000
        chunk_duration = 30
        overlap_sec = 5
        overlap = int(sample_rate * overlap_sec)

        effective_chunk = chunk_duration - overlap_sec
        num_chunks = math.ceil(duration / effective_chunk)

        inputs = self.processor(
            text=[prompt],
            return_tensors="pt",
            padding=True
        ).to(self.device)

        chunks = []

        with torch.no_grad():
            for i in range(num_chunks):
                log.info(f"[ENGINE] Chunk {i+1}/{num_chunks}")

                audio = self.model.generate(
                    **inputs,
                    max_new_tokens=1500,
                    do_sample=True,
                    top_k=250,
                    top_p=0.95,
                    temperature=1.0
                )

                audio = audio.squeeze().cpu()

                if not chunks:
                    chunks.append(audio)
                else:
                    prev = chunks[-1]

                    if len(prev) > overlap and len(audio) > overlap:
                        fade_out = torch.linspace(1, 0, overlap)
                        fade_in = torch.linspace(0, 1, overlap)

                        mixed = prev[-overlap:] * fade_out + audio[:overlap] * fade_in
                        merged = torch.cat([prev[:-overlap], mixed, audio[overlap:]])
                        chunks[-1] = merged
                    else:
                        chunks.append(audio)

        final_audio = torch.cat(chunks)
        target_len = duration * sample_rate

        return final_audio[:target_len], sample_rate