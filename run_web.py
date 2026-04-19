"""Script alternativo para executar a interface Web do Auralume de qualquer diretório."""

import sys
import os
import re

# Adiciona o diretório 'src' ao sys.path para garantir que os módulos sejam encontrados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

def _convert_path_for_wsl(path: str) -> str:
    """Converts a Windows-style path to a WSL-compatible path if necessary."""
    if re.match(r"^[a-zA-Z]:[\\/]", path):
        path = path.replace("\\", "/")
        drive, rest_of_path = path.split(":", 1)
        return f"/mnt/{drive.lower()}{rest_of_path}"
    return path

def main():
    """Função principal para configurar e iniciar a aplicação web."""
    project_root = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(os.path.join(project_root, 'src')):
        print("❌ Erro: Execute este script a partir do diretório raiz do projeto (auralume/).")
        print(f"📁 Diretório atual: {project_root}")
        return

    sys.path.insert(0, project_root)

    try:
        from src.web.app import interface, SETTINGS

        server_settings = SETTINGS.get("server_settings", {})
        server_name = server_settings.get("server_name", "127.0.0.1")
        server_port = server_settings.get("server_port", 7860)
        show_error = server_settings.get("show_error", True)

        # Prepare allowed paths for Gradio
        output_dir_raw = SETTINGS.get("generator_settings", {}).get("output_dir", "outputs")
        allowed_path = _convert_path_for_wsl(output_dir_raw)

        print("🚀 Iniciando Auralume Web...")
        print(f"📱 Acesse: http://{server_name}:{server_port}")
        print("❌ Pressione Ctrl+C para parar")

        interface.launch(
            server_name=server_name,
            server_port=server_port,
            show_error=show_error,
            allowed_paths=[allowed_path]
        )

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Certifique-se de que o ambiente virtual está ativado e as dependências estão instaladas:")
        print("   pip install -r requirements.txt")
    except RuntimeError as e:
        print(f"❌ Erro Crítico na Aplicação: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado ao iniciar a aplicação: {e}")

if __name__ == "__main__":
    main()
