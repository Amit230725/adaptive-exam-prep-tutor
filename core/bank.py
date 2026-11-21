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



# =============================================================================
# BLUEPRINT SECTION 7: 30-ITEM CHAPTER-BALANCED DIAGNOSTIC ASSESSMENT
# =============================================================================
# Breakdown:
# 1. Light: mirrors (6 items)
# 2. Refraction and lenses (6 items)
# 3. Eye and colour (4 items)
# 4. Electricity (8 items)
# 5. Magnetism (6 items)
# Total = exactly 30 items.
# =============================================================================

DIAGNOSTIC_30_BLUEPRINT: List[Dict[str, Any]] = [
    # --- CLUSTER 1: LIGHT: MIRRORS (6 items) ---
    {
        "id": "diag_30_01",
        "cluster": "Light: mirrors",
        "concept": "L5",
        "legacy_concept": "reflection_mirrors",
        "difficulty_label": 1,
        "question": "A spherical concave mirror has a radius of curvature of R = 40 cm. What is its principal focal length?",
        "options": [
            "20 cm, because focal length is half the radius of curvature (f = R/2)",
            "40 cm, because focal length equals the radius of curvature (f = R)",
            "80 cm, because focal length is twice the radius of curvature (f = 2R)",
            "10 cm, because focal length is one-fourth the radius (f = R/4)"
        ],
        "answer_index": 0,
        "tags": [None, "FOCAL_RADIUS", "FOCAL_RADIUS", None],
        "reasoning_options": [
            "The focus is exactly the midpoint between Pole and Centre of Curvature: f = R/2 = 20 cm.",
            "The radius and focal length refer to the exact same geometric length: f = R = 40 cm.",
            "Light bounces across the entire diameter before focusing: f = 2R = 80 cm.",
            "Spherical aberration reduces the effective focal length to a quarter of radius."
        ],
        "explanation": "For spherical mirrors of small aperture, the principal focus F lies midway between the pole P and centre of curvature C. Therefore, f = R / 2 = 40 / 2 = 20 cm.",
        "diagram_alt": "Concave mirror axis showing Pole P at 0 cm, Focus F at 20 cm, and Centre of Curvature C at 40 cm.",
        "followup_probe": "If a convex rear-view mirror has a radius of curvature of 3.0 m, what is its focal length?",
        "source_note": "NCERT Class 10 Ch 9 Section 9.2.1; Blueprint Section 7",
        "is_ai": False,
    },
    {
        "id": "diag_30_02",
        "cluster": "Light: mirrors",
        "concept": "L7",
        "legacy_concept": "reflection_mirrors",
        "difficulty_label": 2,
        "question": "An illuminated object is placed 30 cm in front of a concave mirror of focal length 20 cm. According to the New Cartesian Sign Convention, where is the image formed?",
        "options": [
            "v = -60 cm; a real image formed 60 cm in front of the mirror",
            "v = +60 cm; a virtual image formed 60 cm behind the mirror",
            "v = -12 cm; a real image formed 12 cm in front of the mirror",
            "v = +12 cm; a virtual image formed 12 cm behind the mirror"
        ],
        "answer_index": 0,
        "tags": [None, "MIRROR_SIGN", "MIRROR_SIGN", "MIRROR_SIGN"],
        "reasoning_options": [
            "Both f and u are negative: f = -20 cm, u = -30 cm. 1/v = 1/f - 1/u = 1/(-20) - 1/(-30) = -1/60, so v = -60 cm.",
            "Focal length is positive for concave mirror: f = +20 cm, u = -30 cm, yielding positive v.",
            "Added 1/f + 1/u directly without transposing: 1/v = 1/(-20) + 1/(-30) = -5/60 = -1/12 cm.",
            "Assumed object distance is positive because object is placed on the left: u = +30 cm."
        ],
        "explanation": "By the Cartesian sign convention with pole as origin: f = -20 cm, u = -30 cm. From 1/f = 1/v + 1/u, we have 1/v = 1/f - 1/u = 1/(-20) - 1/(-30) = -1/20 + 1/30 = -1/60, so v = -60 cm. The negative sign denotes a real inverted image in front of the mirror.",
        "diagram_alt": "Concave mirror ray diagram with object between C and F (-30 cm) and real image beyond C (-60 cm).",
        "followup_probe": "If the object is moved to 10 cm in front of the mirror, does the image stay in front or move behind?",
        "source_note": "Blueprint Section 7 & 8 'Corrected example'",
        "is_ai": False,
    },
    {
        "id": "diag_30_03",
        "cluster": "Light: mirrors",
        "concept": "L7",
        "legacy_concept": "reflection_mirrors",
        "difficulty_label": 2,
        "question": "A concave mirror produces a real, inverted image three times larger than the object. If the object distance is u = -15 cm, what is the image distance v?",
        "options": [
            "v = -45 cm, with magnification m = -3",
            "v = +45 cm, with magnification m = +3",
            "v = -5 cm, with magnification m = -1/3",
            "v = +5 cm, with magnification m = +1/3"
        ],
        "answer_index": 0,
        "tags": [None, "MIRROR_SIGN", "MIRROR_SIGN", "MIRROR_SIGN"],
        "reasoning_options": [
            "For a real inverted image, magnification is negative: m = -3. Since m = -v/u, -3 = -v/(-15) => v = -45 cm.",
            "Magnification is always positive regardless of real or virtual orientation: m = +3 => v = +45 cm.",
            "Divided object distance by magnification instead of multiplying: v = u / m = -15 / 3 = -5 cm.",
            "Assumed inverted means positive coordinate: v = +5 cm."
        ],
        "explanation": "Magnification for a mirror is m = -v/u = h'/h. Since the image is real and inverted, h' is negative, so m = -3. Substituting: -3 = -v/(-15) => -3 = v/15 => v = -45 cm.",
        "diagram_alt": "Concave mirror showing object of height 1 cm at -15 cm and inverted image of height -3 cm at -45 cm.",
        "followup_probe": "If m = +0.5, what can you deduce about the nature and type of mirror?",
        "source_note": "NCERT Class 10 Ch 9 Section 9.2.3; Blueprint Section 7",
        "is_ai": False,
    },
    {
        "id": "diag_30_04",
        "cluster": "Light: mirrors",
        "concept": "L6",
        "legacy_concept": "reflection_mirrors",
        "difficulty_label": 2,
        "question": "A ray of light passing through the principal focus (F) of a concave mirror strikes its reflective surface. How does the reflected ray travel?",
        "options": [
            "Parallel to the principal axis",
            "Reflects back along the same path through the focus",
            "Passes through the centre of curvature (C)",
            "Bends toward the normal at an angle of 90 degrees"
        ],
        "answer_index": 0,
        "tags": [None, "MIRROR_SIGN", "MIRROR_SIGN", None],
        "reasoning_options": [
            "By the principle of reversibility of light, a ray directed through the focus reflects parallel to the principal axis.",
            "Confused ray through focus with a ray incident normally through the centre of curvature C.",
            "Assumed focus directs rays toward the centre of curvature.",
            "Assumed reflection at spherical surface is always at right angles."
        ],
        "explanation": "Standard ray optics rule: A ray passing through (or directed toward) the principal focus of a spherical mirror emerges parallel to the principal axis after reflection, reversing the path of a parallel incident ray.",
        "diagram_alt": "Concave mirror showing ray from F hitting mirror and reflecting parallel to principal axis.",
        "followup_probe": "Which ray reflects strictly back along its own path?",
        "source_note": "NCERT Class 10 Ch 9 Section 9.2.2",
        "is_ai": False,
    },
    {
        "id": "diag_30_05",
        "cluster": "Light: mirrors",
        "concept": "L4",
        "legacy_concept": "reflection_mirrors",
        "difficulty_label": 1,
        "question": "Why are convex mirrors universally preferred as rear-view (wing) mirrors in automobiles?",
        "options": [
            "They always form an erect, diminished virtual image and provide a much wider field of view",
            "They form an enlarged real image of approaching vehicles on the glass surface",
            "They have a negative focal length that eliminates blind spots",
            "They converge headlights into a bright focused point"
        ],
        "answer_index": 0,
        "tags": [None, "M8", "MIRROR_SIGN", "CONVEX_ALWAYS_REAL"],
        "reasoning_options": [
            "Convex mirrors curve outwards, producing upright diminished images with an expanded panoramic viewing angle.",
            "Believes mirror image is painted on glass surface and magnified.",
            "Confuses convex mirror sign (f is positive, not negative).",
            "Confuses convex mirror (diverging) with concave mirror (converging)."
        ],
        "explanation": "Convex mirrors always give an erect, virtual though diminished image. Because they curve outwards, they encompass a wider field of view than a plane mirror.",
        "diagram_alt": "Convex mirror with rays diverging outwards, showing wide angular coverage.",
        "followup_probe": "What is the sign of the focal length of a convex mirror under the Cartesian convention?",
        "source_note": "NCERT Class 10 Ch 9 Section 9.2.2",
        "is_ai": False,
    },
    {
        "id": "diag_30_06",
        "cluster": "Light: mirrors",
        "concept": "L6",
        "legacy_concept": "reflection_mirrors",
        "difficulty_label": 2,
        "question": "To use a concave mirror as a shaving or dental inspection mirror, where must the face or tooth be positioned relative to the mirror?",
        "options": [
            "Between the pole (P) and principal focus (F)",
            "At the centre of curvature (C)",
            "Between the focus (F) and centre of curvature (C)",
            "Beyond the centre of curvature (C)"
        ],
        "answer_index": 0,
        "tags": [None, "M8", "MIRROR_SIGN", None],
        "reasoning_options": [
            "When u < f, the reflected rays diverge and appear to meet behind the mirror, creating an erect, enlarged virtual image.",
            "At C, image is real, inverted, and same size (not helpful for shaving).",
            "Between F and C, image is enlarged but real and inverted (upside-down).",
            "Beyond C, image is diminished and inverted."
        ],
        "explanation": "Only when the object is held between the pole and the principal focus (u < f) does a concave mirror produce an upright (erect), magnified virtual image.",
        "diagram_alt": "Concave mirror with object inside focus (between P and F), rays tracing back to enlarged virtual image behind mirror.",
        "followup_probe": "What is the sign of magnification m when an object is between P and F of a concave mirror?",
        "source_note": "NCERT Class 10 Ch 9 Section 9.2.2; Table 9.1",
        "is_ai": False,
    },

    # --- CLUSTER 2: REFRACTION AND LENSES (6 items) ---
    {
        "id": "diag_30_07",
        "cluster": "Refraction and lenses",
        "concept": "L10",
        "legacy_concept": "refraction_laws",
        "difficulty_label": 2,
        "question": "The absolute refractive index of water is 4/3 and of glass is 3/2. What is the refractive index of glass with respect to water (w_n_g)?",
        "options": [
            "9/8 (1.125), calculated as n_glass / n_water",
            "8/9 (0.889), calculated as n_water / n_glass",
            "2/1 (2.0), calculated by multiplying refractive indices",
            "1/6 (0.167), calculated by subtracting refractive indices"
        ],
        "answer_index": 0,
        "tags": [None, "M11", None, None],
        "reasoning_options": [
            "Relative refractive index w_n_g = n_g / n_w = (3/2) / (4/3) = 9/8 = 1.125.",
            "Inverted the ratio by dividing medium 1 by medium 2.",
            "Multiplied optical densities instead of taking the velocity ratio.",
            "Subtracted indices directly."
        ],
        "explanation": "By definition, the relative refractive index of medium 2 with respect to medium 1 is 1_n_2 = n2 / n1. Therefore, w_n_g = n_g / n_w = (3/2) / (4/3) = 9/8 = 1.125.",
        "diagram_alt": "Ray of light passing from water into glass, bending towards the normal.",
        "followup_probe": "Does light travel faster in water or in glass?",
        "source_note": "NCERT Class 10 Ch 9 Section 9.3.2",
        "is_ai": False,
    },
    {
        "id": "diag_30_08",
        "cluster": "Refraction and lenses",
        "concept": "L11",
        "legacy_concept": "refraction_laws",
        "difficulty_label": 2,
        "question": "A monochromatic ray of light enters a rectangular glass slab obliquely from air and emerges back into air from the opposite parallel face. Which statement correctly describes the emergent ray?",
        "options": [
            "It is parallel to the incident ray but laterally displaced sideways",
            "It deviates by an angle of 90 degrees from its incident direction",
            "It converges to a focus on the back surface of the slab",
            "It emerges with reduced speed and different colour"
        ],
        "answer_index": 0,
        "tags": [None, "M11", "M8", "M14"],
        "reasoning_options": [
            "The extent of bending at opposite parallel faces is equal and opposite (i = e), keeping the emergent ray parallel while shifted laterally.",
            "Assumed glass slab acts like a prism that permanently deviates the beam.",
            "Assumed the back surface absorbs and focuses light like a mirror.",
            "Believes light changes colour and loses frequency in glass."
        ],
        "explanation": "Refraction at the air-glass surface bends light toward normal, while refraction at the opposite glass-air surface bends it by the exact same angle away from normal. Hence angle of incidence i equals angle of emergence e, resulting in parallel rays separated by lateral shift.",
        "diagram_alt": "Ray traversing rectangular slab: incident ray, refracted ray inside, parallel emergent ray with lateral shift d.",
        "followup_probe": "What factor increases the lateral displacement through a glass slab?",
        "source_note": "NCERT Class 10 Ch 9 Section 9.3.1; Activity 9.10",
        "is_ai": False,
    },
    {
        "id": "diag_30_09",
        "cluster": "Refraction and lenses",
        "concept": "L14",
        "legacy_concept": "refraction_lenses",
        "difficulty_label": 2,
        "question": "An object is placed at a distance of 2F1 (twice the focal length) in front of a convex lens. Where is the image formed, and what are its characteristics?",
        "options": [
            "At 2F2; real, inverted, and of the same size as the object",
            "At infinity; highly enlarged and virtual",
            "Between F2 and 2F2; real and diminished",
            "Inside F2; erect, virtual, and magnified"
        ],
        "answer_index": 0,
        "tags": [None, "CONVEX_ALWAYS_REAL", "CONVEX_ALWAYS_REAL", "CONVEX_ALWAYS_REAL"],
        "reasoning_options": [
            "At 2F1, symmetric ray convergence forms the image at exactly 2F2 on the opposite side with m = -1.",
            "Confused 2F1 with placing the object at the principal focus F1.",
            "Confused placing object at 2F1 with placing it beyond 2F1.",
            "Confused with magnifying glass placement inside focus."
        ],
        "explanation": "When an object is placed at 2F1 in front of a convex lens, rays refract to intersect precisely at 2F2. The image is real, inverted, and equal in size to the object (magnification m = -1).",
        "diagram_alt": "Convex lens showing object at 2F1 and real inverted image at 2F2 of identical height.",
        "followup_probe": "If the object is shifted from 2F1 toward F1, how does the image position and size change?",
        "source_note": "NCERT Class 10 Ch 9 Section 9.3.3; Table 9.4",
        "is_ai": False,
    },
    {
        "id": "diag_30_10",
        "cluster": "Refraction and lenses",
        "concept": "L14",
        "legacy_concept": "refraction_lenses",
        "difficulty_label": 2,
        "question": "Under what condition does a convex lens form a virtual, erect, and magnified image?",
        "options": [
            "When the object is placed between the optical centre (O) and the principal focus (F1)",
            "When the object is placed beyond 2F1",
            "A convex lens can NEVER form a virtual image under any circumstance",
            "When the object is placed at the principal focus F1"
        ],
        "answer_index": 0,
        "tags": [None, "CONVEX_ALWAYS_REAL", "CONVEX_ALWAYS_REAL", "CONVEX_ALWAYS_REAL"],
        "reasoning_options": [
            "When u < f, refracted rays diverge and do not meet in real space; backward extensions meet to form an erect, magnified virtual image (magnifying glass).",
            "Beyond 2F1 produces a diminished real inverted image.",
            "Harbours the persistent misconception that convex lenses can only produce real images.",
            "At F1, refracted rays are parallel, forming an image at infinity, not an accessible virtual image."
        ],
        "explanation": "When an object is placed within the focal length (between O and F1), the refracted rays diverge on the opposite side. To an observer, they appear to emanate from an erect, magnified virtual image on the same side as the object.",
        "diagram_alt": "Convex lens used as magnifying glass with object inside F1, rays extended backwards to virtual erect image.",
        "followup_probe": "What is the sign of magnification m when a convex lens forms an image of an object placed between O and F1?",
        "source_note": "NCERT Class 10 Ch 9 Section 9.3.3; Blueprint Section 9 CONVEX_ALWAYS_REAL",
        "is_ai": False,
    },
    {
        "id": "diag_30_11",
        "cluster": "Refraction and lenses",
        "concept": "L15",
        "legacy_concept": "refraction_lenses",
        "difficulty_label": 2,
        "question": "A concave lens has a focal length of 15 cm. At what distance should an object be placed from the lens so that it forms an image at 10 cm from the lens?",
        "options": [
            "u = -30 cm (30 cm in front of the lens)",
            "u = +30 cm (30 cm behind the lens)",
            "u = -6 cm (6 cm in front of the lens)",
            "u = +6 cm (6 cm behind the lens)"
        ],
        "answer_index": 0,
        "tags": [None, "MIRROR_SIGN", "MIRROR_SIGN", "MIRROR_SIGN"],
        "reasoning_options": [
            "For a concave lens: f = -15 cm, v = -10 cm (virtual image in front). 1/f = 1/v - 1/u => 1/u = 1/v - 1/f = 1/(-10) - 1/(-15) = -1/10 + 1/15 = -1/30 => u = -30 cm.",
            "Treated object distance as positive coordinate behind the lens.",
            "Used the mirror formula (1/f = 1/v + 1/u) instead of lens formula (1/f = 1/v - 1/u).",
            "Swapped signs of focal length and image distance."
        ],
        "explanation": "For a concave lens, both focal length and virtual image distance are negative: f = -15 cm, v = -10 cm. Using the lens formula: 1/f = 1/v - 1/u => 1/u = 1/v - 1/f = 1/(-10) - 1/(-15) = -1/10 + 1/15 = (-3 + 2)/30 = -1/30 => u = -30 cm.",
        "diagram_alt": "Concave diverging lens with virtual image at -10 cm and object at -30 cm.",
        "followup_probe": "What is the magnification m of the image formed in this case?",
        "source_note": "NCERT Class 10 Ch 9 Section 9.3.4 Example 9.3",
        "is_ai": False,
    },
    {
        "id": "diag_30_12",
        "cluster": "Refraction and lenses",
        "concept": "L16",
        "legacy_concept": "lens_power",
        "difficulty_label": 1,
        "question": "An optometrist prescribes a corrective lens with a optical power of P = +2.5 D. What is the focal length of this lens and what type is it?",
        "options": [
            "+40 cm (+0.4 m); a convex (converging) lens",
            "-40 cm (-0.4 m); a concave (diverging) lens",
            "+25 cm (+0.25 m); a convex lens",
            "+250 cm (+2.5 m); a convex lens"
        ],
        "answer_index": 0,
        "tags": [None, "M13", "MATH_UNITS", "MATH_UNITS"],
        "reasoning_options": [
            "P = 1/f(in metres) => f = 1/P = 1/2.5 = 0.4 m = +40 cm. Positive power indicates a convex lens.",
            "Assumed positive power corresponds to concave lens prescription.",
            "Forgot reciprocal calculation and equated power directly to focal length in cm.",
            "Failed unit conversion from metres to centimetres."
        ],
        "explanation": "Power P = 1 / f (in metres). Therefore, f = 1 / 2.5 D = 0.4 m = +40 cm. A positive focal length and power designate a convex (converging) lens.",
        "diagram_alt": "Convex lens with focal length labeled f = +40 cm and power P = +2.5 D.",
        "followup_probe": "If a thin concave lens of power -1.5 D is placed in contact with this lens, what is the net power of the combination?",
        "source_note": "NCERT Class 10 Ch 9 Section 9.3.5",
        "is_ai": False,
    },

    # --- CLUSTER 3: EYE AND COLOUR (4 items) ---
    {
        "id": "diag_30_13",
        "cluster": "Eye and colour",
        "concept": "E3",
        "legacy_concept": "eye_vision",
        "difficulty_label": 1,
        "question": "What is the least distance of distinct vision (near point) for a normal healthy young adult human eye?",
        "options": [
            "25 cm, achieved when ciliary muscles contract fully to increase lens curvature",
            "Infinity, achieved when the eye is completely relaxed",
            "2.5 cm, equal to the diameter of the human eyeball",
            "10 cm, limited by pupil diameter"
        ],
        "answer_index": 0,
        "tags": [None, None, "MATH_UNITS", None],
        "reasoning_options": [
            "The near point of a normal adult eye is standardized at 25 cm (least strain on ciliary muscles).",
            "Confused near point with the far point of vision (which is at infinity).",
            "Confused least distance of distinct vision with the 2.3-2.5 cm diameter of the eyeball.",
            "Arbitrary distance guess without physiological basis."
        ],
        "explanation": "The minimum distance at which objects can be seen most distinctly without strain is called the least distance of distinct vision or near point. For a normal young adult, it is approximately 25 cm.",
        "diagram_alt": "Human eye focusing on an object at 25 cm onto the retina.",
        "followup_probe": "What happens to the focal length of the eye lens when ciliary muscles relax?",
        "source_note": "NCERT Class 10 Ch 10 Section 10.1",
        "is_ai": False,
    },
    {
        "id": "diag_30_14",
        "cluster": "Eye and colour",
        "concept": "E4",
        "legacy_concept": "defects_vision",
        "difficulty_label": 2,
        "question": "A student sitting on the back bench cannot read the blackboard clearly, but reads their textbook easily. What defect of vision do they have, and how is it corrected?",
        "options": [
            "Myopia (near-sightedness); corrected by a concave lens of suitable focal length",
            "Hypermetropia (far-sightedness); corrected by a convex lens of suitable focal length",
            "Presbyopia; corrected by cylindrical lenses",
            "Astigmatism; corrected by bifocal lenses"
        ],
        "answer_index": 0,
        "tags": [None, "M13", "M13", None],
        "reasoning_options": [
            "Can see nearby objects clearly but cannot see distant objects distinctly = Myopia. Caused by elongated eyeball or excessive lens curvature; corrected by diverging (concave) lens.",
            "Confused myopia with hypermetropia, which is inability to see near objects clearly.",
            "Presbyopia is age-related loss of accommodation affecting near vision in older people.",
            "Astigmatism arises from non-spherical cornea curvature."
        ],
        "explanation": "Myopia (near-sightedness) is the condition where a person can see nearby objects clearly but distant objects appear blurry because parallel rays focus in front of the retina. A concave lens diverges incoming rays so they focus precisely on the retina.",
        "diagram_alt": "Myopic eye forming image in front of retina, and corrected eye with concave lens focusing image on retina.",
        "followup_probe": "If a myopic person has their far point at 80 cm, what must be the focal length of their corrective lens?",
        "source_note": "NCERT Class 10 Ch 10 Section 10.2.1",
        "is_ai": False,
    },
    {
        "id": "diag_30_15",
        "cluster": "Eye and colour",
        "concept": "E8",
        "legacy_concept": "prism_dispersion",
        "difficulty_label": 2,
        "question": "When a narrow beam of white light passes through a glass prism, it splits into a spectrum of seven colours (VIBGYOR). Why does violet light bend the most while red light bends the least?",
        "options": [
            "Violet light has the shortest wavelength and slowest speed in glass, so glass has the highest refractive index for violet",
            "The glass prism chemically dyes the incoming white light rays with pigments",
            "Red light is absorbed by the glass while violet passes through the edges",
            "Violet light has greater energy and bounces off the base of the prism"
        ],
        "answer_index": 0,
        "tags": [None, "M14", "M14", "M14"],
        "reasoning_options": [
            "Refractive index of glass is wavelength-dependent (Cauchy dispersion): shorter wavelength (violet) experiences higher refractive index and bends most.",
            "Believes the prism adds colour to light rather than separating existing wavelengths (Newton debunked this).",
            "Believes spectral separation is caused by selective absorption inside the glass.",
            "Attributed deviation to photon energy bouncing off glass boundaries."
        ],
        "explanation": "Different colours of light bend through different angles with respect to the incident beam as they pass through a prism. Red light has the longest wavelength and bends least; violet has the shortest wavelength and bends most.",
        "diagram_alt": "Glass prism dispersing white light into a fan of rays from Red (top, least bent) to Violet (bottom, most bent).",
        "followup_probe": "How did Isaac Newton prove that white light itself is made of colours rather than coloured by the prism?",
        "source_note": "NCERT Class 10 Ch 10 Section 10.3",
        "is_ai": False,
    },
    {
        "id": "diag_30_16",
        "cluster": "Eye and colour",
        "concept": "E10",
        "legacy_concept": "atmospheric_scattering",
        "difficulty_label": 1,
        "question": "Why does the clear sky appear blue during midday, while the sun appears reddish at sunrise and sunset?",
        "options": [
            "Air molecules scatter short-wavelength blue light far more than red; at sunset, light travels a longer atmospheric path, leaving mainly red light unscattered",
            "The oceans reflect their blue water upwards into the clouds",
            "Dust particles in space create a blue filter around the Earth",
            "The sun cools down during sunrise and sunset, shifting its physical colour"
        ],
        "answer_index": 0,
        "tags": [None, "M11", None, None],
        "reasoning_options": [
            "Rayleigh scattering is proportional to 1/lambda^4: fine air molecules scatter blue light ~16x more than red. At horizon, longer path scatters out blue, transmitting red.",
            "Folk belief that sky colour is caused by oceanic reflection.",
            "Attributed scattering to space dust rather than atmospheric molecules.",
            "Believes solar surface temperature drops at dawn and dusk."
        ],
        "explanation": "Fine molecules in atmosphere scatter shorter wavelengths (blue) much more strongly than longer wavelengths (red) according to Rayleigh's law. Near horizon, light passes through thicker air layers; most blue is scattered away, and mostly red reaches our eyes.",
        "diagram_alt": "Earth with atmosphere showing blue light scattering overhead and red light penetrating through thick horizon at sunset.",
        "followup_probe": "Why would the sky appear dark to an astronaut in space?",
        "source_note": "NCERT Class 10 Ch 10 Section 10.6",
        "is_ai": False,
    },

    # --- CLUSTER 4: ELECTRICITY (8 items) ---
    {
        "id": "diag_30_17",
        "cluster": "Electricity",
        "concept": "C1",
        "legacy_concept": "charge",
        "difficulty_label": 1,
        "question": "A steady current of 0.5 A flows through the filament of an electric bulb for 10 minutes. What is the total amount of electric charge that flows through the circuit?",
        "options": [
            "300 Coulombs (Q = I * t = 0.5 A * 600 s)",
            "5 Coulombs (Q = 0.5 * 10 without converting minutes to seconds)",
            "1200 Coulombs (Q = 600 / 0.5)",
            "0.05 Coulombs (Q = 0.5 / 10)"
        ],
        "answer_index": 0,
        "tags": [None, "MATH_UNITS", "MATH_UNITS", "MATH_UNITS"],
        "reasoning_options": [
            "Time must be in SI units (seconds): 10 min = 600 s. Q = I * t = 0.5 A * 600 s = 300 C.",
            "Substituted minutes directly without converting to seconds (Q = 0.5 * 10 = 5 C).",
            "Divided time by current instead of multiplying.",
            "Divided current by minutes."
        ],
        "explanation": "Electric current is the rate of flow of charge: I = Q / t => Q = I * t. Time t = 10 min = 10 * 60 = 600 seconds. Thus Q = 0.5 A * 600 s = 300 C.",
        "diagram_alt": "Circuit diagram with battery, ammeter reading 0.5 A, and bulb running for 600 seconds.",
        "followup_probe": "If one electron carries 1.6 x 10^-19 C, how many electrons flow in 300 C?",
        "source_note": "NCERT Class 10 Ch 11 Section 11.1 Example 11.1",
        "is_ai": False,
    },
    {
        "id": "diag_30_18",
        "cluster": "Electricity",
        "concept": "C2",
        "legacy_concept": "pd",
        "difficulty_label": 1,
        "question": "How much work is done in moving a charge of 2 Coulombs across two terminals having a potential difference of 12 Volts?",
        "options": [
            "24 Joules (W = V * Q = 12 V * 2 C)",
            "6 Joules (W = 12 / 2)",
            "0.167 Joules (W = 2 / 12)",
            "14 Joules (W = 12 + 2)"
        ],
        "answer_index": 0,
        "tags": [None, "V_I_CONFUSION", "V_I_CONFUSION", None],
        "reasoning_options": [
            "Potential difference V is work done per unit charge (V = W/Q) => W = V * Q = 12 * 2 = 24 J.",
            "Divided voltage by charge instead of multiplying.",
            "Divided charge by voltage.",
            "Added voltage and charge numbers directly."
        ],
        "explanation": "By definition, the electric potential difference between two points is the work done W in moving a unit charge Q from one point to the other: V = W / Q => W = V * Q = 12 V * 2 C = 24 J.",
        "diagram_alt": "Two terminals marked A and B with 12 V potential difference and 2 C charge moving between them.",
        "followup_probe": "Why is an instrument that measures potential difference connected in parallel across the component rather than in series?",
        "source_note": "NCERT Class 10 Ch 11 Section 11.2 Example 11.2",
        "is_ai": False,
    },
    {
        "id": "diag_30_19",
        "cluster": "Electricity",
        "concept": "C4",
        "legacy_concept": "ohm",
        "difficulty_label": 2,
        "question": "According to Ohm's law, a student plots a V-I graph with Potential Difference (V) on the vertical y-axis and Current (I) on the horizontal x-axis for a metallic wire at constant temperature. What does the slope of this graph represent?",
        "options": [
            "The electrical resistance (R = delta_V / delta_I) of the wire",
            "The electrical conductance (1/R) of the wire",
            "The total electric power dissipated by the wire",
            "The quantity of electric charge stored in the wire"
        ],
        "answer_index": 0,
        "tags": [None, "MATH_GRAPHS", "POWER_ENERGY", "CURRENT_CONSUMED"],
        "reasoning_options": [
            "Ohm's law gives V = I * R. In a V vs I plot, slope = delta_V / delta_I = R.",
            "Confused with an I vs V graph (where I is on y-axis, whose slope is 1/R).",
            "Confused resistance with power (P = V * I, area/product not slope).",
            "Believes wire stores charge like a capacitor."
        ],
        "explanation": "Ohm's law states that V is directly proportional to I at constant temperature: V = IR. On a graph with V on the vertical axis and I on the horizontal axis, the slope is delta_V / delta_I = R, which is the resistance of the conductor.",
        "diagram_alt": "Linear V-I graph passing through origin with slope delta_V / delta_I = R.",
        "followup_probe": "If wire A has a steeper V-I slope than wire B, which wire has higher resistance?",
        "source_note": "NCERT Class 10 Ch 11 Section 11.3",
        "is_ai": False,
    },
    {
        "id": "diag_30_20",
        "cluster": "Electricity",
        "concept": "C5",
        "legacy_concept": "resistance",
        "difficulty_label": 2,
        "question": "A cylindrical metallic wire of length l, cross-sectional area A, and resistance R is stretched uniformly to double its original length (2l) without changing its volume. What is its new resistance?",
        "options": [
            "4R, because stretching to double length halves the cross-sectional area (A/2)",
            "2R, because resistance is proportional to length only",
            "R/2, because the wire became thinner and electrons pass easier",
            "R, because it is made of the same material with unchanged resistivity"
        ],
        "answer_index": 0,
        "tags": [None, "M6", "M6", "M6"],
        "reasoning_options": [
            "Volume V = l * A is conserved. Doubling length (2l) forces area to halve (A/2). R' = rho * (2l) / (A/2) = 4 * (rho * l / A) = 4R.",
            "Only accounted for the doubling of length, ignoring the thinning of the wire.",
            "Incorrectly assumed thinning decreases resistance.",
            "Confused intrinsic resistivity (rho, unchanged) with geometry-dependent resistance (R, quadrupled)."
        ],
        "explanation": "Since mass and volume remain constant: Volume = l * A = (2l) * A' => A' = A / 2. New resistance R' = rho * l' / A' = rho * (2l) / (A/2) = 4 * (rho * l / A) = 4R.",
        "diagram_alt": "Wire before stretching (length l, area A) and after stretching (length 2l, area A/2).",
        "followup_probe": "Does the resistivity (rho) of the stretched wire change?",
        "source_note": "NCERT Class 10 Ch 11 Section 11.4 Example 11.6",
        "is_ai": False,
    },
    {
        "id": "diag_30_21",
        "cluster": "Electricity",
        "concept": "C7",
        "legacy_concept": "series",
        "difficulty_label": 2,
        "question": "Two resistors of 10 Ohms and 20 Ohms are connected in series with a 6 V battery and an ammeter. Which statement is physically TRUE about this circuit?",
        "options": [
            "The exact same current (0.2 A) passes through both the 10 Ohm and the 20 Ohm resistor",
            "The 10 Ohm resistor consumes half the current before it reaches the 20 Ohm resistor",
            "The 20 Ohm resistor has a larger current because it has larger resistance",
            "The total circuit resistance is 6.67 Ohms"
        ],
        "answer_index": 0,
        "tags": [None, "CURRENT_CONSUMED", "V_I_CONFUSION", "PARALLEL_ADDITION"],
        "reasoning_options": [
            "In a series circuit, there is only one continuous conducting loop. Charge is conserved, so current I is strictly identical everywhere: I = V / R_total = 6 / 30 = 0.2 A.",
            "Harbours the persistent CURRENT_CONSUMED misconception that earlier components 'eat up' current.",
            "Confused voltage drop (which is higher across 20 Ohms) with current.",
            "Applied parallel resistance formula to a series connection."
        ],
        "explanation": "In a series combination, the current is invariant throughout the circuit. Total resistance is R_s = 10 + 20 = 30 Ohms. The current from the battery is I = 6 V / 30 Ohms = 0.2 A, and this exact same 0.2 A passes through every element in the loop.",
        "diagram_alt": "Series circuit with 6V battery, ammeter reading 0.2A, 10 Ohm resistor, and 20 Ohm resistor in single loop.",
        "followup_probe": "What is the potential difference across the 20 Ohm resistor in this series circuit?",
        "source_note": "NCERT Class 10 Ch 11 Section 11.6.1; Blueprint Section 9 CURRENT_CONSUMED",
        "is_ai": False,
    },
    {
        "id": "diag_30_22",
        "cluster": "Electricity",
        "concept": "C8",
        "legacy_concept": "parallel",
        "difficulty_label": 2,
        "question": "Two resistors of 10 Ohms each are connected in parallel across a 12 V power supply. What is the equivalent resistance of the combination and the total current drawn?",
        "options": [
            "Equivalent resistance is 5 Ohms; total current drawn is 2.4 A",
            "Equivalent resistance is 20 Ohms; total current drawn is 0.6 A",
            "Equivalent resistance is 10 Ohms; total current drawn is 1.2 A",
            "Equivalent resistance is 100 Ohms; total current drawn is 0.12 A"
        ],
        "answer_index": 0,
        "tags": [None, "PARALLEL_ADDITION", "PARALLEL_ADDITION", None],
        "reasoning_options": [
            "Parallel formula: 1/Rp = 1/10 + 1/10 = 2/10 => Rp = 5 Ohms. Total current I = V / Rp = 12 / 5 = 2.4 A.",
            "Added resistances directly (10 + 10 = 20 Ohms), treating parallel branches as series.",
            "Assumed parallel resistances do not change the branch resistance (Rp = 10 Ohms).",
            "Multiplied resistances directly."
        ],
        "explanation": "In parallel combination: 1/Rp = 1/R1 + 1/R2 = 1/10 + 1/10 = 2/10 = 1/5 => Rp = 5 Ohms. The total current drawn from the 12 V source is I = V / Rp = 12 / 5 = 2.4 A (each branch draws 1.2 A).",
        "diagram_alt": "Parallel circuit with 12V battery dividing into two parallel 10 Ohm branches, each carrying 1.2 A.",
        "followup_probe": "Why does adding another parallel branch to your house circuit increase total current drawn from the main supply?",
        "source_note": "NCERT Class 10 Ch 11 Section 11.6.2; Blueprint Section 9 PARALLEL_ADDITION",
        "is_ai": False,
    },
    {
        "id": "diag_30_23",
        "cluster": "Electricity",
        "concept": "C11",
        "legacy_concept": "power",
        "difficulty_label": 2,
        "question": "According to Joule's law of heating (H = I^2 R t), if the current passing through a fixed heating resistor is doubled, what happens to the rate of heat production?",
        "options": [
            "It quadruples (increases by a factor of 4)",
            "It doubles (increases by a factor of 2)",
            "It remains constant because resistance is fixed",
            "It halves because current flows faster"
        ],
        "answer_index": 0,
        "tags": [None, "V_I_CONFUSION", "POWER_ENERGY", None],
        "reasoning_options": [
            "Heat produced is proportional to the square of current (H proportional to I^2). (2I)^2 = 4I^2.",
            "Assumed linear relationship between heat and current (H proportional to I).",
            "Forgot that current drives heating dissipation.",
            "Confused speed with power dissipation."
        ],
        "explanation": "Joule's law states that heat generated H = I^2 * R * t. When current I is doubled to 2I while R and t are kept constant: H' = (2I)^2 * R * t = 4 * (I^2 * R * t) = 4H. Heat generation quadruples.",
        "diagram_alt": "Graph showing parabolic heat production H vs Current I (H proportional to I^2).",
        "followup_probe": "If voltage V across a fixed resistor is doubled, by what factor does power dissipation increase?",
        "source_note": "NCERT Class 10 Ch 11 Section 11.7",
        "is_ai": False,
    },
    {
        "id": "diag_30_24",
        "cluster": "Electricity",
        "concept": "C13",
        "legacy_concept": "power",
        "difficulty_label": 2,
        "question": "An electric refrigerator rated at 400 W operates for 8 hours per day. What is the cost of energy to operate it for 30 days at a domestic tariff rate of Rs 5.00 per kilowatt-hour (kWh)?",
        "options": [
            "Rs 480 (Total energy = 0.4 kW * 8 h/day * 30 days = 96 kWh; 96 * 5 = Rs 480)",
            "Rs 48,000 (Calculated using Watts without converting to kilowatts)",
            "Rs 60 (Only calculated for 1 day: 0.4 * 8 * 5)",
            "Rs 96 (Calculated units but forgot multiplying by cost per unit)"
        ],
        "answer_index": 0,
        "tags": [None, "MATH_UNITS", "POWER_ENERGY", "MATH_UNITS"],
        "reasoning_options": [
            "Power in kW = 400 W / 1000 = 0.4 kW. Total energy in 30 days = 0.4 kW * 8 h * 30 = 96 kWh. Cost = 96 kWh * Rs 5 = Rs 480.",
            "Forgot to divide 400 W by 1000 to convert to kilowatt-hours.",
            "Calculated billing for a single day instead of the full 30-day month.",
            "Computed the total energy units (96 kWh) but omitted the tariff multiplier."
        ],
        "explanation": "Energy in 30 days = Power (in kW) * Time (in hours) = (400/1000 kW) * (8 * 30 h) = 0.4 kW * 240 h = 96 kWh. Total cost = 96 kWh * Rs 5.00/kWh = Rs 480.",
        "diagram_alt": "Electric energy meter calculating units: 400 W appliance * 240 hours = 96 kWh * Rs 5 = Rs 480.",
        "followup_probe": "How many Joules are equivalent to 1 kWh of electrical energy?",
        "source_note": "NCERT Class 10 Ch 11 Section 11.8 Example 11.14",
        "is_ai": False,
    },

    # --- CLUSTER 5: MAGNETISM (6 items) ---
    {
        "id": "diag_30_25",
        "cluster": "Magnetism",
        "concept": "M1",
        "legacy_concept": "magnetic_field",
        "difficulty_label": 1,
        "question": "Which of the following is a fundamental physical property of magnetic field lines around a bar magnet?",
        "options": [
            "No two magnetic field lines ever cross or intersect each other",
            "Magnetic field lines are open curves starting from North and disappearing in space",
            "Magnetic field lines cross at right angles near the neutral points",
            "Field lines are least crowded near the poles where the field is strongest"
        ],
        "answer_index": 0,
        "tags": [None, "M15", "M15", "M15"],
        "reasoning_options": [
            "If two lines crossed, a compass needle placed at the intersection would have to point in two different directions simultaneously, which is impossible.",
            "Field lines are closed continuous loops (North to South outside, South to North inside).",
            "Field lines never intersect at any point in space.",
            "Crowding of lines indicates field strength; lines are most concentrated at poles."
        ],
        "explanation": "Magnetic field lines never intersect. If they did, it would mean that at the point of intersection, the magnetic field has two distinct directions, which is physically impossible.",
        "diagram_alt": "Bar magnet with smooth continuous closed loops of magnetic field lines emerging from North and entering South.",
        "followup_probe": "What is the direction of magnetic field lines INSIDE a bar magnet?",
        "source_note": "NCERT Class 10 Ch 12 Section 12.1",
        "is_ai": False,
    },
    {
        "id": "diag_30_26",
        "cluster": "Magnetism",
        "concept": "M2",
        "legacy_concept": "current_magnetism",
        "difficulty_label": 2,
        "question": "A heavy vertical copper wire carries an electric current upward through a horizontal cardboard. What is the pattern and direction of the magnetic field lines formed on the cardboard?",
        "options": [
            "Concentric circles centered on the wire, directed counter-clockwise when viewed from above",
            "Concentric circles directed clockwise when viewed from above",
            "Straight lines radiating outward like spokes of a bicycle wheel",
            "Parallel horizontal lines directed from North to South"
        ],
        "answer_index": 0,
        "tags": [None, "FIELD_DIRECTION", "FIELD_DIRECTION", "FIELD_DIRECTION"],
        "reasoning_options": [
            "By Maxwell's Right-Hand Thumb Rule: thumb pointing UP -> fingers curl in counter-clockwise direction around the wire.",
            "Inverted hand orientation, confusing clockwise with counter-clockwise.",
            "Confused magnetic field lines around a straight wire with electric field lines radiating from a point charge.",
            "Assumed uniform external field pattern."
        ],
        "explanation": "The magnetic field lines around a straight current conductor are concentric circles. Using the Right-Hand Thumb Rule with thumb pointing upwards (in current direction), the fingers curl counter-clockwise when viewed from above.",
        "diagram_alt": "Vertical wire piercing horizontal card with upward current and concentric counter-clockwise magnetic rings.",
        "followup_probe": "If distance r from the wire is doubled, what happens to the magnetic field strength B?",
        "source_note": "NCERT Class 10 Ch 12 Section 12.2.1",
        "is_ai": False,
    },
    {
        "id": "diag_30_27",
        "cluster": "Magnetism",
        "concept": "M3",
        "legacy_concept": "current_magnetism",
        "difficulty_label": 1,
        "question": "A current through a horizontal power line flows along the East-to-West direction. What is the direction of the magnetic field at a point directly BELOW the power line?",
        "options": [
            "Toward the North",
            "Toward the South",
            "Toward the East",
            "Toward the West"
        ],
        "answer_index": 0,
        "tags": [None, "FIELD_DIRECTION", "FIELD_DIRECTION", "FIELD_DIRECTION"],
        "reasoning_options": [
            "Point right thumb to the West (current). Below the line, fingers curl pointing toward the North.",
            "Curled fingers upward instead of checking the point below the line.",
            "Confused field direction with direction of current flow.",
            "Confused field direction with anti-parallel flow."
        ],
        "explanation": "Applying the Right-Hand Thumb Rule: Point the right thumb toward the West. At points directly below the wire, the curling fingers point towards the North. At points directly above, they point toward the South.",
        "diagram_alt": "Wire aligned East-West with current flowing West; right hand curled showing field pointing North below wire.",
        "followup_probe": "What is the direction of the magnetic field at a point directly ABOVE the power line?",
        "source_note": "NCERT Class 10 Ch 12 Section 12.2.1 Example 12.1",
        "is_ai": False,
    },
    {
        "id": "diag_30_28",
        "cluster": "Magnetism",
        "concept": "M5",
        "legacy_concept": "current_magnetism",
        "difficulty_label": 2,
        "question": "A long cylindrical coil of insulated copper wire wound in a helix is called a solenoid. What is true about the magnetic field INSIDE a current-carrying solenoid?",
        "options": [
            "It is completely uniform and identical at all points, represented by parallel straight lines",
            "It is zero at the center and maximum at the outer surface",
            "It decreases linearly from the ends toward the middle",
            "It is turbulent and points in random directions"
        ],
        "answer_index": 0,
        "tags": [None, "FIELD_DIRECTION", "FIELD_DIRECTION", None],
        "reasoning_options": [
            "Inside a solenoid, the individual circular loop fields superpose to form a dense, uniform, axial magnetic field (similar to inside a bar magnet).",
            "Believes current inside a coil cancels out at the geometric axis.",
            "Assumed field weakens in the center.",
            "Assumed magnetic fields in coils are chaotic."
        ],
        "explanation": "The magnetic field lines inside a current-carrying solenoid are in the form of parallel straight lines. This indicates that the magnetic field is uniform and has the same strength at all interior points.",
        "diagram_alt": "Solenoid coil carrying current, showing uniform parallel field lines through its core and bar-magnet-like exterior loops.",
        "followup_probe": "What happens to the internal field when a soft iron rod is inserted into the solenoid core?",
        "source_note": "NCERT Class 10 Ch 12 Section 12.2.3",
        "is_ai": False,
    },
    {
        "id": "diag_30_29",
        "cluster": "Magnetism",
        "concept": "M7",
        "legacy_concept": "magnetic_force",
        "difficulty_label": 2,
        "question": "According to Fleming's Left-Hand Rule, what do the Forefinger, Centre finger, and Thumb represent when determining the force on a current conductor in a magnetic field?",
        "options": [
            "Forefinger: Magnetic Field; Centre finger: Current; Thumb: Motion / Mechanical Force",
            "Forefinger: Current; Centre finger: Magnetic Field; Thumb: Voltage",
            "Forefinger: Force; Centre finger: Current; Thumb: Magnetic Field",
            "Forefinger: Motion; Centre finger: Earth; Thumb: Electric Charge"
        ],
        "answer_index": 0,
        "tags": [None, "FIELD_DIRECTION", "FIELD_DIRECTION", None],
        "reasoning_options": [
            "Mnemonic FBI or Father-Mother-Child: Thumb = Force/Motion, Forefinger = Field (B), Centre finger = Current (I).",
            "Swapped Forefinger and Centre finger assignments.",
            "Swapped Thumb and Forefinger assignments.",
            "Confused Fleming's rule with domestic earthing terminology."
        ],
        "explanation": "According to Fleming's Left-Hand Rule, stretch thumb, forefinger and middle finger mutually perpendicular: Forefinger points in direction of magnetic Field, middle (centre) finger in direction of Current, and Thumb points in direction of Motion or Force.",
        "diagram_alt": "Fleming's left hand: Forefinger = Field, Middle finger = Current, Thumb = Force.",
        "followup_probe": "Under what orientation between current and magnetic field is the mechanical force maximum?",
        "source_note": "NCERT Class 10 Ch 12 Section 12.3; Blueprint Section 9 FIELD_DIRECTION",
        "is_ai": False,
    },
    {
        "id": "diag_30_30",
        "cluster": "Magnetism",
        "concept": "M10",
        "legacy_concept": "domestic_circuits",
        "difficulty_label": 1,
        "question": "What is the primary function of the green Earth Wire in a domestic 220V AC household circuit?",
        "options": [
            "It conducts fault leakage current safely into the ground with low resistance, preventing severe electric shocks from metal appliances",
            "It supplies return current back to the power station during normal operation",
            "It boosts appliance power efficiency by filtering voltage fluctuations",
            "It serves as a backup live wire in case of a power cut"
        ],
        "answer_index": 0,
        "tags": [None, "M3", None, None],
        "reasoning_options": [
            "Metallic appliances are connected to the earth wire. If live insulation frays and touches the metal casing, current takes the zero-resistance earth path, tripping the fuse instead of shocking a user.",
            "Confused green earth wire with the black neutral wire.",
            "Attributed voltage stabilizing capabilities to earthing.",
            "Believes earth wire carries reserve live power."
        ],
        "explanation": "The metallic body of appliances (toaster, iron, refrigerator) is connected to the earth wire, which provides a low-resistance conducting path for current. Any leakage of current to the metallic body flows directly to ground without passing through the human body.",
        "diagram_alt": "Domestic 3-pin plug showing Live (brown/red), Neutral (blue/black), and Earth (green/yellow) connected to appliance casing.",
        "followup_probe": "Why is an electric fuse always placed in series with the live wire rather than the neutral wire?",
        "source_note": "NCERT Class 10 Ch 12 Section 12.5",
        "is_ai": False,
    },
]

def get_diagnostic_30_questions() -> List[Dict[str, Any]]:
    """Returns the official 30-item Chapter-Balanced Diagnostic Assessment per Blueprint Section 7."""
    return list(DIAGNOSTIC_30_BLUEPRINT)

def get_mock_exam_questions(n: int = 10) -> List[Dict[str, Any]]:
    """
    Returns a balanced 10-item mock exam drawn across all 4 chapters:
    - Light (3 items)
    - Human Eye (2 items)
    - Electricity (3 items)
    - Magnetism (2 items)
    """
    mock_ids = [
        "q_lgt_mir_03", "q_lgt_len_03", "q_lgt_pow_02",  # Light (3)
        "q_eye_def_03", "q_eye_prs_02",                  # Human Eye (2)
        "q_ohm_03", "q_ser_02", "q_par_03",              # Electricity (3)
        "q_mag_fld_03", "q_mag_frc_03",                  # Magnetism (2)
    ]
    items = []
    for qid in mock_ids[:n]:
        q = get_question_by_id(qid)
        if q:
            items.append(q)
    # If any missing, fallback to question bank
    if len(items) < n:
        for q in QUESTION_BANK:
            if q not in items:
                items.append(q)
            if len(items) >= n:
                break
    return items[:n]


def get_question_by_id(item_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve question entry by ID from either QUESTION_BANK or DIAGNOSTIC_30_BLUEPRINT."""
    for q in QUESTION_BANK:
        if q["id"] == item_id:
            return q
    for q in DIAGNOSTIC_30_BLUEPRINT:
        if q["id"] == item_id:
            return q
    return None

def get_questions_for_concept(concept: str) -> List[Dict[str, Any]]:
    """Return all verified questions for a given concept (canonical or legacy)."""
    results = [q for q in QUESTION_BANK if q["concept"] == concept or q.get("canonical_concept") == concept]
    if not results:
        results = [q for q in DIAGNOSTIC_30_BLUEPRINT if q.get("concept") == concept or q.get("legacy_concept") == concept]
    return results
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
