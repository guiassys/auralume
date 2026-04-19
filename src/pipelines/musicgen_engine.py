import logging as log
import torch
from threading import Lock
from typing import Tuple, Optional

from transformers import MusicgenForConditionalGeneration, AutoProcessor, BitsAndBytesConfig


class MusicGenConfig:
    def __init__(
        self,
        model_size: str = "medium",
        sample_rate: int = 32000,
        quantization: Optional[str] = None, # "8bit" or "4bit"
    ):
        self.model_size = model_size
        self.sample_rate = sample_rate
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
            if config: self.config = config
            return

        self.config = config or MusicGenConfig()
        self.device = self._resolve_device()
        
        self.processor = None
        self.model = None
        self.current_model_size = None
        self.current_quantization = None
        self._initialized = True
        log.info("[MusicGenEngine] Initialized for lazy loading.")

    def load_model(self, model_size: str, quantization: Optional[str] = None):
        if self.model is not None and self.current_model_size == model_size and self.current_quantization == quantization:
            return

        with self._lock:
            if self.model is not None and self.current_model_size == model_size and self.current_quantization == quantization:
                return

            log.info(f"[MusicGenEngine] Loading model: {model_size} with quantization: {quantization}")
            self.config.model_size = model_size
            self.config.quantization = quantization
            
            quantization_config = None
            if self.config.quantization == "8bit":
                quantization_config = BitsAndBytesConfig(load_in_8bit=True)
                log.info("Applying 8-bit quantization.")
            elif self.config.quantization == "4bit":
                quantization_config = BitsAndBytesConfig(load_in_4bit=True)
                log.info("Applying 4-bit quantization.")

            self.processor = AutoProcessor.from_pretrained(self.config.model_name)
            
            # Unload previous model from memory
            if self.model is not None:
                del self.model
                torch.cuda.empty_cache()

            if quantization_config:
                self.model = MusicgenForConditionalGeneration.from_pretrained(
                    self.config.model_name,
                    quantization_config=quantization_config,
                    device_map="auto",
                )
            else:
                torch_dtype = torch.float16 if self.device.type == "cuda" else torch.float32
                log.info(f"Using torch_dtype: {torch_dtype}")
                self.model = MusicgenForConditionalGeneration.from_pretrained(
                    self.config.model_name,
                    torch_dtype=torch_dtype,
                ).to(self.device)
            
            self.current_model_size = model_size
            self.current_quantization = quantization
            log.info("Model loaded successfully.")

    def _resolve_device(self) -> torch.device:
        if torch.cuda.is_available():
            return torch.device("cuda")
        log.warning("CUDA not available. Using CPU.")
        return torch.device("cpu")

    def generate(
        self,
        prompt: str,
        duration: int,
        prompt_audio: Optional[torch.Tensor] = None,
        prompt_sr: Optional[int] = None,
        temperature: float = 1.0,
        top_k: int = 250,
        top_p: float = 0.95,
    ) -> Tuple[torch.Tensor, int]:
        
        # This call is now implicit via the service layer
        # self.load_model(self.config.model_size, self.config.quantization)
        
        device = self.model.device

        if prompt_audio is not None:
            audio_for_processor = prompt_audio.squeeze().to("cpu")
            inputs = self.processor(
                audio=audio_for_processor,
                sampling_rate=prompt_sr,
                text=[prompt],
                return_tensors="pt",
                padding=True
            ).to(device)
        else:
            inputs = self.processor(
                text=[prompt],
                return_tensors="pt",
                padding=True
            ).to(device)

        max_new_tokens = int(duration * 50)

        with torch.no_grad():
            audio_tensor = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                top_k=top_k,
                top_p=top_p,
                temperature=temperature,
            )
        return audio_tensor, self.config.sample_rate
