# 🚀 Prompt: Holistic Refactoring for Quality and Coherence

## 🧠 Persona

As an expert AI Software Architect, my role is to analyze the existing Auralume application, identify architectural inconsistencies and opportunities for improvement, and propose a detailed refactoring plan. The primary goal is to enhance the quality, coherence, and length of the generated music while improving code maintainability, performance, and user experience.

---

## 🌍 Context

The user wants to improve the Auralume application to generate high-quality, coherent music up to 3 minutes long. The current implementation suffers from context loss in longer tracks, leading to undesirable style changes and noise. Furthermore, the application's architecture has inconsistencies, performance can be optimized, and several hardcoded parameters still exist.

This plan outlines a holistic refactoring process to address these issues, focusing on activating a more advanced generation pipeline that already exists but is currently inactive.

---

## 🎯 Primary Objective

Refactor the Auralume application to:
1.  **Generate High-Coherence Music:** Produce musically consistent tracks up to 3 minutes long by solving the context loss problem.
2.  **Unify the Architecture:** Eliminate the redundant, simple generation pipeline in favor of the advanced, structure-aware pipeline.
3.  **Optimize Performance:** Improve application startup time and reduce GPU memory consumption through techniques like lazy loading and quantization.
4.  **Enhance Code Quality:** Ensure the codebase adheres to best practices, including the Single Responsibility Principle (SRP) and full configuration-driven behavior (no hardcoding).

---

## ⚠️ Hard Constraints

### ✅ Must Preserve
- All existing UI functionalities must be preserved.
- The application must continue to be driven by the `config.json` file.
- The ability to handle both Windows and Linux style paths for the output directory must be maintained.

### ❌ Forbidden
- Do not break existing core features.
- Do not introduce new hardcoded parameters; all configurations must be sourced from `config.json`.
- Do not remove the "fail-fast" approach for `config.json` loading.

---

## 💡 Key Technical Directives (Prioritized)

1.  **Architectural Unification:** The most critical issue is the dual-pipeline architecture. The simple, naive continuation loop in `TrackGenerator` is the root cause of context loss. The advanced, structure-aware pipeline (`MusicPipeline`, `MusicArchitect`, `MusicComposer`) is the solution. **Our top priority is to make this advanced pipeline the primary engine for music generation.**

2.  **Long-Term Context Management:** The key to coherence in long-form generation is memory. The `MusicComposer`'s use of section-based prompting (`last_context`) and its vector store (RAG) is the correct approach. We must ensure this is properly integrated and utilized.

3.  **Performance Optimization:**
    *   **Lazy Loading:** The MusicGen model should not be loaded into VRAM on application startup. It should be loaded only on the first generation request to ensure a fast startup and efficient resource management.
    *   **Quantization:** To handle long generation tasks and reduce memory footprint, we should add support for model quantization (e.g., 8-bit) as a configurable option.

4.  **Configuration and UI Enhancements:**
    *   The UI must be adapted to fully support the advanced pipeline. This includes providing clear controls for structured generation.
    *   The progress bar logic should be made more accurate by basing it on the actual number of planned generation chunks.
    *   The `config.json` file will be the single source of truth and may need to be restructured to support the new features (e.g., quantization settings).

---

## 🚀 Implementation Plan

### Phase 1: Activate the Advanced Generation Pipeline

1.  **Refactor `MusicGenerationService`:**
    *   Modify `generate_music` to instantiate and invoke the `MusicPipeline` from `musicgen_pipeline.py`.
    *   Remove the direct dependency on `TrackGenerator`. The service will now orchestrate the high-level pipeline.

2.  **Refactor `TrackGenerator` into `MusicGenEngine`:**
    *   The current `TrackGenerator` is misnamed. Its real job is to be the low-level "engine" that generates a single audio chunk based on a prompt.
    *   Rename `TrackGenerator` to `MusicGenEngine` (or similar) and simplify its `generate` method to only produce a single audio segment. The looping and stitching logic will be removed, as this is now the responsibility of the `MusicComposer`.

3.  **Integrate `MusicPipeline` with the UI:**
    *   The `MusicPipeline`'s `build` method expects `prompt`, `duration`, and `style`. The `run_generation` handler in `app.py` will call this.
    *   The `MusicComposer` will receive the full plan from the `MusicArchitect` and iterate through the sections, calling the newly refactored `MusicGenEngine` for each chunk.
    *   The `log_stream` must be passed down through the pipeline (`MusicGenerationService` -> `MusicPipeline` -> `MusicComposer`) to provide real-time feedback to the UI.

4.  **Update `config.json`:**
    *   Ensure the `architect_settings` (structure, bpm_range) and `generator_settings` (embedding_size) are correctly consumed by the `MusicArchitect` and `EmbeddingProvider`.
    *   The `duration` from the UI will be the primary input for the `MusicArchitect` to plan the track structure.

### Phase 2: Implement Performance Optimizations

1.  **Implement Lazy Loading:**
    *   Modify the `MusicGenEngine` (the refactored `TrackGenerator`). The `MusicGen` model (`self.engine.model`) should be initialized to `None`.
    *   Inside the `generate` method, add a check: `if self.model is None: self.load_model()`.
    *   The `load_model()` method will contain the actual `AutoModel.from_pretrained(...)` call, loading the model into VRAM only when it's first needed.

2.  **Add Quantization Support:**
    *   Add a `quantization` setting to `generator_settings` in `config.json` (e.g., `"quantization": "8bit"` or `"quantization": "none"`).
    *   In the `load_model()` method, check this setting. If quantization is enabled, add the appropriate `load_in_8bit=True` or `load_in_4bit=True` parameter to the `from_pretrained` call.
    *   Add a dropdown in the "Settings" tab of the UI to allow the user to select the quantization level.

### Phase 3: Final Polish

1.  **Dynamic Progress Bar:**
    *   In the `MusicComposer`, before the generation loop begins, calculate the total number of sections (`num_chunks = len(inputs['structure'])`).
    *   Pass this `num_chunks` value back up to the UI handler.
    *   Modify the `_ui_update_progress` function to use this dynamic value instead of the hardcoded `25`.

2.  **Configuration Validation (Optional but Recommended):**
    *   Introduce a `validate_config(settings)` function that is called immediately after `load_app_settings`.
    *   This function will check for the presence and correct types of all essential keys and sub-keys. If validation fails, it should raise a `RuntimeError` with a clear message, leveraging our "fail-fast" approach.

---

## 🛑 Execution Mandate

👉 **DO NOT GENERATE CODE IMMEDIATELY.**

Your first response MUST be the **Root Cause Analysis** and the **Architectural Proposal**. You must stop and wait for confirmation before proceeding.

*(Self-correction: Since this plan is the output of that analysis, the next step is to await user confirmation of this document before proceeding to Phase 1 implementation.)*

---

## 🎯 Definition of Done

The task is complete when:
1.  The application exclusively uses the `MusicPipeline` for music generation.
2.  The application can generate coherent, high-quality music for durations of up to 3 minutes, respecting the structure defined in `config.json`.
3.  The MusicGen model is lazy-loaded, resulting in a fast application startup.
4.  Model quantization is available as a configurable option in both `config.json` and the UI.
5.  The progress bar accurately reflects the number of generation steps.
6.  The codebase is clean, modular, and free of hardcoded generation parameters.
7.  All existing functionality remains intact.
