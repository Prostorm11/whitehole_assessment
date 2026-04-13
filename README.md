# Geopolitical Escalation News Classifier

## Overview
This project processes a CSV of English-language news articles and identifies events related to potential geopolitical escalation involving Iran, the US, and Israel.

The system is designed for **high precision** and distinguishes between:
- general political noise
- real events with possible macroeconomic relevance

## Pipeline

### Stage 1: Triage
A rule-based keyword filter identifies strong candidates using the provided event taxonomy.

To reduce false negatives caused by wording variation, borderline articles can optionally be checked using embedding similarity against event prototypes.

### Stage 2: Structured LLM Classification
Candidate articles are sent to the OpenAI API for structured classification.

The model outputs:
- event labels
- physical disruption severity
- escalation breadth
- evidence strength
- signal consistency
- model certainty
- rationale
- matched keywords

### Final Scoring
The script computes the final scores in Python.

#### Risk score
risk_score = 0.45 * physical_score + 0.35 * escalation_score + 0.20 * evidence_score

#### Confidence score
confidence_score = 0.50 * evidence_score + 0.30 * signal_score + 0.20 * model_score

The final confidence label is:
- high
- medium
- low

## Input schema
Required CSV columns:
- pubDate
- link
- content
- source_id

## Output schema
The output CSV preserves all input rows and adds:
- event_labels
- risk_score
- confidence
- rationale
- keywords_detected

## Installation

```bash
pip install pandas openai sentence-transformers torch