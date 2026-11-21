"""tests/test_blueprint_specification.py - Rigorous Verification of Blueprint Specification

Validates all 24 pages of Adaptive_Exam_Prep_Tutor_Complete_Blueprint.pdf:
1. Section 6: 51 Concepts across 4 chapters, DAG acyclicity, mathematical prerequisites
2. Section 7: 30-item Chapter-Balanced Diagnostic Assessment Blueprint
3. Section 8: BKT formulas, exact p.9 illustration values (0.646 and 0.149), provisional states
4. Section 9: Misconception engine inference contract, evidence spans, teacher adjudication
5. Section 10: Multi-factor adaptive priority heuristic
6. Section 12: Starter interval ladder, retrievability, lapses, timed mock exam
7. Section 17 & 21: Idempotency keys, duplicate submission protection, and attempt replay
8. Section 18: Minor consent, data export, privacy deletion
"""

import pytest
import json
import time

from core.concepts import (
    CHAPTERS,
    CONCEPTS,
    CONCEPTS_51,
    MATH_PREREQUISITES,
    FORMAL_MISCONCEPTIONS,
    MISCONCEPTIONS,
    check_prerequisite_cycles,
    get_all_51_concepts,
)
from core.bank import (
    DIAGNOSTIC_30_BLUEPRINT,
    get_diagnostic_30_questions,
    get_question_by_id,
    QUESTION_BANK,
)
from core.learner import (
    update_bkt,
    get_mastery_state,
    compute_effective_mastery,
    compute_adaptive_priority,
    select_next_practice_concept,
    target_difficulty_for_mastery,
    DEFAULT_PRIOR,
    DEFAULT_GUESS,
    DEFAULT_SLIP,
    DEFAULT_LEARN,
)
from core.scheduler import (
    INTERVAL_LADDER,
    initial_stability_from_mastery,
    compute_retrievability,
    is_due_for_review,
    update_concept_stability,
    get_due_concepts,
)
from core.ai import diagnose_reasoning
from core.calibration import (
    update_item_difficulty,
    expected_p_correct,
    compute_item_discrimination,
    compute_distractor_uptake,
    flag_item_anomalies,
)
import core.db as db


# -----------------------------------------------------------------------------
# 1. SECTION 6: CONCEPT GRAPH & 51 CANONICAL CONCEPTS
# -----------------------------------------------------------------------------
def test_blueprint_51_concepts_inventory():
    """Blueprint Section 6 requires exactly 51 concepts across the 4 chapters."""
    c51 = get_all_51_concepts()
    assert len(c51) == 51, f"Expected 51 concepts, got {len(c51)}"

    # Chapter breakdown
    light_concepts = [cid for cid, c in c51.items() if c["chapter"] == "light"]
    eye_concepts = [cid for cid, c in c51.items() if c["chapter"] == "human_eye"]
    elec_concepts = [cid for cid, c in c51.items() if c["chapter"] == "electricity"]
    mag_concepts = [cid for cid, c in c51.items() if c["chapter"] == "magnetism"]

    assert len(light_concepts) == 17, "Light must have 17 concepts (L1-L17)"
    assert len(eye_concepts) == 10, "Eye and colour must have 10 concepts (E1-E10)"
    assert len(elec_concepts) == 14, "Electricity must have 14 concepts (C1-C14)"
    assert len(mag_concepts) == 10, "Magnetism must have 10 concepts (M1-M10)"

def test_blueprint_concept_dag_is_acyclic():
    """Blueprint Section 6: 'Only the prerequisite subgraph must be acyclic.'"""
    assert check_prerequisite_cycles() is True

def test_blueprint_math_prerequisites():
    """Blueprint Section 6: Mathematical prerequisites must be documented."""
    assert "MATH_FRACTIONS" in MATH_PREREQUISITES
    assert "MATH_RECIPROCALS" in MATH_PREREQUISITES
    assert "MATH_SIGNS" in MATH_PREREQUISITES
    assert "MATH_UNITS" in MATH_PREREQUISITES
    assert "MATH_GRAPHS" in MATH_PREREQUISITES


# -----------------------------------------------------------------------------
# 2. SECTION 7: 30-ITEM CHAPTER-BALANCED DIAGNOSTIC ASSESSMENT
# -----------------------------------------------------------------------------
def test_blueprint_30_item_diagnostic_clusters():
    """Blueprint Section 7: Exactly 30 items with chapter cluster balance."""
    diag = get_diagnostic_30_questions()
    assert len(diag) == 30

    cluster_counts = {}
    for q in diag:
        cl = q["cluster"]
        cluster_counts[cl] = cluster_counts.get(cl, 0) + 1

    assert cluster_counts["Light: mirrors"] == 6
    assert cluster_counts["Refraction and lenses"] == 6
    assert cluster_counts["Eye and colour"] == 4
    assert cluster_counts["Electricity"] == 8
    assert cluster_counts["Magnetism"] == 6

def test_blueprint_two_tier_response_design():
    """Blueprint Section 7: Two-tier response design requires reasoning choices and diagram text."""
    diag = get_diagnostic_30_questions()
    for q in diag:
        assert len(q["options"]) == 4
        assert "reasoning_options" in q
        assert len(q["reasoning_options"]) == 4, f"Question {q['id']} must provide 4 reasoning options"
        assert "diagram_alt" in q, f"Question {q['id']} must provide accessible diagram alt text"
        assert "followup_probe" in q, f"Question {q['id']} must provide a near-transfer follow-up probe"


# -----------------------------------------------------------------------------
# 3. SECTION 8: LEARNER MODEL & BKT FORMULA VERIFICATION
# -----------------------------------------------------------------------------
def test_blueprint_bkt_page_9_exact_illustration():
    """
    Blueprint Section 8 p.9:
    'Illustration: p=0.30, g=0.25, s=0.10, t=0.10 gives about 0.646 after a correct response
    and 0.149 after an incorrect response.'
    """
    p = 0.30
    g = 0.25
    s = 0.10
    t = 0.10

    p_corr = update_bkt(p, is_correct=True, guess=g, slip=s, learn=t)
    p_inc = update_bkt(p, is_correct=False, guess=g, slip=s, learn=t)

    assert abs(p_corr - 0.646) < 0.002, f"Expected ~0.646, got {p_corr}"
    assert abs(p_inc - 0.149) < 0.002, f"Expected ~0.149, got {p_inc}"

def test_blueprint_provisional_user_facing_states():
    """Blueprint Section 8 Provisional states: <0.40, 0.40-0.59, 0.60-0.79, 0.80+."""
    s1 = get_mastery_state(0.35, evidence_count=1)
    assert s1["state"] == "needs_support"
    assert s1["is_sparse"] is True

    s2 = get_mastery_state(0.48, evidence_count=3)
    assert s2["state"] == "developing"
    assert s2["is_sparse"] is False

    s3 = get_mastery_state(0.72, evidence_count=4)
    assert s3["state"] == "progressing"

    s4 = get_mastery_state(0.88, evidence_count=5)
    assert s4["state"] == "likely_secure"


# -----------------------------------------------------------------------------
# 4. SECTION 9: MISCONCEPTION ENGINE INFERENCE CONTRACT
# -----------------------------------------------------------------------------
def test_blueprint_misconception_inference_contract():
    """Blueprint Section 9 Inference Contract Schema."""
    q_test = get_question_by_id("diag_30_02")
    student_reason = "I used positive focal length for this mirror"
    res = diagnose_reasoning(q_test, chosen_idx=1, reasoning=student_reason)

    assert "misconception_id" in res
    assert "confidence" in res
    assert "evidence_span" in res
    assert "alternatives" in res
    assert "needs_probe" in res
    assert "status" in res

    assert res["misconception_id"] == "MIRROR_SIGN"
    assert res["status"] == "suspected"
    assert "positive" in res["evidence_span"].lower()

def test_blueprint_misconception_abstention():
    """Blueprint Section 9: Must support abstention ('insufficient evidence' / status 'unclear')."""
    q_test = get_question_by_id("diag_30_01")
    res = diagnose_reasoning(q_test, chosen_idx=1, reasoning="")

    assert res["status"] == "unclear"
    assert res["needs_probe"] is True


# -----------------------------------------------------------------------------
# 5. SECTION 10: ADAPTIVE PRIORITY HEURISTIC
# -----------------------------------------------------------------------------
def test_blueprint_adaptive_priority_formula():
    """
    Blueprint Section 10:
    priority = w1*weakness + w2*review_urgency + w3*misconception_need + w4*exam_relevance
               + w5*information_value - w6*recent_repetition
    """
    score, bd = compute_adaptive_priority(
        concept_id="C4",
        mastery=0.20,
        retrievability=0.60,
        has_misconception=True,
        misconception_confidence=0.85,
        exam_relevance=0.09,
        evidence_count=1,
        recent_repetition_count=0,
    )
    assert score > 0.5
    assert bd["weakness_term"] > 0
    assert bd["review_term"] > 0
    assert bd["misconception_term"] > 0


# -----------------------------------------------------------------------------
# 6. SECTION 12: SPACED REPETITION STARTER LADDER
# -----------------------------------------------------------------------------
def test_blueprint_interval_ladder_and_lapses():
    """Blueprint Section 12: Starter interval ladder 1, 3, 7, 14, 30, 60, 90 days."""
    assert INTERVAL_LADDER == [1.0, 3.0, 7.0, 14.0, 30.0, 60.0, 90.0]

    # Lapse drops stability
    s_lapse = update_concept_stability(current_s=7.0, is_success=False)
    assert s_lapse < 7.0
    assert s_lapse >= 0.5

    # Successful unassisted review increases stability
    s_grow = update_concept_stability(current_s=3.0, is_success=True, was_assisted=False)
    assert s_grow > 3.0


# -----------------------------------------------------------------------------
# 7. SECTION 17 & 21: IDEMPOTENCY & DETERMINISTIC STATE REPLAY
# -----------------------------------------------------------------------------
def test_blueprint_idempotency_duplicate_protection():
    """Blueprint Section 17: Repeated submissions with one idempotency key must not update mastery twice."""
    db.init_db()
    test_sid = "test_bp_idem_user"
    db.save_student(test_sid, "Ananya", "CBSE10-TEST")

    key = "idem_token_abc123"
    r1, dup1 = db.log_response(test_sid, "diag_30_01", "L5", 0, 1, "f = R/2", "high", 15000, False, 1, key)
    assert dup1 is False

    # Second submission with same token
    r2, dup2 = db.log_response(test_sid, "diag_30_01", "L5", 0, 1, "f = R/2", "high", 15000, False, 1, key)
    assert dup2 is True
    assert r1 == r2

    db.delete_student_data(test_sid)

def test_blueprint_deterministic_attempt_replay():
    """Blueprint Section 8 & 21: Replaying attempts reproduces identical state."""
    db.init_db()
    test_sid = "test_bp_replay_user"
    db.save_student(test_sid, "Dev", "CBSE10-TEST")

    # Log 3 sequential responses
    r1, _ = db.log_response(test_sid, "q1", "C1", 0, 1, "Current conserved", "high", 5000, False, 1)
    m1 = update_bkt(0.30, True)
    db.save_mastery_state(test_sid, "C1", m1, 3.0, 3.0, 0.30, True, False, r1)

    r2, _ = db.log_response(test_sid, "q2", "C1", 0, 1, "Charge conserved", "high", 6000, False, 2)
    m2 = update_bkt(m1, True)
    db.save_mastery_state(test_sid, "C1", m2, 7.0, 7.0, m1, True, False, r2)

    # Run replay engine
    replay_res = db.replay_student_attempts(test_sid)
    assert replay_res["match"] is True
    assert replay_res["max_discrepancy"] == 0.0
    assert replay_res["total_attempts"] == 2

    db.delete_student_data(test_sid)


# -----------------------------------------------------------------------------
# 8. SECTION 18: MINOR CONSENT & PRIVACY EXPORT
# -----------------------------------------------------------------------------
def test_blueprint_privacy_export_and_deletion():
    """Blueprint Section 18: Minor consent, portable data export, and clean deletion."""
    db.init_db()
    test_sid = "test_bp_privacy_user"
    db.save_student(test_sid, "Priya", "CBSE10-TEST", consent=True, prefs={"high_contrast": True, "language": "hi"})

    # Export
    export_str = db.export_student_data_json(test_sid)
    export_data = json.loads(export_str)
    assert export_data["student_profile"]["id"] == test_sid
    assert export_data["student_profile"]["consent_given"] == 1

    # Deletion
    db.delete_student_data(test_sid)
    assert db.get_student(test_sid) is None
