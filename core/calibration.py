"""core/calibration.py - Item Difficulty Calibration via Rasch Model / IRT

Implements empirical item difficulty adjustment (Section 6.4):
- Labelled difficulty to initial b: Level 1 = -1.0, Level 2 = 0.0, Level 3 = +1.0
- Student ability: theta = logit(mastery), clamped to [-3.0, 3.0]
- Expected P(correct) = 1 / (1 + exp(-(theta - b)))
- Online gradient update: b <- b + 0.15 * (P_expected - outcome)
- Bayesian shrinkage toward labelled prior to prevent instability with few responses
"""

import math
from typing import Dict, Any, Tuple

# Mapping of integer curriculum difficulty label (1-3) to logit difficulty parameter b0
LABEL_TO_B0 = {
    1: -1.0,  # Easy
    2: 0.0,   # Medium
    3: 1.0,   # Hard
}

PRIOR_SHRINKAGE_WEIGHT = 2.0  # Weight given to original teacher label

def mastery_to_ability(mastery: float) -> float:
    """
    Transforms [0, 1] mastery probability into continuous ability theta in logits.
    Clamped to [-3.0, +3.0] to prevent infinities.
    """
    m = max(0.0474, min(0.9526, float(mastery)))  # logit(0.0474) ≈ -3.0, logit(0.9526) ≈ +3.0
    return math.log(m / (1.0 - m))

def expected_p_correct(theta: float, b: float) -> float:
    """
    Standard Rasch 1-PL Item Response Function:
    P(correct | theta, b) = 1 / (1 + exp(-(theta - b)))
    """
    z = theta - b
    # Numerical stability clamp
    z = max(-10.0, min(10.0, z))
    return 1.0 / (1.0 + math.exp(-z))

def update_item_difficulty(
    current_b: float,
    label_level: int,
    student_mastery: float,
    is_correct: bool,
    n_responses: int,
    learning_rate: float = 0.15,
) -> float:
    """
    Performs online calibration update after a student attempt.
    
    If an able student misses an easy question, item difficulty b increases.
    If a struggling student gets a hard question right, item difficulty b decreases.
    Shrinkage pulls back toward the label prior.
    """
    theta = mastery_to_ability(student_mastery)
    p_exp = expected_p_correct(theta, current_b)
    outcome = 1.0 if is_correct else 0.0

    # Gradient update step: delta = 0.15 * (P_expected - outcome)
    raw_b = current_b + learning_rate * (p_exp - outcome)

    # Bayesian shrinkage toward initial label prior b0
    b0 = LABEL_TO_B0.get(label_level, 0.0)
    total_n = n_responses + 1
    shrunk_b = (total_n * raw_b + PRIOR_SHRINKAGE_WEIGHT * b0) / (total_n + PRIOR_SHRINKAGE_WEIGHT)

    # Clamp b to realistic logit bounds [-3.0, 3.0]
    return round(max(-3.0, min(3.0, shrunk_b)), 3)

def format_calibration_summary(
    label_level: int,
    calibrated_b: float,
    n_responses: int,
) -> Dict[str, Any]:
    """Formats calibration metrics for UI display."""
    b0 = LABEL_TO_B0.get(label_level, 0.0)
    diff = calibrated_b - b0
    if abs(diff) < 0.15:
        status = "Aligned with label"
    elif diff > 0.15:
        status = f"Harder than labelled (+{diff:.2f})"
    else:
        status = f"Easier than labelled ({diff:.2f})"

    return {
        "labelled_b": b0,
        "calibrated_b": calibrated_b,
        "n_responses": n_responses,
        "status": status,
    }
