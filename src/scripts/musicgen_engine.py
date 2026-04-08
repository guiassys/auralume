import logging as log
import torch
import math
from transformers import MusicgenForConditionalGeneration, AutoProcessor
from rich.progress import Progress


class MusicGenEngine:
    def __init__(self, model_size="medium"):
        self.model_name = f"facebook/musicgen-{model_size}"

        log.info(f'[MusicGenEngine] Loading model: {self.model_name}')

        # 🔍 DEBUG CUDA
        log.info(f"torch version: {torch.__version__}")
        log.info(f"CUDA available: {torch.cuda.is_available()}")
        log.info(f"CUDA device count: {torch.cuda.device_count()}")

        if torch.cuda.is_available():
            self.device = torch.device('cuda')
            log.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            self.device = torch.device('cpu')
            log.error("CUDA NÃO está funcionando. Usando CPU.")

        print(f"[MusicGenEngine] Carregando modelo: {self.model_name}")

        self.processor = AutoProcessor.from_pretrained(self.model_name)

        self.model = MusicgenForConditionalGeneration.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device.type == "cuda" else torch.float32
        )

        self.model = self.model.to(self.device)
        self.model.eval()

        print(f"[MusicGenEngine] Device: {self.device}")

    def generate(self, prompt="lofi chill beats", duration=30):
        print(f"\n[LOFI GEN] Prompt: {prompt}")

        chunk_duration = 30
        num_chunks = math.ceil(duration / chunk_duration)
        total_audio = []

        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with Progress() as progress:
            task = progress.add_task("[cyan]Gerando música...", total=num_chunks)

            with torch.no_grad():
                for i in range(num_chunks):
                    current_duration = min(chunk_duration, duration - i * chunk_duration)
                    max_tokens = int(current_duration * 50)

                    audio_chunk = self.model.generate(
                        **inputs,
                        audio_prompt=total_audio[-1].unsqueeze(0) if total_audio else None,
                        max_new_tokens=max_tokens,
                        do_sample=True,
                        top_k=250,
                        top_p=0.95,
                        temperature=1.0
                    )

                    total_audio.append(audio_chunk.squeeze(0))
                    progress.update(task, advance=1)

        audio = torch.cat(total_audio, dim=0) if len(total_audio) > 1 else total_audio[0]

        return audio, 32000