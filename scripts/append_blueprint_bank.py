"""scripts/append_blueprint_bank.py - Adds the official 30-item Chapter-Balanced Blueprint to bank.py"""

import os

blueprint_code = '''

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

'''

with open("core/bank.py", "r", encoding="utf-8") as f:
    original = f.read()

# Replace get_question_by_id and get_questions_for_concept to search both lists
replacement_helpers = '''
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
'''

# Find insertion spot right before get_question_by_id
idx = original.find("def get_question_by_id")
if idx != -1:
    idx2 = original.find("def get_diagnostic_questions", idx)
    updated = original[:idx] + blueprint_code + replacement_helpers + original[idx2:]
    with open("core/bank.py", "w", encoding="utf-8") as f:
        f.write(updated)
    print("Successfully updated bank.py with 30-item Blueprint and unified search!")
else:
    print("Could not locate insertion point in bank.py")
