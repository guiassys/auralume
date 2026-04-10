# 🚀 Prompt: Auralith Evolution — Professional DAW Interface Implementation

**Role:** Senior Software Engineer (Generative AI, Digital Audio, & LangChain).
**Context:** Evolving the **Auralith** system's UI from a basic Gradio layout to a professional Digital Audio Workstation (DAW) experience.
**Language Requirement:** All logs and code documentation MUST be in **English**.

---

## 🧠 1. TECHNICAL STACK & ARCHITECTURE
The system uses a modular Python architecture:
- **UI:** Gradio (Current target for redesign).
- **Inference:** Meta MusicGen via Hugging Face.
- **Orchestration:** LangChain Expression Language (LCEL) & `LofiGenerator`.
- **Engine:** `MusicGenEngine` & `MusicGenerationService`.

---

## 🎯 2. OBJECTIVE: UI/UX OVERHAUL
Redesign the Gradio interface to mimic a professional DAW (e.g., Ableton Live, FL Studio).

### A. Visual Identity (Industrial Dark Mode)
* **Aesthetics:** Graphite grays and matte black backgrounds.
* **Accents:** Neon green or electric blue for active states and progress bars.
* **Typography:** Modern sans-serif with monospaced fonts for technical/numerical data.

### B. Layout Hierarchy
1.  **Header (Global):**
    * Left: Auralith Logo + System Status (CPU/Inference Engine).
    * Center: **Persistent Progress Bar** (Slim, glowing) showing "Rendering..." status and %.
2.  **Sidebar (Left - Expansive):**
    * Icons: [Studio Tools (Active)], [About], [Help].
3.  **Main Workspace (Tabbed Interface):**
    * **Tab 1: Track Definitions:** Genre, BPM, Key, Mood, and Style Prompt.
    * **Tab 2: Studio Adjustments:** Sliders for Reverb, Delay, Compression, and Instrument selection.
    * **Tab 3: Studio Console:** Waveform visualization and Export options (WAV/MP3).
4.  **Footer:** Session timer, versioning, and system links.

### C. Interaction Logic (UX)
* **Non-Blocking Navigation:** Users must be able to switch tabs and browse the sidebar during generation.
* **State Locking:** Use Gradio's `interactive=False` or `gr.update` to lock "Generate" and "Clear" buttons strictly while the process is running. Unlock only upon completion.

---

## ⚠️ 3. CRITICAL CONSTRAINTS & PRESERVATION
> **DO NOT BREAK STABLE FUNCTIONALITY.**

**Must Maintain:**
- ✅ Music generation pipeline & GPU locking.
- ✅ Crossfade/chunking logic.
- ✅ Existing terminal and UI logging behavior.
- ✅ Backward compatibility with current service layers.

**Forbidden:**
- ❌ Removing existing logs.
- ❌ Adding heavy external CSS frameworks (Use Gradio's built-in `css` and `theme` capabilities).
- ❌ Breaking the LCEL chain integration.

---

## 🧼 4. CODE QUALITY & OUTPUT
Provide **complete, production-ready code**. If necessary, split the UI logic into `src/web/ui_components.py` or similar to maintain modularity.

**Requirements:**
- Full `typing` annotations.
- Clean separation between Gradio event listeners and business logic.
- Minimal changes to `MusicGenEngine`—focus on the `web` layer.

---

## 🚀 IMPLEMENTATION STEP-BY-STEP
1.  Define the custom **Gradio Theme** (Dark Mode/Neon Accents).
2.  Refactor the main layout into `gr.Blocks()` with `gr.Tabs()`.
3.  Implement the Sidebar and Header logic.
4.  Update the event triggers to handle **State Locking** for buttons.
5.  **Stop and ask for confirmation after presenting the architectural plan before generating the full code.**