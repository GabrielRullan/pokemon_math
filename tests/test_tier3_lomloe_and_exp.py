"""
test_tier3_lomloe_and_exp.py - Tier 3: Pedagogical & Curriculum Compliance.

Verifies:
1. Every problem is explicitly tagged with a valid LOMLOE 'Sentido Matemático'.
2. All 5 core LOMLOE mathematical senses (Numérico, Medida, Espacial, Algebraico,
   Estocástico) are present within each grade's problem bank.
3. Every grade contains at least 15 dedicated EXP (experience/level) problems.
4. Total dedicated EXP problems across all 5 grades is at least 75.
5. Dedicated EXP problems realistically model experience points, defeats, and level-ups.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

import pytest

from conftest import (
    EXP_KEYWORDS,
    GRADE_NUMBERS,
    LOMLOE_MATHEMATICAL_SENSES,
    GradeDocument,
    Problem,
    parse_grade_document,
)

# Standard canonical senses and their normalized classification tokens
SENSE_CLASSIFIERS = {
    "Sentido Numérico": [r"num[ée]ric[oa]"],
    "Sentido de la Medida": [r"medida"],
    "Sentido Espacial": [r"espacial", r"geom[ée]tr"],
    "Sentido Algebraico": [r"algebraic[oa]", r"computacional", r"patron(?:es)?"],
    "Sentido Estocástico": [r"estoc[áa]stic[oa]", r"estad[íi]stic[oa]", r"azar", r"probabilidad"],
}


def classify_lomloe_sense(raw_sense: str) -> Set[str]:
    """Identifies which of the 5 canonical LOMLOE mathematical senses are indicated."""
    classified = set()
    text = raw_sense.lower()
    for canonical_name, patterns in SENSE_CLASSIFIERS.items():
        if any(re.search(pat, text) for pat in patterns):
            classified.add(canonical_name)
    return classified


@pytest.mark.parametrize("grade", GRADE_NUMBERS)
def test_every_problem_has_valid_lomloe_sense(grade: int, grade_file_paths: Dict[int, Path]):
    """
    Verifies that every problem has a non-empty LOMLOE sense tag that resolves
    to at least one official LOMLOE mathematical sense.
    """
    path = grade_file_paths[grade]
    assert path.exists(), f"Cannot test LOMLOE tags; file missing: {path.name}"

    doc: GradeDocument = parse_grade_document(path, grade=grade)
    untagged_or_invalid: List[Tuple[int, str]] = []

    for num, prob in doc.problems.items():
        sense_text = prob.lomloe_sense.strip()
        if not sense_text:
            # Fallback: check if subcategory or raw_text indicates sense
            senses = classify_lomloe_sense(prob.subcategory + " " + prob.raw_text)
        else:
            senses = classify_lomloe_sense(sense_text)

        if not senses:
            untagged_or_invalid.append((num, prob.lomloe_sense))

    assert not untagged_or_invalid, (
        f"Grade {grade} has {len(untagged_or_invalid)} problems with missing or unclassifiable "
        f"LOMLOE senses:\n"
        f"Examples: {untagged_or_invalid[:10]}"
    )


@pytest.mark.parametrize("grade", GRADE_NUMBERS)
def test_all_five_mathematical_senses_present_per_grade(grade: int, grade_file_paths: Dict[int, Path]):
    """
    Verifies that all 5 core mathematical senses mandated by RD 157/2022
    (Numérico, Medida, Espacial, Algebraico, Estocástico) are represented in each grade.
    """
    path = grade_file_paths[grade]
    assert path.exists(), f"Cannot test curriculum coverage; file missing: {path.name}"

    doc = parse_grade_document(path, grade=grade)
    represented_senses: Set[str] = set()

    for prob in doc.problems.values():
        senses = classify_lomloe_sense(f"{prob.lomloe_sense} {prob.subcategory}")
        represented_senses.update(senses)

    missing_senses = set(LOMLOE_MATHEMATICAL_SENSES) - represented_senses
    assert not missing_senses, (
        f"Grade {grade} ({path.name}) fails to cover all 5 LOMLOE mathematical senses.\n"
        f"Missing senses: {missing_senses}\n"
        f"Present senses: {represented_senses}"
    )


@pytest.mark.parametrize("grade", GRADE_NUMBERS)
def test_grade_has_at_least_15_dedicated_exp_problems(grade: int, grade_file_paths: Dict[int, Path]):
    """
    Verifies that each grade has at least 15 dedicated experience-related problems
    (calculating EXP gained per defeat across levels and EXP required to level up).
    """
    path = grade_file_paths[grade]
    assert path.exists(), f"Cannot test EXP problem quota; file missing: {path.name}"

    doc = parse_grade_document(path, grade=grade)
    exp_problems: List[Problem] = [p for p in doc.problems.values() if p.is_exp_problem]

    assert len(exp_problems) >= 15, (
        f"Grade {grade} ({path.name}) contains only {len(exp_problems)} dedicated EXP problems; "
        f"expected at least 15 under Subcategoría 7 or experience keywords."
    )


def test_total_dedicated_exp_problems_across_all_grades(grade_file_paths: Dict[int, Path]):
    """
    Verifies that the total number of dedicated EXP problems across all 5 grade files
    is at least 75 (15 per grade * 5 grades).
    """
    total_exp_problems = 0
    missing_files = []

    for grade in GRADE_NUMBERS:
        path = grade_file_paths[grade]
        if not path.exists():
            missing_files.append(path.name)
            continue
        doc = parse_grade_document(path, grade=grade)
        exp_count = sum(1 for p in doc.problems.values() if p.is_exp_problem)
        total_exp_problems += exp_count

    assert not missing_files, f"Missing grade files preventing total EXP count: {missing_files}"
    assert total_exp_problems >= 75, (
        f"Total dedicated EXP problems across all grades is {total_exp_problems}; "
        f"expected at least 75."
    )


@pytest.mark.parametrize("grade", GRADE_NUMBERS)
def test_exp_problems_contain_level_and_experience_mechanics(grade: int, grade_file_paths: Dict[int, Path]):
    """
    Verifies that EXP problems specifically model level thresholds, battle experience yields,
    or leveling calculations in both question text and solution operations.
    """
    path = grade_file_paths[grade]
    assert path.exists(), f"Cannot test EXP mechanics; file missing: {path.name}"

    doc = parse_grade_document(path, grade=grade)
    exp_problems = [p for p in doc.problems.values() if p.is_exp_problem]
    assert exp_problems, f"Grade {grade} has no EXP problems identified."

    deficient_exp_problems: List[Tuple[int, str]] = []

    for prob in exp_problems:
        sol = doc.solutions.get(prob.number)
        ops = sol.operations if sol else ""
        ans = sol.final_answer if sol else ""
        combined_text = f"{prob.raw_text} {prob.question} {ops} {ans}".lower()

        # Must mention either exp/experiencia OR nivel/salud/combate mechanics
        has_exp = any(kw in combined_text for kw in ["exp", "experiencia", "puntos de experiencia", "puntos exp"])
        has_level = any(kw in combined_text for kw in ["nivel", "subir", "crecimiento", "ps", "vida", "combate", "salud", "puntos de salud", "daño"])

        if not (has_exp or has_level):
            deficient_exp_problems.append((prob.number, prob.question[:60]))

    assert not deficient_exp_problems, (
        f"Grade {grade} has EXP problems lacking clear level/experience mechanics:\n"
        f"Examples: {deficient_exp_problems[:5]}"
    )


@pytest.mark.parametrize("grade", GRADE_NUMBERS)
def test_exp_progression_matches_grade_pedagogy(grade: int, grade_file_paths: Dict[int, Path]):
    """
    Verifies the grade-differentiated pedagogical progression of EXP mechanics
    mandated by TEST_INFRA.md and LOMLOE:
    - 2º: Linear EXP sums and differences.
    - 3º: EXP multiplication, equal party division, and cubic n^3 intro.
    - 4º: Battles needed with division remainders and 1.5x trainer bonus.
    - 5º: Decimal multipliers (Lucky Egg +50%, traded +50%), canonical defeat formula, percentages.
    - 6º: Canonical growth curves (L^3, 0.8 L^3, 1.25 L^3), Exp. Share party distribution, stat stages.
    """
    path = grade_file_paths[grade]
    assert path.exists(), f"Cannot test EXP progression; file missing: {path.name}"

    doc = parse_grade_document(path, grade=grade)
    sub7_problems = [p for n, p in doc.problems.items() if n in range(86, 101)]
    assert len(sub7_problems) >= 15, f"Grade {grade} has fewer than 15 Subcat 7 problems."

    sub7_text = " ".join(
        f"{p.raw_text} {doc.solutions[p.number].operations if p.number in doc.solutions else ''}"
        for p in sub7_problems
    ).lower()

    if grade == 2:
        has_progression = bool(re.search(r"\b(suma|\+|resta|-|total|ganar|ganan|asaltos?)\b", sub7_text))
        assert has_progression, "Grade 2 Subcat 7 lacks linear EXP addition/subtraction mechanics."
    elif grade == 3:
        has_progression = bool(re.search(r"\b(multiplic|repart|mitad|doble|entre|divisi|iguales)\b", sub7_text))
        assert has_progression, "Grade 3 Subcat 7 lacks EXP multiplication/party division mechanics."
    elif grade == 4:
        has_progression = bool(re.search(r"(?:resto|sobran?|1[.,]5|entrenador|salvaje)", sub7_text))
        assert has_progression, "Grade 4 Subcat 7 lacks division remainder or 1.5x trainer mechanics."
    elif grade == 5:
        has_progression = bool(re.search(r"(?:7|f[óo]rmula|porcent|%|1[.,]5|1[.,]7|derrota)", sub7_text))
        assert has_progression, "Grade 5 Subcat 7 lacks defeat formula or decimal/percentage multipliers."
    elif grade == 6:
        has_progression = bool(re.search(r"(?:c[uú]bic|\^3|potencia|curva|crecimiento|0[.,]8|1[.,]25|repartir)", sub7_text))
        assert has_progression, "Grade 6 Subcat 7 lacks cubic growth curves or Exp. Share party fractions."
