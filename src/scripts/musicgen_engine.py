import logging as log
import math
from threading import Lock
from typing import Tuple, List

import torch
from transformers import MusicgenForConditionalGeneration, AutoProcessor


class MusicGenConfig:
    def __init__(
        self,
        model_size: str = "medium",
        sample_rate: int = 32000,
        chunk_duration: int = 30,
        overlap_sec: int = 5,
        max_new_tokens: int = 1500,
        top_k: int = 250,
        top_p: float = 0.95,
        temperature: float = 1.0,
    ):
        self.model_size = model_size
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.overlap_sec = overlap_sec
        self.max_new_tokens = max_new_tokens
        self.top_k = top_k
        self.top_p = top_p
        self.temperature = temperature

    @property
    def model_name(self) -> str:
        return f"facebook/musicgen-{self.model_size}"


class MusicGenEngine:
    _instance = None
    _lock = Lock()

    def __new__(cls, config: MusicGenConfig = None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: MusicGenConfig = None):
        if hasattr(self, "_initialized"):
            return

        self.config = config or MusicGenConfig()
        self.device = self._resolve_device()

        log.info(f"[MusicGenEngine] Loading model: {self.config.model_name}")

        self.processor = AutoProcessor.from_pretrained(self.config.model_name)

        dtype = torch.float16 if self.device.type == "cuda" else torch.float32

        self.model = MusicgenForConditionalGeneration.from_pretrained(
            self.config.model_name,
            torch_dtype=dtype
        ).to(self.device)

        self.model.eval()

        self._initialized = True

    def _resolve_device(self) -> torch.device:
        if torch.cuda.is_available():
            device = torch.device("cuda")
            log.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
            return device

        log.warning("CUDA not available. Using CPU.")
        return torch.device("cpu")

    def generate(self, prompt: str, duration: int) -> Tuple[torch.Tensor, int]:
        inputs = self._prepare_inputs(prompt)
        chunks = self._generate_chunks(inputs, duration)
        audio = self._merge_chunks(chunks)

        target_len = duration * self.config.sample_rate
        return audio[:target_len], self.config.sample_rate

    def generate_section(self, prompt: str, duration: int) -> Tuple[torch.Tensor, int]:
        return self.generate(prompt, duration)

    def _prepare_inputs(self, prompt: str):
        return self.processor(
            text=[prompt],
            return_tensors="pt",
            padding=True
        ).to(self.device)

    def _generate_chunks(self, inputs, duration: int) -> List[torch.Tensor]:
        cfg = self.config

        overlap = int(cfg.sample_rate * cfg.overlap_sec)
        effective_chunk = cfg.chunk_duration - cfg.overlap_sec
        num_chunks = math.ceil(duration / effective_chunk)

        chunks: List[torch.Tensor] = []

        with torch.no_grad():
            for i in range(num_chunks):
                log.info(f"[ENGINE] Chunk {i+1}/{num_chunks}")

                audio = self.model.generate(
                    **inputs,
                    max_new_tokens=cfg.max_new_tokens,
                    do_sample=True,
                    top_k=cfg.top_k,
                    top_p=cfg.top_p,
                    temperature=cfg.temperature,
                )

                audio = audio.squeeze().cpu()

                if not chunks:
                    chunks.append(audio)
                else:
                    chunks[-1] = self._crossfade(chunks[-1], audio, overlap)

        return chunks

    def _crossfade(
        self,
        previous: torch.Tensor,
        current: torch.Tensor,
        overlap: int
    ) -> torch.Tensor:
        if len(previous) <= overlap or len(current) <= overlap:
            return torch.cat([previous, current])

        fade_out = torch.linspace(1, 0, overlap)
        fade_in = torch.linspace(0, 1, overlap)

        mixed = previous[-overlap:] * fade_out + current[:overlap] * fade_in

        return torch.cat([
            previous[:-overlap],
            mixed,
            current[overlap:]
        ])

    def _merge_chunks(self, chunks: List[torch.Tensor]) -> torch.Tensor:
        if len(chunks) == 1:
            return chunks[0]
        return torch.cat(chunks)