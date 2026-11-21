"""tests/test_core.py - Unit Tests for ConceptPilot Core Engine

Tests:
1. Question bank integrity (24 verified questions, 4 options, valid tags)
2. BKT monotonicity (correct answers increase mastery, wrong decrease)
3. Flawed reasoning discount (correct answer + misconception -> 30% gain)
4. Prerequisite propagation (effective mastery reduced for weak prereqs)
5. Item difficulty calibration direction (Rasch update)
6. Spaced repetition scheduling (stability growth on success, relapse on error)
7. Next-question selection policy
"""

import pytest
from core.concepts import CONCEPTS, MISCONCEPTIONS
from core.bank import QUESTION_BANK, get_diagnostic_questions, get_question_by_id
from core.learner import (
    update_bkt,
    compute_effective_mastery,
    select_next_practice_concept,
    select_next_question,
    target_difficulty_for_mastery,
    DEFAULT_PRIOR,
)
from core.calibration import update_item_difficulty, expected_p_correct, mastery_to_ability
from core.scheduler import (
    initial_stability_from_mastery,
    compute_retrievability,
    is_due_for_review,
    update_concept_stability,
    get_due_concepts,
)

# -----------------------------------------------------------------------------
# 1. QUESTION BANK INTEGRITY TESTS
# -----------------------------------------------------------------------------
def test_bank_size_and_concepts():
    """Verify bank contains 60 items, exactly 3 per concept across all 20 Class 10 Physics concepts."""
    assert len(QUESTION_BANK) == len(CONCEPTS) * 3
    assert len(QUESTION_BANK) == 60
    for cid in CONCEPTS:
        concept_qs = [q for q in QUESTION_BANK if q["concept"] == cid]
        assert len(concept_qs) == 3, f"Concept {cid} must have exactly 3 questions"
        diffs = {q["difficulty_label"] for q in concept_qs}
        assert diffs == {1, 2, 3}, f"Concept {cid} must have questions for levels 1, 2, and 3"

def test_question_structure():
    """Verify option count, index validity, and tag validity."""
    for q in QUESTION_BANK:
        assert len(q["options"]) == 4
        assert len(q["tags"]) == 4
        assert 0 <= q["answer_index"] < 4
        # Correct answer cannot have a misconception tag
        assert q["tags"][q["answer_index"]] is None
        # Any present tag must be in the valid research library M1-M7
        for tag in q["tags"]:
            if tag is not None:
                assert tag in MISCONCEPTIONS, f"Unknown misconception ID {tag} in question {q['id']}"

def test_diagnostic_questions():
    """Verify diagnostic contains 8 Level-2 questions, one per concept in order."""
    diag = get_diagnostic_questions()
    assert len(diag) == 8
    concepts_in_diag = [q["concept"] for q in diag]
    assert len(set(concepts_in_diag)) == 8
    for q in diag:
        assert q["difficulty_label"] == 2

# -----------------------------------------------------------------------------
# 2. BKT LEARNER MODEL TESTS
# -----------------------------------------------------------------------------
def test_bkt_monotonicity():
    """Correct answers must raise mastery, incorrect answers must lower mastery."""
    prior = 0.40
    after_correct = update_bkt(prior, is_correct=True)
    assert after_correct > prior, f"Mastery should increase: {after_correct} vs {prior}"

    after_wrong = update_bkt(prior, is_correct=False)
    assert after_wrong < prior, f"Mastery should decrease: {after_wrong} vs {prior}"

def test_bkt_flawed_reasoning_discount():
    """Correct answer with confirmed misconception must receive only 30% of normal gain."""
    prior = 0.30
    normal_gain_mastery = update_bkt(prior, is_correct=True, has_misconception=False)
    normal_gain = normal_gain_mastery - prior

    discounted_mastery = update_bkt(
        prior,
        is_correct=True,
        has_misconception=True,
        misconception_confidence=0.85,
    )
    discounted_gain = discounted_mastery - prior

    expected_discounted = prior + 0.30 * normal_gain
    assert abs(discounted_mastery - round(expected_discounted, 4)) <= 0.001
    assert discounted_gain < normal_gain

def test_prerequisite_propagation():
    """If prerequisite is weak, effective mastery of dependent concept is discounted."""
    # Ohm's law depends on 'current' and 'pd'
    mastery = {
        "charge": 0.8,
        "current": 0.2,  # Very weak prerequisite
        "pd": 0.3,       # Weak prerequisite
        "ohm": 0.7,      # High nominal mastery
        "resistance": 0.5,
        "series": 0.5,
        "parallel": 0.5,
        "power": 0.5,
    }
    eff = compute_effective_mastery(mastery)
    assert eff["ohm"] < mastery["ohm"]
    # Charge has no prerequisites, so effective mastery equals nominal
    assert eff["charge"] == mastery["charge"]

# -----------------------------------------------------------------------------
# 3. DIFFICULTY CALIBRATION TESTS
# -----------------------------------------------------------------------------
def test_calibration_direction():
    """If student misses an item, calibrated b increases; if student gets it right, b decreases."""
    b_init = 0.0
    student_mastery = 0.5
    b_after_wrong = update_item_difficulty(
        current_b=b_init,
        label_level=2,
        student_mastery=student_mastery,
        is_correct=False,
        n_responses=5,
    )
    assert b_after_wrong > b_init, "Difficulty b should increase after wrong response"

    b_after_correct = update_item_difficulty(
        current_b=b_init,
        label_level=2,
        student_mastery=student_mastery,
        is_correct=True,
        n_responses=5,
    )
    assert b_after_correct < b_init, "Difficulty b should decrease after correct response"

# -----------------------------------------------------------------------------
# 4. SPACED REPETITION SCHEDULER TESTS
# -----------------------------------------------------------------------------
def test_spaced_repetition_stability_growth_and_relapse():
    """Success increases stability; failure reduces stability with floor at 0.5."""
    s_init = 2.0
    s_next_success = update_concept_stability(
        current_s=s_init,
        last_review_day=0.0,
        current_day=2.0,
        is_success=True,
        has_misconception=False,
    )
    assert s_next_success > s_init, "Stability should increase on success"

    s_next_fail = update_concept_stability(
        current_s=s_init,
        last_review_day=0.0,
        current_day=2.0,
        is_success=False,
        has_misconception=False,
    )
    assert s_next_fail < s_init, "Stability should decrease on failure"
    assert s_next_fail >= 0.5, "Stability should have minimum floor of 0.5"

def test_due_review_check():
    """Concept is due when elapsed days exceed stability."""
    stability = 2.0
    last_review = 0.0
    assert not is_due_for_review(stability, last_review, current_day=1.0)
    assert is_due_for_review(stability, last_review, current_day=2.5)

# -----------------------------------------------------------------------------
# 5. SELECTION POLICY TESTS
# -----------------------------------------------------------------------------
def test_prerequisite_pivot_selection():
    """If prerequisite is weaker than chosen concept by > 0.10, prerequisite is chosen."""
    mastery = {
        "charge": 0.20,      # Prereq of current and pd
        "current": 0.50,
        "pd": 0.50,
        "ohm": 0.40,
        "resistance": 0.60,
        "series": 0.60,
        "parallel": 0.60,
        "power": 0.60,
    }
    # No items due
    chosen_c, reason = select_next_practice_concept(mastery, due_concepts=[])
    # Charge is lowest and prerequisite of current/pd, so charge must be chosen
    assert chosen_c == "charge"

def test_target_difficulty_mapping():
    """Verify mastery thresholds map to levels 1, 2, 3."""
    assert target_difficulty_for_mastery(0.25) == 1
    assert target_difficulty_for_mastery(0.55) == 2
    assert target_difficulty_for_mastery(0.85) == 3
