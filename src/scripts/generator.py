import json
import logging
import os
import random
import math
from datetime import datetime
from typing import Dict, Any, Optional

import numpy as np
import soundfile as sf
import torch

from src.scripts.musicgen_engine import MusicGenEngine, MusicGenConfig
from src.web.log_stream import LogStream


class TrackGenerator:
    def __init__(
        self,
        engine: Optional[MusicGenEngine] = None,
        config_path: str = "config.json",
    ):
        self.logger = logging.getLogger(__name__)

        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.generator_settings = self.config.get("generator_settings", {})
        self.architect_settings = self.config.get("architect_settings", {})

        engine_config = MusicGenConfig(
            model_size=self.generator_settings.get("model_size", "medium"),
            sample_rate=self.generator_settings.get("sample_rate", 32000),
        )
        self.engine = engine or MusicGenEngine(config=engine_config)

    def generate(self, config: Dict[str, Any], log_stream: Optional[LogStream] = None) -> str:
        prompt = config.get("prompt", "lofi music")
        duration = int(config.get("duration", 180))
        name = config.get("name")
        
        bpm_range = config.get("bpm_range", self.architect_settings.get("bpm_range", [70, 90]))
        bpm = random.randint(bpm_range[0], bpm_range[1])

        key = config.get("key", self.generator_settings.get("key", "C minor"))
        temperature = config.get("temperature", self.generator_settings.get("temperature", 1.0))
        max_new_tokens = config.get("max_new_tokens", self.generator_settings.get("max_new_tokens", 1500))
        output_dir = config.get("output_dir", self.generator_settings.get("output_dir", "outputs"))

        def _log(message: str):
            self.logger.info(f"[GENERATOR] {message}")
            if log_stream:
                log_stream.log(message)

        _log("Starting new generation pipeline...")

        enriched_prompt = self._enrich_prompt(prompt, bpm, key)
        _log(f"Enriched prompt: '{enriched_prompt}'")

        chunk_duration = self.generator_settings.get("chunk_duration", 10)
        overlap_duration = self.generator_settings.get("overlap_duration", 2)
        
        # Corrected calculation for num_chunks
        effective_chunk_duration = chunk_duration - overlap_duration
        if duration <= chunk_duration:
            num_chunks = 1
            gen_duration = duration # Generate exact duration if less than a chunk
        else:
            num_chunks = 1 + math.ceil((duration - chunk_duration) / effective_chunk_duration)
            gen_duration = chunk_duration

        _log(f"Generation plan: {num_chunks} chunks for a target duration of {duration}s.")

        _log(f"Generating intro chunk (1/{num_chunks})...")
        intro_audio, sr = self.engine.generate(
            enriched_prompt,
            gen_duration,
            temperature=temperature,
            max_new_tokens_override=max_new_tokens
        )
        full_audio = self._apply_fade(intro_audio.squeeze(0), sr, 'in')
        _log("Intro chunk generated.")

        for i in range(1, num_chunks):
            _log(f"Generating continuation chunk ({i + 1}/{num_chunks})...")
            
            # Increase context for the prompt audio
            prompt_context_duration = min(overlap_duration + 1, full_audio.shape[1] / sr)
            prompt_audio = full_audio[:, -int(prompt_context_duration * sr):]

            continuation_audio, _ = self._generate_continuation(
                enriched_prompt,
                prompt_audio,
                chunk_duration,
                sr,
                temperature,
                max_new_tokens
            )
            
            full_audio = self._crossfade_and_append(full_audio, continuation_audio.squeeze(0), overlap_duration, sr)
            _log(f"Continuation chunk {i + 1}/{num_chunks} added.")

        # Trim audio to the exact requested duration
        final_samples = int(duration * sr)
        if full_audio.shape[1] > final_samples:
            full_audio = full_audio[:, :final_samples]
            _log(f"Audio trimmed to {duration}s.")

        _log("Applying final fade-out...")
        fade_out_duration = self.generator_settings.get("fade_out_duration", 2)
        final_audio = self._apply_fade(full_audio, sr, 'out', duration=fade_out_duration)
        _log("Post-processing complete.")

        _log("Saving final audio file...")
        os.makedirs(output_dir, exist_ok=True)
        path = self._save_audio(final_audio, sr, name, output_dir)
        _log(f"Audio saved successfully to: {os.path.basename(path)}")

        return path

    def _enrich_prompt(self, simple_prompt: str, bpm: int, key: str) -> str:
        return f"{simple_prompt}, {bpm} bpm, {key}"

    def _generate_continuation(
        self,
        prompt: str,
        prompt_audio: torch.Tensor,
        duration: int,
        sr: int,
        temperature: float,
        max_new_tokens: int
    ) -> tuple[torch.Tensor, int]:
        return self.engine.generate(
            prompt=prompt,
            duration=duration,
            prompt_audio=prompt_audio,
            prompt_sr=sr,
            temperature=temperature,
            max_new_tokens_override=max_new_tokens
        )

    def _crossfade_and_append(self, audio1: torch.Tensor, audio2: torch.Tensor, overlap_duration: int, sr: int) -> torch.Tensor:
        overlap_samples = int(overlap_duration * sr)
        
        fade_out = torch.linspace(1, 0, overlap_samples, device=audio1.device, dtype=audio1.dtype).unsqueeze(0)
        fade_in = torch.linspace(0, 1, overlap_samples, device=audio1.device, dtype=audio1.dtype).unsqueeze(0)

        # Ensure tensors have enough samples for overlap
        if audio1.shape[1] < overlap_samples or audio2.shape[1] < overlap_samples:
             _log("Warning: Audio chunk is smaller than overlap, skipping crossfade.")
             return torch.cat([audio1, audio2], dim=1)

        crossfaded_part = audio1[:, -overlap_samples:] * fade_out + audio2[:, :overlap_samples] * fade_in

        return torch.cat([
            audio1[:, :-overlap_samples],
            crossfaded_part,
            audio2[:, overlap_samples:]
        ], dim=1)

    def _apply_fade(self, audio: torch.Tensor, sr: int, fade_type: str, duration: int = 1) -> torch.Tensor:
        fade_samples = int(duration * sr)
        if fade_samples == 0:
            return audio
            
        if fade_samples > audio.shape[1]:
            fade_samples = audio.shape[1]

        if fade_type == 'in':
            fade = torch.linspace(0, 1, fade_samples, device=audio.device, dtype=audio.dtype).unsqueeze(0)
            audio[:, :fade_samples] *= fade
        elif fade_type == 'out':
            fade = torch.linspace(1, 0, fade_samples, device=audio.device, dtype=audio.dtype).unsqueeze(0)
            audio[:, -fade_samples:] *= fade

        return audio

    def _save_audio(self, audio: torch.Tensor, sr: int, name: Optional[str], output_dir: str) -> str:
        filename = name or datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(output_dir, f"{filename}.wav")

        audio_np = audio.to(torch.float32).cpu().numpy().T

        peak = np.max(np.abs(audio_np))
        if peak > 0:
            audio_np /= peak

        sf.write(path, audio_np, sr)
        return path
