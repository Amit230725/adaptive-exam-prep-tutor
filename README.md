# ⚡ ConceptPilot
> *"Finds why you got it wrong, not just that you did."*

An adaptive exam-prep tutor with a cognitive learner model for **CBSE Class 10 Science — Chapter 11 "Electricity" (NCERT)**.

Built for the online hackathon under the problem statement: *"Adaptive exam-prep tutor with a learner model."*

---

## 🌟 Key Differentiators

Most AI tutoring tools either dump the full answer onto the student or act reactively like a search engine. Furthermore, multiple-choice quizzes often hide critical conceptual gaps: a student can easily guess the right answer by luck or hold a misconception that happens to cancel out.

**ConceptPilot solves this through research-grounded cognitive design:**
1. **Reasoning-Based Diagnosis:** Requires a brief one-line reason on every attempt. AI evaluates the student's *explanation* against published Physics Education Research (PER) misconceptions (`M1`–`M7`), catching misconceptions even on *correct* answers.
2. **Dual-Pass Question Generation:** Generates new questions targeted at the student's specific misconception, self-verified by an independent second AI solver pass (at temperature 0.0) before presentation.
3. **Prerequisite Propagation:** Models syllabus prerequisites (Charge &rarr; Current/PD &rarr; Ohm's Law &rarr; Resistance &rarr; Series/Parallel &rarr; Power). If foundational concepts are weak, effective mastery of dependent concepts is temporarily discounted by up to 15% to reinforce fundamentals first.
4. **Empirical Rasch IRT Calibration:** Rather than relying on unreliable LLM difficulty estimates, item difficulty $b$ calibrates dynamically from real student response distributions.
5. **Teacher Reteach Planner:** Synthesizes class-wide diagnostic data into an actionable 3-point remedial lesson plan with 5-minute active demonstrations.

---

## 🧩 The 7 Mandatory Hackathon Components

| # | Mandatory Component | Implementation in ConceptPilot |
|---|---|---|
| **1** | **Diagnostic Test** | 8-question standardized baseline across all syllabus topics in prerequisite sequence at Level 2 difficulty. Generates starting knowledge map. |
| **2** | **Concept Graph** | Visualized via Graphviz (`st.graphviz_chart`). Node colors dynamically reflect mastery (🟢 Mastered $\ge 70\%$, 🟡 Developing $40\%-69\%$, 🔴 Gap $<40\%$). |
| **3** | **Learner Model** | 4-parameter Bayesian Knowledge Tracing (`prior=0.30`, `guess=0.25`, `slip=0.10`, `learn=0.12`). Applies only 30% mastery gain if a correct answer hides a misconception. |
| **4** | **Targeted Generation & Calibration** | Gemini Call A generates questions at calibrated difficulty (Level 1, 2, or 3), verified by Call A2 solver pass. Difficulty $b$ calibrated online via Rasch IRT model. |
| **5** | **Misconception Detection** | Gemini Call B evaluates reasoning against research library `M1`–`M7`. Call C issues follow-up probes for `UNCLEAR` reasoning. Rule-based offline fallback. |
| **6** | **Spaced Repetition** | FSRS-inspired memory model tracking stability $S$ and retrievability $R(t) = 0.9^{t/S}$. Reviews triggered at $R \le 90\%$. Interactive `+1 Day` / `+3 Days` demo controls. |
| **7** | **Teacher Dashboard** | PIN-protected (`teacher123`) analytics portal with class heatmaps, risk thresholds, misconception frequencies, Call D AI remedial planner, and CSV export. |

---

## 🔬 Research Misconception Reference Library (M1 – M7)

Derived from published Physics Education Research (McDermott & Shaffer, 1992; Shipstone, 1988; Engelhardt & Beichner, 2004):

- **M1:** Current is "used up" as it passes through a bulb or resistor.
- **M2:** Battery is a constant-current source (current does not depend on the circuit).
- **M3:** Confuses current, voltage, and/or electrical energy.
- **M4:** Battery manufactures or stores charge that runs out.
- **M5:** Adding resistors in parallel increases total resistance.
- **M6:** Resistance depends on the applied voltage or current.
- **M7:** In parallel, current splits equally regardless of branch resistance.

---

## 🛠️ Tech Stack & Architecture

- **Frontend & App Framework:** Streamlit (Python 3.11 / 3.14 compatible).
- **AI Engine:** Google Gemini 2.5 Flash via official `google-genai` SDK.
- **Data Persistence:** Thread-safe SQLite (`data/cp.db`) via `threading.Lock`.
- **Graphing & Visualization:** Graphviz DOT rendered client-side, Altair/Streamlit native charts.
- **Data Processing:** Pandas, NumPy.
- **Testing:** Pytest (19 unit & benchmark tests).

### Project Directory Structure
```
conceptpilot/
├── app.py                      # Main Streamlit application
├── core/
│   ├── concepts.py             # 8-topic syllabus graph & M1-M7 research library
│   ├── bank.py                 # 24 verified CBSE MCQs with distractor tags
│   ├── learner.py              # Bayesian Knowledge Tracing & adaptive selector
│   ├── calibration.py          # Rasch IRT item difficulty calibration
│   ├── scheduler.py            # FSRS-inspired spaced repetition scheduler
│   ├── ai.py                   # Gemini Calls A, A2, B, C, D with safety & caching
│   ├── db.py                   # Thread-safe SQLite store & class queries
│   └── sim.py                  # Seeded 20-student benchmark class [SIMULATED]
├── scripts/
│   └── eval_synthetic.py       # 7-student synthetic benchmark recovery check
├── tests/
│   ├── test_core.py            # Learner model, BKT, Rasch & FSRS unit tests
│   ├── test_ai.py              # AI fallbacks, caching, and sanitization tests
│   ├── test_sim_and_db.py      # Simulation reproducibility and DB tests
│   └── test_eval.py            # Synthetic benchmark runner test
├── .streamlit/
│   └── config.toml             # Theme palette & layout styling
├── requirements.txt            # Pinned dependencies
├── DEMO_SCRIPT.md              # 2-minute hackathon judge demo script
├── SUBMISSION_WRITEUP.md       # Rubric-aligned submission write-up
├── SCREENSHOTS_GUIDE.md        # Submission & LinkedIn visual asset guide
└── README.md                   # Complete documentation
```

---

## 🚀 Quickstart: Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/your-username/conceptpilot.git
cd conceptpilot
```

### 2. Set up virtual environment & install dependencies
```bash
python -m venv .venv

# On Windows:
.\.venv\Scripts\activate
pip install -r requirements.txt

# On macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Unit Tests & Synthetic Benchmark
```bash
python -m pytest tests/
python scripts/eval_synthetic.py
```
*(All 19 tests pass; benchmark verifies 100% recovery of planted PER misconceptions).*

### 4. Launch the Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

*(Optional: Set your Gemini API key via `export GEMINI_API_KEY="your-key"` or enter it directly in the app sidebar. If no key is provided, the app runs seamlessly in offline verified mode).*

---

## ☁️ Deployment Guide (Streamlit Community Cloud)

1. Push this repository to GitHub (ensure `.gitignore` excludes `data/*.db` and secrets).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and click **"New app"**.
3. Select your repository, branch `main`, and main file path: `app.py`.
4. Under **Advanced settings &rarr; Secrets**, configure:
   ```toml
   GEMINI_API_KEY = "your-gemini-api-key"
   GEMINI_MODEL = "gemini-2.5-flash"
   TEACHER_PIN = "teacher123"
   ```
5. Click **"Deploy"**. The application will deploy publicly with mobile and desktop support.

---

## ⚖️ Honest Limits, Ethics & Privacy

- **Formative Learning Companion:** ConceptPilot is an adaptive diagnostic practice prototype, not an officially certified or standardized summative board examination.
- **Human-in-the-Loop:** While all AI-generated questions undergo independent solver verification, final teacher review is always recommended for classroom deployment.
- **Simulated Data Transparency:** Benchmark student data is explicitly tagged `[SIMULATED]`. Real pilot student data is segregated and displayed separately by default.
- **Privacy by Design:** Zero personally identifiable information (PII) is requested or stored. Students participate using anonymous nicknames, and a one-click **"Delete My Data"** option provides complete GDPR compliance.

---

## 📄 License
MIT License. Built for educational innovation.
