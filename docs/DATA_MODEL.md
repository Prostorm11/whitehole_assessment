# DATA_MODEL.md

## Purpose

This document defines the data structures used throughout the system, including:
- input schema
- output schema
- intermediate representations
- scoring components

The goal is to ensure clarity and consistency across all stages of the pipeline.

---

## 1. Input Schema

The system expects a CSV file with the following fields:

| Field      | Type   | Description              |
|------------|--------|--------------------------|
| pubDate    | string | Publication datetime     |
| link       | string | Article URL              |
| content    | string | Full article text        |
| source_id  | string | Source identifier        |

All fields are required.

---

## 2. Output Schema

The output CSV preserves all input columns and adds:

| Field              | Type                    | Description                          |
|--------------------|-------------------------|--------------------------------------|
| event_labels       | JSON string (list[str]) | Detected event categories            |
| risk_score         | float (0.00–1.00)       | Final macro-risk score               |
| confidence         | string                  | low / medium / high                  |
| rationale          | string                  | Short explanation of classification  |
| keywords_detected  | JSON string (list[str]) | Relevant keywords identified         |

---

## 3. Event Labels

The system supports the following predefined categories:

1. Hormuz Closure
2. Kharg/Khark Attack or Seizure
3. Critical Gulf Infrastructure Attacks
4. Direct Entry of Saudi/UAE/Coalition Forces
5. Red Sea / Bab el-Mandeb Escalation

The `event_labels` field may contain:
- zero labels (no relevant event)
- one label
- multiple labels

---

## 4. Triage Data Model

The triage stage produces a structured internal result.

### Structure

```python
TriageResult:
    is_candidate: bool
    triage_status: str
    candidate_event_types: list[str]
    keywords_detected: list[str]
    triage_score: int
    domain_hit: bool
    domain_keywords_detected: list[str]
    embedding_label: Optional[str]
    embedding_similarity: Optional[float]
```

### Field Descriptions

| Field                    | Description                                    |
|--------------------------|------------------------------------------------|
| is_candidate             | Whether the article proceeds to classification |
| triage_status            | strong_pass / borderline_pass / reject         |
| candidate_event_types    | Event types inferred from rule-based filtering |
| keywords_detected        | Matched keywords from taxonomy                 |
| triage_score             | Total rule-based score                         |
| domain_hit               | Whether domain keywords were detected          |
| domain_keywords_detected | List of detected domain anchors                |
| embedding_label          | Best semantic match (if used)                  |
| embedding_similarity     | Similarity score from embeddings               |

---

## 5. Classifier Output Model

The LLM returns structured JSON with the following fields:

```json
{
  "event_labels": [],
  "physical_score": 0.0,
  "escalation_score": 0.0,
  "evidence_score": 0.0,
  "signal_score": 0.0,
  "model_score": 0.0,
  "rationale": "",
  "keywords_detected": []
}
```

### Field Descriptions

| Field             | Description                                  |
|-------------------|----------------------------------------------|
| event_labels      | Predicted event categories                   |
| physical_score    | Severity of physical disruption              |
| escalation_score  | Degree of regional escalation                |
| evidence_score    | Strength of factual evidence                 |
| signal_score      | Internal consistency of the article          |
| model_score       | Model confidence proxy                       |
| rationale         | Short explanation of decision                |
| keywords_detected | Terms supported by the article               |

---

## 6. Risk Score Model

The final `risk_score` is computed using:

```
risk_score = 0.45 * physical_score
           + 0.35 * escalation_score
           + 0.20 * evidence_score
```

Range: `0.00` to `1.00`

---

## 7. Confidence Model

The numeric confidence score is computed as:

```
confidence_score = 0.5 * evidence_score
                 + 0.3 * signal_score
                 + 0.2 * model_score
```

It is mapped to categories:

| Range        | Label  |
|--------------|--------|
| < 0.40       | low    |
| 0.40 – 0.69  | medium |
| ≥ 0.70       | high   |

---

## 8. Serialization Notes

Because CSV fields are string-based:

- `event_labels` is stored as a JSON string
- `keywords_detected` is stored as a JSON string

This ensures compatibility with CSV format and easy parsing downstream.

---

## Summary

The system uses clearly defined data models at each stage:

- structured CSV input/output
- explicit triage representation
- structured classifier output
- deterministic scoring models

This ensures consistency, traceability, and ease of debugging.
