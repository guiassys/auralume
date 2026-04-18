import json
import logging
import numpy as np
from typing import Dict, Any, List, Optional

from langchain_core.runnables import RunnableLambda, RunnableSequence

logger = logging.getLogger(__name__)


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

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

    def search(self, query: np.ndarray, k=2):
        if not self.vectors:
            return []

        sims = [
            (i, np.dot(query, v) / (np.linalg.norm(query) * np.linalg.norm(v) + 1e-8))
            for i, v in enumerate(self.vectors)
        ]

        sims.sort(key=lambda x: x[1], reverse=True)
        return [self.metadata[i] for i, _ in sims[:k]]


# -----------------------------
# EMBEDDING PROVIDER (SRP)
# -----------------------------
class EmbeddingProvider:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def embed(self, text: str) -> np.ndarray:
        embedding_size = self.config["generator_settings"]["embedding_size"]
        return np.random.rand(embedding_size)


# -----------------------------
# ARCHITECT (SRP)
# -----------------------------
class MusicArchitect:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def build_structure(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        duration = inputs["duration"]
        logger.info("[ARCHITECT] Designing music structure")

        generator_settings = self.config["generator_settings"]
        structure = generator_settings["structure"]
        bpm_range = generator_settings["bpm_range"]
        keys = generator_settings["keys"]

        bpm = np.random.randint(bpm_range[0], bpm_range[1])
        key = np.random.choice(keys)

        for s in structure:
            s["duration"] = int(duration * s["ratio"])

        return {
            **inputs,
            "structure": structure,
            "bpm": bpm,
            "key": key
        }


# -----------------------------
# COMPOSER (SRP + RAG)
# -----------------------------
class MusicComposer:
    def __init__(
        self,
        vector_store: Optional[SimpleVectorStore] = None,
        embedding_provider: Optional[EmbeddingProvider] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.config = config or load_config()
        self.vector_store = vector_store or SimpleVectorStore()
        self.embedding_provider = embedding_provider or EmbeddingProvider(self.config)

    def compose(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("[COMPOSER] Generating structured prompts")

        sections_output = []
        base_prompt = inputs["prompt"]
        style = inputs["style"]
        bpm = inputs["bpm"]
        key = inputs["key"]

        last_context = ""

        for section in inputs["structure"]:
            embedding = self.embedding_provider.embed(section["name"])

            retrieved = self.vector_store.search(embedding)
            rag_context = " ".join([r["summary"] for r in retrieved])

            section_prompt = self._build_prompt(
                base_prompt,
                section,
                style,
                bpm,
                key,
                last_context,
                rag_context
            )

            summary = f"{section['name']} with {section['desc']}"

            self.vector_store.add(embedding, {"summary": summary})

            sections_output.append({
                "prompt": section_prompt,
                "duration": section["duration"],
                "name": section["name"]
            })

            last_context = summary

        return {
            "sections": sections_output,
            "bpm": bpm,
            "key": key
        }

    def _build_prompt(
        self,
        base_prompt: str,
        section: Dict[str, Any],
        style: str,
        bpm: int,
        key: str,
        last_context: str,
        rag_context: str
    ) -> str:
        return (
            f"{base_prompt}. Section: {section['name']}. "
            f"{section['desc']}. "
            f"BPM: {bpm}. Key: {key}. Style: {style}. "
            f"Previous context: {last_context}. "
            f"Memory: {rag_context}"
        )


# -----------------------------
# PIPELINE (ORCHESTRATOR)
# -----------------------------
class MusicPipeline:

    def __init__(
        self,
        architect: Optional[MusicArchitect] = None,
        composer: Optional[MusicComposer] = None,
    ):
        config = load_config()
        self.architect = architect or MusicArchitect(config)
        self.composer = composer or MusicComposer(config=config)

        self.pipeline = RunnableSequence(
            RunnableLambda(self._architect_stage),
            RunnableLambda(self._composition_stage)
        )

    def build(self, prompt: str, duration: int, style: str):
        return self.pipeline.invoke({
            "prompt": prompt,
            "duration": duration,
            "style": style
        })

    def _architect_stage(self, inputs: Dict[str, Any]):
        return self.architect.build_structure(inputs)

    def _composition_stage(self, inputs: Dict[str, Any]):
        return self.composer.compose(inputs)