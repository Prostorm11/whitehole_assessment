# ARCHITECTURE.md

## Purpose

This system processes a CSV of news articles to detect geopolitical escalation events involving Iran, the US, and Israel, and outputs structured risk signals.

The design prioritizes:
- high precision
- simplicity
- robustness

---

## 1. System Overview

The system is implemented as a batch pipeline:

```text
Input CSV → Triage → LLM Classification → Scoring → Output CSV
```

- local embeddings (Sentence Transformers) are used for borderline triage instead of API-based embeddings, reducing external API dependency and overall cost


## 2. Architectural Design

The system follows a two-stage pipeline:

**Stage 1 — Triage (Deterministic)**

Filters and selects candidate articles using:

- domain keyword detection
- rule-based scoring
- optional embedding fallback

**Stage 2 — Classification (LLM)**

Performs semantic analysis and outputs structured JSON.

## 3. Components

**main.py**

Orchestrates the pipeline and processes each article.

**io_csv.py**

Handles CSV input/output.

**config.py**

Stores thresholds, keywords, taxonomy, and model settings.

**triage.py**

Implements deterministic filtering logic:

- domain gate
- keyword scoring
- embedding fallback (for borderline cases)

**prompt_builder.py**

Constructs the classification prompt with strict instructions.

**classifier.py**

Handles LLM calls and parses structured output.

**scoring.py**

Computes:

- risk_score
- confidence

## 4. Triage Logic

Triage reduces noise before LLM usage.

**Steps:**

1. Domain Gate → rejects non-relevant articles
2. Keyword Scoring:
   - strong: +2
   - medium: +1
   - speculative: -1
3. Decision:
   - strong → pass
   - borderline → embedding check
   - weak → reject

Embedding is only used for borderline cases.

## 5. Classification

The LLM receives:

- article text
- triage hints
- strict prompt constraints

It outputs structured fields:

- event labels
- component scores
- rationale
- keywords

## 6. Scoring

Final metrics are computed deterministically:

- risk_score from:
  - physical
  - escalation
  - evidence
- confidence from:
  - evidence
  - signal
  - model certainty

This ensures consistency and reproducibility.

## 7. Error Handling

Failures are handled per article:

- pipeline continues
- fallback values assigned
- no batch interruption

## 8. Design Rationale

Key choices:

- deterministic filtering before LLM → higher precision, lower cost
- embeddings only for edge cases → controlled recall improvement
- scoring outside LLM → exact compliance with specification

## 9. Summary

The architecture is a simple two-stage pipeline:

1. deterministic triage filters input
2. LLM performs structured reasoning
3. deterministic scoring produces final outputs
