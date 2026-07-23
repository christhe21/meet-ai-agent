# Component Checklist

Use this as a living status board while implementing.

| Component | File(s) | Status | Notes |
|-----------|---------|--------|-------|
| **Joiner** | `src/joiner/browser_joiner.py` | Skeleton | Playwright launch + Meet join flow |
| **Lonely Trigger** | `src/detector/participant_detector.py` | Skeleton | DOM poll + dwell timer |
| **Ears (STT)** | `src/stt/speech_to_text.py` | Skeleton | Deepgram / Gladia streaming |
| **Ears (Captions)** | `src/stt/captions_scraper.py` | Skeleton | Alternative, lower fidelity |
| **Brain (LLM)** | `src/llm/persona_brain.py` | Skeleton | Persona system + provider calls |
| **Voice (TTS)** | `src/tts/text_to_speech.py` | Skeleton | ElevenLabs / OpenAI |
| **Audio Injector** | `src/audio/injector.py` | Skeleton | Play into virtual mic |
| **Config** | `src/config.py` | Skeleton | dotenv based |
| **Orchestrator** | `src/main.py` | Skeleton | Wire everything together |
| **Virtual Audio Docs** | `scripts/setup_virtual_audio.md` | Draft | Per-OS setup |
| **Spec** | `docs/SPECIFICATION.md` | Complete | Source of truth |
| **Architecture** | `docs/ARCHITECTURE.md` | Draft | |
| **Sequences** | `docs/SEQUENCES.md` | Draft | Mermaid included |

## Implementation Order Suggestion

1. Joiner (get a bot into a Meet room reliably)
2. Detector (read participant count)
3. Captions scraper (quick STT path for testing)
4. LLM + simple persona
5. TTS + manual audio play (hear it outside Meet first)
6. Audio injection into virtual device
7. Full lonely-gated loop
8. Polish latency, error handling, interruptibility
