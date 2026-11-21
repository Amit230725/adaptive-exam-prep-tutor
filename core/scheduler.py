"""core/scheduler.py - Spaced Repetition Scheduling (FSRS-Inspired)

Tracks retrievability R(t) and memory stability S (in days) per concept.
A concept is marked due for review when retrievability drops to <= 90%.
"""

from typing import Dict, List, Any, Optional

def initial_stability_from_mastery(mastery_val: float) -> float:
    """
    Initial stability assignment after the diagnostic test (Section 6.7):
    - Below 0.40 mastery: S = 0.5 days
    - Below 0.70 mastery: S = 1.0 days
    - 0.70 and above:    S = 3.0 days
    """
    if mastery_val < 0.40:
        return 0.5
    elif mastery_val < 0.70:
        return 1.0
    else:
        return 3.0

def compute_retrievability(stability: float, days_since_review: float) -> float:
    """
    FSRS retrievability formula:
    R(t) = 0.9 ^ (t / S)
    """
    if stability <= 0.05:
        return 0.0
    if days_since_review <= 0.0:
        return 1.0
    return round(0.9 ** (days_since_review / stability), 4)

def is_due_for_review(stability: float, last_review_day: float, current_day: float) -> bool:
    """
    Concept is due for review when retrievability R(t) <= 0.90,
    which corresponds to elapsed time t >= S.
    """
    elapsed = max(0.0, current_day - last_review_day)
    r = compute_retrievability(stability, elapsed)
    return r <= 0.90 or elapsed >= stability

def update_concept_stability(
    current_s: float,
    last_review_day: float,
    current_day: float,
    is_success: bool,
    has_misconception: bool = False,
) -> float:
    """
    Updates memory stability S after an attempt:
    - On success (correct without misconception):
        S <- S * (1.6 + (1 - R))
    - On failure or detected misconception:
        S <- max(0.5, S * 0.4)
    """
    elapsed = max(0.0, current_day - last_review_day)
    r = compute_retrievability(current_s, elapsed)

    if is_success and not has_misconception:
        # Retention boost
        multiplier = 1.6 + (1.0 - r)
        new_s = current_s * multiplier
    else:
        # Memory penalty / relapse
        new_s = max(0.5, current_s * 0.4)

    return round(min(180.0, new_s), 2)  # Cap at 180 days

def get_due_concepts(
    schedule: Dict[str, Dict[str, float]],
    current_day: float,
) -> List[str]:
    """Returns list of concept IDs currently due for spaced review."""
    due = []
    for cid, state in schedule.items():
        s = state.get("stability", 1.0)
        last_day = state.get("last_review_day", 0.0)
        if is_due_for_review(s, last_day, current_day):
            due.append(cid)
    return due
