"""Serviço de geração de música para encapsular a lógica de negócio."""

import logging
import os
import re
import subprocess
import threading
import time
import json
import random
import torch
import numpy as np
import soundfile as sf
from typing import Optional, Dict, Any
from pydub import AudioSegment
from datetime import datetime

from src.pipelines.musicgen_engine import MusicGenEngine, MusicGenConfig
from src.pipelines.musicgen_pipeline import MusicPipeline
from src.pipelines.simple_music_pipeline import SimpleMusicPipeline
from src.web.log_stream import LogStream

logger = logging.getLogger(__name__)

class MusicGenerationService:
    """
    Serviço que encapsula a geração de música usando config estruturada.
    Atua como um Orquestrador entre a Interface Web e o Engine de IA.
    """

    def __init__(self, config_path: str = "config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.generator_settings = self.config.get("generator_settings", {})

        # Engine is now initialized without a default model loaded.
        self.engine = MusicGenEngine()
        self._lock = threading.Lock()
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    def _convert_path_for_wsl(self, path: str) -> str:
        if re.match(r"^[a-zA-Z]:[\\/]", path):
            path = path.replace("\\", "/")
            drive, rest = path.split(":", 1)
            return f"/mnt/{drive.lower()}{rest}"
        return path

    def _save_audio(self, audio: torch.Tensor, sr: int, name: str, output_dir: str) -> str:
        output_dir = self._convert_path_for_wsl(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        path = os.path.join(output_dir, f"{name}.wav")
        if audio.ndim > 2:
            audio = audio.squeeze(0)
        
        audio_np = audio.to(torch.float32).cpu().numpy().T

        peak = np.max(np.abs(audio_np))
        if peak > 1.0:
            audio_np /= peak

        sf.write(path, audio_np, sr)
        return path

    def _apply_fade_out(self, audio: torch.Tensor, sr: int, duration: int) -> torch.Tensor:
        fade_duration = duration
        fade_samples = int(fade_duration * sr)
        if fade_samples > audio.shape[1]:
            fade_samples = audio.shape[1]

        if fade_samples > 0:
            fade = torch.linspace(1, 0, fade_samples, device=audio.device, dtype=audio.dtype).unsqueeze(0)
            audio[:, -fade_samples:] *= fade
        return audio

    def generate_music(self, config: Dict[str, Any], log_stream: Optional[LogStream] = None) -> Dict[str, Any]:
        """Executa o pipeline de geração com base no tipo de pipeline."""
        def _log(message: str, level: str = "INFO"):
            logger.info(f"[SERVICE] {message}")
            if log_stream:
                log_stream.log(message, level)

        with self._lock:
            start_time = time.time()
            try:
                pipeline_type = config.get("pipeline_type", "Advanced")
                _log(f"Starting {pipeline_type.lower()} pipeline for project: {config.get('name', 'Unnamed')}")

                # --- Model Loading with Dynamic Quantization ---
                model_size = config.get("model_size")
                quantization = config.get("quantization")
                self.engine.load_model(model_size, quantization)

                if pipeline_type == "Simple":
                    pipeline = SimpleMusicPipeline(self.engine, self.config, log_stream)
                    result = pipeline.run(**config)
                else: # Advanced
                    pipeline = MusicPipeline(self.engine, self.config, log_stream)
                    result = pipeline.build(**config)

                final_audio = result["audio"]
                sr = result["sr"]

                # Final processing
                duration = 30 if pipeline_type == "Simple" else config["duration"]
                final_samples = int(duration * sr)
                if final_audio.shape[1] > final_samples:
                    final_audio = final_audio[:, :final_samples]
                    _log(f"Audio trimmed to {duration}s.")

                if pipeline_type == "Advanced":
                    fade_out_duration = config.get("fade_out_duration", 2)
                    final_audio = self._apply_fade_out(final_audio, sr, fade_out_duration)
                    _log("Final fade-out applied.")

                wav_path = self._save_audio(final_audio, sr, config["name"], config["output_dir"])
                _log(f"WAV file saved to: {os.path.basename(wav_path)}")

                primary_audio_path = wav_path
                generated_files = [wav_path]

                if config.get("audio_format") == ".mp3":
                    _log("Converting to MP3 format...")
                    mp3_path = wav_path.replace(".wav", ".mp3")
                    AudioSegment.from_wav(wav_path).export(mp3_path, format="mp3")
                    os.remove(wav_path)
                    primary_audio_path = mp3_path
                    generated_files = [mp3_path]
                    _log(f"MP3 file created: {os.path.basename(mp3_path)}")

                end_time = time.time()
                _log(f"Total processing time: {time.strftime('%H:%M:%S', time.gmtime(end_time - start_time))}")
                _log(f"Success! Mastered in: {os.path.basename(primary_audio_path)}")

                return {"success": True, "files": generated_files, "error": None}

            except Exception as e:
                error_msg = f"Processing failure: {str(e)}"
                _log(error_msg, level="ERROR")
                logger.error(f"[SERVICE] {error_msg}", exc_info=True)
                return {"success": False, "files": [], "error": error_msg}

    def list_generated_files(self, output_dir: str) -> list:
        """Utilitário opcional para listar músicas já criadas na pasta de output."""
        try:
            path = self._convert_path_for_wsl(output_dir)
            files = [f for f in os.listdir(path) if f.endswith(('.wav', '.mp3', '.mid'))]
            return sorted(files, key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=True)
        except Exception:
            return []
