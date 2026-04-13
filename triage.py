from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from config import (
    EMBEDDING_MODEL_NAME,
    EMBEDDING_SIMILARITY_THRESHOLD,
    EVENT_PROTOTYPES,
    EVENT_TAXONOMY,
    MAX_ARTICLE_CHARS_FOR_EMBEDDING,
    SPECULATIVE_TERMS,
    TRIAGE_BORDERLINE_THRESHOLD,
    TRIAGE_STRONG_THRESHOLD,
    USE_EMBEDDING_FALLBACK,
)
from utils import clip_text, dedupe_keep_order, normalize_text

try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    SentenceTransformer = None
    util = None


@dataclass
class TriageResult:
    is_candidate: bool
    triage_status: str  # strong_pass | borderline_pass | reject
    candidate_event_types: List[str]
    keywords_detected: List[str]
    triage_score: int
    embedding_label: Optional[str] = None
    embedding_similarity: Optional[float] = None


class EmbeddingFallback:
    def __init__(self) -> None:
        self.enabled = USE_EMBEDDING_FALLBACK and SentenceTransformer is not None
        self.model = None
        self.prototype_pairs = []
        self.prototype_embeddings = None

        if self.enabled:
            self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
            prototype_sentences = []
            for label, texts in EVENT_PROTOTYPES.items():
                for text in texts:
                    self.prototype_pairs.append((label, text))
                    prototype_sentences.append(text)
            self.prototype_embeddings = self.model.encode(
                prototype_sentences, convert_to_tensor=True
            )

    def check(self, article_text: str) -> Optional[Dict]:
        if not self.enabled or self.model is None or self.prototype_embeddings is None:
            return None

        reduced = clip_text(article_text, MAX_ARTICLE_CHARS_FOR_EMBEDDING)
        article_embedding = self.model.encode(reduced, convert_to_tensor=True)
        sims = util.cos_sim(article_embedding, self.prototype_embeddings)[0]

        best_idx = int(sims.argmax())
        best_score = float(sims[best_idx])
        best_label = self.prototype_pairs[best_idx][0]

        return {
            "is_candidate": best_score >= EMBEDDING_SIMILARITY_THRESHOLD,
            "best_label": best_label,
            "similarity": round(best_score, 4),
        }


embedding_fallback = EmbeddingFallback()


def compute_rule_score(text: str) -> Dict:
    normalized = normalize_text(text)
    total_score = 0
    matched_keywords: List[str] = []
    event_scores: Dict[str, int] = {}

    for event_label, groups in EVENT_TAXONOMY.items():
        event_score = 0

        for kw in groups["strong_keywords"]:
            if kw in normalized:
                event_score += 2
                matched_keywords.append(kw)

        for kw in groups["medium_keywords"]:
            if kw in normalized:
                event_score += 1
                matched_keywords.append(kw)

        if event_score > 0:
            event_scores[event_label] = event_score
            total_score += event_score

    speculation_penalty = 0
    for term in SPECULATIVE_TERMS:
        if term in normalized:
            speculation_penalty += 1
            matched_keywords.append(term)

    total_score -= speculation_penalty

    candidate_events = [
        event for event, score in sorted(event_scores.items(), key=lambda x: x[1], reverse=True)
    ]

    return {
        "total_score": total_score,
        "event_scores": event_scores,
        "candidate_events": candidate_events,
        "matched_keywords": dedupe_keep_order(matched_keywords),
    }


def triage_article(text: str) -> TriageResult:
    rule_result = compute_rule_score(text)

    score = rule_result["total_score"]
    candidate_events = rule_result["candidate_events"]
    matched_keywords = rule_result["matched_keywords"]

    if score >= TRIAGE_STRONG_THRESHOLD:
        return TriageResult(
            is_candidate=True,
            triage_status="strong_pass",
            candidate_event_types=candidate_events,
            keywords_detected=matched_keywords,
            triage_score=score,
        )

    if score >= TRIAGE_BORDERLINE_THRESHOLD:
        emb = embedding_fallback.check(text)
        if emb and emb["is_candidate"]:
            if emb["best_label"] not in candidate_events:
                candidate_events = candidate_events + [emb["best_label"]]
            return TriageResult(
                is_candidate=True,
                triage_status="borderline_pass",
                candidate_event_types=candidate_events,
                keywords_detected=matched_keywords,
                triage_score=score,
                embedding_label=emb["best_label"],
                embedding_similarity=emb["similarity"],
            )

    return TriageResult(
        is_candidate=False,
        triage_status="reject",
        candidate_event_types=[],
        keywords_detected=matched_keywords,
        triage_score=score,
    )