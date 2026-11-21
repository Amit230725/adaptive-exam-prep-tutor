"""app.py - ConceptPilot: Adaptive Exam-Prep Tutor with a Learner Model

Tagline: "Finds why you got it wrong, not just that you did."
Target: Complete CBSE Class 10 Physics Syllabus (Light, Human Eye, Electricity, Magnetism)
AI Integration: Google Gemini 2.5 Flash via google-genai SDK
Design Theme: Modern Ed-Tech SaaS Dashboard (Reyhan Adinata aesthetic, Royal Cobalt Blue #2563EB)
"""

import os
import uuid
import streamlit as st
import pandas as pd

from core.concepts import (
    CONCEPTS,
    MISCONCEPTIONS,
    CHAPTERS,
    get_ordered_concepts,
    get_chapter_for_concept,
)
from core.bank import (
    QUESTION_BANK,
    get_diagnostic_questions,
    get_question_by_id,
    get_questions_for_concept,
)
from core.learner import (
    update_bkt,
    compute_effective_mastery,
    select_next_practice_concept,
    select_next_question,
    target_difficulty_for_mastery,
    DEFAULT_PRIOR,
)
from core.calibration import update_item_difficulty, format_calibration_summary
from core.scheduler import (
    initial_stability_from_mastery,
    compute_retrievability,
    is_due_for_review,
    update_concept_stability,
    get_due_concepts,
)
from core.db import (
    init_db,
    save_student,
    log_response,
    log_misconception_event,
    save_mastery_state,
    get_item_calibration,
    save_item_calibration,
    delete_student_data,
    get_available_classes,
    get_real_students_mastery,
    get_real_misconception_stats,
    get_all_calibrated_items,
)
from core.sim import generate_simulated_class, get_simulated_misconception_stats
from core.ai import (
    diagnose_reasoning,
    generate_followup_probe,
    generate_targeted_question,
    verify_generated_question,
    generate_reteach_plan,
    get_api_key,
    get_model_name,
)
from core.visuals import (
    generate_mastery_radar_chart_svg,
    generate_circular_progress_svg,
    generate_activity_barchart_svg,
    generate_evaluation_certificate_html,
    simulate_circuit,
    CONCEPT_STUDY_CARDS,
)

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ConceptPilot - Adaptive Physics Tutor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Reyhan Adinata Dribbble Modern EdTech SaaS Dashboard (#2563EB)
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');
  
  html, body, [class*="css"] {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      color: #0F172A;
  }
  
  h1, h2, h3, h4, h5 {
      font-family: 'Space Grotesk', sans-serif;
      color: #0F172A;
      letter-spacing: -0.02em;
  }
  
  .stApp {
      background-color: #F8FAFC;
  }
  
  /* Primary Action Buttons: Royal Cobalt Blue (#2563EB) */
  .stButton > button[kind="primary"] {
      background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
      color: #FFFFFF !important;
      border: 1px solid #1D4ED8 !important;
      font-weight: 600 !important;
      min-height: 44px !important;
      border-radius: 12px !important;
      box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
      transition: all 0.2s ease;
  }
  .stButton > button[kind="primary"]:hover {
      background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
      border-color: #1E40AF !important;
      box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3) !important;
      transform: translateY(-1px);
  }

  /* Secondary Buttons: Crisp Slate */
  .stButton > button:not([kind="primary"]) {
      background-color: #FFFFFF !important;
      color: #1E293B !important;
      border: 1px solid #E2E8F0 !important;
      min-height: 42px !important;
      border-radius: 12px !important;
      font-weight: 500 !important;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
      transition: all 0.15s ease;
  }
  .stButton > button:not([kind="primary"]):hover {
      background-color: #F1F5F9 !important;
      border-color: #CBD5E1 !important;
      color: #0F172A !important;
  }
  
  /* Tap target accessibility for radio options (minimum 44px) */
  div[role="radiogroup"] label {
      min-height: 46px !important;
      display: flex !important;
      align-items: center !important;
      padding: 8px 14px !important;
      border-radius: 10px !important;
      margin-bottom: 6px !important;
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      transition: all 0.15s ease;
  }
  div[role="radiogroup"] label:hover {
      background: #EFF6FF;
      border-color: #BFDBFE;
  }

  /* Dribbble Modern SaaS Card Aesthetic */
  .dribbble-card {
      background-color: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 18px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03), 0 1px 2px rgba(15, 23, 42, 0.05);
      transition: transform 0.15s ease, box-shadow 0.15s ease;
  }
  .dribbble-card:hover {
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
  }

  .stat-card {
      background-color: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 18px;
      padding: 20px 22px;
      box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
      height: 100%;
  }

  .stat-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
  }

  .stat-title {
      font-size: 13px;
      font-weight: 600;
      color: #64748B;
      text-transform: uppercase;
      letter-spacing: 0.5px;
  }

  .stat-icon {
      width: 38px;
      height: 38px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
  }
  .icon-blue { background: #EFF6FF; color: #2563EB; }
  .icon-amber { background: #FEF3C7; color: #D97706; }
  .icon-green { background: #ECFDF5; color: #059669; }
  .icon-purple { background: #F3E8FF; color: #7C3AED; }

  .stat-value {
      font-size: 28px;
      font-weight: 800;
      color: #0F172A;
      line-height: 1.1;
      margin-bottom: 4px;
  }

  .stat-sub {
      font-size: 12px;
      color: #64748B;
  }

  .dribbble-search {
      background-color: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 30px;
      padding: 10px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
      margin-bottom: 24px;
  }

  .cp-card {
      background-color: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 16px;
      padding: 22px 24px;
      margin-bottom: 16px;
      box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
  }
  
  .cp-banner {
      background-color: #EFF6FF;
      border-left: 4px solid #2563EB;
      padding: 14px 18px;
      border-radius: 8px;
      margin-bottom: 16px;
      font-size: 0.94rem;
      color: #1E40AF;
  }
  
  .cp-diagnosis-card {
      background-color: #EFF6FF;
      border-left: 4px solid #2563EB;
      padding: 16px 20px;
      border-radius: 10px;
      margin-top: 14px;
      margin-bottom: 14px;
  }

  .ai-work-panel {
      background-color: #F8FAFC;
      border: 1px solid #CBD5E1;
      border-radius: 10px;
      padding: 16px 20px;
      margin-top: 14px;
      font-size: 0.88rem;
  }
  
  .chip {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
      margin-right: 6px;
      text-transform: uppercase;
  }
  .chip-easy { background-color: #ECFDF5; color: #059669; }
  .chip-med { background-color: #FEF3C7; color: #D97706; }
  .chip-hard { background-color: #FEE2E2; color: #DC2626; }
  .chip-bank { background-color: #F1F5F9; color: #475569; }
  .chip-ai { background-color: #EFF6FF; color: #2563EB; border: 1px solid #BFDBFE; }
  .chip-verified { background-color: #DCFCE7; color: #15803D; }

  /* Mobile responsiveness */
  @media (max-width: 768px) {
      .dribbble-card, .cp-card, .cp-banner, .cp-diagnosis-card, .ai-work-panel {
          padding: 16px;
          margin-bottom: 12px;
      }
      .stButton > button {
          width: 100% !important;
      }
  }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# INTERNATIONALIZATION (I18N) & LOCALIZATION
# -----------------------------------------------------------------------------
I18N = {
    "en": {
        "title": "⚡ ConceptPilot",
        "tagline": "Finds why you got it wrong, not just that you did.",
        "start_diag": "Start Diagnostic Test 🚀",
        "submit_ans": "Submit Answer",
        "next_q": "Next Question ➡️",
        "hint_label": "💡 Socratic Hint:",
        "retry_remaining": "(You have 1 retry remaining)",
        "diag_header": "Diagnostic Test",
        "diag_complete": "🎯 Diagnostic Complete: Your Starting Knowledge Map",
        "begin_adapt": "Begin Adaptive Practice 🚀",
        "why_chosen": "Why this question was chosen:",
        "choose_opt": "Choose one option:",
        "one_line_reason": "Explain your reasoning in one line (Why did you choose this?):",
        "reason_placeholder": "e.g. Because electric charge is conserved and current cannot be consumed.",
        "correct_answer_label": "Correct Answer:",
        "explanation_label": "Explanation:",
        "curriculum_ref": "Curriculum Reference:",
        "diagnostic_insight": "🧠 Diagnostic Insight: Misconception Detected",
        "reasoning_sound": "✅ Scientific Reasoning Sound",
        "mastery_title": "Your Mastery Map",
        "streak_label": "Current Streak:",
        "demo_controls": "Demo Controls",
        "advance_time": "Advance simulated days to observe spaced repetition retrievability drop:",
        "reset_session": "🔄 Reset Session",
        "delete_data": "🗑️ Delete My Data",
    },
    "hi": {
        "title": "⚡ कांसेप्टपायलट (ConceptPilot)",
        "tagline": "यह समझता है कि उत्तर गलत क्यों हुआ, केवल यह नहीं कि गलत था।",
        "start_diag": "प्रारंभिक मूल्यांकन शुरू करें 🚀",
        "submit_ans": "उत्तर जमा करें",
        "next_q": "अगला प्रश्न ➡️",
        "hint_label": "💡 सुकराती संकेत (Socratic Hint):",
        "retry_remaining": "(आपके पास 1 पुनः प्रयास शेष है)",
        "diag_header": "प्रारंभिक मूल्यांकन (Diagnostic)",
        "diag_complete": "🎯 प्रारंभिक मूल्यांकन पूर्ण: आपका ज्ञान मानचित्र",
        "begin_adapt": "अनुकूली अभ्यास शुरू करें 🚀",
        "why_chosen": "यह प्रश्न क्यों चुना गया:",
        "choose_opt": "एक विकल्प चुनें:",
        "one_line_reason": "एक पंक्ति में कारण बताएं (आपने इसे क्यों चुना?):",
        "reason_placeholder": "उदाहरण: क्योंकि आवेश संरक्षित रहता है और धारा की खपत नहीं होती।",
        "correct_answer_label": "सही उत्तर:",
        "explanation_label": "व्याख्या (Explanation):",
        "curriculum_ref": "पाठ्यक्रम संदर्भ:",
        "diagnostic_insight": "🧠 नैदानिक अंतर्दृष्टि: भ्रांति पहचानी गई",
        "reasoning_sound": "✅ वैज्ञानिक तर्क सही है",
        "mastery_title": "आपकी प्रवीणता (Mastery)",
        "streak_label": "लगातार सही उत्तर (Streak):",
        "demo_controls": "डेमो नियंत्रण (Demo Controls)",
        "advance_time": "स्मृति क्षय (Spaced Repetition) देखने के लिए दिन आगे बढ़ाएं:",
        "reset_session": "🔄 सत्र रीसेट करें",
        "delete_data": "🗑️ मेरा डेटा हटाएं",
    }
}

# Initialize SQLite database
init_db()

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
s = st.session_state

if "student_id" not in s:
    s.student_id = f"stu_{uuid.uuid4().hex[:8]}"
    s.nickname = "Aarav"
    s.class_code = "CLASS-10A"
    s.phase = "dashboard"  # "dashboard", "diag", "diag_summary", "adapt"
    s.active_chapter = "all"  # "all", "light", "human_eye", "electricity", "magnetism"
    s.api_key_override = ""
    
    # Concept mastery values [0.0 to 1.0] across all 20 syllabus topics
    s.mastery = {cid: DEFAULT_PRIOR for cid in CONCEPTS}
    
    # Spaced Repetition (FSRS) state per concept
    s.schedule = {
        cid: {"stability": 1.0, "last_review_day": 0.0, "due_day": 0.0, "streak": 0}
        for cid in CONCEPTS
    }
    s.current_day = 0.0  # Fast-forwardable demo timeline
    
    # Diagnostic progression
    s.diag_questions = get_diagnostic_questions()
    s.diag_idx = 0
    s.diag_misconceptions_found = []
    
    # Active session state
    s.current_q = None
    s.selection_reason = ""
    s.attempt = 0
    s.last_result = None  # None, "retry", "done", "probe"
    s.last_diagnosis = None
    s.probe_question = None
    s.asked_ids = set()
    s.history = []
    s.active_misconceptions = {}  # concept -> mid
    s.teacher_auth = False
    s.reteach_plan = None
    s.lang = "en"

if "active_chapter" not in s:
    s.active_chapter = "all"

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS: GRAPH & EVALUATION
# -----------------------------------------------------------------------------
def render_concept_graph(mastery_dict, chapter_filter=None):
    """Generates Graphviz DOT string with node colors based on mastery, optionally filtered by chapter."""
    dot = [
        'digraph ConceptGraph {',
        '  rankdir=LR;',
        '  graph [bgcolor="transparent", pad="0.2", nodesep="0.4", ranksep="0.6"];',
        '  node [fontname="Helvetica", shape="box", style="filled,rounded", fontcolor="#FFFFFF", fontsize=11, height=0.6];',
        '  edge [color="#6B7280", penwidth=1.5, arrowsize=0.8];',
    ]
    if chapter_filter and chapter_filter in CHAPTERS:
        target_cids = set(CHAPTERS[chapter_filter]["concepts"])
    else:
        target_cids = set(CONCEPTS.keys())

    for cid in target_cids:
        data = CONCEPTS[cid]
        m = mastery_dict.get(cid, DEFAULT_PRIOR)
        if m >= 0.70:
            fill_color = "#10B981"  # Emerald Mastered
            badge = "Mastered"
        elif m >= 0.40:
            fill_color = "#F59E0B"  # Amber Developing
            badge = "Developing"
        else:
            fill_color = "#EF4444"  # Rose Needs Review
            badge = "Needs Review"
        
        c_title = data["name"].split("&")[0].split("(")[0].replace('"', '\\"').strip()
        dot.append(f'  "{cid}" [label="{c_title}\\n{int(m * 100)}% ({badge})", fillcolor="{fill_color}"];')
        for prereq in data.get("prerequisites", []):
            if prereq in target_cids:
                dot.append(f'  "{prereq}" -> "{cid}";')
            
    dot.append('}')
    return "\n".join(dot)

def compute_evaluation_metrics(mastery_dict, active_misc_dict):
    """Computes overall CBSE Board Readiness Index (0-100), predicted grade, and chapter breakdown."""
    avg_m = sum(mastery_dict.values()) / max(1, len(mastery_dict))
    score = int(round(avg_m * 100))
    score = max(5, min(99, score))

    if score >= 91:
        grade = "A1 · Outstanding (Top 5% Percentile)"
    elif score >= 81:
        grade = "A2 · Excellent (Top 15% Percentile)"
    elif score >= 71:
        grade = "B1 · Very Good (Board Merit Track)"
    elif score >= 61:
        grade = "B2 · Good (Solid Foundational Base)"
    elif score >= 51:
        grade = "C1 · Above Average"
    elif score >= 41:
        grade = "C2 · Average"
    else:
        grade = "D · Needs Intensive Remediation"

    ch_masteries = {}
    for ch_id, ch_data in CHAPTERS.items():
        c_vals = [mastery_dict.get(c, DEFAULT_PRIOR) for c in ch_data["concepts"]]
        ch_masteries[ch_id] = sum(c_vals) / max(1, len(c_vals))

    active_count = len(active_misc_dict)
    cleared_count = max(0, 17 - active_count)

    return score, grade, ch_masteries, cleared_count

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ ConceptPilot")
    st.caption("CBSE Class 10 Physics · Full Syllabus (4 Chapters)")
    
    # Language Selection (Hindi / English UI toggle)
    lang_val = st.radio("Language / भाषा:", ["English", "हिन्दी"], horizontal=True, index=0 if s.get("lang", "en") == "en" else 1)
    s.lang = "en" if lang_val == "English" else "hi"
    T = I18N[s.lang]
    st.markdown("---")

    # Syllabus / Chapter Scope Selector
    st.subheader("📚 Syllabus Scope")
    scope_options = ["all"] + list(CHAPTERS.keys())
    scope_labels = {
        "all": "🌐 Full Physics (All 4 Chapters)",
        "light": "💡 Ch 9: Light (Mirrors & Lenses)",
        "human_eye": "👁️ Ch 10: Human Eye & World",
        "electricity": "⚡ Ch 11: Electricity",
        "magnetism": "🧲 Ch 12: Magnetic Effects",
    }
    cur_scope = s.get("active_chapter", "all")
    sel_scope = st.selectbox(
        "Active Chapter Focus:",
        options=scope_options,
        index=scope_options.index(cur_scope) if cur_scope in scope_options else 0,
        format_func=lambda x: scope_labels.get(x, x),
        key="sb_chapter_sel"
    )
    if sel_scope != s.get("active_chapter", "all"):
        s.active_chapter = sel_scope
        s.current_q = None
        st.rerun()

    st.markdown("---")

    # AI Connection Status
    active_key = get_api_key(s.api_key_override)
    if active_key:
        st.success(f"🟢 **AI Connected** (`{get_model_name()}`)")
    else:
        st.warning("⚪ **AI Offline:** Using built-in verified questions")
        with st.expander("🔑 Configure Gemini API Key"):
            custom_key = st.text_input("Enter Gemini API Key:", type="password", value=s.api_key_override)
            if st.button("Save Key"):
                s.api_key_override = custom_key.strip()
                st.rerun()

    if s.nickname:
        st.write(f"👤 **Student:** `{s.nickname}`")
        st.write(f"🏫 **Class Code:** `{s.class_code}`")
        st.caption(f"🗓️ **Simulated Timeline:** Day {int(s.current_day)}")
        
        # Streak Tracker
        current_streak = max([s.schedule[c].get("streak", 0) for c in CONCEPTS] or [0])
        if current_streak > 0:
            st.markdown(f"🔥 **{T['streak_label']}** `{current_streak}` in a row!")
        st.markdown("---")

    # Concept Mastery Overview (Filtered by active chapter or grouped)
    st.subheader(T["mastery_title"])
    if s.active_chapter == "all":
        for ch_key, ch_data in CHAPTERS.items():
            with st.expander(f"{ch_data['icon']} {ch_data['short_name']}"):
                for cid in ch_data["concepts"]:
                    c_name = CONCEPTS[cid]["name"].split("&")[0].split("(")[0].strip()
                    m_val = s.mastery.get(cid, DEFAULT_PRIOR)
                    st.progress(float(m_val), text=f"{c_name}: {int(m_val * 100)}%")
    else:
        active_cids = CHAPTERS[s.active_chapter]["concepts"]
        for cid in active_cids:
            c_name = CONCEPTS[cid]["name"].split("&")[0].split("(")[0].strip()
            m_val = s.mastery.get(cid, DEFAULT_PRIOR)
            s_data = s.schedule.get(cid, {})
            stab = s_data.get("stability", 1.0)
            last_d = s_data.get("last_review_day", 0.0)
            due = is_due_for_review(stab, last_d, s.current_day)

            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(float(m_val), text=f"{c_name}: {int(m_val * 100)}%")
            with col2:
                if due:
                    st.markdown("<span style='color:#DC2626;font-size:0.75rem;font-weight:bold;'>DUE</span>", unsafe_allow_html=True)
                else:
                    rem = max(0.0, round(stab - (s.current_day - last_d), 1))
                    st.caption(f"{rem}d")

    st.markdown("---")
    
    # Spaced Repetition Demo Fast-Forward Control
    st.subheader("Demo Controls")
    st.caption("Advance simulated days to observe spaced repetition retrievability drop:")
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("+1 Day", use_container_width=True):
            s.current_day += 1.0
            st.rerun()
    with c_btn2:
        if st.button("+3 Days", use_container_width=True):
            s.current_day += 3.0
            st.rerun()

    st.markdown("---")
    if st.button("🔄 Reset Session", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    if s.nickname and st.button("🗑️ Delete My Data", use_container_width=True):
        delete_student_data(s.student_id)
        st.session_state.clear()
        st.success("Your data has been wiped.")
        st.rerun()

# -----------------------------------------------------------------------------
# MAIN APP: 7-TAB ARCHITECTURE (Modern Reyhan Adinata Dribbble UI)
# -----------------------------------------------------------------------------

tab_dash, tab_diag, tab_practice, tab_lab, tab_eval, tab_teacher, tab_about = st.tabs([
    "🏠 Dashboard",
    "📝 Diagnostic Test",
    "🎯 Adaptive Practice",
    "⚡ Virtual Laboratory",
    "📜 Final Evaluation & Result",
    "📊 Teacher Dashboard",
    "📖 Architecture & How It Works",
])

# Compute active evaluation metrics
eval_score, eval_grade, eval_ch_masteries, eval_cleared_misc = compute_evaluation_metrics(s.mastery, s.active_misconceptions)
mastered_concepts_count = sum(1 for m in s.mastery.values() if m >= 0.70)
total_concepts_count = len(CONCEPTS)

# =============================================================================
# TAB 1: 🏠 DASHBOARD (Reyhan Adinata Dribbble Front Page & Metrics)
# =============================================================================
with tab_dash:
    # Modern Search Bar + Student Status Pill (Image 1 aesthetic)
    st.markdown(f"""
    <div class="dribbble-search">
      <div style="display:flex; align-items:center; gap:12px; color:#64748B;">
        <span style="font-size:16px;">🔍</span>
        <span style="font-size:13px; color:#94A3B8;">Search Class 10 Physics concepts, formulas, or CBSE topics...</span>
      </div>
      <div style="display:flex; align-items:center; gap:10px;">
        <span style="background:#F1F5F9; border:1px solid #E2E8F0; padding:2px 8px; border-radius:6px; font-size:11px; font-weight:600; color:#64748B;">⌘ + F</span>
        <span style="background:#EFF6FF; color:#1D4ED8; font-size:12px; font-weight:600; padding:4px 12px; border-radius:20px;">
          👤 {s.nickname or 'Aarav'} · {s.class_code or 'CLASS-10A'} · 🟢 Active Prep
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Top Stat Cards (Matching Image 1 & Image 2)
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    
    with col_s1:
        circ_svg = generate_circular_progress_svg(mastered_concepts_count / total_concepts_count, size=90, color="#2563EB")
        st.markdown(f"""
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-title">Syllabus Mastery</span>
            <div class="stat-icon icon-blue">📚</div>
          </div>
          <div style="display:flex; align-items:center; justify-content:space-between;">
            <div>
              <div class="stat-value">{int((mastered_concepts_count/total_concepts_count)*100)}%</div>
              <div class="stat-sub">{mastered_concepts_count} / {total_concepts_count} Topics Mastered</div>
            </div>
            <div>{circ_svg}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_s2:
        st.markdown(f"""
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-title">Learning Pace</span>
            <div class="stat-icon icon-amber">⏱️</div>
          </div>
          <div class="stat-value">14.5 <span style="font-size:16px;font-weight:500;color:#64748B;">hrs</span></div>
          <div class="stat-sub">Day {int(s.current_day)} of Prep · 2h 15m today</div>
        </div>
        """, unsafe_allow_html=True)

    with col_s3:
        st.markdown(f"""
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-title">CBSE Readiness</span>
            <div class="stat-icon icon-green">🏆</div>
          </div>
          <div class="stat-value">{eval_score}%</div>
          <div class="stat-sub">Projected Grade: <b style="color:#059669;">{eval_grade.split('·')[0].strip()}</b></div>
        </div>
        """, unsafe_allow_html=True)

    with col_s4:
        st.markdown(f"""
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-title">Misconceptions Cleared</span>
            <div class="stat-icon icon-purple">🛡️</div>
          </div>
          <div class="stat-value">{eval_cleared_misc} <span style="font-size:16px;font-weight:500;color:#64748B;">/ 17</span></div>
          <div class="stat-sub">{len(s.active_misconceptions)} active traps under watch</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Middle Row: Learning Activity Chart (Left) + Skill Progress Bars (Right)
    act_col, skill_col = st.columns([3, 2])
    
    with act_col:
        st.markdown("""
        <div class="dribbble-card" style="margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div>
              <h4 style="margin:0; font-size:18px;">📈 Weekly Learning Activity</h4>
              <small style="color:#64748B;">Adaptive physics practice sessions completed over the last 7 days</small>
            </div>
            <span style="background:#EFF6FF; color:#2563EB; font-weight:700; font-size:12px; padding:4px 12px; border-radius:20px;">
              Active Today: 2h 15m
            </span>
          </div>
        """, unsafe_allow_html=True)
        
        # Render the interactive SVG activity bar chart
        activity_svg = generate_activity_barchart_svg()
        st.components.v1.html(activity_svg, height=240)
        st.markdown("</div>", unsafe_allow_html=True)

    with skill_col:
        st.markdown("""
        <div class="dribbble-card" style="margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
            <h4 style="margin:0; font-size:18px;">📊 NCERT Physics Chapters</h4>
            <small style="color:#64748B;">Class 10 Syllabus</small>
          </div>
        """, unsafe_allow_html=True)
        
        for ch_id, ch_info in CHAPTERS.items():
            ch_m = eval_ch_masteries.get(ch_id, DEFAULT_PRIOR)
            pct = int(ch_m * 100)
            bar_color = "#10B981" if ch_m >= 0.70 else "#2563EB" if ch_m >= 0.40 else "#F59E0B"
            st.markdown(f"""
            <div style="margin-bottom:12px;">
              <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:600; margin-bottom:4px;">
                <span>{ch_info['icon']} {ch_info['short_name']}</span>
                <span style="color:#2563EB;">{pct}%</span>
              </div>
              <div style="background:#E2E8F0; border-radius:8px; height:8px; overflow:hidden;">
                <div style="background:{bar_color}; width:{pct}%; height:8px; border-radius:8px;"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # Lower Row: Cognitive Mastery Radar (Left) + Upcoming Review Schedule (Right)
    rad_col, sch_col = st.columns([1, 1])

    with rad_col:
        st.markdown("""
        <div class="dribbble-card">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <h4 style="margin:0; font-size:18px;">🎯 Cognitive Mastery Radar</h4>
            <small style="color:#64748B;">Polygon vs 70% Target</small>
          </div>
        """, unsafe_allow_html=True)
        radar_scope_cids = CHAPTERS[s.active_chapter]["concepts"] if s.active_chapter != "all" else None
        dash_radar_svg = generate_mastery_radar_chart_svg(s.mastery, concept_keys=radar_scope_cids, width=460, height=340)
        st.components.v1.html(dash_radar_svg, height=360)
        st.markdown("</div>", unsafe_allow_html=True)

    with sch_col:
        st.markdown("""
        <div class="dribbble-card">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <h4 style="margin:0; font-size:18px;">🗓️ Upcoming FSRS Review Schedule</h4>
            <span style="background:#EFF6FF; color:#2563EB; font-weight:600; font-size:11px; padding:3px 10px; border-radius:12px;">Spaced Repetition</span>
          </div>
        """, unsafe_allow_html=True)
        
        due_list = get_due_concepts(s.schedule, s.current_day)
        if due_list:
            st.warning(f"⚠️ **{len(due_list)} concept(s) due for memory consolidation today:**")
            for d_cid in due_list[:4]:
                st.markdown(f"""
                <div style="background:#FEF2F2; border:1px solid #FEE2E2; border-radius:10px; padding:10px 14px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                  <div>
                    <b>{CONCEPTS[d_cid]['name']}</b><br>
                    <small style="color:#991B1B;">Retrievability dropped &lt; 90%</small>
                  </div>
                  <span style="background:#DC2626; color:#FFFFFF; font-size:11px; font-weight:700; padding:2px 8px; border-radius:6px;">DUE NOW</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ **All concepts are currently within optimal retention intervals!**")
            st.caption("Next scheduled reviews based on FSRS memory stability:")
            # Show top 3 scheduled concepts
            sorted_sched = sorted(
                [(cid, s.schedule[cid]["due_day"]) for cid in CONCEPTS],
                key=lambda x: x[1]
            )[:3]
            for s_cid, s_due in sorted_sched:
                rem_days = max(0.1, round(s_due - s.current_day, 1))
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:10px 14px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                  <div>
                    <b>{CONCEPTS[s_cid]['name']}</b><br>
                    <small style="color:#64748B;">Stability: {round(s.schedule[s_cid]['stability'], 1)} days</small>
                  </div>
                  <span style="background:#EFF6FF; color:#2563EB; font-size:11px; font-weight:600; padding:2px 8px; border-radius:6px;">Due in {rem_days}d</span>
                </div>
                """, unsafe_allow_html=True)

        st.caption("💡 Use **Demo Controls** in the sidebar to advance days and observe memory decay.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Quick Launch Action Hub
    st.markdown("### 🚀 Quick Launch Hub")
    h_col1, h_col2, h_col3, h_col4 = st.columns(4)
    with h_col1:
        if st.button("📝 Start Baseline Diagnostic", use_container_width=True, type="primary"):
            s.phase = "diag"
            s.diag_idx = 0
            st.rerun()
    with h_col2:
        if st.button("🎯 Adaptive Practice Loop", use_container_width=True):
            s.phase = "adapt"
            s.current_q = None
            st.rerun()
    with h_col3:
        if st.button("⚡ Open Virtual Circuit Lab", use_container_width=True):
            st.info("Switching to Virtual Laboratory tab...")
    with h_col4:
        if st.button("📜 View Final Board Credential", use_container_width=True):
            st.info("Switching to Final Evaluation & Result tab...")

    # Rapid Evaluation Presets for Judges
    with st.expander("⚡ Hackathon Judges & Fast Evaluation Presets (Click to Auto-Load)"):
        st.caption("Instantly test specific learner states across all 4 chapters without answering all diagnostic questions:")
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            if st.button("Preset 1: Parallel Gap (M5 - Electricity)", use_container_width=True):
                s.nickname = "Judge (Parallel Gap)"
                s.class_code = "CLASS-10A"
                s.active_chapter = "electricity"
                save_student(s.student_id, s.nickname, s.class_code)
                s.mastery["parallel"] = 0.30
                s.mastery["series"] = 0.65
                s.active_misconceptions["parallel"] = "M5"
                for c in CONCEPTS:
                    save_mastery_state(s.student_id, c, s.mastery[c], 1.5, 1.5, 1)
                s.phase = "adapt"
                st.rerun()

            if st.button("Preset 2: Lens Halving Image Gap (M9 - Light)", use_container_width=True):
                s.nickname = "Judge (Lens Half Gap)"
                s.class_code = "CLASS-10A"
                s.active_chapter = "light"
                save_student(s.student_id, s.nickname, s.class_code)
                s.mastery["refraction_lenses"] = 0.32
                s.mastery["lens_power"] = 0.55
                s.active_misconceptions["refraction_lenses"] = "M9"
                for c in CONCEPTS:
                    save_mastery_state(s.student_id, c, s.mastery[c], 1.5, 1.5, 1)
                s.phase = "adapt"
                st.rerun()

        with p_col2:
            if st.button("Preset 3: Myopia / Vision Gap (M12 - Human Eye)", use_container_width=True):
                s.nickname = "Judge (Myopia Gap)"
                s.class_code = "CLASS-10A"
                s.active_chapter = "human_eye"
                save_student(s.student_id, s.nickname, s.class_code)
                s.mastery["defects_vision"] = 0.35
                s.mastery["eye_vision"] = 0.60
                s.active_misconceptions["defects_vision"] = "M12"
                for c in CONCEPTS:
                    save_mastery_state(s.student_id, c, s.mastery[c], 1.5, 1.5, 1)
                s.phase = "adapt"
                st.rerun()

            if st.button("Preset 4: Magnetic Monopole Gap (M15 - Magnetism)", use_container_width=True):
                s.nickname = "Judge (Magnetic Gap)"
                s.class_code = "CLASS-10A"
                s.active_chapter = "magnetism"
                save_student(s.student_id, s.nickname, s.class_code)
                s.mastery["magnetic_field"] = 0.35
                s.mastery["magnetic_force"] = 0.40
                s.active_misconceptions["magnetic_field"] = "M15"
                for c in CONCEPTS:
                    save_mastery_state(s.student_id, c, s.mastery[c], 1.5, 1.5, 1)
                s.phase = "adapt"
                st.rerun()


# =============================================================================
# TAB 2: 📝 DIAGNOSTIC TEST (Baseline Assessment & Knowledge Map)
# =============================================================================
with tab_diag:
    if s.phase not in ("diag", "diag_summary"):
        st.markdown("""
        <div class="dribbble-card">
          <span class="chip chip-med">ORGANISER REQUIREMENT 1</span>
          <h2 style="margin-top:6px;">📝 CBSE Class 10 Physics Diagnostic Assessment</h2>
          <p>Before entering adaptive practice, take a brief 8-question benchmark test. 
          Unlike standard tests, ConceptPilot prompts you for a <b>one-line physical reasoning explanation</b> 
          on every question to diagnose latent mental models and research misconceptions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("start_diag_tab_form"):
            st.markdown("#### Configure Your Diagnostic Assessment")
            diag_nickname = st.text_input("Candidate Nickname:", value=s.nickname or "Aarav")
            diag_class = st.text_input("Class Section:", value=s.class_code or "CLASS-10A")
            
            d_scope_choices = ["all", "light", "human_eye", "electricity", "magnetism"]
            d_scope_labels = {
                "all": "🌐 Full Physics (8 Balanced Cross-Chapter Questions)",
                "light": "💡 Ch 9: Light (Mirrors & Lenses)",
                "human_eye": "👁️ Ch 10: Human Eye & Colourful World",
                "electricity": "⚡ Ch 11: Electricity",
                "magnetism": "🧲 Ch 12: Magnetic Effects of Electric Current",
            }
            d_scope = st.selectbox(
                "Diagnostic Scope:",
                options=d_scope_choices,
                format_func=lambda x: d_scope_labels[x],
                index=0,
            )
            
            start_btn = st.form_submit_button("Start Diagnostic Assessment 🚀", type="primary")
            if start_btn:
                s.nickname = diag_nickname.strip() or "Aarav"
                s.class_code = diag_class.strip() or "CLASS-10A"
                s.active_chapter = d_scope
                save_student(s.student_id, s.nickname, s.class_code)
                s.diag_questions = get_diagnostic_questions(d_scope if d_scope != "all" else None)
                s.diag_idx = 0
                s.phase = "diag"
                st.rerun()

    elif s.phase == "diag":
        q_count = len(s.diag_questions)
        curr_q = s.diag_questions[s.diag_idx]
        concept_id = curr_q["concept"]
        concept_name = CONCEPTS[concept_id]["name"]
        
        # Progress bar
        progress_val = float(s.diag_idx) / float(q_count)
        st.progress(progress_val, text=f"Diagnostic Test: Question {s.diag_idx + 1} of {q_count} · Topic: {concept_name}")
        
        st.markdown(f"""
        <div class="dribbble-card">
          <div style="margin-bottom: 8px;">
            <span class="chip chip-med">DIAGNOSTIC QUESTION {s.diag_idx + 1} / {q_count}</span>
            <span class="chip chip-bank">{concept_name}</span>
          </div>
          <h3 style="margin-top:4px;">{curr_q['question']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer form
        form_key = f"diag_form_{curr_q['id']}_{s.diag_idx}"
        with st.form(form_key):
            selected_option = st.radio(
                "Select your answer:",
                options=range(4),
                format_func=lambda idx: f"({chr(65+idx)}) {curr_q['options'][idx]}",
                index=None,
            )
            
            reasoning = st.text_input(
                "Explain your reasoning in one line (Why did you choose this?):",
                placeholder="e.g. Because electric charge is conserved and current cannot be consumed.",
                max_chars=300,
            )
            
            submit_diag = st.form_submit_button("Submit Answer", type="primary")
            
            if submit_diag:
                if selected_option is None:
                    st.error("Please select an option before submitting.")
                else:
                    with st.spinner("Analyzing your reasoning with diagnostic engine..."):
                        is_correct = (selected_option == curr_q["answer_index"])
                        
                        # AI Call B: Misconception Diagnosis
                        dx = diagnose_reasoning(
                            q=curr_q,
                            chosen_idx=selected_option,
                            reasoning=reasoning,
                            api_key_override=s.api_key_override,
                        )
                        
                        has_misc = (dx["misconception"] in MISCONCEPTIONS)
                        if has_misc:
                            s.diag_misconceptions_found.append({
                                "concept": concept_id,
                                "mid": dx["misconception"],
                                "evidence": dx["evidence"],
                            })
                            s.active_misconceptions[concept_id] = dx["misconception"]
                        
                        # Update BKT mastery
                        old_m = s.mastery.get(concept_id, DEFAULT_PRIOR)
                        new_m = update_bkt(
                            prior_mastery=old_m,
                            is_correct=is_correct,
                            has_misconception=has_misc,
                            misconception_confidence=dx["confidence"],
                        )
                        s.mastery[concept_id] = new_m
                        
                        # Log response in SQLite
                        resp_id = log_response(
                            student_id=s.student_id,
                            question_id=curr_q["id"],
                            concept=concept_id,
                            chosen=selected_option,
                            correct=is_correct,
                            reasoning=reasoning,
                            attempt=1,
                        )
                        if has_misc:
                            log_misconception_event(
                                student_id=s.student_id,
                                response_id=resp_id,
                                concept=concept_id,
                                misconception_id=dx["misconception"],
                                confidence=dx["confidence"],
                                evidence=dx["evidence"],
                                source="ai" if dx.get("is_ai") else "option",
                            )
                        
                        # Item calibration update
                        cal_b, n_ans, n_cor = get_item_calibration(curr_q["id"], curr_q["difficulty_label"])
                        new_b = update_item_difficulty(
                            current_b=cal_b,
                            label_level=curr_q["difficulty_label"],
                            student_mastery=old_m,
                            is_correct=is_correct,
                            n_responses=n_ans,
                        )
                        save_item_calibration(curr_q["id"], curr_q["difficulty_label"], new_b, is_correct)
                        
                        # Spaced repetition initial stability
                        init_s = initial_stability_from_mastery(new_m)
                        s.schedule[concept_id] = {
                            "stability": init_s,
                            "last_review_day": s.current_day,
                            "due_day": s.current_day + init_s,
                            "streak": 1 if is_correct else 0,
                        }
                        save_mastery_state(s.student_id, concept_id, new_m, init_s, s.current_day + init_s, 1 if is_correct else 0)
                        
                        # Move to next question
                        s.diag_idx += 1
                        if s.diag_idx >= q_count:
                            s.phase = "diag_summary"
                        st.rerun()

    elif s.phase == "diag_summary":
        st.balloons()
        st.markdown(f"""
        <div class="dribbble-card">
          <span class="chip chip-verified">DIAGNOSTIC COMPLETED</span>
          <h2 style="margin-top:6px;">🎯 Diagnostic Complete: Your Starting Knowledge Map</h2>
          <p>Great work, <b>{s.nickname}</b>! We analyzed your answers and underlying physical reasoning. 
          Here is your initial cognitive profile before adaptive practice begins.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_g1, col_g2 = st.columns([1, 1])
        with col_g1:
            st.markdown("### 🕸️ Visual Prerequisite Graph")
            st.caption("Prerequisite DAG: 🟢 Mastered (≥70%) · 🟡 Developing (40-69%) · 🔴 Gap (<40%)")
            dot_str = render_concept_graph(s.mastery, s.get("active_chapter", "all"))
            st.graphviz_chart(dot_str, use_container_width=True)
            
        with col_g2:
            st.markdown("### 🎯 Cognitive Mastery Radar")
            st.caption("Competency profile against 70% CBSE target threshold:")
            c_keys = CHAPTERS[s.active_chapter]["concepts"] if s.get("active_chapter", "all") != "all" else None
            radar_svg = generate_mastery_radar_chart_svg(s.mastery, concept_keys=c_keys, width=480, height=360)
            st.components.v1.html(radar_svg, height=380)

        st.markdown("---")
        st.markdown("### 🔍 Diagnostic Findings & Early Misconceptions")
        
        diag_cids = list(set([q["concept"] for q in s.diag_questions])) if s.diag_questions else list(CONCEPTS.keys())
        sorted_concepts = sorted([(cid, s.mastery.get(cid, DEFAULT_PRIOR)) for cid in diag_cids], key=lambda kv: kv[1])
        weakest = sorted_concepts[0]
        st.warning(f"⚠️ **Priority Focus Area:** {CONCEPTS[weakest[0]]['name']} ({int(weakest[1] * 100)}% starting mastery)")
        
        if s.diag_misconceptions_found:
            st.markdown("#### Detected Misconceptions in Reasoning:")
            for m_found in s.diag_misconceptions_found:
                mid = m_found["mid"]
                m_data = MISCONCEPTIONS[mid]
                st.markdown(f"""
                <div style="background:#FFF1F2; border-left:4px solid #EF4444; padding:12px 16px; border-radius:8px; margin-bottom:10px;">
                  <b>{m_data['label']}</b> (Topic: {CONCEPTS[m_found['concept']]['name']})<br>
                  <small style="color:#64748B;"><i>"{m_found['evidence']}"</i></small><br>
                  <span style="color:#0F172A;font-weight:600;">Correction:</span> {m_data['correction']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ **No major foundational misconceptions detected!** Ready for advanced practice.")

        st.markdown("---")
        if st.button("Begin Adaptive Practice 🚀", type="primary", use_container_width=True):
            s.phase = "adapt"
            s.current_q = None
            s.attempt = 0
            s.last_result = None
            s.last_diagnosis = None
            st.rerun()


# =============================================================================
# TAB 3: 🎯 ADAPTIVE PRACTICE (AI Cognitive Tutor & Misconception Buster)
# =============================================================================
with tab_practice:
    # 1. Select or generate next question if not currently active
    if s.current_q is None:
        due_cids = get_due_concepts(s.schedule, s.current_day)
        allowed = CHAPTERS[s.active_chapter]["concepts"] if s.get("active_chapter", "all") != "all" else None
        target_cid, selection_reason = select_next_practice_concept(s.mastery, due_cids, allowed_concepts=allowed)
        target_diff = target_difficulty_for_mastery(s.mastery.get(target_cid, DEFAULT_PRIOR))
        active_m = s.active_misconceptions.get(target_cid)

        chosen_q = None
        question_rationale = ""

        # Attempt AI Question Generation (Call A) + Verification (Call A2) if API connected
        if get_api_key(s.api_key_override):
            with st.spinner("AI drafting and self-verifying targeted question..."):
                samples = get_questions_for_concept(target_cid)
                gen_q = generate_targeted_question(
                    concept=target_cid,
                    difficulty_level=target_diff,
                    active_misconception=active_m,
                    sample_questions=samples,
                    api_key_override=s.api_key_override,
                )
                if gen_q:
                    is_verified = verify_generated_question(gen_q, api_key_override=s.api_key_override)
                    if is_verified:
                        gen_q["verified"] = True
                        chosen_q = gen_q
                        question_rationale = (
                            f"AI-generated Level {target_diff} question independently verified by second solver pass "
                            f"(aimed at {MISCONCEPTIONS[active_m]['label'] if active_m else 'core mastery'})."
                        )

        # Fall back to Question Bank if AI is offline or generation didn't verify
        if not chosen_q:
            chosen_q, bank_rationale = select_next_question(
                concept=target_cid,
                mastery_val=s.mastery.get(target_cid, DEFAULT_PRIOR),
                active_misconception=active_m,
                asked_question_ids=s.asked_ids,
                question_pool=QUESTION_BANK,
            )
            question_rationale = bank_rationale

        s.current_q = chosen_q
        s.selection_reason = f"{selection_reason} {question_rationale}"
        s.attempt = 0
        s.last_result = None
        s.last_diagnosis = None
        s.probe_question = None

    q = s.current_q
    cid = q["concept"]
    c_name = CONCEPTS[cid]["name"]
    diff_label = q["difficulty_label"]
    diff_chip_class = "chip-easy" if diff_label == 1 else "chip-med" if diff_label == 2 else "chip-hard"
    diff_text = "LEVEL 1 · FOUNDATIONAL" if diff_label == 1 else "LEVEL 2 · APPLICATION" if diff_label == 2 else "LEVEL 3 · SYNTHESIS"

    # Selection Rationale Banner (Section 6.3)
    st.markdown(f"""
    <div class="cp-banner">
      🎯 <b>Why this question was chosen:</b> {s.selection_reason}
    </div>
    """, unsafe_allow_html=True)

    # Question Header Chips
    source_chip = (
        '<span class="chip chip-ai">🤖 AI-GENERATED</span><span class="chip chip-verified">✓ VERIFIED SOLVER PASS</span>'
        if q.get("is_ai")
        else '<span class="chip chip-bank">📚 VERIFIED QUESTION BANK</span>'
    )

    # Question Card
    st.markdown(f"""
    <div class="dribbble-card">
      <div style="margin-bottom: 10px;">
        <span class="chip {diff_chip_class}">{diff_text}</span>
        <span class="chip chip-bank">{c_name}</span>
        {source_chip}
      </div>
      <h3 style="margin-top:4px;">{q['question']}</h3>
    </div>
    """, unsafe_allow_html=True)

    # STATE A: Follow-up Probe Question (Call C) if reasoning was UNCLEAR
    if s.last_result == "probe":
        st.info(f"🤔 **Clarification Check:** {s.probe_question}")
        with st.form("probe_form"):
            probe_answer = st.text_input("Your brief clarification:", placeholder="Explain in a few words...")
            if st.form_submit_button("Submit Clarification", type="primary"):
                with st.spinner("Refining diagnostic model..."):
                    combined_reason = f"{s.get('prev_reason', '')}; Clarification: {probe_answer}"
                    dx = diagnose_reasoning(
                        q=q,
                        chosen_idx=s.get("prev_choice", 0),
                        reasoning=combined_reason,
                        api_key_override=s.api_key_override,
                    )
                    s.last_diagnosis = dx
                    s.last_result = "done"
                    st.rerun()

    # STATE B: Awaiting first or retry answer submission
    elif s.last_result in (None, "retry"):
        if s.last_result == "retry":
            st.info(f"💡 **Socratic Hint:** {s.last_diagnosis['hint']} *(You have 1 retry remaining)*")

        form_key = f"practice_form_{q['id']}_{len(s.history)}_{s.attempt}"
        with st.form(form_key):
            selected_opt = st.radio(
                "Choose one option:",
                options=range(4),
                format_func=lambda idx: f"({chr(65+idx)}) {q['options'][idx]}",
                index=None,
            )
            
            why_text = ""
            if s.attempt == 0:
                why_text = st.text_input(
                    "Why did you choose this? (One-line physical reasoning)",
                    placeholder="e.g. Because parallel resistors provide alternate paths, decreasing total resistance.",
                    max_chars=300,
                )

            submit_btn = st.form_submit_button("Submit Answer", type="primary")

            if submit_btn:
                if selected_opt is None:
                    st.error("Please select an answer choice.")
                else:
                    is_correct = (selected_opt == q["answer_index"])
                    
                    if s.attempt == 0:
                        with st.spinner("AI evaluating reasoning against PER misconception models..."):
                            dx = diagnose_reasoning(
                                q=q,
                                chosen_idx=selected_opt,
                                reasoning=why_text,
                                api_key_override=s.api_key_override,
                            )
                            s.last_diagnosis = dx
                            has_misc = (dx["misconception"] in MISCONCEPTIONS)
                            
                            # Call C check: UNCLEAR reasoning prompts follow-up probe
                            if dx["misconception"] == "UNCLEAR" and dx.get("is_ai"):
                                probe_q = generate_followup_probe(
                                    q=q,
                                    chosen_idx=selected_opt,
                                    reasoning=why_text,
                                    api_key_override=s.api_key_override,
                                )
                                s.probe_question = probe_q
                                s.prev_choice = selected_opt
                                s.prev_reason = why_text
                                s.last_result = "probe"
                                st.rerun()

                            # Update BKT mastery on FIRST attempt only
                            old_m = s.mastery.get(cid, DEFAULT_PRIOR)
                            new_m = update_bkt(
                                prior_mastery=old_m,
                                is_correct=is_correct,
                                has_misconception=has_misc,
                                misconception_confidence=dx["confidence"],
                            )
                            s.mastery[cid] = new_m

                            # Update Spaced Repetition stability
                            old_stab = s.schedule[cid].get("stability", 1.0)
                            last_rev = s.schedule[cid].get("last_review_day", s.current_day)
                            new_stab = update_concept_stability(
                                current_s=old_stab,
                                last_review_day=last_rev,
                                current_day=s.current_day,
                                is_success=is_correct,
                                has_misconception=has_misc,
                            )
                            new_streak = s.schedule[cid].get("streak", 0) + 1 if (is_correct and not has_misc) else 0
                            s.schedule[cid] = {
                                "stability": new_stab,
                                "last_review_day": s.current_day,
                                "due_day": s.current_day + new_stab,
                                "streak": new_streak,
                            }
                            save_mastery_state(s.student_id, cid, new_m, new_stab, s.current_day + new_stab, new_streak)

                            # Log response
                            resp_id = log_response(
                                student_id=s.student_id,
                                question_id=q["id"],
                                concept=cid,
                                chosen=selected_opt,
                                correct=is_correct,
                                reasoning=why_text,
                                attempt=1,
                            )
                            if has_misc:
                                log_misconception_event(
                                    student_id=s.student_id,
                                    response_id=resp_id,
                                    concept=cid,
                                    misconception_id=dx["misconception"],
                                    confidence=dx["confidence"],
                                    evidence=dx["evidence"],
                                    source="ai" if dx.get("is_ai") else "option",
                                )
                                s.active_misconceptions[cid] = dx["misconception"]
                            elif is_correct:
                                s.active_misconceptions.pop(cid, None)

                            # Calibrate item difficulty
                            cal_b, n_ans, n_cor = get_item_calibration(q["id"], q["difficulty_label"])
                            new_b = update_item_difficulty(
                                current_b=cal_b,
                                label_level=q["difficulty_label"],
                                student_mastery=old_m,
                                is_correct=is_correct,
                                n_responses=n_ans,
                            )
                            save_item_calibration(q["id"], q["difficulty_label"], new_b, is_correct)
                            s.asked_ids.add(q["id"])

                    if is_correct:
                        s.last_result = "done"
                    elif s.attempt == 0:
                        s.last_result = "retry"
                        s.attempt = 1
                    else:
                        s.last_result = "done"

                    st.rerun()

    # STATE C: Answer finalized (Correct or 2 attempts complete)
    else:
        st.success(f"✅ **Correct Answer:** ({chr(65 + q['answer_index'])}) {q['options'][q['answer_index']]}")
        
        # Step-by-step scientific explanation
        st.markdown(f"""
        <div class="dribbble-card">
          <b>Explanation:</b><br>
          {q['explanation']}<br><br>
          <small style="color:#64748B;"><b>Curriculum Reference:</b> {q['source_note']}</small>
        </div>
        """, unsafe_allow_html=True)

        # Diagnosis Card & "AI at Work" Panel (Section 7)
        dx = s.last_diagnosis
        if dx:
            mid = dx["misconception"]
            if mid in MISCONCEPTIONS:
                m_info = MISCONCEPTIONS[mid]
                st.markdown(f"""
                <div class="cp-diagnosis-card">
                  <b style="color:#1E40AF;">🧠 Diagnostic Insight: Misconception Detected</b><br>
                  <b>{m_info['label']}</b> (Confidence: {int(dx['confidence'] * 100)}%)<br>
                  <i style="color:#4B5563;">Evidence Cited: "{dx['evidence']}"</i><br><br>
                  <b>Scientific Correction:</b> {m_info['correction']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="cp-diagnosis-card" style="border-left-color:#10B981;background-color:#F0FDF4;">
                  <b style="color:#065F46;">✅ Scientific Reasoning Sound</b><br>
                  <i>{dx['evidence']}</i>
                </div>
                """, unsafe_allow_html=True)

            # "AI at Work" Transparency Panel
            cache_tag = "⚡ Cached Result" if dx.get("cached") else "🌐 Live Gemini Inference"
            engine_tag = "Google Gemini 2.5 Flash" if dx.get("is_ai") else "Offline Heuristic Fallback"
            st.markdown(f"""
            <div class="ai-work-panel">
              <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                <b>🤖 AI At Work (Call B Transparency)</b>
                <small style="color:#64748B;">{engine_tag} · {cache_tag}</small>
              </div>
              <b>Input Inspected:</b> {dx.get('ai_read', 'Student response data')}<br>
              <b>Evaluation Output:</b> Misconception ID <code>{dx['misconception']}</code> · Confidence: {int(dx['confidence'] * 100)}%<br>
              <b>Evidence Cited:</b> <i>"{dx['evidence']}"</i><br>
              <b>Verification Pass:</b> {"Independent solver verified key before presentation" if q.get("verified") else "Standard curriculum validation"}
            </div>
            """, unsafe_allow_html=True)

        if st.button("Next Question ➡️", type="primary"):
            s.current_q = None
            s.attempt = 0
            s.last_result = None
            s.last_diagnosis = None
            s.probe_question = None
            st.rerun()


# =============================================================================
# TAB 4: ⚡ VIRTUAL LABORATORY (Circuit Lab & NCERT Formula Reference)
# =============================================================================
with tab_lab:
    st.markdown("""
    <div class="dribbble-card">
      <span class="chip chip-med">INTERACTIVE EXPERIMENTATION</span>
      <h2 style="margin-top:6px;">⚡ Virtual Circuit Laboratory & NCERT Formula Cards</h2>
      <p>Bust circuit misconceptions hands-on. Experiment with live sliders to observe how 
      Series vs Parallel connections change current and equivalent resistance in real-time.</p>
    </div>
    """, unsafe_allow_html=True)

    lab_c1, lab_c2 = st.columns([1, 1])
    with lab_c1:
        st.markdown("#### Circuit Controls")
        circuit_mode = st.radio(
            "Circuit Configuration:",
            options=["Series", "Parallel"],
            horizontal=True,
            key="lab_circuit_mode"
        )
        v_source = st.slider("Battery Voltage (V):", min_value=1.0, max_value=24.0, value=12.0, step=1.0, key="lab_v")
        r1_val = st.slider("Resistor R1 (Ω):", min_value=1.0, max_value=50.0, value=6.0, step=1.0, key="lab_r1")
        r2_val = st.slider("Resistor R2 (Ω):", min_value=1.0, max_value=50.0, value=12.0, step=1.0, key="lab_r2")

    sim_res = simulate_circuit(circuit_mode, v_source, r1_val, r2_val)

    with lab_c2:
        st.markdown(f"#### Laboratory Readings ({sim_res['mode']} Circuit)")
        sim_m1, sim_m2 = st.columns(2)
        with sim_m1:
            st.metric("Equivalent Resistance (Req)", f"{sim_res['r_eq']} Ω")
            st.metric("Branch 1: Current / Volt", f"{sim_res['i1']} A / {sim_res['v1']} V")
        with sim_m2:
            st.metric("Total Circuit Current (Itot)", f"{sim_res['i_total']} A")
            st.metric("Branch 2: Current / Volt", f"{sim_res['i2']} A / {sim_res['v2']} V")
        st.metric("Total Circuit Power", f"{sim_res['p_total']} W", help="P = V × I")

    st.info(f"**Physical Analysis:** {sim_res['explanation']}")
    st.warning(f"**Misconception Alert:** {sim_res['misconception_note']}")

    st.markdown("---")
    st.subheader("📖 Full Syllabus NCERT Topic Revision Cards (All 20 Topics)")
    st.caption("Detailed formula sheet and common CBSE exam traps across Light, Human Eye, Electricity, and Magnetism:")
    
    topic_keys = CHAPTERS[s.active_chapter]["concepts"] if s.active_chapter != "all" else list(CONCEPTS.keys())
    sel_topic = st.selectbox(
        "Select Topic for Quick Study Guide:",
        options=topic_keys,
        index=0,
        format_func=lambda x: CONCEPTS[x]["name"],
        key="lab_revision_topic_sel"
    )
    card = CONCEPT_STUDY_CARDS.get(sel_topic, {})
    if card:
        st.markdown(f"""
        <div class="dribbble-card">
          <h4>📘 {card['title']}</h4>
          <p>{card['summary']}</p>
          <b>Key Formulas & Relationships:</b>
        """, unsafe_allow_html=True)
        for f_item in card.get("formulas", []):
            st.code(f_item, language="text")
        st.markdown(f"""
          <div style="background:#FEF3C7; border-left:4px solid #F59E0B; padding:12px 16px; border-radius:8px; margin-top:10px;">
            <b>⚠️ Common CBSE Board Exam Pitfall:</b><br>
            {card['common_trap']}
          </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# TAB 5: 📜 FINAL EVALUATION & RESULT (Essential Result Section)
# =============================================================================
with tab_eval:
    st.markdown("""
    <div class="dribbble-card">
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div>
          <span class="chip chip-verified">FINAL EVALUATION & COMPETENCY RESULT</span>
          <h2 style="margin-top:6px;">📜 CBSE Board Readiness Evaluation & Official Credential</h2>
          <p>Comprehensive psychometric evaluation based on your Bayesian Knowledge Tracing mastery, 
          empirical Rasch difficulty calibration, and Physics Education Research misconception clearance.</p>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Official Printable Certificate Card (Section requested by User)
    cert_html = generate_evaluation_certificate_html(
        student_name=s.nickname or "Aarav Sharma",
        class_code=s.class_code or "CLASS-10A",
        readiness_score=eval_score,
        grade_tier=eval_grade,
        chapter_masteries=eval_ch_masteries,
        misconceptions_cleared=eval_cleared_misc,
        total_misconceptions=17,
    )
    st.components.v1.html(cert_html, height=520)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # 2. Detailed Chapter-by-Chapter Proficiency Verdict
    st.subheader("📊 Chapter-by-Chapter Board Proficiency Verdict")
    ch_rows = []
    for ch_id, ch_info in CHAPTERS.items():
        ch_m = eval_ch_masteries.get(ch_id, DEFAULT_PRIOR)
        verdict = (
            "🟢 Board Ready (Distinction Level)" if ch_m >= 0.70 else
            "🟡 Developing (Passable, Needs Practice)" if ch_m >= 0.40 else
            "🔴 Critical Gap (Requires Immediate Remediation)"
        )
        ch_rows.append({
            "Chapter": ch_info["name"],
            "Concept Topics": len(ch_info["concepts"]),
            "Mastery Score": f"{int(ch_m * 100)}%",
            "Board Exam Verdict": verdict,
        })
    st.dataframe(pd.DataFrame(ch_rows), use_container_width=True, hide_index=True)

    # 3. Research Misconception Clearance Audit Table (All 17 Models)
    st.subheader("🛡️ Physics Misconception Clearance Audit (17 PER Models)")
    st.caption("Published Physics Education Research diagnostic models checked across your session:")
    
    audit_rows = []
    for mid, minfo in MISCONCEPTIONS.items():
        is_active = any(active_mid == mid for active_mid in s.active_misconceptions.values())
        status = "⚠️ Active Trap Identified" if is_active else "🟢 Cleared / Reasoning Sound"
        audit_rows.append({
            "ID": mid,
            "Research Misconception": minfo["label"],
            "Diagnostic Status": status,
            "Scientific Correction": minfo["correction"],
        })
    st.dataframe(pd.DataFrame(audit_rows), use_container_width=True, hide_index=True)

    # 4. AI Personalized Remedial Study Prescription
    st.subheader("📋 Personalized Remedial Study Prescription")
    # Identify weakest concepts
    weakest_concepts = sorted(
        [(cid, s.mastery.get(cid, DEFAULT_PRIOR)) for cid in CONCEPTS],
        key=lambda x: x[1]
    )[:3]
    
    st.markdown(f"""
    <div class="dribbble-card" style="border-left:4px solid #2563EB;">
      <h4>🎯 AI Pedagogical Recommendation for CBSE Board Success:</h4>
      <ol style="margin-bottom:0;">
        <li><b>Immediate Focus on {CONCEPTS[weakest_concepts[0][0]]['name']} ({int(weakest_concepts[0][1]*100)}% Mastery):</b> 
        This is your lowest-scoring syllabus topic. Review the formula card in the <i>Virtual Laboratory</i> tab and practice Level 1 application problems.</li>
        <li><b>Prerequisite Review:</b> Verify that foundational concepts ({', '.join(CONCEPTS[weakest_concepts[0][0]].get('prerequisites', [])) or 'None'}) are solid before attempting complex multi-concept numericals.</li>
        <li><b>Active Misconceptions ({len(s.active_misconceptions)}):</b> Ensure you always articulate physical reasons rather than applying rote formulas blindly.</li>
      </ol>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# TAB 6: 📊 TEACHER DASHBOARD (PIN Protected, Heatmap, Reteach Plan & Export)
# =============================================================================
with tab_teacher:
    configured_pin = os.environ.get("TEACHER_PIN", "teacher123")
    try:
        if "TEACHER_PIN" in st.secrets:
            configured_pin = str(st.secrets["TEACHER_PIN"]).strip()
    except Exception:
        pass

    if not s.get("teacher_auth", False):
        st.subheader("🔒 Teacher Dashboard Access")
        st.caption("Enter the teacher security PIN to inspect class diagnostics and analytics.")
        
        with st.form("teacher_login_form"):
            entered_pin = st.text_input("Security PIN:", type="password", placeholder="Default demo PIN: teacher123")
            pin_submit = st.form_submit_button("Unlock Dashboard", type="primary")
            
            if pin_submit:
                if entered_pin.strip() == configured_pin:
                    s.teacher_auth = True
                    st.success("Access granted!")
                    st.rerun()
                else:
                    st.error("Incorrect PIN. Please re-enter or check environment configuration.")
    else:
        head_col1, head_col2 = st.columns([4, 1])
        with head_col1:
            st.title("📊 Teacher Analytics & Class Diagnostic Dashboard")
            st.caption("Real-time cognitive diagnostics across CBSE Class 10 Science (Physics)")
        with head_col2:
            if st.button("🔒 Lock Dashboard", use_container_width=True):
                s.teacher_auth = False
                st.rerun()

        st.markdown("---")

        ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 3, 3])
        with ctrl_col1:
            db_classes = get_available_classes()
            class_options = ["ALL"] + (db_classes if db_classes else ["CLASS-10A"])
            selected_class = st.selectbox("Select Class Section:", options=class_options, index=0)

        with ctrl_col2:
            t_chapters = ["all"] + list(CHAPTERS.keys())
            t_chap_labels = {
                "all": "🌐 Full Physics (All 4 Chapters)",
                "light": "💡 Ch 9: Light (Mirrors & Lenses)",
                "human_eye": "👁️ Ch 10: Human Eye & World",
                "electricity": "⚡ Ch 11: Electricity",
                "magnetism": "🧲 Ch 12: Magnetic Effects",
            }
            teacher_scope = st.selectbox(
                "Filter Chapter Scope:",
                options=t_chapters,
                index=0,
                format_func=lambda x: t_chap_labels.get(x, x),
                key="teacher_chapter_filter",
            )

        with ctrl_col3:
            include_sim = st.toggle("Include simulated sample class (20 benchmark students)", value=False)

        if include_sim:
            st.warning("⚠️ **SIMULATED sample data is active:** Benchmark cohort records are labeled with `[SIMULATED]` to distinguish them from real student data.")
        else:
            st.info("ℹ️ **Showing REAL student pilot data only.** Toggle above to overlay the 20-student benchmark class.")

        real_data = get_real_students_mastery(selected_class if selected_class != "ALL" else None)
        
        live_exists = any(r.get("ID") == s.student_id for r in real_data)
        if not live_exists and s.nickname and any(v != DEFAULT_PRIOR for v in s.mastery.values()):
            live_record = {
                "Student": f"{s.nickname} (Live Session)",
                "ID": s.student_id,
                "Class": s.class_code,
                "Is_Simulated": False,
            }
            for cid in CONCEPTS:
                live_record[cid] = round(s.mastery.get(cid, DEFAULT_PRIOR), 2)
            real_data.append(live_record)

        combined_students = list(real_data)
        if include_sim:
            sim_students = generate_simulated_class(20)
            combined_students.extend(sim_students)

        if not combined_students:
            st.markdown("""
            <div class="dribbble-card">
              <h4>No Student Records Found</h4>
              <p>No students have completed the diagnostic in this class yet. 
              Students can start from the <b>Diagnostic Test</b> tab, or you can toggle on 
              <b>'Include simulated sample class'</b> above to inspect demo data.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            df_students = pd.DataFrame(combined_students)
            concept_ids = CHAPTERS[teacher_scope]["concepts"] if teacher_scope != "all" else list(CONCEPTS.keys())
            
            avg_mastery = df_students[concept_ids].mean()
            overall_class_avg = avg_mastery.mean()
            
            student_means = df_students[concept_ids].mean(axis=1)
            at_risk_count = int((student_means < 0.50).sum())
            total_students = len(df_students)

            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            with m_col1:
                st.metric("Total Students Enrolled", total_students)
            with m_col2:
                st.metric("Cohort Average Mastery", f"{int(overall_class_avg * 100)}%")
            with m_col3:
                st.metric("Students At Risk (<50%)", at_risk_count, delta=f"{int((at_risk_count/total_students)*100)}% of class", delta_color="inverse")
            with m_col4:
                weakest_cid = avg_mastery.idxmin()
                st.metric("Weakest Concept", CONCEPTS[weakest_cid]["name"], f"{int(avg_mastery[weakest_cid] * 100)}%")

            st.markdown("---")

            st.subheader("📈 Syllabus-Wide Mastery Breakdown")
            tab_bar, tab_radar = st.tabs(["📊 Concept Bar Chart & At-Risk Counts", "🎯 Cohort Cognitive Radar"])
            
            with tab_bar:
                c_chart1, c_chart2 = st.columns([3, 2])
                with c_chart1:
                    st.markdown("**Average Mastery by Concept Topic (%)**")
                    avg_series = (avg_mastery * 100).round(1)
                    avg_series.index = [CONCEPTS[cid]["name"] for cid in avg_series.index]
                    st.bar_chart(avg_series, color="#2563EB", height=280)

                with c_chart2:
                    st.markdown("**Students Below 50% Threshold by Concept**")
                    below_50 = (df_students[concept_ids] < 0.50).sum()
                    below_df = pd.DataFrame({
                        "Concept": [CONCEPTS[cid]["name"] for cid in concept_ids],
                        "At-Risk Students": below_50.values,
                        "% of Class": [f"{int((v / total_students) * 100)}%" for v in below_50.values],
                    }).sort_values("At-Risk Students", ascending=False)
                    st.dataframe(below_df, use_container_width=True, hide_index=True)

            with tab_radar:
                st.caption("Class-wide average competency vector compared against 70% proficiency target:")
                c_scope_keys = concept_ids if teacher_scope != "all" else None
                cohort_radar_svg = generate_mastery_radar_chart_svg(avg_mastery.to_dict(), concept_keys=c_scope_keys, width=500, height=380)
                st.components.v1.html(cohort_radar_svg, height=400)

            st.markdown("---")

            # Student Cognitive Matrix
            st.subheader("🗺️ Student Cognitive Matrix (Mastery Heatmap)")
            display_cols = ["Student", "Class"] + concept_ids
            df_display = df_students[display_cols].copy()
            
            column_configs = {
                "Student": st.column_config.TextColumn("Student Nickname", width="medium"),
                "Class": st.column_config.TextColumn("Class", width="small"),
            }
            for cid in concept_ids:
                column_configs[cid] = st.column_config.ProgressColumn(
                    CONCEPTS[cid]["name"],
                    help=CONCEPTS[cid]["description"],
                    min_value=0.0,
                    max_value=1.0,
                    format="%.0f%%",
                )

            st.dataframe(df_display, column_config=column_configs, use_container_width=True, hide_index=True)

            # Individual Student Deep-Dive
            with st.expander("👤 Individual Student Profile & Cognitive Deep-Dive"):
                student_names = df_students["Student"].tolist()
                selected_student_name = st.selectbox("Select Student to Inspect:", options=student_names, key="sel_student_drilldown")
                sel_row = df_students[df_students["Student"] == selected_student_name].iloc[0]
                
                st_col1, st_col2 = st.columns([1, 1])
                with st_col1:
                    st.markdown(f"**Cognitive Radar: {selected_student_name}**")
                    student_mastery_dict = {cid: float(sel_row[cid]) for cid in concept_ids}
                    s_radar_svg = generate_mastery_radar_chart_svg(student_mastery_dict, concept_keys=c_scope_keys, width=440, height=340)
                    st.components.v1.html(s_radar_svg, height=360)
                with st_col2:
                    st.markdown("##### 📌 Diagnostic Profile")
                    s_avg = sel_row[concept_ids].mean()
                    s_tier = "🟢 Proficient" if s_avg >= 0.70 else "🟡 Developing" if s_avg >= 0.50 else "🔴 Critical Support Needed"
                    st.write(f"**Cognitive Status:** {s_tier} ({int(s_avg * 100)}% overall mastery)")
                    st.write(f"**Enrolled Class:** {sel_row['Class']}")
                    
                    s_weak = min(concept_ids, key=lambda c: sel_row[c])
                    s_strong = max(concept_ids, key=lambda c: sel_row[c])
                    st.write(f"**Primary Hurdle:** {CONCEPTS[s_weak]['name']} ({int(sel_row[s_weak]*100)}%)")
                    st.write(f"**Greatest Strength:** {CONCEPTS[s_strong]['name']} ({int(sel_row[s_strong]*100)}%)")
                    st.info(f"Prioritize remediation on **{CONCEPTS[s_weak]['name']}** before advancing.")

            st.markdown("---")

            # Top Research Misconceptions Table
            st.subheader("🔍 Identified Class Misconceptions (Reasoning-Based)")
            real_misc_stats = get_real_misconception_stats(selected_class if selected_class != "ALL" else None)
            if include_sim:
                sim_misc_stats = get_simulated_misconception_stats()
                sim_map = {m["Misconception_ID"]: m["Affected_Students"] for m in sim_misc_stats}
                combined_misc = []
                for m in real_misc_stats:
                    mid = m["Misconception_ID"]
                    total_cnt = m["Affected_Students"] + sim_map.get(mid, 0)
                    combined_misc.append({
                        "Misconception_ID": mid,
                        "Misconception": m["Misconception"],
                        "Affected_Students": total_cnt,
                        "Suggested_Teacher_Action": m["Teacher_Action"],
                        "Correction": m["Correction"],
                    })
                combined_misc.sort(key=lambda x: x["Affected_Students"], reverse=True)
                misc_table_data = combined_misc
            else:
                misc_table_data = [
                    {
                        "Misconception_ID": m["Misconception_ID"],
                        "Misconception": m["Misconception"],
                        "Affected_Students": m["Affected_Students"],
                        "Suggested_Teacher_Action": m["Teacher_Action"],
                        "Correction": m["Correction"],
                    }
                    for m in real_misc_stats
                ]

            st.dataframe(pd.DataFrame(misc_table_data), use_container_width=True, hide_index=True)

            # AI Call D: Targeted Remedial Reteach Plan
            st.markdown("---")
            st.subheader("🤖 AI Remedial Reteach Plan Generator (Call D)")
            if st.button("Generate Targeted Remedial Plan 📋", type="primary"):
                with st.spinner("AI analyzing cohort aggregates and designing 5-minute activities..."):
                    concept_dict = {cid: float(avg_mastery[cid]) for cid in concept_ids}
                    plan = generate_reteach_plan(
                        concept_averages=concept_dict,
                        top_misconceptions=misc_table_data,
                        api_key_override=s.api_key_override,
                    )
                    s.reteach_plan = plan
                    st.rerun()

            if s.get("reteach_plan"):
                plan = s.reteach_plan
                st.markdown(f"""
                <div class="dribbble-card" style="border-left: 4px solid #2563EB;">
                  <div style="display:flex; justify-content:space-between;">
                    <h4>📋 Recommended Class Remediation Plan</h4>
                    <small style="color:#64748B;">{"Generated by Gemini 2.5 Flash" if plan.get('is_ai') else "Verified PER Reteach Architecture"}</small>
                  </div>
                  <p><i>{plan.get('overview', '')}</i></p>
                </div>
                """, unsafe_allow_html=True)

                for step in plan.get("lesson_plan", []):
                    st.markdown(f"""
                    <div class="dribbble-card">
                      <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                        <b>Step {step.get('step', 1)}: {step.get('activity_title', 'Remedial Activity')}</b>
                        <span class="chip chip-med">⏱️ {step.get('duration_minutes', 5)} MINUTES</span>
                      </div>
                      <b>Target Misconception:</b> <code>{step.get('target_misconception_id', 'M')}</code> ({step.get('focus_concept', 'Physics')})<br><br>
                      <b>Teacher Instructions:</b><br>
                      {step.get('teacher_instructions', '')}<br><br>
                      <b>Socratic Check Question:</b><br>
                      <i style="color:#1E40AF;">"{step.get('check_question', '')}"</i>
                    </div>
                    """, unsafe_allow_html=True)

            # Empirical Item Difficulty Calibration
            st.markdown("---")
            st.subheader("⚙️ Empirical Question Difficulty Calibration")
            st.caption("Rasch Model calibration: Initial curriculum label $b_0$ updates dynamically as students submit answers.")
            cal_items = get_all_calibrated_items()
            st.dataframe(pd.DataFrame(cal_items), use_container_width=True, hide_index=True)

            # CSV Export
            st.markdown("---")
            st.subheader("📥 Export Class Report")
            csv_content = df_students.to_csv(index=False)
            st.download_button(
                label="Download Class Mastery CSV",
                data=csv_content,
                file_name=f"conceptpilot_{selected_class}_report.csv",
                mime="text/csv",
                type="secondary",
            )


# =============================================================================
# TAB 7: 📖 ARCHITECTURE & HOW IT WORKS (Pedagogical Design & PER Citations)
# =============================================================================
with tab_about:
    st.title("📖 How ConceptPilot Works")
    st.markdown("### *Cognitive Science, Educational Data Mining & Pedagogical AI in Harmony*")
    
    st.markdown("""
    <div class="dribbble-card">
      <h4>🎯 Product Mission & Problem Understanding</h4>
      <p>ConceptPilot is designed to bridge the gap between educational cognitive research and generative AI across 
      the complete <b>CBSE Class 10 Science Physics Syllabus (Light, Human Eye, Electricity, and Magnetic Effects)</b> 
      for candidates and educators. Recent educational studies and teacher interviews highlight several critical challenges in digital exam-preparation:</p>
      <ul>
        <li><b>Reactive vs. Diagnostic Tutors:</b> Research suggests that conversational AI chatbots tend to respond 
        reactively to student prompts—often explaining problems away or solving them outright—rather than diagnosing 
        the underlying knowledge structure and misconceptions of the learner.</li>
        <li><b>The Answer-Giving vs. Abandonment Tradeoff:</b> Research indicates that tutors that simply give away answers 
        can significantly impair retention and exam performance. Conversely, rigid tutors that only withhold answers 
        lead to high student abandonment. ConceptPilot addresses this tension through <b>fast feedback, one targeted 
        Socratic hint, one retry, and short cognitive loops</b>.</li>
        <li><b>Flawed Reasoning Behind Correct Answers:</b> In standardized multiple-choice assessments, a student can 
        easily guess the correct option while holding a deeply flawed mental model (e.g. choosing the correct lens formula answer 
        while believing images reside on the lens glass). ConceptPilot requires a brief one-line 
        reasoning explanation for every first attempt to detect latent misconceptions.</li>
        <li><b>The Unreliability of LLM Difficulty Judgments:</b> Empirical evaluations demonstrate that Large Language 
        Models are notoriously unreliable at judging or generating questions of specific psychometric difficulty. 
        ConceptPilot separates question generation from difficulty estimation, employing an empirical <b>Rasch Item Response 
        Theory (IRT) model</b> that calibrates item difficulty from real student outcomes.</li>
        <li><b>CBSE Competency-Based Board Evolution:</b> The CBSE Class 10 examination framework has systematically 
        shifted toward high-weightage application and competency-based questions across all physics units. Superficial memorization is no longer 
        sufficient; diagnosing core conceptual understanding is essential.</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    # 7 Organiser Components
    st.subheader("🧩 The 7 Mandatory Organiser Components Across All 4 Physics Chapters")
    comp_col1, comp_col2 = st.columns(2)
    
    with comp_col1:
        st.markdown("""
        <div class="dribbble-card">
          <b>1. Diagnostic Baseline Assessment</b><br>
          A standardized baseline diagnostic across core syllabus topics in pedagogical sequence. 
          Supports chapter-specific diagnostics or a balanced cross-chapter diagnostic covering the entire Class 10 Physics syllabus.
        </div>
        
        <div class="dribbble-card">
          <b>2. Syllabus Concept Graph</b><br>
          A directed acyclic graph (DAG) modeling prerequisite relationships across all 20 syllabus concepts spanning 
          Light, Human Eye, Electricity, and Magnetic Effects. Visualized live via Graphviz with real-time mastery-dependent node coloring.
        </div>
        
        <div class="dribbble-card">
          <b>3. Dynamic Learner Model (BKT)</b><br>
          Standard 4-parameter Bayesian Knowledge Tracing (<i>P(L0)=0.30, P(G)=0.25, P(S)=0.10, P(T)=0.12</i>). 
          Includes <b>prerequisite propagation</b> (discounting dependent mastery when foundations are weak) and a 
          <b>30% flawed reasoning gain discount</b> when correct answers are reached via misconceptions.
        </div>
        
        <div class="dribbble-card">
          <b>4. Adaptive Question Selection & Difficulty Calibration</b><br>
          Selects items matching student mastery thresholds (Level 1 &lt;40%, Level 2 &lt;70%, Level 3 &ge;70%), 
          prioritizing due reviews, weak prerequisites, and active misconception traps. Calibrates psychometric 
          difficulty parameter <i>b</i> online using Rasch IRT with Bayesian shrinkage.
        </div>
        """, unsafe_allow_html=True)

    with comp_col2:
        st.markdown("""
        <div class="dribbble-card">
          <b>5. Reasoning-Based Misconception Detection</b><br>
          Evaluates student explanations against a fixed 17-model Physics Education Research (PER) library (M1–M17) 
          spanning Optics, Vision, Circuits, and Electromagnetism. If reasoning is ambiguous, prompts a single-sentence Socratic probe (Call C).
        </div>
        
        <div class="dribbble-card">
          <b>6. Spaced Repetition Scheduling</b><br>
          FSRS-inspired memory model tracking stability <i>S</i> and retrievability <i>R(t) = 0.9^(t/S)</i> per concept. 
          Triggers review when retrievability drops below 90%. Features interactive fast-forward controls for testing memory decay.
        </div>
        
        <div class="dribbble-card">
          <b>7. Teacher Diagnostic Dashboard</b><br>
          PIN-protected portal displaying class-wide cognitive heatmaps, chapter-filtered concept risk distributions, misconception 
          prevalence, empirical item calibration tables, one-click <b>AI Remedial Reteach Plans (Call D)</b>, 
          and CSV export.
        </div>
        """, unsafe_allow_html=True)

    # PER Reference Library
    st.subheader("📚 Full Syllabus Research Misconception Library (M1 – M17)")
    st.caption("Derived from seminal studies by McDermott & Shaffer (1992), Goldberg & McDermott (1987), Galili & Hazan (2000), and Maloney et al. (2001 - CSEM):")
    
    misc_rows = []
    for mid, m_info in MISCONCEPTIONS.items():
        misc_rows.append({
            "ID": mid,
            "Misconception": m_info["label"],
            "Scientific Correction": m_info["correction"],
            "Teacher Action": m_info["reteach_action"],
        })
    st.dataframe(pd.DataFrame(misc_rows), use_container_width=True, hide_index=True)

    # AI Integration & Ethics
    st.subheader("🤖 AI Integration & Safety Architecture")
    st.markdown("""
    <div class="dribbble-card">
      <p>ConceptPilot integrates <b>Google Gemini 2.5 Flash</b> through the modern <code>google-genai</code> SDK 
      with multiple layers of safety and verification:</p>
      <ul>
        <li><b>Dual-Pass Verification (Calls A & A2):</b> Any generated question must be solved by an independent 
        solver pass (temperature 0.0) without access to the key. The question is only accepted if the solver matches 
        the intended answer; otherwise, the app discards the generation and falls back to verified bank items.</li>
        <li><b>Structured JSON Schema Enforcement:</b> All LLM outputs use <code>response_mime_type="application/json"</code> 
        and are rigorously validated against strict Python type schemas. Unknown misconception labels are strictly rejected.</li>
        <li><b>Prompt-Injection Defenses:</b> Student reasoning text is capped at 300 characters, wrapped in isolated 
        untrusted XML tags, and instructed to be treated strictly as passive text data.</li>
        <li><b>Performance & Caching:</b> Identical prompt payloads are hashed and cached in memory to minimize latency 
        and conserve API quota.</li>
        <li><b>Graceful Offline Fallback:</b> If no API key is provided or network errors occur, the system degrades 
        gracefully to rule-based PER option diagnostics and bank items without throwing errors or exposing stack traces.</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)
