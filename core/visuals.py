"""core/visuals.py - High-Impact Educational Visualizations & Interactive Widgets

Contains:
1. SVG Cognitive Mastery Radar Chart (Spider Chart) across all 8 syllabus topics
2. Interactive Virtual Circuit Simulator & Misconception Buster (Series vs Parallel)
3. Topic Explorer & Formula Reference Engine
"""

import math
from typing import Dict, Any, List
from core.concepts import CONCEPTS

def generate_mastery_radar_chart_svg(
    mastery_dict: Dict[str, float],
    width: int = 500,
    height: int = 420,
) -> str:
    """
    Generates a pure SVG 8-axis Radar/Spider chart representing the student's
    cognitive mastery vector across the 8 NCERT Electricity concepts.
    Lightweight, crisp on retina/mobile screens, zero heavy charting dependencies.
    """
    concept_keys = [
        "charge", "current", "pd", "ohm",
        "resistance", "series", "parallel", "power"
    ]
    n_axes = len(concept_keys)
    cx, cy = width / 2, height / 2 + 10
    radius = min(width, height) * 0.36

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

    for i, cid in enumerate(concept_keys):
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
        r_label = radius * 1.22
        x_label = cx + r_label * math.cos(angle)
        y_label = cy + r_label * math.sin(angle)
        
        c_name = CONCEPTS[cid]["name"].replace(" Circuits", "").replace(" & Factors", "")
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
            <text x="{x_label:.1f}" y="{y_label:.1f}" text-anchor="{anchor}" font-family="Inter, sans-serif" font-size="11" font-weight="600" fill="#14213D">
                {c_name} <tspan fill="{color}" font-weight="700">({pct_text})</tspan>
            </text>
        ''')

    # Student Mastery polygon
    data_poly = f'<polygon points="{" ".join(data_points)}" fill="rgba(244, 163, 0, 0.35)" stroke="#F4A300" stroke-width="2.5" />'

    # Mastery data point circles
    circles_svg = []
    for pt in data_points:
        px, py = pt.split(",")
        circles_svg.append(f'<circle cx="{px}" cy="{py}" r="4.5" fill="#F4A300" stroke="#FFFFFF" stroke-width="1.5" />')

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
        <!-- Definitions -->
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

# NCERT Class 10 Physics Quick Reference Cards
CONCEPT_STUDY_CARDS: Dict[str, Dict[str, Any]] = {
    "charge": {
        "title": "Electric Charge & Quantisation",
        "formulas": ["Q = n · e", "e = 1.6 × 10^-19 C", "1 C ≈ 6.25 × 10^18 electrons"],
        "summary": "Electric charge is an intrinsic property of subatomic particles. Protons carry positive charge, while free electrons carry negative charge. In solid conductors, current is the drift of free electrons.",
        "common_trap": "Believing a battery generates new charges from nothing; the charges already exist throughout the wires (M4).",
    },
    "current": {
        "title": "Electric Current & Rate of Flow",
        "formulas": ["I = Q / t", "1 A = 1 C / s", "Conventional flow: + to - ; Electron flow: - to +"],
        "summary": "Current is the rate of flow of electric charge through any cross-section. It is measured in series by an ammeter of very low internal resistance.",
        "common_trap": "Assuming current gets consumed or 'used up' by lamps or resistors (M1).",
    },
    "pd": {
        "title": "Potential Difference & Work Done",
        "formulas": ["V = W / Q", "1 V = 1 J / C", "Measured in parallel by high-resistance voltmeter"],
        "summary": "Potential difference is the work done in moving a unit positive charge between two points in an electric field. The battery maintains this push.",
        "common_trap": "Confusing voltage (energy per charge) with current (rate of charge flow) (M3).",
    },
    "ohm": {
        "title": "Ohm's Law & V-I Characteristics",
        "formulas": ["V = I · R", "Slope of V vs I = R", "Valid at constant temperature"],
        "summary": "At constant temperature, current through a metallic conductor is directly proportional to the potential difference across its terminals.",
        "common_trap": "Thinking a battery outputs constant amperes into any circuit regardless of resistance (M2).",
    },
    "resistance": {
        "title": "Resistance & Factors Influencing Flow",
        "formulas": ["R = ρ · l / A", "Thicker wire &rarr; Lower R", "Longer wire &rarr; Higher R"],
        "summary": "Resistance is opposition to electron drift. It depends on material resistivity (ρ), length (l), and cross-sectional area (A), but NOT on the applied voltage.",
        "common_trap": "Believing that altering the applied voltage changes the resistance of an ohmic wire (M6).",
    },
    "series": {
        "title": "Series Circuits (Single Conducting Path)",
        "formulas": ["R_s = R1 + R2 + ... + Rn", "I_tot = I1 = I2", "V_tot = V1 + V2"],
        "summary": "In series, all components share a single loop. If one component burns out, current stops flowing everywhere. Equivalent resistance is always larger than any individual resistor.",
        "common_trap": "Thinking the first resistor gets more current and starves subsequent components (M1).",
    },
    "parallel": {
        "title": "Parallel Circuits (Independent Branches)",
        "formulas": ["1 / R_p = 1 / R1 + 1 / R2", "V_tot = V1 = V2", "I_tot = I1 + I2"],
        "summary": "In parallel, all branches connect across the same two points, experiencing identical voltage. Total resistance is always less than the smallest individual resistor.",
        "common_trap": "Assuming parallel branches increase total circuit resistance like series circuits do (M5).",
    },
    "power": {
        "title": "Electric Power & Heating Effect",
        "formulas": ["P = V · I = I^2 · R = V^2 / R", "1 W = 1 J / s", "Heat H = I^2 · R · t (Joule's Law)"],
        "summary": "Electric power is the rate at which electrical energy is transformed into other energy forms. Bulb brightness in a circuit is determined by actual power dissipated, not stamped rating alone.",
        "common_trap": "Assuming a higher-wattage rated bulb always glows brighter in series circuits (M3).",
    },
}
