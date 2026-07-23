# Meet AI Agent — Technical Specification

**Version:** 0.1.0 (Scaffold)
**Status:** Design complete / Implementation pending
**Owner:** christhe21

---

## 1. Context & Problem Statement

Google Meet does not expose a public API that allows third-party bots to join a meeting, receive the audio mix, or inject audio as a participant microphone. The only reliable way to participate programmatically is to drive a real browser session (headless or headed) that behaves exactly like a human user.

Users often practice presentations, pitches, lectures, or interviews alone in a Meet room and want an interactive AI partner that can listen and respond in real time with a strong personality. Existing solutions either require a second device + virtual cable or lack the "only activate when alone" safety/privacy gate.

This project solves that by creating a single-process (or small multi-process) agent that:

1. Joins a Meet link as a first-class participant.
2. Monitors participant count.
3. Only enters listening/speaking mode when the count is exactly 1 (the human).
4. Performs low-latency STT → LLM → TTS.
5. Injects the synthesized voice back into the meeting as the bot's microphone stream.

---

## 2. Goals & Non-Goals

### Goals
- Join any Google Meet link programmatically.
- Detect "lonely" state (participant count == 1) with configurable dwell time.
- Real-time transcription of the human's speech.
- Persona-driven responses via LLM system prompt.
- Natural-sounding TTS injected as live microphone audio.
- Configurable personas (Gordon Ramsay, interview coach, Socratic tutor, etc.).
- Graceful handling of Meet UI changes where possible (selectors isolated).

### Non-Goals (v1)
- Multi-party conversation support (bot stays mute when others join).
- Video avatar / face.
- Persistent memory across sessions (stateless per meeting for now).
- Mobile client support.
- Production multi-tenant SaaS.

---

## 3. Architecture Components

### 3.1 Joiner (Browser Automation)
**Responsibility:** Launch a Chromium instance, navigate to the Meet URL, dismiss pre-join screens, turn off camera, set microphone to the virtual audio device, and enter the call.

**Interfaces:**
- `join(meet_url: str, display_name: str = "AI Coach") -> BrowserContext`
- `leave() -> None`
- `is_in_call() -> bool`

**Tech options:**
- Primary: Playwright (Python)
- Fallback / managed: Recall.ai, Meeting Baas, or similar bot-as-a-service

**Key selectors (to be isolated in config):**
- Join button, name input, camera/mic toggles, participant count element.

### 3.2 Lonely Trigger (Participant Detection)
**Responsibility:** Continuously scrape the Meet DOM for the current number of participants. Emit events when the room becomes lonely or ceases to be lonely.

**Interfaces:**
- `start_monitoring(page: Page, poll_interval_ms: int = 1500) -> AsyncIterator[LonelyState]`
- `get_participant_count(page: Page) -> int`

**Logic:**
- Count == 1 for `min_lonely_duration_s` consecutive seconds → activate.
- Count > 1 → immediately deactivate listening/speaking.

### 3.3 Ears (Speech-to-Text)
**Responsibility:** Convert the human's spoken audio into text with low latency and good accuracy.

**Options (priority order):**
1. Capture tab/system audio or browser media stream → Deepgram Nova-2 / Gladia streaming.
2. Scrape Google Meet live closed captions from the DOM (easier, lower fidelity, no extra audio routing).

**Interfaces:**
- `start_listening() -> AsyncIterator[TranscriptChunk]`
- `stop_listening()`

**TranscriptChunk:** `{ text: str, is_final: bool, confidence: float, timestamp: float }`

### 3.4 Brain (LLM + Persona)
**Responsibility:** Turn a completed utterance (or rolling context) into a persona-consistent reply.

**Interfaces:**
- `generate_response(transcript: str, conversation_history: list[Message], persona: Persona) -> str`

**Persona model:**
```python
@dataclass
class Persona:
    name: str
    system_prompt: str
    temperature: float = 0.7
    max_tokens: int = 150
    voice_id: str | None = None  # for TTS mapping
```

**Recommended models (fast):** GPT-4o-mini, Claude 3.5 Haiku, Gemini 1.5 Flash, Grok.

### 3.5 Voice (TTS + Audio Injection)
**Responsibility:** Convert LLM text into speech audio and route it into the Playwright browser's microphone input so Meet transmits it.

**Pipeline:**
1. TTS service (ElevenLabs, OpenAI Audio, Cartesia, etc.) → PCM/WAV/MP3 stream or file.
2. Play the audio into a virtual audio cable (VB-Cable, BlackHole, PulseAudio null sink, etc.).
3. Configure Chromium launch args so the default mic is that virtual device.

**Interfaces:**
- `speak(text: str, voice_id: str | None = None) -> None`  # blocks until playback finishes or is interruptible
- `set_microphone_device(device_name: str)`

---

## 4. Overall Data Flow

```
[Human speaks in Meet]
        ↓
[Browser audio mix / captions]
        ↓
[STT service] → final transcript
        ↓
[LLM + Persona system prompt] → reply text
        ↓
[TTS] → audio bytes
        ↓
[Virtual Audio Device]
        ↓
[Playwright Chromium mic]
        ↓
[Google Meet transmits bot voice]
```

Control plane runs in parallel:
- Participant detector → enable/disable the STT/LLM/TTS loop.

---

## 5. Key Sequences

### 5.1 Join & Idle
1. User starts agent with Meet URL + persona.
2. Joiner launches browser, navigates, fills name, joins.
3. Detector starts polling.
4. Agent remains silent (mic muted or no TTS) while count > 1.

### 5.2 Lonely Activation
1. Detector sees count == 1 for N seconds.
2. Emit `LonelyState.ACTIVE`.
3. STT starts (or captions watcher starts).
4. Mic remains ready (virtual device already selected).

### 5.3 Speak Cycle (when lonely)
1. Human finishes utterance (VAD or silence timeout or final caption).
2. STT yields final transcript.
3. Brain generates reply (with short history).
4. TTS synthesizes.
5. Audio is played into virtual cable → Meet hears it.
6. Optional: short cooldown before next listen.

### 5.4 Deactivation
1. Another participant joins (count >= 2).
2. Immediately stop STT, cancel any pending TTS, mute or silence mic.
3. Return to idle monitoring.

---

## 6. Diagrams Needed

Place Mermaid sources under `docs/diagrams/`:

| File | Purpose |
|------|---------|
| `overview.mmd` | High-level component diagram |
| `data-flow.mmd` | Audio + text pipeline |
| `sequence-join.mmd` | Join + idle sequence |
| `sequence-lonely.mmd` | Lonely activation + speak cycle |
| `sequence-interrupt.mmd` | Someone joins while bot is speaking |

Render them in the README or a docs site later.

---

## 7. Configuration & Secrets

All secrets and tunable parameters live in `.env` (see `.env.example`).

Key variables:
- `MEET_URL`
- `DISPLAY_NAME`
- `PERSONA` (or path to persona YAML)
- `DEEPGRAM_API_KEY` / `GLADIA_API_KEY`
- `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / etc.
- `ELEVENLABS_API_KEY`
- `VIRTUAL_MIC_DEVICE`
- `MIN_LONELY_SECONDS`
- `STT_PROVIDER`
- `LLM_PROVIDER`
- `TTS_PROVIDER`

---

## 8. Directory Layout (Target)

```
src/
  main.py                 # CLI entry + orchestration
  config.py
  joiner/
    browser_joiner.py
  detector/
    participant_detector.py
  stt/
    speech_to_text.py
    captions_scraper.py   # alternative
  llm/
    persona_brain.py
    personas/             # YAML or Python definitions
  tts/
    text_to_speech.py
  audio/
    injector.py
    virtual_device.py
docs/
  SPECIFICATION.md        # this file
  ARCHITECTURE.md
  SEQUENCES.md
  diagrams/
tests/
scripts/
  setup_virtual_audio.sh  # OS-specific helpers
```

---

## 9. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Meet DOM selectors break | Isolate all selectors; prefer managed bot APIs when available |
| Audio routing complexity on Linux/macOS/Windows | Provide per-OS setup scripts; document BlackHole / VB-Cable / PulseAudio |
| Latency (STT + LLM + TTS) | Use streaming STT, fast models, streaming TTS where possible; target < 2.5 s end-to-end |
| Accidental speaking when others present | Hard gate on participant count; immediate mute |
| Cost of STT/LLM/TTS | Make providers pluggable; support local models later |

---

## 10. Future Extensions

- Multiple simultaneous personas / voice switching
- Conversation memory + RAG over the presentation deck
- Video avatar (HeyGen / LivePortrait style)
- Integration with Recall.ai as primary joiner
- Web UI for persona editing and session control
