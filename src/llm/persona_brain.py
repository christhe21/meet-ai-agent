"""
Brain - LLM + Persona layer.

Turns a transcript (+ short history) into a persona-consistent reply.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Message:
    role: str  # "user" | "assistant" | "system"
    content: str


@dataclass
class Persona:
    name: str
    system_prompt: str
    temperature: float = 0.7
    max_tokens: int = 150
    voice_id: Optional[str] = None


# Example built-in personas (can later move to YAML)
PERSONAS = {
    "gordon": Persona(
        name="Gordon Ramsay",
        system_prompt=(
            "You are Gordon Ramsay. You are sitting in a Google Meet listening to a pitch "
            "or lecture. Respond with highly critical, slightly aggressive, but ultimately "
            "constructive questions or feedback. Keep replies short (1-3 sentences)."
        ),
        temperature=0.85,
        voice_id=None,
    ),
    "socratic": Persona(
        name="Socratic Tutor",
        system_prompt=(
            "You are a Socratic tutor. Ask probing, open-ended questions that help the "
            "speaker clarify their own thinking. Never give the answer directly. Keep "
            "replies to 1-2 short questions."
        ),
    ),
}


class PersonaBrain:
    def __init__(self, provider: str = "openai", model: str = "gpt-4o-mini", api_key: Optional[str] = None):
        self.provider = provider
        self.model = model
        self.api_key = api_key

    def get_persona(self, name_or_path: str) -> Persona:
        if name_or_path in PERSONAS:
            return PERSONAS[name_or_path]
        # TODO: load from YAML file
        raise ValueError(f"Unknown persona: {name_or_path}")

    async def generate_response(
        self,
        transcript: str,
        history: List[Message],
        persona: Persona,
    ) -> str:
        """
        Call the LLM with the persona system prompt + history + latest transcript.
        Return the assistant's reply text.
        """
        # TODO: implement provider calls (OpenAI, Anthropic, Gemini, etc.)
        raise NotImplementedError
