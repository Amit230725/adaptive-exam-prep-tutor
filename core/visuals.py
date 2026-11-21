"""core/visuals.py - High-Impact Educational Visualizations & Interactive Widgets

Contains:
1. Dynamic SVG Cognitive Mastery Radar Chart (Spider Chart) across any chapter or syllabus scope
2. Interactive Virtual Circuit Simulator & Misconception Buster (Series vs Parallel)
3. Full Syllabus NCERT Study Guide & Formula Reference Cards across all 4 Class 10 Physics chapters
"""

import math
from typing import Dict, Any, List, Optional
from core.concepts import CONCEPTS, CHAPTERS

def generate_mastery_radar_chart_svg(
    mastery_dict: Dict[str, float],
    concept_keys: Optional[List[str]] = None,
    width: int = 500,
    height: int = 420,
) -> str:
    """
    Generates a pure SVG multi-axis Radar/Spider chart representing the student's
    cognitive mastery vector across selected syllabus topics or chapters.
    Lightweight, crisp on retina/mobile screens, zero heavy charting dependencies.
    """
    if not concept_keys:
        # Default to provided keys if <= 8, else electricity chapter defaults
        available = [k for k in mastery_dict.keys() if k in CONCEPTS]
        if available and len(available) <= 8:
            concept_keys = available
        else:
            concept_keys = [
                "charge", "current", "pd", "ohm",
                "resistance", "series", "parallel", "power"
            ]

    # Filter to valid concepts
    valid_keys = [k for k in concept_keys if k in CONCEPTS]
    if len(valid_keys) < 3:
        valid_keys = list(CONCEPTS.keys())[:8]

    n_axes = len(valid_keys)
    cx, cy = width / 2, height / 2 + 10
    
    # Scale radius and font size according to number of axes
    if n_axes > 10:
        radius = min(width, height) * 0.31
        font_sz = 9
    else:
        radius = min(width, height) * 0.36
        font_sz = 11

    # Concentric background grid polygons (25%, 50%, 75%, 100%)
    grid_svg = []
    for level in [0.25, 0.50, 0.75, 1.0]:
        r_level = radius * level
        pts = []
        for i in range(n_axes):
            angle = (2 * math.pi / n_axes) * i - (math.pi / 2)
            x = cx + r_level * math.cos(angle)
            y = cy + r_level * math.sin(angle)
            pts.append(f"{x:.1f},{y:.1f}")
        stroke_color = "#D1D5DB" if level < 1.0 else "#9CA3AF"
        dash = 'stroke-dasharray="3,3"' if level in [0.25, 0.75] else ""
        grid_svg.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="{stroke_color}" stroke-width="1" {dash} />')

    # Axis spokes and labels
    spokes_svg = []
    labels_svg = []
    data_points = []

    for i, cid in enumerate(valid_keys):
        angle = (2 * math.pi / n_axes) * i - (math.pi / 2)
        # Spoke line
        x_end = cx + radius * math.cos(angle)
        y_end = cy + radius * math.sin(angle)
        spokes_svg.append(f'<line x1="{cx}" y1="{cy}" x2="{x_end:.1f}" y2="{y_end:.1f}" stroke="#E5E7EB" stroke-width="1.2" />')

        # Data polygon point
        m_val = max(0.05, min(1.0, mastery_dict.get(cid, 0.3)))
        r_data = radius * m_val
        x_data = cx + r_data * math.cos(angle)
        y_data = cy + r_data * math.sin(angle)
        data_points.append(f"{x_data:.1f},{y_data:.1f}")

        # Text label with percentage
        r_label = radius * (1.26 if n_axes > 10 else 1.22)
        x_label = cx + r_label * math.cos(angle)
        y_label = cy + r_label * math.sin(angle)
        
        # Abbreviate concept title for clean display
        c_name = CONCEPTS[cid]["name"].split("&")[0].split("(")[0].replace(" Circuits", "").replace("Spherical ", "").strip()
        pct_text = f"{int(m_val * 100)}%"
        
        # Determine anchor
        if abs(math.cos(angle)) < 0.2:
            anchor = "middle"
        elif math.cos(angle) > 0:
            anchor = "start"
        else:
            anchor = "end"

        # Label color based on threshold
        color = "#1B998B" if m_val >= 0.70 else "#F4A300" if m_val >= 0.40 else "#D1495B"

        labels_svg.append(f'''
            <text x="{x_label:.1f}" y="{y_label:.1f}" text-anchor="{anchor}" font-family="Inter, sans-serif" font-size="{font_sz}" font-weight="600" fill="#14213D">
                {c_name} <tspan fill="{color}" font-weight="700">({pct_text})</tspan>
            </text>
        ''')

    # Student Mastery polygon
    data_poly = f'<polygon points="{" ".join(data_points)}" fill="rgba(244, 163, 0, 0.35)" stroke="#F4A300" stroke-width="2.5" />'

    # Mastery data point circles
    circles_svg = []
    for pt in data_points:
        px, py = pt.split(",")
        circles_svg.append(f'<circle cx="{px}" cy="{py}" r="4.0" fill="#F4A300" stroke="#FFFFFF" stroke-width="1.5" />')

    # Target Benchmark line (70% mastery boundary in subtle green)
    target_points = []
    for i in range(n_axes):
        angle = (2 * math.pi / n_axes) * i - (math.pi / 2)
        r_t = radius * 0.70
        xt = cx + r_t * math.cos(angle)
        yt = cy + r_t * math.sin(angle)
        target_points.append(f"{xt:.1f},{yt:.1f}")
    target_poly = f'<polygon points="{" ".join(target_points)}" fill="none" stroke="#1B998B" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.75" />'

    svg_content = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" style="max-width:100%; height:auto; display:block; margin:auto;">
        <style>
            .legend-text {{ font-family: 'Inter', sans-serif; font-size: 11px; fill: #4B5563; }}
        </style>
        <!-- Background Grids -->
        {''.join(grid_svg)}
        <!-- Spokes -->
        {''.join(spokes_svg)}
        <!-- Target 70% Mastery Threshold -->
        {target_poly}
        <!-- Student Mastery Shape -->
        {data_poly}
        {''.join(circles_svg)}
        <!-- Labels -->
        {''.join(labels_svg)}
        <!-- Legend -->
        <g transform="translate({cx - 130}, 20)">
            <rect x="0" y="0" width="12" height="12" fill="rgba(244, 163, 0, 0.4)" stroke="#F4A300" stroke-width="1.5" rx="2" />
            <text x="18" y="10" class="legend-text">Your Mastery</text>
            <line x1="110" y1="6" x2="130" y2="6" stroke="#1B998B" stroke-width="2" stroke-dasharray="3,3" />
            <text x="136" y="10" class="legend-text">70% Target Threshold</text>
        </g>
    </svg>
    """
    return svg_content

def simulate_circuit(
    mode: str,  # "series" or "parallel"
    voltage: float,
    r1: float,
    r2: float,
) -> Dict[str, Any]:
    """
    Simulates electrical circuit parameters for live interactive learning.
    Directly busts misconceptions M1 (current used up), M2 (constant current),
    M5 (parallel increases R), and M7 (parallel current splits equally).
    """
    v = max(0.5, float(voltage))
    r_1 = max(0.5, float(r1))
    r_2 = max(0.5, float(r2))

    if mode.lower() == "series":
        r_eq = r_1 + r_2
        i_tot = v / r_eq
        i_1 = i_tot
        i_2 = i_tot
        v_1 = i_1 * r_1
        v_2 = i_2 * r_2
        p_1 = v_1 * i_1
        p_2 = v_2 * i_2
        p_tot = v * i_tot
        explanation = (
            f"In series, identical current ({i_tot:.2f} A) flows through BOTH resistors (I_tot = I1 = I2). "
            f"Voltage divides proportionally: V1 = {v_1:.2f} V and V2 = {v_2:.2f} V."
        )
        misconception_note = (
            "💡 Notice: Ammeter before R1 and after R2 would read the EXACT same current. "
            "Current is never 'used up' (Busts Misconception M1)!"
        )
    else:  # Parallel
        r_eq = (r_1 * r_2) / (r_1 + r_2)
        i_tot = v / r_eq
        v_1 = v
        v_2 = v
        i_1 = v / r_1
        i_2 = v / r_2
        p_1 = v * i_1
        p_2 = v * i_2
        p_tot = v * i_tot
        explanation = (
            f"In parallel, both branches receive full battery voltage ({v:.1f} V). "
            f"Equivalent resistance drops to {r_eq:.2f} Ω, which is SMALLER than both R1 ({r_1} Ω) and R2 ({r_2} Ω). "
            f"Branch currents divide inversely: I1 = {i_1:.2f} A, I2 = {i_2:.2f} A."
        )
        misconception_note = (
            f"💡 Notice: Connecting {r_2} Ω in parallel with {r_1} Ω reduced total resistance to {r_eq:.2f} Ω, "
            f"drawing MORE total current ({i_tot:.2f} A) from the cell. Adding parallel branches DECREASES total resistance (Busts Misconception M5)!"
        )

    return {
        "mode": mode.capitalize(),
        "v_source": v,
        "r1": r_1,
        "r2": r_2,
        "r_eq": round(r_eq, 2),
        "i_total": round(i_tot, 2),
        "i1": round(i_1, 2),
        "i2": round(i_2, 2),
        "v1": round(v_1, 2),
        "v2": round(v_2, 2),
        "p1": round(p_1, 2),
        "p2": round(p_2, 2),
        "p_total": round(p_tot, 2),
        "explanation": explanation,
        "misconception_note": misconception_note,
    }

# -----------------------------------------------------------------------------
# FULL SYLLABUS NCERT CLASS 10 PHYSICS QUICK REFERENCE STUDY CARDS (20 Topics)
# -----------------------------------------------------------------------------
CONCEPT_STUDY_CARDS: Dict[str, Dict[str, Any]] = {
    # --- CHAPTER 9: LIGHT ---
    "reflection_mirrors": {
        "title": "Spherical Mirrors & Reflection",
        "chapter": "Light – Reflection & Refraction",
        "formulas": [
            "f = R / 2",
            "1/v + 1/u = 1/f (Mirror Formula)",
            "m = h' / h = -v / u (Magnification)",
            "Cartesian Sign: u is always negative; f is negative for concave, positive for convex",
        ],
        "summary": "Concave mirrors converge light and can form real (inverted) or virtual (erect) images depending on object distance. Convex mirrors always diverge light, producing diminished virtual images with a wide field of view.",
        "common_trap": "Believing an optical image resides physically on the mirror glass face rather than at the ray convergence plane in space (M8).",
    },
    "refraction_laws": {
        "title": "Refraction of Light & Snell's Law",
        "chapter": "Light – Reflection & Refraction",
        "formulas": [
            "sin i / sin r = constant = n_21 (Snell's Law)",
            "n = c / v (Absolute Refractive Index)",
            "n_21 = v1 / v2 = n2 / n1",
            "Speed in vacuum: c ≈ 3.0 × 10^8 m/s",
        ],
        "summary": "Refraction is the bending of light when it passes obliquely from one transparent medium to another due to change in speed. Ray bends towards the normal when entering an optically denser medium.",
        "common_trap": "Assuming light rays lose speed or distance energy simply by traveling across clear air (M11).",
    },
    "refraction_lenses": {
        "title": "Spherical Lenses & Ray Optics",
        "chapter": "Light – Reflection & Refraction",
        "formulas": [
            "1/v - 1/u = 1/f (Lens Formula)",
            "m = h' / h = +v / u (Magnification)",
            "Convex lens: f is positive (converging)",
            "Concave lens: f is negative (diverging)",
        ],
        "summary": "Convex lenses converge light rays to a real focus. Concave lenses diverge parallel rays. Ray passing through the optical centre passes undeviated.",
        "common_trap": "Assuming that covering half of a lens cuts the formed image in half (M9). In reality, a complete image is formed, only dimmer.",
    },
    "lens_power": {
        "title": "Power of a Lens & Combinations",
        "chapter": "Light – Reflection & Refraction",
        "formulas": [
            "P = 1 / f (f in meters)",
            "SI Unit: Dioptre (1 D = 1 m^-1)",
            "P_net = P1 + P2 + ... + Pn (Lenses in Contact)",
            "Convex: P > 0; Concave: P < 0",
        ],
        "summary": "Power is the measure of convergence or divergence a lens introduces. A lens of short focal length bends rays more sharply and has higher optical power.",
        "common_trap": "Calculating lens power using focal length in centimeters instead of converting to meters first.",
    },

    # --- CHAPTER 10: HUMAN EYE ---
    "eye_vision": {
        "title": "Human Eye Anatomy & Accommodation",
        "chapter": "Human Eye & Colourful World",
        "formulas": [
            "Near Point (D) = 25 cm (Least distance of distinct vision)",
            "Far Point = Infinity",
            "Ciliary muscles relax ==> Lens thins ==> f increases (Distant objects)",
            "Ciliary muscles contract ==> Lens thickens ==> f decreases (Near objects)",
        ],
        "summary": "The eye forms an inverted real image on the photosensitive retina. Accommodation is the eye's ability to adjust its focal length via flexible ciliary muscles.",
        "common_trap": "Believing vision occurs by the eyes projecting active rays outwards to illuminate objects (M13).",
    },
    "defects_vision": {
        "title": "Defects of Vision & Lens Correction",
        "chapter": "Human Eye & Colourful World",
        "formulas": [
            "Myopia (Near-sighted): Image in front of retina ==> Correct with Concave Lens (P < 0)",
            "Hypermetropia (Far-sighted): Image behind retina ==> Correct with Convex Lens (P > 0)",
            "Presbyopia: Aging ciliary muscles ==> Correct with Bifocal Lenses",
        ],
        "summary": "Myopic individuals cannot clearly see distant objects; hypermetropic individuals cannot see nearby objects distinctly. Corrective lenses restore focus directly onto the retina.",
        "common_trap": "Confusing myopia with hypermetropia or prescribing a convex lens for near-sightedness (M12).",
    },
    "prism_dispersion": {
        "title": "Prism Refraction & White Light Dispersion",
        "chapter": "Human Eye & Colourful World",
        "formulas": [
            "VIBGYOR (Violet, Indigo, Blue, Green, Yellow, Orange, Red)",
            "Angle of Deviation D = (i + e) - A",
            "lambda_red > lambda_violet ==> n_violet > n_red",
            "Violet bends most; Red bends least",
        ],
        "summary": "Dispersion is the splitting of white light into its constituent wavelengths. Newton's inverted prism recombination proves that white light already contains all spectrum colors.",
        "common_trap": "Believing the glass prism dyes or generates color chemically rather than simply separating existing wavelengths (M14).",
    },
    "atmospheric_scattering": {
        "title": "Atmospheric Refraction & Rayleigh Scattering",
        "chapter": "Human Eye & Colourful World",
        "formulas": [
            "Rayleigh Scattering: Intensity I ∝ 1 / lambda^4",
            "Early sunrise / delayed sunset: ~2 minutes each (4 mins total)",
            "Apparent star shift due to continuous refractive index gradient",
        ],
        "summary": "Atmospheric refraction causes twinkling of stars and advance sunrise. Fine atmospheric molecules scatter short blue wavelengths, making daytime skies blue, while longer red rays survive to produce red sunsets.",
        "common_trap": "Assuming starlight twinkles because light loses speed over interstellar distances (M11).",
    },

    # --- CHAPTER 11: ELECTRICITY ---
    "charge": {
        "title": "Electric Charge & Quantisation",
        "chapter": "Electricity",
        "formulas": ["Q = n · e", "e = 1.6 × 10^-19 C", "1 C ≈ 6.25 × 10^18 electrons"],
        "summary": "Electric charge is an intrinsic property of subatomic particles. Protons carry positive charge, while free electrons carry negative charge. In solid conductors, current is the drift of free electrons.",
        "common_trap": "Believing a battery generates new charges from nothing; mobile charges already exist throughout the wires (M4).",
    },
    "current": {
        "title": "Electric Current & Rate of Flow",
        "chapter": "Electricity",
        "formulas": ["I = Q / t", "1 A = 1 C / s", "Conventional flow: + to - ; Electron flow: - to +"],
        "summary": "Current is the rate of flow of electric charge through any cross-section. It is measured in series by an ammeter of very low internal resistance.",
        "common_trap": "Assuming current gets consumed or 'used up' by lamps or resistors (M1).",
    },
    "pd": {
        "title": "Potential Difference & Work Done",
        "chapter": "Electricity",
        "formulas": ["V = W / Q", "1 V = 1 J / C", "Measured in parallel by high-resistance voltmeter"],
        "summary": "Potential difference is the work done in moving a unit positive charge between two points in an electric field. The battery maintains this push.",
        "common_trap": "Confusing voltage (energy per charge) with current (rate of charge flow) (M3).",
    },
    "ohm": {
        "title": "Ohm's Law & V-I Characteristics",
        "chapter": "Electricity",
        "formulas": ["V = I · R", "Slope of V vs I = R", "Valid at constant temperature"],
        "summary": "At constant temperature, current through a metallic conductor is directly proportional to the potential difference across its terminals.",
        "common_trap": "Thinking a battery outputs constant amperes into any circuit regardless of resistance (M2).",
    },
    "resistance": {
        "title": "Resistance & Factors Influencing Flow",
        "chapter": "Electricity",
        "formulas": ["R = ρ · l / A", "Thicker wire ==> Lower R", "Longer wire ==> Higher R"],
        "summary": "Resistance is opposition to electron drift. It depends on material resistivity (ρ), length (l), and cross-sectional area (A), but NOT on the applied voltage.",
        "common_trap": "Believing that altering the applied voltage changes the resistance of an ohmic wire (M6).",
    },
    "series": {
        "title": "Series Circuits (Single Conducting Path)",
        "chapter": "Electricity",
        "formulas": ["R_s = R1 + R2 + ... + Rn", "I_tot = I1 = I2", "V_tot = V1 + V2"],
        "summary": "In series, all components share a single loop. If one component burns out, current stops flowing everywhere. Equivalent resistance is always larger than any individual resistor.",
        "common_trap": "Thinking the first resistor gets more current and starves subsequent components (M1).",
    },
    "parallel": {
        "title": "Parallel Circuits (Independent Branches)",
        "chapter": "Electricity",
        "formulas": ["1 / R_p = 1 / R1 + 1 / R2", "V_tot = V1 = V2", "I_tot = I1 + I2"],
        "summary": "In parallel, all branches connect across the same two points, experiencing identical voltage. Total resistance is always less than the smallest individual resistor.",
        "common_trap": "Assuming parallel branches increase total circuit resistance like series circuits do (M5).",
    },
    "power": {
        "title": "Electric Power & Heating Effect",
        "chapter": "Electricity",
        "formulas": ["P = V · I = I^2 · R = V^2 / R", "1 W = 1 J / s", "Heat H = I^2 · R · t (Joule's Law)"],
        "summary": "Electric power is the rate at which electrical energy is transformed into other energy forms. Bulb brightness in a circuit is determined by actual power dissipated, not stamped rating alone.",
        "common_trap": "Assuming a higher-wattage rated bulb always glows brighter in series circuits (M3).",
    },

    # --- CHAPTER 12: MAGNETIC EFFECTS ---
    "magnetic_field": {
        "title": "Magnetic Field & Continuous Field Lines",
        "chapter": "Magnetic Effects of Electric Current",
        "formulas": [
            "Field lines emerge North and enter South externally",
            "Field lines form closed continuous loops",
            "Field lines NEVER intersect (compass cannot point two ways)",
            "Crowding of lines indicates higher magnetic field strength",
        ],
        "summary": "A magnetic field is a region around a magnet or current where magnetic forces can be detected. Field lines represent the trajectory of a free north pole.",
        "common_trap": "Believing magnetic field lines can cross in regions of high field strength (M17) or that cutting a magnet creates monopoles (M15).",
    },
    "current_magnetism": {
        "title": "Magnetic Field Due to Current & Solenoids",
        "chapter": "Magnetic Effects of Electric Current",
        "formulas": [
            "Right-Hand Thumb Rule: Thumb = Current ==> Fingers = B-Field",
            "Straight Wire: B ∝ I / r (concentric circles)",
            "Circular Loop: Concentric near wire, straight and perpendicular at centre",
            "Solenoid: Uniform parallel lines inside; behaves like a bar magnet",
        ],
        "summary": "Oersted proved that electric current produces a magnetic field. A solenoid carrying current produces a strong, uniform interior magnetic field and acts as an electromagnet.",
        "common_trap": "Confusing the Right-Hand Thumb Rule for field with Fleming's rules for force or induction (M16).",
    },
    "magnetic_force": {
        "title": "Magnetic Force & Fleming's Left-Hand Rule",
        "chapter": "Magnetic Effects of Electric Current",
        "formulas": [
            "F = B · I · L · sin(theta)",
            "Maximum force when conductor is perpendicular to B (theta = 90°)",
            "Zero force when conductor is parallel to B (theta = 0° or 180°)",
            "Fleming's Left-Hand Rule: Thumb = Force, Forefinger = Field, Middle = Current",
        ],
        "summary": "When a current-carrying wire is placed in an external magnetic field, it experiences a mechanical force due to interaction between magnetic fields. This principle powers electric motors.",
        "common_trap": "Applying Fleming's Left-Hand Rule to generators instead of motors (M16).",
    },
    "domestic_circuits": {
        "title": "Domestic AC Circuits & Electrical Safety",
        "chapter": "Magnetic Effects of Electric Current",
        "formulas": [
            "Supply: 220 V, 50 Hz AC (India)",
            "Live wire (Red/Brown) at 220 V; Neutral wire (Black/Blue) at 0 V",
            "Earth wire (Green/Yellow) connected to ground for shock prevention",
            "Electric Fuse: Low melting point wire rated in amperes (1A, 2A, 5A, 15A)",
        ],
        "summary": "Domestic appliances are wired in parallel so each gets 220 V and operates independently. Earthing safely shunts leakage currents to ground to prevent electrocution.",
        "common_trap": "Assuming the earth wire saves power by storing electrons in the ground (M4).",
    },
}
