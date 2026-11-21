"""core/bank.py - Verified CBSE Class 10 Science Question Bank (60 Items)

Covers the entire CBSE Class 10 Science Physics Syllabus (NCERT):
- Chapter 9: Light – Reflection & Refraction (12 items)
- Chapter 10: The Human Eye & Colourful World (12 items)
- Chapter 11: Electricity (24 items)
- Chapter 12: Magnetic Effects of Electric Current (12 items)

Each concept contains 3 calibrated questions:
- Level 1: Foundational knowledge / definition / direct application
- Level 2: Numerical reasoning / multi-step circuit or optical analysis
- Level 3: Conceptual synthesis / counter-intuitive non-obvious scenarios

Each distractor is explicitly mapped to the research misconception it triggers (M1 - M17) or None.
"""

from typing import List, Dict, Any, Optional
from core.concepts import CHAPTERS

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
    # CHAPTER 9: LIGHT – REFLECTION AND REFRACTION (12 Items)
    # =========================================================================

    # --- CONCEPT 1: SPHERICAL MIRRORS & REFLECTION (reflection_mirrors) ---
    Item(
        item_id="q_lgt_mir_01",
        concept="reflection_mirrors",
        difficulty_label=1,
        question="What is the focal length of a spherical concave mirror whose radius of curvature is 30 cm?",
        options=[
            "15 cm; focal length is half the radius of curvature (f = R/2)",
            "60 cm; focal length is twice the radius of curvature (f = 2R)",
            "30 cm; focal length equals radius of curvature for spherical mirrors",
            "Variable; focal length changes depending on where the object is placed",
        ],
        answer_index=0,
        tags=[None, "M10", None, "M10"],
        explanation="For spherical mirrors of small aperture, the focal length is half its radius of curvature: f = R/2 = 30 / 2 = 15 cm. It is a fixed geometric constant of the mirror.",
        source_note="NCERT Class 10 Science, Chapter 9, Section 9.2.1; Spherical Mirrors.",
    ),
    Item(
        item_id="q_lgt_mir_02",
        concept="reflection_mirrors",
        difficulty_label=2,
        question="An object is placed at a distance of 20 cm in front of a concave mirror of focal length 15 cm. At what distance from the mirror will a sharp image be formed on a screen?",
        options=[
            "60 cm in front of the mirror (real and inverted image)",
            "On the mirror's silvered surface (virtual image plane)",
            "60 cm behind the mirror (virtual and erect image)",
            "8.57 cm in front of the mirror",
        ],
        answer_index=0,
        tags=[None, "M8", "M10", None],
        explanation="Using mirror formula 1/v + 1/u = 1/f with Cartesian sign convention: u = -20 cm, f = -15 cm. 1/v = 1/(-15) - 1/(-20) = -1/15 + 1/20 = (-4 + 3)/60 = -1/60 ==> v = -60 cm. The negative sign denotes a real image formed 60 cm in front of the reflecting surface.",
        source_note="NCERT Class 10 Science, Chapter 9, Example 9.1; Mirror Formula.",
    ),
    Item(
        item_id="q_lgt_mir_03",
        concept="reflection_mirrors",
        difficulty_label=3,
        question="Why are convex mirrors universally preferred as rear-view (wing) mirrors in automobiles?",
        options=[
            "They always form an erect, virtual, and diminished image, giving a much wider field of view",
            "They converge parallel light rays to focus real images directly on the mirror surface",
            "They magnify distant vehicles so the driver can inspect fine details",
            "They eliminate reflection blind spots by bending light rays around obstacles",
        ],
        answer_index=0,
        tags=[None, "M8", "M10", None],
        explanation="Convex mirrors are curved outwards. They always produce an erect and diminished virtual image regardless of object position, giving the driver a significantly wider field of view than a plane or concave mirror.",
        source_note="NCERT Class 10 Science, Chapter 9, Section 9.2.3; Uses of Convex Mirrors.",
    ),

    # --- CONCEPT 2: REFRACTION OF LIGHT & SNELL'S LAW (refraction_laws) ---
    Item(
        item_id="q_lgt_refr_01",
        concept="refraction_laws",
        difficulty_label=1,
        question="What happens to a ray of light when it travels obliquely from air (optically rarer) into glass (optically denser)?",
        options=[
            "It slows down and bends towards the normal",
            "It speeds up and bends away from the normal",
            "It bends towards the normal because light loses energy with distance",
            "It continues straight without deviation because glass is transparent",
        ],
        answer_index=0,
        tags=[None, None, "M11", None],
        explanation="When light enters an optically denser medium like glass from air, its speed decreases. Consequently, according to Snell's law, the refracted ray bends towards the normal (angle of refraction r < angle of incidence i).",
        source_note="NCERT Class 10 Science, Chapter 9, Section 9.3; Refraction of Light.",
    ),
    Item(
        item_id="q_lgt_refr_02",
        concept="refraction_laws",
        difficulty_label=2,
        question="The absolute refractive index of diamond is 2.42. If the speed of light in vacuum is 3.0 × 10^8 m/s, what is the speed of light in diamond?",
        options=[
            "1.24 × 10^8 m/s; v = c / n",
            "7.26 × 10^8 m/s; v = c × n",
            "3.00 × 10^8 m/s; speed of light is invariant across all transparent media",
            "0.81 × 10^8 m/s; v = n / c",
        ],
        answer_index=0,
        tags=[None, None, "M11", None],
        explanation="Refractive index is defined as n = c / v. Therefore, speed of light in diamond is v = c / n = (3.0 × 10^8 m/s) / 2.42 ≈ 1.24 × 10^8 m/s.",
        source_note="NCERT Class 10 Science, Chapter 9, Section 9.3.2; Refractive Index.",
    ),
    Item(
        item_id="q_lgt_refr_03",
        concept="refraction_laws",
        difficulty_label=3,
        question="A ray of light enters a rectangular glass slab obliquely and emerges out into air. Which statement describes the emergent ray?",
        options=[
            "The emergent ray is parallel to the incident ray but laterally displaced",
            "The emergent ray converges to a focal point on the bottom face of the slab",
            "The emergent ray bends permanently at 90 degrees to the incident path",
            "The emergent ray loses speed continuously as it leaves the slab",
        ],
        answer_index=0,
        tags=[None, "M8", None, "M11"],
        explanation="At the first air-glass interface, light bends towards normal. At the second glass-air interface, light bends away from normal by an equal and opposite angle. Hence, the emergent ray is strictly parallel to the incident ray, shifted sideways by lateral displacement.",
        source_note="NCERT Class 10 Science, Chapter 9, Section 9.3.1; Refraction through a Glass Slab.",
    ),

    # --- CONCEPT 3: SPHERICAL LENSES & RAY OPTICS (refraction_lenses) ---
    Item(
        item_id="q_lgt_len_01",
        concept="refraction_lenses",
        difficulty_label=1,
        question="Where should an object be placed in front of a convex lens to obtain a real image of the same size as the object?",
        options=[
            "At twice the focal length (at 2F1)",
            "At the principal focus (at F1)",
            "Between the optical centre and principal focus",
            "At infinity",
        ],
        answer_index=0,
        tags=[None, None, "M8", None],
        explanation="When an object is placed at 2F1 of a convex lens, a real, inverted image of exactly the same size (magnification m = -1) is formed at 2F2 on the other side.",
        source_note="NCERT Class 10 Science, Chapter 9, Table 9.4; Image Formation by Convex Lenses.",
    ),
    Item(
        item_id="q_lgt_len_02",
        concept="refraction_lenses",
        difficulty_label=2,
        question="An object is placed 30 cm in front of a convex lens of focal length 20 cm. What are the image distance and magnification?",
        options=[
            "v = +60 cm; magnification m = -2 (real, inverted, enlarged)",
            "v = -12 cm; magnification m = +0.4 (virtual, erect)",
            "v = +12 cm; magnification m = -0.4 (real, inverted)",
            "v = +60 cm; but only the top half of the image forms",
        ],
        answer_index=0,
        tags=[None, None, None, "M9"],
        explanation="Using lens formula 1/v - 1/u = 1/f: u = -30 cm, f = +20 cm. 1/v = 1/f + 1/u = 1/20 + 1/(-30) = (3 - 2)/60 = 1/60 ==> v = +60 cm. Magnification m = v / u = 60 / (-30) = -2.",
        source_note="NCERT Class 10 Science, Chapter 9, Example 9.3; Lens Formula and Magnification.",
    ),
    Item(
        item_id="q_lgt_len_03",
        concept="refraction_lenses",
        difficulty_label=3,
        question="One-half of a convex lens is covered with black paper while forming an image of an illuminated candle on a screen. What will happen to the image?",
        options=[
            "A complete image of the candle is still formed, but its brightness is reduced",
            "The upper half of the candle image disappears completely",
            "The lower half of the candle image disappears completely",
            "The image vanishes entirely because half a lens cannot refract light",
        ],
        answer_index=0,
        tags=[None, "M9", "M9", "M9"],
        explanation="Every portion of a lens refracts light rays coming from all parts of the object to form a complete image. Covering half the lens reduces the light-gathering area by 50%, resulting in a complete image of half the original intensity (brightness).",
        source_note="NCERT Class 10 Science, Chapter End Exercise 9; Classic PER Optics Probe.",
    ),

    # --- CONCEPT 4: POWER OF A LENS & COMBINATIONS (lens_power) ---
    Item(
        item_id="q_lgt_pow_01",
        concept="lens_power",
        difficulty_label=1,
        question="An optician prescribes a corrective lens of power -2.0 D. What is its focal length and lens type?",
        options=[
            "-0.50 m (-50 cm); concave (diverging) lens",
            "+0.50 m (+50 cm); convex (converging) lens",
            "-2.0 m (-200 cm); concave (diverging) lens",
            "+2.0 m (+200 cm); convex (converging) lens",
        ],
        answer_index=0,
        tags=[None, "M12", None, None],
        explanation="Power P = 1 / f(in meters). Thus f = 1 / P = 1 / (-2.0 D) = -0.50 m = -50 cm. A negative focal length corresponds strictly to a concave (diverging) lens.",
        source_note="NCERT Class 10 Science, Chapter 9, Section 9.3.8; Power of a Lens.",
    ),
    Item(
        item_id="q_lgt_pow_02",
        concept="lens_power",
        difficulty_label=2,
        question="Two thin lenses of powers +3.5 D and -1.5 D are placed in close contact. What is the net power and focal length of the combination?",
        options=[
            "Power = +2.0 D; focal length = +50 cm (converging)",
            "Power = +5.0 D; focal length = +20 cm (converging)",
            "Power = -2.0 D; focal length = -50 cm (diverging)",
            "Power = -5.25 D; focal length = -19 cm",
        ],
        answer_index=0,
        tags=[None, None, "M12", None],
        explanation="For thin lenses in contact, net power is algebraic sum: P = P1 + P2 = +3.5 D + (-1.5 D) = +2.0 D. Net focal length f = 1 / P = 1 / 2.0 = +0.50 m = +50 cm.",
        source_note="NCERT Class 10 Science, Chapter 9, Section 9.3.8; Lens Combinations.",
    ),
    Item(
        item_id="q_lgt_pow_03",
        concept="lens_power",
        difficulty_label=3,
        question="A convex lens of focal length 25 cm and a concave lens of focal length 50 cm are kept in contact. What is the power of the combination?",
        options=[
            "+2.0 D; P1 = +4.0 D and P2 = -2.0 D, so P_net = +4.0 - 2.0 = +2.0 D",
            "+6.0 D; powers always add in magnitude regardless of lens type",
            "-2.0 D; diverging effect always dominates converging lenses in contact",
            "+0.06 D; calculated directly from centimeter units without conversion",
        ],
        answer_index=0,
        tags=[None, None, "M12", None],
        explanation="P1 = 1 / f1(m) = 1 / 0.25 = +4.0 D. P2 = 1 / f2(m) = 1 / (-0.50) = -2.0 D. Net power P = P1 + P2 = +4.0 - 2.0 = +2.0 D.",
        source_note="NCERT Class 10 Science, Exemplar Physics Problems; Lens Power Combinations.",
    ),

    # =========================================================================
    # CHAPTER 10: THE HUMAN EYE AND THE COLOURFUL WORLD (12 Items)
    # =========================================================================

    # --- CONCEPT 5: HUMAN EYE & ACCOMMODATION (eye_vision) ---
    Item(
        item_id="q_eye_str_01",
        concept="eye_vision",
        difficulty_label=1,
        question="What is the near point of distinct vision and far point for a young adult with normal vision?",
        options=[
            "Near point = 25 cm; Far point = infinity",
            "Near point = 10 cm; Far point = 100 meters",
            "Near point = 0 cm; Far point = infinity",
            "Near point = 25 cm; Far point = 25 meters",
        ],
        answer_index=0,
        tags=[None, None, "M8", None],
        explanation="For a normal human eye, the least distance of distinct vision (near point) is approximately 25 cm, and the far point is at infinity.",
        source_note="NCERT Class 10 Science, Chapter 10, Section 10.1; The Human Eye.",
    ),
    Item(
        item_id="q_eye_str_02",
        concept="eye_vision",
        difficulty_label=2,
        question="How does the human eye adjust to clearly view objects at varying distances?",
        options=[
            "Ciliary muscles modify the curvature of the crystalline lens (power of accommodation)",
            "The eye projects vision rays outwards with greater intensity towards distant objects",
            "The retina moves mechanically back and forth inside the eyeball",
            "The pupil contracts to slow down incoming light from distant sources",
        ],
        answer_index=0,
        tags=[None, "M13", None, "M11"],
        explanation="The ability of the eye lens to adjust its focal length via contraction or relaxation of ciliary muscles is called accommodation. When ciliary muscles contract, the lens becomes thicker, decreasing focal length for nearby objects.",
        source_note="NCERT Class 10 Science, Chapter 10, Section 10.1.1; Power of Accommodation.",
    ),
    Item(
        item_id="q_eye_str_03",
        concept="eye_vision",
        difficulty_label=3,
        question="When a person views a distant tree, the ciliary muscles are relaxed. What happens to the lens curvature and focal length?",
        options=[
            "The lens becomes thin, and its focal length increases to focus parallel rays on the retina",
            "The lens becomes thick, and its focal length decreases to converge rays quickly",
            "The lens projects active visual rays towards the distant foliage",
            "The lens curvature remains rigid and unchanged throughout life",
        ],
        answer_index=0,
        tags=[None, None, "M13", None],
        explanation="When ciliary muscles are relaxed, tension on suspensory ligaments pulls the flexible eye lens thin. This increases its focal length, allowing parallel rays from distant objects to converge precisely onto the retina.",
        source_note="NCERT Class 10 Science, Chapter 10, Section 10.1.1; Accommodation Mechanism.",
    ),

    # --- CONCEPT 6: DEFECTS OF VISION & LENS CORRECTION (defects_vision) ---
    Item(
        item_id="q_eye_def_01",
        concept="defects_vision",
        difficulty_label=1,
        question="A student sitting on the last bench cannot read the blackboard clearly, but reads her textbook easily. Name the defect and the corrective lens.",
        options=[
            "Myopia (near-sightedness); corrected by a concave lens",
            "Hypermetropia (far-sightedness); corrected by a convex lens",
            "Myopia (near-sightedness); corrected by a convex lens",
            "Presbyopia; corrected by a cylindrical lens",
        ],
        answer_index=0,
        tags=[None, "M12", "M12", None],
        explanation="A person who sees nearby objects clearly but cannot see distant objects distinctly suffers from myopia (near-sightedness). It is corrected using a concave (diverging) lens of suitable power.",
        source_note="NCERT Class 10 Science, Chapter 10, Section 10.2.1; Myopia.",
    ),
    Item(
        item_id="q_eye_def_02",
        concept="defects_vision",
        difficulty_label=2,
        question="The near point of a hypermetropic eye is 75 cm. What is the focal length and type of lens needed to read comfortably at 25 cm?",
        options=[
            "+37.5 cm (convex lens of power +2.67 D)",
            "-37.5 cm (concave lens of power -2.67 D)",
            "+50.0 cm (convex lens of power +2.0 D)",
            "-75.0 cm (concave lens of power -1.33 D)",
        ],
        answer_index=0,
        tags=[None, "M12", None, "M12"],
        explanation="To see an object placed at u = -25 cm, the corrective lens must form a virtual image at the person's near point v = -75 cm. 1/f = 1/v - 1/u = 1/(-75) - 1/(-25) = -1/75 + 3/75 = 2/75 ==> f = +37.5 cm. Power P = 1 / 0.375 = +2.67 D (convex lens).",
        source_note="NCERT Class 10 Science, Chapter 10, Example 10.2; Hypermetropia Correction.",
    ),
    Item(
        item_id="q_eye_def_03",
        concept="defects_vision",
        difficulty_label=3,
        question="Why does an uncorrected myopic eye fail to form a sharp image of distant objects on the retina?",
        options=[
            "Excessive curvature of the lens or elongation of the eyeball focuses rays in front of the retina",
            "The image is formed on the cornea surface rather than reaching the retina",
            "The eyeball is too short, focusing rays behind the retina",
            "The eye fails to project visual rays far enough to reach the object",
        ],
        answer_index=0,
        tags=[None, "M8", "M12", "M13"],
        explanation="In a myopic eye, due to excessive cornea/lens curvature or an elongated eyeball, parallel light rays from infinity converge to a focus in FRONT of the retina. A diverging concave lens pushes the focal point back onto the retina.",
        source_note="NCERT Class 10 Science, Chapter 10, Section 10.2.1; Causes of Myopia.",
    ),

    # --- CONCEPT 7: PRISM REFRACTION & DISPERSION (prism_dispersion) ---
    Item(
        item_id="q_eye_prs_01",
        concept="prism_dispersion",
        difficulty_label=1,
        question="When white light passes through a glass prism, it splits into a band of seven colors. What is this phenomenon called, and which color bends the most?",
        options=[
            "Dispersion; Violet bends the most",
            "Total internal reflection; Red bends the most",
            "Dispersion; Red bends the most because glass creates red light",
            "Atmospheric scattering; Green bends the most",
        ],
        answer_index=0,
        tags=[None, None, "M14", None],
        explanation="The phenomenon of splitting of white light into its constituent colors is called dispersion. Violet light has the shortest visible wavelength, travels slowest in glass, experiences the highest refractive index, and therefore bends the most.",
        source_note="NCERT Class 10 Science, Chapter 10, Section 10.3; Refraction of Light through a Prism.",
    ),
    Item(
        item_id="q_eye_prs_02",
        concept="prism_dispersion",
        difficulty_label=2,
        question="Why do different colors of white light deviate at different angles when passing through a triangular glass prism?",
        options=[
            "Different colors have different wavelengths and travel at different speeds in glass",
            "The prism material dyes and injects chemical colors into the white beam",
            "Violet light slows down because it runs out of distance energy faster than red light",
            "Colors reflect off internal mirrors embedded inside the prism faces",
        ],
        answer_index=0,
        tags=[None, "M14", "M11", None],
        explanation="All visible colors travel at the same speed in vacuum. However, in a transparent dispersive medium like glass, red light travels fastest and bends least, while violet travels slowest and bends most (n_violet > n_red).",
        source_note="NCERT Class 10 Science, Chapter 10, Section 10.3.1; Dispersion Mechanism.",
    ),
    Item(
        item_id="q_eye_prs_03",
        concept="prism_dispersion",
        difficulty_label=3,
        question="In Isaac Newton's landmark experiment, a second identical prism was placed in an inverted position after the first prism. What emerged from the second prism?",
        options=[
            "A beam of pure white light, proving the prism does not create colors but only separates them",
            "A doubled spectrum with 14 distinct color bands",
            "Complete darkness because the second prism absorbed all light wavelengths",
            "Only monochromatic green light remained after crossing both prisms",
        ],
        answer_index=0,
        tags=[None, "M14", None, "M14"],
        explanation="Newton passed white light through a prism to disperse it, then placed a second identical prism inverted. The second prism recombined the seven colors back into a single white beam, conclusively proving that white light contains all spectral colors and the glass prism does not generate colors itself.",
        source_note="NCERT Class 10 Science, Chapter 10, Section 10.3.2; Recombination of Spectrum.",
    ),

    # --- CONCEPT 8: ATMOSPHERIC REFRACTION & SCATTERING (atmospheric_scattering) ---
    Item(
        item_id="q_eye_atm_01",
        concept="atmospheric_scattering",
        difficulty_label=1,
        question="Why do stars appear to twinkle in the night sky, whereas planets do not twinkle?",
        options=[
            "Stars are distant point sources whose light continuously refracts through moving air layers of varying density",
            "Stars lose photon speed as light travels through interstellar space",
            "Planets are closer so the human eye projects stronger vision rays to them",
            "Stars twinkle because planets reflect light only in pulses",
        ],
        answer_index=0,
        tags=[None, "M11", "M13", None],
        explanation="Stars act as point sources of light. Atmospheric air layers continuously shift in temperature and density, altering the refractive index and causing the apparent position and intensity of starlight to fluctuate (twinkle). Planets appear as extended discs that average out these fluctuations.",
        source_note="NCERT Class 10 Science, Chapter 10, Section 10.4.1; Twinkling of Stars.",
    ),
    Item(
        item_id="q_eye_atm_02",
        concept="atmospheric_scattering",
        difficulty_label=2,
        question="Why does the clear sky appear blue during the day, but the sun appears reddish at sunrise and sunset?",
        options=[
            "Fine air molecules scatter short blue wavelengths most; at sunrise/sunset, light traverses thick atmosphere so only longer red light survives unscattered",
            "Air molecules dye the daytime sky blue, and the sun turns physically cooler and redder at dawn",
            "Blue light travels faster in air than red light during midday",
            "Dust particles emit blue light during the day and red light in the morning",
        ],
        answer_index=0,
        tags=[None, "M14", None, None],
        explanation="Rayleigh scattering intensity is proportional to 1 / lambda^4. Shorter blue wavelengths are scattered much more strongly by atmospheric molecules into our eyes. At dawn and dusk, sunlight passes through a much thicker layer of atmosphere, scattering away blue light and leaving predominantly unscattered red wavelengths.",
        source_note="NCERT Class 10 Science, Chapter 10, Section 10.5.2; Colour of the Sun at Sunrise and Sunset.",
    ),
    Item(
        item_id="q_eye_atm_03",
        concept="atmospheric_scattering",
        difficulty_label=3,
        question="Due to atmospheric refraction, the Sun is visible about 2 minutes before actual sunrise and 2 minutes after actual sunset. What causes this?",
        options=[
            "Atmospheric optical density increases towards Earth, bending light rays from below the horizon downwards into our eyes",
            "Visual rays from the eye bend around the horizon curvature to find the sun",
            "Earth rotates slower in the morning and evening by 4 minutes",
            "Sunlight speeds up when entering lower atmospheric layers",
        ],
        answer_index=0,
        tags=[None, "M13", None, "M11"],
        explanation="The optical density of the atmosphere increases progressively toward Earth's surface. Light rays from the Sun when just below the horizon bend continuously downwards towards the observer, causing the Sun's apparent position to appear approximately 0.5 degrees higher than its actual physical position.",
        source_note="NCERT Class 10 Science, Chapter 10, Section 10.4.2; Advance Sunrise and Delayed Sunset.",
    ),

    # =========================================================================
    # CHAPTER 11: ELECTRICITY (24 Items - Concepts 9 to 16)
    # =========================================================================

    # --- CONCEPT 9: CHARGE (Electric Charge & Quantisation) ---
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
    Item(
        item_id="q_chg_02",
        concept="charge",
        difficulty_label=2,
        question="A current of 0.5 A is drawn by a filament of an electric bulb for 10 minutes. What is the total electric charge that flows through the circuit?",
        options=[
            "300 C; calculated from Q = I × t with time in seconds",
            "5 C; calculated from Q = I × t with time in minutes",
            "600 C; because current is doubled by the battery push",
            "0 C; net charge is zero because current is consumed by the bulb",
        ],
        answer_index=0,
        tags=[None, None, "M2", "M1"],
        explanation="I = 0.5 A, t = 10 minutes = 10 × 60 = 600 s. Total charge Q = I × t = 0.5 A × 600 s = 300 C. Notice that time MUST be in SI units (seconds), and charge is never consumed.",
        source_note="NCERT Class 10 Science, Chapter 11, Example 11.1; Formula Q = I*t.",
    ),
    Item(
        item_id="q_chg_03",
        concept="charge",
        difficulty_label=3,
        question="When an electric circuit is closed, a bulb glows almost instantaneously, even though electron drift velocity in copper is less than 1 mm/s. What explains this?",
        options=[
            "Mobile electrons already exist throughout the entire wire; electric field propagates at nearly light speed",
            "The battery ejects high-speed electrons that rush rapidly from the terminal to the bulb",
            "The battery is a constant-current pump that increases electron velocity across the filament",
            "Current gets consumed so fast that charge accumulates at the bulb filament",
        ],
        answer_index=0,
        tags=[None, "M4", "M2", "M1"],
        explanation="The mobile conduction electrons are already uniformly distributed throughout every millimeter of the metal conductor. When the switch closes, an electric field establishes itself along the conductor at nearly the speed of light, exerting a force on all electrons simultaneously.",
        source_note="NCERT Class 10 Science, Chapter 11, Box 'Flow of Charges'; PER misconception on electron flow.",
    ),

    # --- CONCEPT 10: CURRENT (Electric Current & Flow Rate) ---
    Item(
        item_id="q_cur_01",
        concept="current",
        difficulty_label=1,
        question="How is electric current defined, and what instrument is used to measure it in an active circuit?",
        options=[
            "Rate of flow of electric charges (I = Q/t); measured by an ammeter connected in series",
            "Amount of voltage consumed per second; measured by a voltmeter connected in parallel",
            "The energy stored inside the battery terminals; measured by an ammeter in parallel",
            "The electrical pressure pushing charges; measured by an ammeter in series",
        ],
        answer_index=0,
        tags=[None, "M3", "M4", "M3"],
        explanation="Electric current is the rate of flow of electric charge: I = Q/t, measured in Amperes (1 A = 1 C/s). An ammeter has very low internal resistance and is connected in series so all current flows through it.",
        source_note="NCERT Class 10 Science, Chapter 11, Section 11.1; Electric Current.",
    ),
    Item(
        item_id="q_cur_02",
        concept="current",
        difficulty_label=2,
        question="Two ammeters A1 and A2 are placed in a simple single-loop circuit containing one 12 V battery and one 60 W bulb: A1 is placed BEFORE the bulb, and A2 is placed AFTER the bulb. How do their readings compare?",
        options=[
            "A1 reading equals A2 reading (A1 = A2)",
            "A1 reading is greater than A2 reading (A1 > A2) because the bulb consumes current",
            "A2 reading is greater than A1 reading (A2 > A1) because the bulb energizes current",
            "A2 reads zero because all current is converted into light and heat",
        ],
        answer_index=0,
        tags=[None, "M1", None, "M1"],
        explanation="Current is the rate of charge flow through any cross-section. Because electric charge is strictly conserved and there is only a single conductive pathway, the number of coulombs entering the bulb per second equals the number leaving per second. Hence A1 = A2. Current is NEVER consumed.",
        source_note="NCERT Class 10 Science, Chapter 11, Activity 11.1; Published PER classic circuit test.",
    ),
    Item(
        item_id="q_cur_03",
        concept="current",
        difficulty_label=3,
        question="A student connects a 12 V battery to a 6 Ω resistor, measuring 2 A. She then replaces the 6 Ω resistor with a 12 Ω resistor. What happens to the current supplied by the battery?",
        options=[
            "Current decreases to 1 A because the battery maintains constant voltage, so current depends on circuit resistance",
            "Current remains 2 A because a battery always pushes its rated constant current into any circuit",
            "Current increases to 4 A because more resistance draws more current from the cell",
            "Current drops to zero because the battery ran out of stored charges",
        ],
        answer_index=0,
        tags=[None, "M2", "M5", "M4"],
        explanation="A battery is a source of constant potential difference (V = 12 V), NOT constant current. By Ohm's law, I = V / R = 12 V / 12 Ω = 1 A. When resistance doubles, delivered current halves.",
        source_note="NCERT Class 10 Science, Chapter 11, Section 11.2; PER Battery behavior.",
    ),

    # --- CONCEPT 11: POTENTIAL DIFFERENCE (pd) ---
    Item(
        item_id="q_pd_01",
        concept="pd",
        difficulty_label=1,
        question="What is the definition and SI unit of electric potential difference between two points in an electric circuit?",
        options=[
            "Work done in moving a unit positive charge from one point to another (V = W/Q); Volt",
            "Rate of flow of charge through the wire (V = Q/t); Ampere",
            "Total electrical energy stored inside a chemical cell; Joule",
            "Resistance offered by a conductor to unit electric current; Ohm",
        ],
        answer_index=0,
        tags=[None, "M3", "M3", "M3"],
        explanation="Electric potential difference V between two points is defined as work done W in moving a unit charge Q from one point to another: V = W / Q. Its SI unit is the Volt (1 V = 1 Joule / 1 Coulomb).",
        source_note="NCERT Class 10 Science, Chapter 11, Section 11.2; Electric Potential and Potential Difference.",
    ),
    Item(
        item_id="q_pd_02",
        concept="pd",
        difficulty_label=2,
        question="How much work is done in moving a charge of 4 C across two points having a potential difference of 12 V?",
        options=[
            "48 J; calculated from W = V × Q",
            "3 J; calculated from W = V / Q",
            "0.33 J; calculated from W = Q / V",
            "0 J; work is only done when current is consumed by a load",
        ],
        answer_index=0,
        tags=[None, None, None, "M1"],
        explanation="From the definition V = W / Q, the work done is W = V × Q = 12 V × 4 C = 48 Joules.",
        source_note="NCERT Class 10 Science, Chapter 11, Example 11.2; Calculation of Work Done.",
    ),
    Item(
        item_id="q_pd_03",
        concept="pd",
        difficulty_label=3,
        question="Consider an open circuit consisting of a fresh 9 V dry cell with nothing connected between its terminals. Which statement correctly describes the electrical state?",
        options=[
            "Potential difference across terminals is 9 V, but current is 0 A because there is no closed conducting path",
            "Current is 9 A because the battery constantly outputs current from its positive terminal",
            "Potential difference is 0 V because voltage only exists when current is flowing through a wire",
            "Potential difference is 9 V and current is 9 A because voltage and current are the same physical quantity",
        ],
        answer_index=0,
        tags=[None, "M2", "M3", "M3"],
        explanation="Chemical reactions inside the cell maintain a potential difference of 9 V between its terminals whether connected or not. However, since the circuit is open (infinite air resistance), I = V/R = 9/inf = 0 A. Voltage is the electrical pressure, whereas current is the resulting flow.",
        source_note="NCERT Class 10 Science, Chapter 11, Section 11.2; Open Circuit Potential.",
    ),

    # --- CONCEPT 12: OHM'S LAW (ohm) ---
    Item(
        item_id="q_ohm_01",
        concept="ohm",
        difficulty_label=1,
        question="State Ohm's Law and identify the primary physical condition required for its validity.",
        options=[
            "Current through a conductor is directly proportional to potential difference across it (V ∝ I), provided temperature remains constant",
            "Resistance of a conductor decreases linearly as applied voltage increases",
            "Current supplied by any battery is constant regardless of applied resistance",
            "Voltage across a conductor equals the total charge consumed per second",
        ],
        answer_index=0,
        tags=[None, "M6", "M2", "M3"],
        explanation="Ohm's law states that at constant temperature, the electric current flowing through a metallic conductor is directly proportional to the potential difference across its ends: V = I × R.",
        source_note="NCERT Class 10 Science, Chapter 11, Section 11.3; Ohm's Law.",
    ),
    Item(
        item_id="q_ohm_02",
        concept="ohm",
        difficulty_label=2,
        question="In a laboratory experiment verifying Ohm's Law, a student records V = 3.0 V at I = 0.6 A, and V = 6.0 V at I = 1.2 A. What is the resistance of the conductor, and what would the V-I graph look like?",
        options=[
            "5.0 Ω; a straight line passing through the origin whose slope (ΔV/ΔI) equals R",
            "0.2 Ω; a horizontal line because battery current is constant",
            "5.0 Ω; a curved line because resistance changes with voltage",
            "1.8 Ω; a decreasing line because current is used up at higher voltage",
        ],
        answer_index=0,
        tags=[None, "M2", "M6", "M1"],
        explanation="R = V / I = 3.0 V / 0.6 A = 5.0 Ω, and 6.0 V / 1.2 A = 5.0 Ω. A linear relationship with constant R produces a straight line graph passing through the origin.",
        source_note="NCERT Class 10 Science, Chapter 11, Activity 11.2; V-I Graph Analysis.",
    ),
    Item(
        item_id="q_ohm_03",
        concept="ohm",
        difficulty_label=3,
        question="A student connects a nichrome wire to a 4 V source and measures current I = 0.8 A (R = 5 Ω). The student doubles the voltage to 8 V. What is the new resistance of the wire (assuming temperature is held constant)?",
        options=[
            "5 Ω; resistance is an intrinsic physical property of the wire and does not change with applied voltage",
            "10 Ω; according to R = V/I, doubling voltage doubles resistance",
            "2.5 Ω; higher voltage pushes charges faster, reducing resistance by half",
            "0 Ω; higher voltage overcomes all resistance in the wire",
        ],
        answer_index=0,
        tags=[None, "M6", "M6", "M6"],
        explanation="Resistance depends on length, cross-sectional area, material resistivity, and temperature. For an ohmic conductor at constant temperature, R remains 5 Ω. Doubling voltage doubles current to 1.6 A, keeping R = V/I = 8/1.6 = 5 Ω constant.",
        source_note="NCERT Class 10 Science, Chapter 11, Section 11.3; Invariance of Resistance.",
    ),

    # --- CONCEPT 13: RESISTANCE & FACTORS (resistance) ---
    Item(
        item_id="q_res_01",
        concept="resistance",
        difficulty_label=1,
        question="On which factors does the electrical resistance of a uniform cylindrical metallic conductor depend?",
        options=[
            "Directly on length (l), inversely on cross-sectional area (A), and on material resistivity (ρ)",
            "Directly on applied voltage and inversely on the current consumed",
            "Solely on whether the battery is fresh or discharged",
            "Directly on cross-sectional area and inversely on length",
        ],
        answer_index=0,
        tags=[None, "M6", "M4", None],
        explanation="Resistance of a uniform metallic conductor is given by R = ρ × l / A, where ρ is resistivity, l is length, and A is cross-sectional area.",
        source_note="NCERT Class 10 Science, Chapter 11, Section 11.4; Factors on which Resistance Depends.",
    ),
    Item(
        item_id="q_res_02",
        concept="resistance",
        difficulty_label=2,
        question="A cylindrical wire of resistance R is stretched uniformly until its length is doubled (l' = 2l), while its volume remains constant. What is the new resistance R' of the wire?",
        options=[
            "4R; length doubles while area halves (A' = A/2), so R' = ρ(2l)/(A/2) = 4R",
            "2R; resistance is directly proportional to length only",
            "R / 2; stretching makes electrons travel faster through the wire",
            "R; total amount of metal charge has not changed",
        ],
        answer_index=0,
        tags=[None, None, "M6", "M4"],
        explanation="When a wire of volume V = A × l is stretched to length l' = 2l, its cross-sectional area must halve: A' = A / 2. New resistance R' = ρ × (2l) / (A / 2) = 4 × (ρ × l / A) = 4R.",
        source_note="NCERT Class 10 Science, Chapter 11, Example 11.4; Classical Board Exam Problem.",
    ),
    Item(
        item_id="q_res_03",
        concept="resistance",
        difficulty_label=3,
        question="Two copper wires of equal length have diameters in the ratio 1 : 2. What is the ratio of their electrical resistances (R1 : R2)?",
        options=[
            "4 : 1; resistance is inversely proportional to cross-sectional area, which depends on radius squared (A ∝ d^2)",
            "2 : 1; resistance is inversely proportional to diameter directly",
            "1 : 4; thicker wire has more copper atoms and therefore obstructs current four times more",
            "1 : 1; both wires are copper and have identical length, so resistance must be equal",
        ],
        answer_index=0,
        tags=[None, None, "M5", None],
        explanation="A = π × (d/2)^2 = π × d^2 / 4. Thus A1 / A2 = (d1/d2)^2 = (1/2)^2 = 1/4. Since R = ρ × l / A, R1 / R2 = A2 / A1 = 4 / 1 = 4 : 1.",
        source_note="NCERT Class 10 Science, Chapter 11, Section 11.4; Dependence on Area.",
    ),

    # --- CONCEPT 14: SERIES CIRCUITS (series) ---
    Item(
        item_id="q_ser_01",
        concept="series",
        difficulty_label=1,
        question="Three resistors of 2 Ω, 3 Ω, and 5 Ω are connected in series across a 10 V battery. What is the equivalent resistance of the combination?",
        options=[
            "10 Ω; equivalent resistance in series is R_s = R1 + R2 + R3",
            "0.97 Ω; equivalent resistance is always smaller than the smallest resistor",
            "30 Ω; equivalent resistance in series is the product of resistors",
            "5 Ω; equivalent resistance equals the largest single resistor",
        ],
        answer_index=0,
        tags=[None, "M5", None, None],
        explanation="In a series combination, total equivalent resistance is the algebraic sum of individual resistances: R_s = 2 + 3 + 5 = 10 Ω.",
        source_note="NCERT Class 10 Science, Chapter 11, Section 11.6.1; Resistors in Series.",
    ),
    Item(
        item_id="q_ser_02",
        concept="series",
        difficulty_label=2,
        question="Two identical bulbs B1 and B2 are connected in series with a battery. An ammeter is placed between the battery and B1, and another ammeter is placed between B1 and B2. Bulb B1 glows brightly. What happens to Bulb B2?",
        options=[
            "B2 glows with identical brightness because the same electric current flows through both series bulbs",
            "B2 is dimmer than B1 because B1 consumes most of the current first",
            "B2 does not glow at all because B1 uses up all available electric charges",
            "B2 glows brighter because potential difference builds up across the second component",
        ],
        answer_index=0,
        tags=[None, "M1", "M1", "M3"],
        explanation="In a series circuit, there is only one pathway for current: I_tot = I1 = I2. Identical current flows through identical bulbs, dissipating identical power (P = I^2 × R) and producing identical brightness.",
        source_note="NCERT Class 10 Science, Chapter 11, Section 11.6.1; Classic PER Series Bulb Brightness.",
    ),
    Item(
        item_id="q_ser_03",
        concept="series",
        difficulty_label=3,
        question="Two resistors R1 = 10 Ω and R2 = 20 Ω are connected in series to a 6 V battery. What is the potential difference across R1 and R2 respectively?",
        options=[
            "V1 = 2 V and V2 = 4 V; voltage divides in direct proportion to resistance in series",
            "V1 = 6 V and V2 = 6 V; every component in a circuit receives full battery voltage",
            "V1 = 4 V and V2 = 2 V; first resistor consumes more voltage before current moves downstream",
            "V1 = 3 V and V2 = 3 V; voltage always splits equally 50/50 across two series components",
        ],
        answer_index=0,
        tags=[None, "M3", "M1", "M7"],
        explanation="R_s = 10 + 20 = 30 Ω. Circuit current I = V / R_s = 6 / 30 = 0.2 A. Voltage across R1: V1 = I × R1 = 0.2 A × 10 Ω = 2 V. Voltage across R2: V2 = I × R2 = 0.2 A × 20 Ω = 4 V.",
        source_note="NCERT Class 10 Science, Chapter 11, Example 11.7; Voltage Division in Series.",
    ),

    # --- CONCEPT 15: PARALLEL CIRCUITS (parallel) ---
    Item(
        item_id="q_par_01",
        concept="parallel",
        difficulty_label=1,
        question="Two resistors R1 = 6 Ω and R2 = 6 Ω are connected in parallel. What is the equivalent resistance of the combination?",
        options=[
            "3 Ω; 1/R_p = 1/6 + 1/6 = 2/6 = 1/3 ==> R_p = 3 Ω",
            "12 Ω; adding resistors in parallel increases total circuit resistance",
            "6 Ω; equivalent resistance remains unchanged because resistors are identical",
            "36 Ω; in parallel, total resistance equals the product of resistors",
        ],
        answer_index=0,
        tags=[None, "M5", None, None],
        explanation="1 / R_p = 1 / R1 + 1 / R2 = 1/6 + 1/6 = 2/6 = 1/3 ==> R_p = 3 Ω. Connecting resistors in parallel provides multiple conduction paths, always lowering equivalent resistance.",
        source_note="NCERT Class 10 Science, Chapter 11, Section 11.6.2; Resistors in Parallel.",
    ),
    Item(
        item_id="q_par_02",
        concept="parallel",
        difficulty_label=2,
        question="A 12 V battery is connected across two parallel branches: Branch 1 has R1 = 4 Ω, and Branch 2 has R2 = 12 Ω. What are the branch currents I1 and I2, and the total current I_tot drawn from the battery?",
        options=[
            "I1 = 3 A, I2 = 1 A, I_tot = 4 A; current divides inversely with resistance",
            "I1 = 2 A, I2 = 2 A, I_tot = 4 A; parallel branches always split current equally",
            "I1 = 1 A, I2 = 3 A, I_tot = 4 A; higher resistance attracts more current from the cell",
            "I1 = 3 A, I2 = 1 A, I_tot = 2 A; battery current is a constant fixed amount",
        ],
        answer_index=0,
        tags=[None, "M7", "M5", "M2"],
        explanation="Both branches experience full 12 V. Branch 1: I1 = V / R1 = 12 / 4 = 3 A. Branch 2: I2 = V / R2 = 12 / 12 = 1 A. Total current I_tot = I1 + I2 = 3 + 1 = 4 A.",
        source_note="NCERT Class 10 Science, Chapter 11, Example 11.8; Parallel Branch Currents.",
    ),
    Item(
        item_id="q_par_03",
        concept="parallel",
        difficulty_label=3,
        question="Three identical lamps are connected in parallel to a battery. If one lamp's filament burns out (open circuit), what happens to the brightness of the remaining two lamps?",
        options=[
            "Their brightness remains exactly the same because voltage across parallel branches and branch resistance are unchanged",
            "They glow brighter because the current that went to the dead bulb now divides between them",
            "They both turn off because breaking any part of a circuit stops all electric current",
            "They become dimmer because total circuit resistance increases",
        ],
        answer_index=0,
        tags=[None, "M2", "M1", "M5"],
        explanation="Each parallel branch is connected directly across the constant battery voltage V. Power dissipated by each surviving bulb is P = V^2 / R. Since neither V nor R changed for the remaining bulbs, their individual currents and brightness remain unchanged.",
        source_note="NCERT Class 10 Science, Chapter 11, Section 11.6.2; Advantages of Parallel Circuits.",
    ),

    # --- CONCEPT 16: ELECTRIC POWER & HEATING (power) ---
    Item(
        item_id="q_pow_01",
        concept="power",
        difficulty_label=1,
        question="Which mathematical expression correctly represents electric power dissipated by an electrical device?",
        options=[
            "P = V × I = I^2 × R = V^2 / R",
            "P = V / I = I × R^2",
            "P = V^2 × I = W × t",
            "P = I / V = Q × V",
        ],
        answer_index=0,
        tags=[None, "M3", "M3", "M3"],
        explanation="Electric power is rate of doing work: P = W / t = (V × Q) / t = V × I. By Ohm's law (V = I*R), P = (I*R) × I = I^2 × R = V^2 / R. SI unit is Watt (W).",
        source_note="NCERT Class 10 Science, Chapter 11, Section 11.7; Electric Power.",
    ),
    Item(
        item_id="q_pow_02",
        concept="power",
        difficulty_label=2,
        question="An electric bulb is rated 220 V and 100 W. When it is operated on 110 V, what is the actual power consumed?",
        options=[
            "25 W; resistance is constant (484 Ω), so P' = (110)^2 / 484 = 25 W",
            "50 W; halving voltage halves the power consumed directly",
            "100 W; a 100 W bulb always draws 100 W regardless of supply voltage",
            "75 W; battery delivers constant current to the filament",
        ],
        answer_index=0,
        tags=[None, "M3", None, "M2"],
        explanation="Filament resistance is R = V^2 / P = (220)^2 / 100 = 484 Ω. When operated at V' = 110 V, power consumed is P' = (V')^2 / R = (110)^2 / 484 = 12100 / 484 = 25 W.",
        source_note="NCERT Class 10 Science, Chapter End Exercise Question 3; Classic CBSE Board Question.",
    ),
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
        explanation="Filament resistances are R_60 = V^2/P = (220)^2 / 60 ≈ 807 Ω, and R_100 = (220)^2 / 100 = 484 Ω. In series, current I is identical. Actual power is P = I^2 × R. Because R_60 > R_100, the 60 W bulb dissipates more power and glows brighter.",
        source_note="NCERT Class 10 Science, Exemplar Physics Problems; PER Bulb Brightness in Series.",
    ),

    # =========================================================================
    # CHAPTER 12: MAGNETIC EFFECTS OF ELECTRIC CURRENT (12 Items)
    # =========================================================================

    # --- CONCEPT 17: MAGNETIC FIELD & FIELD LINES (magnetic_field) ---
    Item(
        item_id="q_mag_fld_01",
        concept="magnetic_field",
        difficulty_label=1,
        question="Which of the following statements about magnetic field lines outside a bar magnet is TRUE?",
        options=[
            "They emerge from the North pole, enter the South pole, and form closed continuous loops that never intersect",
            "They start at the North pole and permanently terminate at the South pole inside the magnet",
            "They can cross each other in regions where the magnetic field is exceptionally strong",
            "They are straight radial lines emanating outward from isolated magnetic monopoles",
        ],
        answer_index=0,
        tags=[None, None, "M17", "M15"],
        explanation="Magnetic field lines are closed continuous loops. Outside a magnet, they emerge from the North pole and merge into the South pole. By physical definition, field lines can never cross each other.",
        source_note="NCERT Class 10 Science, Chapter 12, Section 12.1; Magnetic Field and Field Lines.",
    ),
    Item(
        item_id="q_mag_fld_02",
        concept="magnetic_field",
        difficulty_label=2,
        question="Why can two magnetic field lines NEVER intersect each other at any point in space?",
        options=[
            "A magnetic compass needle placed at the intersection would have to point in two different directions at once, which is impossible",
            "The magnetic charges at the intersection would neutralize and cancel to zero",
            "Magnetic field lines can only intersect inside ferromagnetic materials",
            "The electric current in the compass needle prevents field lines from meeting",
        ],
        answer_index=0,
        tags=[None, "M15", "M17", "M16"],
        explanation="The tangent to a magnetic field line at any point indicates the direction of the magnetic field at that point. If two lines intersected, the compass needle would simultaneously point in two different directions, which is physically impossible.",
        source_note="NCERT Class 10 Science, Chapter 12, Section 12.1.2; Properties of Field Lines.",
    ),
    Item(
        item_id="q_mag_fld_03",
        concept="magnetic_field",
        difficulty_label=3,
        question="A uniform bar magnet of magnetic moment M is cut into two equal halves along its length. What are the poles and magnetic moment of each piece?",
        options=[
            "Each piece becomes a complete magnet with both North and South poles, having magnetic moment M/2",
            "One piece becomes a pure North monopole and the other a pure South monopole",
            "The magnetism is completely destroyed by the physical cut",
            "Each piece retains full magnetic moment M because magnetism is conserved",
        ],
        answer_index=0,
        tags=[None, "M15", None, None],
        explanation="Isolated magnetic monopoles do not exist. Cutting a bar magnet produces two complete dipole magnets, each having North and South poles. Cutting along the length halves the pole strength, yielding magnetic moment M/2 for each piece.",
        source_note="NCERT Class 10 Science, Chapter 12; Fundamental Magnetic Dipoles.",
    ),

    # --- CONCEPT 18: MAGNETIC FIELD DUE TO CURRENT (current_magnetism) ---
    Item(
        item_id="q_mag_cur_01",
        concept="current_magnetism",
        difficulty_label=1,
        question="According to the Right-Hand Thumb Rule, if the thumb points in the direction of electric current along a straight vertical wire, what do the curled fingers represent?",
        options=[
            "The direction of the circular magnetic field lines encircling the wire",
            "The direction of mechanical force pushing the wire sideways",
            "The direction of induced electrostatic attraction",
            "The direction of the potential difference created by the battery",
        ],
        answer_index=0,
        tags=[None, "M16", None, "M3"],
        explanation="The Right-Hand Thumb Rule states that if you grasp a current-carrying conductor with your right hand such that the thumb points in the direction of current, your curled fingers show the direction of the magnetic field lines.",
        source_note="NCERT Class 10 Science, Chapter 12, Section 12.2.1; Right-Hand Thumb Rule.",
    ),
    Item(
        item_id="q_mag_cur_02",
        concept="current_magnetism",
        difficulty_label=2,
        question="A long horizontal wire carries a direct current from South to North. What is the direction of the magnetic field at a point directly ABOVE the wire?",
        options=[
            "Towards the West; using the Right-Hand Thumb Rule with thumb pointing North",
            "Towards the East; using the Right-Hand Thumb Rule",
            "Vertically upwards away from the wire",
            "Directly South opposing the current",
        ],
        answer_index=0,
        tags=[None, None, None, None],
        explanation="Align the right-hand thumb pointing North (direction of current). Directly above the wire, the curled fingers curl from East to West. Hence the magnetic field directly above the wire points towards the West.",
        source_note="NCERT Class 10 Science, Chapter 12, Section 12.2.1; Magnetic Field Direction.",
    ),
    Item(
        item_id="q_mag_cur_03",
        concept="current_magnetism",
        difficulty_label=3,
        question="How does the magnetic field behave inside the interior of a long, closely-wound current-carrying solenoid?",
        options=[
            "The magnetic field is uniform and parallel to the axis at all interior points",
            "The magnetic field is strongest at the center and drops to zero at the ends",
            "The field lines intersect along the central axis of the cylinder",
            "Current in the solenoid is consumed along its turns, weakening the field downstream",
        ],
        answer_index=0,
        tags=[None, None, "M17", "M1"],
        explanation="Inside a long current-carrying solenoid, the magnetic field lines are straight, parallel, and equidistant lines along the axis. This indicates that the magnetic field is uniform at all points inside the solenoid.",
        source_note="NCERT Class 10 Science, Chapter 12, Section 12.2.3; Magnetic Field in a Solenoid.",
    ),

    # --- CONCEPT 19: MAGNETIC FORCE & FLEMING'S RULE (magnetic_force) ---
    Item(
        item_id="q_mag_frc_01",
        concept="magnetic_force",
        difficulty_label=1,
        question="Under Fleming's Left-Hand Rule, what do the Thumb, Forefinger, and Middle finger represent respectively?",
        options=[
            "Thumb: Motion/Force; Forefinger: Magnetic Field; Middle: Electric Current",
            "Thumb: Electric Current; Forefinger: Magnetic Field; Middle: Motion/Force",
            "Thumb: Induced Current; Forefinger: Magnetic Field; Middle: Motion/Force",
            "Thumb: Voltage; Forefinger: Resistance; Middle: Current",
        ],
        answer_index=0,
        tags=[None, "M16", "M16", "M3"],
        explanation="Fleming's Left-Hand Rule: Stretch the thumb, forefinger, and middle finger mutually perpendicular. Forefinger = Field (B), Middle finger = Current (I), Thumb = Force/Motion (F) experienced by the conductor.",
        source_note="NCERT Class 10 Science, Chapter 12, Section 12.3; Fleming's Left-Hand Rule.",
    ),
    Item(
        item_id="q_mag_frc_02",
        concept="magnetic_force",
        difficulty_label=2,
        question="A positively charged alpha particle projected towards the West is deflected towards the North by a magnetic field. What is the direction of the magnetic field?",
        options=[
            "Vertically upwards (out of the page); using Fleming's Left-Hand Rule",
            "Vertically downwards (into the page)",
            "Towards the South",
            "Towards the East",
        ],
        answer_index=0,
        tags=[None, "M16", None, None],
        explanation="Current direction is the direction of positive charge motion (West). Force is towards North. Using Fleming's Left-Hand Rule: Middle finger points West, Thumb points North ==> Forefinger points Vertically Upwards.",
        source_note="NCERT Class 10 Science, Chapter 12, In-text Question 2; Application of Fleming's Left-Hand Rule.",
    ),
    Item(
        item_id="q_mag_frc_03",
        concept="magnetic_force",
        difficulty_label=3,
        question="A straight copper conductor carrying electric current I is placed in a uniform magnetic field B. At what angle between the conductor and field lines is the magnetic force MAXIMUM?",
        options=[
            "90 degrees (conductor perpendicular to magnetic field lines)",
            "0 degrees (conductor parallel to magnetic field lines)",
            "45 degrees",
            "180 degrees (conductor anti-parallel to magnetic field lines)",
        ],
        answer_index=0,
        tags=[None, None, None, None],
        explanation="The magnetic force on a current-carrying wire of length L in field B is given by F = B × I × L × sin(theta). When theta = 90 degrees, sin(90°) = 1, resulting in the maximum possible mechanical force.",
        source_note="NCERT Class 10 Science, Chapter 12, Section 12.3; Force on a Conductor in a Magnetic Field.",
    ),

    # --- CONCEPT 20: DOMESTIC CIRCUITS & SAFETY DEVICES (domestic_circuits) ---
    Item(
        item_id="q_mag_dom_01",
        concept="domestic_circuits",
        difficulty_label=1,
        question="In standard Indian domestic electric wiring (220 V, 50 Hz AC), what are the standard insulation colors for Live, Neutral, and Earth wires?",
        options=[
            "Live = Red / Brown; Neutral = Black / Light Blue; Earth = Green / Yellow",
            "Live = Green; Neutral = Black; Earth = Red",
            "Live = Black; Neutral = White; Earth = Red",
            "All wires have identical insulation because AC voltage alternates continuously",
        ],
        answer_index=0,
        tags=[None, None, None, "M3"],
        explanation="In Indian domestic circuits, the Live wire has red/brown insulation, the Neutral wire has black/light blue insulation, and the safety Earth wire has green/yellow insulation.",
        source_note="NCERT Class 10 Science, Chapter 12, Section 12.5; Domestic Electric Circuits.",
    ),
    Item(
        item_id="q_mag_dom_02",
        concept="domestic_circuits",
        difficulty_label=2,
        question="What is the primary safety purpose of connecting the Earth wire to metallic appliances such as electric irons, toasters, and refrigerators?",
        options=[
            "It provides a low-resistance path for leakage current to ground, preventing fatal electric shocks to users",
            "It stores excess electrons in the earth to save household electric power",
            "It balances the voltage across the appliance so current is consumed more evenly",
            "It increases total appliance resistance to reduce electrical heating",
        ],
        answer_index=0,
        tags=[None, "M4", "M1", "M5"],
        explanation="The metallic body of an appliance is connected to the Earth wire. If live wire insulation fails and touches the metallic frame, current flows safely to ground through the low-resistance Earth wire, tripping the fuse/MCB without shocking the user.",
        source_note="NCERT Class 10 Science, Chapter 12, Section 12.5; Earthing and Electrical Safety.",
    ),
    Item(
        item_id="q_mag_dom_03",
        concept="domestic_circuits",
        difficulty_label=3,
        question="When does 'short-circuiting' occur in a domestic power circuit, and why is it dangerous?",
        options=[
            "When the live wire and neutral wire come into direct physical contact, dropping circuit resistance close to zero and causing a massive current surge",
            "When electric current is used up before reaching the appliance, creating a vacuum in the wire",
            "When too many appliances are connected in series, multiplying total resistance",
            "When the earth wire disconnects from the ground, cutting off all voltage",
        ],
        answer_index=0,
        tags=[None, "M1", "M5", "M4"],
        explanation="Short-circuiting occurs when Live and Neutral wires touch directly due to damaged insulation or appliance fault. The circuit resistance drops to near zero, causing an enormous surge of current (I = V/R) that produces extreme Joule heating and fire hazard.",
        source_note="NCERT Class 10 Science, Chapter 12, Section 12.5; Short-Circuiting and Overloading.",
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

def get_diagnostic_questions(chapter_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Return diagnostic questions in prerequisite order.
    - If chapter_id is specified (e.g., 'light', 'human_eye', 'electricity', 'magnetism'),
      returns Level 2 diagnostic items for that specific chapter.
    - If chapter_id is None or 'all', returns a comprehensive 8-question diagnostic
      spanning the entire Class 10 Physics syllabus (2 questions per chapter).
    """
    chapter_diag_map = {
        "light": [
            "q_lgt_mir_02",   # reflection_mirrors (Level 2)
            "q_lgt_refr_02",  # refraction_laws (Level 2)
            "q_lgt_len_02",   # refraction_lenses (Level 2)
            "q_lgt_pow_02",   # lens_power (Level 2)
        ],
        "human_eye": [
            "q_eye_str_02",   # eye_vision (Level 2)
            "q_eye_def_02",   # defects_vision (Level 2)
            "q_eye_prs_02",   # prism_dispersion (Level 2)
            "q_eye_atm_02",   # atmospheric_scattering (Level 2)
        ],
        "electricity": [
            "q_chg_02",  # charge (Level 2)
            "q_cur_02",  # current (Level 2)
            "q_pd_02",   # pd (Level 2)
            "q_ohm_02",  # ohm (Level 2)
            "q_res_02",  # resistance (Level 2)
            "q_ser_02",  # series (Level 2)
            "q_par_02",  # parallel (Level 2)
            "q_pow_02",  # power (Level 2)
        ],
        "magnetism": [
            "q_mag_fld_02",  # magnetic_field (Level 2)
            "q_mag_cur_02",  # current_magnetism (Level 2)
            "q_mag_frc_02",  # magnetic_force (Level 2)
            "q_mag_dom_02",  # domestic_circuits (Level 2)
        ],
    }

    if chapter_id and chapter_id in chapter_diag_map:
        diag_ids = chapter_diag_map[chapter_id]
    else:
        # Balanced 8-question diagnostic spanning all 4 chapters of Class 10 Physics
        diag_ids = [
            "q_lgt_mir_02",   # Chapter 9: Light (Mirrors)
            "q_lgt_len_02",   # Chapter 9: Light (Lenses)
            "q_eye_def_02",   # Chapter 10: Human Eye (Defects)
            "q_eye_prs_02",   # Chapter 10: Human Eye (Dispersion)
            "q_cur_02",       # Chapter 11: Electricity (Current conservation)
            "q_par_02",       # Chapter 11: Electricity (Parallel circuits)
            "q_mag_cur_02",   # Chapter 12: Magnetism (Current & Field)
            "q_mag_frc_02",   # Chapter 12: Magnetism (Fleming's Left-Hand Rule)
        ]

    diag_items = []
    for qid in diag_ids:
        q = get_question_by_id(qid)
        if q:
            diag_items.append(q)
    return diag_items
