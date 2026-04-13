from __future__ import annotations

import json
import re
from typing import Any, Dict

from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL
from prompt_builder import build_classifier_prompt


def _extract_json(text: str) -> Dict[str, Any]:
    """
    Try to parse model output as JSON.
    Handles:
    - raw JSON
    - ```json fenced blocks
    - extra text surrounding a JSON object
    """
    text = text.strip()

    fenced_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.DOTALL)
    if fenced_match:
        return json.loads(fenced_match.group(1))

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return json.loads(text[start:end + 1])

    raise ValueError(f"Could not extract valid JSON from model output:\n{text}")


class ArticleClassifier:
    def __init__(self) -> None:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def classify(self, article_text: str, triage_hint: Dict[str, Any]) -> Dict[str, Any]:
        prompt = build_classifier_prompt(article_text, triage_hint)

        response = self.client.responses.create(
            model=OPENAI_MODEL,
            input=prompt,
        )

        text = response.output_text.strip()
        return _extract_json(text)