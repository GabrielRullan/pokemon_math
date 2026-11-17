#!/usr/bin/env python3
"""
Genera la versión HTML lista para imprimir de todos los documentos Markdown
del proyecto Matemáticas Primaria con Pokémon (LOMLOE 2º–6º Primaria),
con estética de ficha infantil, imágenes locales de Pokémon, cuadrícula de
operaciones y «Ficha del Profesor Oak» curricular al final.
"""

from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from pathlib import Path
import markdown

ROOT_DIR = Path(__file__).resolve().parent
OUT_DIR = ROOT_DIR / "html"
DATA_DIR = ROOT_DIR / "data"
IMG_DIR = OUT_DIR / "assets" / "images"

DOCS = [
    {
        "src": "README.md",
        "out": "README.html",
        "title": "Guía Maestra del Proyecto — Matemáticas Pokémon (LOMLOE)",
        "badge": "Índice y Guía",
        "desc": "Visión general del proyecto, mapeo curricular LOMLOE (2º a 6º de Primaria) y estructura de materiales.",
        "is_problems": False,
    },
    {
        "src": "problemas_2_primaria.md",
        "out": "problemas_2_primaria.html",
        "title": "Cuadernillo de Entrenador — 2º de Primaria",
        "badge": "2º Primaria (7–8 años)",
        "desc": "120 ejercicios (100 + 20 Retos Especiales): números hasta 999, sumas/restas, formas 2D, horas, euros y EXP.",
        "is_problems": True,
    },
    {
        "src": "problemas_3_primaria.md",
        "out": "problemas_3_primaria.html",
        "title": "Cuadernillo de Entrenador — 3º de Primaria",
        "badge": "3º Primaria (8–9 años)",
        "desc": "120 ejercicios (100 + 20 Retos Especiales): números hasta 9.999, tablas, división, medidas, gráficos y EXP.",
        "is_problems": True,
    },
    {
        "src": "problemas_4_primaria.md",
        "out": "problemas_4_primaria.html",
        "title": "Cuadernillo de Entrenador — 4º de Primaria",
        "badge": "4º Primaria (9–10 años)",
        "desc": "120 ejercicios (100 + 20 Retos Especiales): multiplicación 2 cifras, división, fracciones, decimales, áreas y EXP.",
        "is_problems": True,
    },
    {
        "src": "problemas_5_primaria.md",
        "out": "problemas_5_primaria.html",
        "title": "Cuadernillo de Entrenador — 5º de Primaria",
        "badge": "5º Primaria (10–11 años)",
        "desc": "120 ejercicios (100 + 20 Retos Especiales): fracciones, decimales, porcentajes, coordenadas, áreas y EXP.",
        "is_problems": True,
    },
    {
        "src": "problemas_6_primaria.md",
        "out": "problemas_6_primaria.html",
        "title": "Cuadernillo de Entrenador — 6º de Primaria",
        "badge": "6º Primaria (11–12 años)",
        "desc": "120 ejercicios (100 + 20 Retos Especiales): porcentajes, proporcionalidad, enteros, volúmenes, probabilidad y EXP.",
        "is_problems": True,
    },
    {
        "src": "referencia_tabla_tipos.md",
        "out": "referencia_tabla_tipos.html",
        "title": "Tabla de Tipos Pokémon y Multiplicadores de Daño",
        "badge": "Referencia",
        "desc": "Matriz completa 18×18, multiplicadores (x0, x0.25, x0.5, x1, x1.5 STAB, x2, x4) y reglas de doble tipo.",
        "is_problems": False,
    },
    {
        "src": "referencia_ps_evoluciones.md",
        "out": "referencia_ps_evoluciones.html",
        "title": "Puntos de Salud (PS) y Escalado en Evoluciones",
        "badge": "Referencia",
        "desc": "Fórmula oficial de PS, caso Shedinja (PS = 1), 18 líneas evolutivas y modelos adaptados a Primaria.",
        "is_problems": False,
    },
    {
        "src": "guia_recursos_activos.md",
        "out": "guia_recursos_activos.html",
        "title": "Guía de Fuentes de Imágenes, Sprites y Datos Pokémon",
        "badge": "Recursos",
        "desc": "Endpoints verificados de PokeAPI v2, sprites en GitHub CDN, Showdown, esquemas y diccionario ES–EN.",
        "is_problems": False,
    },
]

# Compañeros por defecto cuando el enunciado no nombra una especie concreta
COMPANION_ROTATION = [
    (25, "Pikachu"),
    (133, "Eevee"),
    (1, "Bulbasaur"),
    (4, "Charmander"),
    (7, "Squirtle"),
    (39, "Jigglypuff"),
    (143, "Snorlax"),
    (448, "Lucario"),
    (393, "Piplup"),
    (54, "Psyduck"),
]

CHARACTER_COMPANIONS = [
    ("enfermera joy", (113, "Chansey")),
    ("centro pokémon", (113, "Chansey")),
    ("brock", (74, "Geodude")),
    ("misty", (120, "Staryu")),
    ("team rocket", (52, "Meowth")),
    ("jessie", (52, "Meowth")),
    ("james", (52, "Meowth")),
    ("profesor oak", (1, "Bulbasaur")),
    ("huevo", (175, "Togepi")),
    ("fantasma", (94, "Gengar")),
    ("lavanda", (94, "Gengar")),
    ("gary", (133, "Eevee")),
]

SHARED_CSS = r"""
:root {
  --pk-red: #e3350d;
  --pk-red-dark: #b91c1c;
  --pk-red-soft: #fef2f2;
  --pk-yellow: #ffcb05;
  --pk-blue: #1e3a8a;
  --pk-blue-mid: #1d4ed8;
  --pk-blue-soft: #eff6ff;
  --pk-green: #047857;
  --pk-green-soft: #ecfdf5;
  --pk-ink: #1e293b;
  --pk-muted: #475569;
  --pk-border: #cbd5e1;
  --pk-bg: #f1f5f9;
  --pk-surface: #ffffff;
}

*, *::before, *::after {
  box-sizing: border-box;
}

html {
  font-size: 16px;
  scroll-behavior: smooth;
}

body {
  margin: 0;
  font-family: "Trebuchet MS", "Segoe UI", system-ui, -apple-system, sans-serif;
  color: var(--pk-ink);
  background: var(--pk-bg);
  line-height: 1.55;
}

/* Barra superior de herramientas (oculta al imprimir) */
.print-toolbar {
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.7rem 1.25rem;
  background: #0f172a;
  color: #f8fafc;
  border-bottom: 3px solid var(--pk-yellow);
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.18);
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.toolbar-title {
  font-weight: 700;
  font-size: 0.95rem;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.45rem 0.85rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  font-size: 0.85rem;
  font-weight: 700;
  text-decoration: none;
  cursor: pointer;
  transition: background 0.15s ease;
}

.btn:hover {
  background: rgba(255, 255, 255, 0.22);
}

.btn-primary {
  background: var(--pk-red);
  border-color: var(--pk-red);
}

.btn-primary:hover {
  background: var(--pk-red-dark);
}

.btn-toggle.active {
  background: var(--pk-blue-mid);
  border-color: #93c5fd;
}

/* Contenedor principal tipo ficha A4 */
.page-container {
  max-width: 960px;
  margin: 1.5rem auto 3rem;
  padding: 2rem 2.25rem;
  background: var(--pk-surface);
  border: 1px solid var(--pk-border);
  border-radius: 14px;
  box-shadow: 0 6px 24px rgba(15, 23, 42, 0.07);
}

/* Cabecera infantil de entrenador */
.header-box {
  background: linear-gradient(135deg, #ffcb05 0%, #f97316 45%, #e3350d 100%);
  border-radius: 14px;
  padding: 1.15rem 1.4rem;
  color: #ffffff;
  margin-bottom: 1.25rem;
  box-shadow: 0 4px 12px rgba(227, 53, 13, 0.22);
}

.header-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.header-title-row h1 {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 1.55rem;
  color: #ffffff;
  text-shadow: 1px 2px 3px rgba(0, 0, 0, 0.35);
}

.badge-grade {
  background: #ffffff;
  color: var(--pk-red);
  padding: 0.35rem 0.95rem;
  border-radius: 999px;
  font-weight: 800;
  font-size: 0.88rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

.trainer-ranks-bar {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.5rem;
  background: rgba(15, 23, 42, 0.25);
  border-radius: 8px;
  padding: 0.4rem 0.75rem;
  margin-top: 0.7rem;
  font-size: 0.78rem;
  font-weight: 700;
}

.student-fields {
  display: grid;
  grid-template-columns: 2fr 1fr 1.2fr;
  gap: 0.75rem;
  background: rgba(255, 255, 255, 0.96);
  color: #0f172a;
  padding: 0.65rem 0.9rem;
  border-radius: 10px;
  margin-top: 0.75rem;
  font-size: 0.88rem;
  font-weight: 700;
}

.student-field-line {
  border-bottom: 2px dotted #94a3b8;
  padding-bottom: 2px;
}

.kid-welcome {
  background: #fef9c3;
  border: 2px solid #f59e0b;
  border-radius: 10px;
  padding: 0.7rem 1rem;
  margin-bottom: 1.25rem;
  font-size: 0.94rem;
  color: #78350f;
}

h1 {
  margin-top: 0;
  padding-bottom: 0.55rem;
  font-size: 1.7rem;
  line-height: 1.25;
  color: #0f172a;
  border-bottom: 3px solid var(--pk-red);
}

h2 {
  margin-top: 1.75rem;
  margin-bottom: 0.85rem;
  padding: 0.45rem 0.8rem;
  font-size: 1.25rem;
  color: var(--pk-blue);
  background: var(--pk-blue-soft);
  border-left: 5px solid var(--pk-blue-mid);
  border-radius: 0 8px 8px 0;
}

h2.special-challenges-title {
  color: #9a3412;
  background: #ffedd5;
  border-left-color: #ea580c;
}

h3 {
  margin-top: 1.1rem;
  margin-bottom: 0.45rem;
  font-size: 1.06rem;
  color: #0f172a;
}

p, ul, ol {
  margin-top: 0.4rem;
  margin-bottom: 0.6rem;
}

li {
  margin-bottom: 0.25rem;
}

hr {
  border: 0;
  border-top: 1px solid var(--pk-border);
  margin: 1.25rem 0;
}

code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 0.88em;
  background: #f1f5f9;
  padding: 0.12em 0.35em;
  border-radius: 4px;
}

pre {
  background: #0f172a;
  color: #f8fafc;
  padding: 0.9rem 1rem;
  border-radius: 8px;
  overflow-x: auto;
  font-size: 0.85rem;
}

pre code {
  background: transparent;
  padding: 0;
  color: inherit;
}

blockquote {
  margin: 1rem 0;
  padding: 0.65rem 1rem;
  background: var(--pk-red-soft);
  border-left: 4px solid var(--pk-red);
  border-radius: 0 6px 6px 0;
}

/* Tarjeta de problema infantil con imagen y cuadrícula */
.problem-card {
  border: 2px solid #cbd5e1;
  border-radius: 12px;
  padding: 0.85rem 1rem;
  margin-bottom: 1rem;
  background: #ffffff;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
  break-inside: avoid;
  page-break-inside: avoid;
}

.problem-card.is-reto {
  border-color: #fdba74;
  background: #fffaf5;
}

.problem-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  padding-bottom: 0.45rem;
  margin-bottom: 0.6rem;
  border-bottom: 2px dashed #e2e8f0;
}

.problem-card-header h3 {
  margin: 0;
  font-size: 1.05rem;
  color: var(--pk-blue);
}

.problem-card.is-reto .problem-card-header h3 {
  color: #c2410c;
}

.poke-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.15rem 0.55rem;
  border-radius: 999px;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  font-size: 0.75rem;
  font-weight: 700;
  color: #334155;
  white-space: nowrap;
}

.problem-body-grid {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.problem-sprites {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem;
  background: linear-gradient(180deg, #f8fafc 0%, #eff6ff 100%);
  border: 1px solid #dbeafe;
  border-radius: 10px;
}

.poke-sprite {
  width: 82px;
  height: 82px;
  object-fit: contain;
  display: block;
}

.poke-sprite-secondary {
  width: 56px;
  height: 56px;
}

.problem-text {
  flex: 1 1 auto;
  min-width: 0;
  font-size: 0.96rem;
}

.problem-question {
  margin-top: 0.5rem;
  padding: 0.45rem 0.65rem;
  background: #eff6ff;
  border-left: 4px solid var(--pk-blue-mid);
  border-radius: 0 6px 6px 0;
  font-weight: 600;
  color: #0f172a;
}

.workspace-box {
  margin-top: 0.65rem;
  height: 92px;
  border: 1.5px dashed #94a3b8;
  border-radius: 8px;
  background-color: #ffffff;
  background-image:
    linear-gradient(to right, #e2e8f0 1px, transparent 1px),
    linear-gradient(to bottom, #e2e8f0 1px, transparent 1px);
  background-size: 18px 18px;
  position: relative;
}

.workspace-label {
  position: absolute;
  top: 4px;
  left: 8px;
  font-size: 0.72rem;
  font-weight: 700;
  color: #64748b;
  background: rgba(255, 255, 255, 0.85);
  padding: 0 4px;
  border-radius: 3px;
}

body.hide-workspaces .workspace-box {
  display: none !important;
}

/* Solucionario */
.solution-card {
  border: 1px solid var(--pk-border);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  margin-bottom: 0.7rem;
  background: #f8fafc;
  break-inside: avoid;
  page-break-inside: avoid;
}

.solution-card h3 {
  margin-top: 0;
  margin-bottom: 0.4rem;
  padding-bottom: 0.25rem;
  border-bottom: 1px dashed var(--pk-border);
  color: var(--pk-green);
}

/* Ficha del Profesor Oak (para docentes y familias al final) */
.prof-oak-dossier {
  margin-top: 2rem;
  padding: 1.4rem 1.5rem;
  background: var(--pk-green-soft);
  border: 2px solid #10b981;
  border-radius: 12px;
  break-before: page;
  page-break-before: always;
}

.prof-oak-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  border-bottom: 2px solid #6ee7b7;
  padding-bottom: 0.65rem;
  margin-bottom: 1rem;
}

.prof-oak-header h2 {
  margin: 0;
  padding: 0;
  border: 0;
  background: transparent;
  color: #065f46;
  font-size: 1.35rem;
}

.prof-oak-badge {
  background: #065f46;
  color: #ffffff;
  padding: 0.25rem 0.7rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 700;
}

body.hide-solutions .solutions-section,
body.hide-solutions .prof-oak-dossier {
  display: none !important;
}

/* Tablas responsivas y accesibles */
.table-wrapper {
  overflow-x: auto;
  max-inline-size: 100%;
  margin: 1rem 0;
  border: 1px solid var(--pk-border);
  border-radius: 8px;
  background: #ffffff;
  container-type: inline-size;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 0.9rem;
}

thead th {
  position: sticky;
  inset-block-start: 0;
  z-index: 2;
  background: #1e293b;
  color: #ffffff;
  font-weight: 600;
  text-align: left;
  padding: 0.5rem 0.6rem;
  border-bottom: 2px solid #0f172a;
}

tbody td, tbody th {
  padding: 0.42rem 0.6rem;
  border-bottom: 1px solid var(--pk-border);
  border-right: 1px solid #e2e8f0;
  vertical-align: top;
}

tbody tr:nth-child(even) {
  background: #f8fafc;
}

tbody td:first-child, tbody th:first-child {
  font-weight: 600;
}

table.type-matrix {
  font-size: 0.78rem;
  text-align: center;
}

table.type-matrix th, table.type-matrix td {
  padding: 0.28rem 0.32rem;
  text-align: center;
}

table.type-matrix tbody td:first-child {
  position: sticky;
  inset-inline-start: 0;
  z-index: 1;
  background: #f1f5f9;
  text-align: left;
  white-space: nowrap;
}

/* Tarjetas del índice */
.grid-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
  gap: 1rem;
  margin: 1.25rem 0;
}

.doc-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border: 1px solid var(--pk-border);
  border-radius: 10px;
  padding: 1.1rem;
  background: #ffffff;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
  break-inside: avoid;
}

.doc-badge {
  display: inline-block;
  align-self: flex-start;
  padding: 0.18rem 0.55rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  background: var(--pk-blue-soft);
  color: var(--pk-blue);
  margin-bottom: 0.5rem;
}

.doc-card h3 {
  margin: 0 0 0.45rem;
  font-size: 1.05rem;
}

.doc-card p {
  font-size: 0.88rem;
  color: var(--pk-muted);
  margin-bottom: 0.9rem;
}

.doc-card-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  border: 1px solid var(--pk-blue-mid);
  color: var(--pk-blue-mid);
  font-size: 0.84rem;
  font-weight: 600;
  text-decoration: none;
}

.btn-outline:hover {
  background: var(--pk-blue-soft);
}

/* Reglas de impresión A4 */
@page {
  size: A4;
  margin: 12mm 12mm;
}

@media print {
  * {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  body {
    background: #ffffff;
    font-size: 10pt;
    line-height: 1.38;
  }

  .no-print {
    display: none !important;
  }

  .page-container {
    max-width: none;
    margin: 0;
    padding: 0;
    border: 0;
    border-radius: 0;
    box-shadow: none;
  }

  .header-box {
    padding: 0.8rem 1rem;
    margin-bottom: 0.75rem;
  }

  .problem-card {
    padding: 0.55rem 0.75rem;
    margin-bottom: 0.65rem;
    box-shadow: none;
  }

  .poke-sprite {
    width: 64px;
    height: 64px;
  }

  .poke-sprite-secondary {
    width: 46px;
    height: 46px;
  }

  .workspace-box {
    height: 70px;
  }

  h2 {
    font-size: 12pt;
    break-after: avoid;
    page-break-after: avoid;
  }

  h3 {
    font-size: 10pt;
    break-after: avoid;
    page-break-after: avoid;
  }

  .solutions-section {
    break-before: page;
    page-break-before: always;
  }

  .table-wrapper {
    overflow: visible !important;
    border: 0;
  }

  thead {
    display: table-header-group;
  }

  thead th, tbody td:first-child {
    position: static !important;
  }

  tr {
    break-inside: avoid;
    page-break-inside: avoid;
  }

  table {
    font-size: 8.5pt;
  }

  table.type-matrix {
    font-size: 6.8pt;
  }

  table.type-matrix th, table.type-matrix td {
    padding: 2px 2px;
  }

  a {
    color: inherit;
    text-decoration: none;
  }
}
"""


def load_species_map() -> dict[str, int]:
    cache_path = DATA_DIR / "pokemon_species.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))
    return {name.lower(): pid for pid, name in COMPANION_ROTATION}


def find_pokemon_in_block(block_text: str, num: int, species_map: dict[str, int]) -> list[tuple[int, str]]:
    """Devuelve hasta 2 pares (id, Nombre) de Pokémon presentes en el bloque o un compañero temático."""
    low = block_text.lower()
    hits: list[tuple[int, str]] = []
    seen_ids: set[int] = set()

    # Buscar en orden de aparición en el texto para priorizar al protagonista
    candidates: list[tuple[int, int, str]] = []
    for sname, pid in species_map.items():
        if not (IMG_DIR / f"{pid}.png").exists():
            continue
        pat = r"\b" + re.escape(sname.replace("-", "[- ]?")) + r"\b"
        m = re.search(pat, low)
        if m:
            candidates.append((m.start(), pid, sname.replace("-", " ").title()))

    candidates.sort(key=lambda x: x[0])
    for _, pid, display in candidates:
        if pid not in seen_ids:
            seen_ids.add(pid)
            hits.append((pid, display))
        if len(hits) >= 2:
            break

    if not hits:
        for kw, pair in CHARACTER_COMPANIONS:
            if kw in low and (IMG_DIR / f"{pair[0]}.png").exists():
                hits.append(pair)
                break

    if not hits:
        for offset in range(len(COMPANION_ROTATION)):
            pid, display = COMPANION_ROTATION[(num + offset) % len(COMPANION_ROTATION)]
            if (IMG_DIR / f"{pid}.png").exists():
                hits.append((pid, display))
                break

    return hits


def protect_math(md_text: str) -> tuple[str, dict[str, str]]:
    placeholders: dict[str, str] = {}
    counter = 0

    def _store(match: re.Match[str]) -> str:
        nonlocal counter
        key = f"@@MATH_TOKEN_{counter}@@"
        counter += 1
        placeholders[key] = match.group(0)
        return key

    protected = re.sub(r"\$\$[\s\S]+?\$\$", _store, md_text)
    protected = re.sub(r"\$(?!\s)([^$\n]+?)(?<!\s)\$", _store, protected)
    return protected, placeholders


def restore_math(html_text: str, placeholders: dict[str, str]) -> str:
    for key, val in placeholders.items():
        html_text = html_text.replace(key, html.escape(val))
    return html_text


def wrap_tables(html_text: str) -> str:
    def _replace_table(match: re.Match[str]) -> str:
        tbl = match.group(0)
        if "Atacante" in tbl and "Defensor" in tbl:
            tbl = tbl.replace("<table>", '<table class="type-matrix">', 1)
        return f'<div class="table-wrapper" tabindex="0" role="region" aria-label="Tabla de referencia">{tbl}</div>'

    return re.sub(r"<table>[\s\S]*?</table>", _replace_table, html_text)


def format_problem_range(nums: list[int]) -> str:
    if not nums:
        return ""
    nums = sorted(set(nums))
    ranges: list[str] = []
    start = prev = nums[0]
    for n in nums[1:]:
        if n == prev + 1:
            prev = n
        else:
            ranges.append(f"{start}" if start == prev else f"{start}–{prev}")
            start = prev = n
    ranges.append(f"{start}" if start == prev else f"{start}–{prev}")
    return ", ".join(ranges)


def build_oak_dossier(
    intro_html: str,
    by_sense: dict[str, list[int]],
    by_subcat: dict[str, list[int]],
    total_problems: int,
    badge: str,
) -> str:
    sense_rows = "".join(
        f"<tr><td>{html.escape(sense)}</td><td>{len(nums)}</td><td>{format_problem_range(nums)}</td></tr>"
        for sense, nums in sorted(by_sense.items(), key=lambda x: -len(x[1]))
    )
    subcat_rows = "".join(
        f"<tr><td>{html.escape(sub)}</td><td>{len(nums)}</td><td>{format_problem_range(nums)}</td></tr>"
        for sub, nums in by_subcat.items()
    )

    intro_block = f'<div class="oak-intro">{intro_html}</div>' if intro_html.strip() else ""

    return f"""
<section id="ficha-profesor-oak" class="prof-oak-dossier">
  <div class="prof-oak-header">
    <h2>Ficha del Profesor Oak — Guía Curricular y LOMLOE (Docentes y Familias)</h2>
    <span class="prof-oak-badge">{html.escape(badge)} · {total_problems} ejercicios</span>
  </div>
  <p>Esta sección está pensada exclusivamente para <strong>profesorado y familias</strong> (se oculta automáticamente en el <em>Modo Alumno</em>). Resume la alineación de este cuadernillo con el currículo oficial de Primaria (<strong>LOMLOE — Real Decreto 157/2022</strong>).</p>
  {intro_block}
  <h3>Distribución por Sentidos Matemáticos LOMLOE</h3>
  <div class="table-wrapper" tabindex="0" role="region" aria-label="Distribución por Sentidos Matemáticos LOMLOE">
    <table>
      <thead>
        <tr><th>Sentido Matemático (RD 157/2022)</th><th>N.º ejercicios</th><th>Ejercicios</th></tr>
      </thead>
      <tbody>{sense_rows}</tbody>
    </table>
  </div>
  <h3>Desglose por Subcategorías</h3>
  <div class="table-wrapper" tabindex="0" role="region" aria-label="Desglose por Subcategorías">
    <table>
      <thead>
        <tr><th>Subcategoría</th><th>N.º ejercicios</th><th>Ejercicios</th></tr>
      </thead>
      <tbody>{subcat_rows}</tbody>
    </table>
  </div>
  <p><strong>Recomendación de aula/casa:</strong> Se sugiere trabajar entre 2 y 3 ejercicios por sesión (o 1 Reto Especial los viernes), animando al alumno a escribir el planteamiento en la cuadrícula de libreta antes de comprobar el solucionario.</p>
</section>
"""


def build_kid_problem_document(raw_md: str, doc: dict, md: markdown.Markdown, species_map: dict[str, int]) -> str:
    """Construye la ficha infantil: cabecera de entrenador, problemas con imágenes y cuadrícula,
    solucionario separado y Ficha del Profesor Oak al final."""
    # Separar Parte 2 (Solucionario)
    sol_split = re.split(r"(?=^## Parte 2:)", raw_md, maxsplit=1, flags=re.M)
    part1_raw = sol_split[0]
    part2_raw = sol_split[1] if len(sol_split) > 1 else ""

    # Separar Introducción curricular (antes de ## Parte 1:) para moverla a la Ficha del Profesor Oak
    p1_split = re.split(r"(?=^## Parte 1:)", part1_raw, maxsplit=1, flags=re.M)
    intro_raw = ""
    if len(p1_split) > 1:
        # Quitar el H1 principal de intro_raw para quedarnos solo con las secciones introductorias
        intro_candidate = re.sub(r"^#\s+.*$", "", p1_split[0], count=1, flags=re.M).strip()
        intro_raw = intro_candidate
        part1_body = p1_split[1]
    else:
        part1_body = part1_raw

    # Extraer bloques de Parte 1 y Parte 1B
    by_sense: dict[str, list[int]] = defaultdict(list)
    by_subcat: dict[str, list[int]] = defaultdict(list)
    total_problems = 0

    # Dividir por secciones ## Parte 1 y ## Parte 1B
    sections = re.split(r"(?=^## Parte 1[B]?:)", part1_body, flags=re.M)
    rendered_sections: list[str] = []

    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        sec_lines = sec.splitlines()
        sec_heading = sec_lines[0]
        is_reto_sec = "Parte 1B" in sec_heading or "Retos Especiales" in sec_heading
        heading_class = ' class="special-challenges-title"' if is_reto_sec else ""
        sec_title_text = re.sub(r"^##\s+", "", sec_heading).strip()
        rendered_cards: list[str] = [f"<h2{heading_class}>{html.escape(sec_title_text)}</h2>"]

        rest_sec = "\n".join(sec_lines[1:])
        blocks = re.split(r"(?=^### (?:Problema|Reto) \d+(?::|\s*$))", rest_sec, flags=re.M)
        for blk in blocks:
            blk = blk.strip()
            m_head = re.match(r"^### (Problema|Reto) (\d+)(?::\s*(.+))?$", blk, flags=re.M)
            if not m_head:
                # Texto introductorio breve de Parte 1B, etc.
                cleaned = blk.strip()
                if cleaned and cleaned != "---":
                    prot, toks = protect_math(cleaned)
                    md.reset()
                    rendered_cards.append(restore_math(md.convert(prot), toks))
                continue

            kind = m_head.group(1)
            num = int(m_head.group(2))
            ptitle = (m_head.group(3) or "").strip()
            heading_label = f"{kind} {num}: {ptitle}" if ptitle else f"{kind} {num}"
            total_problems += 1

            # Extraer metadatos para la Ficha del Profesor Oak y ocultarlos de la tarjeta infantil
            m_sub = re.search(r"^- \*\*Subcategoría\*\*:\s*(.+)$", blk, flags=re.M)
            m_sen = re.search(r"^- \*\*Sentido LOMLOE\*\*:\s*(.+)$", blk, flags=re.M)
            if m_sub:
                by_subcat[m_sub.group(1).strip()].append(num)
            if m_sen:
                by_sense[m_sen.group(1).strip()].append(num)

            # Quitar cabecera ###, Subcategoría y Sentido LOMLOE del cuerpo visible para el niño
            body_lines = []
            for line in blk.splitlines()[1:]:
                if re.match(r"^- \*\*(?:Subcategoría|Sentido LOMLOE)\*\*:", line.strip()):
                    continue
                if line.strip() == "---":
                    continue
                # Limpiar prefijo "- **Contexto Pokémon**: " para que fluya como una historia natural
                line = re.sub(r"^- \*\*Contexto Pokémon\*\*:\s*", "", line)
                body_lines.append(line)

            clean_md = "\n".join(body_lines).strip()
            # Separar la línea **Pregunta**: si existe para destacarla
            q_match = re.search(r"^\*\*Pregunta\*\*:\s*(.+)$", clean_md, flags=re.M)
            story_md = re.sub(r"^\*\*Pregunta\*\*:\s*.+$", "", clean_md, flags=re.M).strip()

            prot_story, toks_story = protect_math(story_md)
            md.reset()
            story_html = wrap_tables(restore_math(md.convert(prot_story), toks_story))

            question_html = ""
            if q_match:
                prot_q, toks_q = protect_math(q_match.group(1).strip())
                md.reset()
                q_rendered = restore_math(md.convert(prot_q), toks_q)
                # Quitar <p> exterior si es un único párrafo
                q_rendered = re.sub(r"^<p>([\s\S]*)</p>$", r"\1", q_rendered.strip())
                question_html = f'<div class="problem-question"><strong>Reto:</strong> {q_rendered}</div>'

            # Buscar Pokémon asociados y generar sus sprites locales
            pokes = find_pokemon_in_block(blk, num, species_map)
            sprites_html = ""
            pill_label = ""
            if pokes:
                imgs = []
                for idx, (pid, pname) in enumerate(pokes):
                    cls = "poke-sprite" if idx == 0 else "poke-sprite poke-sprite-secondary"
                    imgs.append(f'<img src="assets/images/{pid}.png" alt="{html.escape(pname)}" class="{cls}" loading="lazy">')
                sprites_html = f'<div class="problem-sprites">{"".join(imgs)}</div>'
                main_pid, main_name = pokes[0]
                pill_label = f'<span class="poke-pill">#{main_pid:03d} {html.escape(main_name)}</span>'

            reto_cls = " is-reto" if kind == "Reto" else ""
            card_html = f"""
<article class="problem-card{reto_cls}">
  <div class="problem-card-header">
    <h3>{html.escape(heading_label)}</h3>
    {pill_label}
  </div>
  <div class="problem-body-grid">
    {sprites_html}
    <div class="problem-text">
      {story_html}
      {question_html}
    </div>
  </div>
  <div class="workspace-box" aria-label="Espacio para operaciones">
    <span class="workspace-label">Operaciones y respuesta</span>
  </div>
</article>
"""
            rendered_cards.append(card_html)

        rendered_sections.append("\n".join(rendered_cards))

    # Renderizar Parte 2 (Solucionario)
    sol_html = ""
    if part2_raw:
        prot_sol, toks_sol = protect_math(part2_raw)
        md.reset()
        sol_converted = wrap_tables(restore_math(md.convert(prot_sol), toks_sol))
        sol_converted = wrap_cards(sol_converted, "solution-card")
        sol_html = f'\n<section id="solucionario" class="solutions-section">\n{sol_converted}\n</section>'

    # Renderizar intro curricular dentro de la Ficha del Profesor Oak
    intro_html = ""
    if intro_raw:
        prot_intro, toks_intro = protect_math(intro_raw)
        md.reset()
        intro_html = wrap_tables(restore_math(md.convert(prot_intro), toks_intro))

    oak_html = build_oak_dossier(intro_html, by_sense, by_subcat, total_problems, doc["badge"])

    trainer_header = f"""
<section class="header-box">
  <div class="header-title-row">
    <h1>{html.escape(doc["title"])}</h1>
    <span class="badge-grade">{html.escape(doc["badge"])}</span>
  </div>
  <div class="trainer-ranks-bar">
    <span>0–25 EXP: Novato</span>
    <span>26–50 EXP: Entrenador</span>
    <span>51–80 EXP: As de Gimnasio</span>
    <span>81–100 EXP: Líder</span>
    <span>101–120 EXP: Maestro Pokémon</span>
  </div>
  <div class="student-fields">
    <div class="student-field-line">Entrenador/a:</div>
    <div class="student-field-line">Fecha:</div>
    <div class="student-field-line">Puntos EXP: ____ / {total_problems}</div>
  </div>
</section>
<div class="kid-welcome">
  <strong>¡Misión de Entrenamiento!</strong> Lee cada historia con atención, haz tus cálculos en la cuadrícula de libreta y suma <strong>+1 EXP</strong> por cada reto superado.
</div>
"""

    return trainer_header + "\n".join(rendered_sections) + oak_html + sol_html


def wrap_cards(chunk: str, css_class: str) -> str:
    tokens = re.split(r"(<h3[^>]*>[\s\S]*?</h3>)", chunk)
    if len(tokens) <= 1:
        return chunk

    out = [tokens[0]]
    i = 1
    while i < len(tokens):
        h3 = tokens[i]
        body = tokens[i + 1] if i + 1 < len(tokens) else ""
        split_end = re.split(r"(<h2[^>]*>|<hr\s*/?>)", body, maxsplit=1)
        card_body = split_end[0]
        trailing = "".join(split_end[1:]) if len(split_end) > 1 else ""
        out.append(f'<article class="{css_class}">\n{h3}{card_body}\n</article>{trailing}')
        i += 2
    return "".join(out)


def render_page(title: str, body_html: str, is_problems: bool, is_index: bool = False) -> str:
    toggle_btns = ""
    if is_problems:
        toggle_btns = (
            '<button type="button" id="toggle-solutions" class="btn btn-toggle" '
            'onclick="toggleSolutions()">Modo Alumno (solo ejercicios)</button>'
            '<button type="button" id="toggle-workspaces" class="btn btn-toggle" '
            'onclick="toggleWorkspaces()">Ocultar cuadrículas</button>'
        )

    back_btn = "" if is_index else '<a class="btn" href="index.html">← Índice</a>'

    katex_head = """
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin="anonymous">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" crossorigin="anonymous"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" crossorigin="anonymous"
    onload="renderMathInElement(document.body, {delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}], throwOnError: false});"></script>
"""

    script_js = """
  <script>
    function toggleSolutions() {
      const hidden = document.body.classList.toggle('hide-solutions');
      const btn = document.getElementById('toggle-solutions');
      if (btn) {
        btn.classList.toggle('active', hidden);
        btn.textContent = hidden ? 'Mostrar solucionario y Ficha Oak' : 'Modo Alumno (solo ejercicios)';
      }
    }
    function toggleWorkspaces() {
      const hidden = document.body.classList.toggle('hide-workspaces');
      const btn = document.getElementById('toggle-workspaces');
      if (btn) {
        btn.classList.toggle('active', hidden);
        btn.textContent = hidden ? 'Mostrar cuadrículas' : 'Ocultar cuadrículas';
      }
    }
  </script>
"""

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <style>{SHARED_CSS}</style>
  {"" if is_index else katex_head}
</head>
<body>
  <header class="print-toolbar no-print">
    <div class="toolbar-left">
      {back_btn}
      <span class="toolbar-title">{html.escape(title)}</span>
    </div>
    <div class="toolbar-actions">
      {toggle_btns}
      <button type="button" class="btn btn-primary" onclick="window.print()">Imprimir / Guardar PDF</button>
    </div>
  </header>
  <main class="page-container">
    {body_html}
  </main>
  {script_js}
</body>
</html>
"""


def build_index() -> str:
    cards = []
    for doc in DOCS:
        if doc["src"] == "README.md":
            continue
        cards.append(
            f"""
      <div class="doc-card">
        <div>
          <span class="doc-badge">{html.escape(doc["badge"])}</span>
          <h3>{html.escape(doc["title"])}</h3>
          <p>{html.escape(doc["desc"])}</p>
        </div>
        <div class="doc-card-actions">
          <a class="btn-outline" href="{doc["out"]}">Abrir ficha imprimible</a>
        </div>
      </div>"""
        )

    body = f"""
    <section class="header-box">
      <div class="header-title-row">
        <h1>Matemáticas Primaria con Pokémon — Cuadernillos Imprimibles</h1>
        <span class="badge-grade">2º a 6º Primaria</span>
      </div>
    </section>
    <p>Accede a cualquiera de los cuadernillos de entrenador (120 ejercicios ilustrados por curso con cuadrícula de operaciones, <strong>Ficha del Profesor Oak</strong> para docentes/familias y solucionario paso a paso) o a las tablas de referencia.</p>
    <blockquote>
      <strong>Consejo de impresión:</strong> En cada cuadernillo puedes activar el <em>«Modo Alumno (solo ejercicios)»</em> para imprimir únicamente las páginas del niño (sin solucionario ni Ficha del Profesor Oak), o imprimirlo completo con saltos de página automáticos.
    </blockquote>

    <h2>Cuadernillos de Entrenador (600 ejercicios ilustrados)</h2>
    <div class="grid-cards">
      {"".join(cards[:5])}
    </div>

    <h2>Tablas de Referencia y Recursos</h2>
    <div class="grid-cards">
      {"".join(cards[5:])}
      <div class="doc-card">
        <div>
          <span class="doc-badge">Índice y Guía</span>
          <h3>Guía Maestra del Proyecto (README)</h3>
          <p>Mapeo curricular LOMLOE completo, estructura de carpetas y resumen pedagógico.</p>
        </div>
        <div class="doc-card-actions">
          <a class="btn-outline" href="README.html">Abrir guía maestra</a>
        </div>
      </div>
    </div>
    """
    return render_page("Matemáticas Primaria con Pokémon — Índice Imprimible", body, is_problems=False, is_index=True)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists", "nl2br"])
    species_map = load_species_map()

    for doc in DOCS:
        src_path = ROOT_DIR / doc["src"]
        if not src_path.exists():
            print(f"[SKIP] No encontrado: {src_path}")
            continue

        raw_md = src_path.read_text(encoding="utf-8")
        if doc["is_problems"]:
            html_body = build_kid_problem_document(raw_md, doc, md, species_map)
        else:
            protected_md, math_tokens = protect_math(raw_md)
            md.reset()
            html_body = md.convert(protected_md)
            html_body = restore_math(html_body, math_tokens)
            html_body = wrap_tables(html_body)

        full_html = render_page(doc["title"], html_body, is_problems=doc["is_problems"])
        out_path = OUT_DIR / doc["out"]
        out_path.write_text(full_html, encoding="utf-8")
        print(f"[OK] {out_path.name} ({out_path.stat().st_size // 1024} KB)")

    index_path = OUT_DIR / "index.html"
    index_path.write_text(build_index(), encoding="utf-8")
    print(f"[OK] {index_path.name} ({index_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
