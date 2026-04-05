"""Interface Web para geração de música usando Gradio."""

import gradio as gr
import logging
from typing import Tuple

from src.services.music_service import MusicGenerationService

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instância do serviço
service = MusicGenerationService(output_dir="outputs")


def generate_music_interface(
    name: str,
    duration: int,
    prompt: str
) -> Tuple[str, str]:
    """
    Função principal da interface que conecta UI ao serviço.

    Args:
        name: Nome da música
        duration: Duração selecionada
        prompt: Prompt de estilo

    Returns:
        Tuple: (status_message, file_path_for_download)
    """
    if not prompt.strip():
        return "Erro: Por favor, informe um estilo musical.", None

    if not name.strip():
        name = None  # Usará nome automático

    # Callback para atualizar progresso (usando gr.Info para notificações)
    def progress_callback(message: str):
        gr.Info(message)
        logger.info(message)

    # Executa a geração
    result = service.generate_music(
        name=name,
        duration=duration,
        prompt=prompt,
        progress_callback=progress_callback
    )

    if result['success']:
        return (
            f"✅ Música gerada com sucesso!\nArquivo: {result['file_path']}",
            result['file_path']
        )
    else:
        return f"❌ {result['error']}", None


# Interface Gradio
with gr.Blocks(title="Auralith Studio", theme=gr.themes.Soft()) as interface:
    gr.Markdown("# 🎧 Auralith Studio")
    gr.Markdown("Crie trilhas sonoras Lo-fi personalizadas com IA")

    with gr.Row():
        with gr.Column():
            name_input = gr.Textbox(
                label="Nome da Música (opcional)",
                placeholder="Deixe vazio para nome automático",
                value=""
            )

            duration_input = gr.Dropdown(
                label="Duração (segundos)",
                choices=[30, 60, 90, 180],
                value=180
            )

            prompt_input = gr.Textbox(
                label="Estilo Musical",
                placeholder="Ex: lo-fi hip hop suave, piano Rhodes, progressão Cmaj7-Am7-Dm7-G7, chuva leve...",
                lines=3,
                value="lofi hip hop suave com piano Rhodes, baixo elétrico melódico, progressão Cmaj7-Am7-Dm7-G7, pad analógico e chuva leve"
            )

            generate_btn = gr.Button("🎵 Gerar Música", variant="primary")

        with gr.Column():
            status_output = gr.Textbox(
                label="Status",
                interactive=False,
                lines=5,
                value="Pronto para gerar música!"
            )

            download_output = gr.File(
                label="Download do Arquivo",
                visible=False
            )

    # Conecta o botão à função
    generate_btn.click(
        fn=generate_music_interface,
        inputs=[name_input, duration_input, prompt_input],
        outputs=[status_output, download_output]
    )

    # Torna o download visível quando há arquivo
    def show_download(file_path):
        return gr.update(visible=bool(file_path))

    generate_btn.click(
        fn=show_download,
        inputs=[download_output],
        outputs=[download_output]
    )


if __name__ == "__main__":
    # Executa a interface
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )