"""core/calibration.py - Item Difficulty Calibration via Rasch Model / IRT & Quality Gates

Blueprint References:
- Section 10: "Adaptive selection and difficulty calibration"
- Section 11: "Question generation and content governance" (Quality gates, discrimination, distractor uptake)
"""

import math
from typing import Dict, Any, Tuple, List, Optional, Union

# Mapping of integer curriculum difficulty label (1-3) to logit difficulty parameter b0
LABEL_TO_B0 = {
    1: -1.0,  # Easy / Foundational
    2: 0.0,   # Medium / Application
    3: 1.0,   # Hard / Synthesis
}

PRIOR_SHRINKAGE_WEIGHT = 2.0  # Weight given to original teacher label

def mastery_to_ability(mastery: float) -> float:
    """Converts a BKT mastery probability into a logit ability parameter theta."""
    p = max(0.05, min(0.95, float(mastery)))
    return round(math.log(p / (1.0 - p)), 4)

def expected_p_correct(theta: float, b: float) -> float:
    """Computes Rasch model probability of a correct response: P(correct) = 1 / (1 + exp(-(theta - b)))."""
    diff = max(-5.0, min(5.0, theta - b))
    return round(1.0 / (1.0 + math.exp(-diff)), 4)

def update_item_difficulty(
    current_b: float,
    student_mastery: float,
    outcome: Optional[int] = None,
    n_prior_responses: int = 0,
    initial_label: int = 2,
    lr: float = 0.15,
    label_level: Optional[int] = None,
    is_correct: Optional[bool] = None,
    n_responses: Optional[int] = None,
) -> float:
    """
    Online stochastic gradient update for item difficulty b:
    b <- b + lr * (P_expected - outcome)
    Bayesian shrinkage pulls b gently toward the educator label b0 for small sample sizes.
    Returns the updated b value as a float.
    """
    if is_correct is not None:
        outcome = 1 if is_correct else 0
    elif outcome is None:
        outcome = 1

    if label_level is not None:
        initial_label = label_level

    if n_responses is not None:
        n_prior_responses = n_responses

    theta = mastery_to_ability(student_mastery)
    p_exp = expected_p_correct(theta, current_b)

    gradient_step = lr * (p_exp - float(outcome))
    raw_new_b = current_b + gradient_step

    b0 = LABEL_TO_B0.get(initial_label, 0.0)
    shrinkage = PRIOR_SHRINKAGE_WEIGHT / (PRIOR_SHRINKAGE_WEIGHT + max(1, n_prior_responses))
    shrunk_b = (1.0 - shrinkage) * raw_new_b + shrinkage * b0

    clamped_b = max(-3.0, min(3.0, shrunk_b))
    return round(clamped_b, 4)

def format_calibration_summary(
    arg1: Union[int, float],
    arg2: Union[float, int] = 0.0,
    arg3: int = 0,
) -> Dict[str, Any]:
    """
    Supports both:
    - format_calibration_summary(label_d, cal_b, n_ans)
    - format_calibration_summary(cal_b, n_resp)
    Returns dictionary with labelled_b, calibrated_b, and status strings.
    """
    if isinstance(arg1, int) and arg1 in [1, 2, 3]:
        label_d = arg1
        cal_b = float(arg2)
        n_ans = int(arg3)
    else:
        cal_b = float(arg1)
        n_ans = int(arg2)
        label_d = 2

    b0 = LABEL_TO_B0.get(label_d, 0.0)
    if cal_b < -0.5:
        desc = "Easy (Calibrated)"
    elif cal_b <= 0.5:
        desc = "Medium (Calibrated)"
    else:
        desc = "Hard (Calibrated)"

    status = "Stable" if n_ans >= 10 else ("Calibrating" if n_ans > 0 else "Prior Only")
    return {
        "labelled_b": b0,
        "calibrated_b": cal_b,
        "status": status,
        "desc": desc,
        "summary": f"{desc} | b = {cal_b:+.2f} ({n_ans} responses)",
    }

def compute_item_discrimination(item_responses: List[Dict[str, Any]]) -> float:
    """Computes Point-Biserial Discrimination Index."""
    if len(item_responses) < 4:
        return 0.35
    correct_totals = [r["total_score"] for r in item_responses if r.get("correct") == 1]
    incorrect_totals = [r["total_score"] for r in item_responses if r.get("correct") == 0]
    n = len(item_responses)
    p = len(correct_totals) / n
    if p <= 0.0 or p >= 1.0:
        return 0.0
    all_scores = [r["total_score"] for r in item_responses]
    mean_all = sum(all_scores) / n
    var_all = sum((x - mean_all) ** 2 for x in all_scores) / max(1, n - 1)
    std_all = math.sqrt(max(1e-6, var_all))
    mean_corr = sum(correct_totals) / len(correct_totals) if correct_totals else mean_all
    mean_inc = sum(incorrect_totals) / len(incorrect_totals) if incorrect_totals else mean_all
    r_pbis = ((mean_corr - mean_inc) / max(1e-6, std_all)) * math.sqrt(p * (1.0 - p))
    return round(max(-1.0, min(1.0, r_pbis)), 3)

def compute_distractor_uptake(item_responses: List[Dict[str, Any]]) -> Dict[int, float]:
    """Calculates percentage of attempts picking options 0, 1, 2, 3."""
    total = len(item_responses)
    if total == 0:
        return {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25}
    counts = {0: 0, 1: 0, 2: 0, 3: 0}
    for r in item_responses:
        ch = r.get("chosen", 0)
        if ch in counts:
            counts[ch] += 1
    return {opt: round(cnt / total, 3) for opt, cnt in counts.items()}

def flag_item_anomalies(
    item_id: str,
    difficulty_b: float,
    discrimination: float,
    distractor_uptake: Dict[int, float],
    correct_idx: int,
) -> List[str]:
    """Quality gates per Blueprint Section 11."""
    flags = []
    if discrimination < 0.0:
        flags.append(f"Negative discrimination ({discrimination:.2f}): high scorers miss this item.")
    elif discrimination < 0.15:
        flags.append(f"Low discrimination ({discrimination:.2f}): poor separation.")
    for opt, uptake in distractor_uptake.items():
        if opt != correct_idx and uptake > 0.45:
            flags.append(f"Popular distractor ({chr(65+opt)} chosen by {int(uptake*100)}%).")
    return flags
