"""core/concepts.py - Concept Graph & Research-Backed Misconception Library

Curriculum: CBSE Class 10 Science, Chapter 11 "Electricity" (NCERT).
Misconceptions: Published Physics Education Research (PER) on circuits
(McDermott & Shaffer, 1992; Shipstone, 1988; Engelhardt & Beichner, 2004).
"""

from typing import Dict, List, Optional, Any

# -----------------------------------------------------------------------------
# 1. CONCEPT GRAPH DEFINITIONS
# -----------------------------------------------------------------------------
# Each concept has:
# - id: unique key
# - name: human-readable title
# - prerequisites: list of concept IDs that must be understood first
# - order: recommended diagnostic order
# - description: NCERT syllabus scope

CONCEPTS: Dict[str, Dict[str, Any]] = {
    "charge": {
        "id": "charge",
        "name": "Electric Charge",
        "prerequisites": [],
        "order": 1,
        "description": "Quantisation of charge (Q = n*e), SI unit Coulomb (C), electrons as mobile carriers.",
    },
    "current": {
        "id": "current",
        "name": "Electric Current",
        "prerequisites": ["charge"],
        "order": 2,
        "description": "Rate of flow of charge (I = Q/t), SI unit Ampere (A), measured by ammeter in series, conservation of charge.",
    },
    "pd": {
        "id": "pd",
        "name": "Potential Difference",
        "prerequisites": ["charge"],
        "order": 3,
        "description": "Work done per unit charge (V = W/Q), SI unit Volt (V), role of battery in maintaining electrical push, measured by voltmeter in parallel.",
    },
    "ohm": {
        "id": "ohm",
        "name": "Ohm's Law",
        "prerequisites": ["current", "pd"],
        "order": 4,
        "description": "Linear relationship V = I*R at constant temperature; V-I characteristic curve and slope.",
    },
    "resistance": {
        "id": "resistance",
        "name": "Resistance & Factors",
        "prerequisites": ["ohm"],
        "order": 5,
        "description": "Opposition to flow; dependence on length, cross-sectional area, resistivity (R = rho*l/A); distinction between R and V/I.",
    },
    "series": {
        "id": "series",
        "name": "Series Circuits",
        "prerequisites": ["resistance"],
        "order": 6,
        "description": "Single conductive path: identical current throughout (I_tot = I1 = I2), voltage divides (V_tot = V1 + V2), equivalent resistance R_s = R1 + R2.",
    },
    "parallel": {
        "id": "parallel",
        "name": "Parallel Circuits",
        "prerequisites": ["resistance"],
        "order": 7,
        "description": "Multiple branches: identical voltage across branches (V_tot = V1 = V2), current divides inversely by resistance, 1/R_p = 1/R1 + 1/R2.",
    },
    "power": {
        "id": "power",
        "name": "Electric Power & Energy",
        "prerequisites": ["ohm"],
        "order": 8,
        "description": "Rate of electrical energy dissipation (P = V*I = I^2*R = V^2/R), Watt (W), practical heating and bulb brightness.",
    },
}

# -----------------------------------------------------------------------------
# 2. MISCONCEPTION LIBRARY (FIXED RESEARCH-BASED IDs: M1 - M7)
# -----------------------------------------------------------------------------
# AI and rule engines MUST ONLY reference these exact IDs. Never invent labels.

MISCONCEPTIONS: Dict[str, Dict[str, str]] = {
    "M1": {
        "id": "M1",
        "label": "Current is used up as it passes through a component",
        "description": "The student believes electrical current decreases downstream after passing through bulbs or resistors.",
        "correction": "Electric charge is conserved. Current is the rate of charge flow and remains identical before and after any component in a single path.",
        "challenge_idea": "Two ammeters placed on either side of a single high-resistance bulb.",
        "reteach_action": "Use PhET circuit simulation with ammeters before and after a bulb to visually prove identical flow rates.",
    },
    "M2": {
        "id": "M2",
        "label": "Battery is a constant-current source",
        "description": "The student assumes a battery pushes the exact same amperes regardless of what circuit is connected.",
        "correction": "A battery maintains a constant potential difference across its terminals; the current it delivers depends strictly on total circuit resistance (I = V/R).",
        "challenge_idea": "Compare total current from the same 6 V battery when connected to 10 ohms vs 100 ohms.",
        "reteach_action": "Demonstrate with real multimeter: measure current when adding resistors in series vs parallel to the same battery.",
    },
    "M3": {
        "id": "M3",
        "label": "Confuses current, voltage, and/or electrical energy",
        "description": "The student mixes up the roles of voltage (push/energy per charge), current (rate of flow), and power/energy (Joules/Watts).",
        "correction": "Voltage is the electrical pressure (Joules per Coulomb), current is the traffic flow rate (Coulombs per second), and energy is the total work done.",
        "challenge_idea": "A circuit with high voltage but zero current (open switch) vs high current at low voltage.",
        "reteach_action": "Use water-pipe analogy: pump pressure = voltage, pipe water flow rate = current, water turbine work = energy transferred.",
    },
    "M4": {
        "id": "M4",
        "label": "Battery creates or stores charge that gets exhausted",
        "description": "The student believes the battery physically contains mobile charges that run out, or that the battery generates electrons.",
        "correction": "The mobile electrons already exist throughout the metal wires and components. The battery only supplies the chemical energy to circulate them.",
        "challenge_idea": "Explain why a circuit doesn't fill up with electrons at one end while emptying at the other.",
        "reteach_action": "Bicycle-chain model: the chain links (electrons) are already there; the pedals (battery) only push the loop.",
    },
    "M5": {
        "id": "M5",
        "label": "Adding resistors in parallel increases total resistance",
        "description": "The student applies series intuition (more components = more resistance) to parallel branches.",
        "correction": "Adding parallel branches creates additional paths for current to flow, increasing total conductance and decreasing equivalent resistance.",
        "challenge_idea": "Calculate equivalent resistance of two 6 ohm resistors in parallel vs one alone.",
        "reteach_action": "Toll-booth analogy: opening more parallel toll gates speeds up traffic flow, lowering the overall obstruction.",
    },
    "M6": {
        "id": "M6",
        "label": "Resistance depends on applied voltage or current",
        "description": "The student misinterprets R = V/I as a causal relationship, believing altering V changes the material resistance.",
        "correction": "Resistance of an ohmic conductor is an intrinsic property determined by resistivity, length, and area (R = rho*l/A); it does not change when V or I changes.",
        "challenge_idea": "What is the resistance of a 10 ohm resistor when disconnected from any circuit (V = 0)?",
        "reteach_action": "Plot V vs I experimentally for a resistor. Show that the slope R remains constant across different voltages.",
    },
    "M7": {
        "id": "M7",
        "label": "In parallel, current splits equally regardless of resistance",
        "description": "The student assumes parallel branches always divide total current equally (50/50), ignoring differing branch resistances.",
        "correction": "Current in parallel branches divides inversely proportional to branch resistance (I_branch = V / R_branch); the path of lower resistance carries more current.",
        "challenge_idea": "Calculate branch currents for 2 ohms and 10 ohms in parallel connected to a 10 V battery.",
        "reteach_action": "Dual-pipe drainage demo: a wider pipe drains significantly more water per second than a narrow pipe under equal head pressure.",
    },
}

def get_concept(cid: str) -> Optional[Dict[str, Any]]:
    """Retrieve concept metadata by ID."""
    return CONCEPTS.get(cid)

def get_misconception(mid: str) -> Optional[Dict[str, str]]:
    """Retrieve misconception metadata by ID."""
    return MISCONCEPTIONS.get(mid)

def get_ordered_concepts() -> List[str]:
    """Return concepts sorted in pedagogical order."""
    return sorted(CONCEPTS.keys(), key=lambda c: CONCEPTS[c]["order"])
