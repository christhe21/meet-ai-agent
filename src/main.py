"""
Meet AI Agent - CLI entrypoint and top-level orchestration.

TODO:
- Parse CLI args (meet-url, persona, providers)
- Load config / .env
- Instantiate Joiner, Detector, STT, LLM, TTS, AudioInjector
- Wire the lonely-gate loop
- Handle graceful shutdown
"""

from __future__ import annotations

import asyncio
import argparse
from typing import Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Meet AI Agent")
    parser.add_argument("--meet-url", required=True, help="Google Meet URL")
    parser.add_argument("--persona", default="gordon", help="Persona name or path")
    parser.add_argument("--display-name", default="AI Coach", help="Name shown in Meet")
    # TODO: more flags for providers, keys already in env
    return parser.parse_args()


async def run(meet_url: str, persona: str, display_name: str) -> None:
    """Main orchestration loop."""
    # TODO: implement
    print(f"[TODO] Would join {meet_url} as '{display_name}' with persona '{persona}'")
    raise NotImplementedError("Scaffold only - see docs/SPECIFICATION.md")


def main() -> None:
    args = parse_args()
    asyncio.run(run(args.meet_url, args.persona, args.display_name))


if __name__ == "__main__":
    main()
