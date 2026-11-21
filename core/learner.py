"""core/learner.py - Learner Model, Bayesian Knowledge Tracing (BKT) & Adaptive Selection

Blueprint References:
- Section 8: "Learner model and mastery updates" (BKT, guess=0.25, slip=0.10, learn=0.10, provisional states)
- Section 10: "Adaptive selection and difficulty calibration" (multi-factor priority heuristic)
"""

import math
from typing import Dict, List, Optional, Tuple, Any, Set
from core.concepts import CONCEPTS, CONCEPTS_51, MISCONCEPTIONS, FORMAL_MISCONCEPTIONS

# -----------------------------------------------------------------------------
# BKT PARAMETERS (Calibrated per Blueprint Section 8)
# -----------------------------------------------------------------------------
DEFAULT_PRIOR = 0.30  # Initial unobserved probability of mastery
DEFAULT_GUESS = 0.25  # P(correct | not known) - 4-choice random guess baseline
DEFAULT_SLIP  = 0.10  # P(incorrect | known) - accidental slip
DEFAULT_LEARN = 0.10  # P(transition from not known -> known after an attempt)

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
    
    Formulas (Blueprint Section 8):
    p = prior mastery; g = guess; s = slip; t = learn
    If correct:   q = p*(1-s) / (p*(1-s) + (1-p)*g)
    If incorrect: q = p*s / (p*s + (1-p)*(1-g))
    Next mastery: p_next = q + (1-q)*t
    
    Verification check from Blueprint p.9:
    p=0.30, g=0.25, s=0.10, t=0.10 gives:
    - 0.646 after a correct response
    - 0.149 after an incorrect response
    
    If the answer is correct but a persistent misconception is detected (conf >= 0.60),
    apply only 30% of the knowledge gain.
    """
    p = max(0.01, min(0.99, float(prior_mastery)))

    # 1. Posterior calculation conditioned on evidence observation
    if is_correct:
        numerator = p * (1.0 - slip)
        denominator = numerator + (1.0 - p) * guess
    else:
        numerator = p * slip
        denominator = numerator + (1.0 - p) * (1.0 - guess)

    q = numerator / max(1e-9, denominator)

    # 2. Knowledge transition step
    raw_p_next = q + (1.0 - q) * learn

    # 3. Flawed reasoning discount: if correct but harbours active misconception
    if is_correct and has_misconception and misconception_confidence >= 0.60:
        gain = raw_p_next - prior_mastery
        final_mastery = prior_mastery + (0.30 * gain)
    else:
        final_mastery = raw_p_next

    return round(max(0.01, min(0.99, final_mastery)), 4)

def get_mastery_state(mastery_val: float, evidence_count: int = 0) -> Dict[str, Any]:
    """
    Provisional user-facing states (Blueprint Section 8):
    - Below 0.40: needs support
    - 0.40-0.59: developing
    - 0.60-0.79: progressing
    - 0.80+: likely secure
    Display sparse evidence explicitly (< 2 attempts).
    """
    val = float(mastery_val)
    is_sparse = (evidence_count < 2)

    if val < 0.40:
        state_key = "needs_support"
        label = "Needs Support"
        color = "#EF4444"  # Red
        badge = "🔴 Needs Support"
    elif val < 0.60:
        state_key = "developing"
        label = "Developing"
        color = "#F59E0B"  # Amber
        badge = "🟡 Developing"
    elif val < 0.80:
        state_key = "progressing"
        label = "Progressing"
        color = "#3B82F6"  # Blue
        badge = "🔵 Progressing"
    else:
        state_key = "likely_secure"
        label = "Likely Secure"
        color = "#10B981"  # Emerald
        badge = "🟢 Likely Secure"

    return {
        "state": state_key,
        "label": label,
        "color": color,
        "badge": badge,
        "mastery": val,
        "mastery_pct": int(round(val * 100)),
        "is_sparse": is_sparse,
        "evidence_count": evidence_count,
        "evidence_label": "Sparse evidence" if is_sparse else f"{evidence_count} attempts",
    }

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

        min_prereq_mastery = min([mastery.get(p, DEFAULT_PRIOR) for p in prereqs])
        if min_prereq_mastery < base:
            gap = base - min_prereq_mastery
            penalty = 0.15 * gap
            effective[cid] = max(0.05, round(base - penalty, 4))
        else:
            effective[cid] = base

    return effective

def target_difficulty_for_mastery(mastery_val: float) -> int:
    """
    Target difficulty calibration rule (Blueprint Section 10):
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

def compute_adaptive_priority(
    concept_id: str,
    mastery: float,
    retrievability: float = 1.0,
    has_misconception: bool = False,
    misconception_confidence: float = 0.0,
    exam_relevance: float = 0.07,
    evidence_count: int = 0,
    recent_repetition_count: int = 0,
    w1: float = 0.35,  # weakness
    w2: float = 0.25,  # review urgency
    w3: float = 0.20,  # misconception need
    w4: float = 0.15,  # exam relevance
    w5: float = 0.10,  # information value (sparse evidence boost)
    w6: float = 0.20,  # recent repetition penalty
) -> Tuple[float, Dict[str, Any]]:
    """
    Blueprint Section 10 Priority Heuristic:
    priority = w1*weakness + w2*review_urgency
             + w3*misconception_need + w4*exam_relevance
             + w5*information_value - w6*recent_repetition
    
    Returns:
      (priority_score, breakdown_dict)
    """
    weakness = max(0.0, 1.0 - mastery)
    review_urgency = max(0.0, 1.0 - retrievability)
    misconception_need = float(misconception_confidence) if has_misconception else 0.0
    information_value = 1.0 / (1.0 + max(0, evidence_count))
    recent_repetition = min(1.0, recent_repetition_count * 0.33)

    score = (
        w1 * weakness
        + w2 * review_urgency
        + w3 * misconception_need
        + w4 * exam_relevance
        + w5 * information_value
        - w6 * recent_repetition
    )

    breakdown = {
        "concept_id": concept_id,
        "score": round(score, 4),
        "weakness_term": round(w1 * weakness, 4),
        "review_term": round(w2 * review_urgency, 4),
        "misconception_term": round(w3 * misconception_need, 4),
        "exam_term": round(w4 * exam_relevance, 4),
        "info_term": round(w5 * information_value, 4),
        "repetition_penalty": round(w6 * recent_repetition, 4),
    }
    return score, breakdown

def select_next_practice_concept(
    mastery: Dict[str, float],
    due_concepts: List[str],
    allowed_concepts: Optional[List[str]] = None,
    active_misconceptions: Optional[Dict[str, Any]] = None,
    evidence_counts: Optional[Dict[str, int]] = None,
    recent_history: Optional[List[str]] = None,
) -> Tuple[str, str]:
    """
    Selects the next concept to practice according to the Blueprint Section 10 Priority Heuristic.
    Balances:
    1. Weakness (lower mastery)
    2. Spaced review urgency (retrievability <= 90%)
    3. Active misconception repair need
    4. Exam syllabus weighting
    5. Information value / sparse evidence
    6. Penalty for recent repetitions
    
    Returns:
      (chosen_concept_id, selection_reason_string)
    """
    eff = compute_effective_mastery(mastery)
    
    if allowed_concepts:
        pool = [c for c in allowed_concepts if c in CONCEPTS or c in CONCEPTS_51]
    elif len(mastery) < len(CONCEPTS) and len(mastery) > 0:
        pool = [c for c in mastery.keys() if c in CONCEPTS or c in CONCEPTS_51]
    else:
        pool = list(CONCEPTS.keys())

    if not pool:
        pool = list(CONCEPTS.keys())

    active_due = [c for c in due_concepts if c in pool]
    active_misc = active_misconceptions or {}
    ev_counts = evidence_counts or {}
    history = recent_history or []

    # 1. Spaced review due first
    if active_due:
        c0 = min(active_due, key=lambda c: eff.get(c, DEFAULT_PRIOR))
        cname = CONCEPTS.get(c0, {}).get("name", c0)
        return c0, f"Concept '{cname}' is due for spaced-repetition review (retrievability dropped below 90%)."

    # 2. Score by priority heuristic
    best_cid = pool[0]
    best_score = -999.0
    best_breakdown: Dict[str, Any] = {}

    for cid in pool:
        m_val = eff.get(cid, DEFAULT_PRIOR)
        is_due = (cid in due_concepts)
        retriev = 0.50 if is_due else 0.95
        has_m = (cid in active_misc)
        m_conf = float(active_misc[cid].get("confidence", 0.8)) if has_m else 0.0
        ex_weight = CONCEPTS_51.get(cid, {}).get("exam_weight", 0.07)
        ev_cnt = ev_counts.get(cid, 0)
        rep_cnt = history[-5:].count(cid)

        score, bd = compute_adaptive_priority(
            concept_id=cid,
            mastery=m_val,
            retrievability=retriev,
            has_misconception=has_m,
            misconception_confidence=m_conf,
            exam_relevance=ex_weight,
            evidence_count=ev_cnt,
            recent_repetition_count=rep_cnt,
        )

        if score > best_score:
            best_score = score
            best_cid = cid
            best_breakdown = bd

    # 3. Prerequisite override check
    chosen = best_cid
    cname = CONCEPTS.get(chosen, {}).get("name", chosen)
    m_pct = int(round(mastery.get(chosen, DEFAULT_PRIOR) * 100))
    reason = f"Identified as your lowest mastery area ({m_pct}%). Priority score: {best_breakdown.get('score', 0.0):.2f}."

    prereqs = CONCEPTS.get(chosen, {}).get("prerequisites", [])
    for p in prereqs:
        if p in pool:
            p_mastery = mastery.get(p, DEFAULT_PRIOR)
            c0_mastery = mastery.get(chosen, DEFAULT_PRIOR)
            if p_mastery < (c0_mastery - 0.10):
                chosen = p
                pname = CONCEPTS.get(p, {}).get("name", p)
                reason = (
                    f"Prerequisite '{pname}' ({int(p_mastery * 100)}%) is significantly weaker "
                    f"than '{cname}' ({int(c0_mastery * 100)}%). Reinforcing foundation first."
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
    
    1. Filters question pool to the target concept (or mapped alias).
    2. If an active misconception exists for this concept, prioritises
       questions containing distractors tagged with that misconception.
    3. Matches target difficulty level (Level 1, 2, or 3).
    4. Avoids repeating items in the current session if unasked items exist.
    """
    target_d = target_difficulty_for_mastery(mastery_val)
    
    # Check matching questions by canonical ID or legacy alias
    candidates = [
        q for q in question_pool
        if q.get("concept") == concept or q.get("canonical_concept") == concept or q.get("id", "").startswith(concept)
    ]

    if not candidates:
        # Fallback to entire bank
        candidates = list(question_pool)

    # Prefer unasked questions
    unasked = [q for q in candidates if q["id"] not in asked_question_ids]
    search_pool = unasked if unasked else candidates

    # If an active misconception is flagged, prefer questions targeting it
    if active_misconception:
        misc_pool = [
            q for q in search_pool
            if any(t == active_misconception for t in q.get("tags", []))
        ]
        if misc_pool:
            best = min(misc_pool, key=lambda q: abs(q.get("difficulty_label", 2) - target_d))
            rationale = (
                f"Targeted at misconception '{active_misconception}' "
                f"with difficulty Level {best.get('difficulty_label', 2)} of 3."
            )
            return best, rationale

    # Otherwise pick closest difficulty match
    best = min(search_pool, key=lambda q: abs(q.get("difficulty_label", 2) - target_d))
    rationale = f"Difficulty Level {best.get('difficulty_label', 2)} of 3 calibrated for {int(round(mastery_val * 100))}% mastery."
    return best, rationale
