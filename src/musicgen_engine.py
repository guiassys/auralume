import torch
import math
from transformers import MusicgenForConditionalGeneration, AutoProcessor


class MusicGenEngine:
    def __init__(self, model_size="medium"):
        self.model_name = f"facebook/musicgen-{model_size}"

        print(f"[MusicGenEngine] Carregando modelo: {self.model_name}")

        # CPU ONLY (mais estável no seu caso)
        self.device = "cpu"

        self.processor = AutoProcessor.from_pretrained(self.model_name)

        self.model = MusicgenForConditionalGeneration.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32
        )

        self.model = self.model.to("cpu")
        self.model.eval()

        print("[MusicGenEngine] Device: CPU")

    def generate(self, prompt="lofi chill beats", duration=30):
        print(f"\n[LOFI GEN] Prompt: {prompt}")

        chunk_duration = 30  # segundos por chunk para evitar limite de posição
        num_chunks = math.ceil(duration / chunk_duration)
        total_audio = []

        for i in range(num_chunks):
            current_duration = min(chunk_duration, duration - i * chunk_duration)
            max_tokens = int(current_duration * 50)

            if i == 0:
                # Primeira geração com prompt
                inputs = self.processor(
                    text=[prompt],
                    padding=True,
                    return_tensors="pt"
                )
                inputs = {k: v.to("cpu") for k, v in inputs.items()}
            else:
                # Continuação: usa os tokens gerados anteriormente
                # Para continuação, precisamos passar os input_ids do final da geração anterior
                # Mas para simplificar, regeneramos com prompt (pode haver descontinuidade)
                inputs = self.processor(
                    text=[prompt],
                    padding=True,
                    return_tensors="pt"
                )
                inputs = {k: v.to("cpu") for k, v in inputs.items()}

            with torch.no_grad():
                audio_chunk = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens
                )
            
            total_audio.append(audio_chunk.squeeze(0))

        # Concatena todos os chunks de áudio
        if len(total_audio) > 1:
            audio = torch.cat(total_audio, dim=0)
        else:
            audio = total_audio[0]

        return audio, 32000