"""Interface Web profissional para o Auralith usando Gradio (Compatível com v5/v6)."""

import gradio as gr
import logging
import os
from datetime import datetime
from src.services.music_service import MusicGenerationService

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicialização do Serviço
service = MusicGenerationService(output_dir="outputs")

# Estilização CSS
custom_css = """
.terminal-box textarea { 
    background-color: #0b0f14 !important; 
    color: #00ff41 !important; 
    font-family: 'Courier New', monospace !important; 
    border: 1px solid #182848 !important;
}
.generate-btn { 
    background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%) !important; 
    border: none !important; 
    color: white !important;
    font-weight: bold !important;
}
.main-header { text-align: center; margin-bottom: 20px; }
"""

def create_ui():
    # Removido theme e css daqui para evitar o UserWarning
    with gr.Blocks(title="Auralith Studio") as demo:
        
        gr.Markdown("# 🎧 Auralith AI Music Generator", elem_classes=["main-header"])
        
        with gr.Row():
            # --- PAINEL DE CONTROLE (ESQUERDA) ---
            with gr.Column(scale=2):
                with gr.Group():
                    gr.Markdown("### 🎹 Definições da Track")
                    name_input = gr.Textbox(label="Nome do Projeto", placeholder="Ex: Chill_Rain_Session")
                    prompt_input = gr.Textbox(
                        label="Tema Musical (Prompt)", 
                        placeholder="Ex: lofi, piano, rainy city, nostalgic",
                        lines=3
                    )
                    
                    with gr.Row():
                        duration_input = gr.Dropdown(
                            label="Duração", 
                            choices=[30, 60, 90, 180, 300], 
                            value=60
                        )
                        vibe_input = gr.Dropdown(
                            label="Vibe", 
                            choices=["calm", "sad", "nostalgic", "warm", "dreamy", "chill"], 
                            value="calm"
                        )

                with gr.Group():
                    gr.Markdown("### 🎚️ Ajustes de Estúdio")
                    with gr.Row():
                        bpm_min = gr.Slider(label="BPM Min", minimum=30, maximum=120, value=40, step=1)
                        bpm_max = gr.Slider(label="BPM Max", minimum=30, maximum=140, value=60, step=1)
                    
                    instruments_input = gr.CheckboxGroup(
                        label="Instrumentos",
                        choices=["piano", "jazz piano", "vinyl noise", "soft drums", "electric bass", "pads", "synth"],
                        value=["piano", "soft drums"]
                    )
                    no_abrupt = gr.Checkbox(label="Evitar mudanças bruscas (Smooth Transitions)", value=True)

                with gr.Row():
                    clear_btn = gr.Button("🗑️ Limpar")
                    generate_btn = gr.Button("🎵 GERAR MÚSICA", variant="primary", elem_classes=["generate-btn"])

            # --- PAINEL DE MONITORAMENTO (DIREITA) ---
            with gr.Column(scale=3):
                gr.Markdown("### 🖥️ Studio Console")
                status_output = gr.Textbox(
                    label="Status do Motor de IA",
                    lines=12,
                    interactive=False,
                    elem_classes=["terminal-box"]
                )
                
                # ALTERADO: gr.Box para gr.Group (correção do erro)
                with gr.Group():
                    gr.Markdown("### 📦 Master Output")
                    file_output = gr.File(label="Ficheiro WAV", visible=False)
                    audio_preview = gr.Audio(label="Preview", visible=False)

        # --- LÓGICA DE EXECUÇÃO ---
        def run_generation(name, duration, prompt, b_min, b_max, vibe, inst, abrupt):
            if not prompt.strip():
                return "❌ Erro: Por favor, insira um tema musical.", None, None

            log_history = []
            
            def update_logs(msg):
                timestamp = datetime.now().strftime("%H:%M:%S")
                log_history.append(f"[{timestamp}] {msg}")
                return "\n".join(log_history)

            yield update_logs("Iniciando Pipeline Auralith..."), gr.update(visible=False), gr.update(visible=False)
            
            config = {
                "name": name, "duration": duration, "prompt": prompt,
                "bpm_min": b_min, "bpm_max": b_max, "vibe": vibe,
                "instruments": inst,
                "constraints": ["no abrupt changes", "smooth transitions"] if abrupt else ["smooth transitions"]
            }

            yield update_logs(f"Prompt Gerado: {prompt} | Style: {vibe}"), gr.update(visible=False), gr.update(visible=False)

            result = service.generate_music(
                config=config, 
                progress_callback=lambda m: log_history.append(f"[{datetime.now().strftime('%H:%M:%S')}] {m}")
            )

            if result["success"]:
                final_logs = "\n".join(log_history)
                yield final_logs, gr.update(value=result["file_path"], visible=True), gr.update(value=result["file_path"], visible=True)
            else:
                yield update_logs(f"ERRO: {result['error']}"), gr.update(visible=False), gr.update(visible=False)

        generate_btn.click(
            fn=run_generation,
            inputs=[name_input, duration_input, prompt_input, bpm_min, bpm_max, vibe_input, instruments_input, no_abrupt],
            outputs=[status_output, file_output, audio_preview]
        )

        def clear_form():
            return "", 60, "", 40, 60, "calm", ["piano", "soft drums"], True, "", gr.update(visible=False), gr.update(visible=False)

        clear_btn.click(
            fn=clear_form,
            outputs=[name_input, duration_input, prompt_input, bpm_min, bpm_max, vibe_input, instruments_input, no_abrupt, status_output, file_output, audio_preview]
        )

    return demo

# Define a interface global
interface = create_ui()

# Launch modificado para suportar CSS e Temas corretamente na v6
if __name__ == "__main__":
    interface.launch(
        server_name="0.0.0.0", 
        server_port=7860, 
        show_error=True,
        theme=gr.themes.Soft(primary_hue="blue"),
        css=custom_css
    )