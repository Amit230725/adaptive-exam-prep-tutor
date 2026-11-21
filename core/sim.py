"""core/sim.py - Seeded, Reproducible Simulated Class for Teacher Dashboard

Creates a synthetic class of 20 students with planted pedagogical gaps
(e.g., Potential Difference and Parallel Circuits weaker, as established in PER literature).

STRICT RULE:
All simulated data is clearly labeled "[SIMULATED]" across the UI and export files.
Real student data is stored and displayed separately by default.
"""

import random
from typing import Dict, List, Any, Tuple
import pandas as pd

from core.concepts import CONCEPTS, MISCONCEPTIONS

# Seeded pseudo-random generator for 100% reproducible demo data
SIM_SEED = 42

# Planted population means representing a typical Class 10 cohort
# (Shows classic learning gaps: 'pd' and 'parallel' are historically difficult)
PLANTED_CONCEPT_MEANS: Dict[str, float] = {
    "charge": 0.78,      # Well-understood foundation
    "current": 0.58,     # Moderate
    "pd": 0.38,          # Planted Gap: abstract potential concept
    "ohm": 0.62,         # Moderate
    "resistance": 0.56,  # Moderate
    "series": 0.60,      # Relatively concrete
    "parallel": 0.36,    # Planted Gap: counter-intuitive equivalent resistance
    "power": 0.54,       # Moderate
}

# Planted population counts for research misconceptions across 20 students
PLANTED_MISCONCEPTION_COUNTS: Dict[str, int] = {
    "M1": 11,  # Current used up (most common)
    "M2": 7,   # Battery is constant current
    "M3": 9,   # Confuses V, I, energy
    "M4": 3,   # Battery creates/stores charge
    "M5": 8,   # Parallel increases total R
    "M6": 4,   # Resistance depends on V or I
    "M7": 6,   # Parallel current splits equally
}

def generate_simulated_class(n_students: int = 20) -> List[Dict[str, Any]]:
    """
    Generates a reproducible cohort of n_students with planted realistic variations.
    Each record represents one student's mastery profile.
    """
    rng = random.Random(SIM_SEED)
    students = []
    
    first_names = [
        "Aarav", "Ananya", "Dev", "Diya", "Ishaan",
        "Kavya", "Manish", "Meera", "Neha", "Pranav",
        "Pooja", "Rahul", "Riya", "Rohan", "Sanya",
        "Siddharth", "Sneha", "Tanvi", "Varun", "Zoya",
    ]

    for i in range(min(n_students, len(first_names))):
        name = f"{first_names[i]} [SIMULATED]"
        stu_id = f"sim_{i+1:02d}"
        
        record: Dict[str, Any] = {
            "Student": name,
            "ID": stu_id,
            "Class": "CLASS-10A [SIMULATED]",
            "Is_Simulated": True,
        }
        
        # Sample mastery around planted means with realistic variance
        for cid, mean_val in PLANTED_CONCEPT_MEANS.items():
            noise = rng.gauss(0.0, 0.14)
            sampled = round(min(0.98, max(0.08, mean_val + noise)), 2)
            record[cid] = sampled

        students.append(record)

    return students

def get_simulated_misconception_stats() -> List[Dict[str, Any]]:
    """
    Returns populated misconception frequencies for the simulated class,
    paired with research corrections and teacher actions.
    """
    stats = []
    for mid, count in PLANTED_MISCONCEPTION_COUNTS.items():
        m_info = MISCONCEPTIONS[mid]
        stats.append({
            "Misconception_ID": mid,
            "Misconception": m_info["label"],
            "Affected_Students": count,
            "Prevalence": f"{int((count / 20) * 100)}%",
            "Teacher_Action": m_info["reteach_action"],
            "Correction": m_info["correction"],
            "Source": "SIMULATED",
        })
    # Sort descending by affected student count
    return sorted(stats, key=lambda x: x["Affected_Students"], reverse=True)
