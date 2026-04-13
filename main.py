from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

import argparse

from classifier import ArticleClassifier
from io_csv import read_input_csv, write_output_csv
from scoring import compute_confidence_score, compute_risk_score, map_confidence_label
from triage import triage_article
from utils import safe_json_dumps


def process_articles(input_path: str, output_path: str) -> None:
    df = read_input_csv(input_path)
    classifier = ArticleClassifier()

    output_event_labels = []
    output_risk_scores = []
    output_confidence = []
    output_rationales = []
    output_keywords_detected = []

    for _, row in df.iterrows():
        article_text = str(row["content"])
        triage = triage_article(article_text)

        if not triage.is_candidate:
            output_event_labels.append("[]")
            output_risk_scores.append(0.00)
            output_confidence.append("low")
            output_rationales.append(
                "Rejected at triage due to insufficient event signal or missing target-domain anchors."
            )
            output_keywords_detected.append(safe_json_dumps(triage.keywords_detected))
            continue

        triage_hint = {
            "triage_status": triage.triage_status,
            "candidate_event_types": triage.candidate_event_types,
            "keywords_detected": triage.keywords_detected,
            "triage_score": triage.triage_score,
            "domain_hit": triage.domain_hit,
            "domain_keywords_detected": triage.domain_keywords_detected,
            "embedding_label": triage.embedding_label,
            "embedding_similarity": triage.embedding_similarity,
        }

        try:
            result = classifier.classify(article_text, triage_hint)
        except Exception as exc:
            output_event_labels.append("[]")
            output_risk_scores.append(0.00)
            output_confidence.append("low")
            output_rationales.append(f"Classification failed: {str(exc)}")
            output_keywords_detected.append(
                safe_json_dumps(triage.keywords_detected)
            )
            continue

        physical_score = float(result["physical_score"])
        escalation_score = float(result["escalation_score"])
        evidence_score = float(result["evidence_score"])
        signal_score = float(result["signal_score"])
        model_score = float(result["model_score"])

        risk_score = compute_risk_score(
            physical_score=physical_score,
            escalation_score=escalation_score,
            evidence_score=evidence_score,
        )

        confidence_score = compute_confidence_score(
            evidence_score=evidence_score,
            signal_score=signal_score,
            model_score=model_score,
        )

        confidence_label = map_confidence_label(confidence_score)

        output_event_labels.append(safe_json_dumps(result.get("event_labels", [])))
        output_risk_scores.append(risk_score)
        output_confidence.append(confidence_label)
        output_rationales.append(result.get("rationale", ""))
        output_keywords_detected.append(
            safe_json_dumps(result.get("keywords_detected", triage.keywords_detected))
        )

    df["event_labels"] = output_event_labels
    df["risk_score"] = output_risk_scores
    df["confidence"] = output_confidence
    df["rationale"] = output_rationales
    df["keywords_detected"] = output_keywords_detected

    write_output_csv(df, output_path)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--output", required=True, help="Path to output CSV")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    process_articles(args.input, args.output)