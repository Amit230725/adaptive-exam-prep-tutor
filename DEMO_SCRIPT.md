# ConceptPilot — 2-Minute Hackathon Demo Script

> **Target Audience:** Hackathon Judges & Evaluators  
> **Estimated Delivery:** 120 Seconds  
> **Core Theme:** *"Finds why you got it wrong, not just that you did."*

---

### [0:00 – 0:20] Hook & The Problem
**Speaker:**
> *"Judges, when students use chat-based AI tutors, studies suggest the AI often gives away the answer or acts like a reactive search engine. But on CBSE Class 10 board exams, questions are increasingly competency-based. A student can choose a correct option by luck, or miss an answer due to an arithmetic slip while having sound physics intuition.*
>
> *Meet **ConceptPilot**: an adaptive exam-prep tutor that diagnoses **why** you got an answer wrong by analyzing your underlying physical reasoning against published cognitive research."*

---

### [0:20 – 0:45] The 8-Topic Diagnostic & Concept Graph
*(Action: Start on the Welcome screen. Enter nickname "Aarav". Click "Start Diagnostic Test".)*

**Speaker:**
> *"We start with an 8-topic baseline diagnostic across the NCERT Electricity syllabus. Notice that on every attempt, we require a brief one-line explanation.
>
> Look at the starting map generated at the end of the diagnostic. This interactive graph visualizes the student's prerequisite hierarchy: from Electric Charge up to Series, Parallel, and Power. The node colors dynamically reflect starting mastery: green for mastered, amber for developing, red for gaps."*

---

### [0:45 – 1:15] Reasoning Diagnosis, Socratic Hint & Adaptive Selection
*(Action: Transition to "Begin Adaptive Practice". Show question selection banner. Select a wrong option with flawed reasoning, e.g. "The bulb consumes current".)*

**Speaker:**
> *"Look at this top banner: ConceptPilot explains **why** this question was chosen: 'Prerequisite Potential Difference is weaker than Ohm's Law—reinforcing foundation first'.
>
> Now watch what happens when I answer with a classic physics misconception: 'The bulb uses up current'. 
>
> ConceptPilot doesn't give me the answer. It gives me a **Socratic hint** and unlocks **one retry**.
>
> After the retry, look at the **AI at Work** panel: Gemini 2.5 Flash analyzed my explanation, cited exact evidence from my sentence, and tagged it with **M1 from the McDermott & Shaffer research library**. Even if a student gets the answer right through flawed reasoning, ConceptPilot catches it and discounts the mastery gain."*

---

### [1:15 – 1:35] Spaced Repetition (FSRS) Demo
*(Action: Direct attention to the sidebar mastery bars. Click the "+3 Days" demo button.)*

**Speaker:**
> *"Cognitive research shows that without review, memory stability decays. ConceptPilot implements an FSRS-inspired retrievability model.
>
> Watch what happens when I click our demo control: **'+3 Days'**. 
>
> Notice that Potential Difference immediately flags as **'DUE NOW'**. The next-question selector immediately reprioritizes this concept for spaced retrieval."*

---

### [1:35 – 1:55] Teacher Dashboard & AI Reteach Plan (Call D)
*(Action: Click the "Teacher Dashboard" tab. Enter PIN `teacher123`. Toggle "Include simulated benchmark class".)*

**Speaker:**
> *"Now let's switch to the Teacher Dashboard. Real pilot data is kept segregated from benchmark data by default. When we toggle on the benchmark class, we see a live cognitive heatmap across all students.
>
> We immediately spot our cohort's biggest hurdle: Parallel Circuits. 
>
> With one click on **'Generate Remedial Plan'**, our Call D AI synthesizes anonymous class metrics into an actionable 3-point lesson plan with active 5-minute demonstrations, teacher instructions, and Socratic check questions."*

---

### [1:55 – 2:00] Wrap-up & Honest Limits
**Speaker:**
> *"ConceptPilot runs live today on Streamlit with zero login, strict prompt-injection defenses, dual-pass AI self-verification, and complete offline fallbacks. Thank you!"*
