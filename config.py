from __future__ import annotations

import os
from typing import Dict, List

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

USE_EMBEDDING_FALLBACK = True
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_SIMILARITY_THRESHOLD = 0.62

TRIAGE_STRONG_THRESHOLD = 4
TRIAGE_BORDERLINE_THRESHOLD = 2

MAX_ARTICLE_CHARS_FOR_LLM = 12000
MAX_ARTICLE_CHARS_FOR_EMBEDDING = 2500

# Domain anchors ensure the article is actually in the target geopolitical context.
# This prevents unrelated macro/news events from passing triage just because they
# mention shipping, pipelines, sabotage, etc.
DOMAIN_KEYWORDS = [
    "iran",
    "iranian",
    "irgc",
    "irgc navy",
    "israel",
    "israeli",
    "u.s.",
    "united states",
    "american",
    "americans",
    "houthis",
    "houthi",
    "strait of hormuz",
    "hormuz",
    "red sea",
    "bab el-mandeb",
    "saudi",
    "uae",
    "emirati",
    "fujairah",
    "abqaiq",
    "ras tanura",
    "kharg",
    "khark",
    "gulf",
    "persian gulf",
]

EVENT_TAXONOMY: Dict[str, Dict[str, List[str]]] = {
    "Hormuz Closure": {
        "strong_keywords": [
            "strait of hormuz",
            "hormuz",
            "mine",
            "naval mine",
            "mining",
            "tanker attack",
            "vessel attack",
            "ship attack",
            "shipping halt",
            "transit halt",
            "blockade",
            "war risk insurance",
            "insurance spike",
            "irgc navy",
            "naval incident",
        ],
        "medium_keywords": [
            "shipping",
            "tanker",
            "vessel",
            "transit",
            "gulf shipping",
            "maritime traffic",
        ],
    },
    "Kharg/Khark Attack or Seizure": {
        "strong_keywords": [
            "kharg",
            "khark",
            "oil terminal",
            "export terminal",
            "amphibious landing",
            "seize",
            "seized",
            "takeover",
            "taken over",
            "capture",
            "captured",
            "export halt",
            "loading stop",
            "offshore facilities",
            "loading jetty",
        ],
        "medium_keywords": [
            "terminal",
            "landing",
            "offshore",
            "loading",
            "exports",
        ],
    },
    "Critical Gulf Infrastructure Attacks": {
        "strong_keywords": [
            "refinery",
            "oil facility",
            "processing plant",
            "gas plant",
            "lng terminal",
            "desalination",
            "water plant",
            "pipeline",
            "pumping station",
            "fujairah",
            "abqaiq",
            "ras tanura",
            "drone strike",
            "drone attack",
            "missile strike",
            "missile attack",
            "sabotage",
        ],
        "medium_keywords": [
            "saudi",
            "uae",
            "facility",
            "energy infrastructure",
            "oil infrastructure",
            "gas infrastructure",
        ],
    },
    "Direct Entry of Saudi/UAE/Coalition Forces": {
        "strong_keywords": [
            "coalition",
            "multinational force",
            "ground forces",
            "troop deployment",
            "amphibious operation",
            "saudi intervention",
            "uae intervention",
            "joint operation",
            "allied response",
            "regional war",
        ],
        "medium_keywords": [
            "escalation",
            "troops",
            "forces",
            "allies",
            "intervention",
        ],
    },
    "Red Sea / Bab el-Mandeb Escalation": {
        "strong_keywords": [
            "houthis",
            "houthi attacks",
            "red sea",
            "bab el-mandeb",
            "merchant vessels",
            "cargo ships",
            "shipping reroute",
            "diversion",
            "naval escort",
            "convoy",
        ],
        "medium_keywords": [
            "merchant ship",
            "cargo ship",
            "shipping route",
            "escort",
            "reroute",
        ],
    },
}

SPECULATIVE_TERMS = [
    "may",
    "could",
    "might",
    "warning",
    "warned",
    "threat",
    "threatened",
    "fear",
    "fears",
    "possible",
    "hypothetical",
    "scenario",
    "analysts say",
    "commentary",
    "opinion",
]

EVENT_PROTOTYPES = {
    "Hormuz Closure": [
        "Confirmed disruption of shipping through the Strait of Hormuz.",
        "Tanker attack or naval mining causing transit interruption in Hormuz.",
    ],
    "Kharg/Khark Attack or Seizure": [
        "Attack, seizure, or export halt at the Kharg oil export terminal.",
    ],
    "Critical Gulf Infrastructure Attacks": [
        "Drone or missile strike on Saudi or UAE refinery, pipeline, gas plant, or LNG terminal.",
    ],
    "Direct Entry of Saudi/UAE/Coalition Forces": [
        "Saudi or UAE military intervention, coalition formation, or troop deployment in a wider regional conflict.",
    ],
    "Red Sea / Bab el-Mandeb Escalation": [
        "Houthi attacks on merchant vessels in the Red Sea or Bab el-Mandeb causing shipping disruption.",
    ],
}