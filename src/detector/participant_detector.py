"""
Lonely Trigger - monitors Google Meet participant count via DOM.

Emits state changes when the room becomes (or stops being) lonely.
"""

from __future__ import annotations

import asyncio
from enum import Enum, auto
from typing import AsyncIterator, Optional
from playwright.async_api import Page


class LonelyState(Enum):
    ACTIVE = auto()    # count == 1 for required duration
    INACTIVE = auto()  # count > 1 or not yet confirmed


class ParticipantDetector:
    def __init__(self, min_lonely_seconds: float = 3.0, poll_interval_ms: int = 1500):
        self.min_lonely_seconds = min_lonely_seconds
        self.poll_interval_ms = poll_interval_ms
        self._task: Optional[asyncio.Task] = None

    async def get_participant_count(self, page: Page) -> int:
        """
        Scrape the participant count element.
        Selector is fragile; isolate and update when Meet changes UI.
        Example historical selector: document.querySelector('.uGOf1d')
        """
        # TODO: implement robust selector + fallback
        raise NotImplementedError

    async def start_monitoring(self, page: Page) -> AsyncIterator[LonelyState]:
        """
        Async generator that yields LonelyState changes.
        """
        # TODO: implement polling + dwell timer
        raise NotImplementedError
        yield LonelyState.INACTIVE  # unreachable, for type checkers
