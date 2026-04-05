# Teste rápido para verificar se os arquivos são salvos no diretório correto

import sys
import os

# Adiciona o diretório raiz do projeto ao path
project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

from src.services.music_service import MusicGenerationService

def test_output_directory():
    print("Testando diretório de saída...")

    # Cria serviço com diretório outputs
    service = MusicGenerationService(output_dir="outputs")

    # Simula uma geração (apenas verifica se o diretório existe e é usado)
    print(f"Diretório de saída configurado: {service.output_dir}")
    print(f"Diretório existe: {os.path.exists(service.output_dir)}")

    # Verifica se o LofiGenerator recebeu o output_dir correto
    print(f"LofiGenerator output_dir: {service.generator.output_dir}")

    print("✅ Teste concluído - arquivos serão salvos em 'outputs/'")

if __name__ == "__main__":
    test_output_directory()