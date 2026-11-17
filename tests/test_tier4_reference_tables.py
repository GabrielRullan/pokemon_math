"""
test_tier4_reference_tables.py - Tier 4: Technical & Mechanics Verification.

Verifies:
1. 'referencia_tabla_tipos.md':
   - Contains all 18 canonical Pokemon types in Spanish/English.
   - Contains complete 18x18 interaction matrix.
   - Documents damage multipliers (0x, 0.25x, 0.5x, 1x, 2x, 4x, and 1.5x STAB).
2. 'referencia_ps_evoluciones.md':
   - Documents the canonical HP calculation formula (Base, IV, EV, Level, +10).
   - Documents the canonical Shedinja HP=1 exception.
   - Documents multiple evolutionary lines with base HP progression tables.
3. 'guia_recursos_activos.md':
   - Documents verified PokeAPI endpoints (/pokemon, /pokemon-species, /type, /growth-rate).
   - Documents raw GitHub sprite CDN URLs (PokeAPI/sprites).
   - Documents Pokemon Showdown sprite paths (gen5/, ani/, types/).
   - Documents Veekun CSV database references on GitHub.
   - Contains non-commercial educational attribution and copyright notice (Art. 32 LPI / Fair Use).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

import pytest

from conftest import (
    CANONICAL_18_TYPES_EN,
    CANONICAL_18_TYPES_ES,
    extract_markdown_tables,
    extract_urls,
)


# ===========================================================================
# 1. Type Effectiveness Reference Document Tests
# ===========================================================================

def test_type_table_file_exists(type_table_path: Path):
    """Verifies that 'referencia_tabla_tipos.md' exists and is non-empty."""
    assert type_table_path.exists(), f"Reference file missing: {type_table_path.name}"
    assert type_table_path.stat().st_size > 500, (
        f"Reference file {type_table_path.name} is too small ({type_table_path.stat().st_size} bytes)."
    )


def test_type_table_contains_all_18_canonical_types(type_table_path: Path):
    """
    Verifies that all 18 canonical Pokemon types are documented in 'referencia_tabla_tipos.md'.
    """
    assert type_table_path.exists(), f"File missing: {type_table_path.name}"
    content = type_table_path.read_text(encoding="utf-8")

    missing_types = []
    for tipo_es, tipo_en in zip(CANONICAL_18_TYPES_ES, CANONICAL_18_TYPES_EN):
        # Match type name in Spanish (or English)
        pattern = rf"(?i)\b({re.escape(tipo_es)}|{re.escape(tipo_en)})\b"
        if not re.search(pattern, content):
            missing_types.append(f"{tipo_es} / {tipo_en}")

    assert not missing_types, (
        f"referencia_tabla_tipos.md is missing documentation for canonical types:\n"
        f"{missing_types}"
    )


def test_type_table_full_18x18_matrix_present(type_table_path: Path):
    """
    Verifies that 'referencia_tabla_tipos.md' contains an 18x18 interaction matrix.
    Looks for a markdown table with at least 18 rows or columns representing types.
    """
    assert type_table_path.exists(), f"File missing: {type_table_path.name}"
    content = type_table_path.read_text(encoding="utf-8")
    tables = extract_markdown_tables(content)

    matrix_found = False
    for table in tables:
        # Check if table dimensions match or exceed 18 types (e.g. 18+ rows or 18+ cols)
        num_rows = len(table)
        num_cols = len(table[0]) if num_rows > 0 else 0
        if num_rows >= 18 and num_cols >= 18:
            matrix_found = True
            break
        # Also support 19x19 if headers and labels are included
        if num_rows >= 18 and num_cols >= 10:
            # Check if row headers contain type names
            row_types = sum(
                1 for row in table if any(
                    any(t.lower() in cell.lower() for t in CANONICAL_18_TYPES_ES[:5])
                    for cell in row[:2]
                )
            )
            if row_types >= 10:
                matrix_found = True
                break

    assert matrix_found, (
        f"referencia_tabla_tipos.md does not contain a comprehensive 18-type interaction matrix. "
        f"Found {len(tables)} tables, but none with dimensions covering the 18 types."
    )


def test_type_table_documents_all_multipliers(type_table_path: Path):
    """
    Verifies that 'referencia_tabla_tipos.md' explicitly documents all standard multipliers:
    - 0x (Inmune / Sin efecto)
    - 0.25x / 1/4 (Doble resistencia)
    - 0.5x / 1/2 (Poco eficaz / Resistencia)
    - 1x (Daño normal / Neutro)
    - 2x (Súper eficaz)
    - 4x (Doble debilidad)
    - 1.5x (STAB - Same Type Attack Bonus)
    """
    assert type_table_path.exists(), f"File missing: {type_table_path.name}"
    content = type_table_path.read_text(encoding="utf-8")

    multiplier_checks = {
        "0x (Inmunidad)": r"(?:0\s*[x×]|inmun(?:idad|e)|sin\s+efecto)",
        "0.25x (Doble resistencia)": r"(?:0[,.]25\s*[x×]|1/4\s*[x×]?|cuarto|doble\s+resistencia)",
        "0.5x (Resistencia)": r"(?:0[,.]5\s*[x×]|1/2\s*[x×]?|½\s*[x×]?|poco\s+eficaz|resistencia)",
        "1x (Neutro)": r"(?:1\s*[x×]|daño\s+normal|neutr[ao])",
        "2x (Súper eficaz)": r"(?:2\s*[x×]|s[uú]per\s+eficaz|debilidad)",
        "4x (Doble debilidad)": r"(?:4\s*[x×]|doble\s+debilidad|cu[áa]druple)",
        "1.5x STAB": r"(?:1[,.]5\s*[x×]|stab|mismo\s+tipo)",
    }

    missing_multipliers = []
    for name, pattern in multiplier_checks.items():
        if not re.search(pattern, content, re.IGNORECASE):
            missing_multipliers.append(name)

    assert not missing_multipliers, (
        f"referencia_tabla_tipos.md is missing documentation for multipliers:\n"
        f"{missing_multipliers}"
    )


# ===========================================================================
# 2. HP & Evolution Progression Reference Document Tests
# ===========================================================================

def test_hp_evolution_file_exists(hp_evolution_path: Path):
    """Verifies that 'referencia_ps_evoluciones.md' exists and is non-empty."""
    assert hp_evolution_path.exists(), f"Reference file missing: {hp_evolution_path.name}"
    assert hp_evolution_path.stat().st_size > 500, (
        f"Reference file {hp_evolution_path.name} is too small ({hp_evolution_path.stat().st_size} bytes)."
    )


def test_hp_evolution_documents_canonical_formula(hp_evolution_path: Path):
    """
    Verifies that 'referencia_ps_evoluciones.md' documents the canonical Gen 3-9 HP formula:
    HP = floor(((2 * Base + IV + floor(EV / 4)) * Level) / 100) + Level + 10
    """
    assert hp_evolution_path.exists(), f"File missing: {hp_evolution_path.name}"
    content = hp_evolution_path.read_text(encoding="utf-8")

    # Check for presence of essential formula components
    has_base = bool(re.search(r"(?i)\b(2\s*[*·\u00d7]?\s*Base|Base\s*HP|PS\s*Base|BasePS)\b", content))
    has_iv = bool(re.search(r"(?i)\bIV\b", content))
    has_ev = bool(re.search(r"(?i)\b(EV|EV\s*/\s*4|EV/4)\b", content))
    has_level = bool(re.search(r"(?i)\b(Level|Nivel|L)\b", content))
    has_div_100 = bool(re.search(r"(?:/\s*100|\\frac\{[^}]+\}\{\s*100\s*\}|dividi(?:do|r)\s+entre\s+100)", content))
    has_plus_10 = bool(re.search(r"(?:\+\s*10|\+\s*L\s*\+\s*10|\+\s*Nivel\s*\+\s*10)", content))

    missing_components = []
    if not has_base:
        missing_components.append("2 * Base HP")
    if not has_iv:
        missing_components.append("IV (Individual Values)")
    if not has_ev:
        missing_components.append("EV / 4 (Effort Values)")
    if not has_level:
        missing_components.append("Level (L)")
    if not has_div_100:
        missing_components.append("Division by 100")
    if not has_plus_10:
        missing_components.append("+ Level + 10 constant term")

    assert not missing_components, (
        f"referencia_ps_evoluciones.md is missing canonical HP formula components:\n"
        f"{missing_components}"
    )


def test_hp_evolution_documents_shedinja_exception(hp_evolution_path: Path):
    """
    Verifies that 'referencia_ps_evoluciones.md' explicitly documents the Shedinja
    anomaly (always having exactly 1 HP regardless of level/IV/EV).
    """
    assert hp_evolution_path.exists(), f"File missing: {hp_evolution_path.name}"
    content = hp_evolution_path.read_text(encoding="utf-8")

    has_shedinja = bool(re.search(r"(?i)\bShedinja\b", content))
    has_one_hp = bool(re.search(r"(?i)(?:Shedinja[^\n.]*1\s*(?:PS|HP)|(?:PS|HP)[^\n.]*=.*1\b|1\s*punto\s+de\s+(?:salud|vida))", content))

    assert has_shedinja, "referencia_ps_evoluciones.md does not mention Shedinja."
    assert has_one_hp, "referencia_ps_evoluciones.md does not document that Shedinja has exactly 1 HP/PS."


def test_hp_evolution_covers_multiple_evolutionary_lines(hp_evolution_path: Path):
    """
    Verifies that 'referencia_ps_evoluciones.md' provides concrete Base HP progression tables
    across multiple representative evolutionary families (starters, common lines, high-HP tanks).
    """
    assert hp_evolution_path.exists(), f"File missing: {hp_evolution_path.name}"
    content = hp_evolution_path.read_text(encoding="utf-8")

    # Representative evolutionary species to check
    representative_species = [
        ("Charmander", "Charmeleon", "Charizard"),
        ("Bulbasaur", "Ivysaur", "Venusaur"),
        ("Squirtle", "Wartortle", "Blastoise"),
        ("Pikachu", "Raichu"),
        ("Magikarp", "Gyarados"),
        ("Gastly", "Haunter", "Gengar"),
        ("Happiny", "Chansey", "Blissey"),
    ]

    found_families = 0
    for family in representative_species:
        if all(re.search(rf"(?i)\b{member}\b", content) for member in family):
            found_families += 1

    assert found_families >= 3, (
        f"referencia_ps_evoluciones.md documents only {found_families} complete representative "
        f"evolution families; expected at least 3 distinct evolutionary lines."
    )


# ===========================================================================
# 3. Asset & Data Sourcing Guide Tests
# ===========================================================================

def test_sourcing_guide_file_exists(sourcing_guide_path: Path):
    """Verifies that 'guia_recursos_activos.md' exists and is non-empty."""
    assert sourcing_guide_path.exists(), f"Reference file missing: {sourcing_guide_path.name}"
    assert sourcing_guide_path.stat().st_size > 500, (
        f"Reference file {sourcing_guide_path.name} is too small ({sourcing_guide_path.stat().st_size} bytes)."
    )


def test_sourcing_guide_documents_pokeapi_endpoints(sourcing_guide_path: Path):
    """
    Verifies that 'guia_recursos_activos.md' documents verified PokeAPI REST endpoints:
    - /pokemon
    - /pokemon-species
    - /type
    - /growth-rate
    """
    assert sourcing_guide_path.exists(), f"File missing: {sourcing_guide_path.name}"
    content = sourcing_guide_path.read_text(encoding="utf-8")

    required_endpoints = [
        (r"/pokemon(?:/|\b)", "/pokemon"),
        (r"/pokemon-species", "/pokemon-species"),
        (r"/type(?:/|\b)", "/type"),
        (r"/growth-rate", "/growth-rate"),
    ]

    missing_endpoints = []
    for pattern, name in required_endpoints:
        if not re.search(pattern, content):
            missing_endpoints.append(name)

    assert not missing_endpoints, (
        f"guia_recursos_activos.md is missing PokeAPI endpoints: {missing_endpoints}"
    )


def test_sourcing_guide_documents_sprite_cdn_and_showdown_paths(sourcing_guide_path: Path):
    """
    Verifies that 'guia_recursos_activos.md' documents sprite assets from:
    1. PokeAPI Raw GitHub CDN (PokeAPI/sprites or raw.githubusercontent.com)
    2. Pokémon Showdown sprites CDN (play.pokemonshowdown.com) with subpaths (gen5/, ani/, types/)
    """
    assert sourcing_guide_path.exists(), f"File missing: {sourcing_guide_path.name}"
    content = sourcing_guide_path.read_text(encoding="utf-8")

    has_pokeapi_sprites = bool(
        re.search(r"(?:raw\.githubusercontent\.com/PokeAPI/sprites|PokeAPI/sprites)", content)
    )
    has_showdown = bool(re.search(r"pokemonshowdown\.com", content))
    has_showdown_paths = bool(
        re.search(r"(?:gen5/|gen5ani/|ani/|types/)", content)
    )

    assert has_pokeapi_sprites, (
        "guia_recursos_activos.md does not document PokeAPI Raw GitHub sprite CDN."
    )
    assert has_showdown and has_showdown_paths, (
        "guia_recursos_activos.md does not document Pokémon Showdown sprite subdirectories (gen5/, ani/, types/)."
    )


def test_sourcing_guide_documents_veekun_csv_database(sourcing_guide_path: Path):
    """
    Verifies that 'guia_recursos_activos.md' references the Veekun relational CSV database.
    """
    assert sourcing_guide_path.exists(), f"File missing: {sourcing_guide_path.name}"
    content = sourcing_guide_path.read_text(encoding="utf-8")

    has_veekun = bool(re.search(r"(?i)\bveekun\b", content))
    assert has_veekun, "guia_recursos_activos.md does not document Veekun CSV database."


def test_sourcing_guide_contains_legal_educational_attribution(sourcing_guide_path: Path):
    """
    Verifies that 'guia_recursos_activos.md' includes a legal disclaimer regarding
    non-commercial educational fair use (Art. 32 LPI / Fair Use) and IP attribution
    (Nintendo / Creatures Inc. / GAME FREAK).
    """
    assert sourcing_guide_path.exists(), f"File missing: {sourcing_guide_path.name}"
    content = sourcing_guide_path.read_text(encoding="utf-8")

    has_educational_fair_use = bool(
        re.search(r"(?i)(?:art[íi]culo\s*32|art\.\s*32|lpi|fair\s*use|uso\s+educativo|sin\s+[áa]nimo\s+de\s+lucro|fines\s+educativos)", content)
    )
    has_ip_attribution = bool(
        re.search(r"(?i)(?:Nintendo|GAME\s*FREAK|Creatures|The\s+Pok[ée]mon\s+Company)", content)
    )

    assert has_educational_fair_use, (
        "guia_recursos_activos.md lacks educational fair use / Art. 32 LPI legal disclaimer."
    )
    assert has_ip_attribution, (
        "guia_recursos_activos.md lacks IP attribution to Nintendo / Game Freak / Creatures."
    )
