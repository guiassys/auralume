import logging
import numpy as np
from typing import Dict, Any, List, Optional

from langchain_core.runnables import RunnableLambda, RunnableSequence

logger = logging.getLogger(__name__)


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
    def embed(self, text: str) -> np.ndarray:
        return np.random.rand(128)


# -----------------------------
# ARCHITECT (SRP)
# -----------------------------
class MusicArchitect:
    def build_structure(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        duration = inputs["duration"]

        logger.info("[ARCHITECT] Designing music structure")

        structure = [
            {"name": "intro", "ratio": 0.1, "desc": "minimal, buildup, soft textures"},
            {"name": "verse", "ratio": 0.4, "desc": "groove, melodic progression"},
            {"name": "chorus", "ratio": 0.35, "desc": "full energy, layered, emotional"},
            {"name": "outro", "ratio": 0.15, "desc": "fading out, decay, resolution"},
        ]

        bpm = np.random.randint(70, 90)
        key = np.random.choice(["C minor", "A minor", "D major"])

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
    ):
        self.vector_store = vector_store or SimpleVectorStore()
        self.embedding_provider = embedding_provider or EmbeddingProvider()

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
        self.architect = architect or MusicArchitect()
        self.composer = composer or MusicComposer()

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