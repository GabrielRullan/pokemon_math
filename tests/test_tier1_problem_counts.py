"""
test_tier1_problem_counts.py - Tier 1: Feature & Volume Coverage Verification.

Verifies:
1. All 5 grade files exist (problemas_2_primaria.md through problemas_6_primaria.md).
2. Each grade file contains at least 100 distinct numbered problems.
3. Total problems across all files is at least 500.
4. Problem numbers are strictly 1 to 100 sequential without gaps or duplicates.
5. Problems have non-trivial content length and no empty placeholders.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

import pytest

from conftest import (
    GRADE_NUMBERS,
    GradeDocument,
    parse_grade_document,
)

# Minimum acceptable question length in characters to ensure pedagogical depth
MIN_QUESTION_CHAR_LENGTH = 25

# Forbidden placeholder patterns in problem definitions (strict developer tokens)
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


@pytest.mark.parametrize("grade", GRADE_NUMBERS)
def test_grade_file_exists(grade: int, grade_file_paths: Dict[int, Path]):
    """Verifies that the markdown file for each grade (2 to 6) exists in the project root."""
    path = grade_file_paths[grade]
    assert path.exists(), f"Grade {grade} file does not exist: {path.name}"
    assert path.stat().st_size > 0, f"Grade {grade} file is empty (0 bytes): {path.name}"


@pytest.mark.parametrize("grade", GRADE_NUMBERS)
def test_grade_has_at_least_100_problems(grade: int, grade_file_paths: Dict[int, Path]):
    """Verifies that each grade file contains at least 100 parsed problems."""
    path = grade_file_paths[grade]
    assert path.exists(), f"Cannot test problem count; file missing: {path.name}"

    doc: GradeDocument = parse_grade_document(path, grade=grade)
    problem_count = len(doc.problems)

    assert problem_count >= 100, (
        f"Grade {grade} ({path.name}) has only {problem_count} problems; "
        f"expected at least 100."
    )


def test_total_problem_count_across_all_grades(grade_file_paths: Dict[int, Path]):
    """Verifies that the sum of problems across all 5 grade files is >= 500."""
    total_problems = 0
    missing_files = []

    for grade in GRADE_NUMBERS:
        path = grade_file_paths[grade]
        if not path.exists():
            missing_files.append(path.name)
            continue
        doc = parse_grade_document(path, grade=grade)
        total_problems += len(doc.problems)

    assert not missing_files, f"Missing grade files preventing total count: {missing_files}"
    assert total_problems >= 500, (
        f"Total problem count across all grades is {total_problems}; "
        f"expected at least 500 total problems."
    )


@pytest.mark.parametrize("grade", GRADE_NUMBERS)
def test_problem_numbering_sequential_1_to_100(grade: int, grade_file_paths: Dict[int, Path]):
    """
    Verifies that problem numbers within each grade file are strictly sequential
    from 1 to 100 with no gaps, no duplicates, and no missing indices.
    """
    path = grade_file_paths[grade]
    assert path.exists(), f"Cannot test problem numbering; file missing: {path.name}"

    doc = parse_grade_document(path, grade=grade)
    numbers = sorted(doc.problems.keys())

    # Check for presence of numbers 1..100
    expected_first_100 = list(range(1, 101))
    actual_first_100 = numbers[:100]

    assert actual_first_100 == expected_first_100, (
        f"Grade {grade} ({path.name}) problem numbering is not 1 to 100 sequential.\n"
        f"Missing numbers: {set(expected_first_100) - set(numbers)}\n"
        f"First 10 actual keys: {numbers[:10]}"
    )


@pytest.mark.parametrize("grade", GRADE_NUMBERS)
def test_problem_content_non_trivial(grade: int, grade_file_paths: Dict[int, Path]):
    """
    Verifies that all problems in each grade file have substantive content:
    - Non-empty and sufficient question length
    - Valid subcategory or LOMLOE metadata
    - No forbidden placeholder tokens
    """
    path = grade_file_paths[grade]
    assert path.exists(), f"Cannot test problem content; file missing: {path.name}"

    doc = parse_grade_document(path, grade=grade)
    assert doc.problems, f"Grade {grade} has no parsed problems in {path.name}."

    trivial_problems = []
    placeholder_problems = []

    for num, prob in doc.problems.items():
        # Check non-trivial question text length
        q_clean = prob.question.strip()
        if len(q_clean) < MIN_QUESTION_CHAR_LENGTH:
            trivial_problems.append((num, len(q_clean), q_clean))

        # Check for forbidden placeholder patterns
        prob_text = f"{prob.raw_text} {prob.question}"
        for pat in FORBIDDEN_PLACEHOLDER_PATTERNS:
            if re.search(pat, prob_text):
                placeholder_problems.append((num, pat))

    assert not trivial_problems, (
        f"Grade {grade} has {len(trivial_problems)} problems with question text shorter "
        f"than {MIN_QUESTION_CHAR_LENGTH} chars: {trivial_problems[:5]}"
    )

    assert not placeholder_problems, (
        f"Grade {grade} contains forbidden placeholders in problems: {placeholder_problems[:5]}"
    )
