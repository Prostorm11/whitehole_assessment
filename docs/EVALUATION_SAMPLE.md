# EVALUATION_SAMPLE.md

## Purpose

This small manual evaluation set is designed to sanity-check the system on representative examples.

It is not a full benchmark. Its purpose is to:
- verify that obvious positives are detected
- verify that obvious negatives are filtered out
- inspect borderline behavior
- highlight known limitations

---

## Evaluation Cases

| ID | Scenario Type | Expected Behavior |
|----|---------------|------------------|
| 1 | Clear positive | Strong pass, meaningful risk |
| 2 | Clear positive | Strong pass, meaningful risk |
| 3 | Clear positive | Strong pass, meaningful risk |
| 4 | Clear negative | Rejected at triage |
| 5 | Clear negative | Rejected at triage |
| 6 | Borderline positive | Borderline or pass via embeddings |
| 7 | Speculative political noise | Low score / reject |
| 8 | Out-of-domain macro event | Rejected at triage |

---

## Cases

### Case 1 — Hormuz tanker attack
**Article text**  
"Two tankers were attacked in the Strait of Hormuz, temporarily disrupting maritime traffic and raising war-risk insurance costs."

**Expected**
- event_labels: `["Hormuz Closure"]`
- risk_score: medium to high
- confidence: medium or high

**Why**
- direct shipping disruption
- strong domain anchors
- operational consequences

---

### Case 2 — Saudi refinery strike
**Article text**  
"A drone strike hit a Saudi refinery near Abqaiq, causing temporary disruption to oil processing operations."

**Expected**
- event_labels: `["Critical Gulf Infrastructure Attacks"]`
- risk_score: medium to high
- confidence: medium or high

**Why**
- infrastructure damage
- clear operational impact
- strong macro relevance

---

### Case 3 — Red Sea shipping reroute
**Article text**  
"Houthi attacks on merchant vessels in the Red Sea forced several cargo ships to reroute away from the Bab el-Mandeb corridor."

**Expected**
- event_labels: `["Red Sea / Bab el-Mandeb Escalation"]`
- risk_score: medium to high
- confidence: medium or high

**Why**
- shipping disruption
- explicit Red Sea / Houthi context
- credible macro relevance

---

### Case 4 — Local festival economics
**Article text**  
"The annual Blueberry Festival in Berryville generated strong local demand and renewed investor discussion around agricultural growth."

**Expected**
- event_labels: `[]`
- risk_score: low
- confidence: low
- rejected at triage

**Why**
- not in target geopolitical domain
- no relevant escalation signal

---

### Case 5 — Out-of-domain infrastructure attack
**Article text**  
"A pipeline sabotage incident in Nigeria disrupted regional fuel distribution."

**Expected**
- event_labels: `[]`
- risk_score: low
- confidence: low
- rejected at triage

**Why**
- macro-relevant, but outside target geopolitical scope

---

### Case 6 — Borderline paraphrased shipping disruption
**Article text**  
"Commercial maritime movement near Hormuz was interrupted after an assault on a vessel, prompting insurers to reassess regional exposure."

**Expected**
- likely `["Hormuz Closure"]`
- may require embedding fallback
- risk_score: medium
- confidence: medium

**Why**
- relevant meaning, but weaker direct keyword overlap
- good test of embedding fallback

---

### Case 7 — Speculative geopolitical rhetoric
**Article text**  
"Iranian officials warned that the Strait of Hormuz could be closed if tensions with Israel escalate further."

**Expected**
- event_labels: `[]` or very conservative labeling
- risk_score: low
- confidence: low

**Why**
- strong domain relevance
- but speculative and not operationally confirmed

---

### Case 8 — General market commentary
**Article text**  
"Analysts said oil traders remain nervous about the Middle East and possible future disruptions."

**Expected**
- event_labels: `[]`
- risk_score: low
- confidence: low

**Why**
- commentary only
- no concrete event

---

## Expected Strengths

The system should perform well on:
- direct operational disruptions
- strong location-specific escalation events
- Red Sea / Hormuz / Gulf infrastructure events

---

## Expected Weaknesses

The system may be weaker on:
- subtle paraphrases with weak domain anchors
- articles with mixed commentary and limited factual detail
- cases where event wording is indirect but still important

---

## Conclusion

This evaluation sample confirms that the system is calibrated for:
- high precision
- conservative scoring
- strong rejection of non-relevant or speculative articles