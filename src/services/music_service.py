"""Serviço de geração de música para encapsular a lógica de negócio."""

import logging
import os
import threading
from typing import Optional, Dict, Any, Callable

from src.scripts.generator import LofiGenerator

logger = logging.getLogger(__name__)

class MusicGenerationService:
    """
    Serviço que encapsula a geração de música usando config estruturada.
    Atua como um Orquestrador entre a Interface Web e o Engine de IA.
    """

    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        # Garante que a pasta de saída existe
        os.makedirs(self.output_dir, exist_ok=True)

        # Inicializa o gerador (Engine de IA e Pipeline LangChain)
        self.generator = LofiGenerator(output_dir=self.output_dir)
        
        # Lock crucial para evitar condições de corrida na VRAM da GPU
        self._lock = threading.Lock()

    def generate_music(
        self,
        config: Dict[str, Any],
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:
        """
        Executa o pipeline de geração. 
        O uso do 'with self._lock' garante que apenas uma música seja gerada por vez,
        prevenindo erros de 'Out of Memory' na CUDA.
        """
        
        # Tenta adquirir o lock. Se a GPU estiver ocupada, ele aguarda.
        with self._lock:
            try:
                logger.info(f"[SERVICE] Starting the process for the project.: {config.get('name', 'No name')}")
                logger.debug(f"[SERVICE] Parameters received: {config}")

                if progress_callback:
                    progress_callback("📡 Synchronizing with the GPU and loading models...")

                # Chamada para o gerador (que internamente gerencia os chunks e o crossfade)
                # O gerador agora é seguro contra estouro de tokens (30s chunks)
                file_path = self.generator.generate(config=config)

                if progress_callback:
                    progress_callback(f"✅ Success! Mastered in: {os.path.basename(file_path)}")

                return {
                    "success": True,
                    "file_path": file_path,
                    "error": None
                }

            except Exception as e:
                # Captura erros de CUDA, Memória ou Arquivo
                error_msg = f"Processing failure: {str(e)}"
                logger.error(f"[SERVICE] {error_msg}", exc_info=True)

                if progress_callback:
                    progress_callback(f"❌ {error_msg}")

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