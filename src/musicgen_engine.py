import torch
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

        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt"
        )

        # garante CPU
        inputs = {k: v.to("cpu") for k, v in inputs.items()}

        with torch.no_grad():
            audio = self.model.generate(
                **inputs,
                max_new_tokens=duration * 50
            )

        return audio, 32000