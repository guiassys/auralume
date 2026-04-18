# 🚀 Prompt: Holistic Refactoring for Quality and Coherence

## 🧠 Persona

As an expert AI Software Architect, my role is to analyze the existing Auralume application, identify architectural inconsistencies and opportunities for improvement, and propose a detailed refactoring plan. The primary goal is to enhance the quality, coherence, and length of the generated music while improving code maintainability, performance, and user experience.

---

## 🌍 Context

The user wants to improve the Auralume application to generate high-quality, coherent music up to 3 minutes long. The current implementation suffers from **critical context loss** in longer tracks, where each segment is generated independently, causing the music to lose its identity. This is a direct result of a naive chunking strategy.

This plan outlines a holistic refactoring process to address these issues, focusing on activating an advanced generation pipeline that uses an **Audio Continuation** strategy to maintain musical coherence.

---

## 🎯 Primary Objective

Refactor the Auralume application to:
1.  **Generate High-Coherence Music:** Produce musically consistent tracks up to 3 minutes long by implementing an **audio continuation (priming)** strategy. This solves the core problem of context loss.
2.  **Unify the Architecture:** Eliminate the redundant, simple generation pipeline in favor of the advanced, structure-aware pipeline.
3.  **Optimize Performance:** Improve application startup time and reduce GPU memory consumption through techniques like lazy loading and quantization.
4.  **Enhance Code Quality:** Ensure the codebase adheres to best practices, including the Single Responsibility Principle (SRP) and full configuration-driven behavior (no hardcoding).

---

## ⚠️ Hard Constraints

### ✅ Must Preserve
- All existing UI functionalities, including logging, monitoring, and progress bar updates.
- The application must continue to be driven by the `config.json` file.
- The ability to handle both Windows and Linux style paths for the output directory must be maintained.

### ❌ Forbidden
- Do not break existing core features.
- Do not introduce new hardcoded parameters; all configurations must be sourced from `config.json`.
- Do not remove the "fail-fast" approach for `config.json` loading.

---

## 💡 Key Technical Directives (Prioritized)

1.  **Architectural Unification:** The most critical issue is the dual-pipeline architecture. The simple, naive continuation loop in `TrackGenerator` is the root cause of context loss. The advanced, structure-aware pipeline (`MusicPipeline`, `MusicArchitect`, `MusicComposer`) is the solution. **Our top priority is to make this advanced pipeline the primary engine for music generation.**

2.  **Long-Term Context Management (Audio Continuation):** The key to coherence is **audio continuation**, not just text-prompt continuation. The correct approach is to use the end of the previously generated clip as a "primer" for the next one.
    *   **Mechanism:** The `MusicComposer` will orchestrate this. For a 180s track with 30s chunks:
        1.  **Chunk 1 (0-30s):** Generated from the initial text prompt.
        2.  **Primer (28-30s):** The last `continuation_primer_s` (e.g., 2 seconds) of Chunk 1 are extracted.
        3.  **Chunk 2 (30-58s):** Generated using the 2-second audio primer as the primary prompt. This ensures the model continues the melody, harmony, and rhythm.
        4.  **Stitching:** The new 28-second segment is appended to the first 30s chunk.
        5.  This process repeats until the total duration is reached.
    *   **Configuration:** This behavior must be controlled via `config.json`. We will introduce `use_continuation: true` and `continuation_primer_s: 2` to `generator_settings`.

3.  **Performance Optimization:**
    *   **Lazy Loading:** The MusicGen model should not be loaded into VRAM on application startup. It should be loaded only on the first generation request to ensure a fast startup and efficient resource management.
    *   **Quantization:** To handle long generation tasks and reduce memory footprint, we should add support for model quantization (e.g., 8-bit) as a configurable option.

4.  **Configuration and UI Enhancements:**
    *   The UI must be adapted to fully support the advanced pipeline. This includes providing clear controls for structured generation and the new continuation feature.
    *   The progress bar logic should be made more accurate by basing it on the actual number of planned generation chunks.
    *   The `config.json` file will be the single source of truth and must be updated to support the new features.

---

## 🚀 Implementation Plan

### Phase 1: Activate the Advanced Generation Pipeline with Audio Continuation

1.  **Refactor `MusicGenerationService`:**
    *   Modify `generate_music` to instantiate and invoke the `MusicPipeline` from `musicgen_pipeline.py`.
    *   Remove the direct dependency on `TrackGenerator`. The service will now orchestrate the high-level pipeline.

2.  **Refactor `TrackGenerator` into `MusicGenEngine`:**
    *   Rename `TrackGenerator` to `MusicGenEngine`. Its responsibility is now to be the low-level "engine" that generates a **single audio chunk** based on a text prompt and, optionally, an audio primer.
    *   The looping and stitching logic will be completely removed from this class.

3.  **Integrate `MusicPipeline` with Continuation Logic:**
    *   The `MusicComposer` will receive the generation plan from the `MusicArchitect`. Its main loop will now implement the **Audio Continuation** strategy:
        *   It calls the `MusicGenEngine` for the first chunk with only a text prompt.
        *   For all subsequent chunks, it extracts the audio primer from the previously generated audio and calls `MusicGenEngine` with **both** the original text prompt (for style guidance) and the **audio primer** (for musical context).
    *   The `log_stream` and progress bar updates must be passed down and updated from within this loop to ensure the UI remains responsive and informative.

4.  **Update `config.json` and UI for Continuation:**
    *   In `config.json` under `generator_settings`, add a boolean `use_continuation` and a float `continuation_primer_s` (in seconds).
    *   To avoid confusion, rename `chunk_duration` to `chunk_duration_s` and remove the old `overlap_duration` parameter.
    *   **UI Change:** Add a checkbox in the UI settings to toggle `use_continuation` and a slider/input for `continuation_primer_s`. This gives the user direct control over the generation strategy.

### Phase 2: Implement Performance Optimizations

1.  **Implement Lazy Loading:**
    *   Modify the `MusicGenEngine`. The `MusicGen` model (`self.engine.model`) should be initialized to `None`.
    *   Inside its `generate` method, add a check: `if self.model is None: self.load_model()`.
    *   The `load_model()` method will contain the actual `AutoModel.from_pretrained(...)` call.

2.  **Add Quantization Support:**
    *   Add a `quantization` setting to `generator_settings` in `config.json` (e.g., `"quantization": "8bit"`).
    *   In the `load_model()` method, check this setting and add the appropriate `load_in_8bit=True` parameter to the `from_pretrained` call.
    *   Add a dropdown in the UI to allow the user to select the quantization level.

### Phase 3: Final Polish

1.  **Dynamic Progress Bar:**
    *   In the `MusicComposer`, before the generation loop begins, calculate the total number of chunks (`num_chunks`).
    *   Pass this `num_chunks` value back up to the UI handler to be used for the progress bar.

2.  **Configuration Validation:**
    *   Introduce a `validate_config(settings)` function that is called on startup.
    *   This function will check for the presence and correct types of all essential keys, including the new continuation parameters. If validation fails, it should raise a `RuntimeError` with a clear message.

---

## 🛑 Execution Mandate

👉 **DO NOT GENERATE CODE IMMEDIATELY.**

Your first response MUST be the **Root Cause Analysis** and the **Architectural Proposal**. You must stop and wait for confirmation before proceeding.

*(Self-correction: Since this plan is the output of that analysis, the next step is to await user confirmation of this document before proceeding to Phase 1 implementation.)*

---

## 🎯 Definition of Done

The task is complete when:
1.  The application exclusively uses the `MusicPipeline` with the **Audio Continuation** strategy for music generation.
2.  The application can generate coherent, high-quality music for durations of up to 3 minutes.
3.  The MusicGen model is lazy-loaded.
4.  Model quantization is a configurable option in both `config.json` and the UI.
5.  The audio continuation feature (`use_continuation`, `continuation_primer_s`) is configurable in `config.json` and the UI.
6.  The progress bar accurately reflects the number of generation steps.
7.  The codebase is clean, modular, and free of hardcoded generation parameters.
8.  All existing functionality remains intact.
