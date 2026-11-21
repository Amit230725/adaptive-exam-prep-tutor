"""scripts/eval_synthetic.py - Synthetic-Student Evaluation Benchmark

Evaluates ConceptPilot's diagnostic pipeline against 7 synthetic students,
each holding a single planted misconception (M1 through M7).
Simulates answers and reasoning text using a scripted policy.

STRICT RULE (Section 12):
Presented as a 'simulated check', never as empirical accuracy on real students.
"""

import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Dict, List, Any
from core.concepts import MISCONCEPTIONS
from core.bank import QUESTION_BANK
from core.ai import diagnose_reasoning

# Scripted policy: 7 synthetic students holding planted misconceptions M1 - M7
SYNTHETIC_COHORT = [
    {
        "student": "Synthetic_M1_Tester",
        "planted_misconception": "M1",
        "concept": "current",
        "question_id": "q_cur_01",
        "chosen_index": 1,  # Distractor tagged M1: "0.75 A, because the bulb uses up half the current"
        "scripted_reasoning": "The bulb consumes half the current to produce light energy, so less current comes out.",
    },
    {
        "student": "Synthetic_M2_Tester",
        "planted_misconception": "M2",
        "concept": "ohm",
        "question_id": "q_ohm_02",
        "chosen_index": 1,  # Distractor tagged M2: "2.5 A (battery maintains constant current)"
        "scripted_reasoning": "The battery always pumps out a constant current of 2.5 A regardless of voltage changes.",
    },
    {
        "student": "Synthetic_M3_Tester",
        "planted_misconception": "M3",
        "concept": "power",
        "question_id": "q_pow_01",
        "chosen_index": 1,  # Distractor tagged M3
        "scripted_reasoning": "I divided voltage by current because voltage pushes current, confusing power with resistance.",
    },
    {
        "student": "Synthetic_M4_Tester",
        "planted_misconception": "M4",
        "concept": "pd",
        "question_id": "q_pd_01",
        "chosen_index": 2,  # Distractor tagged M4: "To manufacture new electrons that get burned up"
        "scripted_reasoning": "The battery creates new electrons and stores electric charge that gradually runs out.",
    },
    {
        "student": "Synthetic_M5_Tester",
        "planted_misconception": "M5",
        "concept": "parallel",
        "question_id": "q_par_01",
        "chosen_index": 1,  # Distractor tagged M5: "18 Ω; parallel connections add up total resistance"
        "scripted_reasoning": "Adding resistors in parallel increases resistance because adding components adds opposition: 6 + 12 = 18.",
    },
    {
        "student": "Synthetic_M6_Tester",
        "planted_misconception": "M6",
        "concept": "resistance",
        "question_id": "q_res_03",
        "chosen_index": 1,  # Distractor tagged M6: "8 Ω (doubling voltage doubles resistance)"
        "scripted_reasoning": "Because Ohm's law says R = V/I, increasing applied voltage directly causes resistance to increase.",
    },
    {
        "student": "Synthetic_M7_Tester",
        "planted_misconception": "M7",
        "concept": "parallel",
        "question_id": "q_par_02",
        "chosen_index": 1,  # Distractor tagged M7: "current splits equally between branches"
        "scripted_reasoning": "In parallel circuits current always splits equally 50/50 between branches no matter the resistance.",
    },
]

def run_synthetic_benchmark(api_key: str = None) -> Dict[str, Any]:
    """Runs all 7 synthetic student simulations and computes detection rate."""
    bank_map = {q["id"]: q for q in QUESTION_BANK}
    results = []
    recovered_count = 0

    print("=" * 72)
    print("CONCEPT PILOT - SYNTHETIC STUDENT EVALUATION BENCHMARK")
    print("Simulated Check: 7 Scripted Student Policies with Planted Misconceptions M1 - M7")
    print("=" * 72)

    for case in SYNTHETIC_COHORT:
        planted = case["planted_misconception"]
        q = bank_map.get(case["question_id"])
        if not q:
            continue

        diagnosis = diagnose_reasoning(
            q=q,
            chosen_idx=case["chosen_index"],
            reasoning=case["scripted_reasoning"],
            api_key_override=api_key,
        )

        detected = diagnosis.get("misconception")
        is_recovered = (detected == planted)
        if is_recovered:
            recovered_count += 1

        results.append({
            "student": case["student"],
            "planted": planted,
            "detected": detected,
            "recovered": is_recovered,
            "confidence": diagnosis.get("confidence", 0.0),
            "evidence": diagnosis.get("evidence", ""),
            "engine": "AI" if diagnosis.get("is_ai") else "Offline",
        })

        status_symbol = "✓ PASS" if is_recovered else "✗ FAIL"
        print(f"[{status_symbol}] {case['student']}: Planted={planted} -> Detected={detected} (Conf: {int(diagnosis.get('confidence',0)*100)}%)")
        print(f"       Evidence: \"{diagnosis.get('evidence', '')[:65]}...\"")

    recovery_rate = recovered_count / len(SYNTHETIC_COHORT)
    print("=" * 72)
    print(f"BENCHMARK RESULT: {recovered_count} of {len(SYNTHETIC_COHORT)} recovered ({int(recovery_rate * 100)}% detection rate)")
    print("NOTE: This is a synthetic validation check, not empirical human trial accuracy.")
    print("=" * 72)

    return {
        "total": len(SYNTHETIC_COHORT),
        "recovered": recovered_count,
        "recovery_rate": recovery_rate,
        "details": results,
    }

if __name__ == "__main__":
    key = os.environ.get("GEMINI_API_KEY")
    run_synthetic_benchmark(api_key=key)
