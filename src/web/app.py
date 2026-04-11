"""
Professional Web Interface for Auralith using Gradio with a DAW-inspired,
dark-themed layout and real-time log streaming.
"""
import gradio as gr
import logging
import os
import json
import threading
import time
from src.services.music_service import MusicGenerationService
from src.web.log_stream import LogStream
from src.web.ui_theme import auralith_theme, custom_css

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration Loading ---
def load_app_settings():
    """Loads instrument and default settings from config.json."""
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

# --- UI DEFINITION ---
def create_ui():
    """Builds the Gradio Blocks UI for Auralith Studio."""
    with gr.Blocks(theme=auralith_theme, title="Auralith Studio", css=custom_css) as demo:
        # --- Header ---
        with gr.Row(elem_classes=["header"]):
            gr.Markdown("## 🎹 Auralith Studio", elem_id="logo")
            with gr.Column(scale=3):
                progress_bar = gr.Slider(label="Rendering Progress", value=0, interactive=False, elem_classes=["glowing-progress"])
        
        with gr.Row():
            # --- Sidebar ---
            with gr.Column(scale=1, min_width=100):
                gr.Markdown("### 🛠️ Tools")
                gr.Button("Studio", variant="primary")
                gr.Button("About")
                gr.Button("Help")

            # --- Main Workspace ---
            with gr.Column(scale=5):
                with gr.Tabs() as tabs:
                    # --- Tab 1: Track Definitions ---
                    with gr.TabItem("🎵 Track Definitions", id=0):
                        with gr.Group():
                            name_input = gr.Textbox(label="Project Name", placeholder="e.g., Lofi_Night_Drive")
                            prompt_input = gr.Textbox(label="Style Prompt", placeholder="e.g., lofi, chill, synthwave, 80s", lines=3)
                        with gr.Row():
                            genre_input = gr.Dropdown(label="Genre", choices=["Lofi", "Jazz", "Synthwave", "Ambient", "Classical"], value="Lofi")
                            mood_input = gr.Dropdown(label="Mood", choices=["Calm", "Sad", "Nostalgic", "Warm", "Dreamy", "Chill"], value="Calm")
                        with gr.Row():
                            duration_input = gr.Dropdown(label="Duration (s)", choices=[30, 60, 90, 180, 300], value=60)
                            key_input = gr.Dropdown(label="Key", choices=["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"], value="C")

                    # --- Tab 2: Studio Adjustments ---
                    with gr.TabItem("🎚️ Studio Adjustments", id=1):
                        with gr.Group():
                            gr.Markdown("#### Tempo & Instruments")
                            with gr.Row():
                                bpm_min = gr.Slider(label="BPM Min", minimum=30, maximum=120, value=40, step=1)
                                bpm_max = gr.Slider(label="BPM Max", minimum=30, maximum=140, value=60, step=1)
                            instruments_input = gr.CheckboxGroup(label="Instruments", choices=SETTINGS["instruments"], value=SETTINGS["default_instruments"])
                            no_abrupt = gr.Checkbox(label="Smooth Transitions", value=True)
                        with gr.Group():
                            gr.Markdown("#### Effects (Placeholders)")
                            reverb_slider = gr.Slider(label="Reverb", minimum=0, maximum=1, value=0.2, interactive=True)
                            delay_slider = gr.Slider(label="Delay", minimum=0, maximum=1, value=0.1, interactive=True)
                            compression_slider = gr.Slider(label="Compression", minimum=0, maximum=1, value=0.5, interactive=True)

                    # --- Tab 3: Studio Console & Output ---
                    with gr.TabItem("🖥️ Studio Console", id=2):
                        status_output = gr.Textbox(label="AI Engine Status", lines=15, interactive=False, elem_classes=["terminal-box"])
                        with gr.Row():
                            file_output = gr.File(label="Download WAV", visible=False)
                            audio_preview = gr.Audio(label="Master Preview", type="filepath", visible=False)

        # --- Footer / Main Actions ---
        with gr.Row():
            clear_btn = gr.Button("🗑️ Clear Inputs")
            generate_btn = gr.Button("🚀 GENERATE", variant="primary")

        # --- Event Handling & Logic ---
        def run_generation(name, duration, prompt, bpm_min, bpm_max, mood, instruments, abrupt):
            """Handles the music generation process and UI updates."""
            if not prompt.strip():
                gr.Warning("Prompt is required.")
                yield {
                    tabs: gr.update(selected=2),
                    status_output: "Error: Prompt is required.",
                    generate_btn: gr.update(interactive=True),
                    clear_btn: gr.update(interactive=True),
                }
                return

            # Switch to console tab and lock UI
            yield {
                tabs: gr.update(selected=2),
                status_output: "Initializing generation...",
                generate_btn: gr.update(interactive=False, value="Generating..."),
                clear_btn: gr.update(interactive=False),
                progress_bar: gr.update(value=0, label="Rendering... 0%")
            }

            log_stream = LogStream()
            log_history = []
            
            config = {
                "name": name, "duration": duration, "prompt": prompt,
                "bpm_min": bpm_min, "bpm_max": bpm_max, "vibe": mood,
                "instruments": instruments,
                "constraints": ["no abrupt changes", "smooth transitions"] if abrupt else ["smooth transitions"]
            }

            generation_task_result = {"result": None}
            def generation_task():
                try:
                    result = service.generate_music(config=config, log_stream=log_stream)
                    generation_task_result["result"] = result
                finally:
                    log_stream.end()

            thread = threading.Thread(target=generation_task)
            thread.start()

            # Stream logs and update progress
            total_steps = 25
            for i, log_message in enumerate(log_stream.stream_generator()):
                log_history.append(log_message)
                progress_val = min(0.95, (i + 1) / total_steps)
                progress_label = f"Rendering... {int(progress_val * 100)}%"
                yield {
                    status_output: "\n".join(log_history),
                    progress_bar: gr.update(value=progress_val, label=progress_label)
                }
                time.sleep(0.1)

            thread.join()
            result = generation_task_result["result"]

            # Final UI update
            if result and result["success"]:
                log_history.append(f"✅ Generation successful! Output: {result['file_path']}")
                yield {
                    tabs: gr.update(selected=2),
                    status_output: "\n".join(log_history),
                    file_output: gr.update(value=result["file_path"], visible=True),
                    audio_preview: gr.update(value=result["file_path"], visible=True),
                    generate_btn: gr.update(interactive=True, value="🚀 GENERATE"),
                    clear_btn: gr.update(interactive=True),
                    progress_bar: gr.update(value=1, label="Rendering Complete")
                }
            else:
                error_msg = result.get('error', "An unknown error occurred.") if result else "An unknown error occurred."
                log_history.append(f"❌ ERROR: {error_msg}")
                gr.Error(f"Generation Failed: {error_msg}")
                yield {
                    tabs: gr.update(selected=2),
                    status_output: "\n".join(log_history),
                    generate_btn: gr.update(interactive=True, value="🚀 GENERATE"),
                    clear_btn: gr.update(interactive=True),
                    progress_bar: gr.update(value=0, label="Rendering Failed")
                }

        generate_btn.click(
            fn=run_generation,
            inputs=[name_input, duration_input, prompt_input, bpm_min, bpm_max, mood_input, instruments_input, no_abrupt],
            outputs=[tabs, status_output, generate_btn, clear_btn, progress_bar, file_output, audio_preview]
        )

        def clear_form():
            """Resets all input fields to their default state."""
            return {
                name_input: "",
                prompt_input: "",
                duration_input: 60,
                mood_input: "Calm",
                bpm_min: 40,
                bpm_max: 60,
                instruments_input: SETTINGS["default_instruments"],
                no_abrupt: True,
                status_output: "",
                file_output: gr.update(visible=False),
                audio_preview: gr.update(visible=False),
                progress_bar: gr.update(value=0, label="Rendering Progress"),
                reverb_slider: 0.2,
                delay_slider: 0.1,
                compression_slider: 0.5
            }

        clear_btn.click(fn=clear_form, outputs=[
            name_input, prompt_input, duration_input, mood_input, bpm_min, bpm_max,
            instruments_input, no_abrupt, status_output, file_output, audio_preview, progress_bar,
            reverb_slider, delay_slider, compression_slider
        ])

    return demo

# --- Main Execution ---
interface = create_ui()

if __name__ == "__main__":
    interface.launch(server_name="0.0.0.0", server_port=7860, show_error=True)
