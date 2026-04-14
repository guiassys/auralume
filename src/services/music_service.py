"""Serviço de geração de música para encapsular a lógica de negócio."""

import logging
import os
import subprocess
import sys
import threading
import time
from typing import Optional, Dict, Any
from pydub import AudioSegment

from src.scripts.generator import TrackGenerator
from src.web.log_stream import LogStream

logger = logging.getLogger(__name__)

class MusicGenerationService:
    """
    Serviço que encapsula a geração de música usando config estruturada.
    Atua como um Orquestrador entre a Interface Web e o Engine de IA.
    """

    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.generator = TrackGenerator(output_dir=self.output_dir)
        self._lock = threading.Lock()
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    def _convert_to_mp3(self, wav_path: str) -> str:
        """Converts a WAV file to MP3."""
        mp3_path = wav_path.replace(".wav", ".mp3")
        audio = AudioSegment.from_wav(wav_path)
        audio.export(mp3_path, format="mp3")
        return mp3_path

    def _transcribe_to_midi(self, audio_path: str, log_stream: Optional[LogStream]) -> Optional[str]:
        """
        Calls the dedicated transcription script in a separate Python environment.
        """
        def _log(message: str, level: str = "INFO"):
            logger.info(f"[MIDI] {message}")
            if log_stream:
                log_stream.log(message, level)

        midi_venv_python = os.path.join(self.project_root, ".venv-midi", "bin", "python")
        transcribe_script = os.path.join(self.project_root, "src", "scripts", "transcribe.py")

        if not os.path.exists(midi_venv_python):
            _log("MIDI generation environment (.venv-midi) not found. Skipping.", level="ERROR")
            return None

        _log("Starting MIDI transcription process...")
        command = [midi_venv_python, transcribe_script, audio_path]

        try:
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                cwd=self.project_root
            )
            _log("Transcription script executed successfully.")
            for line in process.stdout.splitlines():
                _log(line)
            
            midi_path = audio_path.rsplit('.', 1)[0] + ".mid"
            if os.path.exists(midi_path):
                _log(f"MIDI file confirmed: {os.path.basename(midi_path)}")
                return midi_path
            else:
                _log("Transcription script finished, but MIDI file not found.", level="ERROR")
                return None

        except subprocess.CalledProcessError as e:
            _log(f"MIDI transcription script failed with exit code {e.returncode}.", level="ERROR")
            _log("--- Script Output (stdout) ---", level="ERROR")
            for line in e.stdout.splitlines():
                _log(line, level="ERROR")
            _log("--- Script Errors (stderr) ---", level="ERROR")
            for line in e.stderr.splitlines():
                _log(line, level="ERROR")
            return None
        except Exception as e:
            _log(f"An unexpected error occurred while running the transcription script: {e}", level="ERROR")
            return None

    def generate_music(
        self,
        config: Dict[str, Any],
        log_stream: Optional[LogStream] = None
    ) -> Dict[str, Any]:
        """
        Executa o pipeline de geração com streaming de logs.
        """
        def _log(message: str, level: str = "INFO"):
            logger.info(f"[SERVICE] {message}")
            if log_stream:
                log_stream.log(message, level)

        with self._lock:
            start_time = time.time()
            try:
                _log(f"Starting the process for project: {config.get('name', 'Unnamed')}")
                _log(f"Input parameters: {config}")

                _log("Synchronizing with the GPU and loading models...")

                wav_path = self.generator.generate(config=config, log_stream=log_stream)
                
                primary_audio_path = wav_path
                generated_files = [wav_path]

                # Convert to MP3 if requested
                if config.get("audio_format") == ".mp3":
                    _log("Converting to MP3 format...")
                    mp3_path = self._convert_to_mp3(wav_path)
                    _log(f"MP3 file created: {os.path.basename(mp3_path)}")
                    os.remove(wav_path)
                    primary_audio_path = mp3_path
                    generated_files = [mp3_path]

                # Generate MIDI file if requested
                if config.get("generate_midi"):
                    midi_path = self._transcribe_to_midi(primary_audio_path, log_stream)
                    if midi_path:
                        generated_files.append(midi_path)

                end_time = time.time()
                processing_time = time.strftime("%H:%M:%S", time.gmtime(end_time - start_time))

                _log(f"Total processing time: {processing_time}")
                _log(f"Success! Mastered in: {os.path.basename(primary_audio_path)}")

                return {
                    "success": True,
                    "files": generated_files,
                    "error": None
                }

            except Exception as e:
                error_msg = f"Processing failure: {str(e)}"
                _log(error_msg, level="ERROR")
                logger.error(f"[SERVICE] {error_msg}", exc_info=True)

                return {
                    "success": False,
                    "files": [],
                    "error": error_msg
                }

    def list_generated_files(self) -> list:
        """Utilitário opcional para listar músicas já criadas na pasta de output."""
        try:
            files = [f for f in os.listdir(self.output_dir) if f.endswith(('.wav', '.mp3', '.mid'))]
            return sorted(files, key=lambda x: os.path.getmtime(os.path.join(self.output_dir, x)), reverse=True)
        except Exception:
            return []