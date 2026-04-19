import json
import logging
import numpy as np
import torch
from typing import Dict, Any, Optional

from langchain_core.runnables import RunnableLambda, RunnableSequence
from src.pipelines.musicgen_engine import MusicGenEngine
from src.web.log_stream import LogStream

logger = logging.getLogger(__name__)

# -----------------------------
# AUDIO STITCHER
# -----------------------------
class AudioStitcher:
    def __init__(self, config: Dict[str, Any], log_stream: Optional[LogStream] = None):
        self.config = config
        self._log = self._create_logger(log_stream)

    def _create_logger(self, log_stream: Optional[LogStream]):
        def _log(message: str):
            logger.info(f"[STITCHER] {message}")
            if log_stream: log_stream.log(message)
        return _log

    def stitch(self, audio1: Optional[torch.Tensor], audio2: torch.Tensor, primer_samples: int) -> torch.Tensor:
        """
        Concatenates audio chunks cleanly.
        MusicGen's output `audio2` starts with the `primer` audio we fed it.
        We simply strip those exact primer samples from `audio2` and append the rest to `audio1`.
        This guarantees perfect sample-level continuity without phase cancellation or noise.
        """
        if audio1 is None: 
            return audio2
            
        if primer_samples > 0 and audio2.shape[1] > primer_samples:
            new_generated_audio = audio2[:, primer_samples:]
            return torch.cat([audio1, new_generated_audio], dim=1)
        else:
            return torch.cat([audio1, audio2], dim=1)

# -----------------------------
# ARCHITECT
# -----------------------------
class MusicArchitect:
    def __init__(self, config: Dict[str, Any], log_stream: Optional[LogStream] = None):
        self.config = config
        self.generator_settings = config.get("generator_settings", {})
        self._log = self._create_logger(log_stream)

    def _create_logger(self, log_stream: Optional[LogStream]):
        def _log(message: str, level: str = "INFO"):
            logger.info(f"[ARCHITECT] {message}")
            if log_stream: log_stream.log(message, level)
        return _log

    def build_structure(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        duration = inputs["duration"]
        self._log(f"Designing music structure for {duration}s.")
        
        structure_template = self.config.get("architect_settings", {}).get("structure", [])
        
        # To avoid pushing MusicGen beyond its ~30s context window comfortably,
        # we aim for chunks of ~20s new audio.
        chunk_duration = self.generator_settings.get("chunk_duration_s", 20)
        
        if not structure_template:
            num_chunks = int(np.ceil(duration / chunk_duration))
            final_structure = [{"name": f"segment_{i+1}", "duration": min(chunk_duration, duration - i * chunk_duration), "desc": ""} for i in range(num_chunks)]
        else:
            total_ratio = sum(s.get("ratio", 0) for s in structure_template)
            
            # Create sub-chunks if a section is too long
            final_structure = []
            for s in structure_template:
                sec_duration = int(duration * s.get("ratio", 0) / total_ratio) if total_ratio > 0 else 0
                if sec_duration <= 0: continue
                
                num_sub_chunks = int(np.ceil(sec_duration / chunk_duration))
                for i in range(num_sub_chunks):
                    sub_dur = min(chunk_duration, sec_duration - i * chunk_duration)
                    if sub_dur <= 0: continue
                    final_structure.append({
                        "name": f"{s['name']}_{i+1}",
                        "duration": sub_dur,
                        "desc": s.get("desc", "")
                    })

        inputs["structure"] = final_structure
        self._log(f"Structure created with {len(final_structure)} steps: {[s['name'] for s in final_structure]}")
        return inputs

# -----------------------------
# COMPOSER
# -----------------------------
class MusicComposer:
    def __init__(self, engine: MusicGenEngine, stitcher: AudioStitcher, log_stream: Optional[LogStream] = None):
        self.engine = engine
        self.stitcher = stitcher
        self._log = self._create_logger(log_stream)

    def _create_logger(self, log_stream: Optional[LogStream]):
        def _log(message: str, level: str = "INFO"):
            logger.info(f"[COMPOSER] {message}")
            if log_stream: log_stream.log(message, level)
        return _log

    def compose(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        self._log("Starting composition process.")
        
        # MusicGen responds best to simple, comma-separated stylistic tags.
        # We avoid sentences and keep it purely descriptive.
        base_style_parts = [
            inputs.get("prompt"),
            inputs.get("genre"),
            inputs.get("vibe")
        ]
        
        # Only add instruments if they are explicitly selected
        instruments = inputs.get("instruments", [])
        if instruments:
            base_style_parts.extend(instruments) # Extend, not append a single joined string

        base_style_prompt = ", ".join(filter(None, base_style_parts))

        full_audio: Optional[torch.Tensor] = None
        sr = self.engine.config.sample_rate
        use_continuation = inputs.get("use_continuation", True)
        primer_duration_s = inputs.get("continuation_primer_s", 5) # 5 seconds gives strong rhythmic context
        
        user_prompt_audio = inputs.get("prompt_audio")
        user_prompt_sr = inputs.get("prompt_sr")

        num_sections = len(inputs["structure"])
        for i, section in enumerate(inputs["structure"]):
            self._log(f"Generating step {i+1}/{num_sections}: {section['name']} ({section['duration']}s)")
            
            # Combine base style with the specific section description
            section_prompt_parts = [base_style_prompt]
            if section.get("desc"):
                section_prompt_parts.append(section.get("desc"))
                
            current_prompt = ", ".join(filter(None, section_prompt_parts))
            
            prompt_audio, prompt_sr = None, None
            primer_samples = 0
            
            # For the first chunk, use the user's reference audio if provided.
            if i == 0 and user_prompt_audio is not None:
                prompt_audio = user_prompt_audio
                prompt_sr = user_prompt_sr
                self._log("Using user reference audio for initial context.")
            # For subsequent chunks, use the stitched generated audio as continuation
            # This counts as `prompt_audio` iterative conditional generation.
            # In order to support `use_cache=False` securely down the line and not crash GPU
            elif use_continuation and full_audio is not None:
                primer_samples = int(primer_duration_s * sr)
                if full_audio.shape[1] > primer_samples:
                    prompt_audio = full_audio[:, -primer_samples:]
                    prompt_sr = sr
                    self._log(f"Using {primer_duration_s}s primer to maintain context.")
                else:
                    self._log("Warning: Previous audio is too short for priming.", level="WARNING")
                    primer_samples = 0

            self._log(f"Prompt: '{current_prompt}'")
            
            chunk_audio, _ = self.engine.generate(
                prompt=current_prompt,
                duration=section["duration"],
                prompt_audio=prompt_audio,
                prompt_sr=prompt_sr,
                temperature=inputs.get("temperature", 0.90) # Slightly reduced temperature for consistency
            )
            
            chunk_audio_clean = chunk_audio.squeeze(0)
            
            # Stitch the audio perfectly by removing the primer overlap
            full_audio = self.stitcher.stitch(full_audio, chunk_audio_clean, primer_samples)

            self._log(f"Step {i+1} complete. Total generated: {full_audio.shape[1]/sr:.2f}s.")

        return {**inputs, "audio": full_audio, "sr": sr}

# -----------------------------
# PIPELINE
# -----------------------------
class MusicPipeline:
    def __init__(self, engine: MusicGenEngine, config: Dict[str, Any], log_stream: Optional[LogStream] = None):
        self.engine = engine
        self.config = config
        self.log_stream = log_stream

        self.architect = MusicArchitect(config, log_stream)
        stitcher = AudioStitcher(config, log_stream)
        self.composer = MusicComposer(engine, stitcher, log_stream)

        self.pipeline = RunnableSequence(
            RunnableLambda(self.architect.build_structure),
            RunnableLambda(self.composer.compose)
        )

    def build(self, **kwargs) -> Dict[str, Any]:
        return self.pipeline.invoke(kwargs)
