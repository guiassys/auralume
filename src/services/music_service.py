"""Serviço de geração de música para encapsular a lógica de negócio."""

import logging
import os
import threading
from typing import Optional, Dict, Any

from src.scripts.generator import LofiGenerator

logger = logging.getLogger(__name__)


class MusicGenerationService:
    """Serviço que encapsula a geração de música usando config estruturada."""

    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.generator = LofiGenerator(output_dir=self.output_dir)
        self._lock = threading.Lock()

    # -----------------------------
    # MAIN ENTRY (CONFIG-BASED)
    # -----------------------------
    def generate_music(
        self,
        config: Dict[str, Any],
        progress_callback: Optional[callable] = None
    ) -> dict:

        with self._lock:
            try:
                logger.info(f"[SERVICE] Config recebida: {config}")

                if progress_callback:
                    progress_callback("Iniciando pipeline estruturado...")

                file_path = self.generator.generate(config=config)

                if progress_callback:
                    progress_callback("Geração concluída!")

                return {
                    "success": True,
                    "file_path": file_path,
                    "error": None
                }

            except Exception as e:
                error_msg = f"Erro na geração: {str(e)}"
                logger.error(error_msg, exc_info=True)

                if progress_callback:
                    progress_callback(error_msg)

                return {
                    "success": False,
                    "file_path": None,
                    "error": error_msg
                }