# ⚡ ConceptPilot
> *"Finds why you got it wrong, not just that you did."*

An adaptive exam-prep tutor with a cognitive learner model for the **Entire CBSE Class 10 Science Physics Syllabus (NCERT)**:
- **Chapter 9:** Light – Reflection and Refraction
- **Chapter 10:** The Human Eye and the Colourful World
- **Chapter 11:** Electricity
- **Chapter 12:** Magnetic Effects of Electric Current

Built for the online hackathon under the problem statement: *"Adaptive exam-prep tutor with a learner model."*

---

## 🌟 Key Differentiators

Most AI tutoring tools either dump the full answer onto the student or act reactively like a search engine. Furthermore, multiple-choice quizzes often hide critical conceptual gaps: a student can easily guess the right answer by luck or hold a misconception that happens to cancel out.

**ConceptPilot solves this through research-grounded cognitive design:**
1. **Reasoning-Based Diagnosis:** Requires a brief one-line reason on every attempt. AI evaluates the student's *explanation* against published Physics Education Research (PER) misconceptions (`M1`–`M17`), catching misconceptions even on *correct* answers.
2. **Complete 4-Chapter Syllabus Coverage:** 20 concepts across Optics, Vision, Circuits, and Electromagnetism with 60 verified CBSE NCERT questions (3 per concept across Levels 1, 2, 3).
3. **Dual-Pass Question Generation:** Generates new questions targeted at the student's specific misconception, self-verified by an independent second AI solver pass (at temperature 0.0) before presentation.
4. **Prerequisite Propagation:** Models syllabus prerequisites across all 4 chapters. If foundational concepts are weak, effective mastery of dependent concepts is temporarily discounted by up to 15% to reinforce fundamentals first.
5. **Empirical Rasch IRT Calibration:** Rather than relying on unreliable LLM difficulty estimates, item difficulty $b$ calibrates dynamically from real student response distributions.
6. **Teacher Reteach Planner:** Synthesizes class-wide diagnostic data into an actionable 3-point remedial lesson plan with 5-minute active demonstrations.
7. **Interactive Virtual Circuit Laboratory & Cognitive Radar:** Pure SVG multi-axis cognitive radar chart and live virtual circuit simulation for instant misconception busting.

---

## 🧩 The 7 Mandatory Hackathon Components

| # | Mandatory Component | Implementation in ConceptPilot |
|---|---|---|
| **1** | **Diagnostic Test** | Multi-scope baseline diagnostic: choose a specific chapter or a balanced 8-question cross-chapter diagnostic spanning all 4 Class 10 Physics chapters. |
| **2** | **Concept Graph** | Visualized via Graphviz (`st.graphviz_chart`). Filterable by chapter or full syllabus. Node colors dynamically reflect mastery (🟢 Mastered $\ge 70\%$, 🟡 Developing $40\%-69\%$, 🔴 Gap $<40\%$). |
| **3** | **Learner Model** | 4-parameter Bayesian Knowledge Tracing (`prior=0.30`, `guess=0.25`, `slip=0.10`, `learn=0.12`). Applies only 30% mastery gain if a correct answer hides a misconception. |
| **4** | **Targeted Generation & Calibration** | Gemini Call A generates questions at calibrated difficulty (Level 1, 2, or 3), verified by Call A2 solver pass. Difficulty $b$ calibrated online via Rasch IRT model. |
| **5** | **Misconception Detection** | Gemini Call B evaluates reasoning against research library `M1`–`M17`. Call C issues follow-up probes for `UNCLEAR` reasoning. Rule-based offline fallback. |
| **6** | **Spaced Repetition** | FSRS-inspired memory model tracking stability $S$ and retrievability $R(t) = 0.9^{t/S}$. Reviews triggered at $R \le 90\%$. Interactive `+1 Day` / `+3 Days` demo controls. |
| **7** | **Teacher Dashboard** | PIN-protected (`teacher123`) analytics portal with chapter filters, class heatmaps, cohort radar charts, individual student drill-down, Call D AI remedial planner, and CSV export. |

---

## 🔬 Research Misconception Reference Library (M1 – M17)

Derived from published Physics Education Research (McDermott, Shaffer, Goldberg, Galili, Maloney et al.):

### Chapter 11: Electricity
- **M1:** Current is "used up" as it passes through a bulb or resistor.
- **M2:** Battery is a constant-current source (current does not depend on the circuit).
- **M3:** Confuses current, voltage, and/or electrical energy.
- **M4:** Battery manufactures or stores charge that runs out.
- **M5:** Adding resistors in parallel increases total resistance.
- **M6:** Resistance depends on the applied voltage or current.
- **M7:** In parallel, current splits equally regardless of branch resistance.

### Chapter 9: Light – Reflection & Refraction
- **M8:** Image is located on the surface of the mirror/lens rather than at ray intersection in space.
- **M9:** Covering half a lens cuts the image in half (rather than dimming full image).
- **M10:** Focal length varies with object position or image distance.
- **M11:** Believes light slows down or stops as it travels further in air.

### Chapter 10: The Human Eye and Colourful World
- **M12:** Confuses myopia with hypermetropia (or prescribes convex lens for myopia).
- **M13:** Believes the eye sees by projecting active vision rays outwards towards objects.
- **M14:** Believes a glass prism dyes or creates colors rather than separating existing wavelengths.

### Chapter 12: Magnetic Effects of Electric Current
- **M15:** Believes cutting a magnet in half isolates north and south monopoles.
- **M16:** Confuses Fleming's Left-Hand Rule (Motor force) with Right-Hand Rule (Induced current).
- **M17:** Believes magnetic field lines can cross each other in strong magnetic fields.

---

## 🛠️ Tech Stack & Architecture

- **Frontend & App Framework:** Streamlit (Python 3.11 / 3.14 compatible).
- **AI Engine:** Google Gemini 2.5 Flash via official `google-genai` SDK.
- **Data Persistence:** Thread-safe SQLite (`data/cp.db`) via `threading.Lock`.
- **Graphing & Visualization:** Graphviz DOT rendered client-side, SVG Cognitive Radar charts.
- **Data Processing:** Pandas, NumPy.
- **Testing:** Pytest (31 unit & benchmark tests, 100% passing).

---

## 🚀 Quickstart & How to Run

```powershell
# 1. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Run unit test suite
pytest tests/

# 3. Launch the web application
streamlit run app.py
```

Open `http://localhost:8501` in your browser. Demo PIN for teacher dashboard: `teacher123`.
