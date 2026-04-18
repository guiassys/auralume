# 🚀 Prompt: Auralume Evolution — Dynamic Processing Log Streaming in UI

You are a **Senior Software Engineer** specialized in **Generative AI, Digital Audio, and LangChain**.

Your mission is to evolve the **Auralume** system by implementing a **real-time dynamic processing log stream in the User Interface (UI)**, allowing users to observe execution logs as if they were viewing a live terminal.

All logs MUST be written in **English**.

---

## 🧠 1. TECHNICAL CONTEXT

The current system uses **Meta MusicGen (via Hugging Face)** and follows a modular architecture:

- Web Interface: **Gradio**
- Service Layer: `MusicGenerationService`
- Orchestrator: `LofiGenerator`
- Pipeline: **LangChain Expression Language (LCEL)**
- Engine: `MusicGenEngine`

---

## ⚠️ CURRENT LIMITATIONS

- ❌ No real-time observability in the UI
- ❌ Logs are not streamed dynamically during execution
- ❌ Users cannot track progress or processing stages
- ❌ No visibility into input parameters or execution timing

---

## 🎯 2. OBJECTIVE

Enhance the system to support **real-time observability via UI log streaming**.

### Core Goals:

1. **Real-time log streaming to UI**
   - Logs should appear progressively (not only after completion)
   - Mimic terminal-like behavior

2. **Input parameter visibility**
   - Display all relevant parameters at the start of execution

3. **Processing status updates**
   - Clear step-by-step execution messages (e.g., loading model, generating chunks, applying crossfade)

4. **Execution timing**
   - Display total processing time at the end:
     ```
     total processing time: 00:01:48
     ```

---

## 🧩 3. IMPLEMENTATION STRATEGY

### Suggested Approach:

- Introduce a **centralized logging stream mechanism**:
  - Use a thread-safe structure (e.g., `queue.Queue`, async generator, or callback handler)
  - Ensure compatibility with Gradio streaming outputs

- Implement a **LogEmitter / LogManager component**:
  - Responsible for:
    - Emitting logs
    - Formatting messages
    - Streaming updates to UI

- Use **LangChain callbacks (if applicable)** for pipeline observability

---

## 🔒 4. CRITICAL CONSTRAINT

> ⚠️ DO NOT BREAK EXISTING FUNCTIONALITY

The current system is stable and production-ready.

### MUST PRESERVE:

- ✅ Music generation pipeline
- ✅ Crossfade and chunking logic
- ✅ GPU locking mechanism
- ✅ Existing logging behavior (terminal + UI console)

---

## 🧱 5. DESIGN PRINCIPLES

- ✅ Incremental enhancement only
- ✅ Minimal and safe code changes
- ✅ Backward compatibility guaranteed
- ✅ No regression in performance or output

---

## 🧼 6. CODE QUALITY REQUIREMENTS

### Mandatory:

- Full type annotations (`typing`)
- Clean and modular architecture
- Detailed logging (in English)
- Clear separation of concerns

### Forbidden:

- ❌ Removing existing logs
- ❌ Breaking compatibility
- ❌ Introducing heavy or unnecessary dependencies

---

## 🖥️ 7. UI INTEGRATION

- The UI already contains a **log console**
- You must:
  - Stream logs dynamically into this console
  - Ensure smooth updates (avoid flickering or blocking)
  - Preserve responsiveness of the UI

---

## 📊 8. LOG FORMAT GUIDELINES

Logs should follow a structured and readable format:

```
[INFO] Starting music generation...
[INFO] Input parameters: tempo=70, mood=lofi, duration=120s
[INFO] Loading model...
[INFO] Generating chunk 1/4...
[INFO] Applying crossfade...
[INFO] Finalizing audio...
[INFO] total processing time: 00:01:48
```

---

## 🧪 9. EXPECTED OUTPUT

Provide **complete, production-ready code**, including:

- New logging/streaming components
- Minimal modifications to existing modules
- Integration with Gradio UI
- Clear typing and documentation

---

## ✅ FINAL REQUIREMENT

The solution must:

- Be **fully functional**
- Be **modular and extensible**
- Preserve all existing behavior
- Provide **real-time observability in the UI**

---

## 🚀 NOW IMPLEMENT

Generate the **full code implementation**, following all the constraints and best practices described above. Follow the steps and ask for confirmation.