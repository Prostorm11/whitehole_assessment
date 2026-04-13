from __future__ import annotations


def clip01(x: float) -> float:
    return max(0.0, min(1.0, x))


def compute_risk_score(
    physical_score: float,
    escalation_score: float,
    evidence_score: float,
) -> float:
    score = (
        0.45 * physical_score
        + 0.35 * escalation_score
        + 0.20 * evidence_score
    )
    return round(clip01(score), 2)


def compute_confidence_score(
    evidence_score: float,
    signal_score: float,
    model_score: float,
) -> float:
    score = (
        0.50 * evidence_score
        + 0.30 * signal_score
        + 0.20 * model_score
    )
    return round(clip01(score), 2)


def map_confidence_label(confidence_score: float) -> str:
    if confidence_score >= 0.70:
        return "high"
    if confidence_score >= 0.40:
        return "medium"
    return "low"