import logging as log
import torch
from threading import Lock
from typing import Tuple, Optional, Dict, Any

from transformers import MusicgenForConditionalGeneration, AutoProcessor


class MusicGenConfig:
    def __init__(
        self,
        model_size: str = "medium",
        sample_rate: int = 32000,
        max_new_tokens: int = 1500,
        top_k: int = 250,
        top_p: float = 0.95,
        temperature: float = 1.0,
        quantization: Optional[str] = None, # "8bit" or "4bit"
    ):
        self.model_size = model_size
        self.sample_rate = sample_rate
        self.max_new_tokens = max_new_tokens
        self.top_k = top_k
        self.top_p = top_p
        self.temperature = temperature
        self.quantization = quantization

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
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.config = config or MusicGenConfig()
        self.device = self._resolve_device()
        self.dtype = torch.float16 if self.device.type == "cuda" and self.config.quantization is None else torch.float32
        
        # Lazy loading: Defer model loading
        self.processor = None
        self.model = None
        self._initialized = True
        log.info("[MusicGenEngine] Initialized for lazy loading.")

    def _load_model_if_needed(self):
        """Loads the model and processor into memory if they haven't been already."""
        if self.model is not None and self.processor is not None:
            return

        with self._lock:
            if self.model is None:
                log.info(f"[MusicGenEngine] Lazily loading model: {self.config.model_name}")
                
                quantization_config: Dict[str, Any] = {}
                if self.config.quantization == "8bit":
                    quantization_config["load_in_8bit"] = True
                    log.info("Applying 8-bit quantization.")
                elif self.config.quantization == "4bit":
                    quantization_config["load_in_4bit"] = True
                    log.info("Applying 4-bit quantization.")

                self.processor = AutoProcessor.from_pretrained(self.config.model_name)
                self.model = MusicgenForConditionalGeneration.from_pretrained(
                    self.config.model_name,
                    torch_dtype=self.dtype,
                    **quantization_config
                ).to(self.device)
                self.model.eval()
                log.info("Model loaded successfully.")

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
        prompt_sr: Optional[int] = None,
        temperature: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        max_new_tokens_override: Optional[int] = None,
    ) -> Tuple[torch.Tensor, int]:
        
        self._load_model_if_needed()

        if prompt_audio is not None:
            inputs = self._prepare_inputs_with_audio(prompt, prompt_audio, prompt_sr)
        else:
            inputs = self._prepare_inputs(prompt)

        gen_temperature = temperature if temperature is not None else self.config.temperature
        gen_top_k = top_k if top_k is not None else self.config.top_k
        gen_top_p = top_p if top_p is not None else self.config.top_p
        max_new_tokens = max_new_tokens_override if max_new_tokens_override is not None else int(duration * 50)

        with torch.no_grad():
            audio_tensor = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                top_k=gen_top_k,
                top_p=gen_top_p,
                temperature=gen_temperature,
            )
        return audio_tensor, self.config.sample_rate

    def _prepare_inputs(self, prompt: str):
        return self.processor(
            text=[prompt],
            return_tensors="pt",
            padding=True
        ).to(self.device)

    def _prepare_inputs_with_audio(self, prompt: str, prompt_audio: torch.Tensor, prompt_sr: int):
        prompt_audio_cpu = prompt_audio.to("cpu")
        if prompt_audio_cpu.ndim > 1:
            prompt_audio_cpu = prompt_audio_cpu.squeeze(0)

        inputs = self.processor(
            audio=prompt_audio_cpu,
            sampling_rate=prompt_sr,
            text=[prompt],
            return_tensors="pt",
            padding=True
        )
        
        # For quantized models, we must use float32 for inputs, but the model itself is quantized.
        # For full precision on GPU, we use float16.
        if self.dtype == torch.float16:
            if 'input_features' in inputs:
                inputs['input_features'] = inputs['input_features'].to(self.dtype)
            if 'input_values' in inputs:
                inputs['input_values'] = inputs['input_values'].to(self.dtype)

        return inputs.to(self.device)
