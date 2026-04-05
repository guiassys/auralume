"""Script para executar a interface Web do Auralith."""

import sys
import os

# Adiciona o diretório raiz do projeto ao path para importar módulos
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from src.web.app import interface

if __name__ == "__main__":
    print("🚀 Iniciando Auralith Studio...")
    print("📱 Acesse: http://localhost:7860")
    print("❌ Pressione Ctrl+C para parar")

    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )