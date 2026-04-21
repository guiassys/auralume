"""
Professional Web Interface for Auratune using Gradio with a DAW-inspired,
dark-themed layout and real-time log streaming.
"""
import gradio as gr
import logging
import os
import json
import re
import sys
import threading
import time
from typing import Dict, Any, Tuple, Optional, List

from src.services.music_service import MusicGenerationService
from src.web.log_stream import LogStream
from src.web.ui_theme import auratune_theme, custom_css

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Path Conversion Utility ---
def _convert_path_for_wsl(path: str) -> str:
    """Converts a Windows-style path to a WSL-compatible path if necessary."""
    if re.match(r"^[a-zA-Z]:[\\/]", path):
        path = path.replace("\\", "/")
        drive, rest_of_path = path.split(":", 1)
        return f"/mnt/{drive.lower()}{rest_of_path}"
    return path

# --- Configuration Loading ---
def load_app_settings():
    """
    Loads all settings strictly from config.json.
    If the file is missing or corrupted, it raises a RuntimeError.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_path, "..", ".."))
    config_path = os.path.join(project_root, "config.json")

    if not os.path.exists(config_path):
        raise RuntimeError(f"CRITICAL: Configuration file not found at {config_path}. The application cannot start.")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        raise RuntimeError(f"CRITICAL: Failed to parse or read config.json. Details: {e}")

# --- Main Application Setup ---
try:
    SETTINGS = load_app_settings()
    service = MusicGenerationService()
except RuntimeError as e:
    logger.critical(e)
    sys.exit(1)

# --- UI DEFINITION ---
def create_ui():
    """Builds the Gradio Blocks UI for Auratune."""
    with gr.Blocks(title="Auratune", theme=auratune_theme, css=custom_css) as demo:
        # --- Header ---
        with gr.Row(elem_classes=["header"]):
            gr.Markdown("## 🎹 Auratune", elem_id="logo")

        with gr.Row(elem_id="pipeline-container"):
            pipeline_type_input = gr.Radio(
                label="Pipeline Type",
                choices=["Simple", "Advanced"],
                value="Simple",
                elem_id="pipeline-selector",
                scale=3
            )

        with gr.Row():
            # --- Main Workspace ---
            with gr.Column(scale=5):
                with gr.Tabs() as tabs:
                    # --- Tab 1: Track Definitions ---
                    with gr.TabItem("🎵 Track Definitions", id=0):
                        with gr.Group():
                            with gr.Row():
                                prompt_input = gr.Textbox(label="Style Prompt", placeholder="e.g., lofi, chill, synthwave, 80s", lines=3, scale=3)
                                reference_audio_input = gr.Audio(label="Reference Audio (Optional)", type="filepath", sources=["upload"], scale=1)
                            model_size_input = gr.Dropdown(
                                label="Model Size",
                                choices=SETTINGS["generator_settings"]["model_sizes"],
                                value=SETTINGS["generator_settings"]["default_model_size"]
                            )

                        with gr.Row(visible=False) as advanced_row_1:
                            bpm_min_input = gr.Slider(label="Min BPM", minimum=SETTINGS["ui_settings"]["bpm_range"]["min"], maximum=SETTINGS["ui_settings"]["bpm_range"]["max"], value=SETTINGS["architect_settings"]["bpm_range"][0], step=SETTINGS["ui_settings"]["bpm_range"]["step"])
                            bpm_max_input = gr.Slider(label="Max BPM", minimum=SETTINGS["ui_settings"]["bpm_range"]["min"], maximum=SETTINGS["ui_settings"]["bpm_range"]["max"], value=SETTINGS["architect_settings"]["bpm_range"][1], step=SETTINGS["ui_settings"]["bpm_range"]["step"])
                            duration_input = gr.Slider(
                                label="Duration (s)",
                                minimum=SETTINGS["ui_settings"]["duration"]["min"],
                                maximum=SETTINGS["ui_settings"]["duration"]["max"],
                                step=SETTINGS["ui_settings"]["duration"]["step"],
                                value=SETTINGS["ui_settings"]["duration"]["default"]
                            )
                        with gr.Row(visible=False) as advanced_row_2:
                            key_input = gr.Dropdown(label="Key", choices=SETTINGS["ui_settings"]["keys"], value=SETTINGS["generator_settings"]["key"])
                            genre_input = gr.Dropdown(label="Genre", choices=SETTINGS["ui_settings"]["genres"], value=SETTINGS["ui_settings"]["genres"][0] if SETTINGS["ui_settings"]["genres"] else None)
                            mood_input = gr.Dropdown(label="Mood", choices=SETTINGS["ui_settings"]["moods"], value=SETTINGS["ui_settings"]["moods"][0] if SETTINGS["ui_settings"]["moods"] else None)

                        with gr.Accordion("Music Structure", open=False, visible=False) as advanced_accordion_1:
                            structure_input = gr.Textbox(
                                label="Structure (JSON format)",
                                value=json.dumps(SETTINGS["architect_settings"]["structure"], indent=4),
                                lines=8,
                                elem_id="json-input",
                                interactive=True
                            )

                        with gr.Accordion("Instruments", open=False, visible=False) as advanced_accordion_2:
                            instruments_input = gr.CheckboxGroup(label="Instruments", choices=SETTINGS["instruments"], value=SETTINGS["default_instruments"])

                    # --- Tab 2: Settings ---
                    with gr.TabItem("⚙️ Settings", id=1, visible=False) as settings_tab:
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
                            temperature_input = gr.Slider(label="Temperature (Creativity)", minimum=SETTINGS["ui_settings"]["temperature"]["min"], maximum=SETTINGS["ui_settings"]["temperature"]["max"], value=SETTINGS["generator_settings"]["temperature"], step=SETTINGS["ui_settings"]["temperature"]["step"])
                        with gr.Group():
                            gr.Markdown("#### Advanced Model Settings")
                            with gr.Row():
                                quantization_input = gr.Dropdown(label="Quantization", choices=["none", "8bit", "4bit"], value=SETTINGS["generator_settings"]["quantization"])
                                max_new_tokens_input = gr.Slider(label="Max New Tokens", minimum=SETTINGS["ui_settings"]["max_new_tokens"]["min"], maximum=SETTINGS["ui_settings"]["max_new_tokens"]["max"], value=SETTINGS["generator_settings"]["max_new_tokens"], step=SETTINGS["ui_settings"]["max_new_tokens"]["step"])
                                embedding_size_input = gr.Slider(
                                    label="Embedding Size",
                                    minimum=SETTINGS["ui_settings"]["embedding_size"]["min"],
                                    maximum=SETTINGS["ui_settings"]["embedding_size"]["max"],
                                    value=SETTINGS["generator_settings"]["embedding_size"],
                                    step=SETTINGS["ui_settings"]["embedding_size"]["step"]
                                )
                        with gr.Group(visible=False) as advanced_group_1:
                            gr.Markdown("#### Audio Processing")
                            with gr.Row():
                                chunk_duration_input = gr.Slider(label="Chunk Duration (s)", minimum=SETTINGS["ui_settings"]["chunk_duration_s"]["min"], maximum=SETTINGS["ui_settings"]["chunk_duration_s"]["max"], value=SETTINGS["generator_settings"]["chunk_duration_s"], step=SETTINGS["ui_settings"]["chunk_duration_s"]["step"])
                                continuation_primer_input = gr.Slider(label="Continuation Primer (s)", minimum=SETTINGS["ui_settings"]["continuation_primer_s"]["min"], maximum=SETTINGS["ui_settings"]["continuation_primer_s"]["max"], value=SETTINGS["generator_settings"]["continuation_primer_s"], step=SETTINGS["ui_settings"]["continuation_primer_s"]["step"])
                            with gr.Row():
                                fade_in_input = gr.Slider(label="Fade-In (s)", minimum=SETTINGS["ui_settings"]["fade_in_duration"]["min"], maximum=SETTINGS["ui_settings"]["fade_in_duration"]["max"], value=SETTINGS["generator_settings"]["fade_in_duration"], step=SETTINGS["ui_settings"]["fade_in_duration"]["step"])
                                fade_out_input = gr.Slider(label="Fade-Out (s)", minimum=SETTINGS["ui_settings"]["fade_out_duration"]["min"], maximum=SETTINGS["ui_settings"]["fade_out_duration"]["max"], value=SETTINGS["generator_settings"]["fade_out_duration"], step=SETTINGS["ui_settings"]["fade_out_duration"]["step"])

                    # --- Tab 3: Console & Output ---
                    with gr.TabItem("🖥️ Console", id=2):
                        status_output = gr.Textbox(label="AI Engine Status", lines=15, interactive=False, elem_classes=["terminal-box"])

            # --- Sidebar ---
            with gr.Column(scale=1, min_width=100):
                gr.Markdown("### ⚡ Actions")
                with gr.Column():
                    clear_btn = gr.Button("🗑️ Clear Inputs")
                    generate_btn = gr.Button("🚀 GENERATE", variant="primary")
                    progress_indicator = gr.Textbox(
                        value="",
                        interactive=False,
                        elem_classes=["progress-indicator", "compact"],
                        visible=False,
                        show_label=False
                    )

                with gr.Column(visible=False) as downloads_group:
                    gr.Markdown("### 📂 Downloads")
                    file_output = gr.File(label="Download Files", visible=False)
                    audio_preview = gr.Audio(label="Master Preview", type="filepath", visible=False)

        # --- UI Interaction Logic ---
        def toggle_pipeline_view(pipeline_type: str):
            is_simple = pipeline_type == "Simple"
            visibility = {"visible": not is_simple}
            return {
                advanced_row_1: gr.update(**visibility),
                advanced_row_2: gr.update(**visibility),
                advanced_accordion_1: gr.update(**visibility),
                advanced_accordion_2: gr.update(**visibility),
                settings_tab: gr.update(visible=not is_simple),
                advanced_group_1: gr.update(**visibility),
            }

        pipeline_type_input.change(
            fn=toggle_pipeline_view,
            inputs=[pipeline_type_input],
            outputs=[
                advanced_row_1, advanced_row_2, advanced_accordion_1,
                advanced_accordion_2, settings_tab, advanced_group_1
            ]
        )

        # --- Helper Functions (Scoped within create_ui) ---
        def _validate_inputs(prompt: str) -> Optional[str]:
            if not prompt.strip():
                return "Prompt is required."
            return None

        def _build_generation_config(*args) -> Dict[str, Any]:
            (pipeline_type, duration, prompt, reference_audio, genre, mood, instruments, bpm_min, bpm_max, key,
             embedding_size, output_dir, output_sufix, audio_format, generate_midi,
             temperature, model_size, quantization, max_new_tokens, chunk_duration, continuation_primer,
             fade_in, fade_out, structure_json) = args
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            name = f"{timestamp}_{output_sufix}"

            try:
                structure = json.loads(structure_json)
            except:
                structure = SETTINGS["architect_settings"]["structure"]

            return {
                "pipeline_type": pipeline_type,
                "name": name, "duration": duration, "prompt": prompt, "reference_audio": reference_audio, 
                "genre": genre, "vibe": mood,
                "instruments": instruments, "bpm_range": [bpm_min, bpm_max], "key": key,
                "structure": structure,
                "embedding_size": embedding_size, "output_dir": output_dir,
                "audio_format": audio_format, "generate_midi": generate_midi, "temperature": temperature,
                "model_size": model_size, "quantization": quantization, "max_new_tokens": max_new_tokens,
                "chunk_duration_s": chunk_duration, "continuation_primer_s": continuation_primer,
                "fade_in_duration": fade_in, "fade_out_duration": fade_out
            }

        def _ui_start_generation():
            return {
                tabs: gr.update(selected=2),
                status_output: "Initializing generation...",
                generate_btn: gr.update(interactive=False, value="Generating..."),
                clear_btn: gr.update(interactive=False),
                progress_indicator: gr.update(value="🔄 Rendering... 0%", visible=True),
                downloads_group: gr.update(visible=False),
                file_output: gr.update(value=None, visible=False),
                audio_preview: gr.update(value=None, visible=False)
            }

        def _ui_update_progress(log_history: List[str], current_step: int, total_steps: int):
            progress_val = min(0.95, current_step / total_steps) if total_steps > 0 else 0
            progress_text = f"🔄 Rendering... {int(progress_val * 100)}%"
            return {
                status_output: "\n".join(log_history),
                progress_indicator: gr.update(value=progress_text)
            }

        def _ui_finish_generation(log_history: List[str], result: Dict[str, Any]):
            log_history.append(f"✅ Generation successful! Output files: {result['files']}")
            return {
                status_output: "\n".join(log_history),
                downloads_group: gr.update(visible=True),
                file_output: gr.update(value=result["files"], visible=True),
                audio_preview: gr.update(value=result["files"][0], visible=True),
                generate_btn: gr.update(interactive=True, value="🚀 GENERATE"),
                clear_btn: gr.update(interactive=True),
                progress_indicator: gr.update(value="✅ Rendering Complete", visible=False)
            }

        def _ui_handle_error(log_history: List[str], error_msg: str):
            log_history.append(f"❌ ERROR: {error_msg}")
            gr.Error(f"Generation Failed: {error_msg}")
            return {
                status_output: "\n".join(log_history),
                generate_btn: gr.update(interactive=True, value="🚀 GENERATE"),
                clear_btn: gr.update(interactive=True),
                progress_indicator: gr.update(value="❌ Rendering Failed", visible=False)
            }

        # --- Main Event Handler ---
        def run_generation(
            pipeline_type, duration, prompt, reference_audio, genre, mood, instruments, bpm_min, bpm_max, key,
            embedding_size,
            output_dir, output_sufix, audio_format, generate_midi, temperature, model_size, quantization, max_new_tokens,
            chunk_duration, continuation_primer, fade_in, fade_out, structure_json
        ):
            error = _validate_inputs(prompt)
            if error:
                gr.Warning(error)
                yield {tabs: gr.update(selected=0), status_output: f"Error: {error}"}
                return

            yield _ui_start_generation()

            config_args = (
                pipeline_type, duration, prompt, reference_audio, genre, mood, instruments, bpm_min, bpm_max, key,
                embedding_size, output_dir, output_sufix, audio_format, generate_midi,
                temperature, model_size, quantization, max_new_tokens, chunk_duration, continuation_primer,
                fade_in, fade_out, structure_json
            )
            config = _build_generation_config(*config_args)

            log_stream, log_history = LogStream(), []
            generation_task_result = {"result": None}

            # State for dynamic progress bar
            progress_state = {"current": 0, "total": 1}
            progress_pattern = re.compile(r"Generating step (\d+)/(\d+)")

            def generation_task():
                try:
                    generation_task_result["result"] = service.generate_music(config=config, log_stream=log_stream)
                finally:
                    log_stream.end()

            thread = threading.Thread(target=generation_task)
            thread.start()

            for log_message in log_stream.stream_generator():
                log_history.append(log_message)

                match = progress_pattern.search(log_message)
                if match:
                    progress_state["current"] = int(match.group(1))
                    progress_state["total"] = int(match.group(2))

                # Yielding only the exact elements needed for progress updates
                yield _ui_update_progress(log_history, progress_state["current"], progress_state["total"])
                time.sleep(0.05) # Shorter sleep for responsiveness

            thread.join()
            result = generation_task_result["result"]

            if result and result["success"]:
                yield _ui_finish_generation(log_history, result)
            else:
                error_msg = result.get('error', "Unknown error") if result else "Unknown error"
                yield _ui_handle_error(log_history, error_msg)

        # --- Event Binding ---
        all_inputs = [
            pipeline_type_input,
            duration_input, prompt_input, reference_audio_input, genre_input, mood_input, instruments_input, bpm_min_input, bpm_max_input, key_input,
            embedding_size_input,
            output_dir_input, output_sufix_input, audio_format_input, generate_midi_input, temperature_input, model_size_input, quantization_input, max_new_tokens_input,
            chunk_duration_input, continuation_primer_input, fade_in_input, fade_out_input, structure_input
        ]

        all_outputs = [
            tabs, status_output, generate_btn, clear_btn, progress_indicator, downloads_group, file_output, audio_preview
        ]

        generate_btn.click(fn=run_generation, inputs=all_inputs, outputs=all_outputs)

        def clear_form():
            return {
                prompt_input: "",
                reference_audio_input: None,
                duration_input: SETTINGS["ui_settings"]["duration"]["default"],
                genre_input: SETTINGS["ui_settings"]["genres"][0] if SETTINGS["ui_settings"]["genres"] else None,
                mood_input: SETTINGS["ui_settings"]["moods"][0] if SETTINGS["ui_settings"]["moods"] else None,
                instruments_input: SETTINGS["default_instruments"],
                bpm_min_input: SETTINGS["architect_settings"]["bpm_range"][0],
                bpm_max_input: SETTINGS["architect_settings"]["bpm_range"][1],
                key_input: SETTINGS["generator_settings"]["key"],
                structure_input: json.dumps(SETTINGS["architect_settings"]["structure"], indent=4),
                embedding_size_input: SETTINGS["generator_settings"]["embedding_size"],
                output_dir_input: SETTINGS["generator_settings"]["output_dir"],
                output_sufix_input: SETTINGS["generator_settings"]["output_sufix"],
                audio_format_input: ".wav",
                generate_midi_input: False,
                temperature_input: SETTINGS["generator_settings"]["temperature"],
                model_size_input: SETTINGS["generator_settings"]["default_model_size"],
                quantization_input: SETTINGS["generator_settings"]["quantization"],
                max_new_tokens_input: SETTINGS["generator_settings"]["max_new_tokens"],
                chunk_duration_input: SETTINGS["generator_settings"]["chunk_duration_s"],
                continuation_primer_input: SETTINGS["generator_settings"]["continuation_primer_s"],
                fade_in_input: SETTINGS["generator_settings"]["fade_in_duration"],
                fade_out_input: SETTINGS["generator_settings"]["fade_out_duration"],
                status_output: "",
                downloads_group: gr.update(visible=False),
                file_output: gr.update(value=None, visible=False),
                audio_preview: gr.update(value=None, visible=False),
                progress_indicator: gr.update(value="", visible=False),
            }

        clear_outputs = [
            prompt_input, reference_audio_input, duration_input, genre_input, mood_input, instruments_input,
            bpm_min_input, bpm_max_input, key_input, structure_input, embedding_size_input,
            output_dir_input, output_sufix_input, audio_format_input, generate_midi_input,
            temperature_input, model_size_input, quantization_input, max_new_tokens_input,
            chunk_duration_input, continuation_primer_input, fade_in_input, fade_out_input,
            status_output, downloads_group, file_output, audio_preview, progress_indicator
        ]
        clear_btn.click(fn=clear_form, outputs=clear_outputs)

    return demo

# --- Create the Gradio UI instance ---
interface = create_ui()

# --- Main Execution ---
if __name__ == "__main__":
    server_settings = SETTINGS.get("server_settings", {})

    output_dir_raw = SETTINGS.get("generator_settings", {}).get("output_dir", "outputs")
    allowed_path = _convert_path_for_wsl(output_dir_raw)

    interface.launch(
        server_name=server_settings.get("server_name", "127.0.0.1"),
        server_port=server_settings.get("server_port", 7860),
        show_error=server_settings.get("show_error", True),
        allowed_paths=[allowed_path]
    )
