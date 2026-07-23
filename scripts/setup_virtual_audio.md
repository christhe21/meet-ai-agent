# Virtual Audio Device Setup

The bot needs a virtual microphone that Chromium can select and that we can play TTS audio into.

## Windows
- Install [VB-Audio Virtual Cable](https://vb-audio.com/Cable/)
- Set `VIRTUAL_MIC_DEVICE` to something like `CABLE Input (VB-Audio Virtual Cable)`
- In Playwright launch args, force the mic to that device if possible, or select it via Meet UI automation.

## macOS
- Install [BlackHole](https://github.com/ExistentialAudio/BlackHole)
- Create a Multi-Output Device if you also want to hear the bot locally.
- Use the BlackHole device name in config.

## Linux
- PulseAudio: create a null sink + loopback
  ```bash
  pactl load-module module-null-sink sink_name=VirtualMic
  pactl load-module module-loopback source=VirtualMic.monitor
  ```
- Or use JACK / PipeWire equivalents.

Always test that Meet shows the virtual device as the selected microphone before relying on automated selection.
