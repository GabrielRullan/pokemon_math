#!/usr/bin/env python3
"""
Generador de diagramas SVG didácticos y listos para imprimir (A4) para los
problemas de Matemáticas Primaria con Pokémon (1º a 6º de Primaria, LOMLOE).

Exporta:
    generate_problem_svg(
        prob_num: int,
        kind: str,
        title: str,
        subcat: str,
        sense: str,
        story_text: str,
        question_text: str,
        grade: int,
    ) -> str
"""

from __future__ import annotations

import html
import math
import re
from typing import Any

# Paleta oficial de alto contraste apta para impresión A4
BLUE = "#1e3a8a"
BLUE_MID = "#2563eb"
BLUE_SOFT = "#eff6ff"
BLUE_FILL = "#dbeafe"
RED = "#e3350d"
RED_SOFT = "#fef2f2"
GREEN = "#047857"
GREEN_SOFT = "#ecfdf5"
AMBER = "#f59e0b"
AMBER_DARK = "#b45309"
AMBER_SOFT = "#fef3c7"
SLATE = "#334155"
INK = "#0f172a"
MUTED = "#64748b"
GRID_LINE = "#cbd5e1"
PURPLE = "#7c3aed"

PALETTE = [BLUE, RED, GREEN, AMBER, BLUE_MID, PURPLE]

SPANISH_NUM_WORDS: dict[str, int] = {
    "una": 1,
    "un": 1,
    "uno": 1,
    "dos": 2,
    "tres": 3,
    "cuatro": 4,
    "cinco": 5,
    "seis": 6,
    "siete": 7,
    "ocho": 8,
    "nueve": 9,
    "diez": 10,
    "once": 11,
    "doce": 12,
}


# ---------------------------------------------------------------------------
# Utilidades SVG y análisis de texto
# ---------------------------------------------------------------------------

def _esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _wrap_svg(inner: str, width: int, height: int, aria_label: str) -> str:
    safe_aria = _esc(aria_label)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" '
        f'style="max-height:150px;max-width:100%;height:auto;display:block;" '
        f'role="img" aria-label="{safe_aria}">'
        f"{inner}</svg>"
    )
    return f'<div class="problem-diagram" aria-label="Ilustración matemática">{svg}</div>'


def _svg_text(
    x: float,
    y: float,
    text: str,
    size: int = 10,
    fill: str = SLATE,
    anchor: str = "middle",
    weight: str = "600",
    extra: str = "",
) -> str:
    extra_attr = f" {extra}" if extra else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="\'Trebuchet MS\', \'Segoe UI\', sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{extra_attr}>'
        f"{_esc(text)}</text>"
    )


def _clean_md(text: str) -> str:
    cleaned = text.replace("**", "").replace("__", "").replace("`", "")
    cleaned = re.sub(r"\$([^$]+)\$", r"\1", cleaned)
    return cleaned


def _parse_es_num(raw: str) -> float | None:
    s = raw.strip().replace("−", "-")
    if not s:
        return None
    sign = -1.0 if s.startswith("-") else 1.0
    s_abs = s.lstrip("+-").strip()
    if not s_abs:
        return None
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?", s_abs):
        s_abs = s_abs.replace(".", "").replace(",", ".")
    elif "," in s_abs and "." not in s_abs:
        s_abs = s_abs.replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(?:\.\d{3})+", s_abs):
        s_abs = s_abs.replace(".", "")
    try:
        return sign * float(s_abs)
    except ValueError:
        return None


def _fmt_num(val: float) -> str:
    if abs(val - round(val)) < 1e-9:
        iv = int(round(val))
        neg = iv < 0
        s = f"{abs(iv):,}".replace(",", ".")
        return f"-{s}" if neg else s
    s = f"{val:.3f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def _short_label(label: str, max_len: int = 13) -> str:
    s = re.sub(r"\s+", " ", label).strip(" :-–—.,;")
    if len(s) <= max_len:
        return s
    return s[: max_len - 1].rstrip() + "…"


# ---------------------------------------------------------------------------
# 1. Reloj analógico
# ---------------------------------------------------------------------------

def _parse_clock_time(text: str) -> tuple[int, int, str] | None:
    """Extrae la hora principal (hora_24, minuto, etiqueta) evitando falsos positivos."""
    low = text.lower()
    scrubbed = re.sub(r"pok[ée][\s\-]?reloj", "dispositivo", low)
    scrubbed = re.sub(r"(?:en el sentido de las )?agujas del reloj", "sentido horario", scrubbed)
    scrubbed = re.sub(r"contra el reloj", "contrarreloj", scrubbed)

    has_hhmm = False
    for m in re.finditer(r"(?<![:\d])\b([01]?\d|2[0-3]):([0-5]\d)\b(?!\d)", scrubbed):
        prefix = scrubbed[max(0, m.start() - 18) : m.start()]
        if not re.search(r"(?:escala|proporci[óo]n|raz[óo]n)\s+$", prefix):
            has_hhmm = True
            break

    has_phrase = bool(
        re.search(
            r"\b(?:"
            r"en punto|"
            r"(?:a\s+)?las\s+(?:\d{1,2}|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce)\s+"
            r"(?:y\s+media|y\s+cuarto|menos\s+cuarto|en\s+punto)"
            r")\b",
            scrubbed,
        )
    )
    has_reloj_word = bool(re.search(r"\breloj\b", scrubbed))

    if not (has_hhmm or has_phrase or has_reloj_word):
        return None

    # Prioridad 1: reloj de estación / pared que marca explícitamente la hora actual
    m_reloj = re.search(
        r"(?:reloj[^.\n]{0,40}?(?:marca|señala)|marca\s+ahora)\s+(?:las\s+)?([01]?\d|2[0-3]):([0-5]\d)\b",
        scrubbed,
    )
    if m_reloj:
        h, mi = int(m_reloj.group(1)), int(m_reloj.group(2))
        return h, mi, f"{h:02d}:{mi:02d}"

    # Prioridad 2: primera aparición cronológica de HH:MM o frase horaria
    first_candidates: list[tuple[int, int, int]] = []
    for m in re.finditer(r"(?<![:\d])\b([01]?\d|2[0-3]):([0-5]\d)\b(?!\d)", scrubbed):
        prefix = scrubbed[max(0, m.start() - 18) : m.start()]
        if re.search(r"(?:escala|proporci[óo]n|raz[óo]n)\s+$", prefix):
            continue
        first_candidates.append((m.start(), int(m.group(1)), int(m.group(2))))
        break

    m_phrase = re.search(
        r"\b(?:a\s+)?las\s+(una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|\d{1,2})\s+"
        r"(y\s+media|y\s+cuarto|menos\s+cuarto|en\s+punto)\b",
        scrubbed,
    )
    if m_phrase:
        h_raw = m_phrase.group(1)
        mod = m_phrase.group(2).strip()
        h = int(h_raw) if h_raw.isdigit() else SPANISH_NUM_WORDS.get(h_raw, 12)
        if "media" in mod:
            mi = 30
        elif "menos cuarto" in mod:
            h = 12 if h == 1 else h - 1
            mi = 45
        elif "cuarto" in mod:
            mi = 15
        else:
            mi = 0
        first_candidates.append((m_phrase.start(), h, mi))

    if first_candidates:
        first_candidates.sort(key=lambda item: item[0])
        _, h, mi = first_candidates[0]
        return h, mi, f"{h:02d}:{mi:02d}"

    return None


def _render_clock_svg(hour: int, minute: int, label: str) -> str:
    w, h = 180, 150
    cx, cy, r = 90.0, 68.0, 54.0
    parts: list[str] = [
        f'<circle cx="{cx}" cy="{cy}" r="{r + 4}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2.5"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{GRID_LINE}" stroke-width="1"/>',
    ]

    for i in range(60):
        ang = math.radians(i * 6 - 90)
        is_hour = i % 5 == 0
        r_in = r - (7.0 if is_hour else 3.5)
        r_out = r - 1.0
        x1 = cx + r_in * math.cos(ang)
        y1 = cy + r_in * math.sin(ang)
        x2 = cx + r_out * math.cos(ang)
        y2 = cy + r_out * math.sin(ang)
        stroke = BLUE if is_hour else "#94a3b8"
        sw = "2" if is_hour else "1"
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"/>')

    for num in range(1, 13):
        ang = math.radians(num * 30 - 90)
        rn = r - 14.5
        nx = cx + rn * math.cos(ang)
        ny = cy + rn * math.sin(ang) + 3.5
        parts.append(_svg_text(nx, ny, str(num), size=9, fill=INK, weight="700"))

    min_ang = math.radians(minute * 6 - 90)
    mx = cx + (r - 15.0) * math.cos(min_ang)
    my = cy + (r - 15.0) * math.sin(min_ang)
    parts.append(
        f'<line x1="{cx}" y1="{cy}" x2="{mx:.1f}" y2="{my:.1f}" '
        f'stroke="{BLUE}" stroke-width="2.6" stroke-linecap="round"/>'
    )

    hour_ang = math.radians(((hour % 12) + minute / 60.0) * 30.0 - 90)
    hx = cx + (r - 27.0) * math.cos(hour_ang)
    hy = cy + (r - 27.0) * math.sin(hour_ang)
    parts.append(
        f'<line x1="{cx}" y1="{cy}" x2="{hx:.1f}" y2="{hy:.1f}" '
        f'stroke="{RED}" stroke-width="3.8" stroke-linecap="round"/>'
    )

    parts.append(f'<circle cx="{cx}" cy="{cy}" r="3.8" fill="{AMBER}" stroke="{BLUE}" stroke-width="1.5"/>')
    parts.append(f'<rect x="52" y="128" width="76" height="17" rx="8" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1"/>')
    parts.append(_svg_text(cx, 140, f"Reloj: {label}", size=9, fill=BLUE, weight="700"))
    return _wrap_svg("".join(parts), w, h, f"Reloj analógico marcando las {label}")


# ---------------------------------------------------------------------------
# 2. Recta numérica / Termómetro / Escala de altitud
# ---------------------------------------------------------------------------

def _render_thermometer_svg(temps: list[float]) -> str:
    w, h = 210, 150
    vals = sorted(set(temps[:4]))
    vmin = min(min(vals), 0.0)
    vmax = max(max(vals), 0.0)
    span = max(vmax - vmin, 10.0)
    vmin_pad = vmin - span * 0.15
    vmax_pad = vmax + span * 0.15

    top_y, bot_y = 18.0, 122.0
    tx = 54.0

    def to_y(v: float) -> float:
        return bot_y - ((v - vmin_pad) / (vmax_pad - vmin_pad)) * (bot_y - top_y)

    parts: list[str] = [
        _svg_text(108, 12, "Escala térmica (°C)", size=9, fill=BLUE, weight="700"),
        f'<rect x="{tx - 7:.1f}" y="{top_y - 4:.1f}" width="14" height="{bot_y - top_y + 10:.1f}" '
        f'rx="7" fill="#f8fafc" stroke="{SLATE}" stroke-width="1.8"/>',
        f'<circle cx="{tx:.1f}" cy="{bot_y + 12:.1f}" r="11" fill="{RED}" stroke="{SLATE}" stroke-width="1.8"/>',
    ]

    y_top_col = to_y(max(vals))
    col_color = RED if max(vals) >= 0 else BLUE_MID
    parts.append(
        f'<rect x="{tx - 4:.1f}" y="{y_top_col:.1f}" width="8" height="{bot_y + 6 - y_top_col:.1f}" '
        f'rx="3" fill="{col_color}" opacity="0.85"/>'
    )

    y0 = to_y(0.0)
    parts.append(
        f'<line x1="{tx - 16:.1f}" y1="{y0:.1f}" x2="{tx + 28:.1f}" y2="{y0:.1f}" '
        f'stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="3,2"/>'
    )
    parts.append(_svg_text(tx - 20, y0 + 3, "0 °C", size=8, fill=BLUE, anchor="end", weight="700"))

    used_y: list[float] = []
    for v in vals:
        yv = to_y(v)
        for py in used_y:
            if abs(yv - py) < 13:
                yv = py - 13 if yv <= py else py + 13
        used_y.append(yv)
        col = BLUE_MID if v < 0 else RED
        sign = "+" if v > 0 else ""
        parts.append(f'<line x1="{tx + 7:.1f}" y1="{to_y(v):.1f}" x2="{tx + 24:.1f}" y2="{yv:.1f}" stroke="{col}" stroke-width="1.5"/>')
        parts.append(f'<circle cx="{tx:.1f}" cy="{to_y(v):.1f}" r="3.2" fill="{col}" stroke="#ffffff" stroke-width="1"/>')
        parts.append(_svg_text(tx + 28, yv + 3.5, f"{sign}{_fmt_num(v)} °C", size=10, fill=col, anchor="start", weight="700"))

    return _wrap_svg("".join(parts), w, h, "Termómetro de temperaturas en grados Celsius")


def _render_altitude_svg(values: list[float]) -> str:
    w, h = 230, 150
    vals = values[:4]
    vmin = min(min(vals), 0.0)
    vmax = max(max(vals), 0.0)
    span = max(vmax - vmin, 10.0)
    vmin_pad = vmin - span * 0.14
    vmax_pad = vmax + span * 0.16
    top_y, bot_y = 20.0, 134.0
    ax = 68.0

    def to_y(v: float) -> float:
        return bot_y - ((v - vmin_pad) / (vmax_pad - vmin_pad)) * (bot_y - top_y)

    y0 = to_y(0.0)
    parts: list[str] = [
        _svg_text(115, 12, "Altitud respecto al nivel del mar", size=9, fill=BLUE, weight="700"),
        f'<rect x="20" y="{top_y:.1f}" width="190" height="{max(0.0, y0 - top_y):.1f}" fill="{BLUE_SOFT}" opacity="0.65"/>',
        f'<rect x="20" y="{y0:.1f}" width="190" height="{max(0.0, bot_y - y0):.1f}" fill="#dbeafe" opacity="0.9"/>',
        f'<line x1="{ax:.1f}" y1="{top_y:.1f}" x2="{ax:.1f}" y2="{bot_y:.1f}" stroke="{SLATE}" stroke-width="2"/>',
        f'<line x1="20" y1="{y0:.1f}" x2="210" y2="{y0:.1f}" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="4,2"/>',
        _svg_text(ax - 6, y0 + 3, "0 m (mar)", size=8, fill=BLUE, anchor="end", weight="700"),
    ]

    used_y: list[float] = []
    for v in sorted(set(vals)):
        yv = to_y(v)
        label_y = yv
        for py in used_y:
            if abs(label_y - py) < 14:
                label_y = py - 14 if label_y <= py else py + 14
        used_y.append(label_y)
        col = GREEN if v >= 0 else RED
        sign = "+" if v > 0 else ""
        parts.append(f'<circle cx="{ax:.1f}" cy="{yv:.1f}" r="4" fill="{col}" stroke="#ffffff" stroke-width="1.2"/>')
        parts.append(f'<line x1="{ax + 4:.1f}" y1="{yv:.1f}" x2="{ax + 20:.1f}" y2="{label_y:.1f}" stroke="{col}" stroke-width="1.3"/>')
        parts.append(_svg_text(ax + 24, label_y + 3.5, f"{sign}{_fmt_num(v)} m", size=10, fill=col, anchor="start", weight="700"))

    return _wrap_svg("".join(parts), w, h, "Escala vertical de altitud y profundidad")


def _render_number_line_svg(
    low: float,
    high: float,
    points: list[tuple[float, str]],
    title_text: str,
    show_zero: bool = False,
) -> str:
    w, h = 300, 120
    x1, x2, y_line = 26.0, 274.0, 68.0
    span = max(high - low, 1e-6)

    def to_x(v: float) -> float:
        clamped = max(low, min(high, v))
        return x1 + ((clamped - low) / span) * (x2 - x1)

    parts: list[str] = [
        _svg_text(w / 2, 16, title_text, size=10, fill=BLUE, weight="700"),
        f'<line x1="{x1 - 8:.1f}" y1="{y_line:.1f}" x2="{x2 + 8:.1f}" y2="{y_line:.1f}" stroke="{SLATE}" stroke-width="2.2"/>',
        f'<polygon points="{x1 - 12:.1f},{y_line:.1f} {x1 - 5:.1f},{y_line - 4:.1f} {x1 - 5:.1f},{y_line + 4:.1f}" fill="{SLATE}"/>',
        f'<polygon points="{x2 + 12:.1f},{y_line:.1f} {x2 + 5:.1f},{y_line - 4:.1f} {x2 + 5:.1f},{y_line + 4:.1f}" fill="{SLATE}"/>',
    ]

    n_ticks = int(round(high - low)) if (high - low) <= 14 and abs(low - round(low)) < 1e-6 and abs(high - round(high)) < 1e-6 else 10
    n_ticks = max(2, min(14, n_ticks))
    for i in range(n_ticks + 1):
        val = low + (span * i) / n_ticks
        tx = to_x(val)
        is_end = i in (0, n_ticks) or i == n_ticks // 2
        tick_h = 8 if is_end else 5
        parts.append(f'<line x1="{tx:.1f}" y1="{y_line - tick_h:.1f}" x2="{tx:.1f}" y2="{y_line + tick_h:.1f}" stroke="{SLATE}" stroke-width="{"1.8" if is_end else "1"}"/>')
        if n_ticks <= 14 and (i % 2 == 0 or n_ticks <= 8 or is_end):
            parts.append(_svg_text(tx, y_line + 21, _fmt_num(val), size=8, fill=SLATE, weight="700" if is_end else "500"))
        elif is_end:
            parts.append(_svg_text(tx, y_line + 21, _fmt_num(val), size=9, fill=BLUE, weight="700"))

    if show_zero and low < 0 < high:
        zx = to_x(0.0)
        parts.append(f'<line x1="{zx:.1f}" y1="{y_line - 12:.1f}" x2="{zx:.1f}" y2="{y_line + 12:.1f}" stroke="{BLUE}" stroke-width="2"/>')
        parts.append(_svg_text(zx, y_line + 21, "0", size=9, fill=BLUE, weight="700"))

    prev_x = -999.0
    tier = 0
    for val, lbl in sorted(points, key=lambda p: p[0]):
        px = to_x(val)
        tier = (tier + 1) % 2 if abs(px - prev_x) < 42 else 0
        prev_x = px
        ly = y_line - (18 if tier == 0 else 32)
        parts.append(f'<line x1="{px:.1f}" y1="{y_line:.1f}" x2="{px:.1f}" y2="{ly + 5:.1f}" stroke="{RED}" stroke-width="1.2" stroke-dasharray="2,2"/>')
        parts.append(f'<circle cx="{px:.1f}" cy="{y_line:.1f}" r="4.5" fill="{RED}" stroke="#ffffff" stroke-width="1.5"/>')
        parts.append(_svg_text(px, ly, lbl, size=9, fill=RED, weight="700"))

    return _wrap_svg("".join(parts), w, h, title_text)


def _try_scale_or_numberline_diagram(
    subcat: str,
    sense: str,
    clean_text: str,
) -> str | None:
    low = clean_text.lower()

    # 1. Termómetro (°C)
    if re.search(r"°\s*c\b|grados\s+c(?:elsius|ent[íi]grados)|term[óo]metro|bajo\s+cero", low):
        temps: list[float] = []
        for m in re.finditer(r"([+-]?\s*\d+(?:[.,]\d+)?)\s*°\s*c\b", low):
            v = _parse_es_num(m.group(1).replace(" ", ""))
            if v is not None:
                temps.append(v)
        for m in re.finditer(r"(\d+(?:[.,]\d+)?)\s*grados?\s+bajo\s+cero", low):
            v = _parse_es_num(m.group(1))
            if v is not None:
                temps.append(-abs(v))
        if temps:
            return _render_thermometer_svg(temps)

    # 2. Altitud / Profundidad respecto al nivel del mar
    if re.search(r"(?:bajo\s+el|sobre\s+el|respecto\s+al)\s+nivel\s+del\s+mar|fosa\s+abisal|submarino", low):
        alts: list[float] = []
        for m in re.finditer(r"([+-]?\d+(?:\.\d{3})*(?:,\d+)?)\s*(?:m\b|metros?)", low):
            v = _parse_es_num(m.group(1))
            if v is not None:
                after = low[m.end() : m.end() + 28]
                if "bajo el nivel del mar" in after and v > 0:
                    v = -v
                alts.append(v)
        if alts:
            return _render_altitude_svg(alts)

    # 3. Recta numérica de enteros (-6 a +6, -7 hasta +5, etc.)
    bounds_m = re.search(r"(?:desde|de)\s+(-\d+)\s+(?:a|hasta)\s+([+-]?\d+)", low)
    if bounds_m or re.search(r"\b(?:escala\s+de\s+enteros|n[úu]meros\s+enteros|recta\s+num[ée]rica)\b", low):
        if bounds_m:
            b1 = float(bounds_m.group(1))
            b2 = float(bounds_m.group(2))
            lo, hi = min(b1, b2), max(b1, b2)
            pts: list[tuple[float, str]] = []
            for m in re.finditer(r"(?<![A-Za-z0-9])([+-]\d+|-\d+)(?!\s*°)", clean_text):
                v = _parse_es_num(m.group(1))
                if v is not None and lo <= v <= hi and (v not in (lo, hi) or "prioridad" in low):
                    pts.append((v, f"{'+' if v > 0 else ''}{_fmt_num(v)}"))
            # Quitar duplicados manteniendo orden
            seen_v: set[float] = set()
            uniq_pts = []
            for pv, pl in pts:
                if pv not in seen_v:
                    seen_v.add(pv)
                    uniq_pts.append((pv, pl))
            return _render_number_line_svg(lo, hi, uniq_pts[:4], "Recta numérica de números enteros", show_zero=True)
        if "neutro (0)" in low or ("enteros" in low and re.search(r"[+-]\d+", clean_text)):
            return _render_number_line_svg(-5, 5, [(0, "Inicio (0)")], "Recta numérica de enteros", show_zero=True)

    # 4. Recta numérica para redondeo / estimación
    is_stat_or_geom = (
        "subcategoría 4" in subcat.lower()
        or "subcategoría 6" in subcat.lower()
        or "espacial" in sense.lower()
        or "estocástico" in sense.lower()
        or bool(re.search(r"\b(?:media|moda|probabilidad|gr[áa]fico|ángulo)\b", low))
    )
    if not is_stat_or_geom and re.search(r"\b(?:redondea|redondeo|m[áa]s\s+cerca)\b", low):
        if re.search(r"\b(?:tienda|poké\s*balls?|precio\s+por)\b", low) and "redondea a las centésimas" in low:
            return None

        step = 100.0
        if re.search(r"mill[óo]n\s+m[áa]s\s+cercano", low):
            step = 1_000_000.0
        elif re.search(r"centena\s+de\s+millar", low):
            step = 100_000.0
        elif re.search(r"decena\s+de\s+millar", low):
            step = 10_000.0
        elif re.search(r"unidad\s+de\s+millar", low):
            step = 1_000.0
        elif re.search(r"centena\s+m[áa]s\s+cercana|centena\s+m[áa]s\s+pr[óo]xima|a\s+qu[ée]\s+centena", low):
            step = 100.0
        elif re.search(r"decena\s+m[áa]s\s+cercana|decena\s+m[áa]s\s+pr[óo]xima|a\s+qu[ée]\s+decena", low):
            step = 10.0
        elif re.search(r"d[ée]cimas?\s+m[áa]s\s+pr[óo]xim", low):
            step = 0.1
        elif re.search(r"cent[ée]simas?\s+m[áa]s\s+pr[óo]xim", low):
            step = 0.01

        nums: list[float] = []
        for m in re.finditer(r"\b\d{1,3}(?:\.\d{3})+(?:,\d+)?\b|\b\d+(?:,\d+)?\b", clean_text):
            v = _parse_es_num(m.group(0))
            if v is None:
                continue
            if step >= 100 and v < 20:
                continue
            if step >= 10_000 and v < 1_000:
                continue
            if v not in nums:
                nums.append(v)

        candidates = [v for v in nums if abs(v % step) > 1e-6] or nums
        if candidates:
            target = candidates[0]
            while step > target and step >= 10:
                step /= 10.0
            lo = math.floor(target / step) * step
            hi = lo + step
            pts = [(target, _fmt_num(target))]
            for extra in candidates[1:4]:
                if lo <= extra <= hi:
                    pts.append((extra, _fmt_num(extra)))
            return _render_number_line_svg(lo, hi, pts, "Recta numérica de aproximación")

    return None


# ---------------------------------------------------------------------------
# 3. Geometría 2D, 3D, Coordenadas, Ángulos y Simetría
# ---------------------------------------------------------------------------

def _render_cartesian_grid_svg(
    points: list[tuple[str, float, float]],
    sym_x: float | None = None,
    connect_poly: bool = False,
) -> str:
    w, h = 230, 150
    xs = [p[1] for p in points]
    ys = [p[2] for p in points]
    if sym_x is not None:
        xs.append(sym_x)
    has_neg = any(x < 0 for x in xs) or any(y < 0 for y in ys)

    if has_neg:
        max_abs = max(max((abs(v) for v in xs + ys), default=6.0), 4.0)
        lim = int(math.ceil(max_abs / 2.0) * 2)
        xmin, xmax, ymin, ymax = -lim, lim, -lim, lim
    else:
        xmin, ymin = 0.0, 0.0
        xmax = math.ceil(max(max(xs, default=8.0) + 2.0, 6.0))
        ymax = math.ceil(max(max(ys, default=8.0) + 2.0, 6.0))

    pad_l, pad_r, pad_t, pad_b = 26.0, 14.0, 12.0, 22.0
    gw = w - pad_l - pad_r
    gh = h - pad_t - pad_b

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * gw

    def sy(y: float) -> float:
        return pad_t + gh - ((y - ymin) / (ymax - ymin)) * gh

    parts: list[str] = [f'<rect x="{pad_l}" y="{pad_t}" width="{gw}" height="{gh}" fill="#ffffff" stroke="{GRID_LINE}" stroke-width="1"/>']

    step_x = max(1, int(math.ceil((xmax - xmin) / 10)))
    step_y = max(1, int(math.ceil((ymax - ymin) / 8)))

    x_val = math.ceil(xmin)
    while x_val <= xmax:
        px = sx(x_val)
        parts.append(f'<line x1="{px:.1f}" y1="{pad_t}" x2="{px:.1f}" y2="{pad_t + gh}" stroke="#e2e8f0" stroke-width="1"/>')
        if x_val % step_x == 0:
            parts.append(_svg_text(px, pad_t + gh + 11, str(int(x_val)), size=7, fill=MUTED))
        x_val += 1

    y_val = math.ceil(ymin)
    while y_val <= ymax:
        py = sy(y_val)
        parts.append(f'<line x1="{pad_l}" y1="{py:.1f}" x2="{pad_l + gw}" y2="{py:.1f}" stroke="#e2e8f0" stroke-width="1"/>')
        if y_val % step_y == 0:
            parts.append(_svg_text(pad_l - 5, py + 2.5, str(int(y_val)), size=7, fill=MUTED, anchor="end"))
        y_val += 1

    ax_y = sy(0.0)
    ax_x = sx(0.0)
    parts.append(f'<line x1="{pad_l}" y1="{ax_y:.1f}" x2="{pad_l + gw + 4:.1f}" y2="{ax_y:.1f}" stroke="{SLATE}" stroke-width="1.6"/>')
    parts.append(f'<line x1="{ax_x:.1f}" y1="{pad_t + gh:.1f}" x2="{ax_x:.1f}" y2="{pad_t - 4:.1f}" stroke="{SLATE}" stroke-width="1.6"/>')
    parts.append(_svg_text(pad_l + gw + 6, ax_y + 3, "X", size=8, fill=INK, anchor="start", weight="700"))
    parts.append(_svg_text(ax_x + 6, pad_t + 6, "Y", size=8, fill=INK, anchor="start", weight="700"))

    if sym_x is not None:
        esx = sx(sym_x)
        parts.append(f'<line x1="{esx:.1f}" y1="{pad_t}" x2="{esx:.1f}" y2="{pad_t + gh}" stroke="{GREEN}" stroke-width="1.6" stroke-dasharray="4,3"/>')
        parts.append(_svg_text(esx + 3, pad_t + 10, f"x={_fmt_num(sym_x)}", size=8, fill=GREEN, anchor="start", weight="700"))

    non_origin = [p for p in points if not (p[0].upper() == "O" and p[1] == 0 and p[2] == 0)]
    if connect_poly and len(non_origin) >= 3:
        pts_str = " ".join(f"{sx(p[1]):.1f},{sy(p[2]):.1f}" for p in non_origin)
        parts.append(f'<polygon points="{pts_str}" fill="{BLUE_FILL}" fill-opacity="0.45" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="3,2"/>')

    for idx, (lbl, px_v, py_v) in enumerate(points[:6]):
        cx = sx(px_v)
        cy = sy(py_v)
        col = RED if idx == 0 else (GREEN if idx == 1 else BLUE)
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.8" fill="{col}" stroke="#ffffff" stroke-width="1.2"/>')
        tag = f"{lbl}({_fmt_num(px_v)},{_fmt_num(py_v)})" if lbl else f"({_fmt_num(px_v)},{_fmt_num(py_v)})"
        tx = cx + (6 if px_v < (xmin + xmax) * 0.7 else -6)
        anc = "start" if px_v < (xmin + xmax) * 0.7 else "end"
        ty = cy - 5 if py_v < ymax * 0.85 else cy + 11
        parts.append(_svg_text(tx, ty, tag, size=8, fill=col, anchor=anc, weight="700"))

    return _wrap_svg("".join(parts), w, h, "Plano cartesiano con puntos de coordenadas")


def _render_board_grid_svg(
    cols: list[str],
    rows: list[str],
    markers: list[tuple[str, str, str, str]],
) -> str:
    ncols, nrows = len(cols), len(rows)
    cell = min(22.0, 110.0 / max(nrows, 1), 150.0 / max(ncols, 1))
    gw, gh = ncols * cell, nrows * cell
    ox = (220.0 - gw) / 2.0 + 8.0
    oy = 16.0
    w, h = 230, max(125, min(150, int(oy + gh + 22)))

    parts: list[str] = []
    for r_idx, r_lbl in enumerate(rows):
        draw_row = (nrows - 1 - r_idx) if rows[0].isdigit() else r_idx
        y = oy + draw_row * cell
        parts.append(_svg_text(ox - 6, y + cell / 2 + 3, r_lbl, size=8, fill=SLATE, anchor="end", weight="700"))
        for c_idx in range(ncols):
            x = ox + c_idx * cell
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell:.1f}" height="{cell:.1f}" fill="#ffffff" stroke="{GRID_LINE}" stroke-width="1"/>')

    for c_idx, c_lbl in enumerate(cols):
        x = ox + c_idx * cell + cell / 2
        parts.append(_svg_text(x, oy + gh + 12, c_lbl, size=8, fill=SLATE, weight="700"))

    col_map = {c.upper(): idx for idx, c in enumerate(cols)}
    row_map = {r.upper(): idx for idx, r in enumerate(rows)}
    for c_lbl, r_lbl, txt, color in markers:
        ci = col_map.get(c_lbl.upper())
        ri = row_map.get(r_lbl.upper())
        if ci is None or ri is None:
            continue
        draw_row = (nrows - 1 - ri) if rows[0].isdigit() else ri
        cx = ox + ci * cell + cell / 2
        cy = oy + draw_row * cell + cell / 2
        parts.append(f'<rect x="{ox + ci * cell + 1.5:.1f}" y="{oy + draw_row * cell + 1.5:.1f}" width="{cell - 3:.1f}" height="{cell - 3:.1f}" rx="3" fill="{color}" fill-opacity="0.18" stroke="{color}" stroke-width="1.3"/>')
        parts.append(_svg_text(cx, cy + 3, txt, size=8, fill=color, weight="700"))

    return _wrap_svg("".join(parts), w, h, "Mapa en cuadrícula con filas y columnas")


def _render_angle_svg(angles: list[float], compass_mode: bool = False) -> str:
    if compass_mode:
        cx, cy, r = 95.0, 74.0, 50.0
        parts = [
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8" stroke-dasharray="3,2"/>',
            f'<line x1="{cx}" y1="{cy - r - 6}" x2="{cx}" y2="{cy + r + 6}" stroke="{GRID_LINE}" stroke-width="1"/>',
            f'<line x1="{cx - r - 6}" y1="{cy}" x2="{cx + r + 6}" y2="{cy}" stroke="{GRID_LINE}" stroke-width="1"/>',
            _svg_text(cx, cy - r - 9, "N (0°)", size=9, fill=BLUE, weight="700"),
            _svg_text(cx + r + 14, cy + 3, "E", size=9, fill=SLATE, weight="700"),
            _svg_text(cx, cy + r + 15, "S", size=9, fill=SLATE, weight="700"),
            _svg_text(cx - r - 12, cy + 3, "O", size=9, fill=SLATE, weight="700"),
            f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r + 8}" stroke="{BLUE}" stroke-width="2.6" stroke-linecap="round"/>',
            f'<polygon points="{cx},{cy - r + 2} {cx - 4},{cy - r + 11} {cx + 4},{cy - r + 11}" fill="{BLUE}"/>',
            f'<path d="M {cx + 12:.1f},{cy - 24:.1f} A 26,26 0 0 1 {cx + 26:.1f},{cy:.1f}" fill="none" stroke="{RED}" stroke-width="2"/>',
            f'<polygon points="{cx + 26:.1f},{cy + 3:.1f} {cx + 22:.1f},{cy - 5:.1f} {cx + 30:.1f},{cy - 5:.1f}" fill="{RED}"/>',
            _svg_text(178, 68, "Giro horario", size=9, fill=RED, anchor="start", weight="700"),
            _svg_text(178, 82, "90° por giro", size=9, fill=SLATE, anchor="start"),
        ]
        return _wrap_svg("".join(parts), 260, 145, "Rosa de los vientos y ángulo de giro")

    w, h = 280 if len(angles) >= 2 else 210, 145
    parts = []
    n = min(3, len(angles))
    slot_w = w / n
    for i, deg in enumerate(angles[:3]):
        deg_clamped = max(10.0, min(180.0, deg))
        ox = i * slot_w + slot_w * 0.25 if deg_clamped < 120 else i * slot_w + slot_w * 0.5
        oy = 104.0
        ray = 52.0 if n == 1 else 36.0
        parts.append(f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{ox + ray:.1f}" y2="{oy:.1f}" stroke="{BLUE}" stroke-width="2.4" stroke-linecap="round"/>')
        rad = math.radians(deg_clamped)
        ex = ox + ray * math.cos(rad)
        ey = oy - ray * math.sin(rad)
        parts.append(f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{RED}" stroke-width="2.4" stroke-linecap="round"/>')
        if abs(deg_clamped - 90.0) < 0.5:
            parts.append(f'<rect x="{ox:.1f}" y="{oy - 11:.1f}" width="11" height="11" fill="none" stroke="{GREEN}" stroke-width="1.5"/>')
        else:
            ar = 18.0
            ax = ox + ar * math.cos(rad)
            ay = oy - ar * math.sin(rad)
            parts.append(f'<path d="M {ox + ar:.1f},{oy:.1f} A {ar},{ar} 0 0 0 {ax:.1f},{ay:.1f}" fill="{AMBER_SOFT}" fill-opacity="0.7" stroke="{AMBER}" stroke-width="1.8"/>')
        parts.append(f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="3" fill="{INK}"/>')
        parts.append(_svg_text(ox + (12 if deg_clamped < 120 else 0), oy + 20, f"{_fmt_num(deg)}°", size=10, fill=INK, weight="700"))

    return _wrap_svg("".join(parts), w, h, "Diagrama de ángulos geométricos")


def _render_prism_svg(dims: list[str], is_cube: bool = False) -> str:
    w, h = 230, 148
    bx, by = 52.0, 52.0
    bw, bh = (64.0, 64.0) if is_cube else (94.0, 54.0)
    dx, dy = 34.0, -24.0

    parts = [
        f'<line x1="{bx + dx:.1f}" y1="{by + dy:.1f}" x2="{bx + dx:.1f}" y2="{by + bh + dy:.1f}" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3,3"/>',
        f'<line x1="{bx:.1f}" y1="{by + bh:.1f}" x2="{bx + dx:.1f}" y2="{by + bh + dy:.1f}" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3,3"/>',
        f'<line x1="{bx + dx:.1f}" y1="{by + bh + dy:.1f}" x2="{bx + bw + dx:.1f}" y2="{by + bh + dy:.1f}" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3,3"/>',
        f'<polygon points="{bx},{by} {bx + bw},{by} {bx + bw + dx},{by + dy} {bx + dx},{by + dy}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>',
        f'<polygon points="{bx + bw},{by} {bx + bw + dx},{by + dy} {bx + bw + dx},{by + bh + dy} {bx + bw},{by + bh}" fill="{BLUE_FILL}" stroke="{BLUE}" stroke-width="1.8"/>',
        f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#ffffff" fill-opacity="0.78" stroke="{BLUE}" stroke-width="2"/>',
    ]

    if is_cube:
        lbl = dims[0] if dims else "Cubo (6 caras)"
        parts.append(_svg_text(bx + bw / 2, by + bh + 16, f"arista = {lbl}" if dims else lbl, size=9, fill=RED, weight="700"))
    else:
        if len(dims) >= 1:
            parts.append(_svg_text(bx + bw / 2, by + bh + 16, dims[0], size=9, fill=RED, weight="700"))
        if len(dims) >= 2:
            parts.append(_svg_text(bx + bw + dx / 2 + 12, by + bh + dy / 2 + 10, dims[1], size=9, fill=GREEN, anchor="start", weight="700"))
        if len(dims) >= 3:
            parts.append(_svg_text(bx - 6, by + bh / 2 + 3, dims[2], size=9, fill=BLUE, anchor="end", weight="700"))

    return _wrap_svg("".join(parts), w, h, "Prisma rectangular tridimensional")


def _render_pyramid_svg() -> str:
    w, h = 200, 145
    apex = (100.0, 20.0)
    fl, fr = (46.0, 114.0), (132.0, 118.0)
    bl, br = (74.0, 88.0), (156.0, 92.0)
    parts = [
        f'<polygon points="{fl[0]},{fl[1]} {fr[0]},{fr[1]} {br[0]},{br[1]} {bl[0]},{bl[1]}" fill="{AMBER_SOFT}" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="3,2"/>',
        f'<line x1="{apex[0]}" y1="{apex[1]}" x2="{bl[0]}" y2="{bl[1]}" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3,2"/>',
        f'<polygon points="{apex[0]},{apex[1]} {fl[0]},{fl[1]} {fr[0]},{fr[1]}" fill="{BLUE_SOFT}" fill-opacity="0.7" stroke="{BLUE}" stroke-width="1.8"/>',
        f'<polygon points="{apex[0]},{apex[1]} {fr[0]},{fr[1]} {br[0]},{br[1]}" fill="{BLUE_FILL}" fill-opacity="0.75" stroke="{BLUE}" stroke-width="1.8"/>',
        _svg_text(100, 136, "Pirámide cuadrangular", size=9, fill=SLATE, weight="700"),
    ]
    return _wrap_svg("".join(parts), w, h, "Pirámide de base cuadrada")


def _render_round_solids_svg(has_cyl: bool, has_sph: bool, has_cone: bool, has_cube: bool, radius_lbl: str = "") -> str:
    w, h = 240, 145
    parts: list[str] = []
    shapes: list[str] = []
    if has_cyl:
        shapes.append("cyl")
    if has_cone:
        shapes.append("cone")
    if has_sph:
        shapes.append("sph")
    if has_cube:
        shapes.append("cube")
    if not shapes:
        shapes = ["cyl"]

    slot = w / len(shapes)
    for idx, kind in enumerate(shapes):
        cx = idx * slot + slot / 2
        if kind == "cyl":
            parts.extend([
                f'<path d="M {cx - 26},98 A 26,9 0 0 0 {cx + 26},98" fill="{BLUE_FILL}" stroke="{BLUE}" stroke-width="1.8"/>',
                f'<path d="M {cx - 26},98 A 26,9 0 0 1 {cx + 26},98" fill="none" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3,2"/>',
                f'<line x1="{cx - 26}" y1="40" x2="{cx - 26}" y2="98" stroke="{BLUE}" stroke-width="1.8"/>',
                f'<line x1="{cx + 26}" y1="40" x2="{cx + 26}" y2="98" stroke="{BLUE}" stroke-width="1.8"/>',
                f'<ellipse cx="{cx}" cy="40" rx="26" ry="9" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>',
                _svg_text(cx, 128, "Cilindro", size=9, fill=BLUE, weight="700"),
            ])
        elif kind == "sph":
            parts.extend([
                f'<circle cx="{cx}" cy="68" r="34" fill="{RED_SOFT}" stroke="{RED}" stroke-width="2"/>',
                f'<ellipse cx="{cx}" cy="68" rx="34" ry="10" fill="none" stroke="{RED}" stroke-width="1.3" stroke-dasharray="3,2"/>',
            ])
            if radius_lbl:
                parts.append(f'<line x1="{cx}" y1="68" x2="{cx + 34}" y2="68" stroke="{BLUE}" stroke-width="2"/>')
                parts.append(f'<circle cx="{cx}" cy="68" r="2.6" fill="{INK}"/>')
                parts.append(_svg_text(cx, 128, radius_lbl, size=9, fill=BLUE, weight="700"))
            else:
                parts.append(_svg_text(cx, 128, "Esfera", size=9, fill=RED, weight="700"))
        elif kind == "cone":
            parts.extend([
                f'<path d="M {cx - 26},98 L {cx},32 L {cx + 26},98" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.8"/>',
                f'<ellipse cx="{cx}" cy="98" rx="26" ry="8" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.8"/>',
                _svg_text(cx, 128, "Cono", size=9, fill=GREEN, weight="700"),
            ])
        elif kind == "cube":
            bx, by, s = cx - 22, 54, 38
            parts.extend([
                f'<polygon points="{bx},{by} {bx + s},{by} {bx + s + 14},{by - 12} {bx + 14},{by - 12}" fill="{AMBER_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>',
                f'<polygon points="{bx + s},{by} {bx + s + 14},{by - 12} {bx + s + 14},{by + s - 12} {bx + s},{by + s}" fill="{BLUE_FILL}" stroke="{BLUE}" stroke-width="1.6"/>',
                f'<rect x="{bx}" y="{by}" width="{s}" height="{s}" fill="#ffffff" stroke="{BLUE}" stroke-width="1.8"/>',
                _svg_text(cx, 128, "Cubo", size=9, fill=BLUE, weight="700"),
            ])

    return _wrap_svg("".join(parts), w, h, "Cuerpos geométricos tridimensionales")


def _render_2d_shape_svg(low: str, clean_text: str) -> str | None:
    # A. Casos de simetría
    if re.search(r"\bsimetr[íi]a\b", low):
        if "mew" in low:
            w, h = 230, 130
            parts = []
            for idx, ch in enumerate(["M", "E", "W"]):
                cx = 48 + idx * 66
                parts.append(_svg_text(cx, 78, ch, size=40, fill=BLUE, weight="800"))
                parts.append(f'<line x1="{cx}" y1="26" x2="{cx}" y2="96" stroke="{RED}" stroke-width="1.8" stroke-dasharray="4,3"/>')
            parts.append(_svg_text(115, 116, "Eje de simetría vertical", size=9, fill=RED, weight="700"))
            return _wrap_svg("".join(parts), w, h, "Simetría vertical en letras MEW")

        if "butterfree" in low or "manchas" in low:
            w, h = 240, 145
            cx = 120.0
            parts = [
                f'<path d="M {cx},32 C 62,18 32,58 52,102 C 74,116 106,96 {cx},88 Z" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>',
                f'<path d="M {cx},32 C 178,18 208,58 188,102 C 166,116 134,96 {cx},88 Z" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="3,2"/>',
                f'<line x1="{cx}" y1="16" x2="{cx}" y2="124" stroke="{RED}" stroke-width="2" stroke-dasharray="4,3"/>',
            ]
            for idx, dist in enumerate([4, 8, 12]):
                sx = cx - dist * 5.2
                sy = 46 + idx * 20
                parts.append(f'<circle cx="{sx:.1f}" cy="{sy}" r="4.5" fill="{AMBER}" stroke="{BLUE}" stroke-width="1.2"/>')
                parts.append(_svg_text(sx, sy - 8, f"{dist} cm", size=8, fill=SLATE, weight="700"))
            parts.append(_svg_text(165, 70, "? cm", size=11, fill=RED, weight="700"))
            parts.append(_svg_text(cx, 138, "Eje de simetría", size=9, fill=RED, weight="700"))
            return _wrap_svg("".join(parts), w, h, "Simetría axial de las alas de Butterfree")

    # B. Mosaico de polígonos distintos (ej. 3, 5 y 6 lados) o cuadrados + círculos o rectángulo + triángulo
    if "baldosa a" in low and "baldosa b" in low and "baldosa c" in low:
        w, h = 270, 132
        pts5 = " ".join(f"{135 + 26 * math.cos(math.radians(72 * k - 90)):.1f},{62 + 26 * math.sin(math.radians(72 * k - 90)):.1f}" for k in range(5))
        pts6 = " ".join(f"{220 + 26 * math.cos(math.radians(60 * k)):.1f},{62 + 26 * math.sin(math.radians(60 * k)):.1f}" for k in range(6))
        parts = [
            f'<polygon points="48,36 22,86 74,86" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>',
            _svg_text(48, 108, "Baldosa A", size=8, fill=BLUE, weight="700"),
            f'<polygon points="{pts5}" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2"/>',
            _svg_text(135, 108, "Baldosa B", size=8, fill=GREEN, weight="700"),
            f'<polygon points="{pts6}" fill="{AMBER_SOFT}" stroke="{AMBER_DARK}" stroke-width="2"/>',
            _svg_text(220, 108, "Baldosa C", size=8, fill=AMBER_DARK, weight="700"),
        ]
        return _wrap_svg("".join(parts), w, h, "Mosaico con tres baldosas poligonales")

    if "cuadrados" in low and "círculos" in low:
        w, h = 230, 125
        parts = [
            f'<rect x="34" y="28" width="60" height="60" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>',
            _svg_text(64, 108, "Cuadrado", size=9, fill=BLUE, weight="700"),
            f'<circle cx="164" cy="58" r="30" fill="{RED_SOFT}" stroke="{RED}" stroke-width="2"/>',
            _svg_text(164, 108, "Círculo", size=9, fill=RED, weight="700"),
        ]
        return _wrap_svg("".join(parts), w, h, "Cuadrados de líneas rectas y círculos de líneas curvas")

    if ("rectángulo" in low or "rectangular" in low) and ("triángulo" in low or "triangular" in low) and ("al lado" in low or "adosado" in low or "sobre una gran explanada" in low):
        w, h = 260, 140
        if "sobre una gran explanada" in low:
            parts = [
                f'<rect x="34" y="20" width="192" height="96" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2"/>',
                f'<polygon points="130,36 86,98 174,98" fill="{AMBER_SOFT}" stroke="{AMBER_DARK}" stroke-width="1.8"/>',
                _svg_text(130, 130, "Explanada 50 × 30 m (tarima b=20, h=14)", size=8, fill=INK, weight="700"),
            ]
            return _wrap_svg("".join(parts), w, h, "Tarima triangular sobre explanada rectangular")
        if "adosado" in low:
            parts = [
                f'<rect x="34" y="34" width="110" height="68" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>',
                f'<polygon points="144,34 196,68 144,102" fill="{AMBER_SOFT}" stroke="{AMBER_DARK}" stroke-width="2"/>',
                _svg_text(89, 72, "20 × 12 m", size=9, fill=BLUE, weight="700"),
                _svg_text(166, 120, "b=12, h=7 m", size=8, fill=AMBER_DARK, weight="700"),
            ]
            return _wrap_svg("".join(parts), w, h, "Rectángulo con triángulo adosado")
        parts = [
            f'<rect x="28" y="32" width="90" height="62" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>',
            f'<polygon points="186,32 146,94 226,94" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2"/>',
            _svg_text(73, 114, "Rectángulo", size=9, fill=BLUE, weight="700"),
            _svg_text(186, 114, "Triángulo", size=9, fill=GREEN, weight="700"),
        ]
        return _wrap_svg("".join(parts), w, h, "Rectángulo y triángulo separados")

    # C. Corona circular (R y r)
    if "corona circular" in low or (re.search(r"\bR\s*=\s*\d+", clean_text) and re.search(r"\br\s*=\s*\d+", clean_text)):
        m_big = re.search(r"\bR\s*=\s*(\d+(?:[.,]\d+)?)\s*(cm|m|dm)?", clean_text)
        m_sml = re.search(r"\br\s*=\s*(\d+(?:[.,]\d+)?)\s*(cm|m|dm)?", clean_text)
        r_big = f"R = {m_big.group(1)} {m_big.group(2) or ''}".strip() if m_big else "R"
        r_sml = f"r = {m_sml.group(1)} {m_sml.group(2) or ''}".strip() if m_sml else "r"
        w, h = 210, 145
        cx, cy = 85.0, 72.0
        parts = [
            f'<circle cx="{cx}" cy="{cy}" r="54" fill="{BLUE_FILL}" stroke="{BLUE}" stroke-width="2"/>',
            f'<circle cx="{cx}" cy="{cy}" r="24" fill="{AMBER_SOFT}" stroke="{AMBER_DARK}" stroke-width="1.8"/>',
            f'<line x1="{cx}" y1="{cy}" x2="{cx + 54}" y2="{cy}" stroke="{BLUE}" stroke-width="1.6"/>',
            f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 24}" stroke="{RED}" stroke-width="1.6"/>',
            f'<circle cx="{cx}" cy="{cy}" r="2.8" fill="{INK}"/>',
            _svg_text(152, 62, r_big, size=9, fill=BLUE, anchor="start", weight="700"),
            _svg_text(152, 82, r_sml, size=9, fill=RED, anchor="start", weight="700"),
        ]
        return _wrap_svg("".join(parts), w, h, "Corona circular concéntrica")

    # D. Estadio con remates semicirculares
    if "semicírculo" in low and "rectángulo" in low:
        w, h = 250, 140
        parts = [
            f'<rect x="65" y="34" width="120" height="68" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.8" stroke-dasharray="3,2"/>',
            f'<path d="M 65,34 A 34,34 0 0 0 65,102" fill="{BLUE_FILL}" stroke="{BLUE}" stroke-width="2"/>',
            f'<path d="M 185,34 A 34,34 0 0 1 185,102" fill="{BLUE_FILL}" stroke="{BLUE}" stroke-width="2"/>',
            f'<line x1="65" y1="34" x2="185" y2="34" stroke="{BLUE}" stroke-width="2"/>',
            f'<line x1="65" y1="102" x2="185" y2="102" stroke="{BLUE}" stroke-width="2"/>',
            _svg_text(125, 120, "20 m", size=10, fill=BLUE, weight="700"),
            _svg_text(125, 72, "d = 10 m", size=9, fill=RED, weight="700"),
        ]
        return _wrap_svg("".join(parts), w, h, "Estadio rectangular con semicírculos en los extremos")

    # E. Círculo / circunferencia / Poké Ball
    no_unit_square = re.sub(r"\b(?:metros?|cent[íi]metros?|dec[íi]metros?)\s+cuadrados\b", "", low)
    if re.search(r"\b(?:c[íi]rculo|circular|circunferencia|esf[ée]rico|rodadura)\b", low) and not re.search(r"\bcuadrad[oa]\b", no_unit_square):
        m_r = re.search(r"\b(?:radio(?:\s+exterior)?\s*(?:de\s*)?r?\s*=\s*|r\s*=\s*)(\d+(?:[.,]\d+)?)\s*(cm|m|dm)?", low)
        m_d = re.search(r"\bdi[áa]metro(?:\s+medido)?\s*(?:de\s*)?(\d+(?:[.,]\d+)?)\s*(cm|m|dm)?", low)
        m_p = re.search(r"longitud(?:\s+perimetral)?(?:\s+medida\s+exactamente)?\s*(?:de\s*)?(\d+(?:[.,]\d+)?)\s*(cm|m|dm)?", low)
        w, h = 210, 145
        cx, cy, rr = 105.0, 68.0, 48.0
        parts = [f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2.2"/>']
        if m_r:
            lbl = f"r = {m_r.group(1)} {m_r.group(2) or ''}".strip()
            parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + rr}" y2="{cy}" stroke="{RED}" stroke-width="2"/>')
            parts.append(_svg_text(cx + rr / 2, cy - 6, lbl, size=9, fill=RED, weight="700"))
        elif m_d:
            lbl = f"d = {m_d.group(1)} {m_d.group(2) or ''}".strip()
            parts.append(f'<line x1="{cx - rr}" y1="{cy}" x2="{cx + rr}" y2="{cy}" stroke="{RED}" stroke-width="2"/>')
            parts.append(_svg_text(cx, cy - 6, lbl, size=9, fill=RED, weight="700"))
        elif m_p:
            lbl = f"P = {m_p.group(1)} {m_p.group(2) or ''}".strip()
            parts.append(_svg_text(cx, 134, lbl, size=9, fill=BLUE, weight="700"))
            parts.append(_svg_text(cx, cy + 4, "r = ?", size=10, fill=RED, weight="700"))
        else:
            parts.append(f'<line x1="{cx - rr}" y1="{cy}" x2="{cx + rr}" y2="{cy}" stroke="{RED}" stroke-width="1.6"/>')
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="#ffffff" stroke="{RED}" stroke-width="2"/>')
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="2.6" fill="{INK}"/>')
        return _wrap_svg("".join(parts), w, h, "Círculo geométrico")

    # F. Cuadrícula de baldosas / píxeles / cuadrado perfecto
    if re.search(r"\b(?:baldosas?|p[íi]xeles|cuadraditos|tatamis|cuadrado\s+perfecto|cuadrado\s+m[áa]gico)\b", low):
        if "cuadrado mágico" in low:
            cells = re.findall(r"\|\s*(\d+|\?)\s*\|\s*(\d+|\?)\s*\|\s*(\d+|\?)\s*\|", clean_text)
            if len(cells) >= 3:
                w, h = 180, 138
                parts = []
                for r in range(3):
                    for c in range(3):
                        x, y = 42 + c * 32, 18 + r * 32
                        val = cells[r][c]
                        is_q = val == "?"
                        parts.append(f'<rect x="{x}" y="{y}" width="32" height="32" fill="{AMBER_SOFT if is_q else BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5"/>')
                        parts.append(_svg_text(x + 16, y + 20, val, size=11, fill=RED if is_q else INK, weight="700"))
                parts.append(_svg_text(90, 130, "Cuadrado mágico", size=9, fill=SLATE, weight="700"))
                return _wrap_svg("".join(parts), w, h, "Cuadrado mágico 3 por 3")

        m_fc_grid = re.search(r"(\d+)\s+filas,\s+con\s+(\d+)\s+baldosas", low)
        if m_fc_grid:
            rows_n, cols_n = int(m_fc_grid.group(1)), int(m_fc_grid.group(2))
            cell = min(22.0, 96.0 / rows_n, 160.0 / cols_n)
            gw, gh = cols_n * cell, rows_n * cell
            ox, oy = (220 - gw) / 2, 18.0
            parts = []
            for r in range(rows_n):
                for c in range(cols_n):
                    parts.append(f'<rect x="{ox + c * cell:.1f}" y="{oy + r * cell:.1f}" width="{cell:.1f}" height="{cell:.1f}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1"/>')
            parts.append(_svg_text(110, oy + gh + 16, f"{rows_n} filas × {cols_n} col.", size=9, fill=BLUE, weight="700"))
            return _wrap_svg("".join(parts), 220, 140, f"Cuadrícula de {rows_n} por {cols_n} baldosas")

        m_grid = re.search(r"(\d+)\s*(?:baldosas|cuadraditos|filas|metros)?\s*(?:de\s+largo\s*)?(?:por|×|x)\s*(\d+)", low)
        if m_grid:
            cols_n, rows_n = int(m_grid.group(1)), int(m_grid.group(2))
            if 2 <= cols_n <= 12 and 2 <= rows_n <= 12:
                cell = min(22.0, 96.0 / rows_n, 160.0 / cols_n)
                gw, gh = cols_n * cell, rows_n * cell
                ox, oy = (220 - gw) / 2, 16.0
                parts = []
                for r in range(rows_n):
                    for c in range(cols_n):
                        parts.append(f'<rect x="{ox + c * cell:.1f}" y="{oy + r * cell:.1f}" width="{cell:.1f}" height="{cell:.1f}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1"/>')
                parts.append(_svg_text(110, oy + gh + 16, f"{cols_n} × {rows_n}", size=10, fill=RED, weight="700"))
                return _wrap_svg("".join(parts), 220, 145, f"Cuadrícula de {cols_n} por {rows_n}")

        m_side = re.search(r"(\d+)\s*(?:baldosas|filas|metros)\s+por\s+lado", low)
        if m_side:
            n = int(m_side.group(1))
            vis_n = min(n, 8)
            cell = 92.0 / vis_n
            ox, oy = 64.0, 16.0
            parts = []
            for r in range(vis_n):
                for c in range(vis_n):
                    is_border = r in (0, vis_n - 1) or c in (0, vis_n - 1)
                    fill = AMBER_SOFT if (is_border and "borde" in low) else BLUE_SOFT
                    parts.append(f'<rect x="{ox + c * cell:.1f}" y="{oy + r * cell:.1f}" width="{cell:.1f}" height="{cell:.1f}" fill="{fill}" stroke="{BLUE}" stroke-width="1"/>')
            parts.append(_svg_text(110, 128, f"{n} × {n} baldosas", size=10, fill=RED, weight="700"))
            return _wrap_svg("".join(parts), 220, 142, f"Cuadrícula cuadrada de {n} por {n}")

    # G. Figura en L
    if re.search(r"forma\s+de\s+l\b|pol[íi]gono\s+en\s+'l'", low):
        w, h = 230, 145
        parts = [
            f'<polygon points="48,22 108,22 108,68 182,68 182,118 48,118" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2.2"/>',
            f'<line x1="108" y1="68" x2="108" y2="118" stroke="{RED}" stroke-width="1.3" stroke-dasharray="3,2"/>',
            _svg_text(115, 136, "Figura compuesta en forma de L", size=9, fill=SLATE, weight="700"),
        ]
        return _wrap_svg("".join(parts), w, h, "Polígono compuesto en forma de L")

    # H. Rectángulos anidados o rombo inscrito
    if "rombo" in low and "rect" in low:
        w, h = 230, 145
        parts = [
            f'<rect x="40" y="24" width="150" height="92" fill="{RED_SOFT}" stroke="{RED}" stroke-width="2"/>',
            f'<polygon points="115,24 190,70 115,116 40,70" fill="{BLUE_FILL}" stroke="{BLUE}" stroke-width="2"/>',
            f'<line x1="40" y1="70" x2="190" y2="70" stroke="{SLATE}" stroke-width="1" stroke-dasharray="3,2"/>',
            f'<line x1="115" y1="24" x2="115" y2="116" stroke="{SLATE}" stroke-width="1" stroke-dasharray="3,2"/>',
            _svg_text(115, 134, "16 m × 10 m", size=9, fill=INK, weight="700"),
        ]
        return _wrap_svg("".join(parts), w, h, "Rombo inscrito en un rectángulo")

    if ("pasillo" in low and "piscina" in low) or ("laguna" in low and "exterior" in low):
        w, h = 240, 145
        parts = [
            f'<rect x="35" y="18" width="170" height="102" fill="{AMBER_SOFT}" stroke="{AMBER_DARK}" stroke-width="2"/>',
            f'<rect x="65" y="38" width="110" height="62" fill="{BLUE_FILL}" stroke="{BLUE}" stroke-width="2"/>',
            _svg_text(120, 73, "Zona interior", size=9, fill=BLUE, weight="700"),
            _svg_text(120, 136, "Recinto exterior + interior", size=9, fill=SLATE, weight="700"),
        ]
        return _wrap_svg("".join(parts), w, h, "Rectángulo exterior con recinto interior")

    # I. Dos figuras comparativas lado a lado
    if re.search(r"\b(?:ambas\s+pistas|dos\s+parcelas|dos\s+diseños|diseño\s+a)\b", low):
        dims_list = re.findall(r"(\d+(?:[.,]\d+)?)\s*(?:m|metros?)\s*(?:de\s+largo\s*)?(?:por|×|x)\s*(\d+(?:[.,]\d+)?)\s*(?:m|metros?)?", low)
        sq_m = re.search(r"cuadrad[oa][^.\n]{0,30}?(\d+(?:[.,]\d+)?)\s*(?:m|metros?)\s+de\s+lado", low)
        w, h = 270, 140
        parts = []
        if sq_m and dims_list:
            sl = sq_m.group(1)
            l1, w1 = dims_list[0]
            parts.extend([
                f'<rect x="26" y="28" width="76" height="76" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>',
                _svg_text(64, 70, f"{sl} m", size=9, fill=BLUE, weight="700"),
                _svg_text(64, 120, "Diseño cuadrado", size=8, fill=SLATE, weight="700"),
                f'<rect x="140" y="36" width="106" height="60" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2"/>',
                _svg_text(193, 109, f"{l1} m × {w1} m", size=9, fill=GREEN, weight="700"),
                _svg_text(193, 124, "Diseño rectangular", size=8, fill=SLATE, weight="700"),
            ])
            return _wrap_svg("".join(parts), w, h, "Comparación entre pista cuadrada y rectangular")
        if len(dims_list) >= 2:
            (l1, w1), (l2, w2) = dims_list[0], dims_list[1]
            parts.extend([
                f'<rect x="22" y="38" width="96" height="52" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>',
                _svg_text(70, 68, f"{l1}×{w1} m", size=9, fill=BLUE, weight="700"),
                _svg_text(70, 112, "Parcela A", size=8, fill=SLATE, weight="700"),
                f'<rect x="148" y="32" width="96" height="64" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2"/>',
                _svg_text(196, 68, f"{l2}×{w2} m", size=9, fill=GREEN, weight="700"),
                _svg_text(196, 112, "Parcela B", size=8, fill=SLATE, weight="700"),
            ])
            return _wrap_svg("".join(parts), w, h, "Comparación de dos parcelas rectangulares")

    # J. Polígonos específicos: hexágono, pentágono (o 5 lados), trapecio, romboide
    if "hexágono" in low or ("panal" in low and "6 lados" in low):
        w, h = 230, 145
        count_3 = "3 celdas" in low or "3 celdillas" in low
        parts = []
        centers = [(66.0, 68.0), (115.0, 68.0), (164.0, 68.0)] if count_3 else [(115.0, 68.0)]
        rad = 28.0 if count_3 else 46.0
        for cx, cy in centers:
            pts = []
            for k in range(6):
                a = math.radians(60 * k + 30)
                pts.append(f"{cx + rad * math.cos(a):.1f},{cy + rad * math.sin(a):.1f}")
            parts.append(f'<polygon points="{" ".join(pts)}" fill="{AMBER_SOFT}" stroke="{AMBER_DARK}" stroke-width="2"/>')
        m_l = re.search(r"lados?\s+de\s+(\d+(?:[.,]\d+)?)\s*(cm|m)", low)
        m_ap = re.search(r"apotema\s+de\s+(\d+(?:[.,]\d+)?)\s*(cm|m)", low)
        if not count_3 and m_ap:
            parts.append(f'<line x1="115" y1="68" x2="115" y2="{68 + rad * math.cos(math.radians(30)):.1f}" stroke="{RED}" stroke-width="1.8" stroke-dasharray="3,2"/>')
            parts.append(_svg_text(170, 64, f"ap = {m_ap.group(1)} {m_ap.group(2)}", size=8, fill=RED, anchor="start", weight="700"))
        if m_l:
            parts.append(_svg_text(115, 134, f"lado = {m_l.group(1)} {m_l.group(2)}", size=9, fill=BLUE, weight="700"))
        elif re.search(r"5\s*cm\s+de\s+lado", low):
            parts.append(_svg_text(115, 134, "lado = 5 cm", size=9, fill=BLUE, weight="700"))
        return _wrap_svg("".join(parts), w, h, "Hexágono regular")

    if "pentágono" in low or "cinco lados" in low:
        w, h = 230, 148
        cx, cy, rad = 115.0, 74.0, 48.0
        pts_xy = []
        for k in range(5):
            a = math.radians(72 * k - 90)
            pts_xy.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
        pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts_xy)
        parts = [f'<polygon points="{pts_str}" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2"/>']
        sides = re.findall(r"(\d+(?:[.,]\d+)?)\s*(?:m\b|metros?)", low)
        if len(sides) >= 5:
            for k in range(5):
                x1, y1 = pts_xy[k]
                x2, y2 = pts_xy[(k + 1) % 5]
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                nx, ny = cx + (mx - cx) * 1.32, cy + (my - cy) * 1.32
                parts.append(_svg_text(nx, ny + 3, f"{sides[k]} m", size=8, fill=INK, weight="700"))
        return _wrap_svg("".join(parts), w, h, "Pentágono con longitudes de lados")

    if "trapecio" in low:
        w, h = 230, 140
        parts = [
            f'<polygon points="75,32 155,32 190,104 40,104" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>',
            _svg_text(115, 24, "8 m", size=9, fill=BLUE, weight="700"),
            _svg_text(115, 122, "16 m", size=9, fill=BLUE, weight="700"),
            _svg_text(44, 68, "10 m", size=9, fill=RED, weight="700"),
            _svg_text(186, 68, "10 m", size=9, fill=RED, weight="700"),
        ]
        return _wrap_svg("".join(parts), w, h, "Trapecio isósceles")

    if "romboide" in low:
        w, h = 240, 142
        m_b = re.search(r"base\s+de\s+(\d+(?:[.,]\d+)?)\s*(m|cm)", low)
        m_h = re.search(r"altura[^.\n]{0,20}?(\d+(?:[.,]\d+)?)\s*(m|cm)", low)
        b_lbl = f"b = {m_b.group(1)} {m_b.group(2)}" if m_b else "base"
        h_lbl = f"h = {m_h.group(1)} {m_h.group(2)}" if m_h else "altura"
        parts = [
            f'<polygon points="68,30 198,30 170,106 40,106" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2"/>',
            f'<line x1="68" y1="30" x2="68" y2="106" stroke="{RED}" stroke-width="1.6" stroke-dasharray="4,2"/>',
            f'<rect x="68" y="96" width="10" height="10" fill="none" stroke="{RED}" stroke-width="1.2"/>',
            _svg_text(74, 72, h_lbl, size=9, fill=RED, anchor="start", weight="700"),
            _svg_text(105, 124, b_lbl, size=9, fill=GREEN, weight="700"),
        ]
        return _wrap_svg("".join(parts), w, h, "Romboide con base y altura")

    # K. Triángulos
    if re.search(r"\btri[áa]ngul[oa]s?\b", low):
        if "terreno 1" in low and "terreno 2" in low:
            w, h = 280, 138
            parts = [
                f'<polygon points="48,26 16,94 80,94" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>',
                _svg_text(48, 112, "10, 10, 10 m", size=8, fill=BLUE, weight="700"),
                _svg_text(48, 125, "60°", size=8, fill=SLATE),
                f'<polygon points="140,46 98,94 186,94" fill="{AMBER_SOFT}" stroke="{AMBER_DARK}" stroke-width="1.8"/>',
                _svg_text(142, 112, "8, 8, 12 m", size=8, fill=AMBER_DARK, weight="700"),
                _svg_text(142, 125, "110°", size=8, fill=SLATE),
                f'<polygon points="212,26 212,94 264,94" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.8"/>',
                f'<rect x="212" y="84" width="9" height="10" fill="none" stroke="{GREEN}" stroke-width="1.2"/>',
                _svg_text(238, 112, "6, 8, 10 m", size=8, fill=GREEN, weight="700"),
                _svg_text(238, 125, "90°", size=8, fill=SLATE),
            ]
            return _wrap_svg("".join(parts), w, h, "Tres terrenos triangulares")

        w, h = 220, 142
        parts = [f'<polygon points="110,22 44,112 176,112" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2.2"/>']
        sides = re.findall(r"(\d+(?:[.,]\d+)?)\s*(cm|m|dm|metros?|cent[íi]metros?)", low)
        if "mitad del lado de abajo" in low:
            parts.append(f'<line x1="110" y1="22" x2="110" y2="112" stroke="{RED}" stroke-width="1.8"/>')
        elif "tres lados exactamente iguales" in low or "equilátero" in low:
            if sides:
                lbl = f"{sides[0][0]} {'cm' if 'cm' in sides[0][1] else 'm'}"
                parts.append(_svg_text(64, 64, lbl, size=9, fill=BLUE, anchor="end", weight="700"))
                parts.append(_svg_text(156, 64, lbl, size=9, fill=BLUE, anchor="start", weight="700"))
                parts.append(_svg_text(110, 130, lbl, size=9, fill=BLUE, weight="700"))
        elif len(sides) >= 3:
            u = "cm" if "cm" in sides[0][1] or "cent" in sides[0][1] else "m"
            parts.append(_svg_text(66, 64, f"{sides[0][0]} {u}", size=9, fill=BLUE, anchor="end", weight="700"))
            parts.append(_svg_text(154, 64, f"{sides[1][0]} {u}", size=9, fill=BLUE, anchor="start", weight="700"))
            parts.append(_svg_text(110, 130, f"{sides[2][0]} {u}", size=9, fill=RED, weight="700"))
        elif "dos lados iguales" in low and len(sides) >= 2:
            u = "cm" if "cm" in sides[0][1] or "cent" in sides[0][1] else "m"
            parts.append(_svg_text(66, 64, f"{sides[0][0]} {u}", size=9, fill=BLUE, anchor="end", weight="700"))
            parts.append(_svg_text(154, 64, f"{sides[0][0]} {u}", size=9, fill=BLUE, anchor="start", weight="700"))
            parts.append(_svg_text(110, 130, f"{sides[1][0]} {u}", size=9, fill=RED, weight="700"))
        elif "base" in low and "altura" in low and len(sides) >= 2:
            parts.append(f'<line x1="110" y1="22" x2="110" y2="112" stroke="{RED}" stroke-width="1.6" stroke-dasharray="3,2"/>')
            parts.append(_svg_text(116, 74, f"h = {sides[1][0]}", size=9, fill=RED, anchor="start", weight="700"))
            parts.append(_svg_text(110, 130, f"b = {sides[0][0]}", size=9, fill=BLUE, weight="700"))
        else:
            for vx, vy in [(110, 22), (44, 112), (176, 112)]:
                parts.append(f'<circle cx="{vx}" cy="{vy}" r="3.5" fill="{RED}"/>')
        return _wrap_svg("".join(parts), w, h, "Figura geométrica triangular")

    # L. Rectángulos y cuadrados generales
    if re.search(r"\b(?:rect[áa]ngulo|rectangular|marco|tatami|cuadrado|cuadrada|recinto|piscina|plataforma|estadio)\b", low):
        m_dims = re.search(
            r"(\d+(?:[.,]\d+)?)\s*(cm|m|dm|metros?|cent[íi]metros?)\s*(?:de\s+(?:largo|longitud)\s*)?(?:por|y|×|x)\s*(\d+(?:[.,]\d+)?)\s*(cm|m|dm|metros?|cent[íi]metros?)",
            low,
        )
        m_lc = re.search(r"largos?\s+miden\s+(\d+(?:[.,]\d+)?)\s*(cm|m|metros?).*?cortos?\s+miden\s+(\d+(?:[.,]\d+)?)\s*(cm|m|metros?)", low)
        if m_dims or m_lc:
            if m_dims:
                d1, u1, d2 = m_dims.group(1), m_dims.group(2), m_dims.group(3)
            else:
                d1, u1, d2 = m_lc.group(1), m_lc.group(2), m_lc.group(3)
            unit = "cm" if "cm" in u1 or "cent" in u1 else ("dm" if "dm" in u1 else "m")
            w, h = 230, 142
            parts = [
                f'<rect x="44" y="26" width="132" height="78" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2.2"/>',
                _svg_text(110, 122, f"{d1} {unit}", size=10, fill=BLUE, weight="700"),
                _svg_text(184, 68, f"{d2} {unit}", size=10, fill=RED, anchor="start", weight="700"),
            ]
            return _wrap_svg("".join(parts), w, h, f"Rectángulo de {d1} por {d2} {unit}")

        m_area_only = re.search(r"superficie\s+sea\s+(?:exactamente\s+)?(\d+(?:[.,]\d+)?)\s*m²", low)
        if m_area_only:
            w, h = 220, 136
            parts = [
                f'<rect x="46" y="26" width="128" height="78" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2.2"/>',
                _svg_text(110, 69, f"Área = {m_area_only.group(1)} m²", size=10, fill=GREEN, weight="700"),
                _svg_text(110, 120, "b × h = 240", size=9, fill=SLATE, weight="700"),
            ]
            return _wrap_svg("".join(parts), w, h, f"Estadio rectangular de {m_area_only.group(1)} metros cuadrados")

        if "cuadrado" in low or "cuadrada" in low:
            m_sq = re.search(r"(\d+(?:[.,]\d+)?)\s*(cm|m|dm|metros?|cent[íi]metros?)\s+(?:de\s+)?(?:lado|longitud|cada\s+uno)", low)
            if not m_sq:
                m_sq = re.search(r"lados?\s+miden\s+(\d+(?:[.,]\d+)?)\s*(cm|m|dm|metros?|cent[íi]metros?)", low)
            m_p = re.search(r"recorre\s+exactamente\s+(\d+(?:[.,]\d+)?)\s*(m|metros?)", low)
            w, h = 200, 142
            parts = [f'<rect x="56" y="20" width="88" height="88" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2.2"/>']
            if m_sq:
                u = "cm" if "cm" in m_sq.group(2) or "cent" in m_sq.group(2) else "m"
                parts.append(_svg_text(100, 126, f"lado = {m_sq.group(1)} {u}", size=10, fill=RED, weight="700"))
            elif m_p:
                parts.append(_svg_text(100, 126, f"Perímetro = {m_p.group(1)} m", size=10, fill=RED, weight="700"))
            else:
                for vx, vy in [(56, 20), (144, 20), (56, 108), (144, 108)]:
                    parts.append(f'<circle cx="{vx}" cy="{vy}" r="3.2" fill="{RED}"/>')
            return _wrap_svg("".join(parts), w, h, "Cuadrado geométrico")

        w, h = 210, 136
        parts = [f'<rect x="42" y="28" width="126" height="76" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2.2"/>']
        for vx, vy in [(42, 28), (168, 28), (42, 104), (168, 104)]:
            parts.append(f'<circle cx="{vx}" cy="{vy}" r="3.4" fill="{RED}"/>')
        return _wrap_svg("".join(parts), w, h, "Rectángulo geométrico")

    # M. Posición espacial (1º Primaria: izquierda/derecha, dentro/fuera, arriba/abajo, laberinto)
    if "laberinto" in low and "norte" in low:
        w, h = 210, 142
        parts = [
            f'<polyline points="72,112 72,38 136,38 136,112" fill="none" stroke="{BLUE}" stroke-width="2.6" stroke-linejoin="round"/>',
            f'<circle cx="72" cy="112" r="4" fill="{GREEN}"/>',
            f'<polygon points="136,118 131,106 141,106" fill="{RED}"/>',
            _svg_text(58, 75, "4 m", size=9, fill=BLUE, anchor="end", weight="700"),
            _svg_text(104, 30, "3 m", size=9, fill=BLUE, weight="700"),
            _svg_text(146, 75, "4 m", size=9, fill=BLUE, anchor="start", weight="700"),
            _svg_text(182, 34, "N ↑", size=9, fill=RED, weight="700"),
        ]
        return _wrap_svg("".join(parts), w, h, "Recorrido con giros en el laberinto")

    if "dentro" in low and "fuera" in low and "hierba" in low:
        m_in = re.search(r"dentro[^.\n]{0,25}?(\d+)", low)
        m_out = re.search(r"fuera[^.\n]{0,35}?(\d+)", low)
        n_in = m_in.group(1) if m_in else "?"
        n_out = m_out.group(1) if m_out else "?"
        w, h = 230, 140
        parts = [
            f'<rect x="20" y="16" width="190" height="108" rx="10" fill="{AMBER_SOFT}" stroke="{SLATE}" stroke-width="1.5"/>',
            f'<ellipse cx="115" cy="70" rx="64" ry="38" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2.2"/>',
            _svg_text(115, 74, f"{n_in} dentro", size=10, fill=GREEN, weight="700"),
            _svg_text(172, 30, f"{n_out} fuera", size=9, fill=AMBER_DARK, weight="700"),
        ]
        return _wrap_svg("".join(parts), w, h, "Pokémon dentro y fuera de la hierba alta")

    if "izquierda" in low and "derecha" in low and "pikachu" in low:
        w, h = 260, 115
        parts = [
            f'<line x1="25" y1="54" x2="235" y2="54" stroke="{GRID_LINE}" stroke-width="2"/>',
            _svg_text(58, 28, "← Izquierda", size=9, fill=BLUE, weight="700"),
            _svg_text(202, 28, "Derecha →", size=9, fill=GREEN, weight="700"),
        ]
        for i in range(7):
            cx = 36 + i * 31
            is_mid = i == 3
            col = AMBER if is_mid else (BLUE if i < 3 else GREEN)
            parts.append(f'<circle cx="{cx}" cy="54" r="{11 if is_mid else 8}" fill="{col}" stroke="#ffffff" stroke-width="1.5"/>')
            if is_mid:
                parts.append(_svg_text(cx, 84, "Pikachu", size=9, fill=INK, weight="700"))
        return _wrap_svg("".join(parts), w, h, "Fila de Pokémon a izquierda y derecha de Pikachu")

    if "arriba" in low and "abajo" in low and "estantería" in low:
        w, h = 220, 130
        parts = [
            f'<rect x="35" y="20" width="150" height="88" fill="#f8fafc" stroke="{SLATE}" stroke-width="2"/>',
            f'<line x1="35" y1="64" x2="185" y2="64" stroke="{SLATE}" stroke-width="2"/>',
            _svg_text(110, 46, "Arriba: 12", size=10, fill=BLUE, weight="700"),
            _svg_text(110, 90, "Abajo: 14", size=10, fill=RED, weight="700"),
        ]
        return _wrap_svg("".join(parts), w, h, "Estantería con balda arriba y abajo")

    return None


def _try_geometry_diagram(
    subcat: str,
    sense: str,
    clean_text: str,
) -> str | None:
    low = clean_text.lower()
    # Excluir falsos positivos no geométricos
    scrubbed = re.sub(r"\bárea\s+silvestre\b", "zona silvestre", low)
    scrubbed = re.sub(r"\b(?:f[óo]rmula\s+del|al)\s+cubo\b", "potencia3", scrubbed)
    scrubbed = re.sub(r"\bcurvas?\s+c[úu]bicas?\b", "curva", scrubbed)
    scrubbed = re.sub(r"\bal\s+cuadrado\b", "potencia2", scrubbed)
    scrubbed = re.sub(r"\b(?:en\s+)?áreas\s+y\s+hectáreas\b", "hectareas", scrubbed)
    scrubbed = re.sub(r"\btorre\s+prisma\b", "torre alta", scrubbed)
    scrubbed = re.sub(r"\besfera\s+aural\b", "ataque aural", scrubbed)
    scrubbed = re.sub(r"\bc[íi]rculo\s+rojo\b", "marca roja", scrubbed)
    scrubbed = re.sub(r"\bdado\s+c[úu]bico\b", "dado", scrubbed)

    is_spatial = "subcategoría 4" in subcat.lower() or "espacial" in sense.lower()
    if "subcategoría 5" in subcat.lower():
        scrubbed = re.sub(r"\bpista\s+circular\b", "pista", scrubbed)
    if not is_spatial:
        # Pirámides numéricas o de patrones no son cuerpos 3D
        scrubbed = re.sub(r"\bpir[áa]mide\b", "monticulo", scrubbed)

    has_geom_kw = bool(
        re.search(
            r"\b(?:"
            r"cuadrad[oa]s?|rect[áa]ngul[oa]s?|rectangular|tri[áa]ngul[oa]s?|triangular|"
            r"c[íi]rculo|circular|circunferencia|corona\s+circular|semic[íi]rculo|"
            r"rombo|romboide|trapecio|pent[áa]gono|hex[áa]gono|pol[íi]gono|"
            r"per[íi]metro|área|cubo|c[úu]bic[oa]s?|prisma|pir[áa]mide|cilindro|cono|esfera|ortoedro|"
            r"baldosas?|tatamis?|valla|coordenadas?|cuadrante|plano\s+cartesiano|simetr[íi]a|ángulos?"
            r")\b",
            scrubbed,
        )
    )
    if not (is_spatial or has_geom_kw):
        return None

    # 1. Cuadrícula cartesiana numérica
    coord_matches = list(
        re.finditer(
            r"([A-Za-z][₀-₉0-9'′]*)?\s*\(\s*(-?\d+(?:[.,]\d+)?)\s*,\s*(-?\d+(?:[.,]\d+)?)\s*\)",
            clean_text,
        )
    )
    if len(coord_matches) >= 1 and re.search(r"\b(?:coordenadas?|cuadrante|plano|eje|radar|sim[ée]trico)\b", scrubbed):
        pts: list[tuple[str, float, float]] = []
        for m in coord_matches:
            lbl = (m.group(1) or "").strip()
            xv = _parse_es_num(m.group(2))
            yv = _parse_es_num(m.group(3))
            if xv is not None and yv is not None:
                pts.append((lbl, xv, yv))
        if pts:
            m_sym = re.search(r"\bx\s*=\s*(-?\d+(?:[.,]\d+)?)", low)
            sym_x = _parse_es_num(m_sym.group(1)) if m_sym else None
            poly = bool(re.search(r"\b(?:tri[áa]ngul|rect[áa]ngul|figura|v[ée]rtices|cuadrado)\b", scrubbed))
            return _render_cartesian_grid_svg(pts, sym_x=sym_x, connect_poly=poly)

    # 2. Tablero alfanumérico (A1..F6 o Fila/Columna)
    if re.search(r"\b(?:casilla|tablero|cuadr[íi]cula)\b", scrubbed) and re.search(r"\b[A-F][1-6]\b|fila\s+[A-D].*columna\s+[1-4]", clean_text, re.I):
        cols = ["A", "B", "C", "D", "E", "F"] if re.search(r"\bF\b|\b6\b", clean_text) else (
            ["A", "B", "C", "D", "E"] if re.search(r"\bE\b|\b5\b", clean_text) else ["A", "B", "C", "D"]
        )
        rows = ["1", "2", "3", "4", "5", "6"][: len(cols)]
        m_fc = re.search(r"fila\s+([A-D])\s*,\s*columna\s+([1-4])", clean_text, re.I)
        if m_fc:
            return _render_board_grid_svg(["1", "2", "3", "4"], ["A", "B", "C", "D"], [(m_fc.group(2), m_fc.group(1).upper(), "P", RED)])
        markers: list[tuple[str, str, str, str]] = []
        for m in re.finditer(r"\b([A-F])([1-6])\b", clean_text):
            c_l, r_l = m.group(1), m.group(2)
            ctx = clean_text[max(0, m.start() - 25) : m.end() + 25].lower()
            if "snorlax" in ctx or "bloquea" in ctx:
                markers.append((c_l, r_l, "X", RED))
            elif "ash" in ctx or "charmander" in ctx or "empieza" in ctx or "sale" in ctx or "está en" in ctx:
                markers.append((c_l, r_l, "A", BLUE))
            else:
                markers.append((c_l, r_l, "•", GREEN))
        return _render_board_grid_svg(cols, rows, markers[:5])

    # 3. Ángulos
    if re.search(r"\bángulos?\b|\d+\s*°", scrubbed) and "sectores" not in scrubbed and "triángulo" not in scrubbed:
        if "norte" in low and ("sentido" in low or "turnos" in low):
            return _render_angle_svg([90.0], compass_mode=True)
        degs = [float(m.group(1).replace(",", ".")) for m in re.finditer(r"(\d+(?:[.,]\d+)?)\s*°", clean_text)]
        degs = [d for d in degs if 0 < d <= 360]
        if degs:
            return _render_angle_svg(degs[:3], compass_mode=False)

    # 4. Cuerpos geométricos 3D
    if "torre" in scrubbed and "cubos" in scrubbed:
        w, h = 210, 145
        parts = [
            f'<rect x="45" y="96" width="120" height="22" fill="{BLUE_FILL}" stroke="{BLUE}" stroke-width="1.8"/>',
            f'<rect x="65" y="72" width="80" height="24" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.8"/>',
            f'<rect x="92" y="48" width="26" height="24" fill="{AMBER_SOFT}" stroke="{AMBER_DARK}" stroke-width="1.8"/>',
            _svg_text(105, 111, "3 × 3", size=9, fill=BLUE, weight="700"),
            _svg_text(105, 88, "2 × 2", size=9, fill=GREEN, weight="700"),
            _svg_text(105, 64, "1", size=9, fill=AMBER_DARK, weight="700"),
        ]
        return _wrap_svg("".join(parts), w, h, "Torre escalonada de cubos")

    if re.search(r"\b(?:prisma|ortoedro|pir[áa]mide|cilindro|cono|esfera|c[úu]bic[oa]s?|cuerpo\s+geom[ée]trico|contenedor(?:es)?\s+c[úu]bicos?|cubo\s+perfecto)\b", scrubbed):
        if "pirámide" in scrubbed:
            return _render_pyramid_svg()
        has_cyl = "cilindro" in scrubbed
        has_sph = "esfera" in scrubbed or "esférica" in scrubbed
        has_cone = "cono" in scrubbed
        has_cube = bool(re.search(r"\bcubo\b|\bc[úu]bic", scrubbed))
        if has_cyl or has_sph or has_cone:
            m_rad = re.search(r"\br\s*=\s*(\d+(?:[.,]\d+)?)\s*(cm|m|dm)", low)
            r_lbl = f"r = {m_rad.group(1)} {m_rad.group(2)}" if m_rad else ""
            return _render_round_solids_svg(has_cyl, has_sph, has_cone, has_cube, radius_lbl=r_lbl)
        if has_cube and "prisma" not in scrubbed:
            dims: list[str] = []
            m_ar = re.search(r"arista\s+mide\s+(\d+(?:[.,]\d+)?)\s*(m|dm|cm)", low)
            m_7 = re.search(r"(\d+)\s+pok[ée]\s*balls?\s+a\s+lo\s+largo", low)
            if m_ar:
                dims.append(f"{m_ar.group(1)} {m_ar.group(2)}")
            elif m_7:
                dims.append(f"{m_7.group(1)}×{m_7.group(1)}×{m_7.group(1)}")
            return _render_prism_svg(dims, is_cube=True)
        dims = []
        for pat in [
            r"(\d+(?:[.,]\d+)?)\s*(cm|m|dm|metros?|cent[íi]metros?)\s+de\s+largo",
            r"(\d+(?:[.,]\d+)?)\s*(cm|m|dm|metros?|cent[íi]metros?)\s+de\s+ancho",
            r"(\d+(?:[.,]\d+)?)\s*(cm|m|dm|metros?|cent[íi]metros?)\s+de\s+(?:alto|altura|profundidad)",
        ]:
            mm = re.search(pat, low)
            if mm:
                u = "cm" if "cm" in mm.group(2) or "cent" in mm.group(2) else ("dm" if "dm" in mm.group(2) else "m")
                dims.append(f"{mm.group(1)} {u}")
        return _render_prism_svg(dims, is_cube=False)

    # 5. Figuras planas 2D
    return _render_2d_shape_svg(low, clean_text)


# ---------------------------------------------------------------------------
# 4. Estadística, Pictogramas, Tablas y Probabilidad
# ---------------------------------------------------------------------------

def _extract_stat_pairs(clean_text: str) -> list[tuple[str, float]]:
    pairs: list[tuple[str, float]] = []
    seen_labels: set[str] = set()

    # 1) Filas de tabla Markdown: | Nombre | 12 |
    for line in clean_text.splitlines():
        m_row = re.match(r"^\|\s*([^|]+?)\s*\|\s*(\d+(?:[.,]\d+)?)\s*\|", line.strip())
        if m_row:
            lbl = m_row.group(1).strip()
            if lbl.lower() in ("pokémon", "día", "tipo", "especie", "fila", "amigo", "entrenador"):
                continue
            val = _parse_es_num(m_row.group(2))
            if val is not None and lbl not in seen_labels:
                seen_labels.add(lbl)
                pairs.append((lbl, val))
    if len(pairs) >= 2:
        return pairs[:5]

    # 2) Patrón "Nombre (N [unidad])"
    for m in re.finditer(r"\b([A-ZÁÉÍÓÚ][A-Za-zÁÉÍÓÚáéíóúñÑ0-9.\- ]{1,18})\s*\(\s*(?:Nivel\s+)?(\d+(?:[.,]\d+)?)\s*(?:ejemplares?|kg|votos?|puntos?|cm)?\s*\)", clean_text):
        lbl = m.group(1).strip()
        if lbl.lower() in ("nivel", "fracción", "base", "tipo"):
            continue
        val = _parse_es_num(m.group(2))
        if val is not None and lbl not in seen_labels:
            seen_labels.add(lbl)
            pairs.append((lbl, val))
    if len(pairs) >= 2:
        return pairs[:5]

    # 3) Patrón "Nombre: N [unidad]"
    for m in re.finditer(r"(?:^|[;\n,\-]\s*|:\s+)([A-ZÁÉÍÓÚ0-9'\"][^:;\n,]{0,20}?)\s*:\s*(\d+(?:[.,]\d+)?)\s*(?:votos?|pok[ée]mon|kg|puntos?|ejemplares?|metros?)?", clean_text, re.M):
        lbl = m.group(1).strip()
        if lbl.lower() in ("clave", "pregunta", "contexto pokémon", "total", "datos") or len(lbl) < 1:
            continue
        val = _parse_es_num(m.group(2))
        if val is not None and lbl not in seen_labels:
            seen_labels.add(lbl)
            pairs.append((lbl, val))
    if len(pairs) >= 2:
        return pairs[:5]

    # 4) Patrón "N prefieren Tipo X" / "barra de X llega a N" / "la de Tipo Agua 1 Pokémon"
    for m in re.finditer(r"\b(\d+(?:[.,]\d+)?)\s+(?:prefieren|son\s+de)\s+(?:tipo\s+)?([A-ZÁÉÍÓÚ][a-záéíóúñ]+)", clean_text, re.I):
        val = _parse_es_num(m.group(1))
        lbl = m.group(2).strip().title()
        if val is not None and lbl not in seen_labels:
            seen_labels.add(lbl)
            pairs.append((lbl, val))
    if len(pairs) >= 2:
        return pairs[:5]

    for m in re.finditer(r"(?:barra\s+de\s+|la\s+de\s+|gimnasio\s+)((?:tipo\s+)?[a-záéíóúñ]+)\s+(?:alcanza\s+una\s+altura\s+de|llega\s+a|tiene|a)\s+(\d+(?:[.,]\d+)?)\s*(?:votos?|pok[ée]mon|cuadraditos?|marcas?)", clean_text, re.I):
        lbl = m.group(1).strip().title()
        val = _parse_es_num(m.group(2))
        if val is not None and lbl not in seen_labels:
            seen_labels.add(lbl)
            pairs.append((lbl, val))
    if len(pairs) >= 2:
        return pairs[:5]

    for m in re.finditer(r"(?:la\s+de\s+)(Tipo\s+[A-ZÁÉÍÓÚa-záéíóúñ]+)\s+(\d+(?:[.,]\d+)?)\s*Pok[ée]mon", clean_text, re.I):
        lbl = m.group(1).strip().title()
        val = _parse_es_num(m.group(2))
        if val is not None and lbl not in seen_labels:
            seen_labels.add(lbl)
            pairs.append((lbl, val))
    if len(pairs) >= 2:
        return pairs[:5]

    # 5) Patrón "Rojos 12, Azules 10..." o "Bulbasaur 70 cm..."
    for m in re.finditer(r"\b([A-ZÁÉÍÓÚ][a-záéíóúñ]+)\s+(\d+(?:[.,]\d+)?)\b", clean_text):
        lbl = m.group(1).strip()
        if lbl.lower() in ("mide", "mida", "mismo", "entre", "nivel", "ronda", "mes", "tipo", "clase", "pokémon"):
            continue
        val = _parse_es_num(m.group(2))
        if val is not None and lbl not in seen_labels:
            seen_labels.add(lbl)
            pairs.append((lbl, val))
    if len(pairs) >= 2:
        return pairs[:5]

    return pairs


def _render_bar_chart_svg(pairs: list[tuple[str, float]], title_text: str = "Gráfico de datos", missing_q: bool = False) -> str:
    w, h = 310, 148
    items = pairs[:5]
    max_v = max((v for _, v in items), default=1.0)
    if max_v <= 0:
        max_v = 1.0

    pad_l, pad_r, pad_t, pad_b = 34.0, 12.0, 22.0, 30.0
    cw = w - pad_l - pad_r
    ch = h - pad_t - pad_b
    n = len(items) + (1 if missing_q else 0)
    slot = cw / max(n, 1)
    bw = min(38.0, slot * 0.62)

    parts = [
        _svg_text(w / 2, 14, title_text, size=9, fill=BLUE, weight="700"),
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + ch}" stroke="{SLATE}" stroke-width="1.5"/>',
        f'<line x1="{pad_l}" y1="{pad_t + ch}" x2="{w - pad_r}" y2="{pad_t + ch}" stroke="{SLATE}" stroke-width="1.5"/>',
    ]

    for frac in (0.5, 1.0):
        gy = pad_t + ch * (1.0 - frac)
        parts.append(f'<line x1="{pad_l}" y1="{gy:.1f}" x2="{w - pad_r}" y2="{gy:.1f}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,2"/>')
        parts.append(_svg_text(pad_l - 4, gy + 3, _fmt_num(max_v * frac), size=7, fill=MUTED, anchor="end"))

    for idx, (lbl, val) in enumerate(items):
        col = PALETTE[idx % len(PALETTE)]
        bh = (val / max_v) * ch
        bx = pad_l + idx * slot + (slot - bw) / 2
        by = pad_t + ch - bh
        parts.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{max(bh, 2.0):.1f}" rx="3" fill="{col}"/>')
        parts.append(_svg_text(bx + bw / 2, by - 4, _fmt_num(val), size=8, fill=col, weight="700"))
        parts.append(_svg_text(bx + bw / 2, pad_t + ch + 14, _short_label(lbl, 11), size=8, fill=INK, weight="700"))

    if missing_q:
        idx = len(items)
        bx = pad_l + idx * slot + (slot - bw) / 2
        by = pad_t + ch * 0.3
        bh = ch * 0.7
        parts.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="3" fill="{AMBER_SOFT}" stroke="{AMBER_DARK}" stroke-width="1.5" stroke-dasharray="3,2"/>')
        parts.append(_svg_text(bx + bw / 2, by + bh / 2 + 4, "?", size=13, fill=RED, weight="800"))
        parts.append(_svg_text(bx + bw / 2, pad_t + ch + 14, f"#{idx + 1}", size=8, fill=RED, weight="700"))

    return _wrap_svg("".join(parts), w, h, title_text)


def _render_double_bar_chart_svg(
    cats: list[tuple[str, float, float]],
    leg1: str,
    leg2: str,
) -> str:
    w, h = 320, 148
    items = cats[:4]
    max_v = max((max(v1, v2) for _, v1, v2 in items), default=1.0)
    if max_v <= 0:
        max_v = 1.0

    pad_l, pad_r, pad_t, pad_b = 30.0, 12.0, 24.0, 30.0
    cw = w - pad_l - pad_r
    ch = h - pad_t - pad_b
    slot = cw / max(len(items), 1)
    bw = min(20.0, slot * 0.34)

    parts = [
        f'<rect x="{pad_l}" y="6" width="9" height="9" rx="2" fill="{BLUE}"/>',
        _svg_text(pad_l + 13, 14, leg1, size=8, fill=BLUE, anchor="start", weight="700"),
        f'<rect x="{pad_l + 90}" y="6" width="9" height="9" rx="2" fill="{RED}"/>',
        _svg_text(pad_l + 103, 14, leg2, size=8, fill=RED, anchor="start", weight="700"),
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + ch}" stroke="{SLATE}" stroke-width="1.5"/>',
        f'<line x1="{pad_l}" y1="{pad_t + ch}" x2="{w - pad_r}" y2="{pad_t + ch}" stroke="{SLATE}" stroke-width="1.5"/>',
    ]

    for idx, (lbl, v1, v2) in enumerate(items):
        cx = pad_l + idx * slot + slot / 2
        h1 = (v1 / max_v) * ch
        h2 = (v2 / max_v) * ch
        x1 = cx - bw - 2
        x2 = cx + 2
        parts.append(f'<rect x="{x1:.1f}" y="{pad_t + ch - h1:.1f}" width="{bw:.1f}" height="{max(h1, 2.0):.1f}" rx="2" fill="{BLUE}"/>')
        parts.append(_svg_text(x1 + bw / 2, pad_t + ch - h1 - 3, _fmt_num(v1), size=7, fill=BLUE, weight="700"))
        parts.append(f'<rect x="{x2:.1f}" y="{pad_t + ch - h2:.1f}" width="{bw:.1f}" height="{max(h2, 2.0):.1f}" rx="2" fill="{RED}"/>')
        parts.append(_svg_text(x2 + bw / 2, pad_t + ch - h2 - 3, _fmt_num(v2), size=7, fill=RED, weight="700"))
        parts.append(_svg_text(cx, pad_t + ch + 14, _short_label(lbl, 11), size=8, fill=INK, weight="700"))

    return _wrap_svg("".join(parts), w, h, "Gráfico de barras dobles comparativo")


def _render_pie_or_spinner_svg(sectors: list[tuple[str, float]], is_spinner: bool = False) -> str:
    w, h = 290, 145
    total = sum(v for _, v in sectors)
    if total <= 0:
        return ""
    cx, cy, r = 74.0, 74.0, 54.0
    parts: list[str] = []

    if len(sectors) == 1:
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PALETTE[0]}" stroke="#ffffff" stroke-width="2"/>')
    else:
        angle = -90.0
        for idx, (lbl, val) in enumerate(sectors[:5]):
            sweep = (val / total) * 360.0
            a1 = math.radians(angle)
            a2 = math.radians(angle + sweep)
            x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
            x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
            large = 1 if sweep > 180.0 else 0
            col = PALETTE[idx % len(PALETTE)]
            parts.append(
                f'<path d="M {cx},{cy} L {x1:.1f},{y1:.1f} A {r},{r} 0 {large} 1 {x2:.1f},{y2:.1f} Z" '
                f'fill="{col}" stroke="#ffffff" stroke-width="1.8"/>'
            )
            angle += sweep

    if is_spinner:
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + 22}" y2="{cy - 22}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{AMBER}" stroke="{INK}" stroke-width="1.5"/>')

    for idx, (lbl, val) in enumerate(sectors[:5]):
        ly = 34 + idx * 24
        col = PALETTE[idx % len(PALETTE)]
        parts.append(f'<rect x="148" y="{ly - 9}" width="11" height="11" rx="2" fill="{col}"/>')
        parts.append(_svg_text(165, ly, f"{_short_label(lbl, 14)}: {_fmt_num(val)}", size=9, fill=INK, anchor="start", weight="700"))

    title = "Ruleta de premios" if is_spinner else "Gráfico de sectores"
    parts.append(_svg_text(cx, 12, title, size=9, fill=BLUE, weight="700"))
    return _wrap_svg("".join(parts), w, h, title)


def _render_urn_svg(bags: list[list[tuple[str, int, str]]], title_text: str = "Urna / Bolsa de extracción") -> str:
    w = 300 if len(bags) == 1 else 320
    h = 148
    parts = [_svg_text(w / 2, 13, title_text, size=9, fill=BLUE, weight="700")]

    if len(bags) == 1:
        items = bags[0]
        parts.append(f'<rect x="24" y="24" width="110" height="110" rx="14" fill="#f8fafc" stroke="{BLUE}" stroke-width="2"/>')
        parts.append(f'<line x1="36" y1="24" x2="122" y2="24" stroke="{RED}" stroke-width="3" stroke-dasharray="5,3"/>')
        total_items = sum(c for _, c, _ in items)
        dots: list[str] = []
        if total_items <= 20:
            for _, cnt, col in items:
                dots.extend([col] * cnt)
        else:
            for _, cnt, col in items:
                n_rep = max(1, round((cnt / max(total_items, 1)) * 14))
                dots.extend([col] * n_rep)
        dots = dots[:18]
        for idx, col in enumerate(dots):
            row = idx // 5
            col_i = idx % 5
            bx = 42 + col_i * 18 + (4 if row % 2 == 1 else 0)
            by = 118 - row * 20
            parts.append(f'<circle cx="{bx}" cy="{by}" r="7" fill="{col}" stroke="#ffffff" stroke-width="1.2"/>')

        for idx, (lbl, cnt, col) in enumerate(items[:5]):
            ly = 44 + idx * 22
            parts.append(f'<circle cx="156" cy="{ly - 3}" r="6" fill="{col}"/>')
            parts.append(_svg_text(168, ly, f"{cnt} × {_short_label(lbl, 16)}", size=9, fill=INK, anchor="start", weight="700"))
    else:
        for b_idx, items in enumerate(bags[:2]):
            ox = 20 + b_idx * 155
            parts.append(f'<rect x="{ox}" y="26" width="128" height="110" rx="10" fill="#f8fafc" stroke="{BLUE}" stroke-width="1.8"/>')
            parts.append(_svg_text(ox + 64, 41, f"Caja / Bolsa {'AB'[b_idx]}", size=9, fill=BLUE, weight="700"))
            total_items = sum(c for _, c, _ in items)
            dots = []
            for _, cnt, col in items:
                n_rep = cnt if total_items <= 12 else max(1, round((cnt / total_items) * 10))
                dots.extend([col] * n_rep)
            for idx, col in enumerate(dots[:12]):
                bx = ox + 22 + (idx % 5) * 20
                by = 76 - (idx // 5) * 18
                parts.append(f'<circle cx="{bx}" cy="{by}" r="6.5" fill="{col}" stroke="#ffffff" stroke-width="1"/>')
            for idx, (lbl, cnt, col) in enumerate(items[:2]):
                ly = 104 + idx * 16
                parts.append(f'<circle cx="{ox + 16}" cy="{ly - 3}" r="4.5" fill="{col}"/>')
                parts.append(_svg_text(ox + 26, ly, f"{cnt} {_short_label(lbl, 13)}", size=8, fill=INK, anchor="start", weight="700"))

    return _wrap_svg("".join(parts), w, h, title_text)


def _render_pictogram_svg(rows: list[tuple[str, float]], key_text: str, mode: str = "circle") -> str:
    w, h = 300, max(120, min(150, 38 + len(rows[:5]) * 22))
    parts = [_svg_text(w / 2, 14, key_text, size=9, fill=BLUE, weight="700")]

    for r_idx, (lbl, count) in enumerate(rows[:5]):
        y = 36 + r_idx * 22
        parts.append(_svg_text(14, y + 3, _short_label(lbl, 12), size=9, fill=INK, anchor="start", weight="700"))
        sx = 104.0
        if mode == "tally":
            full_groups = int(count) // 5
            rem = int(count) % 5
            cx = sx
            for _ in range(min(full_groups, 4)):
                for s in range(4):
                    parts.append(f'<line x1="{cx + s * 5}" y1="{y - 8}" x2="{cx + s * 5}" y2="{y + 5}" stroke="{BLUE}" stroke-width="1.8"/>')
                parts.append(f'<line x1="{cx - 2}" y1="{y + 3}" x2="{cx + 18}" y2="{y - 6}" stroke="{RED}" stroke-width="1.8"/>')
                cx += 26
            for s in range(rem):
                parts.append(f'<line x1="{cx + s * 5}" y1="{y - 8}" x2="{cx + s * 5}" y2="{y + 5}" stroke="{BLUE}" stroke-width="1.8"/>')
        elif mode == "star":
            whole = int(math.floor(count))
            for i in range(min(whole, 9)):
                ix = sx + i * 18
                parts.append(_svg_text(ix, y + 4, "★", size=14, fill=AMBER_DARK, weight="700"))
        else:
            whole = int(math.floor(count))
            has_half = (count - whole) >= 0.4
            for i in range(min(whole, 9)):
                ix = sx + i * 18
                parts.append(f'<circle cx="{ix}" cy="{y - 1}" r="6.5" fill="{RED}" stroke="{INK}" stroke-width="1"/>')
            if has_half:
                ix = sx + min(whole, 9) * 18
                parts.append(
                    f'<path d="M {ix},{y - 7.5} A 6.5,6.5 0 0 0 {ix},{y + 5.5} Z" fill="{AMBER}" stroke="{INK}" stroke-width="1"/>'
                )

    return _wrap_svg("".join(parts), w, h, key_text)


def _render_line_chart_svg(points: list[tuple[str, float]], title_text: str = "Evolución temporal") -> str:
    w, h = 300, 145
    items = points[:6]
    max_v = max((v for _, v in items), default=10.0)
    min_v = 0.0
    pad_l, pad_r, pad_t, pad_b = 34.0, 20.0, 22.0, 28.0
    cw = w - pad_l - pad_r
    ch = h - pad_t - pad_b

    parts = [
        _svg_text(w / 2, 13, title_text, size=9, fill=BLUE, weight="700"),
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + ch}" stroke="{SLATE}" stroke-width="1.5"/>',
        f'<line x1="{pad_l}" y1="{pad_t + ch}" x2="{w - pad_r}" y2="{pad_t + ch}" stroke="{SLATE}" stroke-width="1.5"/>',
    ]

    coords: list[tuple[float, float, str, float]] = []
    for idx, (lbl, val) in enumerate(items):
        px = pad_l + (idx / max(len(items) - 1, 1)) * cw
        py = pad_t + ch - ((val - min_v) / max(max_v - min_v, 1.0)) * ch
        coords.append((px, py, lbl, val))

    poly_pts = " ".join(f"{px:.1f},{py:.1f}" for px, py, _, _ in coords)
    parts.append(f'<polyline points="{poly_pts}" fill="none" stroke="{BLUE}" stroke-width="2.4"/>')
    for px, py, lbl, val in coords:
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{RED}" stroke="#ffffff" stroke-width="1.2"/>')
        parts.append(_svg_text(px, py - 7, _fmt_num(val), size=8, fill=INK, weight="700"))
        parts.append(_svg_text(px, pad_t + ch + 14, _short_label(lbl, 9), size=8, fill=SLATE, weight="700"))

    return _wrap_svg("".join(parts), w, h, title_text)


def _render_tree_svg(branches_l1: list[tuple[str, str]], branches_l2: list[tuple[str, str]], root_label: str) -> str:
    w, h = 310, 145
    rx, ry = 36.0, 72.0
    parts = [
        f'<rect x="6" y="{ry - 13}" width="60" height="26" rx="6" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>',
        _svg_text(rx, ry + 3, _short_label(root_label, 10), size=8, fill=BLUE, weight="700"),
    ]
    n1 = len(branches_l1)
    y1_positions = [36.0, 108.0] if n1 == 2 else [28.0 + i * 44.0 for i in range(n1)]
    for idx1, (lbl1, prob1) in enumerate(branches_l1[:3]):
        y1 = y1_positions[idx1]
        parts.append(f'<line x1="66" y1="{ry}" x2="122" y2="{y1:.1f}" stroke="{SLATE}" stroke-width="1.6"/>')
        if prob1:
            parts.append(_svg_text(94, (ry + y1) / 2 - 4, prob1, size=8, fill=RED, weight="700"))
        parts.append(f'<rect x="122" y="{y1 - 11:.1f}" width="72" height="22" rx="5" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.4"/>')
        parts.append(_svg_text(158, y1 + 3, _short_label(lbl1, 12), size=8, fill=GREEN, weight="700"))

        if idx1 == 0 or n1 <= 2:
            offsets = [-15.0, 15.0] if len(branches_l2) == 2 else [-18.0, 0.0, 18.0]
            for idx2, (lbl2, prob2) in enumerate(branches_l2[:3]):
                y2 = y1 + offsets[idx2]
                parts.append(f'<line x1="194" y1="{y1:.1f}" x2="232" y2="{y2:.1f}" stroke="{SLATE}" stroke-width="1.2"/>')
                parts.append(f'<rect x="232" y="{y2 - 8:.1f}" width="72" height="16" rx="4" fill="{AMBER_SOFT}" stroke="{AMBER_DARK}" stroke-width="1"/>')
                tag2 = f"{_short_label(lbl2, 8)} {prob2}".strip()
                parts.append(_svg_text(268, y2 + 3, tag2, size=7, fill=INK, weight="700"))

    return _wrap_svg("".join(parts), w, h, "Diagrama de árbol de posibilidades")


def _render_die_svg() -> str:
    w, h = 290, 118
    parts = [_svg_text(w / 2, 14, "Dado cúbico equilibrado (6 caras)", size=9, fill=BLUE, weight="700")]
    for face in range(1, 7):
        fx = 16 + (face - 1) * 44
        fy = 30
        is_even = face % 2 == 0
        col = BLUE if is_even else RED
        bg = BLUE_SOFT if is_even else RED_SOFT
        parts.append(f'<rect x="{fx}" y="{fy}" width="36" height="36" rx="6" fill="{bg}" stroke="{col}" stroke-width="1.8"/>')
        parts.append(_svg_text(fx + 18, fy + 23, str(face), size=14, fill=col, weight="800"))
    parts.append(_svg_text(86, 90, "Impares (1, 3, 5)", size=9, fill=RED, weight="700"))
    parts.append(_svg_text(210, 90, "Pares (2, 4, 6)", size=9, fill=BLUE, weight="700"))
    return _wrap_svg("".join(parts), w, h, "Caras del dado numeradas del 1 al 6")


def _render_prob_scale_svg() -> str:
    w, h = 290, 108
    parts = [
        _svg_text(w / 2, 16, "Escala de probabilidad de sucesos", size=9, fill=BLUE, weight="700"),
        f'<line x1="36" y1="56" x2="254" y2="56" stroke="{SLATE}" stroke-width="3"/>',
        f'<circle cx="36" cy="56" r="7" fill="{RED}"/>',
        f'<circle cx="145" cy="56" r="7" fill="{AMBER}"/>',
        f'<circle cx="254" cy="56" r="7" fill="{GREEN}"/>',
        _svg_text(36, 80, "Imposible (0)", size=9, fill=RED, weight="700"),
        _svg_text(145, 80, "Posible", size=9, fill=AMBER_DARK, weight="700"),
        _svg_text(254, 80, "Seguro (1)", size=9, fill=GREEN, weight="700"),
    ]
    return _wrap_svg("".join(parts), w, h, "Escala de probabilidad: Imposible, Posible, Seguro")


def _render_double_entry_table_svg() -> str:
    w, h = 270, 128
    parts = [
        _svg_text(w / 2, 14, "Tabla de doble entrada (50 Pokémon)", size=9, fill=BLUE, weight="700"),
        f'<rect x="18" y="24" width="234" height="88" fill="#ffffff" stroke="{BLUE}" stroke-width="1.5"/>',
        f'<line x1="18" y1="52" x2="252" y2="52" stroke="{BLUE}" stroke-width="1.3"/>',
        f'<line x1="18" y1="82" x2="252" y2="82" stroke="{BLUE}" stroke-width="1"/>',
        f'<line x1="102" y1="24" x2="102" y2="112" stroke="{BLUE}" stroke-width="1.3"/>',
        f'<line x1="176" y1="24" x2="176" y2="112" stroke="{GRID_LINE}" stroke-width="1"/>',
        _svg_text(139, 42, "Sanos (25)", size=8, fill=GREEN, weight="700"),
        _svg_text(214, 42, "Con estado", size=8, fill=RED, weight="700"),
        _svg_text(60, 71, "Machos (30)", size=8, fill=INK, weight="700"),
        _svg_text(139, 71, "?", size=10, fill=BLUE, weight="800"),
        _svg_text(214, 71, "15", size=9, fill=RED, weight="700"),
        _svg_text(60, 100, "Hembras (20)", size=8, fill=INK, weight="700"),
        _svg_text(139, 100, "?", size=10, fill=BLUE, weight="800"),
        _svg_text(214, 100, "10", size=9, fill=RED, weight="700"),
    ]
    return _wrap_svg("".join(parts), w, h, "Tabla de doble entrada médica")


def _try_stats_diagram(
    subcat: str,
    sense: str,
    clean_text: str,
) -> str | None:
    low = clean_text.lower()
    scrubbed = re.sub(r"\bmedia\s+r[áa]pida\b|\bmedio\s+r[áa]pido\b", "curva rapida", low)

    is_stochastic = "subcategoría 6" in subcat.lower() or "estocástico" in sense.lower()
    has_stat_kw = bool(
        re.search(
            r"\b(?:"
            r"gr[áa]fico\s+de\s+barras|gr[áa]fico\s+de\s+l[íi]neas|gr[áa]fico\s+circular|diagrama\s+de\s+sectores|"
            r"pictograma|tabla\s+de\s+recuento|marcas\s+de\s+recuento|tabla\s+de\s+doble\s+entrada|"
            r"diagrama\s+de\s+[áa]rbol|media\s+aritm[ée]tica|media\s+ponderada|moda|probabilidad|urna|ruleta|dado\s+c[úu]bico"
            r")\b",
            scrubbed,
        )
    )
    if not (is_stochastic or has_stat_kw):
        return None

    # 1. Ruleta o diagrama de sectores
    if "ruleta" in low or "diagrama de sectores" in low or "gráfico circular" in low:
        sectors: list[tuple[str, float]] = []
        for m in re.finditer(r"(\d+)\s+(?:sectores?|partes?)\s+(?:son\s+de\s+color\s+[a-záéíóú]+\s*\(premio:\s*|tienen\s+(?:el\s+dibujo\s+de\s+una?\s+|premio\s+de\s+)|conceden\s+(?:una?\s+)?)([A-ZÁÉÍÓÚa-záéíóúñ\s]+?)(?:\)|\s+y\b|,|\.)", clean_text):
            lbl = m.group(2).strip()
            lbl = re.sub(r"^(?:M[áa]quina\s+T[ée]cnica\s*\()?([A-Za-zÁÉÍÓÚáéíóú ]+)\)?$", r"\1", lbl)
            sectors.append((lbl, float(m.group(1))))
        if not sectors:
            sectors = _extract_stat_pairs(clean_text)
        if sectors:
            return _render_pie_or_spinner_svg(sectors, is_spinner=("ruleta" in low))

    # 2. Dado cúbico
    if re.search(r"\bdado(?:\s+c[úu]bico)?\b", low) and "dado que" not in low:
        return _render_die_svg()

    # 3. Tabla de doble entrada
    if "tabla de doble entrada" in low and "machos" in low and "hembras" in low:
        return _render_double_entry_table_svg()

    # 4. Diagrama de árbol o probabilidad compuesta
    if "diagrama de árbol" in low or "triataque" in low or "encuentros consecutivos" in low or "turnos sucesivos" in low:
        if "triataque" in low:
            return _render_tree_svg(
                [("Efecto", "1/5"), ("Sin efecto", "4/5")],
                [("Quema", "1/3"), ("Congela", "1/3"), ("Paraliza", "1/3")],
                "Triataque",
            )
        if "starly" in low and "bidoof" in low:
            return _render_tree_svg(
                [("Starly", "50%"), ("Bidoof", "35%"), ("Kricketot", "15%")],
                [("Starly", "1/2"), ("Otro", "1/2")],
                "Encuentro 1",
            )
        if "roca afilada" in low:
            return _render_tree_svg(
                [("T1 Acierto", "4/5"), ("T1 Fallo", "1/5")],
                [("T2 Acierto", "4/5"), ("T2 Fallo", "1/5")],
                "3 Turnos",
            )
        probs = re.findall(r"(?:de\s+(?:que\s+(?:sea|herede)\s+)?)?([A-Za-zÁÉÍÓÚáéíóúñ ]{3,20}?)\s+(?:es\s+de|es)\s+(\d+/\d+)", low)
        if len(probs) >= 2:
            l1 = [(p[0].strip().title(), p[1]) for p in probs[:2]]
            l2 = [(p[0].strip().title(), p[1]) for p in probs[2:4]] or [("Opción A", "?"), ("Opción B", "?")]
            return _render_tree_svg(l1, l2, "Inicio")
        if "bulbasaur" in low and "charmander" in low:
            return _render_tree_svg(
                [("Bulbasaur", ""), ("Charmander", ""), ("Squirtle", "")],
                [("Poké Ball", ""), ("Super Ball", ""), ("Otras", "")],
                "Inicial",
            )

    # 5. Gráfico de líneas
    if "gráfico de líneas" in low:
        pts = _extract_stat_pairs(clean_text)
        if len(pts) >= 3:
            return _render_line_chart_svg(pts, "Gráfico de líneas")

    # 6. Pictograma y marcas de recuento
    if "pictograma" in low or "marcas de recuento" in low or "tabla de recuento" in low or "rayita" in low or "IIII" in clean_text or "||||" in clean_text:
        # Tabla Markdown con I+ o \| \| \|
        tally_rows: list[tuple[str, float]] = []
        for line in clean_text.splitlines():
            m_i = re.match(r"^\|\s*([A-Za-zÁÉÍÓÚáéíóúñ]+)\s*\|\s*(I+)\s*\|", line.strip())
            if m_i:
                tally_rows.append((m_i.group(1), float(len(m_i.group(2)))))
                continue
            m_p = re.match(r"^\|\s*([A-Za-zÁÉÍÓÚáéíóúñ]+)\s*\|\s*((?:\\?\|\s*)+)\|", line.strip())
            if m_p:
                cnt = m_p.group(2).count("|")
                if cnt > 0:
                    tally_rows.append((m_p.group(1), float(cnt)))
        if tally_rows:
            return _render_pictogram_svg(tally_rows, "Tabla de recuento", mode="tally")

        # Marcas inline |||| |||| ||
        tally_inline: list[tuple[str, float]] = []
        for m in re.finditer(r"([A-ZÁÉÍÓÚ][a-záéíóúñ]+)(?:\s*\([^)]+\))?\s*:\s*([| ]+)\s*[;.]", clean_text):
            cnt = m.group(2).count("|")
            if cnt > 0:
                tally_inline.append((m.group(1), float(cnt)))
        if tally_inline:
            return _render_pictogram_svg(tally_inline, "Recuento de votos", mode="tally")

        # Tabla Markdown con símbolos ● / ◐ / 🧺 / ★
        sym_rows: list[tuple[str, float]] = []
        is_star = False
        for m in re.finditer(r"\|\s*([A-ZÁÉÍÓÚ][a-záéíóúñ]+)\s*\|\s*([^|\n]+?)\s*\|", clean_text):
            lbl, cell = m.group(1), m.group(2)
            if lbl.lower() in ("pokémon", "día", "entrenador"):
                continue
            stars = cell.count("★")
            if stars > 0:
                is_star = True
                sym_rows.append((lbl, float(stars)))
                continue
            full = cell.count("●") + cell.count("🧺")
            half = 0.5 if ("◐" in cell or "media" in cell.lower()) else 0.0
            if "media" in cell.lower() and "🧺" in cell:
                full = max(0, cell.count("🧺") - 1)
            if full + half > 0:
                sym_rows.append((lbl, full + half))
        if sym_rows:
            m_key = re.search(r"(?:cada|vale|representa|clave:)[^.\n]{0,55}?(\d+)\s+(?:bayas?|pok[ée]mon|capturas?)", low)
            sym_ch = "★" if is_star else "●"
            key_txt = f"Pictograma ({sym_ch} = {m_key.group(1)})" if m_key else "Pictograma"
            return _render_pictogram_svg(sym_rows, key_txt, mode=("star" if is_star else "circle"))

        # Pictograma inline: "Starly: ● ● ◐. Bidoof: ● ● ● ●."
        inline_syms: list[tuple[str, float]] = []
        for m in re.finditer(r"([A-ZÁÉÍÓÚ][a-záéíóúñ]+)\s*:\s*([●◐★ ]+)", clean_text):
            cell = m.group(2)
            full = cell.count("●") + cell.count("★")
            half = 0.5 * cell.count("◐")
            if full + half > 0:
                inline_syms.append((m.group(1), full + half))
        if len(inline_syms) >= 2:
            m_key = re.search(r"●\s*=\s*(\d+)", clean_text)
            key_txt = f"Pictograma (● = {m_key.group(1)})" if m_key else "Pictograma"
            return _render_pictogram_svg(inline_syms, key_txt, mode="circle")

        txt_rows: list[tuple[str, float]] = []
        for m in re.finditer(r"([A-ZÁÉÍÓÚ][A-Za-zÁÉÍÓÚáéíóúñ ]{2,20}?)\s*:\s*(\d+)\s+(?:dibujos?|estrellas?)(\s+y\s+medi[oa])?", clean_text):
            cnt = float(m.group(2)) + (0.5 if m.group(3) else 0.0)
            txt_rows.append((m.group(1).strip(), cnt))
        if not txt_rows:
            m_est = re.search(r"(\d+)\s+estrellas?\s+doradas?", low)
            if m_est:
                txt_rows.append(("Misty", float(m_est.group(1))))
        if txt_rows:
            return _render_pictogram_svg(txt_rows, "Pictograma de símbolos", mode="circle")

    # 7. Gráficos de barras dobles (bloques █, Día/Noche, Rojo/Azul, Mañana/Tarde)
    if "█" in clean_text and "barras dobles" in low:
        gym_rows: list[tuple[str, float, float]] = []
        for m in re.finditer(r"Gimnasio\s+de\s+([A-ZÁÉÍÓÚ][a-záéíóúñ]+)\s*\([^)]+\)\s*:\s*victorias[^█]*?(█+)\s*,\s*derrotas\s*(█+)", clean_text):
            gym_rows.append((m.group(1), float(len(m.group(2))), float(len(m.group(3)))))
        if gym_rows:
            return _render_double_bar_chart_svg(gym_rows, "Victorias (█=6)", "Derrotas (█=6)")

    if "barras dobles" in low or ("por la mañana" in low and "por la tarde" in low):
        dbl_rows: list[tuple[str, float, float]] = []
        for m in re.finditer(r"-\s*([A-ZÁÉÍÓÚ][A-Za-zÁÉÍÓÚáéíóúñ ()]{1,22}?)\s*:\s*(?:[A-Za-z]+\s+)?(\d+)\s*(?:avistamientos\s+de\s+d[íi]a|puntos|de\s+d[íi]a)\s*/\s*(?:[A-Za-z]+\s+)?(\d+)", clean_text):
            dbl_rows.append((m.group(1).strip(), float(m.group(2)), float(m.group(3))))
        if dbl_rows:
            leg1, leg2 = ("Día", "Noche") if "noche" in low else ("Equipo Rojo", "Equipo Azul")
            return _render_double_bar_chart_svg(dbl_rows, leg1, leg2)

        m_ld = re.findall(r"([A-ZÁÉÍÓÚ][a-záéíóúñ]+)\s+captur[óo]\s+(\d+)\s+por\s+la\s+mañana\s+y\s+(\d+)\s+por\s+la\s+tarde", clean_text)
        if m_ld:
            dbl_rows = [(x[0], float(x[1]), float(x[2])) for x in m_ld]
            return _render_double_bar_chart_svg(dbl_rows, "Mañana", "Tarde")

    # 8. Bolsas / Cajas / Urnas / Mochilas de probabilidad
    if re.search(r"\b(?:bolsa|caja|ba[úu]l|urna|caparaz[óo]n|bolsillo|mochila|compartimento)\b", low) and re.search(r"\b(?:sin\s+mirar|al\s+azar|extraer|sacar|ojos\s+cerrados|seguro,\s*posible)\b", low):
        color_cycle = [RED, BLUE_MID, AMBER, PURPLE, GREEN]
        segments = re.split(r"\.\s+(?=En\s+otra\s+caja|La\s+bolsa\s+B)", clean_text)
        bags: list[list[tuple[str, int, str]]] = []
        for seg in segments[:2]:
            items: list[tuple[str, int, str]] = []
            for idx, m in enumerate(re.finditer(r"(\d+)\s+((?:Pok[ée]|Super|Ultra|Master|Safari)\s*Balls?(?:\s+rojas?|\s+azules?|\s+cl[áa]sicas?|\s+est[áa]ndar)?|Bayas?\s+[A-ZÁÉÍÓÚ][a-záéíóú]+|bayas?\s+[A-ZÁÉÍÓÚ][a-záéíóú]+|Pociones?|Ant[íi]dotos?)", seg, re.I)):
                cnt = int(m.group(1))
                lbl = m.group(2).strip()
                col = BLUE_MID if "super" in lbl.lower() else (AMBER if "ultra" in lbl.lower() else (PURPLE if "master" in lbl.lower() else color_cycle[idx % len(color_cycle)]))
                items.append((lbl, cnt, col))
            if items:
                bags.append(items)
        if bags:
            return _render_urn_svg(bags, "Contenido para extracción al azar")

    # 9. Media ponderada / Frecuencia esperada / Precisión observada
    if "media ponderada" in low:
        return _render_bar_chart_svg([("Teoría (40%)", 8.0), ("Práctica (60%)", 9.0)], "Notas y pesos porcentuales")
    if "onda trueno" in low and "acierta" in low:
        return _render_bar_chart_svg([("Teórica", 90.0), ("Aciertos (42/50)", 84.0)], "Precisión teórica (%)")
    if "golpes críticos" in low and "120" in low:
        return _render_prob_scale_svg()
    if "variocolor" in low and "512" in low:
        return _render_prob_scale_svg()

    # 10. Datos numéricos simples / barras
    pairs = _extract_stat_pairs(clean_text)
    if len(pairs) >= 2:
        return _render_bar_chart_svg(pairs, "Datos del problema")

    # Secuencias de números para media / moda / rango (ej. "85, 92, 78 y 105")
    if re.search(r"\b(?:media|moda|rango|mediana)\b", scrubbed):
        m_seq = re.search(r"(?:son|hecho|niveles|datos|:)\s*((?:\d+(?:[.,]\d+)?(?:\s*(?:puntos|kg))?\s*,\s*){2,}\d+(?:[.,]\d+)?(?:\s+y\s+\d+(?:[.,]\d+)?)?)", clean_text)
        if m_seq:
            raw_nums = re.findall(r"\d+(?:[.,]\d+)?", m_seq.group(1))
            seq_pairs = [(f"#{i + 1}", _parse_es_num(v) or 0.0) for i, v in enumerate(raw_nums[:5])]
            if len(seq_pairs) >= 3:
                miss_q = "falta" in low or "quinta ronda" in low or "sexto pokémon" in low
                return _render_bar_chart_svg(seq_pairs, "Valores registrados", missing_q=miss_q)

    # 11. Escala cualitativa de probabilidad
    if re.search(r"\bseguro,\s*posible\s+(?:o|e)\s+imposible\b", low):
        return _render_prob_scale_svg()

    return None


# ---------------------------------------------------------------------------
# Punto de entrada público
# ---------------------------------------------------------------------------

def generate_problem_svg(
    prob_num: int,
    kind: str,
    title: str,
    subcat: str,
    sense: str,
    story_text: str,
    question_text: str,
    grade: int,
) -> str:
    """
    Genera un fragmento HTML auto-contenido con un diagrama SVG didáctico para
    un problema matemático (1º–6º Primaria), o "" si el problema no requiere diagrama.
    """
    _ = (prob_num, kind, grade)
    title_s = title or ""
    subcat_s = subcat or ""
    sense_s = sense or ""
    story_s = story_text or ""
    question_s = question_text or ""

    combined_raw = "\n".join(part for part in (title_s, story_s, question_s) if part).strip()
    if not combined_raw:
        return ""
    clean_text = _clean_md(combined_raw)
    low = clean_text.lower()

    # 1. Reloj analógico
    clock_info = _parse_clock_time(clean_text)
    if clock_info is not None:
        hour, minute, label = clock_info
        return _render_clock_svg(hour, minute, label)

    # 2. Recta numérica / Termómetro / Altitud
    scale_svg = _try_scale_or_numberline_diagram(subcat_s, sense_s, clean_text)
    if scale_svg:
        return scale_svg

    # 3. Priorizar Estadística / Probabilidad cuando es explícitamente estocástico o gráfico estadístico
    if (
        "subcategoría 6" in subcat_s.lower()
        or "estocástico" in sense_s.lower()
        or "diagrama de sectores" in low
        or "gráfico circular" in low
    ):
        stats_svg = _try_stats_diagram(subcat_s, sense_s, clean_text)
        if stats_svg:
            return stats_svg

    # 4. Geometría 2D/3D, Coordenadas, Ángulos, Simetría
    geom_svg = _try_geometry_diagram(subcat_s, sense_s, clean_text)
    if geom_svg:
        return geom_svg

    # 5. Estadística / Probabilidad fuera de Subcategoría 6
    stats_svg = _try_stats_diagram(subcat_s, sense_s, clean_text)
    if stats_svg:
        return stats_svg

    return ""
