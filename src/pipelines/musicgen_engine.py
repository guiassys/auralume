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
            
            torch_dtype = torch.float16 if self.device.type == "cuda" else torch.float32
            
            quantization_config = None
            if self.config.quantization == "8bit":
                quantization_config = BitsAndBytesConfig(
                    load_in_8bit=True,
                )
                log.info("Applying 8-bit quantization.")
            elif self.config.quantization == "4bit":
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch_dtype,
                )
                log.info(f"Applying 4-bit quantization with compute dtype {torch_dtype}.")

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
                    torch_dtype=torch_dtype, # Explicitly pass torch_dtype even with quantization config
                )
            else:
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
        
        device = self.model.device
        
        # Determine base generation dtype depending on context
        target_dtype = torch.float16 if self.device.type == "cuda" else torch.float32

        if prompt_audio is not None:
            # Squeeze and send to cpu as numpy for the processor
            # DO NOT clamp the tensor if it's already bounded or dynamically scaled by earlier logic
            audio_for_processor = prompt_audio.squeeze().to("cpu").numpy()
            
            # Create the inputs using processor
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
            
        # Ensure ALL floating point tensors in the input dict match the target dtype exactly!
        # This is absolutely necessary for Audio generation (Encodec) with BitsAndBytes
        for k, v in inputs.items():
            if torch.is_tensor(v) and v.is_floating_point():
                inputs[k] = v.to(target_dtype)

        max_new_tokens = int(duration * 50)

        with torch.no_grad():
            # The generate function of transformers models when using 8bit or 4bit sometimes has
            # trouble with specific tensors staying float32 during conditional generation.
            # Using autocast is safe but we also must disable caching if we are continuing 
            # from an audio prompt with mixed types to prevent assert errors in attention blocks.
            with torch.autocast(device_type=self.device.type, dtype=target_dtype):
                
                # In bitsandbytes quantized conditional generation, passing use_cache=True 
                # (which is the default) along with prompt audio can trigger CUDA assert errors
                # during attention pass where the past_key_values clash. We explicitly disable it
                # if prompt_audio is present to safely unroll generation over time.
                use_cache = False if prompt_audio is not None else True
                
                audio_tensor = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    do_sample=True,
                    top_k=top_k,
                    top_p=top_p,
                    temperature=temperature,
                    use_cache=use_cache
                )

        return audio_tensor, self.config.sample_rate
