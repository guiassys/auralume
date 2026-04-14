"""
A dedicated script for audio-to-MIDI transcription using Basic Pitch.
This script is designed to be called from a separate Python environment
to avoid dependency conflicts.
"""
import sys
import os
import logging
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [TRANSCRIBER] - %(levelname)s - %(message)s')

def transcribe_audio_to_midi(audio_path: str):
    """
    Transcribes a single audio file to a MIDI file in the same directory.

    Args:
        audio_path (str): The absolute path to the input audio file.
    """
    if not os.path.exists(audio_path):
        logging.error(f"Input audio file not found: {audio_path}")
        sys.exit(1)

    output_directory = os.path.dirname(audio_path)
    
    logging.info(f"Starting transcription for: {os.path.basename(audio_path)}")
    logging.info(f"Output directory: {output_directory}")

    try:
        # This function saves the file to disk and does not return anything
        # when only saving is requested.
        predict_and_save(
            audio_path_list=[audio_path],
            model_or_model_path=ICASSP_2022_MODEL_PATH,
            output_directory=output_directory,
            save_midi=True,
            sonify_midi=False,
            save_model_outputs=False,
            save_notes=False,
        )
        
        # The library saves the file with a "_basic_pitch" suffix.
        # Let's rename it to match the original audio file's name for consistency.
        original_midi_path = os.path.join(output_directory, os.path.basename(audio_path).rsplit('.', 1)[0] + "_basic_pitch.mid")
        final_midi_path = os.path.join(output_directory, os.path.basename(audio_path).rsplit('.', 1)[0] + ".mid")

        if os.path.exists(original_midi_path):
            os.rename(original_midi_path, final_midi_path)
            logging.info(f"Successfully created and renamed MIDI file to: {os.path.basename(final_midi_path)}")
            sys.exit(0)
        else:
            logging.error(f"MIDI file was not created at the expected path: {original_midi_path}")
            sys.exit(1)

    except Exception as e:
        logging.error(f"An unexpected error occurred during transcription: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <path_to_audio_file>")
        sys.exit(1)
    
    input_audio_path = sys.argv[1]
    transcribe_audio_to_midi(input_audio_path)