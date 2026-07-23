"""
Audio injection - play TTS audio into the virtual microphone device
that Chromium / Google Meet is configured to use.

OS-specific notes:
- Windows: VB-Cable
- macOS: BlackHole
- Linux: PulseAudio null sink or JACK
"""

from __future__ import annotations

from typing import Optional


class AudioInjector:
    def __init__(self, device_name: Optional[str] = None):
        self.device_name = device_name

    def list_devices(self) -> list[str]:
        """Return available playback devices (for debugging)."""
        # TODO: use sounddevice / pyaudio / soundcard
        raise NotImplementedError

    async def play(self, audio_bytes: bytes, sample_rate: int = 24000) -> None:
        """
        Play the given audio into the configured virtual mic device.
        Blocks until playback finishes (or is cancelled).
        """
        # TODO: implement with sounddevice or equivalent
        raise NotImplementedError

    def stop(self) -> None:
        """Interrupt current playback if any."""
        raise NotImplementedError
