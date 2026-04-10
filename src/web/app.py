"""Professional Web Interface for Auralith using Gradio with Real-Time Log Streaming."""

import gradio as gr
import logging
import os
import json
import threading
from src.services.music_service import MusicGenerationService
from src.web.log_stream import LogStream

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- CONFIGURATION LOADING ---
def load_app_settings():
    base_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_path, "..", ".."))
    config_path = os.path.join(project_root, "config.json")
    
    default_data = {
        "instruments": ["piano", "jazz piano", "vinyl noise", "soft drums", "electric bass", "pads", "synth"],
        "default_instruments": ["piano", "soft drums"]
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.info(f"Successfully loaded settings from: {config_path}")
                return {
                    "instruments": list(data.get("instruments", default_data["instruments"])),
                    "default_instruments": list(data.get("default_instruments", default_data["default_instruments"]))
                }
        except Exception as e:
            logger.error(f"Error reading config.json: {e}")
    else:
        logger.warning(f"Config file not found at: {config_path}. Using defaults.")
    
    return default_data

SETTINGS = load_app_settings()
service = MusicGenerationService(output_dir="outputs")

# --- UI STYLING ---
custom_css = """
.terminal-box textarea { background-color: #0b0f14 !important; color: #00ff41 !important; font-family: 'Courier New', monospace !important; border: 1px solid #182848 !important; }
.generate-btn { background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%) !important; border: none !important; color: white !important; font-weight: bold !important; }
.main-header { text-align: center; margin-bottom: 20px; }
"""

# --- UI DEFINITION ---
def create_ui():
    with gr.Blocks(title="Auralith Studio", css=custom_css) as demo:
        gr.Markdown("# 🎧 Auralith AI Music Generator", elem_classes=["main-header"])
        
        with gr.Row():
            with gr.Column(scale=2):
                with gr.Group():
                    gr.Markdown("### 🎹 Track Definitions")
                    name_input = gr.Textbox(label="Project name", placeholder="Ex: Chill_Rain_Session")
                    prompt_input = gr.Textbox(label="Musical Theme (Prompt)", placeholder="Ex: lofi, piano, rainy city, nostalgic", lines=3)
                    with gr.Row():
                        duration_input = gr.Dropdown(label="Duration (seconds)", choices=[30, 60, 90, 180, 300], value=60)
                        vibe_input = gr.Dropdown(label="Vibe", choices=["calm", "sad", "nostalgic", "warm", "dreamy", "chill"], value="calm")

                with gr.Group():
                    gr.Markdown("### 🎚️ Studio Adjustments")
                    with gr.Row():
                        bpm_min = gr.Slider(label="BPM Min", minimum=30, maximum=120, value=40, step=1)
                        bpm_max = gr.Slider(label="BPM Max", minimum=30, maximum=140, value=60, step=1)
                    instruments_input = gr.CheckboxGroup(label="Instruments", choices=SETTINGS["instruments"], value=SETTINGS["default_instruments"])
                    no_abrupt = gr.Checkbox(label="Avoiding abrupt changes (Smooth Transitions)", value=True)

                with gr.Row():
                    clear_btn = gr.Button("🗑️ Clean")
                    generate_btn = gr.Button("🎵 GENERATE MUSIC", variant="primary", elem_classes=["generate-btn"])

            with gr.Column(scale=3):
                gr.Markdown("### 🖥️ Studio Console")
                status_output = gr.Textbox(label="AI Engine Status", lines=12, interactive=False, elem_classes=["terminal-box"])
                with gr.Group():
                    gr.Markdown("### 📦 Master Output")
                    file_output = gr.File(label="WAV File", visible=False)
                    audio_preview = gr.Audio(label="Preview", visible=False)

        # --- EXECUTION LOGIC ---
        def run_generation(name, duration, prompt, b_min, b_max, vibe, inst, abrupt):
            if not prompt.strip():
                yield "❌ Error: Please enter a musical theme.", gr.update(visible=False), gr.update(visible=False), gr.update(interactive=True)
                return

            yield "Starting...", gr.update(visible=False), gr.update(visible=False), gr.update(interactive=False)

            log_stream = LogStream()
            log_history = []
            
            config = {
                "name": name, "duration": duration, "prompt": prompt,
                "bpm_min": b_min, "bpm_max": b_max, "vibe": vibe,
                "instruments": inst,
                "constraints": ["no abrupt changes", "smooth transitions"] if abrupt else ["smooth transitions"]
            }

            # This function will run in a separate thread
            def generation_task():
                try:
                    result = service.generate_music(config=config, log_stream=log_stream)
                    # Store result in a shared object to be retrieved later
                    generation_task.result = result
                finally:
                    log_stream.end()

            generation_task.result = None
            thread = threading.Thread(target=generation_task)
            thread.start()

            # Stream logs to the UI from the main thread
            for log_message in log_stream.stream_generator():
                log_history.append(log_message)
                yield "\n".join(log_history), gr.update(visible=False), gr.update(visible=False), gr.update(interactive=False)

            thread.join() # Ensure the thread is finished
            result = generation_task.result

            if result and result["success"]:
                yield (
                    "\n".join(log_history),
                    gr.update(value=result["file_path"], visible=True),
                    gr.update(value=result["file_path"], visible=True),
                    gr.update(interactive=True)
                )
            else:
                error_message = result['error'] if result else "An unknown error occurred."
                log_history.append(f"[ERROR] {error_message}")
                yield (
                    "\n".join(log_history),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(interactive=True)
                )

        generate_btn.click(
            fn=run_generation,
            inputs=[name_input, duration_input, prompt_input, bpm_min, bpm_max, vibe_input, instruments_input, no_abrupt],
            outputs=[status_output, file_output, audio_preview, generate_btn]
        )

        def clear_form():
            return "", 60, "", 40, 60, "calm", SETTINGS["default_instruments"], True, "", gr.update(visible=False), gr.update(visible=False), gr.update(interactive=True)

        clear_btn.click(
            fn=clear_form,
            outputs=[name_input, duration_input, prompt_input, bpm_min, bpm_max, vibe_input, instruments_input, no_abrupt, status_output, file_output, audio_preview, generate_btn]
        )

    return demo

interface = create_ui()

if __name__ == "__main__":
    interface.launch(server_name="0.0.0.0", server_port=7860, show_error=True)