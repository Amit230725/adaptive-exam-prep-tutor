"""core/scheduler.py - Spaced Repetition Scheduling & Retrieval Tracking

Blueprint Reference: Section 12 "Spaced repetition and exam readiness"
Starter interval ladder: 1, 3, 7, 14, 30, 60, 90 days.
Retrievability: R(t) = 0.9 ^ (t / S)
Handles lapses, assisted vs unassisted responses, and review due queue.
"""

from typing import Dict, List, Any, Optional, Tuple

# Starter interval ladder in days (Blueprint Section 12)
INTERVAL_LADDER = [1.0, 3.0, 7.0, 14.0, 30.0, 60.0, 90.0]

def initial_stability_from_mastery(mastery_val: float) -> float:
    """
    Initial stability assignment after diagnostic assessment:
    - Below 0.40 mastery: S = 1.0 day
    - Below 0.70 mastery: S = 3.0 days
    - 0.70 and above:    S = 7.0 days
    """
    if mastery_val < 0.40:
        return 1.0
    elif mastery_val < 0.70:
        return 3.0
    else:
        return 7.0

def compute_retrievability(stability: float, days_since_review: float) -> float:
    """
    Memory retrievability R(t):
    R(t) = 0.9 ^ (t / S)
    At t = S days, R(S) = 0.90 (90% retrievability threshold).
    """
    s = max(0.1, float(stability))
    t = max(0.0, float(days_since_review))
    return round(0.9 ** (t / s), 4)

def is_due_for_review(
    stability: float,
    last_review_day: float,
    current_day: float,
    threshold: float = 0.90,
) -> bool:
    """
    A concept is due when retrievability drops to <= threshold (or days elapsed >= stability).
    """
    days_elapsed = max(0.0, current_day - last_review_day)
    r = compute_retrievability(stability, days_elapsed)
    return r <= threshold

def update_concept_stability(
    current_s: float = 1.0,
    last_review_day: float = 0.0,
    current_day: float = 0.0,
    is_success: bool = True,
    has_misconception: bool = False,
    was_correct: Optional[bool] = None,
    was_assisted: bool = False,
    current_stability: Optional[float] = None,
    streak: int = 0,
) -> float:
    """
    Updates concept stability per Blueprint Section 12:
    - If success without misconception: stability increases (multiplied by ~1.6, up to ladder limit).
    - If success with misconception: stability increases moderately (multiplied by 1.1).
    - If failure / lapse: stability decreases with a minimum floor of 0.5 days.
    Returns new stability as a float.
    """
    if was_correct is not None:
        is_success = was_correct
    if current_stability is not None:
        current_s = current_stability

    s = max(0.5, float(current_s))

    if is_success:
        if has_misconception or was_assisted:
            new_s = s * 1.15
        else:
            new_s = s * 1.6
        new_s = min(90.0, new_s)
    else:
        # Lapse: decrease stability, minimum floor 0.5
        new_s = max(0.5, s * 0.5)

    return round(new_s, 2)

def get_due_concepts(
    schedule: Dict[str, Dict[str, Any]],
    current_day: float,
    threshold: float = 0.90,
) -> List[str]:
    """Returns list of concept IDs currently due for spaced review."""
    due = []
    for cid, data in schedule.items():
        s = data.get("stability", 1.0)
        last_d = data.get("last_review_day", 0.0)
        if is_due_for_review(s, last_d, current_day, threshold):
            due.append(cid)
    return due
