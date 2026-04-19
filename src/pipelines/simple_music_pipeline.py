import torch
import time

class SimpleMusicPipeline:
    """
    A simplified music generation pipeline that generates a high-quality,
    loopable 30-second audio clip based on the user's prompt.
    """
    def __init__(self, engine, config, log_stream=None):
        self.engine = engine
        self.config = config
        self.log_stream = log_stream

    def _log(self, message: str, level: str = "INFO"):
        if self.log_stream:
            self.log_stream.log(message, level)

    def run(self, **kwargs):
        """
        Executes the simple generation process respecting the user's prompt.
        """
        self._log("Starting simple music generation.")

        # Use the user's prompt, but ensure 'seamless loop' is included for quality.
        user_prompt = kwargs.get("prompt", "lofi hip hop")
        if "loop" not in user_prompt.lower():
            final_prompt = f"{user_prompt}, seamless loop"
        else:
            final_prompt = user_prompt

        duration = 30  # Fixed duration for simple mode
        temperature = kwargs.get("temperature", 0.9)

        self._log(f"Using user prompt: '{final_prompt}'")
        self._log(f"Duration: {duration}s")
        self._log("Generating step 1/1...")

        audio_tensor, sr = self.engine.generate(
            prompt=final_prompt,
            duration=duration,
            temperature=temperature,
        )

        # Squeeze the tensor to remove the batch dimension.
        audio_tensor_squeezed = audio_tensor.squeeze(0)

        self._log("Generation complete. No fade-out applied to ensure loopability.")
        return {"audio": audio_tensor_squeezed, "sr": sr}
