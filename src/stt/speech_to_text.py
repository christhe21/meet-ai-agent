"""
Ears - Speech-to-Text abstraction.

Primary path: streaming STT (Deepgram / Gladia).
Alternative path: scrape Google Meet live captions (see captions_scraper.py).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import AsyncIterator, Optional


@dataclass
class TranscriptChunk:
    text: str
    is_final: bool
    confidence: float = 0.0
    timestamp: float = 0.0


class SpeechToText:
    def __init__(self, provider: str = "deepgram", api_key: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key

    async def start_listening(self) -> AsyncIterator[TranscriptChunk]:
        """
        Yield transcript chunks as they arrive.
        Only final chunks should normally be sent to the LLM.
        """
        # TODO: connect to Deepgram/Gladia websocket or local VAD + STT
        raise NotImplementedError
        yield TranscriptChunk(text="", is_final=True)  # unreachable

    async def stop_listening(self) -> None:
        raise NotImplementedError
