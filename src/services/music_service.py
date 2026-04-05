"""Serviço de geração de música para encapsular a lógica de negócio."""

import logging
import os
import threading
from typing import Optional

from src.scripts.generator import LofiGenerator

logger = logging.getLogger(__name__)


class MusicGenerationService:
    """Serviço que encapsula a geração de música usando o pipeline existente."""

    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.generator = LofiGenerator()
        self._lock = threading.Lock()  # Para isolamento básico em múltiplos usuários

    def generate_music(
        self,
        name: str,
        duration: int,
        prompt: str,
        progress_callback: Optional[callable] = None
    ) -> dict:
        """
        Gera música usando o pipeline existente.

        Args:
            name: Nome da música
            duration: Duração em segundos
            prompt: Prompt de estilo musical
            progress_callback: Função opcional para atualizar progresso

        Returns:
            dict: {'success': bool, 'file_path': str, 'error': str}
        """
        with self._lock:
            try:
                logger.info(f"Iniciando geração: {name}, duração: {duration}s, prompt: {prompt}")

                if progress_callback:
                    progress_callback("Iniciando pipeline de geração...")

                # Reutiliza o pipeline existente
                file_path = self.generator.generate(
                    prompt=prompt,
                    duration=duration,
                    name=name
                )

                if progress_callback:
                    progress_callback("Geração concluída!")

                logger.info(f"Geração concluída: {file_path}")

                return {
                    'success': True,
                    'file_path': file_path,
                    'error': None
                }

            except Exception as e:
                error_msg = f"Erro na geração: {str(e)}"
                logger.error(error_msg, exc_info=True)

                if progress_callback:
                    progress_callback(f"Erro: {error_msg}")

                return {
                    'success': False,
                    'file_path': None,
                    'error': error_msg
                }