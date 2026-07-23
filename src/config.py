"""
Configuration loader.

Loads from environment variables (and later optionally from YAML).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    meet_url: Optional[str] = None
    display_name: str = "AI Coach"
    persona: str = "gordon"

    # Providers
    stt_provider: str = "deepgram"
    llm_provider: str = "openai"
    tts_provider: str = "elevenlabs"

    # Keys (never log these)
    deepgram_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    elevenlabs_api_key: Optional[str] = None

    # Behavior
    min_lonely_seconds: float = 3.0
    virtual_mic_device: Optional[str] = None

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            meet_url=os.getenv("MEET_URL"),
            display_name=os.getenv("DISPLAY_NAME", "AI Coach"),
            persona=os.getenv("PERSONA", "gordon"),
            stt_provider=os.getenv("STT_PROVIDER", "deepgram"),
            llm_provider=os.getenv("LLM_PROVIDER", "openai"),
            tts_provider=os.getenv("TTS_PROVIDER", "elevenlabs"),
            deepgram_api_key=os.getenv("DEEPGRAM_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY"),
            min_lonely_seconds=float(os.getenv("MIN_LONELY_SECONDS", "3.0")),
            virtual_mic_device=os.getenv("VIRTUAL_MIC_DEVICE"),
        )
