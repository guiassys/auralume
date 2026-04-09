import logging
import numpy as np
from typing import Dict, Any, List
from langchain_core.runnables import RunnableLambda, RunnableSequence

logger = logging.getLogger(__name__)


class SimpleVectorStore:
    """Lightweight FAISS-like store (pluggable futuramente)"""

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


class MusicPipeline:

    def __init__(self):
        self.vector_store = SimpleVectorStore()

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

    # -----------------------------
    # STAGE 1 - ARCHITECT
    # -----------------------------
    def _architect_stage(self, inputs: Dict[str, Any]):

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
    # STAGE 2 - COMPOSITION + RAG
    # -----------------------------
    def _composition_stage(self, inputs: Dict[str, Any]):

        logger.info("[COMPOSER] Generating structured prompts")

        sections_output = []
        base_prompt = inputs["prompt"]
        style = inputs["style"]
        bpm = inputs["bpm"]
        key = inputs["key"]

        last_context = ""

        for section in inputs["structure"]:

            # fake embedding (placeholder para CLAP)
            embedding = np.random.rand(128)

            retrieved = self.vector_store.search(embedding)

            rag_context = " ".join([r["summary"] for r in retrieved])

            section_prompt = (
                f"{base_prompt}. Section: {section['name']}. "
                f"{section['desc']}. "
                f"BPM: {bpm}. Key: {key}. Style: {style}. "
                f"Previous context: {last_context}. "
                f"Memory: {rag_context}"
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