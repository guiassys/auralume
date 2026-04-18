# 🚀 Prompt: Settings Tab Implementation

## 🧠 Persona

You are an expert Python developer specializing in building user interfaces with the Gradio library. Your task is to add a new feature to the Auralume Visualizer application, allowing users to configure system parameters through the interface.

You will act as a:
Senior Generative AI Engineer focused on extending an existing music generation pipeline to allow for more user control over the generation process.

---

## 🌍 Context

We have a system that generates music in `.wav` format using AI. We want to add a new feature to provide users with more flexibility in the input fields.

Currently, many parameters are hardcoded. The plan is to move these to a `config.json` file to serve as default values. Additionally, a new "Settings" tab will be created in the UI, allowing users to view and modify these parameters before starting the music generation process.

---

## 🎯 Primary Objective

Refactor the application to remove all hardcoded parameters and place them in a `config.json` file to serve as defaults. Implement a new "Settings" tab in the Gradio UI to allow users to override these default parameters before generation.

The new features must be:
- Default parameters loaded from `config.json`.
- A new "Settings" tab in the UI with components for each parameter.
- The generation process must use the user-defined values from the "Settings" tab, overriding the defaults.

---

## ⚙️ Existing Stack

- AI-based music generation model
- Python-based backend
- Gradio-based frontend for UI elements

---

## ⚠️ Hard Constraints

### ✅ Must Preserve

- The existing functionality of generating `.wav` files.
- The current workflow if no new options are selected by the user.
- The quality of the generated audio.

### ❌ Forbidden

- Breaking the existing music generation process.
- Removing any existing functionality.
- Degrading the performance of the system.

---

## 💡 Key Technical Directives (Prioritized)

- Identify all hardcoded parameters in the codebase.
- Create a `config.json` file with sensible default values for the identified parameters.
- Modify the application to read `config.json` to load default settings.
- Create a new "Settings" tab in the Gradio interface.
- Populate the "Settings" tab with UI components (e.g., sliders, dropdowns) for each parameter.
- Ensure the UI components in the "Settings" tab are initialized with the default values from `config.json`.
- Update the "Generate" button's function to take the values from the "Settings" tab as input for the music generation engine.

---

## 🚀 Implementation Plan

1.  **Configuration**:
    - Create a `config.json` file at the root of the project.
    - Add all identified parameters to `config.json`. Examples: `bpm`, `key`, `output_dir`, `chunk_duration`, `model_size`, `temperature`, etc.

2.  **Backend**:
    - Create a utility function to load the `config.json` file into a Python dictionary. This will provide the default settings.
    - Refactor the `musicgen_engine.py` and any other relevant files to accept generation parameters as arguments, instead of using hardcoded values.

3.  **Frontend (Gradio UI)**:
    - In the main UI file, add a new `gr.Tab(label="Settings")`.
    - Inside this tab, create Gradio components corresponding to the parameters in `config.json` (e.g., `gr.Slider` for `temperature`, `gr.Dropdown` for `key`).
    - Load the default values from the configuration file to set the initial state of these UI components.
    - Pass the interactive Gradio components from the "Settings" tab as inputs to the function that handles the "Generate" button click. This ensures the user's current selections are used.

---

## 🛑 Execution Mandate

👉 **DO NOT GENERATE CODE IMMEDIATELY.**

Your first response MUST be the **Root Cause Analysis** and the **Architectural Proposal**. You must stop and wait for confirmation before proceeding.

---

## 🎯 Definition of Done

The task is complete when:

-   A `config.json` file exists with all the specified parameters.
-   The application loads default values from `config.json` on startup.
-   A new "Settings" tab is present in the UI, displaying all configurable parameters with their default values.
-   The user can modify the values in the "Settings" tab.
-   Clicking the "Generate" button uses the values currently set in the "Settings" tab to generate the music.
-   The existing music generation process works as before if the settings are not changed.
