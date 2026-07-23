"""
Voice - Text-to-Speech abstraction.

Produces audio bytes (or streams) that the AudioInjector can play into the virtual mic.
"""

from __future__ import annotations

from typing import Optional


class TextToSpeech:
    def __init__(self, provider: str = "elevenlabs", api_key: Optional[str] = None, default_voice_id: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key
        self.default_voice_id = default_voice_id

    async def synthesize(self, text: str, voice_id: Optional[str] = None) -> bytes:
        """
        Convert text to audio bytes (prefer PCM or WAV for low latency).
        """
        # TODO: call ElevenLabs / OpenAI Audio / Cartesia / local Coqui etc.
        raise NotImplementedError

    async def synthesize_stream(self, text: str, voice_id: Optional[str] = None):
        """Optional streaming variant for lower time-to-first-byte."""
        raise NotImplementedError
