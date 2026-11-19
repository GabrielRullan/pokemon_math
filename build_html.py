#!/usr/bin/env python3
"""
Genera la versión HTML lista para imprimir de todos los documentos Markdown
del proyecto Matemáticas Primaria con Pokémon (LOMLOE 1º–6º Primaria),
con estética de ficha infantil, imágenes locales de Pokémon, diagramas SVG,
andamiaje NEAE, filtros interactivos y «Ficha del Profesor Oak» curricular.
"""

from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from pathlib import Path
import markdown

try:
    from svg_diagrams import generate_problem_svg
except ImportError:
    generate_problem_svg = None

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
        "desc": "Visión general del proyecto, mapeo curricular LOMLOE (1º a 6º de Primaria) y estructura de materiales.",
        "is_problems": False,
    },
    {
        "src": "problemas_1_primaria.md",
        "out": "problemas_1_primaria.html",
        "title": "Cuadernillo de Entrenador — 1º de Primaria",
        "badge": "1º Primaria (6–7 años)",
        "desc": "120 ejercicios (100 + 20 Retos Especiales): números hasta 99, sumas/restas sin llevada, formas 2D, horas en punto, monedas y EXP.",
        "is_problems": True,
        "grade": 1,
    },
    {
        "src": "problemas_2_primaria.md",
        "out": "problemas_2_primaria.html",
        "title": "Cuadernillo de Entrenador — 2º de Primaria",
        "badge": "2º Primaria (7–8 años)",
        "desc": "120 ejercicios (100 + 20 Retos Especiales): números hasta 999, sumas/restas, formas 2D, horas, euros y EXP.",
        "is_problems": True,
        "grade": 2,
    },
    {
        "src": "problemas_3_primaria.md",
        "out": "problemas_3_primaria.html",
        "title": "Cuadernillo de Entrenador — 3º de Primaria",
        "badge": "3º Primaria (8–9 años)",
        "desc": "120 ejercicios (100 + 20 Retos Especiales): números hasta 9.999, tablas, división, medidas, gráficos y EXP.",
        "is_problems": True,
        "grade": 3,
    },
    {
        "src": "problemas_4_primaria.md",
        "out": "problemas_4_primaria.html",
        "title": "Cuadernillo de Entrenador — 4º de Primaria",
        "badge": "4º Primaria (9–10 años)",
        "desc": "120 ejercicios (100 + 20 Retos Especiales): multiplicación 2 cifras, división, fracciones, decimales, áreas y EXP.",
        "is_problems": True,
        "grade": 4,
    },
    {
        "src": "problemas_5_primaria.md",
        "out": "problemas_5_primaria.html",
        "title": "Cuadernillo de Entrenador — 5º de Primaria",
        "badge": "5º Primaria (10–11 años)",
        "desc": "120 ejercicios (100 + 20 Retos Especiales): fracciones, decimales, porcentajes, coordenadas, áreas y EXP.",
        "is_problems": True,
        "grade": 5,
    },
    {
        "src": "problemas_6_primaria.md",
        "out": "problemas_6_primaria.html",
        "title": "Cuadernillo de Entrenador — 6º de Primaria",
        "badge": "6º Primaria (11–12 años)",
        "desc": "120 ejercicios (100 + 20 Retos Especiales): porcentajes, proporcionalidad, enteros, volúmenes, probabilidad y EXP.",
        "is_problems": True,
        "grade": 6,
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
  flex-direction: column;
  gap: 0.55rem;
  padding: 0.7rem 1.25rem;
  background: #0f172a;
  color: #f8fafc;
  border-bottom: 3px solid var(--pk-yellow);
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.18);
}

.toolbar-main {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.toolbar-filters {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem 0.75rem;
  padding-top: 0.45rem;
  border-top: 1px solid rgba(255, 255, 255, 0.14);
}

.filter-group {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: #e2e8f0;
}

.filter-select,
.filter-input {
  background: #ffffff;
  color: #0f172a;
  border: 1px solid #94a3b8;
  border-radius: 6px;
  padding: 0.25rem 0.45rem;
  font-size: 0.8rem;
  font-weight: 600;
}

.filter-select {
  max-width: 215px;
}

.filter-input {
  width: 60px;
}

.filter-status {
  margin-left: auto;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  background: rgba(255, 203, 5, 0.18);
  border: 1px solid rgba(255, 203, 5, 0.45);
  color: #fde047;
  font-size: 0.78rem;
  font-weight: 700;
}

.btn-preset {
  background: rgba(16, 185, 129, 0.22);
  border-color: rgba(110, 231, 183, 0.45);
}

.btn-preset:hover {
  background: rgba(16, 185, 129, 0.38);
}

.is-filtered-hidden {
  display: none !important;
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

.problem-question p {
  margin: 0.25rem 0;
}

.problem-question p:first-child {
  margin-top: 0;
}

.problem-question p:last-child {
  margin-bottom: 0;
}

.problem-question ul,
.problem-question ol {
  margin: 0.35rem 0 0.2rem 1.25rem;
}

.problem-diagram {
  margin: 0.55rem 0 0.25rem;
  padding: 0.4rem;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.problem-diagram svg {
  max-width: 100%;
  max-height: 150px;
  width: auto;
  height: auto;
  display: block;
}

.rotom-hint {
  margin-top: 0.5rem;
  padding: 0.38rem 0.65rem;
  background: #fffbeb;
  border: 1px solid #fcd34d;
  border-left: 4px solid #f59e0b;
  border-radius: 0 6px 6px 0;
  font-size: 0.83rem;
  color: #78350f;
}

body.hide-hints .rotom-hint {
  display: none !important;
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
  overflow: hidden;
}

body.grade-early .workspace-box,
.page-container.grade-early .workspace-box {
  height: 115px;
}

.workspace-columns {
  display: grid;
  grid-template-columns: 1fr 1.85fr 1.15fr;
  height: 100%;
  width: 100%;
}

.workspace-col {
  border-right: 1px dashed #cbd5e1;
  padding: 3px 6px;
}

.workspace-col:last-child {
  border-right: 0;
}

.workspace-col-title {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  color: #64748b;
  background: rgba(255, 255, 255, 0.9);
  padding: 0 4px;
  border-radius: 3px;
  border: 1px solid #e2e8f0;
}

body.hide-workspaces .workspace-box {
  display: none !important;
}

/* Solucionario */
.solutions-subcat-heading {
  margin-top: 1.35rem;
  margin-bottom: 0.65rem;
  padding: 0.38rem 0.75rem;
  font-size: 1.05rem;
  color: #065f46;
  background: #ecfdf5;
  border-left: 4px solid #10b981;
  border-radius: 0 6px 6px 0;
}

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

.sol-meta {
  margin: 0 0 0.45rem;
  font-size: 0.8rem;
  color: #1e293b;
  background: #e2e8f0;
  display: inline-block;
  padding: 0.14rem 0.55rem;
  border-radius: 6px;
}

.oak-details {
  margin-top: 1rem;
  background: #ffffff;
  border: 1px solid #a7f3d0;
  border-radius: 8px;
  padding: 0.65rem 0.9rem;
}

.oak-details summary {
  cursor: pointer;
  font-weight: 700;
  color: #065f46;
}

.rubric-table td,
.rubric-table th {
  font-size: 0.82rem;
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

  .problem-diagram {
    margin: 0.35rem 0 0.15rem;
    padding: 0.25rem;
  }

  .problem-diagram svg {
    max-height: 150px;
  }

  .rotom-hint {
    padding: 0.25rem 0.5rem;
    font-size: 8.5pt;
  }

  .workspace-box {
    height: 70px;
  }

  body.grade-early .workspace-box,
  .page-container.grade-early .workspace-box {
    height: 95px;
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


CANONICAL_SENSE_RULES: list[tuple[str, str]] = [
    (r"num[ée]ric", "Sentido Numérico"),
    (r"medida", "Sentido de la Medida"),
    (r"espacial|geom[ée]tr", "Sentido Espacial"),
    (r"algebraic|computacional|patron", "Sentido Algebraico"),
    (r"estoc[áa]stic|estad[íi]stic|azar|probabilidad", "Sentido Estocástico"),
]

# Reglas (patrón regex, pista sin revelar números de respuesta)
ROTOM_HINT_RULES: list[tuple[str, str]] = [
    (
        r"cuadrado\s+m[áa]gico",
        "Halla primero la suma mágica de una fila, columna o diagonal completa y úsala para deducir cada casilla que falta.",
    ),
    (
        r"pir[áa]mide\s+(?:num[ée]rica|multiplicativa|de\s+(?:bayas|piedras))",
        "En una pirámide numérica, cada casilla superior se calcula operando con las dos casillas situadas justo debajo.",
    ),
    (
        r"\b(?:ecuaci[óo]n|inc[óo]gnita)\b|primer\s+grado",
        "Despeja la incógnita paso a paso: traduce cada frase a una operación y comprueba tu solución sustituyendo.",
    ),
    (
        r"f[óo]rmula\s+can[óo]nica|sustituye\s+los\s+valores",
        "Sustituye cada letra por su valor numérico respetando la jerarquía de operaciones (paréntesis, multiplicaciones y divisiones antes que sumas).",
    ),
    (
        r"\b(?:reloj|en\s+punto|y\s+media|y\s+cuarto|menos\s+cuarto)\b",
        "Fíjate en la aguja corta (horas) y la aguja larga (minutos): cada marca grande equivale a 5 minutos.",
    ),
    (
        r"\b(?:suceso\s+(?:seguro|posible|imposible)|seguro,\s*posible|posible\s+o\s+imposible)\b",
        "Piensa si el suceso ocurre siempre (seguro), algunas veces (posible) o nunca (imposible) según los datos.",
    ),
    (
        r"\b(?:probabilidad|al\s+azar|urna|ruleta|suceso\s+contrario|(?:lanzar|tirar)\s+(?:un|dos|varios)?\s*dados?)\b",
        "Cuenta primero el total de casos posibles y después cuántos casos favorables cumplen la condición.",
    ),
    (
        r"\b(?:media\s+aritm[ée]tica|calcula(?:r)?\s+la\s+media|halla(?:r)?\s+la\s+media|media,\s*mediana|promedio)\b",
        "Para hallar la media, suma todos los valores obtenidos y divide el resultado entre el número total de datos.",
    ),
    (
        r"\bmoda\b",
        "La moda es el dato o categoría que se repite con mayor frecuencia.",
    ),
    (
        r"\b(?:gr[áa]fico|pictograma|tabla\s+de\s+recuento|diagrama\s+de\s+sectores|encuesta|frecuencia)\b",
        "Lee con atención los ejes, la leyenda o el valor de cada símbolo del gráfico antes de sumar o comparar.",
    ),
    (
        r"\b(?:escala|maqueta)\b|\b1\s*:\s*\d+",
        "Aplica la razón de la escala comparando la medida del plano o maqueta con la realidad en la misma unidad.",
    ),
    (
        r"\b(?:hora|horas|minuto|minutos|segundo|segundos|calendario|semana|semanas)\b",
        "Comprueba si debes pasar horas a minutos (× 60) o minutos a segundos antes de sumar o restar tiempos.",
    ),
    (
        r"(?:\bdescuento\b|\brebaja\b|\biva\b|\bporcentaje\b|\bpor\s+ciento\b|%)",
        "Calcula primero la parte correspondiente al tanto por ciento (multiplica y divide entre 100) antes del paso final.",
    ),
    (
        r"(?:€|\beuros?\b|\bc[ée]ntimos?\b|\bmonedas?\b|\bbilletes?\b|\bpok[ée]d[óo]lar(?:es)?\b|\bpok[ée]monedas?\b|\bcambio\b|\bprecio\b|\bcuesta\b|\btienda\b)",
        "Anota el precio de cada artículo que compras y, si te piden el cambio, réstaselo al dinero entregado.",
    ),
    (
        r"(?:bajo\s+cero|°\s*c|bajo\s+el\s+nivel\s+del\s+mar|\bprofundidad\b|\baltitud\b|\bnegativo\b|\benteros?\b|\bprioridad\b)",
        "Usa una recta con el 0 como referencia: mide por un lado el tramo negativo hasta 0 y súmale la parte positiva.",
    ),
    (
        r"(?:\bpotencias?\b|\bc[uú]bic[ao]s?\b|cuadrado\s+perfecto|cuadrados\s+perfectos|ra[íi]z\s+cuadrada|\belevado\b|al\s+cuadrado|\btatamis?\b|\^\s*[23]|[²³])",
        "Recuerda que una potencia multiplica la base por sí misma y la raíz cuadrada busca qué número al cuadrado da el total.",
    ),
    (
        r"(?:m\.c\.m|m\.c\.d|\bdivisible\b|\bdivisores?\b|\bm[uú]ltiplos?\b|\bprimos?\b|\bcompuestos?\b)",
        "Aplica las reglas de divisibilidad o escribe de forma ordenada los múltiplos o divisores comunes.",
    ),
    (
        r"\b(?:hect[áa]reas?|metros\s+cuadrados|m²|km²|cm²)\b",
        "Pasa todas las unidades de superficie a la misma unidad (recuerda que en superficie cada salto multiplica o divide por 100).",
    ),
    (
        r"\b(?:coordenadas?|cuadrantes?|plano\s+cartesiano)\b",
        "Lee y escribe siempre primero la coordenada horizontal (X) y después la vertical (Y), cuidando los signos.",
    ),
    (
        r"\bsimetr",
        "Imagina doblar la figura por su eje de simetría y comprueba si los dos lados coinciden exactamente.",
    ),
    (
        r"\b[áa]ngulos?\b|\d+\s*°(?!\s*c)",
        "Recuerda las referencias clave: un ángulo recto mide 90°, uno llano 180° y la vuelta completa 360°.",
    ),
    (
        r"\b(?:per[íi]metro|valla|contorno|rodear)\b",
        "El perímetro se obtiene sumando las longitudes de todos los lados exteriores del contorno.",
    ),
    (
        r"\b(?:[áa]rea|superficie)\b",
        "Identifica la forma geométrica, anota sus dimensiones (base, altura o radio) y aplica su fórmula de área.",
    ),
    (
        r"\b(?:fracci[óo]n|fracciones|numerador|denominador|irreducible|equivalente)\b|\d+/\d+",
        "Comprueba si los denominadores son iguales; si no lo son, busca primero un denominador común equivalente.",
    ),
    (
        r"\b(?:volumen\s+(?:de\s+un|del)\s+(?:cubo|prisma|cilindro|cono)|cilindros?|conos?|poliedros?|aristas?|v[ée]rtices?|cuerpo\s+geom[ée]trico)\b",
        "Identifica las caras, vértices o aristas de la figura, o multiplica sus tres dimensiones en las mismas unidades.",
    ),
    (
        r"\b(?:km|hm|dam|m|dm|cm|mm|kg|hg|dag|g|mg|kl|hl|dal|l|dl|cl|ml|metros?|cent[íi]metros?|kil[óo]metros?|palmos?|pasos?)\b",
        "Pasa todas las medidas a la misma unidad antes de comparar, sumar o multiplicar.",
    ),
    (
        r"\b(?:tri[áa]ngulos?|cuadrados?|rect[áa]ngulos?|c[íi]rculos?|circunferencias?|radios?|di[áa]metros?|pol[íi]gonos?)\b",
        "Haz un boceto rápido en la cuadrícula señalando lados, vértices o el radio/diámetro antes de operar.",
    ),
    (
        r"\b(?:decimales?|d[ée]cimas?|cent[ée]simas?|mil[ée]simas?)\b",
        "Alinea bien las comas decimales al sumar o restar, y cuenta las cifras decimales totales al multiplicar.",
    ),
    (
        r"\b(?:stab|multiplicador|s[uú]per\s+eficaz|eficaz|debilidad|resistencia)\b",
        "Aplica el multiplicador de cada tipo del defensor y recuerda multiplicar por 1,5 si coincide con el tipo del atacante.",
    ),
    (
        r"(?:puntos\s+de\s+salud|\bps\b|\bpoci[óo]n\b|\bpociones\b|baya\s+aranja|curaci[óo]n)",
        "Sigue el orden de los turnos: resta el daño recibido y suma las curaciones sin superar el máximo.",
    ),
    (
        r"(?:\bexp\b|experiencia|subir\s+de\s+nivel|curva\s+de\s+crecimiento|curva\s+media|huevo\s+suerte|caramelo\s+raro)",
        "Compara la EXP acumulada o ganada por combate con el objetivo necesario para alcanzar el siguiente nivel.",
    ),
    (
        r"\b(?:redondea|m[áa]s\s+cercan[ao]|recta\s+num[ée]rica)\b",
        "Fíjate en la cifra siguiente al orden que redondeas: si es 5 o mayor sube, y si es menor que 5 se mantiene.",
    ),
    (
        r"\b(?:decenas?|centenas?|unidades?|anterior|posterior|par|impar|ordinal|menor\s+a\s+mayor|mayor\s+a\s+menor)\b",
        "Coloca cada cifra en su posición (UM, C, D, U) y compáralas ordenadamente de izquierda a derecha.",
    ),
    (
        r"\b(?:serie|patr[óo]n|secuencia|pista|l[óo]gica|misterioso|adivina|deducci[óo]n)\b",
        "Comprueba cuánto cambia de un paso al siguiente o ve descartando las opciones que incumplen cada pista.",
    ),
]

SUBCAT_FALLBACK_HINTS: dict[str, str] = {
    "1": "Descompón el número según el valor posicional de cada cifra antes de comparar u ordenar.",
    "2": "Identifica si el problema pide juntar (sumar), comparar/quitar (restar), repetir (multiplicar) o repartir (dividir).",
    "3": "Subraya la magnitud y su unidad de medida en cada dato antes de calcular.",
    "4": "Dibuja un esquema sencillo de la figura o recorrido en la cuadrícula para visualizar los datos.",
    "5": "Busca la regla o patrón que relaciona los datos y compruébala paso a paso.",
    "6": "Organiza los datos en una pequeña tabla o lista ordenada antes de responder.",
    "7": "Anota por separado los datos del combate (nivel, PS o EXP) y resuelve por pasos.",
    "reto": "Divide este reto en pasos cortos, anota los datos de cada pista y revisa al final todas las preguntas.",
}

CYCLE_INFO: dict[int, tuple[str, str, list[tuple[str, str, str]]]] = {
    1: (
        "Primer Ciclo (1º–2º de Primaria)",
        "1º–2º Prim.",
        [
            ("CE1 · Interpretar situaciones cotidianas matemáticamente", "1.1, 1.2 (1.er ciclo)", "Lectura comprensiva de historias Pokémon y extracción de datos en 1 o 2 pasos."),
            ("CE2 · Resolver problemas aplicando estrategias y comprobación", "2.1, 2.2 (1.er ciclo)", "Uso de sumas, restas sin/con llevada, conteo visual y verificación de resultados."),
            ("CE3 · Formular y comprobar conjeturas sencillas guiadas", "3.1, 3.2 (1.er ciclo)", "Adivinanzas de la Pokédex, estimación en recta numérica y retos lógicos 101–120."),
            ("CE4 · Pensamiento computacional, patrones y algoritmos", "4.1, 4.2 (1.er ciclo)", "Series numéricas (+2, +5, +10), patrones de Poké Balls e instrucciones ordenadas."),
            ("CE5 · Conexiones entre ideas matemáticas y entorno cercano", "5.1, 5.2 (1.er ciclo)", "Relación entre numeración, relojes analógicos, monedas de euro y puntos EXP."),
            ("CE6 · Comunicar ideas y resultados con lenguaje adecuado", "6.1, 6.2 (1.er ciclo)", "Expresión escrita de la respuesta con unidad explícita en la zona guiada NEAE."),
            ("CE7 · Autoconfianza y gestión emocional ante retos", "7.1, 7.2 (1.er ciclo)", "Andamiaje con pistas de Rotom Dex y progresión motivadora de rangos de Entrenador."),
            ("CE8 · Trabajo cooperativo y respeto a la diversidad", "8.1, 8.2 (1.er ciclo)", "Resolución por parejas y puesta en común de distintas estrategias en clase."),
        ],
    ),
    2: (
        "Segundo Ciclo (3º–4º de Primaria)",
        "3º–4º Prim.",
        [
            ("CE1 · Modelizar situaciones mediante representaciones", "1.1, 1.2 (2.º ciclo)", "Traducción de contextos Pokémon (tiendas, rutas, combates) a operaciones combinadas."),
            ("CE2 · Resolver situaciones eligiendo estrategias eficaces", "2.1, 2.2 (2.º ciclo)", "Multiplicación multidígito, división entera con resto, fracciones simples y decimales."),
            ("CE3 · Explorar, formular y argumentar conjeturas", "3.1, 3.2 (2.º ciclo)", "Comprobación de propiedades, rejillas lógicas y retos de optimización (101–120)."),
            ("CE4 · Pensamiento computacional y generalización guiada", "4.1, 4.2 (2.º ciclo)", "Secuencias crecientes, reglas de multiplicadores y descomposición de retos en subpasos."),
            ("CE5 · Conectar sentidos matemáticos entre sí y con la realidad", "5.1, 5.2 (2.º ciclo)", "Vínculo entre magnitudes métricas (cm/m, g/kg, ml/l), perímetros, áreas y EXP."),
            ("CE6 · Comunicar y representar con precisión multimodal", "6.1, 6.2 (2.º ciclo)", "Interpretación de diagramas SVG, tablas de recuento, gráficos de barras y unidades."),
            ("CE7 · Perseverancia, aceptación del error y autonomía", "7.1, 7.2 (2.º ciclo)", "Autorregulación con la estructura Datos–Operación–Respuesta y pistas opcionales."),
            ("CE8 · Colaboración activa y valoración de estrategias ajenas", "8.1, 8.2 (2.º ciclo)", "Debate en pequeño grupo sobre métodos alternativos en el Gimnasio matemático."),
        ],
    ),
    3: (
        "Tercer Ciclo (5º–6º de Primaria)",
        "5º–6º Prim.",
        [
            ("CE1 · Interpretar y modelizar situaciones complejas", "1.1, 1.2 (3.er ciclo)", "Análisis de enunciados multipaso con porcentajes, enteros, escalas y mecánicas oficiales."),
            ("CE2 · Explorar vías de resolución y validar coherencia", "2.1, 2.2 (3.er ciclo)", "Operaciones con fracciones (m.c.m.), proporcionalidad, volúmenes y caza del error."),
            ("CE3 · Formular hipótesis, justificar y refutar razonadamente", "3.1, 3.2 (3.er ciclo)", "Argumentación algebraica, divisibilidad, primos/compuestos y probabilidad de Laplace."),
            ("CE4 · Pensamiento computacional, fórmulas y modelización", "4.1, 4.2 (3.er ciclo)", "Aplicación de fórmulas canónicas (PS, daño con STAB, curvas cúbicas L³ y Repartir EXP)."),
            ("CE5 · Interrelacionar ideas matemáticas y contextos reales", "5.1, 5.2 (3.er ciclo)", "Integración de plano cartesiano (4 cuadrantes), porcentajes, estadística y geometría 3D."),
            ("CE6 · Comunicar rigorosamente con lenguaje formal y gráfico", "6.1, 6.2 (3.er ciclo)", "Lectura e interpretación de gráficas SVG, notación fraccionaria/decimal y unidades exactas."),
            ("CE7 · Autorregulación emocional ante la incertidumbre", "7.1, 7.2 (3.er ciclo)", "Gestión de retos avanzados sin pistas previas (Contenidos Específicos reservados al docente)."),
            ("CE8 · Trabajo en equipo heterogéneo y respeto mutuo", "8.1, 8.2 (3.er ciclo)", "Co-evaluación mediante rúbrica competencial y resolución colaborativa de ligas/retos."),
        ],
    ),
}


def infer_subcat_code(prob_num: int, kind: str, raw_subcat: str) -> str:
    """Devuelve '1'..'7' para problemas base o 'reto' para Retos Especiales."""
    if kind.lower() == "reto" or prob_num > 100:
        return "reto"
    m = re.search(r"Subcategor[ií]a\s*([1-7])\b", raw_subcat, flags=re.I)
    if m:
        return m.group(1)
    if 1 <= prob_num <= 15:
        return "1"
    if 16 <= prob_num <= 35:
        return "2"
    if 36 <= prob_num <= 50:
        return "3"
    if 51 <= prob_num <= 65:
        return "4"
    if 66 <= prob_num <= 75:
        return "5"
    if 76 <= prob_num <= 85:
        return "6"
    return "7"


def infer_canonical_senses(prob_num: int, raw_sense: str, raw_subcat: str) -> list[str]:
    """Infiere los Sentidos LOMLOE canónicos para etiquetar filtros y tarjetas."""
    found: list[str] = []
    for text in (raw_sense.lower(), raw_subcat.lower()):
        for pat, canonical in CANONICAL_SENSE_RULES:
            if re.search(pat, text) and canonical not in found:
                found.append(canonical)
        if found:
            return found

    if 36 <= prob_num <= 50:
        return ["Sentido de la Medida"]
    if 51 <= prob_num <= 65:
        return ["Sentido Espacial"]
    if 66 <= prob_num <= 75:
        return ["Sentido Algebraico"]
    if 76 <= prob_num <= 85:
        return ["Sentido Estocástico"]
    return ["Sentido Numérico"]


def generate_rotom_hint(
    subcat_code: str,
    story_text: str,
    question_text: str,
    grade: int,
) -> str:
    """Genera una pista heurística sin spoilers para Rotom Dex."""
    combined = f"{story_text} {question_text}".lower()
    if grade in (1, 2) and re.search(r"\b(?:reloj|en\s+punto|y\s+media)\b", combined):
        return "La aguja corta señala la hora y la aguja larga los minutos: arriba es «en punto» y abajo es «y media»."
    for pat, hint_text in ROTOM_HINT_RULES:
        if re.search(pat, combined):
            return hint_text
    return SUBCAT_FALLBACK_HINTS.get(subcat_code, SUBCAT_FALLBACK_HINTS["reto"])


def build_lomloe_ce_table(grade: int) -> str:
    """Construye la tabla de Competencias Específicas (CE1–CE8) y Criterios según el ciclo."""
    cycle_num = 1 if grade <= 2 else (2 if grade <= 4 else 3)
    cycle_title, cycle_short, rows = CYCLE_INFO[cycle_num]
    rows_html = "".join(
        f"<tr><td>{html.escape(ce)}</td><td>{html.escape(crit)}</td><td>{html.escape(conn)}</td></tr>"
        for ce, crit, conn in rows
    )
    return f"""
  <h3>Competencias Específicas (CE1–CE8) y Criterios de Evaluación — {html.escape(cycle_title)}</h3>
  <div class="table-wrapper" tabindex="0" role="region" aria-label="Competencias Específicas LOMLOE">
    <table>
      <thead>
        <tr>
          <th>Competencia Específica (LOMLOE)</th>
          <th>Criterios de Evaluación (RD 157/2022 · {html.escape(cycle_short)})</th>
          <th>Aplicación en el Cuadernillo Pokémon</th>
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
  </div>
"""


def build_rubric_table() -> str:
    """Construye la Rúbrica de Evaluación Competencial de 4 niveles para docentes."""
    dimensions = [
        (
            "Comprensión y extracción de datos",
            "Identifica datos aislados con ayuda directa; confunde magnitudes o la pregunta.",
            "Extrae los datos principales en problemas simples, aunque omite algún matiz en enunciados largos.",
            "Identifica con autonomía todos los datos relevantes y comprende exactamente qué se pregunta.",
            "Sintetiza datos explícitos e implícitos (tablas, gráficas, pistas) y detecta información superflua.",
        ),
        (
            "Estrategia y modelización",
            "Elige la operación por ensayo-error sin un plan claro o sin esquema previo.",
            "Aplica estrategias conocidas en ejercicios rutinarios con apoyo de pistas o andamiaje.",
            "Selecciona y ordena adecuadamente las operaciones o fórmulas matemáticas necesarias.",
            "Combina varias estrategias, valida alternativas y resuelve retos abiertos o multipaso con soltura.",
        ),
        (
            "Cálculo y precisión",
            "Comete errores frecuentes en el algoritmo básico o al operar con números/unidades.",
            "Realiza cálculos básicos correctamente, con algún fallo puntual en llevadas, decimales o conversiones.",
            "Ejecuta los cálculos numéricos, fraccionarios o geométricos con precisión y comprueba el resultado.",
            "Calcula con agilidad y exactitud, verifica la coherencia del orden de magnitud y detecta errores.",
        ),
        (
            "Comunicación y unidades",
            "Escribe solo una cifra suelta sin explicar el proceso ni indicar las unidades.",
            "Presenta parte del procedimiento en la cuadrícula, pero olvida unidades o redacta la respuesta incompleta.",
            "Ordena Datos, Operación y Respuesta completa con las unidades físicas o del juego correctas.",
            "Argumenta cada paso con vocabulario matemático preciso, gráficos claros y unidades impecables.",
        ),
    ]
    rows_html = "".join(
        f"<tr><td>{html.escape(dim)}</td><td>{html.escape(n1)}</td><td>{html.escape(n2)}</td>"
        f"<td>{html.escape(n3)}</td><td>{html.escape(n4)}</td></tr>"
        for dim, n1, n2, n3, n4 in dimensions
    )
    return f"""
  <h3>Rúbrica de Evaluación Competencial (4 Niveles LOMLOE)</h3>
  <div class="table-wrapper" tabindex="0" role="region" aria-label="Rúbrica de Evaluación Competencial">
    <table class="rubric-table">
      <thead>
        <tr>
          <th>Dimensión</th>
          <th>1. En inicio</th>
          <th>2. En desarrollo</th>
          <th>3. Adquirido</th>
          <th>4. Excelente</th>
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
  </div>
"""


def build_oak_dossier(
    intro_html: str,
    by_sense: dict[str, list[int]],
    by_subcat: dict[str, list[int]],
    total_problems: int,
    badge: str,
    grade: int = 0,
    by_contenido: list[tuple[int, str, str]] | None = None,
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
    ce_block = build_lomloe_ce_table(grade)
    rubric_block = build_rubric_table()

    contenido_block = ""
    if by_contenido:
        cont_rows = "".join(
            f"<tr><td>{num}</td><td>{html.escape(title)}</td><td>{html.escape(cont)}</td></tr>"
            for num, title, cont in by_contenido
        )
        contenido_block = f"""
  <details open class="oak-details">
    <summary>Mapa de Contenidos Específicos por Ejercicio ({len(by_contenido)} ejercicios — oculto en las tarjetas del alumno)</summary>
    <div class="table-wrapper" tabindex="0" role="region" aria-label="Contenidos Específicos por Ejercicio">
      <table>
        <thead>
          <tr><th>N.º</th><th>Ejercicio</th><th>Contenido Específico (LOMLOE)</th></tr>
        </thead>
        <tbody>{cont_rows}</tbody>
      </table>
    </div>
  </details>
"""

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
  {ce_block}
  {rubric_block}
  {contenido_block}
  <p><strong>Recomendación de aula/casa:</strong> Se sugiere trabajar entre 2 y 3 ejercicios por sesión (o usar el botón <em>«Ficha de sesión (5 ej.)»</em>), animando al alumnado a organizar <em>Datos · Operación · Respuesta</em> en la cuadrícula NEAE antes de comprobar el solucionario.</p>
</section>
"""


def render_question_html(question_md: str, md: markdown.Markdown) -> str:
    """Renderiza bloques **Pregunta**: de una o varias líneas sin romper etiquetas."""
    if not question_md.strip():
        return ""
    prot_q, toks_q = protect_math(question_md.strip())
    md.reset()
    q_rendered = wrap_tables(restore_math(md.convert(prot_q), toks_q)).strip()
    single_p = re.fullmatch(r"<p>([\s\S]*)</p>", q_rendered)
    if single_p and "</p>" not in single_p.group(1):
        return f'<div class="problem-question"><strong>Reto:</strong> {single_p.group(1)}</div>'
    if q_rendered.startswith("<p>"):
        q_rendered = q_rendered.replace("<p>", "<p><strong>Reto:</strong> ", 1)
    else:
        q_rendered = f"<strong>Reto:</strong> {q_rendered}"
    return f'<div class="problem-question">{q_rendered}</div>'


def build_kid_problem_document(raw_md: str, doc: dict, md: markdown.Markdown, species_map: dict[str, int]) -> str:
    """Construye la ficha infantil: cabecera de entrenador, problemas con imágenes, SVG,
    pistas Rotom Dex, cuadrícula NEAE 3 zonas, Ficha del Profesor Oak y solucionario."""
    grade = doc.get("grade") or 0
    if not grade:
        m_g = re.search(r"problemas_(\d+)_primaria", doc["src"])
        grade = int(m_g.group(1)) if m_g else 0

    # Separar Parte 2 (Solucionario)
    sol_split = re.split(r"(?=^## Parte 2:)", raw_md, maxsplit=1, flags=re.M)
    part1_raw = sol_split[0]
    part2_raw = sol_split[1] if len(sol_split) > 1 else ""

    # Separar Introducción curricular (antes de ## Parte 1:) para moverla a la Ficha del Profesor Oak
    p1_split = re.split(r"(?=^## Parte 1:)", part1_raw, maxsplit=1, flags=re.M)
    intro_raw = ""
    if len(p1_split) > 1:
        intro_candidate = re.sub(r"^#\s+.*$", "", p1_split[0], count=1, flags=re.M).strip()
        intro_raw = intro_candidate
        part1_body = p1_split[1]
    else:
        part1_body = part1_raw

    by_sense: dict[str, list[int]] = defaultdict(list)
    by_subcat: dict[str, list[int]] = defaultdict(list)
    by_contenido: list[tuple[int, str, str]] = []
    problem_meta: dict[int, dict[str, str]] = {}
    total_problems = 0

    sections = re.split(r"(?=^## Parte 1B?\b)", part1_body, flags=re.M)
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
        sec_kind = "reto" if is_reto_sec else "problema"
        rendered_cards: list[str] = [f"<h2{heading_class}>{html.escape(sec_title_text)}</h2>"]

        rest_sec = "\n".join(sec_lines[1:])
        blocks = re.split(r"(?=^### (?:Problema|Reto) \d+(?::|\s*$))", rest_sec, flags=re.M)
        for blk in blocks:
            blk = blk.strip()
            m_head = re.match(r"^### (Problema|Reto) (\d+)(?::\s*(.+))?$", blk, flags=re.M)
            if not m_head:
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

            # Extraer metadatos docentes (nunca mostrar Contenido Específico al alumno)
            m_sub = re.search(r"^(?:-\s*)?\*\*Subcategoría\*\*:\s*(.+)$", blk, flags=re.M)
            m_sen = re.search(r"^(?:-\s*)?\*\*Sentido LOMLOE\*\*:\s*(.+)$", blk, flags=re.M)
            m_cont = re.search(r"^(?:-\s*)?\*\*Contenido Específico\*\*:\s*(.+)$", blk, flags=re.M)
            subcat_raw = m_sub.group(1).strip() if m_sub else ""
            sense_raw = m_sen.group(1).strip() if m_sen else ""
            cont_raw = m_cont.group(1).strip() if m_cont else ""

            if subcat_raw:
                by_subcat[subcat_raw].append(num)
            if sense_raw:
                by_sense[sense_raw].append(num)
            if cont_raw:
                by_contenido.append((num, ptitle or f"{kind} {num}", cont_raw))

            kind_attr = kind.lower()
            subcat_code = infer_subcat_code(num, kind, subcat_raw)
            senses_list = infer_canonical_senses(num, sense_raw, subcat_raw)
            sense_attr = "|".join(senses_list)

            problem_meta[num] = {
                "kind": kind_attr,
                "subcat": subcat_code,
                "sense": sense_attr,
                "contenido": cont_raw,
            }

            # Quitar cabecera ###, Subcategoría, Sentido LOMLOE y Contenido Específico
            body_lines = []
            for line in blk.splitlines()[1:]:
                stripped = line.strip()
                if re.match(r"^(?:-\s*)?\*\*(?:Subcategoría|Sentido LOMLOE|Contenido Específico)\*\*:", stripped):
                    continue
                if stripped == "---":
                    continue
                line = re.sub(r"^(?:-\s*)?\*\*Contexto Pokémon\*\*:\s*", "", line)
                body_lines.append(line)

            clean_md = "\n".join(body_lines).strip()
            # Extraer **Pregunta**: aunque ocupe varias líneas (ej. 5º y 6º con a), b), c) o tablas)
            q_split = re.split(r"^\*\*Pregunta\*\*:\s*", clean_md, maxsplit=1, flags=re.M)
            if len(q_split) == 2:
                story_md = q_split[0].strip()
                question_md = q_split[1].strip()
            else:
                story_md = clean_md
                question_md = ""

            prot_story, toks_story = protect_math(story_md)
            md.reset()
            story_html = wrap_tables(restore_math(md.convert(prot_story), toks_story))
            question_html = render_question_html(question_md, md)

            # Diagrama SVG opcional de svg_diagrams.py
            diagram_html = ""
            if generate_problem_svg is not None:
                try:
                    svg_out = generate_problem_svg(
                        num, kind, ptitle, subcat_raw, sense_raw, story_md, question_md, grade
                    )
                    if svg_out and svg_out.strip():
                        diagram_html = svg_out.strip()
                except Exception:
                    diagram_html = ""

            # Pista no-spoiler de Rotom Dex
            hint_text = generate_rotom_hint(subcat_code, story_md, question_md, grade)
            hint_html = (
                f'<div class="rotom-hint"><strong>💡 Pista de Rotom Dex:</strong> '
                f'{html.escape(hint_text)}</div>'
            )

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
<article class="problem-card{reto_cls}" data-num="{num}" data-kind="{html.escape(kind_attr)}" data-subcat="{html.escape(subcat_code)}" data-sense="{html.escape(sense_attr)}">
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
  {diagram_html}
  {hint_html}
  <div class="workspace-box" aria-label="Espacio para operaciones">
    <div class="workspace-columns">
      <div class="workspace-col"><span class="workspace-col-title">Datos</span></div>
      <div class="workspace-col"><span class="workspace-col-title">Operación / Planteamiento</span></div>
      <div class="workspace-col"><span class="workspace-col-title">Respuesta y unidades</span></div>
    </div>
  </div>
</article>
"""
            rendered_cards.append(card_html)

        rendered_sections.append(
            f'<section class="problem-section" data-section-kind="{sec_kind}">\n'
            + "\n".join(rendered_cards)
            + "\n</section>"
        )

    # Renderizar Parte 2 (Solucionario)
    sol_html = ""
    if part2_raw:
        prot_sol, toks_sol = protect_math(part2_raw)
        md.reset()
        sol_converted = wrap_tables(restore_math(md.convert(prot_sol), toks_sol))
        sol_converted = wrap_cards(sol_converted, "solution-card", problem_meta=problem_meta)
        sol_html = f'\n<section id="solucionario" class="solutions-section">\n{sol_converted}\n</section>'

    # Renderizar intro curricular dentro de la Ficha del Profesor Oak
    intro_html = ""
    if intro_raw:
        prot_intro, toks_intro = protect_math(intro_raw)
        md.reset()
        intro_html = wrap_tables(restore_math(md.convert(prot_intro), toks_intro))

    oak_html = build_oak_dossier(
        intro_html=intro_html,
        by_sense=by_sense,
        by_subcat=by_subcat,
        total_problems=total_problems,
        badge=doc["badge"],
        grade=grade,
        by_contenido=by_contenido,
    )

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
  <strong>¡Misión de Entrenamiento!</strong> Lee cada historia con atención, organiza <em>Datos · Operación · Respuesta</em> en la cuadrícula y suma <strong>+1 EXP</strong> por cada reto superado.
</div>
"""

    return trainer_header + "\n".join(rendered_sections) + oak_html + sol_html


def wrap_cards(
    chunk: str,
    css_class: str,
    problem_meta: dict[int, dict[str, str]] | None = None,
) -> str:
    tokens = re.split(r"(<h3[^>]*>[\s\S]*?</h3>)", chunk)
    if len(tokens) <= 1:
        return chunk

    out = [tokens[0]]
    i = 1
    while i < len(tokens):
        h3 = tokens[i]
        body = tokens[i + 1] if i + 1 < len(tokens) else ""
        h3_text = re.sub(r"<[^>]+>", "", h3).strip()
        m_sol = re.match(r"^Soluci[óo]n\s+(Problema|al\s+Reto)\s+(\d+)\b", h3_text, flags=re.I)

        # No envolver encabezados divisorios de sección (ej. "### Soluciones — Subcategoría...")
        if not m_sol:
            if 'class="' in h3:
                styled_h3 = re.sub(r'class="([^"]*)"', r'class="\1 solutions-subcat-heading"', h3, count=1)
            else:
                styled_h3 = re.sub(r"^<h3\b", '<h3 class="solutions-subcat-heading"', h3, count=1)
            out.append(f"{styled_h3}{body}")
            i += 2
            continue

        num = int(m_sol.group(2))
        meta = (problem_meta or {}).get(num, {})
        kind_default = "reto" if "reto" in m_sol.group(1).lower() or num > 100 else "problema"
        meta_kind = meta.get("kind", kind_default)
        meta_subcat = meta.get("subcat", infer_subcat_code(num, meta_kind, ""))
        meta_sense = meta.get("sense", "|".join(infer_canonical_senses(num, "", "")))
        meta_cont = meta.get("contenido", "")

        split_end = re.split(r"(<h2[^>]*>|<hr\s*/?>)", body, maxsplit=1)
        card_body = split_end[0]
        trailing = "".join(split_end[1:]) if len(split_end) > 1 else ""

        contenido_html = ""
        if meta_cont:
            contenido_html = (
                f'\n<p class="sol-meta"><strong>Contenido específico:</strong> '
                f'{html.escape(meta_cont)}</p>'
            )
        reto_cls = " is-reto" if meta_kind == "reto" else ""
        attrs = (
            f'data-num="{num}" data-kind="{html.escape(meta_kind)}" '
            f'data-subcat="{html.escape(meta_subcat)}" data-sense="{html.escape(meta_sense)}"'
        )
        out.append(
            f'<article class="{css_class}{reto_cls}" {attrs}>\n'
            f'{h3}{contenido_html}{card_body}\n</article>{trailing}'
        )
        i += 2
    return "".join(out)


def render_page(
    title: str,
    body_html: str,
    is_problems: bool,
    is_index: bool = False,
    grade: int = 0,
) -> str:
    toggle_btns = ""
    filter_bar = ""
    if is_problems:
        toggle_btns = (
            '<button type="button" id="toggle-solutions" class="btn btn-toggle" '
            'onclick="toggleSolutions()">Modo Alumno (solo ejercicios)</button>'
            '<button type="button" id="toggle-workspaces" class="btn btn-toggle" '
            'onclick="toggleWorkspaces()">Ocultar cuadrículas</button>'
            '<button type="button" id="toggle-hints" class="btn btn-toggle" '
            'onclick="toggleHints()">Ocultar pistas</button>'
        )
        filter_bar = """
    <div class="toolbar-filters">
      <label class="filter-group">Subcategoría:
        <select id="filter-subcat" class="filter-select" onchange="onFilterInputChange()">
          <option value="all">Todas (1–120)</option>
          <option value="1">1. Numeración y valor posicional</option>
          <option value="2">2. Operaciones y cálculo</option>
          <option value="3">3. Medida, tiempo y dinero</option>
          <option value="4">4. Geometría y espacio</option>
          <option value="5">5. Patrones y álgebra</option>
          <option value="6">6. Datos, gráficos y azar</option>
          <option value="7">7. Combate, nivel y EXP</option>
          <option value="reto">Retos Especiales (101–120)</option>
        </select>
      </label>
      <label class="filter-group">Sentido LOMLOE:
        <select id="filter-sense" class="filter-select" onchange="onFilterInputChange()">
          <option value="all">Todos los sentidos</option>
          <option value="Sentido Numérico">Sentido Numérico</option>
          <option value="Sentido de la Medida">Sentido de la Medida</option>
          <option value="Sentido Espacial">Sentido Espacial</option>
          <option value="Sentido Algebraico">Sentido Algebraico</option>
          <option value="Sentido Estocástico">Sentido Estocástico</option>
        </select>
      </label>
      <label class="filter-group">Desde:
        <input type="number" id="filter-from" class="filter-input" min="1" max="120" value="1" oninput="onFilterInputChange()">
      </label>
      <label class="filter-group">Hasta:
        <input type="number" id="filter-to" class="filter-input" min="1" max="120" value="120" oninput="onFilterInputChange()">
      </label>
      <button type="button" id="btn-session-preset" class="btn btn-preset" onclick="applySessionPreset()">Ficha de sesión (5 ej.)</button>
      <button type="button" id="btn-filter-reset" class="btn" onclick="resetFilters()">Restablecer</button>
      <span id="filter-status" class="filter-status">120 / 120 ej.</span>
    </div>"""

    back_btn = "" if is_index else '<a class="btn" href="index.html">← Índice</a>'
    early_cls = " grade-early" if (is_problems and grade in (1, 2, 3)) else ""
    body_cls = ' class="grade-early"' if (is_problems and grade in (1, 2, 3)) else ""

    katex_head = """
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin="anonymous">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" crossorigin="anonymous"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" crossorigin="anonymous"
    onload="renderMathInElement(document.body, {delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}], throwOnError: false});"></script>
"""

    script_js = """
  <script>
    let sessionLimit = null;

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

    function toggleHints() {
      const hidden = document.body.classList.toggle('hide-hints');
      const btn = document.getElementById('toggle-hints');
      if (btn) {
        btn.classList.toggle('active', hidden);
        btn.textContent = hidden ? 'Mostrar pistas' : 'Ocultar pistas';
      }
    }

    function applyFilters() {
      const subcatEl = document.getElementById('filter-subcat');
      const senseEl = document.getElementById('filter-sense');
      const fromEl = document.getElementById('filter-from');
      const toEl = document.getElementById('filter-to');
      if (!subcatEl || !senseEl || !fromEl || !toEl) return;

      const subcatVal = subcatEl.value;
      const senseVal = senseEl.value;
      let fromNum = parseInt(fromEl.value, 10);
      let toNum = parseInt(toEl.value, 10);
      if (isNaN(fromNum) || fromNum < 1) fromNum = 1;
      if (isNaN(toNum) || toNum > 120) toNum = 120;
      if (fromNum > toNum) {
        const tmp = fromNum;
        fromNum = toNum;
        toNum = tmp;
      }

      const problemCards = Array.from(document.querySelectorAll('.problem-card'));
      const visibleNums = new Set();
      let shownCount = 0;

      problemCards.forEach((card) => {
        const num = parseInt(card.dataset.num || '0', 10);
        const kind = card.dataset.kind || '';
        const subcat = card.dataset.subcat || '';
        const senses = (card.dataset.sense || '').split('|').filter(Boolean);

        const matchSubcat =
          subcatVal === 'all' ||
          (subcatVal === 'reto' ? (subcat === 'reto' || kind === 'reto') : subcat === subcatVal);
        const matchSense = senseVal === 'all' || senses.includes(senseVal);
        const matchRange = num >= fromNum && num <= toNum;

        let show = matchSubcat && matchSense && matchRange;
        if (show && sessionLimit !== null && shownCount >= sessionLimit) {
          show = false;
        }

        card.classList.toggle('is-filtered-hidden', !show);
        if (show) {
          shownCount += 1;
          visibleNums.add(String(num));
        }
      });

      document.querySelectorAll('.solution-card').forEach((sol) => {
        const num = sol.dataset.num || '';
        sol.classList.toggle('is-filtered-hidden', !visibleNums.has(num));
      });

      document.querySelectorAll('.problem-section').forEach((sec) => {
        const hasVisible = sec.querySelector('.problem-card:not(.is-filtered-hidden)') !== null;
        sec.classList.toggle('is-filtered-hidden', !hasVisible);
      });

      document.querySelectorAll('.solutions-subcat-heading').forEach((hd) => {
        let el = hd.nextElementSibling;
        let hasVisibleSol = false;
        while (el && !el.classList.contains('solutions-subcat-heading')) {
          if (el.classList.contains('solution-card') && !el.classList.contains('is-filtered-hidden')) {
            hasVisibleSol = true;
            break;
          }
          el = el.nextElementSibling;
        }
        hd.classList.toggle('is-filtered-hidden', !hasVisibleSol);
      });

      const statusEl = document.getElementById('filter-status');
      if (statusEl) {
        statusEl.textContent = `${shownCount} / ${problemCards.length} ej.`;
      }
    }

    function onFilterInputChange() {
      sessionLimit = null;
      applyFilters();
    }

    function applySessionPreset() {
      sessionLimit = 5;
      applyFilters();
    }

    function resetFilters() {
      const subcatEl = document.getElementById('filter-subcat');
      const senseEl = document.getElementById('filter-sense');
      const fromEl = document.getElementById('filter-from');
      const toEl = document.getElementById('filter-to');
      if (subcatEl) subcatEl.value = 'all';
      if (senseEl) senseEl.value = 'all';
      if (fromEl) fromEl.value = '1';
      if (toEl) toEl.value = '120';
      sessionLimit = null;
      applyFilters();
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
<body{body_cls}>
  <header class="print-toolbar no-print">
    <div class="toolbar-main">
      <div class="toolbar-left">
        {back_btn}
        <span class="toolbar-title">{html.escape(title)}</span>
      </div>
      <div class="toolbar-actions">
        {toggle_btns}
        <button type="button" class="btn btn-primary" onclick="window.print()">Imprimir / Guardar PDF</button>
      </div>
    </div>{filter_bar}
  </header>
  <main class="page-container{early_cls}">
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
        <span class="badge-grade">1º a 6º Primaria</span>
      </div>
    </section>
    <p>Accede a cualquiera de los cuadernillos de entrenador (120 ejercicios ilustrados por curso con diagramas SVG, pistas opcionales de Rotom Dex, cuadrícula de operaciones NEAE, <strong>Ficha del Profesor Oak</strong> con rúbrica LOMLOE CE1–CE8 y solucionario paso a paso) o a las tablas de referencia.</p>
    <blockquote>
      <strong>Consejo de impresión:</strong> En cada cuadernillo puedes filtrar por subcategoría, sentido LOMLOE o rango (<em>«Ficha de sesión (5 ej.)»</em>), ocultar las pistas o activar el <em>«Modo Alumno (solo ejercicios)»</em> para imprimir fichas personalizadas en A4.
    </blockquote>

    <h2>Cuadernillos de Entrenador (720 ejercicios ilustrados)</h2>
    <div class="grid-cards">
      {"".join(cards[:6])}
    </div>

    <h2>Tablas de Referencia y Recursos</h2>
    <div class="grid-cards">
      {"".join(cards[6:])}
      <div class="doc-card">
        <div>
          <span class="doc-badge">Índice y Guía</span>
          <h3>Guía Maestra del Proyecto (README)</h3>
          <p>Mapeo curricular LOMLOE completo (1º a 6º de Primaria), estructura de carpetas y resumen pedagógico.</p>
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

        full_html = render_page(
            doc["title"],
            html_body,
            is_problems=doc["is_problems"],
            grade=doc.get("grade", 0),
        )
        out_path = OUT_DIR / doc["out"]
        out_path.write_text(full_html, encoding="utf-8")
        print(f"[OK] {out_path.name} ({out_path.stat().st_size // 1024} KB)")

    index_path = OUT_DIR / "index.html"
    index_path.write_text(build_index(), encoding="utf-8")
    print(f"[OK] {index_path.name} ({index_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
