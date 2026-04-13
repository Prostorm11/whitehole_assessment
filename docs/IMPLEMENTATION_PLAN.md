# IMPLEMENTATION_PLAN.md

## Purpose

This document explains how the system was implemented, including the main design decisions, trade-offs, and reasoning behind them.

The focus is on how the specification was translated into a practical and robust solution.

---

## 1. Implementation Strategy

The system was implemented incrementally in the following order:

1. Define configuration and taxonomy (`config.py`)
2. Implement CSV input/output (`io_csv.py`)
3. Build deterministic triage (`triage.py`)
4. Implement LLM classification (`classifier.py`)
5. Add deterministic scoring (`scoring.py`)
6. Integrate all components (`main.py`)
7. Add error handling and robustness improvements

This approach ensured that a working deterministic pipeline was established before adding the LLM.

---

## 2. Triage Design Decisions

### Domain Filtering

A domain keyword gate was introduced before keyword scoring.

Reason:
- ensures articles are within the Iran / US / Israel context  
- prevents unrelated macroeconomic news from passing  

Trade-off:
- slightly lower recall  
- significantly higher precision  

---

### Rule-Based Scoring

Keyword scoring was implemented as:
- strong keywords → +2  
- medium keywords → +1  
- speculative terms → -1  

Reason:
- simple and interpretable  
- easy to tune  
- fully deterministic  

---

### Embedding Fallback

A semantic fallback using Sentence Transformers is applied only to borderline cases.

Reason:
- captures relevant articles with different wording  
- improves recall without weakening precision  

Additional benefit:
- runs locally, avoiding external embedding API calls  

---

## 3. Classification Design Decisions

### Use of OpenAI Responses API

The classification stage uses the OpenAI Responses API, as required.

Reason:
- aligns with specification  
- provides strong reasoning capabilities  

---

### Structured Output Strategy

The intended design was to enforce schema-level structured output.

In practice, the implementation uses:
- strict prompt instructions  
- deterministic JSON parsing  

Reason:
- ensures compatibility across environments  
- avoids dependency on SDK-specific features  
- remains robust for batch processing  

---

## 4. Deterministic Scoring

Final scores are computed in Python rather than by the model.

### Risk Score
Based on:
- physical disruption  
- escalation breadth  
- evidence strength  

### Confidence
Based on:
- evidence clarity  
- signal consistency  
- model certainty  

Reason:
- guarantees exact compliance with specification formulas  
- ensures reproducibility  
- avoids model inconsistency  

---

## 5. Error Handling

The system is designed for robust batch execution.

If classification fails:
- the pipeline continues  
- the article receives fallback outputs  
- the failure is recorded in the rationale  

Reason:
- prevents full pipeline failure  
- ensures all rows are processed  

---

## 6. Prompt Design

The prompt was iteratively refined to improve:

- precision (avoid over-classification)  
- consistency (stable outputs)  
- structure (valid JSON responses)  

Key constraints included:
- restricted label space  
- conservative classification behavior  
- explicit output format  

---

## 7. Assumptions

- Articles are written in English  
- Input CSV follows the required schema  
- Keyword taxonomy is sufficient for initial filtering  
- LLM can follow structured prompt instructions  

---

## 8. Limitations

- Keyword matching may miss some linguistic variations  
- Domain filtering may reject rare edge cases  
- Embedding fallback is limited to simple similarity matching  
- Output structure depends on prompt compliance  

---

## 9. Possible Improvements

- Use named entity recognition for stronger domain detection  
- Expand semantic filtering in triage  
- Add evaluation dataset for calibration  
- Enable strict schema enforcement once SDK support is stable  

---

## 10. Summary

The implementation focuses on:

- high precision through deterministic filtering  
- controlled use of LLM for reasoning  
- reproducible scoring outside the model  
- robustness for batch processing  

The final system is simple, reliable, and aligned with the specification.