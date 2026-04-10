"""Serviço de geração de música para encapsular a lógica de negócio."""

import logging
import os
import threading
import time
from typing import Optional, Dict, Any

from src.scripts.generator import LofiGenerator
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
        self.generator = LofiGenerator(output_dir=self.output_dir)
        self._lock = threading.Lock()

    def generate_music(
        self,
        config: Dict[str, Any],
        log_stream: Optional[LogStream] = None
    ) -> Dict[str, Any]:
        """
        Executa o pipeline de geração com streaming de logs.
        O uso do 'with self._lock' garante que apenas uma música seja gerada por vez.
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

                file_path = self.generator.generate(config=config, log_stream=log_stream)

                end_time = time.time()
                processing_time = time.strftime("%H:%M:%S", time.gmtime(end_time - start_time))

                _log(f"Total processing time: {processing_time}")
                _log(f"Success! Mastered in: {os.path.basename(file_path)}")

                return {
                    "success": True,
                    "file_path": file_path,
                    "error": None
                }

            except Exception as e:
                error_msg = f"Processing failure: {str(e)}"
                _log(error_msg, level="ERROR")
                logger.error(f"[SERVICE] {error_msg}", exc_info=True)

                return {
                    "success": False,
                    "file_path": None,
                    "error": error_msg
                }

    def list_generated_files(self) -> list:
        """Utilitário opcional para listar músicas já criadas na pasta de output."""
        try:
            files = [f for f in os.listdir(self.output_dir) if f.endswith('.wav')]
            return sorted(files, key=lambda x: os.path.getmtime(os.path.join(self.output_dir, x)), reverse=True)
        except Exception:
            return []