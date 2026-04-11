import logging as log
import torch
from threading import Lock
from typing import Tuple, Optional

from transformers import MusicgenForConditionalGeneration, AutoProcessor


class MusicGenConfig:
    def __init__(
        self,
        model_size: str = "medium",
        sample_rate: int = 32000,
        max_new_tokens: int = 1500, # Corresponds to ~30s of audio
        top_k: int = 250,
        top_p: float = 0.95,
        temperature: float = 1.0,
    ):
        self.model_size = model_size
        self.sample_rate = sample_rate
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
        self.dtype = torch.float16 if self.device.type == "cuda" else torch.float32

        log.info(f"[MusicGenEngine] Loading model: {self.config.model_name}")
        self.processor = AutoProcessor.from_pretrained(self.config.model_name)
        self.model = MusicgenForConditionalGeneration.from_pretrained(
            self.config.model_name,
            torch_dtype=self.dtype
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

    def generate(
        self,
        prompt: str,
        duration: int,
        prompt_audio: Optional[torch.Tensor] = None,
        prompt_sr: Optional[int] = None
    ) -> Tuple[torch.Tensor, int]:

        if prompt_audio is not None:
            inputs = self._prepare_inputs_with_audio(prompt, prompt_audio, prompt_sr)
        else:
            inputs = self._prepare_inputs(prompt)

        # Adjust max_new_tokens based on duration
        # MusicGen's tokenizer has a rate of 50 tokens/sec
        max_new_tokens = int(duration * 50)

        with torch.no_grad():
            audio_tensor = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                top_k=self.config.top_k,
                top_p=self.config.top_p,
                temperature=self.config.temperature,
            )

        # The output is on the same device as the model, which is what we want
        return audio_tensor, self.config.sample_rate

    def _prepare_inputs(self, prompt: str):
        return self.processor(
            text=[prompt],
            return_tensors="pt",
            padding=True
        ).to(self.device)

    def _prepare_inputs_with_audio(self, prompt: str, prompt_audio: torch.Tensor, prompt_sr: int):
        # 1. Ensure prompt audio is on CPU for the processor
        prompt_audio_cpu = prompt_audio.to("cpu")

        # 2. Squeeze to 1D tensor if needed
        if prompt_audio_cpu.ndim > 1:
            prompt_audio_cpu = prompt_audio_cpu.squeeze(0)

        inputs = self.processor(
            audio=prompt_audio_cpu,
            sampling_rate=prompt_sr,
            text=[prompt],
            return_tensors="pt",
            padding=True
        )

        # 3. Correct dtype mismatch for ALL relevant tensors
        if self.dtype == torch.float16:
            if 'input_features' in inputs: # Text prompt features
                inputs['input_features'] = inputs['input_features'].to(self.dtype)
            if 'input_values' in inputs: # Audio prompt features
                inputs['input_values'] = inputs['input_values'].to(self.dtype)

        # 4. Move all tensors to the target device (GPU)
        return inputs.to(self.device)
