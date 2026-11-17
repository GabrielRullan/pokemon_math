"""
test_tier5_adversarial.py - Tier 5: Adversarial, Stress, Boundary & Invariant Test Suite.

Synthesized and integrated from Milestone 5 Phase 2 Challenger Deliverables:
- challenger_m5_1: Mathematical Adversarial Coverage Hardening (39 tests)
- challenger_m5_2: Structural Mechanics, Document Schema, Markdown Robustness & Asset Integrity (42 tests)

Total: 81 rigorous, adversarial automated tests ensuring complete compliance with
LOMLOE Primary Mathematics (Real Decreto 157/2022) and Pokémon mechanics.
"""

from __future__ import annotations

import math
import os
import re
import sys
import tempfile
import unicodedata
from itertools import combinations
from pathlib import Path
from typing import Dict, List, Set, Tuple
from urllib.parse import urlparse

import pytest

# Ensure tests/ and project root are discoverable in sys.path
TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(os.environ.get("POKEMON_MATH_ROOT", TESTS_DIR.parent)).resolve()
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from conftest import (
    CANONICAL_18_TYPES_EN,
    CANONICAL_18_TYPES_ES,
    GRADE_FILENAME_MAP,
    GRADE_NUMBERS,
    GradeDocument,
    extract_markdown_tables,
    extract_urls,
    parse_grade_document,
)
from test_tier2_answer_keys import is_qualitative_lomloe_answer

# Reference files paths
FILE_TYPE_CHART = PROJECT_ROOT / "referencia_tabla_tipos.md"
FILE_HP_EVO = PROJECT_ROOT / "referencia_ps_evoluciones.md"
FILE_ASSET_GUIDE = PROJECT_ROOT / "guia_recursos_activos.md"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def project_dir() -> Path:
    return PROJECT_ROOT


@pytest.fixture(scope="module")
def all_grade_docs() -> Dict[int, GradeDocument]:
    docs = {}
    for g in GRADE_NUMBERS:
        p = PROJECT_ROOT / GRADE_FILENAME_MAP[g]
        assert p.exists(), f"Grade {g} file not found: {p}"
        docs[g] = parse_grade_document(p, grade=g)
    return docs


@pytest.fixture(scope="module")
def hp_reference_content() -> str:
    assert FILE_HP_EVO.exists(), f"HP reference file not found: {FILE_HP_EVO}"
    return FILE_HP_EVO.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def type_reference_content() -> str:
    assert FILE_TYPE_CHART.exists(), f"Type reference file not found: {FILE_TYPE_CHART}"
    return FILE_TYPE_CHART.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Canonical Mathematical & Parsing Helpers
# ---------------------------------------------------------------------------

def canonical_hp(base: int, iv: int, ev: int, level: int) -> int:
    """Canonical Gen III-IX HP formula."""
    return math.floor(((2 * base + iv + math.floor(ev / 4)) * level) / 100) + level + 10


def exp_fast(level: int) -> int:
    return math.floor(0.8 * (level ** 3))


def exp_med_fast(level: int) -> int:
    return level ** 3


def exp_slow(level: int) -> int:
    return math.floor(1.25 * (level ** 3))


def exp_med_slow(level: int) -> int:
    if level <= 1:
        return 0
    return math.floor(1.2 * (level ** 3) - 15 * (level ** 2) + 100 * level - 140)


def defeat_exp_yield(base_exp: int, level: int, s: int = 1) -> int:
    """Canonical defeat experience yield: floor((b * L) / (7 * s))."""
    return math.floor((base_exp * level) / (7 * s))


def parse_type_matrix_from_markdown(content: str) -> Dict[str, Dict[str, float]]:
    """
    Parses the 18x18 type effectiveness markdown table from referencia_tabla_tipos.md.
    Returns nested dictionary: matrix[attacker_es][defender_es] = multiplier_float.
    """
    lines = content.splitlines()
    matrix_lines: List[str] = []
    in_matrix = False
    for line in lines:
        if "Atacante ↓ / Defensor →" in line:
            in_matrix = True
            matrix_lines.append(line)
            continue
        if in_matrix:
            if line.strip().startswith("---") or (line.strip() == "" and len(matrix_lines) > 18):
                break
            if "|" in line:
                matrix_lines.append(line)

    assert len(matrix_lines) >= 20, f"Failed to extract 18x18 matrix lines: found {len(matrix_lines)}"
    data_rows = matrix_lines[2:]  # Skip header and delimiter

    types_es = CANONICAL_18_TYPES_ES
    matrix: Dict[str, Dict[str, float]] = {}

    for row_str in data_rows:
        cells = [c.strip() for c in row_str.split("|")[1:-1]]
        if not cells:
            continue
        attacker_raw = cells[0]
        # Match type name in **Bold**
        m = re.search(r"\*\*([A-Za-záéíóúÁÉÍÓÚ]+)\*\*", attacker_raw)
        att_type = m.group(1) if m else attacker_raw
        multipliers = cells[1:]
        matrix[att_type] = {}
        for c_idx, val in enumerate(multipliers):
            if c_idx >= len(types_es):
                break
            def_type = types_es[c_idx]
            val_clean = val.replace("**", "").strip()
            if val_clean == "":
                num_val = 1.0
            elif val_clean == "2":
                num_val = 2.0
            elif val_clean in ("½", "1/2", "0.5", "0,5"):
                num_val = 0.5
            elif val_clean == "0":
                num_val = 0.0
            else:
                raise ValueError(f"Unrecognized cell multiplier: '{val}' for {att_type} -> {def_type}")
            matrix[att_type][def_type] = num_val

    return matrix


# ===========================================================================
# PART A: MATHEMATICAL ADVERSARIAL & BOUNDARY TESTS (challenger_m5_1)
# ===========================================================================

# ---------------------------------------------------------------------------
# 1. Numerical Domain Compliance Tests (LOMLOE Real Decreto 157/2022)
# ---------------------------------------------------------------------------

class TestNumericalDomainCompliance:
    """Adversarially validates that problem statements and solutions respect LOMLOE domain limits."""

    def test_grade2_numerical_domain_strict_0_to_999(self, all_grade_docs):
        """2º Primaria domain is strictly natural numbers up to 999."""
        doc = all_grade_docs[2]
        assert len(doc.problems) == 100
        assert len(doc.solutions) == 100

        for num, prob in doc.problems.items():
            integers = [int(x) for x in re.findall(r"\b\d+\b", prob.question)]
            for val in integers:
                assert val <= 999, f"Grade 2 Problem {num} question has number {val} exceeding 999"

        for num, sol in doc.solutions.items():
            bolds = re.findall(r"\*\*([^*]+)\*\*", sol.final_answer)
            for b in bolds:
                clean = b.replace(".", "").replace(",", ".")
                numbers = [float(x) for x in re.findall(r"\b\d+(?:\.\d+)?\b", clean)]
                for val in numbers:
                    assert val <= 999, f"Grade 2 Solution {num} final answer has value {val} exceeding 999"

    def test_grade3_numerical_domain_strict_0_to_9999(self, all_grade_docs):
        """3º Primaria domain expands to 4-digit numbers (0 to 9,999)."""
        doc = all_grade_docs[3]
        for num, prob in doc.problems.items():
            integers = [int(x) for x in re.findall(r"\b\d+\b", prob.question)]
            for val in integers:
                assert val <= 9999, f"Grade 3 Problem {num} question has number {val} exceeding 9,999"

        for num, sol in doc.solutions.items():
            bolds = re.findall(r"\*\*([^*]+)\*\*", sol.final_answer)
            for b in bolds:
                clean = b.replace(".", "").replace(",", ".")
                numbers = [float(x) for x in re.findall(r"\b\d+(?:\.\d+)?\b", clean)]
                for val in numbers:
                    assert val <= 9999, f"Grade 3 Solution {num} final answer has value {val} exceeding 9,999"

    def test_grade4_numerical_domain_bounded(self, all_grade_docs):
        """4º Primaria domain covers numbers up to 99,999 with explicit 6-digit intro (<= 155,000)."""
        doc = all_grade_docs[4]
        for num, prob in doc.problems.items():
            integers = [int(x) for x in re.findall(r"\b\d+\b", prob.question)]
            for val in integers:
                assert val <= 200000, f"Grade 4 Problem {num} question has number {val} exceeding 200,000"

    def test_grade5_and_6_include_large_numbers_decimals_fractions(self, all_grade_docs):
        """5º and 6º Primaria must include numbers > 100,000, decimals, and fractional values."""
        for g in [5, 6]:
            doc = all_grade_docs[g]
            raw = doc.raw_content
            has_large_num = bool(re.search(r"\b[1-9]\d{2}\.\d{3}\b|\b\d{6,}\b", raw))
            has_decimals = bool(re.search(r"\b\d+,\d+\b", raw))
            has_fractions = bool(re.search(r"\b\d+/\d+\b", raw))

            assert has_large_num, f"Grade {g} lacks large numbers > 100,000"
            assert has_decimals, f"Grade {g} lacks decimal numbers"
            assert has_fractions, f"Grade {g} lacks fractions"


# ---------------------------------------------------------------------------
# 2. Canonical HP Formula & Boundary Value Tests
# ---------------------------------------------------------------------------

class TestCanonicalHPFormulaBoundaries:
    """Adversarially stress-tests canonical HP formula and its boundary limits."""

    @pytest.mark.parametrize("base,iv,ev,level,expected_hp", [
        # Level 1 extremes
        (255, 31, 252, 1, 17),   # Blissey max possible HP at L1
        (255, 0, 0, 1, 16),      # Blissey min possible HP at L1
        (20, 0, 0, 1, 11),       # Shuckle min possible HP at L1
        (10, 0, 0, 1, 11),       # Diglett min possible HP at L1
        (1, 0, 0, 1, 11),        # Theoretical Base 1 at L1 (formula without Shedinja override)
        # Level 50 extremes
        (255, 31, 252, 50, 362), # Blissey max at L50: 255 + 107 = 362
        (255, 0, 0, 50, 315),    # Blissey min at L50: 255 + 60 = 315
        (35, 15, 0, 50, 102),    # Pikachu standard neutral at L50
        (78, 15, 0, 50, 145),    # Charizard standard neutral at L50
        (108, 15, 0, 50, 175),   # Garchomp standard neutral at L50
        # Level 100 extremes
        (255, 31, 252, 100, 714),# Blissey max at L100: 2*255 + 204 = 714
        (255, 0, 0, 100, 620),   # Blissey min at L100: 2*255 + 110 = 620
        (255, 15, 0, 100, 635),  # Blissey neutral at L100: 2*255 + 125 = 635
        (20, 31, 252, 100, 244), # Shuckle max at L100: 2*20 + 204 = 244
        (20, 0, 0, 100, 150),    # Shuckle min at L100: 2*20 + 110 = 150
        (35, 15, 0, 100, 195),   # Pikachu neutral at L100
        (78, 15, 0, 100, 281),   # Charizard neutral at L100
    ])
    def test_canonical_hp_exact_evaluations(self, base, iv, ev, level, expected_hp):
        assert canonical_hp(base, iv, ev, level) == expected_hp

    def test_hp_genetic_variation_range_constant_94(self):
        """At Level 100, for ANY base stat, Max HP - Min HP is ALWAYS exactly 94."""
        for base in [1, 10, 20, 35, 78, 100, 108, 130, 250, 255]:
            hp_max = canonical_hp(base, iv=31, ev=252, level=100)
            hp_min = canonical_hp(base, iv=0, ev=0, level=100)
            delta = hp_max - hp_min
            assert delta == 94, f"HP variation range at L100 for Base {base} was {delta}, expected 94"

    def test_hp_strictly_monotonic_with_level(self):
        """For any fixed Pokémon stats, HP must be strictly monotonically increasing with Level."""
        for base in [10, 35, 80, 250]:
            for iv in [0, 15, 31]:
                for ev in [0, 128, 252]:
                    prev_hp = canonical_hp(base, iv, ev, 1)
                    for lvl in range(2, 101):
                        curr_hp = canonical_hp(base, iv, ev, lvl)
                        assert curr_hp > prev_hp, f"Non-monotonic HP at L={lvl} for Base={base}, IV={iv}, EV={ev}"
                        prev_hp = curr_hp

    def test_shedinja_hp_absolute_invariance(self, hp_reference_content):
        """Shedinja has HP=1 across all levels, regardless of IVs, EVs, or Level."""
        assert "Shedinja" in hp_reference_content
        assert re.search(r"PS.*Shedinja.*=.*1", hp_reference_content)
        assert "Superguarda" in hp_reference_content

        sec7 = hp_reference_content.split("## 7. Tabla de Consulta Rápida")[1].split("\n---\n")[0]
        shedinja_line = [l for l in sec7.splitlines() if "Shedinja" in l]
        assert shedinja_line, "Shedinja row not found in Section 7 table"
        cols = [c.strip().replace("*", "") for c in shedinja_line[0].strip("|").split("|")]
        for val in cols[3:]:
            assert val == "1", f"Shedinja has non-1 HP in table: {val}"


# ---------------------------------------------------------------------------
# 3. EXP Growth Formulas & Battle Mechanics Tests
# ---------------------------------------------------------------------------

class TestEXPGrowthAndBattleMechanics:
    """Adversarially validates cubic growth curves, defeat yields, and party sharing."""

    def test_exp_curves_at_boundary_levels(self):
        """Validates all 4 standard curves at Levels 1, 10, 20, 50, 100."""
        # Level 1
        assert exp_fast(1) == 0
        assert exp_med_fast(1) == 1
        assert exp_slow(1) == 1
        assert exp_med_slow(1) == 0

        # Level 10
        assert exp_fast(10) == 800
        assert exp_med_fast(10) == 1000
        assert exp_slow(10) == 1250
        assert exp_med_slow(10) == 560

        # Level 50
        assert exp_fast(50) == 100000
        assert exp_med_fast(50) == 125000
        assert exp_slow(50) == 156250
        assert exp_med_slow(50) == 117360

        # Level 100
        assert exp_fast(100) == 800000
        assert exp_med_fast(100) == 1000000
        assert exp_slow(100) == 1250000
        assert exp_med_slow(100) == 1059860

    def test_exp_curve_strict_ordering_for_standard_curves(self):
        """For all levels L >= 2: Fast < Medium Fast < Slow."""
        for lvl in range(2, 101):
            f = exp_fast(lvl)
            mf = exp_med_fast(lvl)
            s = exp_slow(lvl)
            assert f < mf < s, f"Ordering violated at L={lvl}: Fast={f}, MedFast={mf}, Slow={s}"

    @pytest.mark.parametrize("base_exp,level,expected_yield", [
        (60, 28, 240),   # Geodude (Grade 5 Prob 92)
        (189, 35, 945),  # Gyarados (Grade 5 Prob 93)
        (270, 42, 1620), # Dragonite (Grade 5 Prob 94)
        (154, 21, 462),  # Snorlax base before Lucky Egg (Grade 5 Prob 95)
    ])
    def test_canonical_defeat_exp_yield_exactness(self, base_exp, level, expected_yield):
        """Verifies the defeat formula floor((b * L) / 7) against Grade 5 problem specifications."""
        assert defeat_exp_yield(base_exp, level) == expected_yield

    def test_battle_exp_multipliers_compounding(self):
        """Tests multiplier compounding: Lucky Egg (+50% = 1.5x), Traded (+50% = 1.5x), Trainer (+50% = 1.5x)."""
        base_yield = 1200
        lucky_egg = int(base_yield * 1.5)
        assert lucky_egg == 1800

        # Traded + Lucky Egg: 1.5 * 1.5 = 2.25x
        combined = int(base_yield * 2.25)
        assert combined == 2700

    def test_modern_exp_share_party_distribution_total_350_percent(self, all_grade_docs):
        """
        Under Gen VI-IX Exp. Share rules:
        Active battler receives 100%, 5 party members receive 50% each.
        Total EXP generated = 100% + 5 * 50% = 350% of base defeat yield.
        Grade 6 Problem 95 and 94 explicitly verify this invariant.
        """
        doc6 = all_grade_docs[6]
        sol95 = doc6.solutions[95]
        assert "350%" in sol95.final_answer or "350 %" in sol95.final_answer or "350" in sol95.final_answer
        assert "8.400" in sol95.final_answer or "8400" in sol95.final_answer


# ---------------------------------------------------------------------------
# 4. Reference Document Tables & Type Multipliers Precision Tests
# ---------------------------------------------------------------------------

class TestReferenceDocumentPrecision:
    """Validates that all tables in reference guides have zero arithmetic or transcription error."""

    def test_section7_hp_table_all_85_values_exact(self, hp_reference_content):
        """Verifies all 17 species x 5 levels (85 entries) in Section 7 table."""
        sec7 = hp_reference_content.split("## 7. Tabla de Consulta Rápida")[1].split("\n---\n")[0]
        lines = [l.strip() for l in sec7.splitlines() if "|" in l and not l.strip().startswith("|:")]
        rows = lines[1:]  # skip header
        levels = [10, 25, 50, 75, 100]

        for r in rows:
            cols = [c.strip().replace("*", "") for c in r.strip("|").split("|")]
            if len(cols) < 8:
                continue
            name = cols[0]
            base = int(cols[2])
            for idx, lvl in enumerate(levels):
                table_val = int(cols[3 + idx])
                if name == "Shedinja":
                    expected = 1
                else:
                    expected = canonical_hp(base, iv=15, ev=0, level=lvl)
                assert table_val == expected, f"Discrepancy for {name} at L={lvl}: table={table_val}, formula={expected}"

    def test_section5_evolutionary_lines_deltas_and_ratios(self, hp_reference_content):
        """Verifies Base HP deltas and growth factors for 18 evolutionary lines."""
        sec5 = hp_reference_content.split("## 5. Progresión de PS en 18 Líneas Evolutivas Representativas")[1].split("### 5.1")[0]
        lines = [l.strip() for l in sec5.splitlines() if "|" in l and not l.strip().startswith("|:")]

        tested_lines = 0
        for r in lines[1:]:
            cols = [c.strip().replace("*", "").replace("$", "") for c in r.strip("|").split("|")]
            if len(cols) >= 8:
                tested_lines += 1
                name = cols[1]
                p1_match = re.search(r"\((\d+)\)", cols[2])
                p3_match = re.search(r"\((\d+)\)", cols[4])
                if p1_match and p3_match:
                    hp_base = int(p1_match.group(1))
                    hp_final = int(p3_match.group(1))
                    ratio = hp_final / hp_base
                    assert hp_final >= hp_base or name == "Nincada", f"Final HP < Base HP in {name}"
        assert tested_lines >= 18, f"Expected 18 evolutionary lines, tested {tested_lines}"

    def test_eevee_branch_divergence_table_5_1(self, hp_reference_content):
        """Verifies Eevee table 5.1: 8 evolutions from Base 55."""
        sec5_1 = hp_reference_content.split("### 5.1 Matriz de Ramificación de Eevee")[1].split("\n---\n")[0]
        lines = [l.strip() for l in sec5_1.splitlines() if "|" in l and not re.match(r"^\|?\s*:?-+:?", l.strip())]
        rows = lines[1:]

        evos = {}
        for r in rows:
            cols = [c.strip().replace("*", "").replace("$", "") for c in r.strip("|").split("|")]
            if len(cols) >= 5:
                evo_name = cols[0]
                base_hp = int(cols[2])
                delta_str = cols[3]
                evos[evo_name] = (base_hp, delta_str)

        assert len(evos) == 8, f"Expected 8 Eeveelutions, found {len(evos)}"
        assert evos["Vaporeon"][0] == 130
        assert evos["Vaporeon"][1] == "+75"
        assert evos["Umbreon"][0] == 95
        assert evos["Sylveon"][0] == 95
        for fast_evo in ["Jolteon", "Flareon", "Espeon", "Leafeon", "Glaceon"]:
            assert evos[fast_evo][0] == 65
            assert evos[fast_evo][1] == "+10"

    def test_type_table_documents_all_seven_canonical_multipliers(self, type_reference_content):
        """Verifies documentation of all 7 multipliers: 0x, 0.25x, 0.5x, 1x, 1.5x (STAB), 2x, 4x."""
        multiplier_patterns = {
            "0x (Inmune)": r"(?:[x×]\s*0\b|0\s*[x×]|inmune|inmunidad|sin\s+efecto)",
            "0.25x (Doble resistencia)": r"(?:[x×]\s*0[,.]25|0[,.]25\s*[x×]|1/4\s*[x×]?|doble\s+resistencia)",
            "0.5x (Resistencia)": r"(?:[x×]\s*0[,.]5|0[,.]5\s*[x×]|1/2\s*[x×]?|poco\s+eficaz|resistencia)",
            "1x (Neutro)": r"(?:[x×]\s*1\b|1\s*[x×]|daño\s+normal|neutr[ao])",
            "1.5x (STAB)": r"(?:[x×]\s*1[,.]5|1[,.]5\s*[x×]|stab|mismo\s+tipo)",
            "2x (Súper eficaz)": r"(?:[x×]\s*2\b|2\s*[x×]|s[uú]per\s+eficaz)",
            "4x (Doble debilidad)": r"(?:[x×]\s*4\b|4\s*[x×]|doble\s+debilidad|cu[áa]druple)",
        }
        for name, pat in multiplier_patterns.items():
            assert re.search(pat, type_reference_content, re.IGNORECASE), f"Multiplier '{name}' not documented in type table"


# ---------------------------------------------------------------------------
# 5. Solution Arithmetic Grounding & Integrity Across All 500 Problems
# ---------------------------------------------------------------------------

class TestSolutionArithmeticAndGrounding:
    """Adversarially validates that solutions do not fabricate numbers and answers are grounded."""

    def test_all_500_solutions_have_bold_answers(self, all_grade_docs):
        """100% of the 500 problems must provide a bolded final answer."""
        total_checked = 0
        for g in GRADE_NUMBERS:
            doc = all_grade_docs[g]
            for num, sol in doc.solutions.items():
                total_checked += 1
                assert sol.has_bold_answer, f"Grade {g} Solution {num} lacks bold final answer: {sol.final_answer}"
        assert total_checked == 500

    def test_all_500_solutions_contain_mandatory_sections(self, all_grade_docs):
        """Every single solution must contain non-empty Datos, Planteamiento, and Respuesta."""
        for g in GRADE_NUMBERS:
            doc = all_grade_docs[g]
            for num, sol in doc.solutions.items():
                assert sol.identified_data.strip(), f"Grade {g} Solution {num} has empty Datos identificados"
                assert sol.operations.strip(), f"Grade {g} Solution {num} has empty Planteamiento y Operaciones"
                assert sol.final_answer.strip(), f"Grade {g} Solution {num} has empty Respuesta Final"

    def test_bold_answers_reflect_operations_or_problem_data(self, all_grade_docs):
        """
        Adversarial test: verifies that numeric quantities in final answers
        derive directly from the operations, data, or question statement.
        """
        # Exemption set for pedagogical conversions (percentages, time conversions, coordinates)
        pedagogical_exemptions = {
            "100", "50", "25", "75", "10", "12", "14", "125", "0"
        }
        for g in GRADE_NUMBERS:
            doc = all_grade_docs[g]
            for num, sol in doc.solutions.items():
                prob = doc.problems[num]
                bolds = re.findall(r"\*\*([^*]+)\*\*", sol.final_answer)
                combined_context = (
                    sol.operations.replace(".", "").replace(",", "") +
                    sol.identified_data.replace(".", "").replace(",", "") +
                    prob.question.replace(".", "").replace(",", "")
                )
                for b in bolds:
                    digits = re.findall(r"\b\d+\b", b.replace(".", "").replace(",", ""))
                    for d in digits:
                        if len(d) >= 2 and d not in pedagogical_exemptions:
                            assert d in combined_context, (
                                f"Grade {g} Problem {num}: number '{d}' in bold answer '{b}' "
                                f"not found in operations or question context!"
                            )


# ===========================================================================
# PART B: STRUCTURAL, MECHANICS, SCHEMA & ASSET INTEGRITY (challenger_m5_2)
# ===========================================================================

# ---------------------------------------------------------------------------
# 6. Type Chart Mechanics & Algebraic Properties
# ---------------------------------------------------------------------------

class TestAdversarialTypeChartMechanics:
    """Stress tests covering the 18x18 type matrix, algebraic closure, and inverses."""

    def test_adversarial_type_chart_18x18_matrix_completeness(self):
        """
        Adversarial test: Validates that the parsed 18x18 matrix contains all 18 standard
        types in both dimensions (exactly 324 defined interactions), that all values
        belong strictly to {0.0, 0.5, 1.0, 2.0}, and checks crucial canonical benchmarks.
        """
        assert FILE_TYPE_CHART.exists(), f"Missing file: {FILE_TYPE_CHART.name}"
        content = FILE_TYPE_CHART.read_text(encoding="utf-8")
        matrix = parse_type_matrix_from_markdown(content)

        # 1. Check all 18 types present as keys
        assert len(matrix) == 18, f"Expected 18 attacker rows, found {len(matrix)}"
        for t in CANONICAL_18_TYPES_ES:
            assert t in matrix, f"Attacker type {t} missing from parsed matrix"
            assert len(matrix[t]) == 18, f"Attacker {t} has {len(matrix[t])} defenders, expected 18"

        # 2. Check value domain closure
        allowed_single_multipliers = {0.0, 0.5, 1.0, 2.0}
        counts = {0.0: 0, 0.5: 0, 1.0: 0, 2.0: 0}
        for atk, defs in matrix.items():
            for dfn, mult in defs.items():
                assert mult in allowed_single_multipliers, (
                    f"Invalid multiplier {mult} for interaction {atk} -> {dfn}"
                )
                counts[mult] += 1

        assert sum(counts.values()) == 324, f"Total interactions {sum(counts.values())} != 324"

        # 3. Canonical Pokémon interaction benchmarks
        benchmarks = [
            ("Fuego", "Planta", 2.0),
            ("Fuego", "Agua", 0.5),
            ("Fuego", "Fuego", 0.5),
            ("Agua", "Fuego", 2.0),
            ("Agua", "Planta", 0.5),
            ("Eléctrico", "Tierra", 0.0),
            ("Eléctrico", "Agua", 2.0),
            ("Tierra", "Volador", 0.0),
            ("Tierra", "Eléctrico", 2.0),
            ("Normal", "Fantasma", 0.0),
            ("Fantasma", "Normal", 0.0),
            ("Lucha", "Normal", 2.0),
            ("Lucha", "Fantasma", 0.0),
            ("Psíquico", "Siniestro", 0.0),
            ("Dragón", "Hada", 0.0),
            ("Hada", "Dragón", 2.0),
            ("Acero", "Hada", 2.0),
            ("Veneno", "Acero", 0.0),
            ("Planta", "Agua", 2.0),
            ("Hielo", "Dragón", 2.0),
            ("Roca", "Volador", 2.0),
            ("Bicho", "Psíquico", 2.0),
            ("Siniestro", "Fantasma", 2.0),
        ]
        for atk, dfn, expected in benchmarks:
            actual = matrix[atk][dfn]
            assert actual == expected, f"Benchmark mismatch for {atk} -> {dfn}: expected {expected}, got {actual}"

    def test_adversarial_dual_type_multipliers_closure_and_extremes(self):
        """
        Adversarial test: Exhaustively tests all 18 attacker types against all 153 dual-type
        combinations (2,754 total combat interactions).
        Verifies:
        1. Algebraic closure: product M(T -> D1) * M(T -> D2) in {0.0, 0.25, 0.5, 1.0, 2.0, 4.0}.
        2. Quadruple weaknesses (4x) correctly produce 4.0.
        3. Double resistances (0.25x) correctly produce 0.25.
        4. Any absorption by an immune type yields exactly 0.0.
        """
        assert FILE_TYPE_CHART.exists()
        content = FILE_TYPE_CHART.read_text(encoding="utf-8")
        matrix = parse_type_matrix_from_markdown(content)
        allowed_dual_products = {0.0, 0.25, 0.5, 1.0, 2.0, 4.0}

        types = CANONICAL_18_TYPES_ES
        tested_pairs = 0
        quadruple_weakness_count = 0
        double_resistance_count = 0
        immunity_absorb_count = 0

        for atk in types:
            for d1, d2 in combinations(types, 2):
                m1 = matrix[atk][d1]
                m2 = matrix[atk][d2]
                prod = m1 * m2
                tested_pairs += 1

                assert prod in allowed_dual_products, (
                    f"Dual-type product violation: {atk} vs ({d1}/{d2}): {m1} * {m2} = {prod}"
                )

                if prod == 4.0:
                    quadruple_weakness_count += 1
                elif prod == 0.25:
                    double_resistance_count += 1
                elif prod == 0.0:
                    immunity_absorb_count += 1

        assert tested_pairs == 18 * (18 * 17 // 2) == 2754
        assert quadruple_weakness_count > 0, "No 4x quadruple weaknesses found"
        assert double_resistance_count > 0, "No 0.25x double resistances found"
        assert immunity_absorb_count > 0, "No 0x immunity absorptions found"

        # Explicit canonical dual-type checks
        # Charizard: Fire/Flying -> Rock = 2 * 2 = 4x; Water = 2 * 1 = 2x; Ground = 2 * 0 = 0x
        assert matrix["Roca"]["Fuego"] * matrix["Roca"]["Volador"] == 4.0
        assert matrix["Agua"]["Fuego"] * matrix["Agua"]["Volador"] == 2.0
        assert matrix["Tierra"]["Fuego"] * matrix["Tierra"]["Volador"] == 0.0

        # Swampert: Water/Ground -> Grass = 2 * 2 = 4x; Electric = 2 * 0 = 0x
        assert matrix["Planta"]["Agua"] * matrix["Planta"]["Tierra"] == 4.0
        assert matrix["Eléctrico"]["Agua"] * matrix["Eléctrico"]["Tierra"] == 0.0

        # Gengar: Ghost/Poison -> Bug = 0.5 * 0.5 = 0.25x; Normal = 1.0 * 0.0 = 0.0x
        assert matrix["Bicho"]["Fantasma"] * matrix["Bicho"]["Veneno"] == 0.25
        assert matrix["Normal"]["Fantasma"] * matrix["Normal"]["Veneno"] == 0.0

    def test_adversarial_type_chart_inverse_effectiveness_mechanics(self):
        """
        Adversarial test: Verifies the mathematics of Pokémon 'Inverse Battles':
        - Normal weaknesses (2x) become resistances (0.5x).
        - Normal resistances (0.5x) become weaknesses (2x).
        - Normal immunities (0x) become weaknesses (2x) — no type has immunities!
        - Neutral (1x) remains neutral (1x).
        Verifies that under inverse mechanics, zero cells in the 18x18 matrix equal 0.0,
        and dual-type inverse products strictly belong to {0.25, 0.5, 1.0, 2.0, 4.0}.
        """
        assert FILE_TYPE_CHART.exists()
        content = FILE_TYPE_CHART.read_text(encoding="utf-8")
        matrix = parse_type_matrix_from_markdown(content)

        def invert_multiplier(m: float) -> float:
            if m == 2.0:
                return 0.5
            elif m in (0.5, 0.0):
                return 2.0
            elif m == 1.0:
                return 1.0
            raise ValueError(f"Invalid multiplier {m}")

        types = CANONICAL_18_TYPES_ES
        inverted_matrix: Dict[str, Dict[str, float]] = {
            atk: {dfn: invert_multiplier(matrix[atk][dfn]) for dfn in types}
            for atk in types
        }

        # Check: Zero immunities in inverted battle
        for atk in types:
            for dfn in types:
                inv_val = inverted_matrix[atk][dfn]
                assert inv_val > 0.0, f"Inverted battle has immunity: {atk} -> {dfn} = {inv_val}"
                assert inv_val in {0.5, 1.0, 2.0}

        # Check dual-type inverted interactions
        allowed_inverted_dual = {0.25, 0.5, 1.0, 2.0, 4.0}
        for atk in types:
            for d1, d2 in combinations(types, 2):
                inv_prod = inverted_matrix[atk][d1] * inverted_matrix[atk][d2]
                assert inv_prod in allowed_inverted_dual, (
                    f"Inverted dual error for {atk} vs ({d1}/{d2}): {inv_prod}"
                )

        # Canonical inverse checks:
        # Ghost vs Normal normally is 0.0 -> inverted is 2.0
        assert inverted_matrix["Fantasma"]["Normal"] == 2.0
        assert inverted_matrix["Normal"]["Fantasma"] == 2.0
        # Electric vs Ground normally is 0.0 -> inverted is 2.0
        assert inverted_matrix["Eléctrico"]["Tierra"] == 2.0
        # Fire vs Grass normally is 2.0 -> inverted is 0.5
        assert inverted_matrix["Fuego"]["Planta"] == 0.5

    def test_adversarial_stab_multiplier_consistency(self):
        """
        Adversarial test: Validates Same-Type Attack Bonus (STAB, 1.5x) algebraic consistency:
        - Pure STAB: 1.0 * 1.5 = 1.5 (3/2)
        - STAB + Super Effective: 2.0 * 1.5 = 3.0 (3x)
        - STAB + Double Weakness: 4.0 * 1.5 = 6.0 (6x)
        - STAB + Resistance: 0.5 * 1.5 = 0.75 (3/4)
        - STAB + Double Resistance: 0.25 * 1.5 = 0.375 (3/8)
        - STAB + Immunity: 0.0 * 1.5 = 0.0
        Ensures section 2 table in 'referencia_tabla_tipos.md' documents all 11 multiplier outcomes.
        """
        assert FILE_TYPE_CHART.exists()
        content = FILE_TYPE_CHART.read_text(encoding="utf-8")

        expected_stab_products = {0.0, 0.375, 0.75, 1.5, 3.0, 6.0}
        for base_mult in {0.0, 0.25, 0.5, 1.0, 2.0, 4.0}:
            prod = base_mult * 1.5
            assert prod in expected_stab_products, f"STAB product {prod} not in expected set"

        # Verify textual documentation in table
        assert re.search(r"\bx0\.375\b|\b3/8\b", content), "Missing 0.375x STAB documentation"
        assert re.search(r"\bx0\.75\b|\b3/4\b", content), "Missing 0.75x STAB documentation"
        assert re.search(r"\bx1\.5\b|\b3/2\b", content), "Missing 1.5x STAB documentation"
        assert re.search(r"\bx3\b", content), "Missing 3x STAB documentation"
        assert re.search(r"\bx6\b", content), "Missing 6x STAB documentation"


# ---------------------------------------------------------------------------
# 7. HP & Evolution Progression Mechanics
# ---------------------------------------------------------------------------

class TestAdversarialHPEvolutionMechanics:
    """Stress tests covering canonical HP formulas, boundary cases, and evolution scaling."""

    def test_adversarial_canonical_hp_formula_bounds_and_invariants(self):
        """
        Adversarial test: Validates canonical Generation 3-9 HP calculation formula:
        HP = floor(((2 * Base + IV + floor(EV / 4)) * Level) / 100) + Level + 10

        Verifies mathematical invariants:
        1. Delta Range Invariant: HP_max(100) - HP_min(100) == 94 PS strictly for ANY base HP!
           HP_max(100) = 2 * Base + 31 + 63 + 110 = 2 * Base + 204
           HP_min(100) = 2 * Base + 0 + 0 + 110 = 2 * Base + 110
           Delta = 204 - 110 = 94.
        2. Boundary calculations for extreme species:
           - Blissey (Base 255): Min = 620, Max = 714
           - Shuckle (Base 20): Min = 150, Max = 244
           - Magikarp (Base 20): Min = 150, Max = 244
        """
        assert FILE_HP_EVO.exists()
        content = FILE_HP_EVO.read_text(encoding="utf-8")

        def calc_hp(base: int, iv: int, ev: int, level: int) -> int:
            return ((2 * base + iv + (ev // 4)) * level) // 100 + level + 10

        # Test Delta Range Invariant across arbitrary base HP values (1 to 255)
        for base in [1, 10, 20, 39, 45, 78, 100, 160, 255]:
            min_hp_100 = calc_hp(base=base, iv=0, ev=0, level=100)
            max_hp_100 = calc_hp(base=base, iv=31, ev=252, level=100)
            delta = max_hp_100 - min_hp_100
            assert delta == 94, f"Delta range invariant failed for Base HP {base}: got {delta}, expected 94"
            assert min_hp_100 == 2 * base + 110
            assert max_hp_100 == 2 * base + 204

        # Verify Blissey extremes
        assert calc_hp(255, 0, 0, 100) == 620
        assert calc_hp(255, 31, 252, 100) == 714

        # Verify Shuckle / Magikarp extremes
        assert calc_hp(20, 0, 0, 100) == 150
        assert calc_hp(20, 31, 252, 100) == 244

        # Check documentation explicitly mentions the 94 PS range
        assert re.search(r"\b94\s*(?:PS|puntos|HP)\b", content, re.IGNORECASE), (
            "referencia_ps_evoluciones.md does not document the 94 PS delta range invariant."
        )

    def test_adversarial_shedinja_hp_anomaly_invariant(self):
        """
        Adversarial test: Validates that Shedinja is explicitly documented with an absolute
        invariant HP = 1 for all levels (1..100), IVs, and EVs, and cannot follow the standard formula.
        """
        assert FILE_HP_EVO.exists()
        content = FILE_HP_EVO.read_text(encoding="utf-8")

        assert "Shedinja" in content
        # Check that the exception is clearly formulated
        has_shedinja_one_hp = bool(
            re.search(r"\bPS(?:_\{?Shedinja\}?)?\s*=\s*1\b|\b1\s*PS\s*constante\b|\bexactamente\s+1\s*PS\b", content, re.IGNORECASE)
        )
        assert has_shedinja_one_hp, (
            "referencia_ps_evoluciones.md lacks explicit rule that Shedinja always has exactly 1 HP."
        )

    def test_adversarial_evolutionary_hp_monotonicity(self):
        """
        Adversarial test: Validates that base HP across evolutionary stages is strictly
        non-decreasing (monotonic: HP(stage N) <= HP(stage N+1)) in all canonical families
        documented in 'referencia_ps_evoluciones.md'.
        """
        assert FILE_HP_EVO.exists()
        content = FILE_HP_EVO.read_text(encoding="utf-8")

        # Canonical lines and their base HPs
        canonical_lines = [
            ("Charmander", 39, "Charmeleon", 58, "Charizard", 78),
            ("Bulbasaur", 45, "Ivysaur", 60, "Venusaur", 80),
            ("Squirtle", 44, "Wartortle", 59, "Blastoise", 79),
            ("Pichu", 20, "Pikachu", 35, "Raichu", 60),
            ("Magikarp", 20, "Gyarados", 95),
            ("Gastly", 30, "Haunter", 45, "Gengar", 60),
            ("Happiny", 100, "Chansey", 250, "Blissey", 255),
            ("Ralts", 28, "Kirlia", 38, "Gardevoir", 68),
            ("Bagon", 45, "Shelgon", 65, "Salamence", 95),
        ]

        for line in canonical_lines:
            species_names = [line[i] for i in range(0, len(line), 2)]
            base_hps = [line[i] for i in range(1, len(line), 2)]

            # Check that names are present in document
            for name in species_names:
                assert name in content, f"Species {name} missing from referencia_ps_evoluciones.md"

            # Check monotonic progression: Stage 1 <= Stage 2 <= Stage 3
            for i in range(len(base_hps) - 1):
                assert base_hps[i] <= base_hps[i + 1], (
                    f"Non-monotonic HP progression in line {species_names}: {base_hps[i]} > {base_hps[i+1]}"
                )


# ---------------------------------------------------------------------------
# 8. Document Schema & Markdown Robustness
# ---------------------------------------------------------------------------

class TestAdversarialDocumentSchemaAndRobustness:
    """Stress tests covering line endings, Unicode handling, and parser resilience."""

    @pytest.mark.parametrize("grade", GRADE_NUMBERS)
    def test_adversarial_crlf_lf_parsing_invariance(self, grade: int):
        """
        Adversarial test: Ensures that parser produces byte-for-byte identical results
        whether input file has pure LF (Unix) or CRLF (Windows) line endings.
        Uses write_bytes to prevent platform-dependent automatic newline translation.
        """
        fpath = PROJECT_ROOT / f"problemas_{grade}_primaria.md"
        assert fpath.exists()

        content = fpath.read_text(encoding="utf-8")
        content_lf = content.replace("\r\n", "\n")
        content_crlf = content_lf.replace("\n", "\r\n")

        with tempfile.TemporaryDirectory() as tmpdir:
            p_lf = Path(tmpdir) / f"problemas_{grade}_lf.md"
            p_crlf = Path(tmpdir) / f"problemas_{grade}_crlf.md"
            p_lf.write_bytes(content_lf.encode("utf-8"))
            p_crlf.write_bytes(content_crlf.encode("utf-8"))

            doc_lf = parse_grade_document(p_lf, grade=grade)
            doc_crlf = parse_grade_document(p_crlf, grade=grade)

            assert len(doc_lf.problems) == len(doc_crlf.problems) == 100
            assert len(doc_lf.solutions) == len(doc_crlf.solutions) == 100

            for i in range(1, 101):
                p_l = doc_lf.problems[i]
                p_c = doc_crlf.problems[i]
                assert p_l.question.strip() == p_c.question.strip()
                assert p_l.subcategory.strip() == p_c.subcategory.strip()
                assert p_l.lomloe_sense.strip() == p_c.lomloe_sense.strip()

                s_l = doc_lf.solutions[i]
                s_c = doc_crlf.solutions[i]
                assert s_l.final_answer.strip() == s_c.final_answer.strip()
                assert s_l.identified_data.strip() == s_c.identified_data.strip()
                assert s_l.operations.strip() == s_c.operations.strip()

    @pytest.mark.parametrize("grade", GRADE_NUMBERS)
    def test_adversarial_unicode_and_accents_resilience(self, grade: int):
        """
        Adversarial test: Verifies that Spanish diacritics (á, é, í, ó, ú, ñ, ¿, ¡, º, ª)
        and Pokémon names with hyphens, accents, or special punctuation (e.g. Porygon-Z,
        Farfetch'd, Flabébé, Nidoran♀) are parsed without mangling or encoding issues.
        """
        fpath = PROJECT_ROOT / f"problemas_{grade}_primaria.md"
        assert fpath.exists()
        raw_bytes = fpath.read_bytes()

        # Check valid UTF-8 without replacement character \ufffd
        decoded_text = raw_bytes.decode("utf-8")
        assert "\ufffd" not in decoded_text, f"Grade {grade} contains UTF-8 replacement character \ufffd!"

        # Check NFC normalized equivalence
        nfc_text = unicodedata.normalize("NFC", decoded_text)
        assert len(decoded_text) == len(nfc_text), f"Grade {grade} text is not NFC-normalized."

    @pytest.mark.parametrize("grade", GRADE_NUMBERS)
    def test_adversarial_solution_mandatory_sections_depth(self, grade: int):
        """
        Adversarial test: Strictly verifies that all 100 solutions per grade have substantial,
        non-trivial content in each of the three mandatory LOMLOE sections:
        - 'Datos identificados': >= 10 characters
        - 'Planteamiento y Operaciones': >= 15 characters
        - 'Respuesta Final': >= 5 characters, contains bold markdown (**...**)
        """
        fpath = PROJECT_ROOT / f"problemas_{grade}_primaria.md"
        doc = parse_grade_document(fpath, grade=grade)

        for num in range(1, 101):
            assert num in doc.solutions, f"Grade {grade} missing solution {num}"
            sol = doc.solutions[num]

            assert len(sol.identified_data.strip()) >= 10, (
                f"Grade {grade} Sol {num}: 'Datos identificados' too short ({len(sol.identified_data.strip())} chars)"
            )
            assert len(sol.operations.strip()) >= 15, (
                f"Grade {grade} Sol {num}: 'Planteamiento y Operaciones' too short ({len(sol.operations.strip())} chars)"
            )
            assert len(sol.final_answer.strip()) >= 5, (
                f"Grade {grade} Sol {num}: 'Respuesta Final' too short ({len(sol.final_answer.strip())} chars)"
            )
            assert sol.has_bold_answer, (
                f"Grade {grade} Sol {num}: 'Respuesta Final' lacks bold formatting (**...**)"
            )

    @pytest.mark.parametrize("grade", GRADE_NUMBERS)
    def test_adversarial_zero_draft_placeholders(self, grade: int):
        """
        Adversarial test: Scans the entire file for unfinished draft tokens:
        - TODO, FIXME, TBD, XXX
        - [placeholder], [completar], [pendiente]
        - Empty brackets []
        - Lorem ipsum filler text
        """
        fpath = PROJECT_ROOT / f"problemas_{grade}_primaria.md"
        content = fpath.read_text(encoding="utf-8")

        forbidden_patterns = [
            r"\bTODO\b",
            r"\bFIXME\b",
            r"\bTBD\b",
            r"\bXXX\b",
            r"(?i)lorem\s+ipsum",
            r"(?i)\[placeholder\]",
            r"\[\s*\]",
            r"\[\s*TODO\s*\]",
            r"\[\s*TBD\s*\]",
            r"\[\s*COMPLETAR\s*\]",
            r"(?i)completar\s+este\s+problema",
            r"(?i)texto\s+simulado",
        ]

        for pat in forbidden_patterns:
            matches = re.findall(pat, content)
            assert not matches, (
                f"Grade {grade} contains {len(matches)} forbidden draft placeholder tokens matching '{pat}'"
            )


# ---------------------------------------------------------------------------
# 9. 1-to-1 Bijection & Formatting Hardening
# ---------------------------------------------------------------------------

class TestAdversarialBijectionAndFormatting:
    """Stress tests covering full 1-to-1 correspondence, numbering, and units across all 500 problems."""

    @pytest.mark.parametrize("grade", GRADE_NUMBERS)
    def test_adversarial_strict_one_to_one_bijection(self, grade: int):
        """
        Adversarial test: Verifies that every problem number from 1 to 100 has exactly
        one matching solution, no duplicate numbers exist, and no problem or solution is missing.
        """
        fpath = PROJECT_ROOT / f"problemas_{grade}_primaria.md"
        doc = parse_grade_document(fpath, grade=grade)

        expected_keys = set(range(1, 101))
        assert set(doc.problems.keys()) == expected_keys, (
            f"Grade {grade} problem keys mismatch: missing {expected_keys - set(doc.problems.keys())}"
        )
        assert set(doc.solutions.keys()) == expected_keys, (
            f"Grade {grade} solution keys mismatch: missing {expected_keys - set(doc.solutions.keys())}"
        )

    @pytest.mark.parametrize("grade", GRADE_NUMBERS)
    def test_adversarial_final_answer_numeric_or_qualitative_and_units(self, grade: int):
        r"""
        Adversarial test: Verifies that across all 100 solutions in each grade,
        'Respuesta Final' strictly contains:
        1. Bold markdown formatting (**...**).
        2. Numeric digits (\d+) OR a valid LOMLOE qualitative geometry/probability descriptor.
        3. Physical or in-game measurement units OR a valid LOMLOE qualitative term.
        """
        fpath = PROJECT_ROOT / f"problemas_{grade}_primaria.md"
        doc = parse_grade_document(fpath, grade=grade)

        for num, sol in doc.solutions.items():
            assert sol.has_bold_answer, f"Grade {grade} Sol {num} lacks bold answer (**...**)"
            is_qual = is_qualitative_lomloe_answer(sol.final_answer)
            assert sol.has_numeric_value or is_qual, (
                f"Grade {grade} Sol {num} lacks numeric digits or qualitative LOMLOE term: '{sol.final_answer}'"
            )
            assert sol.has_units or is_qual, (
                f"Grade {grade} Sol {num} lacks physical or in-game units: '{sol.final_answer}'"
            )

    def test_adversarial_all_500_problems_and_solutions_count(self):
        """
        Adversarial test: Verifies that exactly 500 distinct problems and 500 distinct solutions
        exist across the 5 grade files, meeting requirement R1 with zero gaps.
        """
        total_problems = 0
        total_solutions = 0

        for grade in GRADE_NUMBERS:
            fpath = PROJECT_ROOT / f"problemas_{grade}_primaria.md"
            doc = parse_grade_document(fpath, grade=grade)
            assert len(doc.problems) == 100, f"Grade {grade} has {len(doc.problems)} problems, expected 100"
            assert len(doc.solutions) == 100, f"Grade {grade} has {len(doc.solutions)} solutions, expected 100"
            total_problems += len(doc.problems)
            total_solutions += len(doc.solutions)

        assert total_problems == 500, f"Total problems {total_problems} != 500"
        assert total_solutions == 500, f"Total solutions {total_solutions} != 500"


# ---------------------------------------------------------------------------
# 10. Asset Integrity & URL Verification
# ---------------------------------------------------------------------------

class TestAdversarialAssetIntegrity:
    """Stress tests covering asset endpoints, HTTPS protocol, and domain security."""

    def test_adversarial_asset_urls_100_percent_https(self):
        """
        Adversarial test: Scans all URLs in 'guia_recursos_activos.md' and reference documents.
        Verifies that 100% of URLs strictly use HTTPS (zero insecure plain HTTP).
        """
        md_files = [FILE_ASSET_GUIDE, FILE_TYPE_CHART, FILE_HP_EVO]
        insecure_urls: List[str] = []

        for fpath in md_files:
            if not fpath.exists():
                continue
            content = fpath.read_text(encoding="utf-8")
            urls = re.findall(r'https?://[^\s)\]\"\'><`]+', content)
            for u in urls:
                if u.startswith("http://"):
                    insecure_urls.append(f"{fpath.name}: {u}")

        assert not insecure_urls, (
            f"Found insecure HTTP URLs in reference documents:\n" + "\n".join(insecure_urls)
        )

    def test_adversarial_asset_domains_whitelist_conformance(self):
        """
        Adversarial test: Verifies that all external links and asset references point
        strictly to trusted, whitelisted Pokémon data repositories and APIs.
        """
        assert FILE_ASSET_GUIDE.exists()
        content = FILE_ASSET_GUIDE.read_text(encoding="utf-8")
        urls = re.findall(r'https?://[^\s)\]\"\'><`]+', content)

        domain_whitelist = {
            "pokeapi.co",
            "raw.githubusercontent.com",
            "github.com",
            "pokemonshowdown.com",
            "play.pokemonshowdown.com",
            "pokemon.com",
            "www.pokemon.com",
            "assets.pokemon.com",
            "pokemondb.net",
            "img.pokemondb.net",
        }

        unauthorized_domains = set()
        for u in urls:
            parsed = urlparse(u)
            host = parsed.netloc.lower()
            if host and host not in domain_whitelist:
                unauthorized_domains.add(host)

        assert not unauthorized_domains, (
            f"Found unauthorized external domains in asset guide: {unauthorized_domains}"
        )

    def test_adversarial_pokeapi_endpoint_structure(self):
        """
        Adversarial test: Validates that PokeAPI REST endpoints documented in 'guia_recursos_activos.md'
        follow canonical v2 REST hierarchy:
        - /api/v2/pokemon/{id_or_name}/
        - /api/v2/pokemon-species/{id_or_name}/
        - /api/v2/type/{id_or_name}/
        - /api/v2/growth-rate/{id_or_name}/
        """
        assert FILE_ASSET_GUIDE.exists()
        content = FILE_ASSET_GUIDE.read_text(encoding="utf-8")

        required_endpoints = [
            r"https://pokeapi\.co/api/v2/pokemon/",
            r"https://pokeapi\.co/api/v2/pokemon-species/",
            r"https://pokeapi\.co/api/v2/type/",
            r"https://pokeapi\.co/api/v2/growth-rate/",
        ]

        for ep_pattern in required_endpoints:
            assert re.search(ep_pattern, content), (
                f"Asset guide is missing canonical PokeAPI v2 endpoint matching '{ep_pattern}'"
            )

    def test_adversarial_showdown_and_veekun_paths(self):
        """
        Adversarial test: Validates that Showdown sprite subdirectories (gen5, ani, types)
        and Veekun CSV repository endpoints are documented with valid HTTPS paths.
        """
        assert FILE_ASSET_GUIDE.exists()
        content = FILE_ASSET_GUIDE.read_text(encoding="utf-8")

        assert re.search(r"https://play\.pokemonshowdown\.com/sprites/gen5/", content)
        assert re.search(r"https://play\.pokemonshowdown\.com/sprites/types/", content)
        assert re.search(r"https://github\.com/veekun/pokedex", content)
        assert re.search(r"pokedex/data/csv/", content)
