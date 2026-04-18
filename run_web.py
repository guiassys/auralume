"""Script alternativo para executar a interface Web do Auralume de qualquer diretório."""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

def main():
    # Encontra o diretório raiz do projeto independentemente de onde o script é executado
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Assume que este script está na raiz do projeto
    project_root = current_dir

    # Verifica se estamos no diretório correto procurando por 'src'
    if not os.path.exists(os.path.join(project_root, 'src')):
        print("❌ Erro: Execute este script a partir do diretório raiz do projeto (auralume/)")
        print("📁 Diretório atual:", project_root)
        return

    # Adiciona ao path
    sys.path.insert(0, project_root)

    try:
        from src.web.app import interface
        print("🚀 Iniciando Auralume Web...")
        print("📱 Acesse: http://localhost:7860")
        print("❌ Pressione Ctrl+C para parar")

        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            show_error=True
        )
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Certifique-se de que todas as dependências estão instaladas:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()