"""core/bank.py - Verified CBSE Class 10 Science Question Bank (24 Items)

All questions align strictly with NCERT Class 10 Science (Electricity)
and Physics Education Research (PER) diagnostics.
Each concept contains exactly 3 calibrated questions:
  - Level 1: Foundational knowledge / definition / direct application
  - Level 2: Numerical reasoning / multi-step circuit analysis
  - Level 3: Conceptual synthesis / counter-intuitive non-obvious circuits

Each distractor is explicitly mapped to the misconception it triggers (M1 - M7) or None.
Solutions and derivations are provided in the comments and explanation strings.
"""

from typing import List, Dict, Any, Optional

def Item(
    item_id: str,
    concept: str,
    difficulty_label: int,
    question: str,
    options: List[str],
    answer_index: int,
    tags: List[Optional[str]],
    explanation: str,
    source_note: str,
) -> Dict[str, Any]:
    """Helper constructor for a question bank entry."""
    assert len(options) == 4, f"Question {item_id} must have exactly 4 options"
    assert len(tags) == 4, f"Question {item_id} must have exactly 4 distractor tags"
    assert 0 <= answer_index < 4, f"Question {item_id} answer_index out of bounds"
    assert tags[answer_index] is None, f"Correct option for {item_id} cannot have a misconception tag"
    return {
        "id": item_id,
        "concept": concept,
        "difficulty_label": difficulty_label,
        "question": question,
        "options": options,
        "answer_index": answer_index,
        "tags": tags,
        "explanation": explanation,
        "source_note": source_note,
        "is_ai": False,
    }

QUESTION_BANK: List[Dict[str, Any]] = [
    # =========================================================================
    # CONCEPT 1: CHARGE (Electric Charge)
    # =========================================================================
    # --- Item 1 (Level 1 - Easy) ---
    # Solution: 1 electron has charge e = 1.602e-19 C. 1 C = 1 / (1.602e-19) = 6.24e18 electrons.
    Item(
        item_id="q_chg_01",
        concept="charge",
        difficulty_label=1,
        question="What is the SI unit of electric charge, and approximately how many electronic charges constitute one unit of this charge?",
        options=[
            "Coulomb; approximately 6.25 × 10^18 electrons",
            "Ampere; approximately 1 × 10^6 electrons stored in a cell",
            "Volt; approximately 6.25 × 10^18 electrons consumed per second",
            "Ohm; a fixed store of charge that opposes current",
        ],
        answer_index=0,
        tags=[None, "M3", "M3", "M3"],
        explanation="The SI unit of electric charge is the Coulomb (C). Since the elementary charge on one electron is e = 1.6 × 10^-19 C, the number of electrons in 1 C is n = Q/e = 1 / (1.6 × 10^-19) ≈ 6.25 × 10^18 electrons.",
        source_note="NCERT Class 10 Science, Chapter 11, Section 11.1; Quantisation of charge Q = n*e.",
    ),

    # --- Item 2 (Level 2 - Medium) ---
    # Solution: I = 0.5 A, t = 10 min = 600 s. Q = I * t = 0.5 A * 600 s = 300 C.
    Item(
        item_id="q_chg_02",
        concept="charge",
        difficulty_label=2,
        question="A current of 0.5 A is drawn by a filament of an electric bulb for 10 minutes. Find the amount of electric charge that flows through the circuit.",
        options=[
            "300 C",
            "5 C (0.5 A × 10 without time conversion)",
            "120 C (time divided by current)",
            "0 C (all charge created by the cell is consumed by the filament)",
        ],
        answer_index=0,
        tags=[None, None, None, "M1"],
        explanation="Electric current is the rate of charge flow: I = Q / t. Time must be converted to SI units: t = 10 min = 10 × 60 s = 600 s. Therefore, Q = I × t = 0.5 A × 600 s = 300 C.",
        source_note="NCERT Class 10 Science, Example 11.1.",
    ),

    # --- Item 3 (Level 3 - Hard) ---
    # Solution: n = 3.75e19, t = 10 s. Q = n*e = 3.75e19 * 1.6e-19 C = 6.0 C. I = Q/t = 6.0/10 = 0.60 A.
    Item(
        item_id="q_chg_03",
        concept="charge",
        difficulty_label=3,
        question="If 3.75 × 10^19 electrons pass through a given cross-section of a wire in 10 seconds, what is the electric current flowing through that cross-section?",
        options=[
            "0.60 A",
            "6.0 A (omitting the 10-second duration)",
            "0.30 A (assuming half the electrons are consumed by wire resistance)",
            "3.75 A (dividing electron count by time directly without electron charge)",
        ],
        answer_index=0,
        tags=[None, "M3", "M1", "M3"],
        explanation="Total charge Q = n × e = (3.75 × 10^19) × (1.6 × 10^-19 C) = 6.0 C. The current is I = Q / t = 6.0 C / 10 s = 0.60 A. Mobile electrons are not consumed in transit.",
        source_note="PER Diagnostic; McDermott & Shaffer (1992); NCERT Section 11.1.",
    ),

    # =========================================================================
    # CONCEPT 2: CURRENT (Electric Current)
    # =========================================================================
    # --- Item 4 (Level 1 - Easy) ---
    # Solution: Conservation of charge: current in series is identical everywhere.
    Item(
        item_id="q_cur_01",
        concept="current",
        difficulty_label=1,
        question="In a circuit with an illuminated bulb, ammeter A1 is connected immediately before the bulb and reads 1.5 A. Ammeter A2 is connected immediately after the bulb. What does ammeter A2 read?",
        options=[
            "1.5 A, because electric charge is conserved and current is not consumed",
            "0.75 A, because the bulb uses up half the current to produce light",
            "0 A, because all electric current is converted into light and heat",
            "3.0 A, because the battery pumps extra current after the restriction",
        ],
        answer_index=0,
        tags=[None, "M1", "M1", "M2"],
        explanation="Current represents the rate of charge flow past a point. By the principle of conservation of electric charge, charges cannot accumulate or vanish inside a filament. The number of Coulombs per second entering the bulb equals the number leaving it.",
        source_note="Classic PER Circuit Diagnostic (Shipstone 1988); NCERT Section 11.1.",
    ),

    # --- Item 5 (Level 2 - Medium) ---
    # Solution: Ammeter is connected in series; low resistance avoids altering circuit current.
    Item(
        item_id="q_cur_02",
        concept="current",
        difficulty_label=2,
        question="A student wishes to measure the electric current flowing through a 10 Ω resistor in a circuit. How must the ammeter be connected, and what electrical property must it possess?",
        options=[
            "In series with the resistor, with a very low internal resistance",
            "In parallel with the resistor, so it captures the battery's fixed output current",
            "In series with the resistor, with a very high resistance to store charge",
            "Directly across the battery terminals, because battery current is constant regardless of circuit",
        ],
        answer_index=0,
        tags=[None, "M2", "M4", "M2"],
        explanation="An ammeter measures the rate of charge flow through a branch, so all current must pass through it (connected in series). It must have very low resistance so that its insertion does not appreciably decrease the total current of the circuit.",
        source_note="NCERT Class 10 Science, Section 11.1; Ammeter usage guidelines.",
    ),

    # --- Item 6 (Level 3 - Hard) ---
    # Solution: Identical bulbs in series carry identical current and have identical resistance -> equal brightness.
    Item(
        item_id="q_cur_03",
        concept="current",
        difficulty_label=3,
        question="Two identical lamps L1 and L2 are connected in series with a 9 V cell. Which statement correctly compares the current through each lamp and their observed brightness?",
        options=[
            "Current through L1 equals current through L2, and both lamps glow with equal brightness",
            "L1 has more current and glows brighter because it receives fresh current from the cell first",
            "L2 has more current because charge accelerates as it returns to the negative terminal",
            "L1 and L2 carry the same current, but L1 glows brighter because current loses energy inside L1",
        ],
        answer_index=0,
        tags=[None, "M1", "M3", "M3"],
        explanation="In a series circuit, there is only one continuous conducting loop. The current I is identical at all points (I_L1 = I_L2). Since the lamps are identical, their resistances are equal, so power dissipated P = I^2 * R is identical for both. L1 and L2 glow with equal brightness.",
        source_note="McDermott & Shaffer (1992); Research in Physics Education on Series Circuits.",
    ),

    # =========================================================================
    # CONCEPT 3: PD (Potential Difference)
    # =========================================================================
    # --- Item 7 (Level 1 - Easy) ---
    # Solution: Battery maintains potential difference; mobile charges exist in wires.
    Item(
        item_id="q_pd_01",
        concept="pd",
        difficulty_label=1,
        question="What is the primary physical function of a chemical cell or battery when connected in an electric circuit?",
        options=[
            "To maintain an electric potential difference that exerts a force on mobile electrons already in the conductor",
            "To provide a constant current of fixed amperes no matter what resistance is attached",
            "To manufacture and supply new electrons that are gradually burned up by components",
            "To store electric current and release it as energy until the current is exhausted",
        ],
        answer_index=0,
        tags=[None, "M2", "M4", "M3"],
        explanation="A battery does not create charge or pump a fixed current. Chemical reactions inside the cell maintain a potential difference between its terminals. This voltage creates an electric field throughout the wires that pushes the free electrons already present in the metal.",
        source_note="NCERT Class 10 Science, Section 11.2 'Electric Potential and Potential Difference'.",
    ),

    # --- Item 8 (Level 2 - Medium) ---
    # Solution: W = V * Q = 12 V * 4 C = 48 J.
    Item(
        item_id="q_pd_02",
        concept="pd",
        difficulty_label=2,
        question="How much work is done in moving an electric charge of 4 C across two points having a potential difference of 12 V?",
        options=[
            "48 J",
            "3 J (dividing 12 V by 4 C)",
            "16 J (adding 12 V and 4 C)",
            "0 J (because a battery only supplies current without doing mechanical work)",
        ],
        answer_index=0,
        tags=[None, "M3", None, "M3"],
        explanation="Potential difference V is defined as work done W per unit charge Q (V = W / Q). Rearranging gives W = V × Q = 12 V × 4 C = 48 Joules.",
        source_note="NCERT Class 10 Science, Example 11.2.",
    ),

    # --- Item 9 (Level 3 - Hard) ---
    # Solution: Voltmeter connected in parallel; high resistance prevents drawing branch current.
    Item(
        item_id="q_pd_03",
        concept="pd",
        difficulty_label=3,
        question="A student connects a voltmeter across a 15 Ω resistor. Why must an ideal voltmeter possess a very high resistance, and what does it measure?",
        options=[
            "High resistance ensures negligible current is diverted through it; it measures electrical potential energy change per unit charge",
            "High resistance absorbs all circuit current so it can measure the rate of charge consumption",
            "High resistance keeps the battery current perfectly constant across changing loads",
            "High resistance is required because voltage is the speed at which electrons travel",
        ],
        answer_index=0,
        tags=[None, "M1", "M2", "M3"],
        explanation="A voltmeter is connected in parallel across the two points whose potential difference is being measured. If it had low resistance, it would short-circuit the component by drawing large current. A very high resistance ensures negligible current flows through the voltmeter, keeping circuit conditions undisturbed.",
        source_note="NCERT Class 10 Science, Section 11.2; Laboratory apparatus design.",
    ),

    # =========================================================================
    # CONCEPT 4: OHM (Ohm's Law)
    # =========================================================================
    # --- Item 10 (Level 1 - Easy) ---
    # Solution: V proportional to I at constant temperature (V = I*R).
    Item(
        item_id="q_ohm_01",
        concept="ohm",
        difficulty_label=1,
        question="According to Ohm's law, if the temperature and physical state of a metallic conductor remain constant, what is the exact relationship between potential difference (V) and current (I)?",
        options=[
            "The potential difference V across ends is directly proportional to the current I passing through it (V ∝ I)",
            "The current I stays constant regardless of V because the power source fixes the current",
            "The potential difference V is inversely proportional to current because higher voltage uses up more current",
            "The resistance R increases linearly as the applied potential difference V increases",
        ],
        answer_index=0,
        tags=[None, "M2", "M1", "M6"],
        explanation="Ohm's law states that the electric current flowing through a metallic conductor is directly proportional to the potential difference applied across its ends, provided its temperature remains constant: V ∝ I, or V = I × R, where R is the constant resistance.",
        source_note="NCERT Class 10 Science, Section 11.3 'Ohm's Law'.",
    ),

    # --- Item 11 (Level 2 - Medium) ---
    # Solution: R = 10 V / 2.5 A = 4 Ω. V_new = 20 V => I_new = 20 / 4 = 5.0 A.
    Item(
        item_id="q_ohm_02",
        concept="ohm",
        difficulty_label=2,
        question="A potential difference of 10 V across a resistor produces a current of 2.5 A. If the potential difference is increased to 20 V at constant temperature, what will the new current be?",
        options=[
            "5.0 A (current doubles because resistance remains 4 Ω)",
            "2.5 A (the battery maintains a constant current regardless of applied voltage)",
            "1.25 A (doubling the voltage uses up twice as much current inside the resistor)",
            "10.0 A (the current quadruples because voltage and resistance both double)",
        ],
        answer_index=0,
        tags=[None, "M2", "M1", "M6"],
        explanation="From Ohm's law, resistance R = V / I = 10 V / 2.5 A = 4 Ω. Since the temperature remains constant, R remains 4 Ω. When V is increased to 20 V, the new current is I_new = V_new / R = 20 V / 4 Ω = 5.0 A.",
        source_note="NCERT Class 10 Science, Section 11.3.",
    ),

    # --- Item 12 (Level 3 - Hard) ---
    # Solution: V-I graph slope represents R. For an ohmic conductor, R is constant independent of V.
    Item(
        item_id="q_ohm_03",
        concept="ohm",
        difficulty_label=3,
        question="A student plots a graph of Potential Difference (V, vertical axis) against Current (I, horizontal axis) for a metallic wire. What does the slope of this graph represent, and how does the slope change if the applied voltage is doubled?",
        options=[
            "The slope represents Resistance (R); the slope remains unchanged because R is an intrinsic property independent of V",
            "The slope represents Resistance (R); the slope doubles because higher voltage produces higher resistance",
            "The slope represents Electric Power; the slope doubles with voltage",
            "The slope represents Stored Charge; it gradually decreases to zero as battery charge runs out",
        ],
        answer_index=0,
        tags=[None, "M6", "M3", "M4"],
        explanation="On a V vs I plot, slope = ΔV / ΔI = R (resistance). For an ohmic conductor at constant temperature, the slope is a straight line through the origin. Resistance R depends on material, length, and cross-section, not on the applied voltage. Hence the slope remains constant.",
        source_note="NCERT Class 10 Science, Activity 11.1; V-I Characteristic of Ohmic Resistors.",
    ),

    # =========================================================================
    # CONCEPT 5: RESISTANCE (Resistance & Factors)
    # =========================================================================
    # --- Item 13 (Level 1 - Easy) ---
    # Solution: R = rho * l / A. Length doubled -> R' = 2R.
    Item(
        item_id="q_res_01",
        concept="resistance",
        difficulty_label=1,
        question="A uniform cylindrical metallic wire has resistance R. If its length is doubled while its cross-sectional area and material remain unchanged, what is its new resistance?",
        options=[
            "2R (resistance is directly proportional to conductor length: R = ρl/A)",
            "R/2 (longer wire allows charges to move faster through the circuit)",
            "R (resistance depends only on the battery connected to the circuit)",
            "4R (resistance is proportional to the square of conductor length)",
        ],
        answer_index=0,
        tags=[None, None, "M2", None],
        explanation="Resistance of a uniform conductor is directly proportional to its length (l) and inversely proportional to its area of cross-section (A): R = ρ × (l / A). If length becomes 2l with A constant, R' = ρ × (2l / A) = 2R.",
        source_note="NCERT Class 10 Science, Section 11.4 'Factors on which the Resistance of a Conductor Depends'.",
    ),

    # --- Item 14 (Level 2 - Medium) ---
    # Solution: Volume V = l*A = const. If l' = 2l, A' = A/2. R' = rho*(2l)/(A/2) = 4*R = 4*16 = 64 Ω.
    Item(
        item_id="q_res_02",
        concept="resistance",
        difficulty_label=2,
        question="A wire of resistance 16 Ω is stretched uniformly so that its length becomes twice its original length. Assuming its density and mass remain constant, what is the new resistance of the stretched wire?",
        options=[
            "64 Ω (volume is conserved: doubling length halves cross-sectional area, so resistance quadruples)",
            "32 Ω (doubling length simply doubles resistance without considering cross-sectional thinning)",
            "16 Ω (resistance is a material constant that cannot be altered by mechanical stretching)",
            "8 Ω (stretching opens wider parallel paths for electron flow)",
        ],
        answer_index=0,
        tags=[None, None, None, "M5"],
        explanation="When a wire is stretched, its volume V = l × A remains constant. If length doubles (l' = 2l), the cross-sectional area must halve (A' = A / 2). New resistance R' = ρ × (l' / A') = ρ × (2l / (A / 2)) = 4 × [ρ × (l / A)] = 4 × R = 4 × 16 Ω = 64 Ω.",
        source_note="NCERT Class 10 Science, Example 11.6 style problem (Volume conservation).",
    ),

    # --- Item 15 (Level 3 - Hard) ---
    # Solution: R = 4 Ω. Swapping voltage to 24 V does not change R; it only changes current (I = 6 A).
    Item(
        item_id="q_res_03",
        concept="resistance",
        difficulty_label=3,
        question="A 12 V source is connected across a nichrome resistor, producing a current of 3 A. If the source is replaced with a 24 V battery (at constant temperature), what is the new resistance of the nichrome wire?",
        options=[
            "4 Ω (resistance is determined by resistivity, length, and cross-section, not by applied voltage)",
            "8 Ω (because R = V/I, doubling the voltage doubles the resistance)",
            "2 Ω (higher voltage pushes current more easily, halving the opposition to flow)",
            "Infinite Ω (because the battery's fixed current capacity is exceeded by the resistor)",
        ],
        answer_index=0,
        tags=[None, "M6", "M6", "M2"],
        explanation="Initial resistance R = V / I = 12 V / 3 A = 4 Ω. Resistance is an intrinsic structural property of the wire determined by its material resistivity, length, and cross-sectional area (R = ρl/A). Changing the applied voltage to 24 V increases the current to 6 A, but the resistance itself remains 4 Ω.",
        source_note="PER Misconception Diagnostic M6; McDermott (1992); NCERT Section 11.4.",
    ),

    # =========================================================================
    # CONCEPT 6: SERIES (Series Circuits)
    # =========================================================================
    # --- Item 16 (Level 1 - Easy) ---
    # Solution: R_eq = 2 + 3 + 5 = 10 Ω. I = 10 V / 10 Ω = 1.0 A.
    Item(
        item_id="q_ser_01",
        concept="series",
        difficulty_label=1,
        question="Three resistors of 2 Ω, 3 Ω, and 5 Ω are connected in series to a 10 V battery. What is the equivalent resistance of the combination and the current supplied by the battery?",
        options=[
            "Equivalent resistance = 10 Ω; Current = 1.0 A",
            "Equivalent resistance = 0.97 Ω; Current = 10.3 A",
            "Equivalent resistance = 10 Ω; Current = 3.0 A because a 10 V battery provides a fixed 3 A",
            "Equivalent resistance = 5 Ω; Current = 0.5 A because the first resistor consumes half the current",
        ],
        answer_index=0,
        tags=[None, "M5", "M2", "M1"],
        explanation="In a series combination, total resistance is the algebraic sum of individual resistances: R_s = R1 + R2 + R3 = 2 + 3 + 5 = 10 Ω. By Ohm's law, total current from the battery is I = V / R_s = 10 V / 10 Ω = 1.0 A.",
        source_note="NCERT Class 10 Science, Section 11.6.1 'Resistors in Series'.",
    ),

    # --- Item 17 (Level 2 - Medium) ---
    # Solution: R_tot = 10 + 20 = 30 Ω. I = 12 / 30 = 0.4 A. V1 = 0.4*10 = 4 V. V2 = 0.4*20 = 8 V.
    Item(
        item_id="q_ser_02",
        concept="series",
        difficulty_label=2,
        question="Two resistors R1 = 10 Ω and R2 = 20 Ω are connected in series with a 12 V battery. A student measures the voltage drop across each resistor. What are V1 and V2?",
        options=[
            "V1 = 4 V and V2 = 8 V (current I = 0.4 A; V1 = 0.4×10 = 4 V, V2 = 0.4×20 = 8 V)",
            "V1 = 12 V and V2 = 12 V (both resistors receive full battery voltage in series)",
            "V1 = 8 V and V2 = 4 V (the first resistor gets more voltage because current reaches it first and is used up)",
            "V1 = 6 V and V2 = 6 V (voltage always splits equally regardless of individual resistance values)",
        ],
        answer_index=0,
        tags=[None, "M3", "M1", "M7"],
        explanation="In series, current is constant throughout: I = V / (R1 + R2) = 12 V / (10 + 20) Ω = 0.4 A. Voltage across R1 is V1 = I × R1 = 0.4 A × 10 Ω = 4 V. Voltage across R2 is V2 = I × R2 = 0.4 A × 20 Ω = 8 V. Note that V1 + V2 = 4 + 8 = 12 V.",
        source_note="NCERT Class 10 Science, Section 11.6.1.",
    ),

    # --- Item 18 (Level 3 - Hard) ---
    # Solution: Series circuit has a single path. If one bulb burns out, path is broken -> all bulbs go out.
    Item(
        item_id="q_ser_03",
        concept="series",
        difficulty_label=3,
        question="Three identical lamps are connected in series with an 18 V DC supply. What happens to the circuit if the filament of the middle lamp burns out (creating an open circuit)?",
        options=[
            "All three lamps go out immediately because series circuits have a single continuous conducting path",
            "The first lamp stays lit and glows brighter because current no longer has to travel to subsequent lamps",
            "The third lamp stays lit because the battery continues pushing its constant current into the return wire",
            "The other two lamps receive 9 V each because the electric charge jumps across the gap",
        ],
        answer_index=0,
        tags=[None, "M1", "M2", "M3"],
        explanation="In a series circuit, all components lie on a single continuous loop. If any component burns out or is removed, the circuit is broken at that point. Current stops flowing everywhere in the loop, so all lamps extinguish immediately.",
        source_note="Classic PER Series Circuit Diagnostic (Engelhardt & Beichner 2004); NCERT Section 11.6.1.",
    ),

    # =========================================================================
    # CONCEPT 7: PARALLEL (Parallel Circuits)
    # =========================================================================
    # --- Item 19 (Level 1 - Easy) ---
    # Solution: 1/R_p = 1/6 + 1/12 = 3/12 = 1/4 => R_p = 4 Ω.
    Item(
        item_id="q_par_01",
        concept="parallel",
        difficulty_label=1,
        question="Two resistors of 6 Ω and 12 Ω are connected in parallel across a 12 V battery. What is the equivalent resistance of the parallel combination?",
        options=[
            "4 Ω (1/Rp = 1/6 + 1/12 = 3/12 = 1/4 Ω^-1)",
            "18 Ω (Rp = 6 + 12 = 18 Ω; parallel connections add up total resistance)",
            "9 Ω (the simple arithmetic mean of the two resistors)",
            "6 Ω (equivalent resistance equals the lower resistor because the higher resistor is blocked)",
        ],
        answer_index=0,
        tags=[None, "M5", "M5", None],
        explanation="For resistors in parallel: 1 / R_p = 1 / R1 + 1 / R2 = 1/6 + 1/12 = (2 + 1) / 12 = 3 / 12 = 1 / 4. Inverting gives R_p = 4 Ω. The equivalent resistance of a parallel combination is always smaller than the smallest individual resistance.",
        source_note="NCERT Class 10 Science, Section 11.6.2 'Resistors in Parallel'.",
    ),

    # --- Item 20 (Level 2 - Medium) ---
    # Solution: V = 12 V. I1 = 12/4 = 3 A. I2 = 12/12 = 1 A. I_tot = 3 + 1 = 4 A.
    Item(
        item_id="q_par_02",
        concept="parallel",
        difficulty_label=2,
        question="A 12 V battery is connected across two parallel branches containing 4 Ω and 12 Ω resistors respectively. What is the current through each branch and the total current drawn from the battery?",
        options=[
            "Branch 1: 3 A; Branch 2: 1 A; Total current = 4 A",
            "Branch 1: 2 A; Branch 2: 2 A; Total current = 4 A (current splits equally between branches regardless of resistance)",
            "Branch 1: 1 A; Branch 2: 3 A; Total current = 4 A (higher resistance draws more current from the cell)",
            "Branch 1: 3 A; Branch 2: 1 A; Total current = 2 A (current is consumed in branch 1 before reaching branch 2)",
        ],
        answer_index=0,
        tags=[None, "M7", "M3", "M1"],
        explanation="In parallel, full battery voltage (12 V) appears across every branch. Current through 4 Ω: I1 = V / R1 = 12 V / 4 Ω = 3 A. Current through 12 Ω: I2 = V / R2 = 12 V / 12 Ω = 1 A. Total current from battery: I_tot = I1 + I2 = 3 A + 1 A = 4 A. Current divides inversely with branch resistance.",
        source_note="NCERT Class 10 Science, Section 11.6.2.",
    ),

    # --- Item 21 (Level 3 - Hard) ---
    # Solution: 2 bulbs in parallel: R = 50 Ω, I = 220/50 = 4.4 A. 3 bulbs: R = 33.3 Ω, I = 220/33.3 = 6.6 A.
    Item(
        item_id="q_par_03",
        concept="parallel",
        difficulty_label=3,
        question="Two identical 100 Ω lamps are connected in parallel to a 220 V supply. If a third identical 100 Ω lamp is switched ON in parallel with them, what happens to the total equivalent resistance and the total mains current?",
        options=[
            "Total resistance drops from 50 Ω to 33.3 Ω, and total current drawn increases from 4.4 A to 6.6 A",
            "Total resistance rises from 200 Ω to 300 Ω because adding appliances adds resistance to the circuit",
            "Total current stays constant at 4.4 A because mains supply provides a fixed current",
            "Each existing lamp dims significantly because the mains supply runs out of stored charge",
        ],
        answer_index=0,
        tags=[None, "M5", "M2", "M4"],
        explanation="With two 100 Ω lamps in parallel, R_eq = 100 / 2 = 50 Ω, drawing I = 220 / 50 = 4.4 A. Adding a third 100 Ω lamp in parallel provides another path for current: R_eq = 100 / 3 ≈ 33.3 Ω. Total mains current increases to I = 220 / 33.33 ≈ 6.6 A. Each lamp still has 220 V across it and continues glowing at full brightness.",
        source_note="NCERT Class 10 Science, Section 11.6.2; Domestic Electric Circuits.",
    ),

    # =========================================================================
    # CONCEPT 8: POWER (Electric Power & Heating)
    # =========================================================================
    # --- Item 22 (Level 1 - Easy) ---
    # Solution: P = V * I = 220 V * 5 A = 1100 W.
    Item(
        item_id="q_pow_01",
        concept="power",
        difficulty_label=1,
        question="An electric room heater is connected to a 220 V supply line and draws a current of 5 A. What is the electric power consumed by the heater?",
        options=[
            "1100 W (P = V × I = 220 V × 5 A = 1100 W)",
            "44 W (calculated as 220 V / 5 A)",
            "1100 J (confusing power in Watts with electrical energy in Joules)",
            "225 W (calculated as 220 V + 5 A)",
        ],
        answer_index=0,
        tags=[None, "M3", "M3", None],
        explanation="Electric power P is the rate at which electrical energy is dissipated in a circuit: P = V × I. Given V = 220 V and I = 5 A, P = 220 × 5 = 1100 Watts (W). Power is measured in Watts (Joules per second), not Joules.",
        source_note="NCERT Class 10 Science, Section 11.8 'Electric Power'.",
    ),

    # --- Item 23 (Level 2 - Medium) ---
    # Solution: R = V^2 / P = 220^2 / 100 = 484 Ω. At 110 V: P' = V'^2 / R = 110^2 / 484 = 12100 / 484 = 25 W.
    Item(
        item_id="q_pow_02",
        concept="power",
        difficulty_label=2,
        question="An electric bulb is rated 220 V and 100 W. When it is operated on 110 V, what will be the power consumed by the bulb (assume filament resistance remains constant)?",
        options=[
            "25 W (R = V^2/P = 484 Ω; at 110 V, P' = V'^2/R = 110^2 / 484 = 25 W)",
            "50 W (assuming power decreases linearly by half when voltage halves)",
            "100 W (the bulb always dissipates its stamped rated power regardless of voltage)",
            "75 W (assuming current remains constant while voltage drops)",
        ],
        answer_index=0,
        tags=[None, "M3", None, "M2"],
        explanation="From rated specifications, resistance of the bulb filament is R = V^2 / P = (220)^2 / 100 = 48400 / 100 = 484 Ω. When operated at V' = 110 V, power consumed is P' = (V')^2 / R = (110)^2 / 484 = 12100 / 484 = 25 W. (Power is proportional to voltage squared, so halving voltage quarters power).",
        source_note="NCERT Class 10 Science, Chapter End Exercise Question 3 (Classic CBSE Board Question).",
    ),

    # --- Item 24 (Level 3 - Hard) ---
    # Solution: R1 = 220^2 / 60 = 806.7 Ω; R2 = 220^2 / 100 = 484 Ω.
    # In series, I is identical: P_actual = I^2 * R. Since R1 > R2, P1 > P2, so 60 W bulb glows brighter!
    Item(
        item_id="q_pow_03",
        concept="power",
        difficulty_label=3,
        question="Two bulbs rated (60 W, 220 V) and (100 W, 220 V) are connected in series across a 220 V mains supply. Which bulb glows brighter and why?",
        options=[
            "The 60 W bulb glows brighter because its higher resistance (807 Ω vs 484 Ω) dissipates more power with equal series current (P = I^2 × R)",
            "The 100 W bulb glows brighter because higher rated wattage always yields brighter light in any circuit",
            "Both bulbs glow with equal brightness because the series circuit forces identical power into all components",
            "Neither bulb glows because series connection uses up all charge before reaching the second bulb",
        ],
        answer_index=0,
        tags=[None, "M3", "M2", "M1"],
        explanation="Filament resistances are R_60 = V^2/P = (220)^2 / 60 ≈ 807 Ω, and R_100 = (220)^2 / 100 = 484 Ω. In a series circuit, the current I is identical through both bulbs. Actual power dissipated is P = I^2 × R. Because R_60 > R_100, the 60 W bulb dissipates more electrical power (I^2 × 807 > I^2 × 484) and therefore glows brighter than the 100 W bulb.",
        source_note="NCERT Class 10 Science, Exemplar Physics Problems; PER Bulb Brightness in Series.",
    ),
]

def get_question_by_id(item_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve question entry by ID."""
    for q in QUESTION_BANK:
        if q["id"] == item_id:
            return q
    return None

def get_questions_for_concept(concept: str) -> List[Dict[str, Any]]:
    """Return all verified questions for a given concept."""
    return [q for q in QUESTION_BANK if q["concept"] == concept]

def get_diagnostic_questions() -> List[Dict[str, Any]]:
    """
    Return 8 diagnostic questions in prerequisite order.
    Uses Level 2 (medium) items so that initial diagnostic tests
    can accurately measure baseline ability across all 8 syllabus topics.
    """
    diag_ids = [
        "q_chg_02",  # charge (Level 2)
        "q_cur_02",  # current (Level 2)
        "q_pd_02",   # pd (Level 2)
        "q_ohm_02",  # ohm (Level 2)
        "q_res_02",  # resistance (Level 2)
        "q_ser_02",  # series (Level 2)
        "q_par_02",  # parallel (Level 2)
        "q_pow_02",  # power (Level 2)
    ]
    diag_items = []
    for qid in diag_ids:
        q = get_question_by_id(qid)
        if q:
            diag_items.append(q)
    return diag_items
