"""core/learner.py - Learner Model, Bayesian Knowledge Tracing (BKT) & Adaptive Selection

Implements:
1. Standard 4-parameter Bayesian Knowledge Tracing with misconception discount
2. Prerequisite propagation for effective mastery calculation
3. Multi-factor next-question selection policy (reviews, gaps, prerequisites, difficulty target)
"""

import math
from typing import Dict, List, Optional, Tuple, Any, Set
from core.concepts import CONCEPTS, MISCONCEPTIONS

# -----------------------------------------------------------------------------
# BKT DEFAULT PARAMETERS (NCERT / Physics Domain Calibrated)
# -----------------------------------------------------------------------------
DEFAULT_PRIOR = 0.30  # Initial probability of knowing the concept
DEFAULT_GUESS = 0.25  # P(correct | not known) - 4-choice MCQ guess baseline
DEFAULT_SLIP  = 0.10  # P(incorrect | known) - accidental slip
DEFAULT_LEARN = 0.12  # P(transition from not known -> known after an attempt)

def update_bkt(
    prior_mastery: float,
    is_correct: bool,
    has_misconception: bool = False,
    misconception_confidence: float = 0.0,
    guess: float = DEFAULT_GUESS,
    slip: float = DEFAULT_SLIP,
    learn: float = DEFAULT_LEARN,
) -> float:
    """
    Updates student mastery using Bayesian Knowledge Tracing.
    
    Special rule from specification (Section 6.2):
    "If the answer is correct but a misconception is detected with confidence >= 0.6,
    apply only 30% of the gain."
    """
    p = max(0.01, min(0.99, float(prior_mastery)))

    # 1. Posterior calculation conditioned on observation
    if is_correct:
        numerator = p * (1.0 - slip)
        denominator = numerator + (1.0 - p) * guess
    else:
        numerator = p * slip
        denominator = numerator + (1.0 - p) * (1.0 - guess)

    posterior = numerator / max(1e-9, denominator)

    # 2. Knowledge acquisition step
    raw_new_mastery = posterior + (1.0 - posterior) * learn

    # 3. Flawed reasoning discount: if correct but held key misconception
    if is_correct and has_misconception and misconception_confidence >= 0.6:
        gain = raw_new_mastery - prior_mastery
        final_mastery = prior_mastery + (0.30 * gain)
    else:
        final_mastery = raw_new_mastery

    return round(max(0.01, min(0.99, final_mastery)), 4)

def compute_effective_mastery(mastery: Dict[str, float]) -> Dict[str, float]:
    """
    Prerequisite propagation:
    If a concept's prerequisites have lower mastery, temporarily discount the
    effective mastery of its direct dependents by up to 15% when choosing
    what to practice. Does not overwrite permanent stored mastery.
    """
    effective = {}
    for cid, data in CONCEPTS.items():
        base = mastery.get(cid, DEFAULT_PRIOR)
        prereqs = data.get("prerequisites", [])
        if not prereqs:
            effective[cid] = base
            continue

        # Find worst prerequisite gap
        min_prereq_mastery = min([mastery.get(p, DEFAULT_PRIOR) for p in prereqs])
        if min_prereq_mastery < base:
            # Scale reduction up to 15% based on how far behind the prerequisite is
            gap = base - min_prereq_mastery
            penalty = 0.15 * gap
            effective[cid] = max(0.05, round(base - penalty, 4))
        else:
            effective[cid] = base

    return effective

def target_difficulty_for_mastery(mastery_val: float) -> int:
    """
    Target difficulty calibration rule (Section 6.3):
    - Below 0.40 mastery: Level 1 (Easy / Foundational)
    - Below 0.70 mastery: Level 2 (Medium / Application)
    - 0.70 and above:    Level 3 (Hard / Synthesis)
    """
    if mastery_val < 0.40:
        return 1
    elif mastery_val < 0.70:
        return 2
    else:
        return 3

def select_next_practice_concept(
    mastery: Dict[str, float],
    due_concepts: List[str],
) -> Tuple[str, str]:
    """
    Selects the next concept to practice according to priority hierarchy:
    1. Concepts due for spaced repetition review come first.
    2. Otherwise choose lowest effective-mastery concept.
    3. Prerequisite check: if a prerequisite is weaker than chosen concept
       by > 0.10, pivot to the prerequisite first.
       
    Returns:
      (chosen_concept_id, selection_reason_string)
    """
    eff = compute_effective_mastery(mastery)

    # 1. Spaced review due first
    if due_concepts:
        # If multiple are due, pick the one with lowest effective mastery
        c0 = min(due_concepts, key=lambda c: eff.get(c, 0.3))
        reason = f"Concept '{CONCEPTS[c0]['name']}' is due for spaced-repetition review (retrievability dropped below 90%)."
    else:
        # 2. Pick lowest effective mastery
        c0 = min(list(CONCEPTS.keys()), key=lambda c: eff.get(c, 0.3))
        reason = f"Identified as your lowest mastery area ({int(mastery.get(c0, 0.3) * 100)}%)."

    # 3. Prerequisite override check
    chosen = c0
    prereqs = CONCEPTS[c0].get("prerequisites", [])
    for p in prereqs:
        p_mastery = mastery.get(p, 0.3)
        c0_mastery = mastery.get(c0, 0.3)
        if p_mastery < (c0_mastery - 0.10):
            chosen = p
            reason = (
                f"Prerequisite '{CONCEPTS[p]['name']}' ({int(p_mastery * 100)}%) is significantly weaker "
                f"than '{CONCEPTS[c0]['name']}' ({int(c0_mastery * 100)}%). Reinforcing foundation first."
            )
            break

    return chosen, reason

def select_next_question(
    concept: str,
    mastery_val: float,
    active_misconception: Optional[str],
    asked_question_ids: Set[str],
    question_pool: List[Dict[str, Any]],
) -> Tuple[Dict[str, Any], str]:
    """
    Selects the best matching question for the chosen concept.
    
    1. Filters question pool to the target concept.
    2. If an active misconception exists for this concept, prioritises
       questions containing distractors tagged with that misconception.
    3. Matches target difficulty level.
    4. Avoids repeating items in the current session if unasked items exist.
    """
    target_d = target_difficulty_for_mastery(mastery_val)
    candidates = [q for q in question_pool if q["concept"] == concept]

    if not candidates:
        # Fallback to entire bank
        candidates = list(question_pool)

    # Prefer unasked questions
    unasked = [q for q in candidates if q["id"] not in asked_question_ids]
    search_pool = unasked if unasked else candidates

    # If an active misconception is flagged, prefer questions targeting it
    if active_misconception and active_misconception in MISCONCEPTIONS:
        misc_pool = [
            q for q in search_pool
            if any(t == active_misconception for t in q.get("tags", []))
        ]
        if misc_pool:
            # Pick best difficulty match among misconception-targeted items
            best = min(misc_pool, key=lambda q: abs(q["difficulty_label"] - target_d))
            rationale = (
                f"Targeted at misconception '{MISCONCEPTIONS[active_misconception]['label']}' "
                f"with difficulty level {best['difficulty_label']} of 3."
            )
            return best, rationale

    # Otherwise pick closest difficulty match
    best = min(search_pool, key=lambda q: abs(q["difficulty_label"] - target_d))
    rationale = f"Difficulty level {best['difficulty_label']} of 3 calibrated for {int(mastery_val * 100)}% mastery."
    return best, rationale
