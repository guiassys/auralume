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
    """Loads all settings from config.json."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_path, "..", ".."))
    config_path = os.path.join(project_root, "config.json")
    
    default_data = {
        "instruments": ["piano", "jazz piano", "vinyl noise", "soft drums", "electric bass", "pads", "synth"],
        "default_instruments": ["piano", "soft drums"],
        "generator_settings": {
            "bpm": 85, "key": "C minor", "output_dir": "outputs", "output_sufix": "v01_gen", "model_size": "medium",
            "temperature": 1.0, "max_new_tokens": 1500, "chunk_duration": 10,
            "overlap_duration": 2, "fade_in_duration": 1, "fade_out_duration": 1
        },
        "ui_settings": {
            "keys": ["C minor", "A minor", "D major", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],
            "genres": ["Lofi", "Jazz", "Synthwave", "Ambient", "Classical"],
            "moods": ["Calm", "Sad", "Nostalgic", "Warm", "Dreamy", "Chill"],
            "duration": {"min": 30, "max": 300, "step": 10, "default": 60}
        }
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.info(f"Successfully loaded settings from: {config_path}")
                settings = default_data.copy()
                settings.update(data)
                settings["generator_settings"].update(data.get("generator_settings", {}))
                settings["ui_settings"].update(data.get("ui_settings", {}))
                return settings
        except Exception as e:
            logger.error(f"Error reading config.json: {e}")
    else:
        logger.warning(f"Config file not found at: {config_path}. Using defaults.")
    
    return default_data

SETTINGS = load_app_settings()
service = MusicGenerationService()

# --- UI DEFINITION ---
def create_ui():
    """Builds the Gradio Blocks UI for Auralume."""
    with gr.Blocks(theme=auralith_theme, title="Auralume", css=custom_css) as demo:
        # --- Header ---
        with gr.Row(elem_classes=["header"]):
            gr.Markdown("## 🎹 Auralume", elem_id="logo")
        
        with gr.Row():
            # --- Main Workspace ---
            with gr.Column(scale=5):
                with gr.Tabs() as tabs:
                    # --- Tab 1: Track Definitions ---
                    with gr.TabItem("🎵 Track Definitions", id=0):
                        with gr.Group():
                            prompt_input = gr.Textbox(label="Style Prompt", placeholder="e.g., lofi, chill, synthwave, 80s", lines=3)
                        with gr.Row():
                            bpm_input = gr.Slider(label="BPM (Beats Per Minute)", minimum=40, maximum=160, value=SETTINGS["generator_settings"]["bpm"], step=1)
                            duration_input = gr.Slider(
                                label="Duration (s)", 
                                minimum=SETTINGS["ui_settings"]["duration"]["min"], 
                                maximum=SETTINGS["ui_settings"]["duration"]["max"], 
                                step=SETTINGS["ui_settings"]["duration"]["step"], 
                                value=SETTINGS["ui_settings"]["duration"]["default"]
                            )
                        with gr.Row():
                            key_input = gr.Dropdown(label="Key", choices=SETTINGS["ui_settings"]["keys"], value=SETTINGS["generator_settings"]["key"])
                            genre_input = gr.Dropdown(label="Genre", choices=SETTINGS["ui_settings"]["genres"], value=SETTINGS["ui_settings"]["genres"][0])
                            mood_input = gr.Dropdown(label="Mood", choices=SETTINGS["ui_settings"]["moods"], value=SETTINGS["ui_settings"]["moods"][0])
                        instruments_input = gr.CheckboxGroup(label="Instruments", choices=SETTINGS["instruments"], value=SETTINGS["default_instruments"])

                    # --- Tab 2: Settings ---
                    with gr.TabItem("⚙️ Settings", id=1):
                        with gr.Group():
                            gr.Markdown("#### File & Output")
                            with gr.Row():
                                output_dir_input = gr.Textbox(label="Output Directory", value=SETTINGS["generator_settings"]["output_dir"])
                                output_sufix_input = gr.Textbox(label="Output Sufix", value=SETTINGS["generator_settings"]["output_sufix"])
                            with gr.Row():
                                audio_format_input = gr.Radio(label="Audio Format", choices=[".wav", ".mp3"], value=".wav")
                                generate_midi_input = gr.Checkbox(label="Generate MIDI File", value=False)
                        with gr.Group():
                            gr.Markdown("#### Core Generation Parameters")
                            temperature_input = gr.Slider(label="Temperature (Creativity)", minimum=0.1, maximum=2.0, value=SETTINGS["generator_settings"]["temperature"], step=0.05)
                        with gr.Group():
                            gr.Markdown("#### Advanced Model Settings")
                            with gr.Row():
                                model_size_input = gr.Dropdown(label="Model Size", choices=["small", "medium", "large"], value=SETTINGS["generator_settings"]["model_size"])
                                max_new_tokens_input = gr.Slider(label="Max New Tokens", minimum=256, maximum=4096, value=SETTINGS["generator_settings"]["max_new_tokens"], step=128)
                        with gr.Group():
                            gr.Markdown("#### Audio Processing")
                            with gr.Row():
                                chunk_duration_input = gr.Slider(label="Chunk Duration (s)", minimum=5, maximum=30, value=SETTINGS["generator_settings"]["chunk_duration"], step=1)
                                overlap_duration_input = gr.Slider(label="Overlap Duration (s)", minimum=1, maximum=5, value=SETTINGS["generator_settings"]["overlap_duration"], step=1)
                            with gr.Row():
                                fade_in_input = gr.Slider(label="Fade-In (s)", minimum=0, maximum=5, value=SETTINGS["generator_settings"]["fade_in_duration"], step=0.5)
                                fade_out_input = gr.Slider(label="Fade-Out (s)", minimum=0, maximum=5, value=SETTINGS["generator_settings"]["fade_out_duration"], step=0.5)

                    # --- Tab 3: Console & Output ---
                    with gr.TabItem("🖥️ Console", id=2):
                        status_output = gr.Textbox(label="AI Engine Status", lines=15, interactive=False, elem_classes=["terminal-box"])
                        with gr.Row():
                            file_output = gr.File(label="Download Files", visible=False)
                            audio_preview = gr.Audio(label="Master Preview", type="filepath", visible=False)

            # --- Sidebar ---
            with gr.Column(scale=1, min_width=100):
                gr.Markdown("### Actions")
                
                # --- Main Actions ---
                with gr.Column():
                    clear_btn = gr.Button("🗑️ Clear Inputs")
                    generate_btn = gr.Button("🚀 GENERATE", variant="primary")
                    progress_bar = gr.Slider(label="Rendering Progress", value=0, interactive=False, elem_classes=["glowing-progress"], visible=False)

        # --- Event Handling & Logic ---
        def run_generation(
            duration, prompt, genre, mood, instruments, bpm, key,
            output_dir, output_sufix, audio_format, generate_midi, temperature, model_size, max_new_tokens,
            chunk_duration, overlap_duration, fade_in, fade_out
        ):
            if not prompt.strip():
                gr.Warning("Prompt is required.")
                yield { tabs: gr.update(selected=0), status_output: "Error: Prompt is required." }
                return

            yield {
                tabs: gr.update(selected=2), status_output: "Initializing generation...",
                generate_btn: gr.update(interactive=False, value="Generating..."),
                clear_btn: gr.update(interactive=False),
                progress_bar: gr.update(value=0, label="Rendering... 0%", visible=True)
            }

            log_stream, log_history = LogStream(), []
            
            # Generate a timestamp-based name
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            name = f"{timestamp}_{output_sufix}"

            config = {
                "name": name, "duration": duration, "prompt": prompt, "genre": genre, "vibe": mood, 
                "instruments": instruments, "bpm": bpm, "key": key, "output_dir": output_dir, 
                "audio_format": audio_format, "generate_midi": generate_midi, "temperature": temperature, 
                "model_size": model_size, "max_new_tokens": max_new_tokens, "chunk_duration": chunk_duration, 
                "overlap_duration": overlap_duration, "fade_in_duration": fade_in, "fade_out_duration": fade_out
            }

            generation_task_result = {"result": None}
            def generation_task():
                try:
                    generation_task_result["result"] = service.generate_music(config=config, log_stream=log_stream)
                finally:
                    log_stream.end()

            thread = threading.Thread(target=generation_task)
            thread.start()

            for i, log_message in enumerate(log_stream.stream_generator()):
                log_history.append(log_message)
                progress_val = min(0.95, (i + 1) / 25)
                yield {
                    status_output: "\n".join(log_history),
                    progress_bar: gr.update(value=progress_val, label=f"Rendering... {int(progress_val * 100)}%")
                }
                time.sleep(0.1)

            thread.join()
            result = generation_task_result["result"]

            if result and result["success"]:
                log_history.append(f"✅ Generation successful! Output files: {result['files']}")
                yield {
                    status_output: "\n".join(log_history),
                    file_output: gr.update(value=result["files"], visible=True),
                    audio_preview: gr.update(value=result["files"][0], visible=True),
                    generate_btn: gr.update(interactive=True, value="🚀 GENERATE"),
                    clear_btn: gr.update(interactive=True),
                    progress_bar: gr.update(value=1, label="Rendering Complete", visible=False)
                }
            else:
                error_msg = result.get('error', "Unknown error") if result else "Unknown error"
                log_history.append(f"❌ ERROR: {error_msg}")
                gr.Error(f"Generation Failed: {error_msg}")
                yield {
                    status_output: "\n".join(log_history),
                    generate_btn: gr.update(interactive=True, value="🚀 GENERATE"),
                    clear_btn: gr.update(interactive=True),
                    progress_bar: gr.update(value=0, label="Rendering Failed", visible=False)
                }

        all_inputs = [
            duration_input, prompt_input, genre_input, mood_input, instruments_input, bpm_input, key_input,
            output_dir_input, output_sufix_input, audio_format_input, generate_midi_input, temperature_input, model_size_input, max_new_tokens_input,
            chunk_duration_input, overlap_duration_input, fade_in_input, fade_out_input
        ]
        generate_btn.click(fn=run_generation, inputs=all_inputs, outputs=[tabs, status_output, generate_btn, clear_btn, progress_bar, file_output, audio_preview])

        def clear_form():
            return {
                prompt_input: "",
                duration_input: SETTINGS["ui_settings"]["duration"]["default"],
                genre_input: SETTINGS["ui_settings"]["genres"][0],
                mood_input: SETTINGS["ui_settings"]["moods"][0],
                instruments_input: SETTINGS["default_instruments"],
                bpm_input: SETTINGS["generator_settings"]["bpm"],
                key_input: SETTINGS["generator_settings"]["key"],
                output_dir_input: SETTINGS["generator_settings"]["output_dir"],
                output_sufix_input: SETTINGS["generator_settings"]["output_sufix"],
                audio_format_input: ".wav", generate_midi_input: False,
                temperature_input: SETTINGS["generator_settings"]["temperature"],
                model_size_input: SETTINGS["generator_settings"]["model_size"],
                max_new_tokens_input: SETTINGS["generator_settings"]["max_new_tokens"],
                chunk_duration_input: SETTINGS["generator_settings"]["chunk_duration"],
                overlap_duration_input: SETTINGS["generator_settings"]["overlap_duration"],
                fade_in_input: SETTINGS["generator_settings"]["fade_in_duration"],
                fade_out_input: SETTINGS["generator_settings"]["fade_out_duration"],
                status_output: "", file_output: gr.update(visible=False),
                audio_preview: gr.update(visible=False),
                progress_bar: gr.update(value=0, label="Rendering Progress", visible=False),
            }

        clear_outputs = [
            prompt_input, duration_input, genre_input, mood_input, instruments_input, bpm_input, key_input,
            output_dir_input, output_sufix_input, audio_format_input, generate_midi_input, temperature_input, model_size_input, max_new_tokens_input,
            chunk_duration_input, overlap_duration_input, fade_in_input, fade_out_input,
            status_output, file_output, audio_preview, progress_bar
        ]
        clear_btn.click(fn=clear_form, outputs=clear_outputs)

    return demo

# --- Main Execution ---
interface = create_ui()

if __name__ == "__main__":
    interface.launch(server_name="0.0.0.0", server_port=7860, show_error=True)
