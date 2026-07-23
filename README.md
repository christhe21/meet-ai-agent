# Meet AI Agent

**Real-time voice-to-voice AI companion for Google Meet.**

A headless bot that joins your Google Meet, stays silent while others are present, and when you are alone activates a customizable AI personality (e.g. Gordon Ramsay, Socratic tutor, interview coach). It listens to your speech, thinks, and talks back through the meeting audio.

> "You are Gordon Ramsay. You are sitting in a Google Meet listening to a pitch..."

## Core Idea

Google Meet has no public bot API. We emulate a real participant using browser automation, capture audio (or captions), run STT → LLM → TTS, then inject the generated voice as the bot's microphone.

Activation is gated by participant count so the AI only "wakes up" when you are practicing alone.

## High-Level Components

| Component | Responsibility |
|-----------|----------------|
| **Joiner** | Playwright (or managed service) joins the Meet link as a headless Chrome user |
| **Lonely Trigger** | Scrapes DOM for participant count; activates only when count == 1 |
| **Ears (STT)** | Real-time speech-to-text (Deepgram / Gladia) or Meet live captions |
| **Brain (LLM)** | Fast LLM + system prompt defining the persona |
| **Voice (TTS + Injection)** | ElevenLabs / OpenAI TTS → virtual audio device → Meet mic |

## Status

🚧 Scaffold + full specification. Implementation in progress.

See [`docs/SPECIFICATION.md`](docs/SPECIFICATION.md) for the complete technical specification, architecture, sequences, and component contracts.

## Quick Start (once implemented)

```bash
git clone https://github.com/christhe21/meet-ai-agent.git
cd meet-ai-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill keys
python -m src.main --meet-url "https://meet.google.com/xxx-yyyy-zzz" --persona gordon
```

## License

MIT
