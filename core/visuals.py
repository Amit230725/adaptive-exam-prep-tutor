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
    width: int = 540,
    height: int = 440,
) -> str:
    """
    Generates a pure SVG multi-axis Radar/Spider chart representing the student's
    cognitive mastery vector across selected syllabus topics or chapters.
    Lightweight, crisp on retina/mobile screens, zero heavy charting dependencies.
    """
    if not concept_keys:
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
    cx = width / 2
    # Provide generous headroom at the top so top vertex label never collides with legend
    cy = (height - 50) / 2 + 25
    
    # Scale radius and font size according to number of axes
    if n_axes > 10:
        radius = min(width, height) * 0.27
        font_sz = 9
    else:
        radius = min(width, height) * 0.30
        font_sz = 11

    # Concentric background grid polygons (25%, 50%, 75%, 100%)
    grid_svg = []
    scale_labels = []
    for level, pct_str in [(0.25, "25%"), (0.50, "50%"), (0.75, "75%"), (1.0, "100%")]:
        r_level = radius * level
        pts = []
        for i in range(n_axes):
            angle = (2 * math.pi / n_axes) * i - (math.pi / 2)
            x = cx + r_level * math.cos(angle)
            y = cy + r_level * math.sin(angle)
            pts.append(f"{x:.1f},{y:.1f}")
        stroke_color = "#E2E8F0" if level < 1.0 else "#CBD5E1"
        dash = 'stroke-dasharray="3,3"' if level in [0.25, 0.75] else ""
        grid_svg.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="{stroke_color}" stroke-width="1.2" {dash} />')
        # Subtle scale marker on top spoke
        scale_labels.append(f'<text x="{cx + 5:.1f}" y="{cy - r_level + 9:.1f}" font-family="Inter, sans-serif" font-size="8.5" fill="#94A3B8" font-weight="500">{pct_str}</text>')

    # Axis spokes and labels
    spokes_svg = []
    labels_svg = []
    data_points = []

    for i, cid in enumerate(valid_keys):
        angle = (2 * math.pi / n_axes) * i - (math.pi / 2)
        # Spoke line
        x_end = cx + radius * math.cos(angle)
        y_end = cy + radius * math.sin(angle)
        spokes_svg.append(f'<line x1="{cx}" y1="{cy}" x2="{x_end:.1f}" y2="{y_end:.1f}" stroke="#E2E8F0" stroke-width="1.2" />')

        # Data polygon point
        m_val = max(0.05, min(1.0, mastery_dict.get(cid, 0.3)))
        r_data = radius * m_val
        x_data = cx + r_data * math.cos(angle)
        y_data = cy + r_data * math.sin(angle)
        data_points.append(f"{x_data:.1f},{y_data:.1f}")

        # Text label with percentage - positioned cleanly outside vertex with proper anchor
        c_name = CONCEPTS[cid]["name"].split("&")[0].split("(")[0].replace(" Circuits", "").replace("Spherical ", "").strip()
        pct_text = f"{int(m_val * 100)}%"
        
        # Label color based on threshold
        color = "#10B981" if m_val >= 0.70 else "#F59E0B" if m_val >= 0.40 else "#EF4444"

        # Direction-aware label positioning
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        if abs(cos_a) < 0.2:
            # Top or bottom vertex
            anchor = "middle"
            x_label = cx
            y_label = (cy - radius - 14) if sin_a < 0 else (cy + radius + 18)
        elif cos_a > 0:
            # Right side
            anchor = "start"
            x_label = x_end + 12
            y_label = y_end + 4
        else:
            # Left side
            anchor = "end"
            x_label = x_end - 12
            y_label = y_end + 4

        labels_svg.append(f'''
            <text x="{x_label:.1f}" y="{y_label:.1f}" text-anchor="{anchor}" font-family="Inter, sans-serif" font-size="{font_sz}" font-weight="600" fill="#0F172A">
                {c_name} <tspan fill="{color}" font-weight="700">({pct_text})</tspan>
            </text>
        ''')

    # Student Mastery polygon with gradient fill
    data_poly = f'<polygon points="{" ".join(data_points)}" fill="url(#masteryPolyGrad)" stroke="#2563EB" stroke-width="2.5" />'

    # Mastery data point circles
    circles_svg = []
    for pt in data_points:
        px, py = pt.split(",")
        circles_svg.append(f'<circle cx="{px}" cy="{py}" r="4.5" fill="#2563EB" stroke="#FFFFFF" stroke-width="2" />')

    # Target Benchmark line (70% mastery boundary in emerald dashed green)
    target_points = []
    for i in range(n_axes):
        angle = (2 * math.pi / n_axes) * i - (math.pi / 2)
        r_t = radius * 0.70
        xt = cx + r_t * math.cos(angle)
        yt = cy + r_t * math.sin(angle)
        target_points.append(f"{xt:.1f},{yt:.1f}")
    target_poly = f'<polygon points="{" ".join(target_points)}" fill="none" stroke="#10B981" stroke-width="2" stroke-dasharray="5,4" opacity="0.9" />'

    svg_content = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" style="max-width:100%; height:auto; display:block; margin:auto;">
        <defs>
            <linearGradient id="masteryPolyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#2563EB" stop-opacity="0.45" />
                <stop offset="100%" stop-color="#3B82F6" stop-opacity="0.15" />
            </linearGradient>
        </defs>
        <style>
            .legend-text {{ font-family: 'Inter', sans-serif; font-size: 11px; fill: #334155; font-weight: 600; }}
        </style>
        <!-- Background Grids & Scale -->
        {''.join(grid_svg)}
        {''.join(scale_labels)}
        <!-- Spokes -->
        {''.join(spokes_svg)}
        <!-- Target 70% Mastery Threshold -->
        {target_poly}
        <!-- Student Mastery Shape -->
        {data_poly}
        {''.join(circles_svg)}
        <!-- Labels -->
        {''.join(labels_svg)}
        <!-- Legend: Clean pill placed at the bottom, completely separated from top labels -->
        <g transform="translate({cx - 140:.1f}, {height - 24})">
            <rect x="-10" y="-12" width="280" height="26" rx="13" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1" />
            <rect x="8" y="-5" width="12" height="12" rx="3" fill="rgba(37, 99, 235, 0.45)" stroke="#2563EB" stroke-width="1.8" />
            <text x="26" y="5" class="legend-text">Your Mastery</text>
            <line x1="120" y1="1" x2="150" y2="1" stroke="#10B981" stroke-width="2.5" stroke-dasharray="4,3" />
            <text x="158" y="5" class="legend-text">70% Target</text>
        </g>
    </svg>
    """
    return svg_content

def generate_circular_progress_svg(
    percentage: float,
    size: int = 110,
    stroke_width: int = 10,
    color: str = "#2563EB",
    track_color: str = "#E2E8F0",
) -> str:
    """
    Renders a modern circular progress ring matching the Reyhan Adinata Dribbble dashboard style.
    """
    p = max(0.0, min(1.0, float(percentage)))
    radius = (size - stroke_width) / 2
    circumference = 2 * math.pi * radius
    dashoffset = circumference * (1.0 - p)
    cx, cy = size / 2, size / 2
    pct_str = f"{int(p * 100)}%"

    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="display:block;margin:auto;">
        <circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{track_color}" stroke-width="{stroke_width}" />
        <circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{color}" stroke-width="{stroke_width}"
                stroke-dasharray="{circumference:.2f}" stroke-dashoffset="{dashoffset:.2f}"
                stroke-linecap="round" transform="rotate(-90 {cx} {cy})" />
        <text x="{cx}" y="{cy + 6}" font-family="Inter, sans-serif" font-size="{int(size * 0.22)}" font-weight="700"
              fill="#0F172A" text-anchor="middle">{pct_str}</text>
    </svg>
    """

def generate_activity_barchart_svg(
    days_data: Optional[List[Dict[str, Any]]] = None,
    width: int = 600,
    height: int = 240,
) -> str:
    """
    Renders the modern ed-tech weekly learning activity bar chart with active highlighted column,
    replicating the Dribbble dashboard aesthetic.
    """
    if not days_data:
        days_data = [
            {"day": "Mon", "value": 28, "active": False},
            {"day": "Tue", "value": 65, "active": False},
            {"day": "Wed", "value": 30, "active": False},
            {"day": "Thu", "value": 90, "active": True, "tooltip": "Learning time<br><b>2h 15m</b>"},
            {"day": "Fri", "value": 45, "active": False},
            {"day": "Sat", "value": 75, "active": False},
            {"day": "Sun", "value": 35, "active": False},
        ]

    n_bars = len(days_data)
    padding_x = 35
    avail_w = width - (2 * padding_x)
    col_w = avail_w / n_bars
    bar_w = min(56.0, col_w * 0.62)
    chart_h = height - 60

    bars_svg = []
    labels_svg = []
    overlay_svg = []

    for i, item in enumerate(days_data):
        bx = padding_x + (i * col_w) + (col_w - bar_w) / 2
        pct = max(0.08, min(1.0, item["value"] / 100.0))
        bh = chart_h * pct
        by = 25 + (chart_h - bh)

        if item.get("active", False):
            # Vibrant Cobalt Blue Bar with subtle pattern
            bars_svg.append(f'''
                <rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" rx="10"
                      fill="#2563EB" />
                <path d="M {bx+6} {by+14} Q {bx+bar_w/2} {by+8} {bx+bar_w-6} {by+14}" stroke="rgba(255,255,255,0.4)" stroke-width="1.8" fill="none" />
                <path d="M {bx+6} {by+26} Q {bx+bar_w/2} {by+20} {bx+bar_w-6} {by+26}" stroke="rgba(255,255,255,0.4)" stroke-width="1.8" fill="none" />
                <path d="M {bx+6} {by+38} Q {bx+bar_w/2} {by+32} {bx+bar_w-6} {by+38}" stroke="rgba(255,255,255,0.4)" stroke-width="1.8" fill="none" />
            ''')
            # Floating Tooltip Pill on top of active bar
            tip_w, tip_h = 92, 38
            tip_x = (bx + bar_w / 2) - (tip_w / 2)
            tip_y = max(2, by - tip_h - 8)
            overlay_svg.append(f'''
                <g transform="translate({tip_x:.1f}, {tip_y:.1f})">
                    <rect width="{tip_w}" height="{tip_h}" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1" />
                    <text x="{tip_w/2}" y="14" font-family="Inter, sans-serif" font-size="9" fill="#64748B" text-anchor="middle">Learning time</text>
                    <text x="{tip_w/2}" y="28" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#2563EB" text-anchor="middle">2h 15m</text>
                </g>
            ''')
        else:
            # Clean Slate Blue Outline Bar
            bars_svg.append(f'''
                <rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" rx="10"
                      fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2" />
            ''')

        # Day Label
        font_weight = "700" if item.get("active") else "500"
        font_color = "#2563EB" if item.get("active") else "#64748B"
        labels_svg.append(f'''
            <text x="{bx + bar_w/2:.1f}" y="{height - 15}" font-family="Inter, sans-serif" font-size="12"
                  font-weight="{font_weight}" fill="{font_color}" text-anchor="middle">{item["day"]}</text>
        ''')

    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" style="width:100%; height:auto; display:block;">
        <line x1="{padding_x}" y1="{height - 35}" x2="{width - padding_x}" y2="{height - 35}" stroke="#F1F5F9" stroke-width="1.5" />
        {''.join(bars_svg)}
        {''.join(overlay_svg)}
        {''.join(labels_svg)}
    </svg>
    """

def generate_evaluation_certificate_html(
    student_name: str,
    class_code: str,
    readiness_score: int,
    grade_tier: str,
    chapter_masteries: Dict[str, float],
    misconceptions_cleared: int,
    total_misconceptions: int = 17,
) -> str:
    """
    Generates a prestigious, high-resolution CBSE Class 10 Physics
    Certificate of Conceptual Competency & Board Exam Readiness Report.
    """
    rows_html = []
    for ch_id, ch_data in CHAPTERS.items():
        m_val = chapter_masteries.get(ch_id, 0.5)
        pct = int(m_val * 100)
        status_badge = (
            '<span style="background:#ECFDF5;color:#065F46;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;">🟢 BOARD READY</span>'
            if m_val >= 0.70 else
            '<span style="background:#FFFBEB;color:#92400E;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;">🟡 DEVELOPING</span>'
            if m_val >= 0.40 else
            '<span style="background:#FFF1F2;color:#9F1239;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;">🔴 GAP IDENTIFIED</span>'
        )
        bar_fill = "#10B981" if m_val >= 0.70 else "#F59E0B" if m_val >= 0.40 else "#EF4444"
        rows_html.append(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div style="width:42%; font-weight:600; font-size:13px; color:#1E293B;">{ch_data['name']}</div>
            <div style="width:38%; margin: 0 12px;">
                <div style="background:#E2E8F0; border-radius:8px; height:8px; overflow:hidden;">
                    <div style="background:{bar_fill}; width:{pct}%; height:8px; border-radius:8px;"></div>
                </div>
            </div>
            <div style="width:20%; text-align:right;">{status_badge}</div>
        </div>
        """)

    return f"""
    <div style="background:#FFFFFF; border:2px solid #E2E8F0; border-radius:20px; padding:32px 36px; box-shadow:0 10px 30px -5px rgba(0,0,0,0.06); font-family:'Inter', sans-serif; position:relative; overflow:hidden; max-width:850px; margin:auto;">
        <!-- Top decorative ribbon -->
        <div style="position:absolute; top:0; left:0; right:0; height:8px; background:linear-gradient(90deg, #2563EB, #3B82F6, #10B981);"></div>
        
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px;">
            <div>
                <span style="background:#EFF6FF; color:#1D4ED8; font-size:11px; font-weight:700; padding:4px 10px; border-radius:6px; letter-spacing:0.5px;">OFFICIAL DIAGNOSTIC CREDENTIAL</span>
                <h2 style="font-family:'Space Grotesk', sans-serif; margin:8px 0 2px 0; color:#0F172A; font-size:24px;">CBSE Class 10 Science (Physics)</h2>
                <div style="color:#64748B; font-size:13px;">Cognitive Learner Evaluation & Board Readiness Assessment</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:32px; font-weight:800; color:#2563EB; line-height:1;">{readiness_score}<span style="font-size:16px; color:#94A3B8;">/100</span></div>
                <div style="font-size:12px; font-weight:700; color:#10B981;">{grade_tier}</div>
            </div>
        </div>

        <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:14px 18px; margin-bottom:24px; display:flex; justify-content:space-between;">
            <div><small style="color:#64748B;">Candidate Nickname</small><br><b>{student_name}</b></div>
            <div><small style="color:#64748B;">Enrolled Class</small><br><b>{class_code}</b></div>
            <div><small style="color:#64748B;">Misconceptions Busted</small><br><b style="color:#059669;">{misconceptions_cleared} / {total_misconceptions}</b></div>
            <div><small style="color:#64748B;">Verification Protocol</small><br><b>BKT + Rasch IRT</b></div>
        </div>

        <h4 style="margin:0 0 14px 0; font-size:15px; color:#0F172A;">Curriculum Chapter Mastery Breakdown</h4>
        {''.join(rows_html)}

        <div style="border-top:1px dashed #CBD5E1; margin-top:24px; padding-top:16px; display:flex; justify-content:space-between; align-items:center; font-size:11px; color:#64748B;">
            <div>Verified by ConceptPilot Adaptive Diagnostic Engine · Powered by Google Gemini 2.5 Flash</div>
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="color:#10B981;">●</span> Verified Authenticated Learning Session
            </div>
        </div>
    </div>
    """

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
