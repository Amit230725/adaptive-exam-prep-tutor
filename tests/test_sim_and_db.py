"""tests/test_sim_and_db.py - Tests for Database Aggregations, Simulated Class & Reteach Plan

Verifies:
1. Seeded simulated class generation reproducibility and labeling
2. Class-wide database queries and filtering
3. Call D AI/Offline reteach plan generation
"""

import pytest
from core.concepts import CONCEPTS, MISCONCEPTIONS
from core.sim import generate_simulated_class, get_simulated_misconception_stats
from core.db import (
    init_db,
    save_student,
    save_mastery_state,
    get_real_students_mastery,
    get_all_calibrated_items,
)
from core.ai import generate_reteach_plan

def test_simulated_class_reproducibility_and_labels():
    """Verify simulated class produces exactly 20 students with [SIMULATED] labels."""
    sim1 = generate_simulated_class(20)
    sim2 = generate_simulated_class(20)
    assert len(sim1) == 20
    assert len(sim2) == 20
    assert sim1[0]["Student"] == sim2[0]["Student"]
    assert "[SIMULATED]" in sim1[0]["Student"]
    assert sim1[0]["Is_Simulated"] is True

    # Check all concepts exist
    for cid in CONCEPTS:
        assert cid in sim1[0]
        assert 0.0 <= sim1[0][cid] <= 1.0

def test_simulated_misconceptions():
    """Verify simulated misconception stats match research library."""
    stats = get_simulated_misconception_stats()
    assert len(stats) == 7
    for row in stats:
        assert row["Misconception_ID"] in MISCONCEPTIONS
        assert row["Affected_Students"] > 0
        assert row["Source"] == "SIMULATED"

def test_db_student_mastery_aggregation():
    """Verify real students are stored and retrieved from SQLite."""
    init_db()
    test_id = "test_stu_99"
    save_student(test_id, "TestPupil", "CLASS-TEST")
    save_mastery_state(test_id, "charge", 0.85, 3.0, 3.0, 1)
    save_mastery_state(test_id, "current", 0.65, 1.5, 1.5, 1)

    records = get_real_students_mastery("CLASS-TEST")
    assert any(r["Student"] == "TestPupil" for r in records)
    pupil = next(r for r in records if r["Student"] == "TestPupil")
    assert pupil["charge"] == 0.85
    assert pupil["current"] == 0.65
    assert pupil["Is_Simulated"] is False

def test_calibrated_items_retrieval():
    """Verify all 24 questions are represented in calibration report."""
    items = get_all_calibrated_items()
    assert len(items) == 24
    for it in items:
        assert "Question_ID" in it
        assert "Labelled_b0" in it
        assert "Calibrated_b" in it
        assert "Calibration_Status" in it

def test_call_d_reteach_plan_structure():
    """Verify Call D produces 3-step remedial plan with 5-minute activities."""
    concept_avg = {"pd": 0.35, "parallel": 0.38, "current": 0.55}
    top_misc = [
        {"Misconception_ID": "M5", "Misconception": "Parallel increases resistance", "Affected_Students": 8},
        {"Misconception_ID": "M1", "Misconception": "Current used up", "Affected_Students": 7},
        {"Misconception_ID": "M3", "Misconception": "Confuses V and I", "Affected_Students": 6},
    ]

    plan = generate_reteach_plan(concept_avg, top_misc, api_key_override=None)
    assert "overview" in plan
    assert "lesson_plan" in plan
    steps = plan["lesson_plan"]
    assert len(steps) >= 1
    assert steps[0]["duration_minutes"] == 5
    assert "teacher_instructions" in steps[0]
    assert "check_question" in steps[0]
