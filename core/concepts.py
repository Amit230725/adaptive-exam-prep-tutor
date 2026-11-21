"""core/concepts.py - Concept Graph & Research-Backed Misconception Library

Curriculum: Complete CBSE Class 10 Science Physics Syllabus (NCERT):
- Chapter 9: Light – Reflection and Refraction
- Chapter 10: The Human Eye and the Colourful World
- Chapter 11: Electricity
- Chapter 12: Magnetic Effects of Electric Current

Misconceptions: Published Physics Education Research (PER)
- Optics: Goldberg & McDermott (1987), Galili & Hazan (2000)
- Human Eye & Vision: Guesne (1985), Selley (1996)
- Circuits: McDermott & Shaffer (1992), Shipstone (1988), Engelhardt & Beichner (2004)
- Electromagnetism: Maloney, O'Kuma, Hieggelke & Van Heuvelen (2001 - CSEM)
"""

from typing import Dict, List, Optional, Any

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
        "description": "Spherical mirrors, mirror formula, refraction laws, Snell's law, spherical lenses, lens formula, and power of a lens.",
    },
    "human_eye": {
        "id": "human_eye",
        "name": "Chapter 10: The Human Eye & Colourful World",
        "short_name": "Human Eye",
        "icon": "👁️",
        "order": 2,
        "concepts": ["eye_vision", "defects_vision", "prism_dispersion", "atmospheric_scattering"],
        "description": "Structure of eye, power of accommodation, myopia & hypermetropia correction, prism dispersion, and atmospheric scattering.",
    },
    "electricity": {
        "id": "electricity",
        "name": "Chapter 11: Electricity",
        "short_name": "Electricity",
        "icon": "⚡",
        "order": 3,
        "concepts": ["charge", "current", "pd", "ohm", "resistance", "series", "parallel", "power"],
        "description": "Electric charge, current, potential difference, Ohm's law, resistance factors, series & parallel combinations, and Joule's heating.",
    },
    "magnetism": {
        "id": "magnetism",
        "name": "Chapter 12: Magnetic Effects of Electric Current",
        "short_name": "Magnetic Effects",
        "icon": "🧲",
        "order": 4,
        "concepts": ["magnetic_field", "current_magnetism", "magnetic_force", "domestic_circuits"],
        "description": "Magnetic field lines, Right-Hand Thumb Rule, circular loops, solenoids, Fleming's Left-Hand Rule, and domestic circuit safety.",
    },
}

# -----------------------------------------------------------------------------
# 2. FULL SYLLABUS CONCEPT GRAPH DEFINITIONS (20 Concepts)
# -----------------------------------------------------------------------------
CONCEPTS: Dict[str, Dict[str, Any]] = {
    # --- CHAPTER 9: LIGHT – REFLECTION AND REFRACTION ---
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
        "name": "Power of a Lens & Combinations",
        "chapter": "light",
        "prerequisites": ["refraction_lenses"],
        "order": 4,
        "description": "Degree of convergence/divergence, power P = 1/f (in meters), unit Dioptre (D), algebraic combination of thin lenses P = P1 + P2.",
    },

    # --- CHAPTER 10: THE HUMAN EYE AND THE COLOURFUL WORLD ---
    "eye_vision": {
        "id": "eye_vision",
        "name": "Human Eye & Accommodation",
        "chapter": "human_eye",
        "prerequisites": ["refraction_lenses"],
        "order": 5,
        "description": "Structure of eye (cornea, iris, pupil, crystalline lens, ciliary muscles, retina), power of accommodation, near point (25 cm) and far point (infinity).",
    },
    "defects_vision": {
        "id": "defects_vision",
        "name": "Defects of Vision & Lens Correction",
        "chapter": "human_eye",
        "prerequisites": ["eye_vision", "refraction_lenses"],
        "order": 6,
        "description": "Myopia (near-sightedness, corrected by concave lens), Hypermetropia (far-sightedness, corrected by convex lens), and Presbyopia (bifocal lenses).",
    },
    "prism_dispersion": {
        "id": "prism_dispersion",
        "name": "Prism Refraction & Dispersion",
        "chapter": "human_eye",
        "prerequisites": ["refraction_laws"],
        "order": 7,
        "description": "Refraction through glass prism, angle of deviation, dispersion of white light into spectrum (VIBGYOR), inverted prism recombination, rainbow formation.",
    },
    "atmospheric_scattering": {
        "id": "atmospheric_scattering",
        "name": "Atmospheric Refraction & Scattering",
        "chapter": "human_eye",
        "prerequisites": ["refraction_laws", "prism_dispersion"],
        "order": 8,
        "description": "Optical density gradient in atmosphere; twinkling of stars, advanced sunrise and delayed sunset, Tyndall effect, blue sky, reddish sun at sunrise/sunset.",
    },

    # --- CHAPTER 11: ELECTRICITY ---
    "charge": {
        "id": "charge",
        "name": "Electric Charge & Quantisation",
        "chapter": "electricity",
        "prerequisites": [],
        "order": 9,
        "description": "Quantisation of charge (Q = n*e), SI unit Coulomb (C), electrons as mobile carriers in metallic conductors.",
    },
    "current": {
        "id": "current",
        "name": "Electric Current & Flow Rate",
        "chapter": "electricity",
        "prerequisites": ["charge"],
        "order": 10,
        "description": "Rate of flow of charge (I = Q/t), SI unit Ampere (A), measured by ammeter in series, conservation of charge.",
    },
    "pd": {
        "id": "pd",
        "name": "Potential Difference & Voltage",
        "chapter": "electricity",
        "prerequisites": ["charge"],
        "order": 11,
        "description": "Work done per unit charge (V = W/Q), SI unit Volt (V), role of cell in maintaining electrical pressure, measured by voltmeter in parallel.",
    },
    "ohm": {
        "id": "ohm",
        "name": "Ohm's Law & V-I Characteristics",
        "chapter": "electricity",
        "prerequisites": ["current", "pd"],
        "order": 12,
        "description": "Linear relationship V = I*R at constant temperature; V-I characteristic curve and resistance as constant slope.",
    },
    "resistance": {
        "id": "resistance",
        "name": "Resistance & Material Factors",
        "chapter": "electricity",
        "prerequisites": ["ohm"],
        "order": 13,
        "description": "Opposition to electron drift; dependence on length, area, resistivity (R = rho*l/A); distinction between R and V/I.",
    },
    "series": {
        "id": "series",
        "name": "Series Circuits & Voltage Division",
        "chapter": "electricity",
        "prerequisites": ["resistance"],
        "order": 14,
        "description": "Single conductive path: identical current throughout (I_tot = I1 = I2), voltage divides (V_tot = V1 + V2), equivalent resistance R_s = R1 + R2.",
    },
    "parallel": {
        "id": "parallel",
        "name": "Parallel Circuits & Current Splitting",
        "chapter": "electricity",
        "prerequisites": ["resistance"],
        "order": 15,
        "description": "Multiple branches: identical voltage across branches (V_tot = V1 = V2), current divides inversely by resistance, 1/R_p = 1/R1 + 1/R2.",
    },
    "power": {
        "id": "power",
        "name": "Electric Power & Joule's Heating",
        "chapter": "electricity",
        "prerequisites": ["ohm"],
        "order": 16,
        "description": "Rate of electrical energy dissipation (P = V*I = I^2*R = V^2/R), Watt (W), Joule's heating law (H = I^2*R*t), bulb brightness.",
    },

    # --- CHAPTER 12: MAGNETIC EFFECTS OF ELECTRIC CURRENT ---
    "magnetic_field": {
        "id": "magnetic_field",
        "name": "Magnetic Field & Field Lines",
        "chapter": "magnetism",
        "prerequisites": [],
        "order": 17,
        "description": "Magnetic field around a bar magnet, properties of field lines (closed continuous loops, North to South externally, never intersect, density indicates field strength).",
    },
    "current_magnetism": {
        "id": "current_magnetism",
        "name": "Magnetic Field Due to Current",
        "chapter": "magnetism",
        "prerequisites": ["current", "magnetic_field"],
        "order": 18,
        "description": "Oersted's discovery; field due to straight conductor, Right-Hand Thumb Rule, circular loop, and solenoid as an electromagnet.",
    },
    "magnetic_force": {
        "id": "magnetic_force",
        "name": "Magnetic Force & Fleming's Left-Hand Rule",
        "chapter": "magnetism",
        "prerequisites": ["current_magnetism"],
        "order": 19,
        "description": "Force experienced by current-carrying conductor in external magnetic field (F = B*I*L); Fleming's Left-Hand Rule (Thumb: Force, Forefinger: Field, Middle: Current).",
    },
    "domestic_circuits": {
        "id": "domestic_circuits",
        "name": "Domestic Circuits & Safety Devices",
        "chapter": "magnetism",
        "prerequisites": ["power", "series", "parallel", "magnetic_force"],
        "order": 20,
        "description": "Domestic AC wiring (Live 220 V, Neutral 0 V, Earth wire), parallel appliance connections, electric fuse rating, short-circuiting, and overloading safety.",
    },
}

# -----------------------------------------------------------------------------
# 3. RESEARCH-BACKED MISCONCEPTION LIBRARY (FIXED IDs: M1 - M17)
# -----------------------------------------------------------------------------
# Derived from published Physics Education Research (PER).
# AI and rule engines MUST ONLY reference these exact IDs. Never invent labels.

MISCONCEPTIONS: Dict[str, Dict[str, str]] = {
    # --- ELECTRICITY (M1 - M7) ---
    "M1": {
        "id": "M1",
        "chapter": "electricity",
        "label": "Current is used up as it passes through a component",
        "description": "The student believes electrical current decreases downstream after passing through bulbs or resistors.",
        "correction": "Electric charge is conserved. Current is the rate of charge flow and remains identical before and after any component in a single path.",
        "challenge_idea": "Two ammeters placed on either side of a single high-resistance bulb.",
        "reteach_action": "Use PhET circuit simulation with ammeters before and after a bulb to visually prove identical flow rates.",
    },
    "M2": {
        "id": "M2",
        "chapter": "electricity",
        "label": "Battery is a constant-current source",
        "description": "The student assumes a battery pushes the exact same amperes regardless of what circuit is connected.",
        "correction": "A battery maintains a constant potential difference across its terminals; the current it delivers depends strictly on total circuit resistance (I = V/R).",
        "challenge_idea": "Compare total current from the same 6 V battery when connected to 10 ohms vs 100 ohms.",
        "reteach_action": "Demonstrate with real multimeter: measure current when adding resistors in series vs parallel to the same battery.",
    },
    "M3": {
        "id": "M3",
        "chapter": "electricity",
        "label": "Confuses current, voltage, and/or electrical energy",
        "description": "The student mixes up the roles of voltage (push/energy per charge), current (rate of flow), and power/energy (Joules/Watts).",
        "correction": "Voltage is the electrical pressure (Joules per Coulomb), current is the traffic flow rate (Coulombs per second), and energy is the total work done.",
        "challenge_idea": "A circuit with high voltage but zero current (open switch) vs high current at low voltage.",
        "reteach_action": "Use water-pipe analogy: pump pressure = voltage, pipe water flow rate = current, water turbine work = energy transferred.",
    },
    "M4": {
        "id": "M4",
        "chapter": "electricity",
        "label": "Battery creates or stores charge that gets exhausted",
        "description": "The student believes the battery physically contains mobile charges that run out, or that the battery generates electrons.",
        "correction": "The mobile electrons already exist throughout the metal wires and components. The battery only supplies the chemical energy to circulate them.",
        "challenge_idea": "Explain why a circuit doesn't fill up with electrons at one end while emptying at the other.",
        "reteach_action": "Bicycle-chain model: the chain links (electrons) are already there; the pedals (battery) only push the loop.",
    },
    "M5": {
        "id": "M5",
        "chapter": "electricity",
        "label": "Adding resistors in parallel increases total resistance",
        "description": "The student applies series intuition (more components = more resistance) to parallel branches.",
        "correction": "Adding parallel branches creates additional paths for current to flow, increasing total conductance and decreasing equivalent resistance.",
        "challenge_idea": "Calculate equivalent resistance of two 6 ohm resistors in parallel vs one alone.",
        "reteach_action": "Toll-booth analogy: opening more parallel toll gates speeds up traffic flow, lowering the overall obstruction.",
    },
    "M6": {
        "id": "M6",
        "chapter": "electricity",
        "label": "Resistance depends on applied voltage or current",
        "description": "The student misinterprets R = V/I as a causal relationship, believing altering V changes the material resistance.",
        "correction": "Resistance of an ohmic conductor is an intrinsic property determined by resistivity, length, and area (R = rho*l/A); it does not change when V or I changes.",
        "challenge_idea": "What is the resistance of a 10 ohm resistor when disconnected from any circuit (V = 0)?",
        "reteach_action": "Plot V vs I experimentally for a resistor. Show that the slope R remains constant across different voltages.",
    },
    "M7": {
        "id": "M7",
        "chapter": "electricity",
        "label": "In parallel, current splits equally regardless of resistance",
        "description": "The student assumes parallel branches always divide total current equally (50/50), ignoring differing branch resistances.",
        "correction": "Current in parallel branches divides inversely proportional to branch resistance (I_branch = V / R_branch); the path of lower resistance carries more current.",
        "challenge_idea": "Calculate branch currents for 2 ohms and 10 ohms in parallel connected to a 10 V battery.",
        "reteach_action": "Dual-pipe drainage demo: a wider pipe drains significantly more water per second than a narrow pipe under equal head pressure.",
    },

    # --- LIGHT: REFLECTION & REFRACTION (M8 - M11) ---
    "M8": {
        "id": "M8",
        "chapter": "light",
        "label": "Image is located on the surface of the mirror/lens",
        "description": "The student believes an optical image resides physically on the glass face rather than at the ray convergence/divergence point in space.",
        "correction": "An image is formed where reflected or refracted light rays physically intersect (real image) or appear to diverge from (virtual image), located in front or behind the optical element.",
        "challenge_idea": "Place a screen at various distances in front of a concave mirror to locate the sharp image plane.",
        "reteach_action": "Ray-box optical bench demonstration: project real image onto paper screen to prove image location depends on object distance.",
    },
    "M9": {
        "id": "M9",
        "chapter": "light",
        "label": "Covering half a lens cuts the image in half",
        "description": "The student assumes each half of a lens forms a corresponding half of the image, so blocking one half removes half the image.",
        "correction": "Every portion of a lens receives light rays from every point of the object and forms a complete image. Covering half the lens only reduces brightness by half.",
        "challenge_idea": "Cover the top half of a convex lens with black paper and observe the screen image of a candle flame.",
        "reteach_action": "Classroom demo: cover half a projector lens with cardboard; observe that full slide remains visible, only slightly dimmer.",
    },
    "M10": {
        "id": "M10",
        "chapter": "light",
        "label": "Focal length varies with object position or image distance",
        "description": "The student treats focal length f as a variable dependent on where the object is placed (u) or where the image forms (v).",
        "correction": "Focal length is a geometric constant of a spherical mirror or lens determined solely by its radius of curvature (f = R/2) and refractive index.",
        "challenge_idea": "Calculate focal length of a concave mirror when object is at 20 cm vs 40 cm.",
        "reteach_action": "Measure radius of curvature with spherometer and show that f remains strictly invariant regardless of object distance.",
    },
    "M11": {
        "id": "M11",
        "chapter": "light",
        "label": "Light slows down or stops as it travels further in air",
        "description": "The student believes light rays lose speed or run out of distance energy simply by traveling across empty air.",
        "correction": "Light propagates at a constant speed c (approx 3 × 10^8 m/s in vacuum/air). Its intensity decreases with distance (inverse-square law), but speed remains strictly constant.",
        "challenge_idea": "Compare the speed of laser light 1 meter from source vs 100 meters away in air.",
        "reteach_action": "Distinguish between photon speed (constant medium property) and luminous intensity (geometric divergence over area).",
    },

    # --- HUMAN EYE & COLOURFUL WORLD (M12 - M14) ---
    "M12": {
        "id": "M12",
        "chapter": "human_eye",
        "label": "Confuses myopia with hypermetropia (or prescribes convex lens for myopia)",
        "description": "The student mixes up short-sightedness and far-sightedness, or reverses the corrective concave vs convex lenses.",
        "correction": "Myopia (near-sightedness: image forms in front of retina due to excessive eye convergence) is corrected by a diverging concave lens. Hypermetropia is corrected by a converging convex lens.",
        "challenge_idea": "A student cannot read the blackboard from the last bench. What defect is this and which lens corrects it?",
        "reteach_action": "Draw side-by-side eyeball ray diagrams: show eyeball elongation in myopia and how a concave lens diverges rays to focus onto retina.",
    },
    "M13": {
        "id": "M13",
        "chapter": "human_eye",
        "label": "Believes the eye sees by projecting active vision rays outwards",
        "description": "The student holds the historical extramission belief that vision occurs by the eye sending out visual rays to illuminate objects.",
        "correction": "Vision occurs strictly by intromission: external light reflected from an object enters the pupil and is focused onto the photosensitive retina.",
        "challenge_idea": "Explain why we cannot see anything in a completely lightless room even if our eyes are wide open.",
        "reteach_action": "Dark room demonstration: show that sight is impossible without incoming photons striking the retinal rod and cone cells.",
    },
    "M14": {
        "id": "M14",
        "chapter": "human_eye",
        "label": "Believes a prism dyes or creates colors in white light",
        "description": "The student thinks the glass material produces colored light rather than dispersing wavelengths already present in white light.",
        "correction": "White light is a polychromatic mixture of all visible wavelengths. A prism only disperses them because glass has a different refractive index for each wavelength.",
        "challenge_idea": "Newton's classic experiment: recombine dispersed spectrum with an identical inverted prism.",
        "reteach_action": "Recombine rainbow spectrum using second inverted prism to recover pure white light, proving prism does not create color.",
    },

    # --- MAGNETIC EFFECTS (M15 - M17) ---
    "M15": {
        "id": "M15",
        "chapter": "magnetism",
        "label": "Believes cutting a magnet in half isolates north and south monopoles",
        "description": "The student believes severing a bar magnet leaves one piece purely North and the other piece purely South.",
        "correction": "Isolated magnetic monopoles do not exist in nature. Cutting a magnet creates two smaller complete dipoles, each with its own North and South poles.",
        "challenge_idea": "If a bar magnet of pole strength m is broken into two equal halves, what are the poles on each half?",
        "reteach_action": "Magnetic domain model: show alignment of microscopic atomic magnetic dipoles within ferromagnetic material.",
    },
    "M16": {
        "id": "M16",
        "chapter": "magnetism",
        "label": "Confuses Fleming's Left-Hand Rule with Right-Hand Rule",
        "description": "The student applies the Left-Hand rule (motor / force) to electromagnetic induction or Right-Hand rule to motor torque.",
        "correction": "Fleming's Left-Hand Rule is for motors (predicts direction of mechanical Force given Field and Current). Fleming's Right-Hand Rule is for generators (predicts Induced Current).",
        "challenge_idea": "Which rule determines the deflection of a current-carrying wire placed in a perpendicular magnetic field?",
        "reteach_action": "Mnemonic: 'FBI' (Force-Thumb, B-Field-Forefinger, I-Current-Middle) and Left Hand = Labour/Motor, Right Hand = Receive/Generator.",
    },
    "M17": {
        "id": "M17",
        "chapter": "magnetism",
        "label": "Believes magnetic field lines can cross each other in strong fields",
        "description": "The student assumes high magnetic field intensity causes adjacent field lines to intersect or overlap.",
        "correction": "Magnetic field lines can NEVER intersect. If they crossed, a magnetic compass needle at the intersection would point in two contradictory directions simultaneously, which is physically impossible.",
        "challenge_idea": "What would a compass needle do if placed at an intersection point of two magnetic field lines?",
        "reteach_action": "Iron filings demo with two like poles facing each other: show field lines repelling and bending away, never intersecting.",
    },
}

# -----------------------------------------------------------------------------
# 4. HELPER RETRIEVAL FUNCTIONS
# -----------------------------------------------------------------------------
def get_concept(cid: str) -> Optional[Dict[str, Any]]:
    """Retrieve concept metadata by ID."""
    return CONCEPTS.get(cid)

def get_misconception(mid: str) -> Optional[Dict[str, Any]]:
    """Retrieve misconception metadata by ID."""
    return MISCONCEPTIONS.get(mid)

def get_ordered_concepts(chapter_id: Optional[str] = None) -> List[str]:
    """
    Returns concept IDs sorted in recommended pedagogical order.
    Optionally filters by specific chapter.
    """
    if chapter_id and chapter_id in CHAPTERS:
        cids = CHAPTERS[chapter_id]["concepts"]
        return sorted(cids, key=lambda c: CONCEPTS[c]["order"])
    return sorted(CONCEPTS.keys(), key=lambda c: CONCEPTS[c]["order"])

def get_chapter_for_concept(cid: str) -> Optional[str]:
    """Returns the chapter ID for a given concept ID."""
    c = CONCEPTS.get(cid)
    return c.get("chapter") if c else None
