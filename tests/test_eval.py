"""tests/test_eval.py - Unit test for synthetic benchmark execution"""

from scripts.eval_synthetic import run_synthetic_benchmark

def test_synthetic_cohort_recovery():
    """Verify all 7 synthetic student profiles run through the diagnosis pipeline cleanly."""
    res = run_synthetic_benchmark(api_key=None)
    assert res["total"] == 7
    # Offline heuristic + distractor tags should recover 100% of planted cases
    assert res["recovered"] == 7
    assert res["recovery_rate"] == 1.0
