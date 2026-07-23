"""
Joiner component - Playwright-based Google Meet participant.

Responsibilities:
- Launch Chromium with correct mic device
- Navigate to Meet URL
- Handle pre-join UI (name, camera off, mic settings)
- Enter the call and keep the page alive
"""

from __future__ import annotations

from typing import Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page


class BrowserJoiner:
    def __init__(self, display_name: str = "AI Coach", headless: bool = True):
        self.display_name = display_name
        self.headless = headless
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    async def join(self, meet_url: str) -> Page:
        """Join the given Meet URL and return the active page."""
        # TODO: implement full flow
        # - launch with --use-fake-ui-for-media-stream or real virtual device
        # - fill name, turn camera off, set mic
        # - click Join
        # - wait for in-call indicators
        raise NotImplementedError

    async def leave(self) -> None:
        """Leave the call and close browser."""
        raise NotImplementedError

    @property
    def page(self) -> Optional[Page]:
        return self._page

    @property
    def is_in_call(self) -> bool:
        # TODO: check for in-call DOM markers
        return False
