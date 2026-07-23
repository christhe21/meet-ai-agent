# Sequence Descriptions

## 1. Application Startup & Join

```mermaid
sequenceDiagram
    actor User
    participant Main
    participant Joiner
    participant Browser
    participant Meet
    participant Detector

    User->>Main: start(--meet-url, --persona)
    Main->>Joiner: join(url, name)
    Joiner->>Browser: launch + navigate
    Browser->>Meet: join call
    Meet-->>Browser: in-call UI
    Joiner-->>Main: context ready
    Main->>Detector: start_monitoring(page)
    Note over Detector: poll participant count
```

## 2. Lonely Activation + Speak Cycle

```mermaid
sequenceDiagram
    participant Detector
    participant Orchestrator
    participant STT
    participant LLM
    participant TTS
    participant Audio
    participant Meet

    Detector->>Orchestrator: LonelyState.ACTIVE (count==1 for N s)
    Orchestrator->>STT: start_listening()
    loop while lonely
        STT->>Orchestrator: final transcript
        Orchestrator->>LLM: generate(transcript, history, persona)
        LLM-->>Orchestrator: reply text
        Orchestrator->>TTS: synthesize(reply)
        TTS-->>Orchestrator: audio bytes
        Orchestrator->>Audio: play_to_virtual_mic(audio)
        Audio->>Meet: mic stream
    end
```

## 3. Interrupt (Someone Joins)

```mermaid
sequenceDiagram
    participant Detector
    participant Orchestrator
    participant STT
    participant TTS

    Detector->>Orchestrator: LonelyState.INACTIVE (count >= 2)
    Orchestrator->>STT: stop_listening()
    Orchestrator->>TTS: cancel_current()
    Note over Orchestrator: mic silenced / no further TTS
```

Copy the Mermaid blocks into `docs/diagrams/*.mmd` when ready for rendering.
