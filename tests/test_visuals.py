"""tests/test_visuals.py - Unit Tests for Visualizations & Circuit Simulation"""

import pytest
from core.visuals import generate_mastery_radar_chart_svg, simulate_circuit, CONCEPT_STUDY_CARDS
from core.concepts import CONCEPTS

def test_radar_chart_svg_generation():
    """Verify SVG radar chart renders cleanly with all concepts and valid XML markup."""
    sample_mastery = {
        "charge": 0.8,
        "current": 0.6,
        "pd": 0.4,
        "ohm": 0.7,
        "resistance": 0.5,
        "series": 0.65,
        "parallel": 0.35,
        "power": 0.55,
    }
    svg = generate_mastery_radar_chart_svg(sample_mastery)
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "<polygon" in svg
    for cid in CONCEPTS:
        c_short = CONCEPTS[cid]["name"].replace(" Circuits", "").replace(" & Factors", "")
        assert c_short in svg

def test_circuit_simulation_series():
    """Verify series circuit Ohm's law and power calculations."""
    sim = simulate_circuit(mode="series", voltage=12.0, r1=4.0, r2=8.0)
    assert sim["r_eq"] == 12.0  # 4 + 8
    assert sim["i_total"] == 1.0  # 12 / 12
    assert sim["v1"] == 4.0  # 1 * 4
    assert sim["v2"] == 8.0  # 1 * 8
    assert sim["p_total"] == 12.0  # 12 * 1
    assert "M1" in sim["misconception_note"]

def test_circuit_simulation_parallel():
    """Verify parallel circuit calculations."""
    sim = simulate_circuit(mode="parallel", voltage=12.0, r1=6.0, r2=12.0)
    assert sim["r_eq"] == 4.0  # (6 * 12) / (6 + 12) = 72 / 18 = 4.0
    assert sim["i1"] == 2.0  # 12 / 6
    assert sim["i2"] == 1.0  # 12 / 12
    assert sim["i_total"] == 3.0  # 2 + 1
    assert "M5" in sim["misconception_note"]

def test_study_cards_coverage():
    """Verify all 8 concepts have rich NCERT formula cards."""
    for cid in CONCEPTS:
        assert cid in CONCEPT_STUDY_CARDS
        assert len(CONCEPT_STUDY_CARDS[cid]["formulas"]) >= 2
        assert "common_trap" in CONCEPT_STUDY_CARDS[cid]
