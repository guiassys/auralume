import torch
import math
from transformers import MusicgenForConditionalGeneration, AutoProcessor
from rich.progress import Progress


class MusicGenEngine:
    def __init__(self, model_size="medium", use_float16=True, enable_optimizations=True):
        self.model_name = f"facebook/musicgen-{model_size}"
        self.use_float16 = use_float16
        self.enable_optimizations = enable_optimizations

        print(f"[MusicGenEngine] Carregando modelo: {self.model_name}")
        print(f"[MusicGenEngine] Float16: {use_float16}, Otimizações: {enable_optimizations}")

        # Verifica disponibilidade da GPU com suporte a float16
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.dtype = torch.float16 if (use_float16 and self.device.type == 'cuda') else torch.float32

        self.processor = AutoProcessor.from_pretrained(self.model_name)

        # Carrega modelo com dtype otimizado
        self.model = MusicgenForConditionalGeneration.from_pretrained(
            self.model_name,
            torch_dtype=self.dtype,
            device_map="auto" if self.device.type == 'cuda' else "cpu"
        )

        self.model = self.model.to(self.device)
        self.model.eval()

        # Otimizações para maior velocidade
        if self.enable_optimizations and self.device.type == 'cuda':
            try:
                # Enable flash attention (mais rápido e menos memória)
                self.model.enable_flash_attention_2()
                print("[MusicGenEngine] Flash Attention 2 ativado")
            except Exception as e:
                print(f"[MusicGenEngine] Flash Attention 2 não disponível: {e}")

            try:
                # Compilar modelo para GPU (torchscript otimizado)
                self.model = torch.compile(self.model, mode="reduce-overhead")
                print("[MusicGenEngine] Modelo compilado com torch.compile")
            except Exception as e:
                print(f"[MusicGenEngine] torch.compile não disponível: {e}")

        print(f"[MusicGenEngine] Device: {self.device}, Dtype: {self.dtype}")

    def generate(self, prompt="lofi chill beats", duration=30):
        print(f"\n[LOFI GEN] Prompt: {prompt}")

        chunk_duration = 30  # segundos por chunk para evitar limite de posição
        num_chunks = math.ceil(duration / chunk_duration)
        total_audio = []

        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Converter inputs para dtype apropriado se necessário
        if self.dtype == torch.float16:
            for key in inputs:
                if inputs[key].dtype == torch.float32:
                    inputs[key] = inputs[key].half()

        with Progress() as progress:
            task = progress.add_task("[cyan]Gerando música...", total=num_chunks)
            
            # Usar torch.cuda.amp para mixed precision (mais rápido)
            with torch.no_grad():
                with torch.cuda.amp.autocast(enabled=(self.device.type == 'cuda' and self.use_float16)):
                    for i in range(num_chunks):
                        current_duration = min(chunk_duration, duration - i * chunk_duration)
                        max_tokens = int(current_duration * 50)

                        audio_chunk = self.model.generate(
                            **inputs,
                            max_new_tokens=max_tokens,
                            do_sample=True,
                            top_k=250,
                            top_p=0.0,
                            temperature=1.0,
                            use_cache=True  # Cache de KV para speedup
                        )

                        total_audio.append(audio_chunk.squeeze(0))
                        progress.update(task, advance=1)

        # Concatena todos os chunks de áudio
        if len(total_audio) > 1:
            audio = torch.cat(total_audio, dim=0)
        else:
            audio = total_audio[0]

        return audio, 32000
