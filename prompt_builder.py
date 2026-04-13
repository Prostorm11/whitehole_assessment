from __future__ import annotations

from config import MAX_ARTICLE_CHARS_FOR_LLM
from utils import clip_text


def build_classifier_prompt(article_text: str, triage_hint: dict) -> str:
    clipped_article = clip_text(article_text, MAX_ARTICLE_CHARS_FOR_LLM)

    return f"""
You are classifying a news article for geopolitical escalation risk related to Iran, the US, and Israel.

Your task is to identify whether the article describes a real event with potential macroeconomic impact, not general political noise.

Be conservative. Prioritize high precision.
Do not over-classify speculative, rhetorical, or commentary-driven articles as major events.

Allowed event labels:
1. Hormuz Closure
2. Kharg/Khark Attack or Seizure
3. Critical Gulf Infrastructure Attacks
4. Direct Entry of Saudi/UAE/Coalition Forces
5. Red Sea / Bab el-Mandeb Escalation

Calibration:
- Pure rhetoric, threats, warnings, commentary, or hypotheticals should usually stay below 0.40 final risk.
- High risk requires evidence of real operational disruption or credible widening of the conflict.
- If ambiguous, be conservative.
- Assign an event label only when the article provides enough evidence that the event is genuinely relevant.
- If the article is mostly commentary or weakly related, return an empty event_labels list.
- keywords_detected should include only terms actually supported by the article.
- rationale must be short and specific.
- All scores must be between 0.00 and 1.00.

Return only a valid JSON object.
Do not use markdown.
Do not wrap the JSON in code fences.
Do not include any explanatory text before or after the JSON.

Use exactly this schema:
{{
  "event_labels": ["..."],
  "physical_score": 0.0,
  "escalation_score": 0.0,
  "evidence_score": 0.0,
  "signal_score": 0.0,
  "model_score": 0.0,
  "rationale": "...",
  "keywords_detected": ["..."]
}}

Triage hint:
{triage_hint}

Article:
\"\"\"
{clipped_article}
\"\"\"
""".strip()