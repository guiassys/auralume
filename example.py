"""Exemplo de uso programático do serviço de geração de música."""

import sys
import os

# Adiciona o diretório raiz do projeto ao path
project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

from src.services.music_service import MusicGenerationService

def main():
    # Instancia o serviço
    service = MusicGenerationService(output_dir="outputs")

    # Gera música
    result = service.generate_music(
        name="exemplo_lofi",
        duration=60,
        prompt="lofi hip hop, chill beats, soft piano"
    )

    if result['success']:
        print(f"✅ Música gerada: {result['file_path']}")
    else:
        print(f"❌ Erro: {result['error']}")

if __name__ == "__main__":
    main()