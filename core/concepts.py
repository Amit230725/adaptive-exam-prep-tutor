"""core/concepts.py - Concept Graph & Misconception Knowledge Model

Curriculum: Complete CBSE Class 10 Science Physics Syllabus (NCERT):
- Chapter 9: Light – Reflection and Refraction
- Chapter 10: The Human Eye and the Colourful World
- Chapter 11: Electricity
- Chapter 12: Magnetic Effects of Electric Current

Blueprint Reference: Section 6 "Curriculum and concept-graph design"
- 20 Primary Syllabus Concepts with verified 60-item question bank (3 items per concept, levels 1-3)
- 51 Granular Inventory Concepts (L1-L17, E1-E10, C1-C14, M1-M10) + Mathematical Prerequisites
- 17 Research Misconceptions (M1 - M17)
- 8 Formal Section 9 Misconception Codes (CURRENT_CONSUMED, MIRROR_SIGN, etc.)
"""

from typing import Dict, List, Optional, Any, Set

# -----------------------------------------------------------------------------
# 0. MATHEMATICAL PREREQUISITES (Blueprint Section 6)
# -----------------------------------------------------------------------------
MATH_PREREQUISITES: Dict[str, Dict[str, Any]] = {
    "MATH_FRACTIONS": {
        "id": "MATH_FRACTIONS",
        "name": "Fractions & Ratios",
        "description": "Manipulating fractions, cross-multiplication, and simplifying numerical ratios.",
    },
    "MATH_RECIPROCALS": {
        "id": "MATH_RECIPROCALS",
        "name": "Reciprocal Equations",
        "description": "Solving equations of form 1/x = 1/a + 1/b for focal length and parallel resistance.",
    },
    "MATH_SIGNS": {
        "id": "MATH_SIGNS",
        "name": "Signed Arithmetic & Conventions",
        "description": "Handling positive and negative integers in algebraic substitution.",
    },
    "MATH_UNITS": {
        "id": "MATH_UNITS",
        "name": "Unit Conversions & Dimensionality",
        "description": "Converting cm to m, mA to A, kW to W, and Joules to kWh.",
    },
    "MATH_GRAPHS": {
        "id": "MATH_GRAPHS",
        "name": "Graph Reading & Slopes",
        "description": "Interpreting linear slopes in V-I graphs to extract physical resistance.",
    },
}

# -----------------------------------------------------------------------------
# 1. CHAPTER STRUCTURE
# -----------------------------------------------------------------------------
CHAPTERS: Dict[str, Dict[str, Any]] = {
    "light": {
        "id": "light",
        "name": "Chapter 9: Light – Reflection & Refraction",
        "short_name": "Light",
        "icon": "💡",
        "order": 1,
        "concepts": ["reflection_mirrors", "refraction_laws", "refraction_lenses", "lens_power"],
        "concepts_51": [
            "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8",
            "L9", "L10", "L11", "L12", "L13", "L14", "L15", "L16", "L17"
        ],
        "description": "Spherical mirrors, mirror formula, refraction laws, Snell's law, spherical lenses, lens formula, and power of a lens.",
    },
    "human_eye": {
        "id": "human_eye",
        "name": "Chapter 10: The Human Eye & Colourful World",
        "short_name": "Human Eye",
        "icon": "👁️",
        "order": 2,
        "concepts": ["eye_vision", "defects_vision", "prism_dispersion", "atmospheric_scattering"],
        "concepts_51": [
            "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10"
        ],
        "description": "Structure of eye, power of accommodation, myopia & hypermetropia correction, prism dispersion, and atmospheric scattering.",
    },
    "electricity": {
        "id": "electricity",
        "name": "Chapter 11: Electricity",
        "short_name": "Electricity",
        "icon": "⚡",
        "order": 3,
        "concepts": ["charge", "current", "pd", "ohm", "resistance", "series", "parallel", "power"],
        "concepts_51": [
            "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8",
            "C9", "C10", "C11", "C12", "C13", "C14"
        ],
        "description": "Electric charge, current, potential difference, Ohm's law, resistance factors, series & parallel combinations, and Joule's heating.",
    },
    "magnetism": {
        "id": "magnetism",
        "name": "Chapter 12: Magnetic Effects of Electric Current",
        "short_name": "Magnetic Effects",
        "icon": "🧲",
        "order": 4,
        "concepts": ["magnetic_field", "current_magnetism", "magnetic_force", "domestic_circuits"],
        "concepts_51": [
            "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"
        ],
        "description": "Magnetic field lines, Right-Hand Thumb Rule, circular loops, solenoids, Fleming's Left-Hand Rule, and domestic circuit safety.",
    },
}

# -----------------------------------------------------------------------------
# 2. 20 PRIMARY SYLLABUS CONCEPTS (Strictly 20 items, perfectly matching bank)
# -----------------------------------------------------------------------------
CONCEPTS: Dict[str, Dict[str, Any]] = {
    # --- CHAPTER 9: LIGHT ---
    "reflection_mirrors": {
        "id": "reflection_mirrors",
        "name": "Spherical Mirrors & Reflection",
        "chapter": "light",
        "prerequisites": [],
        "order": 1,
        "description": "Laws of reflection; concave and convex mirrors, principal focus, focal length f = R/2, mirror formula 1/v + 1/u = 1/f, magnification m = -v/u.",
    },
    "refraction_laws": {
        "id": "refraction_laws",
        "name": "Refraction of Light & Snell's Law",
        "chapter": "light",
        "prerequisites": [],
        "order": 2,
        "description": "Bending of light across media, optically rarer vs denser media, Snell's law (sin i / sin r = constant), absolute and relative refractive index (n = c/v).",
    },
    "refraction_lenses": {
        "id": "refraction_lenses",
        "name": "Spherical Lenses & Ray Optics",
        "chapter": "light",
        "prerequisites": ["refraction_laws"],
        "order": 3,
        "description": "Convex and concave lenses, optical centre, principal focus, ray diagrams, lens formula 1/v - 1/u = 1/f, magnification m = v/u, Cartesian sign convention.",
    },
    "lens_power": {
        "id": "lens_power",
        "name": "Power of a Lens",
        "chapter": "light",
        "prerequisites": ["refraction_lenses"],
        "order": 4,
        "description": "Definition of power P = 1/f (in metres), unit Dioptre (D), positive for convex lens, negative for concave lens, combination of thin lenses in contact P = P1 + P2.",
    },

    # --- CHAPTER 10: THE HUMAN EYE & COLOURFUL WORLD ---
    "eye_vision": {
        "id": "eye_vision",
        "name": "Human Eye & Accommodation",
        "chapter": "human_eye",
        "prerequisites": ["refraction_lenses"],
        "order": 5,
        "description": "Structure of human eye, cornea, iris, pupil, eye lens, retina, ciliary muscles, power of accommodation, near point (25 cm) and far point (infinity).",
    },
    "defects_vision": {
        "id": "defects_vision",
        "name": "Defects of Vision & Correction",
        "chapter": "human_eye",
        "prerequisites": ["eye_vision", "lens_power"],
        "order": 6,
        "description": "Myopia (short-sightedness, concave lens correction), Hypermetropia (far-sightedness, convex lens correction), and Presbyopia (bifocal correction).",
    },
    "prism_dispersion": {
        "id": "prism_dispersion",
        "name": "Prism Refraction & Dispersion",
        "chapter": "human_eye",
        "prerequisites": ["refraction_laws"],
        "order": 7,
        "description": "Refraction of light through a triangular glass prism, angle of deviation, dispersion of white light into VIBGYOR, recombination with inverted prism.",
    },
    "atmospheric_scattering": {
        "id": "atmospheric_scattering",
        "name": "Atmospheric Refraction & Scattering",
        "chapter": "human_eye",
        "prerequisites": ["refraction_laws"],
        "order": 8,
        "description": "Atmospheric refraction effects (twinkling of stars, advance sunrise and delayed sunset), Tyndall effect, Rayleigh scattering, blue colour of sky, reddish sunrise/sunset.",
    },

    # --- CHAPTER 11: ELECTRICITY ---
    "charge": {
        "id": "charge",
        "name": "Electric Charge & Conductors",
        "chapter": "electricity",
        "prerequisites": [],
        "order": 9,
        "description": "Fundamental electric charge (positive and negative), SI unit Coulomb (C), quantization Q = ne, elementary charge e = 1.6x10^-19 C, conductors vs insulators.",
    },
    "current": {
        "id": "current",
        "name": "Electric Current & Circuits",
        "chapter": "electricity",
        "prerequisites": ["charge"],
        "order": 10,
        "description": "Rate of flow of electric charge I = Q/t, SI unit Ampere (A), conventional current vs electron drift, ammeter connection (in series with low resistance).",
    },
    "pd": {
        "id": "pd",
        "name": "Potential Difference & Voltage",
        "chapter": "electricity",
        "prerequisites": ["charge"],
        "order": 11,
        "description": "Work done per unit charge moving between two points V = W/Q, SI unit Volt (V), role of battery/cell, voltmeter connection (in parallel with high resistance).",
    },
    "ohm": {
        "id": "ohm",
        "name": "Ohm's Law & V-I Graph",
        "chapter": "electricity",
        "prerequisites": ["current", "pd"],
        "order": 12,
        "description": "Ohm's Law V = IR at constant temperature, linear V-I characteristic for ohmic conductors, slope = R, definition of electrical resistance and the Ohm (Ω).",
    },
    "resistance": {
        "id": "resistance",
        "name": "Factors Affecting Resistance & Resistivity",
        "chapter": "electricity",
        "prerequisites": ["ohm"],
        "order": 13,
        "description": "Resistance R proportional to length l, inversely proportional to area A (R = rho * l / A), resistivity rho (Ω m), temperature dependence, conductor vs alloy vs insulator.",
    },
    "series": {
        "id": "series",
        "name": "Resistors in Series Combination",
        "chapter": "electricity",
        "prerequisites": ["ohm"],
        "order": 14,
        "description": "Series circuit rules: single path, invariant current throughout, total voltage divides V = V1 + V2 + V3, equivalent resistance Rs = R1 + R2 + R3.",
    },
    "parallel": {
        "id": "parallel",
        "name": "Resistors in Parallel Combination",
        "chapter": "electricity",
        "prerequisites": ["ohm"],
        "order": 15,
        "description": "Parallel circuit rules: multiple independent branches, invariant voltage across all branches, total current divides I = I1 + I2 + I3, 1/Rp = 1/R1 + 1/R2.",
    },
    "power": {
        "id": "power",
        "name": "Electric Power & Joule's Heating",
        "chapter": "electricity",
        "prerequisites": ["current", "pd", "ohm"],
        "order": 16,
        "description": "Joule's Law of Heating H = I^2 R t, electric power P = VI = I^2 R = V^2 / R, SI unit Watt (W), commercial energy unit kilowatt-hour (1 kWh = 3.6x10^6 J).",
    },

    # --- CHAPTER 12: MAGNETIC EFFECTS OF ELECTRIC CURRENT ---
    "magnetic_field": {
        "id": "magnetic_field",
        "name": "Magnetic Fields & Field Lines",
        "chapter": "magnetism",
        "prerequisites": [],
        "order": 17,
        "description": "Magnetic field concept, properties of magnetic field lines (continuous closed loops, north to south outside magnet, do not intersect, crowded at poles).",
    },
    "current_magnetism": {
        "id": "current_magnetism",
        "name": "Oersted Effect & Magnetic Field of Current",
        "chapter": "magnetism",
        "prerequisites": ["current", "magnetic_field"],
        "order": 18,
        "description": "Magnetic field produced by electric current in straight conductor, Maxwell's Right-Hand Thumb Rule, circular loops, solenoids, electromagnet construction.",
    },
    "magnetic_force": {
        "id": "magnetic_force",
        "name": "Magnetic Force & Fleming's Left-Hand Rule",
        "chapter": "magnetism",
        "prerequisites": ["current_magnetism"],
        "order": 19,
        "description": "Force exerted by magnetic field on a current-carrying conductor, direction given by Fleming's Left-Hand Rule (Thumb-Force, Forefinger-Field, Middle-Current), motor principle.",
    },
    "domestic_circuits": {
        "id": "domestic_circuits",
        "name": "Domestic Electric Circuits & Safety",
        "chapter": "magnetism",
        "prerequisites": ["parallel", "power"],
        "order": 20,
        "description": "220V AC domestic circuit wiring (Live, Neutral, Earth wire), role of earthing for metal appliances, electric fuse rating, short-circuiting and overloading prevention.",
    },
}

# -----------------------------------------------------------------------------
# 3. 51 GRANULAR BLUEPRINT CONCEPTS (Blueprint Section 6)
# -----------------------------------------------------------------------------
CONCEPTS_51: Dict[str, Dict[str, Any]] = {
    # Light: L1 - L17
    "L1": {"id": "L1", "code": "L1", "name": "Propagation & Nature of Light", "chapter": "light", "order": 1, "prerequisites": [], "exam_weight": 0.04},
    "L2": {"id": "L2", "code": "L2", "name": "Laws of Reflection", "chapter": "light", "order": 2, "prerequisites": ["L1"], "exam_weight": 0.05},
    "L3": {"id": "L3", "code": "L3", "name": "Plane Mirrors & Virtual Images", "chapter": "light", "order": 3, "prerequisites": ["L2"], "exam_weight": 0.04},
    "L4": {"id": "L4", "code": "L4", "name": "Spherical Mirrors (Concave & Convex)", "chapter": "light", "order": 4, "prerequisites": ["L2"], "exam_weight": 0.06},
    "L5": {"id": "L5", "code": "L5", "name": "Mirror Terms & Focal Geometry", "chapter": "light", "order": 5, "prerequisites": ["L4"], "exam_weight": 0.06},
    "L6": {"id": "L6", "code": "L6", "name": "Mirror Ray Diagrams", "chapter": "light", "order": 6, "prerequisites": ["L5"], "exam_weight": 0.08},
    "L7": {"id": "L7", "code": "L7", "name": "Mirror Formula & Magnification", "chapter": "light", "order": 7, "prerequisites": ["L5", "L6"], "exam_weight": 0.09},
    "L8": {"id": "L8", "code": "L8", "name": "Mirror Cartesian Sign Convention", "chapter": "light", "order": 8, "prerequisites": ["L5"], "exam_weight": 0.08},
    "L9": {"id": "L9", "code": "L9", "name": "Refraction of Light & Optical Density", "chapter": "light", "order": 9, "prerequisites": ["L1"], "exam_weight": 0.06},
    "L10": {"id": "L10", "code": "L10", "name": "Snell's Law & Refractive Index", "chapter": "light", "order": 10, "prerequisites": ["L9"], "exam_weight": 0.08},
    "L11": {"id": "L11", "code": "L11", "name": "Refraction through Glass Slab & Shift", "chapter": "light", "order": 11, "prerequisites": ["L10"], "exam_weight": 0.05},
    "L12": {"id": "L12", "code": "L12", "name": "Spherical Lenses (Convex & Concave)", "chapter": "light", "order": 12, "prerequisites": ["L9"], "exam_weight": 0.06},
    "L13": {"id": "L13", "code": "L13", "name": "Lens Terms & Principal Foci", "chapter": "light", "order": 13, "prerequisites": ["L12"], "exam_weight": 0.05},
    "L14": {"id": "L14", "code": "L14", "name": "Lens Ray Diagrams & Image Formation", "chapter": "light", "order": 14, "prerequisites": ["L13"], "exam_weight": 0.08},
    "L15": {"id": "L15", "code": "L15", "name": "Lens Formula & Magnification", "chapter": "light", "order": 15, "prerequisites": ["L13", "L14"], "exam_weight": 0.09},
    "L16": {"id": "L16", "code": "L16", "name": "Power of a Lens (Dioptres)", "chapter": "light", "order": 16, "prerequisites": ["L15"], "exam_weight": 0.07},
    "L17": {"id": "L17", "code": "L17", "name": "Integrated Optical Numericals", "chapter": "light", "order": 17, "prerequisites": ["L7", "L8", "L15", "L16"], "exam_weight": 0.09},

    # Eye & Colour: E1 - E10
    "E1": {"id": "E1", "code": "E1", "name": "Human Eye Structure & Physiology", "chapter": "human_eye", "order": 18, "prerequisites": ["L12"], "exam_weight": 0.05},
    "E2": {"id": "E2", "code": "E2", "name": "Power of Accommodation", "chapter": "human_eye", "order": 19, "prerequisites": ["E1"], "exam_weight": 0.06},
    "E3": {"id": "E3", "code": "E3", "name": "Near Point & Far Point of Vision", "chapter": "human_eye", "order": 20, "prerequisites": ["E2"], "exam_weight": 0.05},
    "E4": {"id": "E4", "code": "E4", "name": "Myopia & Correction", "chapter": "human_eye", "order": 21, "prerequisites": ["E3", "L15", "L16"], "exam_weight": 0.08},
    "E5": {"id": "E5", "code": "E5", "name": "Hypermetropia & Correction", "chapter": "human_eye", "order": 22, "prerequisites": ["E3", "L15", "L16"], "exam_weight": 0.08},
    "E6": {"id": "E6", "code": "E6", "name": "Presbyopia & Bifocals", "chapter": "human_eye", "order": 23, "prerequisites": ["E4", "E5"], "exam_weight": 0.05},
    "E7": {"id": "E7", "code": "E7", "name": "Refraction through Prism", "chapter": "human_eye", "order": 24, "prerequisites": ["L9", "L10"], "exam_weight": 0.06},
    "E8": {"id": "E8", "code": "E8", "name": "Dispersion & Spectrum (VIBGYOR)", "chapter": "human_eye", "order": 25, "prerequisites": ["E7"], "exam_weight": 0.07},
    "E9": {"id": "E9", "code": "E9", "name": "Scattering of Light & Tyndall Effect", "chapter": "human_eye", "order": 26, "prerequisites": ["L1"], "exam_weight": 0.06},
    "E10": {"id": "E10", "code": "E10", "name": "Atmospheric Optical Phenomena", "chapter": "human_eye", "order": 27, "prerequisites": ["E8", "E9"], "exam_weight": 0.07},

    # Electricity: C1 - C14
    "C1": {"id": "C1", "code": "C1", "name": "Electric Charge & Current", "chapter": "electricity", "order": 28, "prerequisites": [], "exam_weight": 0.06},
    "C2": {"id": "C2", "code": "C2", "name": "Potential Difference & Voltmeter", "chapter": "electricity", "order": 29, "prerequisites": ["C1"], "exam_weight": 0.06},
    "C3": {"id": "C3", "code": "C3", "name": "Circuit Schematics & Symbols", "chapter": "electricity", "order": 30, "prerequisites": ["C1", "C2"], "exam_weight": 0.05},
    "C4": {"id": "C4", "code": "C4", "name": "Ohm's Law & V-I Characteristic", "chapter": "electricity", "order": 31, "prerequisites": ["C1", "C2", "C3"], "exam_weight": 0.09},
    "C5": {"id": "C5", "code": "C5", "name": "Resistance Factors (Length, Area)", "chapter": "electricity", "order": 32, "prerequisites": ["C4"], "exam_weight": 0.07},
    "C6": {"id": "C6", "code": "C6", "name": "Resistivity (rho)", "chapter": "electricity", "order": 33, "prerequisites": ["C5"], "exam_weight": 0.06},
    "C7": {"id": "C7", "code": "C7", "name": "Series Combination of Resistors", "chapter": "electricity", "order": 34, "prerequisites": ["C4"], "exam_weight": 0.08},
    "C8": {"id": "C8", "code": "C8", "name": "Parallel Combination of Resistors", "chapter": "electricity", "order": 35, "prerequisites": ["C4"], "exam_weight": 0.09},
    "C9": {"id": "C9", "code": "C9", "name": "Mixed Series-Parallel Analysis", "chapter": "electricity", "order": 36, "prerequisites": ["C7", "C8"], "exam_weight": 0.09},
    "C10": {"id": "C10", "code": "C10", "name": "Heating Effect of Electric Current", "chapter": "electricity", "order": 37, "prerequisites": ["C4", "C7"], "exam_weight": 0.05},
    "C11": {"id": "C11", "code": "C11", "name": "Joule's Law of Heating", "chapter": "electricity", "order": 38, "prerequisites": ["C10"], "exam_weight": 0.08},
    "C12": {"id": "C12", "code": "C12", "name": "Electric Power (Watts)", "chapter": "electricity", "order": 39, "prerequisites": ["C4", "C11"], "exam_weight": 0.08},
    "C13": {"id": "C13", "code": "C13", "name": "Commercial Energy & Cost Billing", "chapter": "electricity", "order": 40, "prerequisites": ["C12"], "exam_weight": 0.06},
    "C14": {"id": "C14", "code": "C14", "name": "Integrated Circuit Numericals", "chapter": "electricity", "order": 41, "prerequisites": ["C9", "C12", "C13"], "exam_weight": 0.09},

    # Magnetism: M1 - M10
    "M1": {"id": "M1", "code": "M1", "name": "Magnetic Fields & Field Lines", "chapter": "magnetism", "order": 42, "prerequisites": [], "exam_weight": 0.06},
    "M2": {"id": "M2", "code": "M2", "name": "Field of Straight Current Conductor", "chapter": "magnetism", "order": 43, "prerequisites": ["C1", "M1"], "exam_weight": 0.07},
    "M3": {"id": "M3", "code": "M3", "name": "Right-Hand Thumb Rule", "chapter": "magnetism", "order": 44, "prerequisites": ["M2"], "exam_weight": 0.07},
    "M4": {"id": "M4", "code": "M4", "name": "Magnetic Field in a Circular Loop", "chapter": "magnetism", "order": 45, "prerequisites": ["M3"], "exam_weight": 0.06},
    "M5": {"id": "M5", "code": "M5", "name": "Magnetic Field in Solenoid", "chapter": "magnetism", "order": 46, "prerequisites": ["M4"], "exam_weight": 0.08},
    "M6": {"id": "M6", "code": "M6", "name": "Magnetic Force on Current Conductor", "chapter": "magnetism", "order": 47, "prerequisites": ["M1", "C1"], "exam_weight": 0.07},
    "M7": {"id": "M7", "code": "M7", "name": "Fleming's Left-Hand Rule", "chapter": "magnetism", "order": 48, "prerequisites": ["M6"], "exam_weight": 0.08},
    "M8": {"id": "M8", "code": "M8", "name": "Electric Motor Principle & AC/DC", "chapter": "magnetism", "order": 49, "prerequisites": ["M7"], "exam_weight": 0.07},
    "M9": {"id": "M9", "code": "M9", "name": "Domestic Electric Circuits", "chapter": "magnetism", "order": 50, "prerequisites": ["C8", "C13"], "exam_weight": 0.07},
    "M10": {"id": "M10", "code": "M10", "name": "Circuit Safety: Earthing & Fuses", "chapter": "magnetism", "order": 51, "prerequisites": ["M9", "C11"], "exam_weight": 0.08},
}

# -----------------------------------------------------------------------------
# 4. FORMAL SECTION 9 MISCONCEPTION TAXONOMY (Blueprint Section 9)
# -----------------------------------------------------------------------------
FORMAL_MISCONCEPTIONS: Dict[str, Dict[str, Any]] = {
    "CURRENT_CONSUMED": {
        "code": "CURRENT_CONSUMED",
        "label": "Current is Consumed in Circuit",
        "hypothesis": "Current is used up by a resistor or light bulb as it travels through a series path.",
        "useful_disambiguating_evidence": "Compare predicted ammeter readings before and after a series component (I_in == I_out).",
        "correct_principle": "Electric charge is conserved. Current is the rate of flow of charge and is strictly identical at all points in a single unbranched loop.",
        "contrast_intuition": "Flawed: 'The bulb uses up the current so less current returns to the cell.'\nCorrect: 'Current is not fuel; energy is carried by charges, but every Coulomb entering leaves the component.'",
        "approved_probes": ["If an ammeter reads 1.5 A before a 10 Ohm resistor, what does an identical ammeter read right after it?"],
        "remediation_hint": "Remember the closed pipe water analogy: water cannot disappear inside a constricted pipe; flow rate in equals flow rate out.",
        "chapter": "electricity",
        "related_concepts": ["current", "series"],
    },
    "V_I_CONFUSION": {
        "code": "V_I_CONFUSION",
        "label": "Voltage & Current are Interchangeable",
        "hypothesis": "Voltage and current are the same thing, or voltage flows through wires like a fluid.",
        "useful_disambiguating_evidence": "Ask for physical meaning and units (Joules/Coulomb vs Coulombs/second) before numerical calculation.",
        "correct_principle": "Current (I) is the flow rate of charge (Amperes = C/s). Voltage (V) is the work done per unit charge (Volts = J/C) driving that flow.",
        "contrast_intuition": "Flawed: 'There is a voltage flowing through this bulb.'\nCorrect: 'Current flows THROUGH a component; voltage is the potential difference ACROSS its two terminals.'",
        "approved_probes": ["Can a battery maintain 12 Volts across its terminals when connected to an open switch with zero current?"],
        "remediation_hint": "Think of voltage as the electric pressure pushed by the battery, and current as the resulting rate of traffic.",
        "chapter": "electricity",
        "related_concepts": ["current", "pd", "ohm"],
    },
    "PARALLEL_ADDITION": {
        "code": "PARALLEL_ADDITION",
        "label": "Parallel Resistances Added Directly",
        "hypothesis": "Adding resistors in parallel increases total equivalent resistance (adding paths increases difficulty).",
        "useful_disambiguating_evidence": "Ask whether opening a parallel highway lane increases or decreases total traffic congestion.",
        "correct_principle": "Adding parallel branches creates alternate pathways for charge, always reducing total equivalent resistance: 1/Rp = 1/R1 + 1/R2.",
        "contrast_intuition": "Flawed: 'Two 10 Ohm resistors in parallel give 20 Ohms.'\nCorrect: 'Two 10 Ohm resistors in parallel give 5 Ohms because charge has two equal paths to cross.'",
        "approved_probes": ["What happens to the total resistance of your home circuit when you turn on a second light bulb in parallel?"],
        "remediation_hint": "More parallel branches are like more open checkout counters at a store: customers clear out faster, so resistance drops.",
        "chapter": "electricity",
        "related_concepts": ["parallel"],
    },
    "MIRROR_SIGN": {
        "code": "MIRROR_SIGN",
        "label": "Inconsistent Cartesian Sign Convention",
        "hypothesis": "Mirror distances or focal lengths use arbitrary signs (e.g. treating concave focal length as positive).",
        "useful_disambiguating_evidence": "Inspect signed substitution in 1/f = 1/v + 1/u separately from the algebraic calculation.",
        "correct_principle": "Concave mirror focus lies in front of mirror: f is NEGATIVE (-). Object in front: u is NEGATIVE (-). Real image in front: v is NEGATIVE (-).",
        "contrast_intuition": "Flawed: 'f = 20 cm for a concave mirror.'\nCorrect: 'By Cartesian convention with pole as origin, concave mirror focal length is strictly f = -20 cm.'",
        "approved_probes": ["For a concave mirror of focal length 15 cm with an object at 30 cm, what signs must be substituted for f and u?"],
        "remediation_hint": "Always set the mirror pole at the coordinate origin (0, 0). Distances against the incoming ray (to the left) are negative.",
        "chapter": "light",
        "related_concepts": ["reflection_mirrors"],
    },
    "FOCAL_RADIUS": {
        "code": "FOCAL_RADIUS",
        "label": "Focal Length Equals Radius of Curvature",
        "hypothesis": "Focal length equals the radius of curvature (f = R) rather than half of it (f = R/2).",
        "useful_disambiguating_evidence": "Ask the geometric relationship between the centre of curvature C and focus F, and check mirror formula substitutions.",
        "correct_principle": "For spherical mirrors of small aperture, the principal focus lies midway between the pole and centre of curvature: f = R / 2.",
        "contrast_intuition": "Flawed: 'If radius of curvature is 40 cm, then focal length is 40 cm.'\nCorrect: 'The focal length is half the radius: f = 40 / 2 = 20 cm.'",
        "approved_probes": ["If a convex security mirror has a radius of curvature of 3.0 m, what is its focal length?"],
        "remediation_hint": "Focus is the midpoint! F cuts the distance between Pole and Centre of Curvature exactly in half.",
        "chapter": "light",
        "related_concepts": ["reflection_mirrors"],
    },
    "CONVEX_ALWAYS_REAL": {
        "code": "CONVEX_ALWAYS_REAL",
        "label": "Convex Lenses Always Form Real Images",
        "hypothesis": "Convex lenses can only produce real and inverted images, forgetting the magnifying glass case.",
        "useful_disambiguating_evidence": "Probe the object-inside-focus case (u < f), such as reading with a handheld magnifying glass.",
        "correct_principle": "When an object is placed closer than the principal focus (between F1 and optical centre O), a convex lens forms an erect, magnified, virtual image.",
        "contrast_intuition": "Flawed: 'Convex lenses always produce real images on a screen.'\nCorrect: 'Inside the focal length, rays diverge and must be projected backwards to form a virtual, magnified image.'",
        "approved_probes": ["Where must a stamp be placed relative to a convex lens to use it as a simple magnifying glass?"],
        "remediation_hint": "Think of a detective's magnifying glass: you see an upright, enlarged virtual image through the glass because the object is inside f.",
        "chapter": "light",
        "related_concepts": ["refraction_lenses"],
    },
    "POWER_ENERGY": {
        "code": "POWER_ENERGY",
        "label": "Power & Energy are the Same Quantity",
        "hypothesis": "Power (Watts) and electrical energy (Joules or kWh) are used interchangeably.",
        "useful_disambiguating_evidence": "Ask units and a duration-dependent consumption problem (e.g. comparing a 1000W iron for 5 mins vs a 100W bulb for 10 hours).",
        "correct_principle": "Power is the instantaneous rate of energy consumption (Joules/second). Electrical energy is the total accumulated work: Energy = Power * Time.",
        "contrast_intuition": "Flawed: 'The electric bill charges for the maximum power of the appliance.'\nCorrect: 'The bill charges for kilowatt-hours (energy = power in kW * hours used), not peak wattage alone.'",
        "approved_probes": ["Which uses more electrical energy: a 1000 W heater running for 10 minutes or a 100 W bulb running for 5 hours?"],
        "remediation_hint": "Power is speedometer speed (km/h); Energy is total distance traveled (km). Speed * time = distance.",
        "chapter": "electricity",
        "related_concepts": ["power"],
    },
    "FIELD_DIRECTION": {
        "code": "FIELD_DIRECTION",
        "label": "Magnetic Field or Force Rules Confused",
        "hypothesis": "Confuses Right-Hand Thumb Rule (field direction around wire) with Fleming's Left-Hand Rule (mechanical force on wire).",
        "useful_disambiguating_evidence": "Use labelled current/field/force diagrams with one unknown and ask which specific physical rule applies.",
        "correct_principle": "Right-Hand Thumb Rule determines the shape and direction of magnetic field created by current. Fleming's Left-Hand Rule determines motor force on current inside external field.",
        "contrast_intuition": "Flawed: 'Use Left-Hand rule to find magnetic field lines around a straight wire.'\nCorrect: 'Right hand grips the wire for field lines; Left hand finds the direction of thrust/motion.'",
        "approved_probes": ["Which rule predicts which way an aluminum rod will jump when carrying current between the poles of a horseshoe magnet?"],
        "remediation_hint": "Right hand = Current MAKES a magnetic field. Left hand = External magnetic field PUSHES a current conductor (Motor).",
        "chapter": "magnetism",
        "related_concepts": ["current_magnetism", "magnetic_force"],
    },
}

# -----------------------------------------------------------------------------
# 5. RESEARCH-BACKED MISCONCEPTION LIBRARY (M1 - M17, strictly 17 entries)
# -----------------------------------------------------------------------------
MISCONCEPTIONS: Dict[str, Dict[str, Any]] = {
    "M1": {
        "id": "M1", "chapter": "electricity", "formal_code": "CURRENT_CONSUMED",
        "label": "Current is used up as it passes through a bulb/resistor",
        "description": "Student believes charges are destroyed or consumed in electrical components, so less current returns to the battery.",
        "concept": "current",
        "correction": "Electric current is strictly conserved throughout a single loop: every Coulomb that enters a component also exits it.",
        "challenge_idea": "If two identical ammeters are connected before and after a resistor, what will their readings show?",
        "reteach_action": "Two-ammeter series demonstration: connect identical ammeters before and after a light bulb to prove I_before == I_after.",
        "source": "McDermott & Shaffer (1992); Shipstone (1988)",
    },
    "M2": {
        "id": "M2", "chapter": "electricity", "formal_code": "V_I_CONFUSION",
        "label": "Battery is a constant-current source",
        "description": "Student believes a battery pushes the exact same total current regardless of the circuit resistance attached.",
        "concept": "ohm",
        "correction": "A battery maintains a constant potential difference across its terminals; total current drawn depends on equivalent resistance I = V/R.",
        "challenge_idea": "Does your car battery push the same current to a tiny dashboard clock as it does to the engine starter motor?",
        "reteach_action": "Variable resistor demo: connect a 10 Ohm and then 100 Ohm resistor to a 9V cell, observing ammeter needle drop.",
        "source": "Cohen, Eylon & Ganiel (1983)",
    },
    "M3": {
        "id": "M3", "chapter": "electricity", "formal_code": "V_I_CONFUSION",
        "label": "Confuses current, voltage, and electrical energy",
        "description": "Student uses 'voltage' and 'current' interchangeably, or believes voltage travels through wires.",
        "concept": "pd",
        "correction": "Current is the rate of flow of charge (Amperes); voltage is the electrical potential energy difference (Volts) across two points.",
        "challenge_idea": "Can high voltage exist between two terminals with zero current flowing?",
        "reteach_action": "Water circuit analogy: voltage is water pressure in the pipe; current is litres of water passing per second.",
        "source": "Engelhardt & Beichner (2004 - DIRECT)",
    },
    "M4": {
        "id": "M4", "chapter": "electricity", "formal_code": "CURRENT_CONSUMED",
        "label": "Battery manufactures or stores raw charge that empties out",
        "description": "Student believes battery is a tank of static charge rather than a closed loop energy pump.",
        "concept": "charge",
        "correction": "A battery does not create or store net charge; mobile charges pre-exist inside the copper wire, and chemical reactions push them in a loop.",
        "challenge_idea": "If charges came out of the battery, where would they go when the circuit is switched off?",
        "reteach_action": "Closed bicycle chain demonstration: turning the pedals moves all links simultaneously throughout the loop.",
        "source": "Chambers & Andre (1997)",
    },
    "M5": {
        "id": "M5", "chapter": "electricity", "formal_code": "PARALLEL_ADDITION",
        "label": "Adding resistors in parallel increases total resistance",
        "description": "Student applies series intuition (more components = more resistance) to parallel branches.",
        "concept": "parallel",
        "correction": "Adding parallel branches creates alternate pathways for current, always decreasing the total equivalent resistance (1/Rp = 1/R1 + 1/R2).",
        "challenge_idea": "If a store opens a second checkout lane, does customer waiting time increase or decrease?",
        "reteach_action": "Highway lane analogy: adding extra lanes always reduces total traffic congestion.",
        "source": "McDermott & Shaffer (1992)",
    },
    "M6": {
        "id": "M6", "chapter": "electricity", "formal_code": "V_I_CONFUSION",
        "label": "Resistance depends on applied voltage or current",
        "description": "Student misinterprets R = V/I to mean changing battery voltage alters the intrinsic resistance of an ohmic wire.",
        "concept": "resistance",
        "correction": "For an ohmic conductor, resistance R is an intrinsic physical property determined by geometry and material (R = rho * l / A), independent of V or I.",
        "challenge_idea": "If you disconnect a 10 Ohm resistor from a battery, does its resistance become zero?",
        "reteach_action": "Ohm's Law graph slope verification: show that doubling V doubles I while slope (R) remains constant.",
        "source": "Gunstone & White (1981)",
    },
    "M7": {
        "id": "M7", "chapter": "electricity", "formal_code": "PARALLEL_ADDITION",
        "label": "In parallel, current splits equally regardless of branch resistances",
        "description": "Student splits current 50/50 without checking branch resistances.",
        "concept": "parallel",
        "correction": "Current in parallel divides inversely proportional to branch resistance (I1 * R1 = I2 * R2 = V). More current flows through the smaller resistor.",
        "challenge_idea": "If one branch has 1 Ohm and the parallel branch has 1000 Ohms, do equal currents pass through both?",
        "reteach_action": "Two parallel bulbs with unequal wattages: show that higher-wattage lower-resistance branch draws much more current.",
        "source": "Liegeois et al. (2003)",
    },
    "M8": {
        "id": "M8", "chapter": "light", "formal_code": "MIRROR_SIGN",
        "label": "Image is located on the surface of the mirror/lens",
        "description": "Student believes optical images are painted on the glass surface rather than formed at the geometric intersection of rays in space.",
        "concept": "reflection_mirrors",
        "correction": "An optical image is located in space where reflected or refracted rays actually intersect (real image) or appear to diverge from (virtual image).",
        "challenge_idea": "If you look into a plane mirror and move your head left or right, does your image stay fixed on one glass spot?",
        "reteach_action": "Parallax demonstration: locate real image in front of a concave mirror using an upright optical pin.",
        "source": "Goldberg & McDermott (1987)",
    },
    "M9": {
        "id": "M9", "chapter": "light", "formal_code": "CONVEX_ALWAYS_REAL",
        "label": "Covering half a lens cuts the image in half",
        "description": "Student believes top half of lens forms top half of image, rather than every point on lens forming the complete image with reduced brightness.",
        "concept": "refraction_lenses",
        "correction": "Every portion of a lens forms a complete image of the object. Covering half the lens reduces the light collected, dimming the entire image by 50%.",
        "challenge_idea": "If you block the top half of your camera lens with black paper, does the bottom half of the photo turn black?",
        "reteach_action": "Cardboard aperture demonstration: project a filament image onto a screen, cover half the lens, and verify the full image remains intact though dimmer.",
        "source": "Galili & Hazan (2000)",
    },
    "M10": {
        "id": "M10", "chapter": "light", "formal_code": "FOCAL_RADIUS",
        "label": "Focal length varies with object position or equals radius",
        "description": "Student believes moving an object closer changes the mirror's or lens's intrinsic focal length, or conflates f with R.",
        "concept": "reflection_mirrors",
        "correction": "Focal length is an intrinsic property determined solely by surface curvature: f = R / 2 for spherical mirrors.",
        "challenge_idea": "Does bringing your face closer to a shaving mirror change the curve of the glass?",
        "reteach_action": "Optical bench demonstration: measure f for distant tree, then show f is identical when object is 50 cm away.",
        "source": "Bendall, Goldberg & Galili (1993)",
    },
    "M11": {
        "id": "M11", "chapter": "light", "formal_code": "MIRROR_SIGN",
        "label": "Light slows down and runs out of energy traveling in uniform air",
        "description": "Student attributes image dimming to light fatigue rather than inverse-square geometric spreading.",
        "concept": "refraction_laws",
        "correction": "Light travels at constant speed c in uniform medium; intensity decreases with distance because energy spreads over a spherical wavefront (1/r^2).",
        "challenge_idea": "If light ran out of energy in air, could we see starlight that has traveled trillions of kilometres?",
        "reteach_action": "Laser pointer demonstration across classroom: show sharp beam brightness does not fatigue in clean air.",
        "source": "Guesne (1985)",
    },
    "M12": {
        "id": "M12", "chapter": "human_eye", "formal_code": "CONVEX_ALWAYS_REAL",
        "label": "Eye sees by projecting vision rays outward to the object",
        "description": "Active extramission theory: student believes the human eye emits seeing rays rather than capturing incoming light.",
        "concept": "eye_vision",
        "correction": "Vision occurs when external light reflected from an object enters the pupil and forms an image on the retina.",
        "challenge_idea": "If eyes shoot out seeing rays, why can we not see anything inside a pitch-black room?",
        "reteach_action": "Dark room experiment: turn off all lights, prove complete blindness until a single photon source is switched on.",
        "source": "Winer, Cottrell, Karefilaki & Gregg (1996)",
    },
    "M13": {
        "id": "M13", "chapter": "human_eye", "formal_code": "CONVEX_ALWAYS_REAL",
        "label": "Myopia corrected with convex lens / Hypermetropia with concave",
        "description": "Student inverts corrective lens prescriptions (confuses converging vs diverging requirements).",
        "concept": "defects_vision",
        "correction": "In myopia, the eye converges rays too strongly (focus in front of retina), requiring a diverging (concave) lens. In hypermetropia, rays focus behind retina, requiring a converging (convex) lens.",
        "challenge_idea": "If rays meet too early in front of the retina, do you need to bend them inward more or spread them out?",
        "reteach_action": "Ray box diagram comparison: project parallel rays through converging lens and show how concave pre-lens shifts focus back to retina.",
        "source": "Selley (1996)",
    },
    "M14": {
        "id": "M14", "chapter": "human_eye", "formal_code": "CONVEX_ALWAYS_REAL",
        "label": "Prism adds colour to pure white light",
        "description": "Student believes glass prism stains or dyes incoming light rather than separating pre-existing wavelengths.",
        "concept": "prism_dispersion",
        "correction": "White light is a polychromatic mixture of all visible wavelengths; the prism bends each wavelength by a different angle (dispersion).",
        "challenge_idea": "If a prism adds colour, why does monochromatic laser light not split into colours when passing through a prism?",
        "reteach_action": "Newton's inverted prism recombination: place an inverted prism behind the first prism and recombine VIBGYOR into pure white light.",
        "source": "Galili & Hazan (2000)",
    },
    "M15": {
        "id": "M15", "chapter": "magnetism", "formal_code": "FIELD_DIRECTION",
        "label": "Magnetic poles can be isolated as single monopoles",
        "description": "Student believes cutting a bar magnet in half isolates a pure North pole and a pure South pole.",
        "concept": "magnetic_field",
        "correction": "Magnetic monopoles do not exist in classical electromagnetism; cutting a magnet in half immediately produces two new complete dipole magnets.",
        "challenge_idea": "If you cut a bar magnet at the exact equator, what do the cut faces do when brought together?",
        "reteach_action": "Fracture demonstration: break a small ceramic magnet in half and demonstrate that the two cut faces strongly attract each other (North and South).",
        "source": "Maloney et al. (2001 - CSEM)",
    },
    "M16": {
        "id": "M16", "chapter": "magnetism", "formal_code": "FIELD_DIRECTION",
        "label": "Magnetic field exerts force parallel to field lines",
        "description": "Student applies electric field intuition (F parallel to E) to magnetic force (which is perpendicular: F = q v x B).",
        "concept": "magnetic_force",
        "correction": "The mechanical force on a current conductor is perpendicular to both the current and the magnetic field lines (Fleming's Left-Hand Rule).",
        "challenge_idea": "If current flows along the field lines, how much magnetic force is exerted?",
        "reteach_action": "Kicking wire experiment: suspend a copper wire between poles of a horseshoe magnet and show it kicks perpendicular to both current and field.",
        "source": "Maloney et al. (2001 - CSEM)",
    },
    "M17": {
        "id": "M17", "chapter": "magnetism", "formal_code": "FIELD_DIRECTION",
        "label": "Confuses Left-Hand and Right-Hand rules for current and field",
        "description": "Student applies Fleming's Left-Hand Rule to straight wire field lines or Right-Hand Rule to motor force.",
        "concept": "magnetic_force",
        "correction": "Right-Hand Thumb Rule determines magnetic field created BY current. Fleming's Left-Hand Rule determines mechanical force ON current in an external field.",
        "challenge_idea": "Which rule tells you which way an electric motor armature will turn?",
        "reteach_action": "Mnemonic: 'FBI' (Force-Thumb, B-Field-Forefinger, I-Current-Middle) and Left Hand = Labour/Motor.",
        "source": "Bagno & Eylon (1997)",
    },
}

# -----------------------------------------------------------------------------
# 6. HELPER RETRIEVAL FUNCTIONS
# -----------------------------------------------------------------------------
def get_concept(cid: str) -> Optional[Dict[str, Any]]:
    """Retrieve concept metadata by ID (supports 20 concepts and 51 codes)."""
    if cid in CONCEPTS:
        return CONCEPTS[cid]
    if cid in CONCEPTS_51:
        return CONCEPTS_51[cid]
    return None

def get_misconception(mid: str) -> Optional[Dict[str, Any]]:
    """Retrieve misconception metadata by ID."""
    if mid in MISCONCEPTIONS:
        return MISCONCEPTIONS[mid]
    if mid in FORMAL_MISCONCEPTIONS:
        return FORMAL_MISCONCEPTIONS[mid]
    return None

def get_ordered_concepts(chapter_id: Optional[str] = None) -> List[str]:
    """Returns concept IDs sorted in recommended pedagogical order."""
    if chapter_id and chapter_id in CHAPTERS:
        cids = CHAPTERS[chapter_id]["concepts"]
        return sorted(cids, key=lambda c: CONCEPTS[c]["order"])
    return sorted(CONCEPTS.keys(), key=lambda c: CONCEPTS[c]["order"])

def get_chapter_for_concept(cid: str) -> Optional[str]:
    """Returns the chapter ID for a given concept ID."""
    c = get_concept(cid)
    return c.get("chapter") if c else None

def get_all_51_concepts() -> Dict[str, Dict[str, Any]]:
    """Returns the full 51-concept taxonomy dictionary."""
    return CONCEPTS_51

def check_prerequisite_cycles() -> bool:
    """
    Asserts that the prerequisite subgraph across all concepts is strictly acyclic (DAG).
    Blueprint requirement: 'Only the prerequisite subgraph must be acyclic.'
    """
    for pool in [CONCEPTS, CONCEPTS_51]:
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(cid: str) -> bool:
            visited.add(cid)
            rec_stack.add(cid)
            prereqs = pool.get(cid, {}).get("prerequisites", [])
            for p in prereqs:
                if p not in visited:
                    if dfs(p):
                        return True
                elif p in rec_stack:
                    raise ValueError(f"Graph cycle detected between {cid} and {p}!")
            rec_stack.remove(cid)
            return False

        for cid in pool:
            if cid not in visited:
                if dfs(cid):
                    return False
    return True

# Validate DAG acyclicity at import time
check_prerequisite_cycles()
