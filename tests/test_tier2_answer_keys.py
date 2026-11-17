"""
test_tier2_answer_keys.py - Tier 2: Boundary & Corner Cases (Answer Keys & Mathematical Integrity).

Verifies:
1. Strict 1-to-1 correspondence between each problem and its solution (no missing, no orphan solutions).
2. Every solution has non-empty 'Datos identificados', 'Planteamiento y Operaciones', and 'Respuesta Final'.
3. No forbidden placeholders (TBD, TODO, lorem, empty brackets, etc.).
4. Final answers are formatted in bold (**...**) and include explicit numeric values and relevant units.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

import pytest

from conftest import (
    GRADE_NUMBERS,
    GradeDocument,
    parse_grade_document,
)

# Strict developer placeholder patterns
FORBIDDEN_PLACEHOLDER_PATTERNS: List[str] = [
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
    r"\bCOMPLETAR\b",
]


def is_qualitative_lomloe_answer(text: str) -> bool:
    """
    Checks if text contains legitimate qualitative LOMLOE mathematical terms
    (e.g. geometric solids/shapes, probability/stochastic vocabulary, or relational expressions)
    that do not require numeric digits or physical measurement units.
    """
    qualitative_patterns = [
        # Geometry: shapes, bodies, solids
        r"\b(?:esfera|cubo|cilindro|cono|prisma|pir[áa]mide|poliedro|c[íi]rculo|cuadrado|rect[áa]ngulo|tri[áa]ngulo|pent[áa]gono|hex[áa]gono|oct[óo]gono|rombo|trapecio|pol[íi]gono)\b",
        # Probability & stochastic vocabulary
        r"\b(?:seguro|posible|imposible|m[áa]s\s+(?:probable|posible)|menos\s+(?:probable|posible)|igual\s+de\s+(?:probable|posible)|azar|probabilidad)\b",
        # Qualitative color patterns
        r"\b(?:amarill[ao]|azul|roj[ao]|verde|negro|blanco)\b",
        # Pure numeric relational comparisons (e.g. 245 < 254 < 425)
        r"[<>=]",
    ]
    return any(re.search(pat, text, re.IGNORECASE) for pat in qualitative_patterns)


@pytest.mark.parametrize("grade", GRADE_NUMBERS)
def test_problem_to_solution_one_to_one_correspondence(grade: int, grade_file_paths: Dict[int, Path]):
    """
    Verifies that every problem has exactly one corresponding solution (no missing solutions),
    and every solution corresponds to a valid problem (no orphan solutions).
    """
    path = grade_file_paths[grade]
    assert path.exists(), f"Cannot test solution correspondence; file missing: {path.name}"

    doc: GradeDocument = parse_grade_document(path, grade=grade)

    problem_keys = set(doc.problems.keys())
    solution_keys = set(doc.solutions.keys())

    missing_solutions = problem_keys - solution_keys
    orphan_solutions = solution_keys - problem_keys

    assert not missing_solutions, (
        f"Grade {grade} ({path.name}) is missing solutions for problems: {sorted(missing_solutions)[:10]}"
    )
    assert not orphan_solutions, (
        f"Grade {grade} ({path.name}) has orphan solutions without problems: {sorted(orphan_solutions)[:10]}"
    )
    assert len(doc.solutions) >= 100, (
        f"Grade {grade} ({path.name}) has {len(doc.solutions)} solutions; expected at least 100."
    )


@pytest.mark.parametrize("grade", GRADE_NUMBERS)
def test_solution_mandatory_sections_present_and_non_empty(grade: int, grade_file_paths: Dict[int, Path]):
    """
    Verifies that every solution contains all three required pedagogical components:
    - Datos identificados (identified quantities/variables)
    - Planteamiento y Operaciones (mathematical procedure and arithmetic steps)
    - Respuesta Final (explicit final conclusion)
    """
    path = grade_file_paths[grade]
    assert path.exists(), f"Cannot test solution schema; file missing: {path.name}"

    doc = parse_grade_document(path, grade=grade)
    assert doc.solutions, f"Grade {grade} has no parsed solutions in {path.name}."

    deficient_solutions: List[Tuple[int, str]] = []

    for num, sol in doc.solutions.items():
        if len(sol.identified_data.strip()) < 3:
            deficient_solutions.append((num, "Missing or trivial 'Datos identificados'"))
        if len(sol.operations.strip()) < 5:
            deficient_solutions.append((num, "Missing or trivial 'Planteamiento y Operaciones'"))
        if len(sol.final_answer.strip()) < 3:
            deficient_solutions.append((num, "Missing or trivial 'Respuesta Final'"))

    assert not deficient_solutions, (
        f"Grade {grade} has {len(deficient_solutions)} solutions violating required schema:\n"
        f"Examples: {deficient_solutions[:10]}"
    )


@pytest.mark.parametrize("grade", GRADE_NUMBERS)
def test_solutions_contain_no_placeholders(grade: int, grade_file_paths: Dict[int, Path]):
    """
    Verifies that no solutions contain unfinished draft placeholders
    such as 'TBD', 'TODO', 'lorem ipsum', empty brackets, or 'COMPLETAR'.
    """
    path = grade_file_paths[grade]
    assert path.exists(), f"Cannot test placeholders; file missing: {path.name}"

    doc = parse_grade_document(path, grade=grade)
    assert doc.solutions, f"Grade {grade} has no parsed solutions in {path.name}."
    placeholder_solutions: List[Tuple[int, str]] = []

    for num, sol in doc.solutions.items():
        full_text = f"{sol.raw_text} {sol.identified_data} {sol.operations} {sol.final_answer}"
        for pat in FORBIDDEN_PLACEHOLDER_PATTERNS:
            if re.search(pat, full_text):
                placeholder_solutions.append((num, pat))

    assert not placeholder_solutions, (
        f"Grade {grade} solutions contain forbidden placeholder tokens:\n"
        f"Examples: {placeholder_solutions[:10]}"
    )


@pytest.mark.parametrize("grade", GRADE_NUMBERS)
def test_final_answer_formatting_bold_numeric_and_units(grade: int, grade_file_paths: Dict[int, Path]):
    """
    Verifies that each solution's 'Respuesta Final' meets pedagogical presentation standards:
    1. Result is emphasized with bold markdown formatting (**...**).
    2. Includes an explicit numerical value (digits), or legitimate LOMLOE qualitative mathematical terms.
    3. Includes contextual or mathematical units (e.g. EXP, PS, Pokémon, monedas, km, kg, etc.),
       exempting pure numeration problems and qualitative answers.
    """
    path = grade_file_paths[grade]
    assert path.exists(), f"Cannot test final answer formatting; file missing: {path.name}"

    doc = parse_grade_document(path, grade=grade)
    assert doc.solutions, f"Grade {grade} has no parsed solutions in {path.name}."
    non_bold_answers: List[Tuple[int, str]] = []
    missing_numeric_answers: List[Tuple[int, str]] = []
    missing_units_answers: List[Tuple[int, str]] = []

    for num, sol in doc.solutions.items():
        ans_text = sol.final_answer.strip()
        is_qual = is_qualitative_lomloe_answer(ans_text)

        if not sol.has_bold_answer:
            non_bold_answers.append((num, ans_text))

        # Quantitative solutions require numbers; LOMLOE qualitative solutions (geometry, probability) are accepted
        if not sol.has_numeric_value and not is_qual:
            missing_numeric_answers.append((num, ans_text))

        # Units required, exempting pure numeration (Subcat 1: 1..15) and qualitative geometry/probability answers
        is_subcat_1 = (num <= 15)
        if not sol.has_units and not (is_subcat_1 or is_qual):
            missing_units_answers.append((num, ans_text))

    assert not non_bold_answers, (
        f"Grade {grade} has {len(non_bold_answers)} answers lacking bold (**...**) emphasis:\n"
        f"Examples: {non_bold_answers[:5]}"
    )

    assert not missing_numeric_answers, (
        f"Grade {grade} has {len(missing_numeric_answers)} answers lacking numeric values:\n"
        f"Examples: {missing_numeric_answers[:5]}"
    )

    assert not missing_units_answers, (
        f"Grade {grade} has {len(missing_units_answers)} answers lacking explicit units:\n"
        f"Examples: {missing_units_answers[:5]}"
    )


def test_total_solution_count_across_all_grades(grade_file_paths: Dict[int, Path]):
    """Verifies that the total number of solutions across all 5 grade files is >= 500."""
    total_solutions = 0
    missing_files = []

    for grade in GRADE_NUMBERS:
        path = grade_file_paths[grade]
        if not path.exists():
            missing_files.append(path.name)
            continue
        doc = parse_grade_document(path, grade=grade)
        total_solutions += len(doc.solutions)

    assert not missing_files, f"Missing grade files preventing solution count: {missing_files}"
    assert total_solutions >= 500, (
        f"Total solution count across all grades is {total_solutions}; "
        f"expected at least 500 total solutions."
    )
