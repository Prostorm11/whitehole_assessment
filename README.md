# CHECK DETAILED INFORMATION (ARCHITECTURE,IMPLEMENTATION AND DATA_MODEL) FROM THE README UNDER DOCS FOLDER

# Geopolitical News Risk Detection with AI

## Overview

This project implements a system that analyzes news articles to detect geopolitical escalation events involving Iran, the United States, and Israel.

The system identifies events with potential macroeconomic impact, filters out background political noise, and produces structured outputs suitable for downstream use.

The design prioritizes **high precision**, ensuring that only meaningful signals are surfaced.

---

## Key Features

- Two-stage pipeline:
  - deterministic triage (filtering)
  - LLM-based classification
- Multi-label event classification
- Structured output (JSON-like fields in CSV)
- Deterministic risk and confidence scoring
- Cost-efficient design with local embeddings

---

## Event Categories

The system classifies articles into the following categories:

1. Hormuz Closure
2. Kharg/Khark Attack or Seizure
3. Critical Gulf Infrastructure Attacks
4. Direct Entry of Saudi/UAE/Coalition Forces
5. Red Sea / Bab el-Mandeb Escalation

---

## System Architecture

```text
Input CSV → Triage → LLM Classification → Scoring → Output CSV
```

- **Triage:** filters irrelevant articles using rules + optional embeddings
- **Classification:** uses OpenAI API to extract structured signals
- **Scoring:** computes final risk and confidence deterministically

---

## Installation

**1. Clone repository**

```bash
git clone <https://github.com/Prostorm11/whitehole_assessment>
cd <whitehole_assessment>
```

**2. Create virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate     # Mac/Linux
.venv\Scripts\activate        # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set environment variables**

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

---

## Usage

Run the pipeline:

```bash
python main.py --input data/newsdata.csv --output outputs/result.csv
```

---

## Input Format

The input CSV must contain:

| Field     | Description              |
|-----------|--------------------------|
| pubDate   | Publication datetime     |
| link      | Article URL              |
| content   | Full article text        |
| source_id | Source identifier        |

---

## Output Format

The output CSV includes:

| Field             | Description                         |
|-------------------|-------------------------------------|
| event_labels      | Detected event categories           |
| risk_score        | Final macro-risk score (0.00–1.00)  |
| confidence        | low / medium / high                 |
| rationale         | Short explanation of classification |
| keywords_detected | Relevant keywords identified        |

---

## Design Decisions

**High Precision Filtering**
- Domain-based filtering ensures relevance
- Keyword scoring reduces noise
- Speculative language is penalized

**Controlled Use of LLM**
- Only candidate articles are sent to the LLM
- Reduces cost and improves reliability

**Local Embedding Fallback**
- Sentence Transformers used for borderline cases
- Avoids external embedding API calls
- Improves recall without reducing precision

**Deterministic Scoring**
- Risk and confidence computed outside the model
- Ensures consistency and exact compliance with specification

---

## Limitations

- Keyword matching may miss some linguistic variations
- Domain filtering may reject rare edge cases
- LLM output depends on prompt adherence

---

## Possible Improvements

- Named Entity Recognition for stronger domain detection
- Expanded semantic filtering in triage
- Evaluation dataset for calibration
- Full schema enforcement via API (when supported)

---

## Project Structure

```
├── main.py
├── config.py
├── io_csv.py
├── triage.py
├── prompt_builder.py
├── classifier.py
├── scoring.py
├── utils.py
├── data/
├── outputs/
├── docs/
└── README.md
```

---

## Summary

This project implements a robust, high-precision system for detecting geopolitically significant events from news data using a combination of:

- deterministic filtering
- LLM-based reasoning
- structured outputs
- reproducible scoring

The solution is simple, efficient, and aligned with the provided specification.
