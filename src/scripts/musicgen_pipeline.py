import json
import logging
import numpy as np
import torch
from typing import Dict, Any, List, Optional

from langchain_core.runnables import RunnableLambda, RunnableSequence
from src.scripts.musicgen_engine import MusicGenEngine
from src.web.log_stream import LogStream

logger = logging.getLogger(__name__)

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

# -----------------------------
# AUDIO STITCHER (SRP)
# -----------------------------
class AudioStitcher:
    def __init__(self, config: Dict[str, Any], log_stream: Optional[LogStream] = None):
        self.config = config
        self.generator_settings = config.get("generator_settings", {})
        self._log = self._create_logger(log_stream)

    def _create_logger(self, log_stream: Optional[LogStream]):
        def _log(message: str):
            logger.info(f"[STITCHER] {message}")
            if log_stream:
                log_stream.log(message)
        return _log

    def crossfade_and_append(self, audio1: torch.Tensor, audio2: torch.Tensor, sr: int) -> torch.Tensor:
        overlap_duration = self.generator_settings.get("overlap_duration", 2)
        overlap_samples = int(overlap_duration * sr)
        
        if audio1 is None:
            return audio2

        if audio1.shape[1] < overlap_samples or audio2.shape[1] < overlap_samples:
            self._log("Warning: Audio chunk is smaller than overlap, skipping crossfade.")
            return torch.cat([audio1, audio2], dim=1)

        fade_out = torch.linspace(1, 0, overlap_samples, device=audio1.device, dtype=audio1.dtype).unsqueeze(0)
        fade_in = torch.linspace(0, 1, overlap_samples, device=audio1.device, dtype=audio1.dtype).unsqueeze(0)
        
        crossfaded_part = audio1[:, -overlap_samples:] * fade_out + audio2[:, :overlap_samples] * fade_in
        
        return torch.cat([audio1[:, :-overlap_samples], crossfaded_part, audio2[:, overlap_samples:]], dim=1)

    def apply_fade(self, audio: torch.Tensor, sr: int, fade_type: str, duration_key: str) -> torch.Tensor:
        duration = self.generator_settings.get(duration_key, 1)
        fade_samples = int(duration * sr)
        if fade_samples == 0 or audio is None:
            return audio
        
        if fade_samples > audio.shape[1]:
            fade_samples = audio.shape[1]

        if fade_type == 'in':
            fade = torch.linspace(0, 1, fade_samples, device=audio.device, dtype=audio.dtype).unsqueeze(0)
            audio[:, :fade_samples] *= fade
        elif fade_type == 'out':
            fade = torch.linspace(1, 0, fade_samples, device=audio.device, dtype=audio.dtype).unsqueeze(0)
            audio[:, -fade_samples:] *= fade
        return audio

# -----------------------------
# VECTOR STORE (DIP ready)
# -----------------------------
class SimpleVectorStore:
    def __init__(self):
        self.vectors = []
        self.metadata = []

    def add(self, vector: np.ndarray, meta: dict):
        self.vectors.append(vector)
        self.metadata.append(meta)

    def search(self, query: np.ndarray, k=1):
        if not self.vectors:
            return []
        sims = [(i, np.dot(query, v) / (np.linalg.norm(query) * np.linalg.norm(v) + 1e-8)) for i, v in enumerate(self.vectors)]
        sims.sort(key=lambda x: x[1], reverse=True)
        return [self.metadata[i] for i, _ in sims[:k]]

# -----------------------------
# EMBEDDING PROVIDER (SRP)
# -----------------------------
class EmbeddingProvider:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.embedding_size = config.get("generator_settings", {}).get("embedding_size", 128)

    def embed(self, text: str) -> np.ndarray:
        return np.random.rand(self.embedding_size)

# -----------------------------
# ARCHITECT (SRP)
# -----------------------------
class MusicArchitect:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def build_structure(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        duration = inputs["duration"]
        logger.info("[ARCHITECT] Designing music structure")
        
        arch_settings = self.config["architect_settings"]
        structure_template = arch_settings["structure"]
        
        total_ratio = sum(s["ratio"] for s in structure_template)
        
        for s in structure_template:
            s["duration"] = int(duration * (s["ratio"] / total_ratio))

        return {**inputs, "structure": structure_template}

# -----------------------------
# COMPOSER (SRP + RAG)
# -----------------------------
class MusicComposer:
    def __init__(self, engine: MusicGenEngine, stitcher: AudioStitcher, vector_store: SimpleVectorStore, embedding_provider: EmbeddingProvider, config: Dict[str, Any], log_stream: Optional[LogStream] = None):
        self.engine = engine
        self.stitcher = stitcher
        self.vector_store = vector_store
        self.embedding_provider = embedding_provider
        self.config = config
        self._log = self._create_logger(log_stream)

    def _create_logger(self, log_stream: Optional[LogStream]):
        def _log(message: str):
            logger.info(f"[COMPOSER] {message}")
            if log_stream:
                log_stream.log(message)
        return _log

    def compose(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        self._log("Starting composition process.")
        base_prompt = inputs["prompt"]
        style = inputs.get("style", "") # Style might not be used directly in prompt but good to have
        bpm = inputs["bpm"]
        key = inputs["key"]
        
        full_audio: Optional[torch.Tensor] = None
        last_context = ""
        sr = self.config.get("generator_settings", {}).get("sample_rate", 32000)
        overlap_duration = self.config.get("generator_settings", {}).get("overlap_duration", 2)

        for i, section in enumerate(inputs["structure"]):
            self._log(f"Generating section {i+1}/{len(inputs['structure'])}: {section['name']}")
            
            embedding = self.embedding_provider.embed(section["name"])
            retrieved = self.vector_store.search(embedding)
            rag_context = " ".join([r["summary"] for r in retrieved])

            section_prompt = self._build_prompt(base_prompt, section, style, bpm, key, last_context, rag_context)
            self._log(f"Section prompt: {section_prompt}")

            prompt_audio = None
            if full_audio is not None:
                prompt_context_duration = min(overlap_duration + 1, full_audio.shape[1] / sr)
                prompt_audio = full_audio[:, -int(prompt_context_duration * sr):]

            chunk_audio, _ = self.engine.generate(
                prompt=section_prompt,
                duration=section["duration"],
                prompt_audio=prompt_audio,
                prompt_sr=sr if prompt_audio is not None else None
            )
            
            full_audio = self.stitcher.crossfade_and_append(full_audio, chunk_audio.squeeze(0), sr)
            
            summary = f"{section['name']} with {section['desc']}"
            self.vector_store.add(embedding, {"summary": summary})
            last_context = summary

        return {**inputs, "audio": full_audio, "sr": sr}

    def _build_prompt(self, base_prompt: str, section: Dict[str, Any], style: str, bpm: int, key: str, last_context: str, rag_context: str) -> str:
        return (f"{base_prompt}, {style}. Section: {section['name']}. "
                f"{section['desc']}. BPM: {bpm}. Key: {key}. "
                f"The previous section was: {last_context}. "
                f"Related musical ideas: {rag_context}")

# -----------------------------
# PIPELINE (ORCHESTRATOR)
# -----------------------------
class MusicPipeline:
    def __init__(self, engine: MusicGenEngine, config: Dict[str, Any], log_stream: Optional[LogStream] = None):
        self.config = config
        self.engine = engine
        self.log_stream = log_stream

        # Setup components
        self.architect = MusicArchitect(config)
        stitcher = AudioStitcher(config, log_stream)
        vector_store = SimpleVectorStore()
        embedding_provider = EmbeddingProvider(config)
        self.composer = MusicComposer(engine, stitcher, vector_store, embedding_provider, config, log_stream)

        self.pipeline = RunnableSequence(
            RunnableLambda(self._architect_stage),
            RunnableLambda(self._composition_stage)
        )

    def build(self, prompt: str, duration: int, style: str, bpm: int, key: str) -> Dict[str, Any]:
        return self.pipeline.invoke({
            "prompt": prompt,
            "duration": duration,
            "style": style,
            "bpm": bpm,
            "key": key
        })

    def _architect_stage(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return self.architect.build_structure(inputs)

    def _composition_stage(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return self.composer.compose(inputs)
