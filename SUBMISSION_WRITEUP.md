# ConceptPilot — Hackathon Submission Write-Up

> **Project Name:** ConceptPilot  
> **Tagline:** *"Finds why you got it wrong, not just that you did."*  
> **Target Curriculum:** CBSE Class 10 Science — Chapter 11 "Electricity" (NCERT)  
> **Live Web App:** Public Streamlit Deployment (No Login Required)

---

## 1. Problem Understanding & Educational Context (Score Weight: 20/100)
Recent learning-science literature reveals critical limitations in digital tutoring tools:
1. **Reactive Answer-Dumping:** Conventional generative chat tutors act reactively—either handing out complete solutions (which research shows impairs long-term retention) or withholding guidance completely (which leads to user abandonment).
2. **Hidden Misconceptions in Multiple-Choice Quizzes:** Standard quiz platforms only check whether the selected radio button matches the key. In STEM disciplines like physics, a student can easily guess the correct answer through flawed physical intuition (e.g. assuming a battery delivers fixed current).
3. **The Pitfall of LLM Difficulty Estimation:** Studies demonstrate that LLMs are poor judges of question difficulty. Psychometric difficulty must be calibrated empirically from real human response distributions.
4. **CBSE Board Exam Evolution:** CBSE Class 10 examinations have transitioned toward application- and competency-based questions. Diagnosing conceptual models is now vital for board success.

*Note: All claims in ConceptPilot adhere to evidence-based framing using "research suggests" rather than dogmatic assertions.*

---

## 2. Technical Architecture & Innovation (Score Weight: 15/100)
ConceptPilot introduces four major pedagogical differentiators:
- **Reasoning-Based Misconception Detection:** Evaluates the student's one-line natural language reasoning against a verified Physics Education Research (PER) taxonomy (`M1`–`M7`), detecting misconceptions even when the final choice is correct.
- **Flawed Reasoning BKT Discount:** Implements a 4-parameter Bayesian Knowledge Tracing model. If a student answers correctly while harboring an active misconception, they receive only 30% of the normal knowledge acquisition gain.
- **Prerequisite Propagation:** Models prerequisite graphs (Charge &rarr; Current/PD &rarr; Ohm's Law &rarr; Resistance &rarr; Series/Parallel &rarr; Power). Weak foundations temporarily penalize the effective mastery of dependent concepts by up to 15% to redirect practice upstream.
- **Rasch Item Response Theory Calibration:** Question difficulty parameter $b$ calibrates dynamically online via empirical gradient updates: $b \leftarrow b + 0.15 \times (P_{\text{expected}} - \text{outcome})$, stabilized by Bayesian shrinkage.

---

## 3. Generative AI Integration & Verification (Score Weight: 25/100)
Built with **Google Gemini 2.5 Flash** through the modern `google-genai` SDK:
- **Call A (Targeted Question Generation):** Crafts CBSE-style MCQs targeting active student misconceptions at calibrated difficulty levels.
- **Call A2 (Dual-Pass Self-Verification):** An independent solver pass solves generated questions blind to the key at temperature 0.0. Items are accepted into practice only if the solver matches the key.
- **Call B (Misconception Diagnosis):** Evaluates student reasoning against fixed research labels (`M1`–`M7`). Never invents labels.
- **Call C (Socratic Probing):** When reasoning is ambiguous (`UNCLEAR`), generates a single-sentence conceptual probe.
- **Call D (AI Reteach Plan):** Synthesizes anonymous cohort metrics into a 3-point remedial plan with 5-minute active demonstrations.
- **Safety & Fallbacks:** Strict JSON validation schemas, prompt-injection isolation tags, 300-char input capping, in-memory MD5 caching, and resilient offline rule-based fallbacks.

---

## 4. Prototype Quality, Mobile UX & Real-Life Readiness (Score Weight: 25/100)
- **Zero-Barrier Access:** Instant entry with nicknames; no passwords or personal data required.
- **High-Contrast Workbook Design:** Clean palette (amber `#F4A300` filament accent, `#14213D` ink, signal green `#1B998B`, alert red `#D1495B`).
- **Interactive Visual Hierarchy:** Live Graphviz concept DAG updates color dynamically with student mastery.
- **Mobile First:** Responsive CSS with minimum 44px touch targets on all buttons and radio choices.
- **Bilingual Interface:** Real-time English & हिन्दी UI localization toggle.
- **Teacher Dashboard:** PIN-protected portal featuring cohort heatmaps, risk metrics, misconception tables, Rasch calibration curves, and one-click CSV export.

---

## 5. LinkedIn Content & Engagement Plan (Score Weight: 15/100)
- **Hook Post:** *"Why getting the right answer on an exam question might actually be hiding a critical learning gap."*
- **Visuals:** Carousel featuring: (1) Graphviz live concept map, (2) The "AI at Work" reasoning diagnostic panel, (3) The Teacher class heatmap, (4) Call D AI remedial lesson plan.
- **Discussion Prompt:** Tagging STEM educators and CBSE teachers on the role of formative diagnostic AI vs. homework-solver bots.

---

## 6. Honest Limits & Privacy Disclaimers
- **Formative Prototype:** Designed as an adaptive study companion, not a certified summative board examination.
- **Teacher Oversight:** Recommends educator review for all generated questions.
- **Benchmark Transparency:** Simulated cohorts are explicitly marked `[SIMULATED]`; real student data is segregated.
- **Privacy by Design:** Zero PII collected; GDPR-compliant "Delete My Data" feature.
