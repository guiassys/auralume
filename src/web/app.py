"""Interface Web para geração de música usando Gradio (Prompt Structured Version)."""

import gradio as gr
import logging
from typing import Tuple, Dict, Any

from src.services.music_service import MusicGenerationService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

service = MusicGenerationService(output_dir="outputs")


# -----------------------------
# PROMPT BUILDER (FRONTEND)
# -----------------------------
def build_config(
    name: str,
    duration: int,
    prompt: str,
    bpm_min: int,
    bpm_max: int,
    vibe: str,
    instruments: list,
    no_abrupt_changes: bool
) -> Dict[str, Any]:

    return {
        "name": name.strip() if name.strip() else None,
        "duration": duration,
        "prompt": prompt.strip(),
        "style": "lo-fi hip hop",
        "bpm_min": bpm_min,
        "bpm_max": bpm_max,
        "vibe": vibe,
        "instruments": instruments,
        "constraints": (
            ["no abrupt changes", "smooth transitions"]
            if no_abrupt_changes else
            ["smooth transitions"]
        )
    }


# -----------------------------
# MAIN GENERATION FUNCTION
# -----------------------------
def generate_music_interface(
    name: str,
    duration: int,
    prompt: str,
    bpm_min: int,
    bpm_max: int,
    vibe: str,
    instruments: list,
    no_abrupt_changes: bool
) -> Tuple[str, str]:

    if not prompt.strip():
        return "❌ Erro: informe um tema musical.", None

    config = build_config(
        name=name,
        duration=duration,
        prompt=prompt,
        bpm_min=bpm_min,
        bpm_max=bpm_max,
        vibe=vibe,
        instruments=instruments,
        no_abrupt_changes=no_abrupt_changes
    )

    def progress_callback(message: str):
        gr.Info(message)
        logger.info(message)

    result = service.generate_music(
        config=config,
        progress_callback=progress_callback
    )

    if result["success"]:
        return (
            f"✅ Música gerada com sucesso!\nArquivo: {result['file_path']}",
            result["file_path"]
        )
    else:
        return f"❌ Erro: {result['error']}", None


# -----------------------------
# UI (DAW-STYLE CONTROL PANEL)
# -----------------------------
with gr.Blocks(title="Auralith Web", theme=gr.themes.Soft()) as interface:

    gr.Markdown("# 🎧 Auralith AI Music Generator")
    gr.Markdown("Gere músicas com controle musical estruturado (tipo DAW simplificada).")

    with gr.Row():

        # ---------------- LEFT PANEL ----------------
        with gr.Column():

            name_input = gr.Textbox(
                label="Nome da Música",
                placeholder="Opcional"
            )

            prompt_input = gr.Textbox(
                label="Tema Musical",
                placeholder="Ex: lofi study, chill night, rainy city",
                lines=2
            )

            duration_input = gr.Dropdown(
                label="Duração (segundos)",
                choices=[30, 60, 90, 180, 300],
                value=180
            )

            bpm_min = gr.Slider(
                label="BPM mínimo",
                minimum=30,
                maximum=120,
                value=40,
                step=1
            )

            bpm_max = gr.Slider(
                label="BPM máximo",
                minimum=30,
                maximum=140,
                value=60,
                step=1
            )

            vibe_input = gr.Dropdown(
                label="Vibe",
                choices=[
                    "calm",
                    "sad",
                    "nostalgic",
                    "warm",
                    "dreamy",
                    "chill"
                ],
                value="calm"
            )

            instruments_input = gr.CheckboxGroup(
                label="Instrumentos (opcional)",
                choices=[
                    "piano",
                    "jazz piano",
                    "vinyl noise",
                    "soft drums",
                    "electric bass",
                    "pads",
                    "synth"
                ],
                value=["piano", "soft drums"]
            )

            no_abrupt_changes = gr.Checkbox(
                label="Evitar mudanças bruscas (recomendado)",
                value=True
            )

            generate_btn = gr.Button("🎵 Gerar Música", variant="primary")

        # ---------------- RIGHT PANEL ----------------
        with gr.Column():

            status_output = gr.Textbox(
                label="Status",
                interactive=False,
                lines=6
            )

            download_output = gr.File(
                label="Download",
                visible=False
            )

    # -----------------------------
    # EVENT
    # -----------------------------
    generate_btn.click(
        fn=generate_music_interface,
        inputs=[
            name_input,
            duration_input,
            prompt_input,
            bpm_min,
            bpm_max,
            vibe_input,
            instruments_input,
            no_abrupt_changes
        ],
        outputs=[
            status_output,
            download_output
        ]
    )

    # show download when file exists
    def show_download(file_path):
        return gr.update(visible=bool(file_path))

    generate_btn.click(
        fn=show_download,
        inputs=[download_output],
        outputs=[download_output]
    )


# -----------------------------
# LAUNCH
# -----------------------------
if __name__ == "__main__":
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )