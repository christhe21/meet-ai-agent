# Architecture Overview

## Component Diagram (textual)

```
+------------------+       +-------------------+       +------------------+
|   CLI / main.py  |------>|     Joiner        |------>|  Chromium +      |
|                  |       |  (Playwright)     |       |  Google Meet     |
+--------+---------+       +---------+---------+       +--------+---------+
         |                           |                          |
         |                           v                          |
         |                 +-------------------+                |
         |                 | Lonely Trigger    |<---------------+
         |                 | (DOM scraper)     |
         |                 +---------+---------+
         |                           |
         v                           v
+------------------+       +-------------------+
|   Orchestrator   |<----->|  Activation Gate  |
+--------+---------+       +-------------------+
         |
         +------------+-------------+-------------+
         |            |             |             |
         v            v             v             v
   +-----------+ +----------+ +-----------+ +-------------+
   |   STT     | |   LLM    | |   TTS     | | Audio Inject|
   | (Deepgram)| | (Persona)| | (11Labs)  | | (Virtual Mic)
   +-----------+ +----------+ +-----------+ +-------------+
```

## Process Model

Single Python process (asyncio) is preferred for v1:

- Playwright runs in the same process (or via playwright's own browser process).
- STT and TTS are outbound HTTP/WebSocket clients.
- Virtual audio is OS-level; the Python process only plays audio into the correct device.

## Extensibility Points

Every major component is behind a protocol / ABC so providers can be swapped:

- `STTProvider`
- `LLMProvider`
- `TTSProvider`
- `JoinerBackend` (Playwright vs managed API)

See `src/*/base.py` (to be created) for the contracts.
