"""
Alternative Ears implementation: scrape Google Meet live closed captions.

Pros: no extra audio routing, simpler setup.
Cons: lower accuracy, depends on Meet enabling captions, more brittle selectors.
"""

from __future__ import annotations

from typing import AsyncIterator
from playwright.async_api import Page

from .speech_to_text import TranscriptChunk


class CaptionsScraper:
    def __init__(self, page: Page):
        self.page = page

    async def ensure_captions_on(self) -> None:
        """Click the captions button if not already enabled."""
        # TODO
        raise NotImplementedError

    async def stream_captions(self) -> AsyncIterator[TranscriptChunk]:
        """Watch the captions container and yield new text."""
        # TODO: MutationObserver via page.evaluate or polling
        raise NotImplementedError
        yield TranscriptChunk(text="", is_final=True)
