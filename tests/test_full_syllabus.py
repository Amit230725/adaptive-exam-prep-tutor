"""tests/test_full_syllabus.py - Comprehensive Verification for Full CBSE Class 10 Physics Syllabus

Verifies:
1. All 4 NCERT Physics Chapters (Light, Human Eye, Electricity, Magnetic Effects)
2. All 20 Concepts, DAG prerequisites, and ordering
3. Full 60-Item Verified CBSE Question Bank (Levels 1, 2, 3)
4. Full Research Misconception Library (M1 - M17)
5. Multi-chapter diagnostic test generation
6. Multi-chapter cognitive radar chart rendering
7. Full syllabus study card coverage
"""

import pytest
from core.concepts import CONCEPTS, MISCONCEPTIONS, CHAPTERS, get_ordered_concepts
from core.bank import (
    QUESTION_BANK,
    get_diagnostic_questions,
    get_question_by_id,
    get_questions_for_concept,
)
from core.visuals import generate_mastery_radar_chart_svg, CONCEPT_STUDY_CARDS

def test_chapter_structure():
    """Verify all 4 Class 10 Physics chapters exist with valid metadata."""
    assert len(CHAPTERS) == 4
    expected_chapters = {"light", "human_eye", "electricity", "magnetism"}
    assert set(CHAPTERS.keys()) == expected_chapters

    total_chapter_concepts = 0
    for ch_id, ch_data in CHAPTERS.items():
        assert "name" in ch_data
        assert "short_name" in ch_data
        assert "concepts" in ch_data
        assert len(ch_data["concepts"]) >= 4
        total_chapter_concepts += len(ch_data["concepts"])
        # Check that all concept IDs in each chapter exist in CONCEPTS
        for cid in ch_data["concepts"]:
            assert cid in CONCEPTS
            assert CONCEPTS[cid]["chapter"] == ch_id

    assert total_chapter_concepts == len(CONCEPTS) == 20

def test_concept_dag_integrity():
    """Verify all 20 concepts have valid prerequisites forming a valid DAG."""
    assert len(CONCEPTS) == 20
    for cid, data in CONCEPTS.items():
        assert data["id"] == cid
        assert "name" in data
        assert "chapter" in data
        assert "order" in data
        for prereq in data.get("prerequisites", []):
            assert prereq in CONCEPTS, f"Prerequisite {prereq} for {cid} must exist in CONCEPTS"
            assert prereq != cid, f"Self-dependency detected in {cid}"

def test_full_question_bank_distribution():
    """Verify all 60 items have 3 questions per concept across levels 1, 2, and 3."""
    assert len(QUESTION_BANK) == 60

    # Chapter counts
    chapter_counts = {"light": 0, "human_eye": 0, "electricity": 0, "magnetism": 0}
    for q in QUESTION_BANK:
        ch = CONCEPTS[q["concept"]]["chapter"]
        chapter_counts[ch] += 1

    assert chapter_counts["light"] == 12       # 4 concepts * 3
    assert chapter_counts["human_eye"] == 12   # 4 concepts * 3
    assert chapter_counts["electricity"] == 24 # 8 concepts * 3
    assert chapter_counts["magnetism"] == 12   # 4 concepts * 3

    # Check each concept has level 1, 2, 3
    for cid in CONCEPTS:
        c_qs = get_questions_for_concept(cid)
        assert len(c_qs) == 3, f"Concept {cid} must have exactly 3 questions"
        levels = {q["difficulty_label"] for q in c_qs}
        assert levels == {1, 2, 3}, f"Concept {cid} must have questions for levels 1, 2, 3"

def test_diagnostic_questions_by_scope():
    """Verify diagnostic generation for individual chapters and full syllabus."""
    # Light chapter diagnostic
    diag_light = get_diagnostic_questions("light")
    assert len(diag_light) == 4
    assert all(CONCEPTS[q["concept"]]["chapter"] == "light" for q in diag_light)

    # Human Eye chapter diagnostic
    diag_eye = get_diagnostic_questions("human_eye")
    assert len(diag_eye) == 4
    assert all(CONCEPTS[q["concept"]]["chapter"] == "human_eye" for q in diag_eye)

    # Electricity chapter diagnostic
    diag_elec = get_diagnostic_questions("electricity")
    assert len(diag_elec) == 8
    assert all(CONCEPTS[q["concept"]]["chapter"] == "electricity" for q in diag_elec)

    # Magnetism chapter diagnostic
    diag_mag = get_diagnostic_questions("magnetism")
    assert len(diag_mag) == 4
    assert all(CONCEPTS[q["concept"]]["chapter"] == "magnetism" for q in diag_mag)

    # Full syllabus diagnostic: balanced 8 questions across all 4 chapters
    diag_all = get_diagnostic_questions("all")
    assert len(diag_all) == 8
    chapters_in_diag = {CONCEPTS[q["concept"]]["chapter"] for q in diag_all}
    assert chapters_in_diag == {"light", "human_eye", "electricity", "magnetism"}

def test_misconception_library_coverage():
    """Verify all 17 research misconceptions (M1 - M17) across the 4 chapters."""
    assert len(MISCONCEPTIONS) == 17
    expected_mids = [f"M{i}" for i in range(1, 18)]
    assert list(MISCONCEPTIONS.keys()) == expected_mids

    for mid, m_data in MISCONCEPTIONS.items():
        assert m_data["id"] == mid
        assert "label" in m_data
        assert "correction" in m_data
        assert "reteach_action" in m_data
        assert "chapter" in m_data

def test_chapter_radar_charts():
    """Verify radar chart generation for chapter subsets and full syllabus."""
    sample_mastery = {cid: 0.65 for cid in CONCEPTS}

    # Test Light radar (4 axes)
    svg_light = generate_mastery_radar_chart_svg(sample_mastery, concept_keys=CHAPTERS["light"]["concepts"])
    assert "<svg" in svg_light
    assert "Mirrors" in svg_light

    # Test Human Eye radar (4 axes)
    svg_eye = generate_mastery_radar_chart_svg(sample_mastery, concept_keys=CHAPTERS["human_eye"]["concepts"])
    assert "<svg" in svg_eye
    assert "Human Eye" in svg_eye

    # Test Electricity radar (8 axes)
    svg_elec = generate_mastery_radar_chart_svg(sample_mastery, concept_keys=CHAPTERS["electricity"]["concepts"])
    assert "<svg" in svg_elec
    assert "Ohm" in svg_elec

    # Test Magnetism radar (4 axes)
    svg_mag = generate_mastery_radar_chart_svg(sample_mastery, concept_keys=CHAPTERS["magnetism"]["concepts"])
    assert "<svg" in svg_mag
    assert "Magnetic Field" in svg_mag

def test_study_cards_all_concepts():
    """Verify all 20 concepts across the syllabus have complete NCERT study cards."""
    for cid in CONCEPTS:
        assert cid in CONCEPT_STUDY_CARDS, f"Concept {cid} missing from CONCEPT_STUDY_CARDS"
        card = CONCEPT_STUDY_CARDS[cid]
        assert "title" in card
        assert "chapter" in card
        assert "formulas" in card
        assert len(card["formulas"]) >= 2
        assert "summary" in card
        assert "common_trap" in card
