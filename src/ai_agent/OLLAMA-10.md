# 🚀 Prompt: Add Audio Format Selection and MIDI File Generation

## 🧠 Persona

You are an expert AI audio engineer specialized in generative music pipelines, audio formats, and MIDI integration.

You will act as a:
Senior Generative AI Engineer focused on extending an existing music generation pipeline with new output options, ensuring backward compatibility and high-quality results.

---

## 🌍 Context

We have a system that generates music in `.wav` format using AI. We want to add a new feature to provide users with more flexibility in the output format and to allow for further editing in Digital Audio Workstations (DAWs).

The new feature should be integrated with minimal disruption to the existing, functional system.

---

## 🎯 Primary Objective

Extend the current music generation system to allow users to select the audio output format and optionally generate a MIDI file.

The new features must be:
- Integrated into the frontend with new UI elements.
- Implemented with default values to maintain the current behavior.
- Robust and without breaking the existing functionality.

---

## ⚙️ Existing Stack

- AI-based music generation model
- Python-based backend
- Frontend with UI elements for music generation
- Current output format: `.wav`

---

## ⚠️ Hard Constraints

### ✅ Must Preserve

- The existing functionality of generating `.wav` files.
- The current workflow if no new options are selected.
- The quality of the generated audio.

### ❌ Forbidden

- Breaking the existing music generation process.
- Making the new options the default.
- Degrading the performance of the system.

---

## 💡 Key Technical Directives (Prioritized)

1.  **Frontend Changes**:
    -   Add a checkbox/radio button group for selecting the desired audio format.
        -   Options: `.wav`, `.mp3`.
        -   Default value: `.wav`.
    -   Add a checkbox/radio button group for opting in to MIDI file generation.
        -   Options: `Yes`, `No`.
        -   Default value: `No`.

2.  **Backend Changes**:
    -   If the user selects `.mp3`, the system should convert the generated `.wav` file to `.mp3` format.
    -   If the user selects `Yes` for MIDI file generation, the system should generate and save a `.mid` file corresponding to the generated music.
    -   The system should handle the new parameters from the frontend to control these features.

---

## 🚀 Implementation Plan

1.  **Frontend**:
    -   Add the new UI elements (checkboxes/radio buttons) to the user interface.
    -   Ensure the default values are set as specified (`.wav` and `No`).
    -   Pass the selected values to the backend when the music generation is triggered.

2.  **Backend**:
    -   Modify the API endpoint to accept the new parameters (e.g., `format`, `generate_midi`).
    -   Implement the logic to handle the `.mp3` conversion if `format` is `.mp3`.
    -   Implement the logic to generate the `.mid` file if `generate_midi` is `true`.
    -   Ensure the file naming and storage are handled correctly for the new files.

---

## 🛑 Execution Mandate

👉 **DO NOT GENERATE CODE IMMEDIATELY.**

Your first response MUST be the **Root Cause Analysis** and the **Architectural Proposal**. You must stop and wait for confirmation before proceeding.

---

## 🎯 Definition of Done

The task is complete when:

-   The user can select the audio format (`.wav` or `.mp3`) from the frontend.
-   The user can choose to generate a MIDI file from the frontend.
-   The system correctly generates the files in the selected formats.
-   The default behavior of the system remains unchanged.
-   The new features are well-integrated and tested.