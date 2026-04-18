"""Script alternativo para executar a interface Web do Auralume de qualquer diretório."""

import sys
import os

# Adiciona o diretório 'src' ao sys.path para garantir que os módulos sejam encontrados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

def main():
    """Função principal para configurar e iniciar a aplicação web."""
    # Encontra o diretório raiz do projeto
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Verifica se o script está sendo executado do lugar certo
    if not os.path.exists(os.path.join(project_root, 'src')):
        print("❌ Erro: Execute este script a partir do diretório raiz do projeto (auralume/).")
        print(f"📁 Diretório atual: {project_root}")
        return

    # Adiciona a raiz do projeto ao path para importações relativas
    sys.path.insert(0, project_root)

    try:
        # Importa a interface e as configurações do módulo da aplicação
        from src.web.app import interface, SETTINGS

        server_settings = SETTINGS.get("server_settings", {})
        server_name = server_settings.get("server_name", "127.0.0.1")
        server_port = server_settings.get("server_port", 7860)
        show_error = server_settings.get("show_error", True)

        print("🚀 Iniciando Auralume Web...")
        print(f"📱 Acesse: http://{server_name}:{server_port}")
        print("❌ Pressione Ctrl+C para parar")

        # Inicia a interface Gradio com as configurações carregadas
        interface.launch(
            server_name=server_name,
            server_port=server_port,
            show_error=show_error
        )

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Certifique-se de que o ambiente virtual está ativado e as dependências estão instaladas:")
        print("   pip install -r requirements.txt")
    except RuntimeError as e:
        # Captura erros críticos de configuração (ex: config.json ausente)
        print(f"❌ Erro Crítico na Aplicação: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado ao iniciar a aplicação: {e}")

if __name__ == "__main__":
    main()
