import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional

import numpy as np
import soundfile as sf
import torch

from src.scripts.musicgen_engine import MusicGenEngine
from src.web.log_stream import LogStream


class TrackGenerator:
    def __init__(
        self,
        output_dir: str = "outputs",
        engine: Optional[MusicGenEngine] = None,
    ):
        self.output_dir = output_dir
        self.engine = engine or MusicGenEngine()
        self.logger = logging.getLogger(__name__)
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, config: Dict[str, Any], log_stream: Optional[LogStream] = None) -> str:
        prompt = config.get("prompt", "lofi music")
        duration = int(config.get("duration", 180))
        name = config.get("name")

        def _log(message: str):
            self.logger.info(f"[GENERATOR] {message}")
            if log_stream:
                log_stream.log(message)

        _log("Starting new generation pipeline...")

        # 1. Prompt Enrichment
        enriched_prompt = self._enrich_prompt(prompt)
        _log(f"Enriched prompt: '{enriched_prompt}'")

        # 2. Generation Plan
        chunk_duration = 10  # seconds
        overlap_duration = 2  # seconds
        num_chunks = (duration - chunk_duration) // (chunk_duration - overlap_duration) + 1

        # 3. Intro Generation
        _log("Generating intro chunk (1/)...")
        intro_audio, sr = self.engine.generate(enriched_prompt, chunk_duration)
        full_audio = intro_audio.squeeze(0)  # Squeeze to (channels, samples)
        _log("Intro chunk generated.")

        # 4. Continuation Loop
        for i in range(1, num_chunks):
            _log(f"Generating continuation chunk ({i + 1}/{num_chunks})...")
            prompt_audio = full_audio[:, -int(overlap_duration * sr):]

            continuation_audio, _ = self._generate_continuation(
                enriched_prompt,
                prompt_audio,
                chunk_duration,
                sr
            )
            # Squeeze the continuation chunk as well
            continuation_audio = continuation_audio.squeeze(0)

            full_audio = self._crossfade_and_append(full_audio, continuation_audio, overlap_duration, sr)
            _log(f"Continuation chunk {i + 1}/{num_chunks} added.")

        # 5. Outro and Post-Processing
        _log("Applying final fade-out...")
        final_audio = self._apply_fade_out(full_audio, sr, duration=2)
        _log("Post-processing complete.")

        # 6. Save to file
        _log("Saving final audio file...")
        path = self._save_audio(final_audio, sr, name)
        _log(f"Audio saved successfully to: {os.path.basename(path)}")

        return path

    def _enrich_prompt(self, simple_prompt: str) -> str:
        # Placeholder for a more sophisticated prompt engineering logic
        return f"{simple_prompt}, lofi chill, calm, instrumental, 90 bpm, C minor"

    def _generate_continuation(self, prompt: str, prompt_audio: torch.Tensor, duration: int, sr: int) -> tuple[torch.Tensor, int]:
        return self.engine.generate(
            prompt=prompt,
            duration=duration,
            prompt_audio=prompt_audio,
            prompt_sr=sr
        )

    def _crossfade_and_append(self, audio1: torch.Tensor, audio2: torch.Tensor, overlap_duration: int, sr: int) -> torch.Tensor:
        overlap_samples = int(overlap_duration * sr)

        # Ensure fade tensors have same dtype and device as audio
        fade_out = torch.linspace(1, 0, overlap_samples, device=audio1.device, dtype=audio1.dtype).unsqueeze(0)
        fade_in = torch.linspace(0, 1, overlap_samples, device=audio1.device, dtype=audio1.dtype).unsqueeze(0)

        # Apply crossfade
        crossfaded_part = audio1[:, -overlap_samples:] * fade_out + audio2[:, :overlap_samples] * fade_in

        # Concatenate
        return torch.cat([
            audio1[:, :-overlap_samples],
            crossfaded_part,
            audio2[:, overlap_samples:]
        ], dim=1)

    def _apply_fade_out(self, audio: torch.Tensor, sr: int, duration: int) -> torch.Tensor:
        fade_out_samples = int(duration * sr)
        if fade_out_samples > audio.shape[1]:
            fade_out_samples = audio.shape[1]

        # Ensure fade tensor has same dtype and device as audio
        fade_out = torch.linspace(1, 0, fade_out_samples, device=audio.device, dtype=audio.dtype).unsqueeze(0)
        audio[:, -fade_out_samples:] *= fade_out
        return audio

    def _save_audio(self, audio: torch.Tensor, sr: int, name: Optional[str]) -> str:
        filename = name or datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.output_dir, f"{filename}.wav")

        # Convert to numpy for soundfile, ensuring it's float32 for sf.write
        audio_np = audio.to(torch.float32).cpu().numpy().T

        # Normalize
        peak = np.max(np.abs(audio_np))
        if peak > 0:
            audio_np /= peak

        sf.write(path, audio_np, sr)
        return path
