"""
test_grade1_primaria.py - Comprehensive validation suite for 1º de Primaria (problemas_1_primaria.md).

Verifies:
1. File existence, UTF-8 integrity, strict NFC normalization, and CRLF/LF parsing invariance.
2. Exact Markdown schema matching problemas_2_primaria.md (H1, Intro, Parte 1, Parte 1B, Parte 2).
3. 100 core problems + 100 core solutions parsed via conftest.parse_grade_document with 1-to-1 title parity.
4. Exact distribution across the 7 canonical subcategories and coverage of all 5 LOMLOE senses.
5. At least 15 dedicated EXP/combat mechanics problems (86-100) with PS, Pociones (+20 PS), Bayas Aranja (+10 PS).
6. All 20 Retos Especiales (101-120) and their matching solutions (### Solución al Reto 101..120).
7. Strict 0-99 numerical bound across all problem statements, questions, contexts, and bold final answers.
8. Every 2-digit number in a bold final answer appears in operations, identified_data, or question.
9. Bold answers, explicit units (or qualitative LOMLOE terms), and zero placeholder tokens.
"""

from __future__ import annotations

import os
import re
import sys
import tempfile
import unicodedata
from pathlib import Path
from typing import Dict, List, Tuple

import pytest

TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(os.environ.get("POKEMON_MATH_ROOT", TESTS_DIR.parent)).resolve()
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from conftest import (
    LOMLOE_MATHEMATICAL_SENSES,
    GradeDocument,
    Solution,
    get_canonical_subcat_and_sense,
    normalize_text,
    parse_grade_document,
)
from test_tier2_answer_keys import is_qualitative_lomloe_answer
from test_tier3_lomloe_and_exp import classify_lomloe_sense

GRADE1_PATH = PROJECT_ROOT / "problemas_1_primaria.md"

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


@pytest.fixture(scope="module")
def grade1_raw_text() -> str:
    assert GRADE1_PATH.exists(), f"Missing file: {GRADE1_PATH}"
    return GRADE1_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def grade1_doc() -> GradeDocument:
    assert GRADE1_PATH.exists(), f"Missing file: {GRADE1_PATH}"
    return parse_grade_document(GRADE1_PATH, grade=1)


def parse_retos_and_solutions(content: str) -> Tuple[Dict[int, Dict[str, str]], Dict[int, Dict[str, str]]]:
    """Parses Retos 101..120 from Parte 1B and their corresponding solutions in Parte 2."""
    norm = normalize_text(content)
    part2_split = re.split(r"(?mi)^\s*##\s+Parte\s+2:", norm, maxsplit=1)
    assert len(part2_split) == 2, "Missing '## Parte 2:' section divider."
    part1_all, part2_all = part2_split

    part1b_split = re.split(r"(?mi)^\s*##\s+Parte\s+1B:", part1_all, maxsplit=1)
    assert len(part1b_split) == 2, "Missing '## Parte 1B:' section divider."
    part1b_text = part1b_split[1]

    retos: Dict[int, Dict[str, str]] = {}
    reto_splits = re.split(r"(?mi)^\s*###\s+Reto\s+(\d+):\s*([^\n]+)", part1b_text)
    for i in range(1, len(reto_splits), 3):
        rnum = int(reto_splits[i])
        rtitle = reto_splits[i + 1].strip()
        rbody = reto_splits[i + 2].strip()

        m_sub = re.search(r"(?im)^-\s+\*\*Subcategor[íi]a\*\*:\s*([^\n]+)", rbody)
        m_sen = re.search(r"(?im)^-\s+\*\*Sentido\s+LOMLOE\*\*:\s*([^\n]+)", rbody)
        m_ctx = re.search(r"(?is)-\s+\*\*Contexto\s+Pok[ée]mon\*\*:\s*([\s\S]+?)(?=\n\s*\*\*Pregunta\*\*:)", rbody)
        m_q = re.search(r"(?im)^\*\*Pregunta\*\*:\s*(.+)$", rbody)

        retos[rnum] = {
            "title": rtitle,
            "subcategory": m_sub.group(1).strip() if m_sub else "",
            "sense": m_sen.group(1).strip() if m_sen else "",
            "context": m_ctx.group(1).strip() if m_ctx else "",
            "question": m_q.group(1).strip() if m_q else "",
            "body": rbody,
        }

    reto_solutions: Dict[int, Dict[str, str]] = {}
    sol_splits = re.split(r"(?mi)^\s*###\s+Soluci[óo]n\s+al\s+Reto\s+(\d+):\s*([^\n]+)", part2_all)
    for i in range(1, len(sol_splits), 3):
        snum = int(sol_splits[i])
        stitle = sol_splits[i + 1].strip()
        sbody = sol_splits[i + 2].strip()

        m_data = re.search(
            r"(?is)-\s+\*\*Datos\s+identificados\*\*:\s*([\s\S]*?)(?=\n\s*-\s+\*\*Planteamiento|\Z)",
            sbody,
        )
        m_ops = re.search(
            r"(?is)-\s+\*\*Planteamiento\s+y\s+Operaciones\*\*:\s*([\s\S]*?)(?=\n\s*-\s+\*\*Respuesta|\Z)",
            sbody,
        )
        m_resp = re.search(
            r"(?is)-\s+\*\*Respuesta\s+Final\*\*:\s*([\s\S]*?)(?=\n\s*###|\Z)",
            sbody,
        )

        reto_solutions[snum] = {
            "title": stitle,
            "datos": m_data.group(1).strip() if m_data else "",
            "operaciones": m_ops.group(1).strip() if m_ops else "",
            "respuesta": m_resp.group(1).strip() if m_resp else "",
            "body": sbody,
        }

    return retos, reto_solutions


def test_grade1_file_exists_and_utf8_nfc():
    """Verifies file existence, valid UTF-8 encoding, and strict NFC normalization."""
    assert GRADE1_PATH.exists(), f"Missing {GRADE1_PATH.name}"
    raw_bytes = GRADE1_PATH.read_bytes()
    assert len(raw_bytes) > 1000, "problemas_1_primaria.md is unexpectedly small"

    decoded = raw_bytes.decode("utf-8")
    assert "\ufffd" not in decoded, "Found UTF-8 replacement character"
    nfc_text = unicodedata.normalize("NFC", decoded)
    assert decoded == nfc_text, "problemas_1_primaria.md is not UTF-8 NFC normalized"


def test_grade1_required_section_headings(grade1_raw_text: str):
    """Verifies exact canonical document headings matching problemas_2_primaria.md."""
    required_headings = [
        "# Banco de Problemas Matemáticos Pokémon — 1º de Primaria (LOMLOE)",
        "## Introducción Curricular y Pedagógica",
        "## Parte 1: Enunciados de los Problemas (1 al 100)",
        "## Parte 1B: Retos Especiales (101 al 120)",
        "## Parte 2: Solucionario y Respuestas Razonadas (1 al 100)",
        "### Soluciones — Parte 1B: Retos Especiales (101 al 120)",
    ]
    for h in required_headings:
        assert h in grade1_raw_text, f"Missing required heading: {h}"


def test_grade1_core_100_problems_and_solutions_via_parser(grade1_doc: GradeDocument, grade1_raw_text: str):
    """Verifies 100 core problems and 100 core solutions parsed via parse_grade_document with title parity."""
    assert len(grade1_doc.problems) == 100, f"Expected 100 problems, got {len(grade1_doc.problems)}"
    assert len(grade1_doc.solutions) == 100, f"Expected 100 solutions, got {len(grade1_doc.solutions)}"
    assert sorted(grade1_doc.problems.keys()) == list(range(1, 101))
    assert sorted(grade1_doc.solutions.keys()) == list(range(1, 101))

    part1_only = grade1_raw_text.split("## Parte 1B:")[0]
    part2_only = grade1_raw_text.split("## Parte 2:")[1]
    prob_titles = {
        int(m.group(1)): m.group(2).strip()
        for m in re.finditer(r"(?m)^### Problema (\d+):\s*(.+)$", part1_only)
    }
    sol_titles = {
        int(m.group(1)): m.group(2).strip()
        for m in re.finditer(r"(?m)^### Solución Problema (\d+):\s*(.+)$", part2_only)
    }
    assert sorted(prob_titles.keys()) == list(range(1, 101))
    assert sorted(sol_titles.keys()) == list(range(1, 101))
    assert prob_titles == sol_titles, "Core problem and solution titles do not match 1-to-1"

    for num, prob in grade1_doc.problems.items():
        assert len(prob.question.strip()) >= 25, f"Problem {num} question < 25 chars: {prob.question}"
        assert prob.pokemon_context.strip(), f"Problem {num} missing Contexto Pokémon"
        assert prob.subcategory.strip(), f"Problem {num} missing Subcategoría"
        assert prob.lomloe_sense.strip(), f"Problem {num} missing Sentido LOMLOE"


def test_grade1_canonical_subcategories_and_all_five_senses(grade1_doc: GradeDocument):
    """Verifies exact distribution across 7 subcategories and coverage of all 5 LOMLOE senses."""
    represented_senses = set()

    for num in range(1, 101):
        prob = grade1_doc.problems[num]
        expected_subcat, expected_sense = get_canonical_subcat_and_sense(num)
        assert prob.subcategory.strip() == expected_subcat, (
            f"Problem {num} subcategory '{prob.subcategory}' != expected '{expected_subcat}'"
        )
        assert prob.lomloe_sense.strip() == expected_sense, (
            f"Problem {num} sense '{prob.lomloe_sense}' != expected '{expected_sense}'"
        )
        classified = classify_lomloe_sense(prob.lomloe_sense)
        assert classified == {expected_sense}, f"Problem {num} failed LOMLOE classification: {classified}"
        represented_senses.update(classified)

    assert set(LOMLOE_MATHEMATICAL_SENSES) == represented_senses, (
        f"Missing LOMLOE senses: {set(LOMLOE_MATHEMATICAL_SENSES) - represented_senses}"
    )


def test_grade1_at_least_15_exp_problems_with_mechanics(grade1_doc: GradeDocument):
    """Verifies >= 15 EXP/combat problems (86-100) with EXP, level, PS, Poción, or Baya Aranja."""
    exp_probs = [p for p in grade1_doc.problems.values() if p.is_exp_problem]
    assert len(exp_probs) >= 15, f"Expected >= 15 EXP problems, got {len(exp_probs)}"

    for num in range(86, 101):
        prob = grade1_doc.problems[num]
        sol = grade1_doc.solutions[num]
        combined = f"{prob.raw_text} {sol.operations} {sol.final_answer}".lower()
        assert any(kw in combined for kw in ["exp", "experiencia", "nivel", "ps", "poción", "baya aranja"]), (
            f"Problem {num} lacks combat/EXP/PS mechanics"
        )


def test_grade1_core_solutions_bold_units_and_grounding(grade1_doc: GradeDocument):
    """Verifies mandatory solution fields, bold formatting, units, and 2-digit bold number grounding."""
    for num in range(1, 101):
        prob = grade1_doc.problems[num]
        sol = grade1_doc.solutions[num]

        assert len(sol.identified_data.strip()) >= 10, f"Sol {num} Datos identificados too short"
        assert len(sol.operations.strip()) >= 15, f"Sol {num} Planteamiento y Operaciones too short"
        assert len(sol.final_answer.strip()) >= 5, f"Sol {num} Respuesta Final too short"

        assert sol.has_bold_answer, f"Sol {num} missing bold (**...**) answer"
        is_qual = is_qualitative_lomloe_answer(sol.final_answer)
        assert sol.has_numeric_value or is_qual, f"Sol {num} lacks numeric value or qualitative term: {sol.final_answer}"
        assert sol.has_units or is_qual, f"Sol {num} lacks units or qualitative term: {sol.final_answer}"

        # 2-digit numbers in bold final answers must appear in operations, identified_data, or question
        bolds = re.findall(r"\*\*([^*]+)\*\*", sol.final_answer)
        combined_context = (
            sol.operations.replace(".", "").replace(",", "")
            + " "
            + sol.identified_data.replace(".", "").replace(",", "")
            + " "
            + prob.question.replace(".", "").replace(",", "")
        )
        for b in bolds:
            digits = re.findall(r"\b\d+\b", b.replace(".", "").replace(",", ""))
            for d in digits:
                if len(d) >= 2:
                    assert d in combined_context, (
                        f"Sol {num}: 2-digit number '{d}' in bold '{b}' not grounded in operations/data/question"
                    )


def test_grade1_retos_101_to_120_and_solutions(grade1_raw_text: str):
    """Verifies all 20 Retos (101-120) and their matching solutions in Parte 2."""
    retos, reto_solutions = parse_retos_and_solutions(grade1_raw_text)
    assert sorted(retos.keys()) == list(range(101, 121)), f"Retos keys mismatch: {sorted(retos.keys())}"
    assert sorted(reto_solutions.keys()) == list(range(101, 121)), (
        f"Reto solution keys mismatch: {sorted(reto_solutions.keys())}"
    )

    for num in range(101, 121):
        r = retos[num]
        rs = reto_solutions[num]

        assert r["title"] == rs["title"], f"Reto {num} title mismatch: '{r['title']}' vs '{rs['title']}'"
        assert r["subcategory"], f"Reto {num} missing Subcategoría"
        assert r["sense"] in LOMLOE_MATHEMATICAL_SENSES, f"Reto {num} invalid LOMLOE sense: {r['sense']}"
        assert r["context"], f"Reto {num} missing Contexto Pokémon"
        assert len(r["question"]) >= 25, f"Reto {num} question < 25 chars"

        assert len(rs["datos"]) >= 10, f"Reto Sol {num} Datos too short"
        assert len(rs["operaciones"]) >= 15, f"Reto Sol {num} Operaciones too short"
        assert len(rs["respuesta"]) >= 5, f"Reto Sol {num} Respuesta too short"

        sol_obj = Solution(
            number=num,
            raw_text=rs["body"],
            identified_data=rs["datos"],
            operations=rs["operaciones"],
            final_answer=rs["respuesta"],
            grade=1,
        )
        assert sol_obj.has_bold_answer, f"Reto Sol {num} missing bold answer"
        is_qual = is_qualitative_lomloe_answer(sol_obj.final_answer)
        assert sol_obj.has_numeric_value or is_qual, f"Reto Sol {num} lacks numeric value or qualitative term"
        assert sol_obj.has_units or is_qual, f"Reto Sol {num} lacks units or qualitative term: {sol_obj.final_answer}"

        bolds = re.findall(r"\*\*([^*]+)\*\*", sol_obj.final_answer)
        combined_context = (
            rs["operaciones"].replace(".", "").replace(",", "")
            + " "
            + rs["datos"].replace(".", "").replace(",", "")
            + " "
            + r["question"].replace(".", "").replace(",", "")
        )
        for b in bolds:
            digits = re.findall(r"\b\d+\b", b.replace(".", "").replace(",", ""))
            for d in digits:
                if len(d) >= 2:
                    assert d in combined_context, (
                        f"Reto Sol {num}: 2-digit number '{d}' in bold '{b}' not grounded"
                    )


def test_grade1_numerical_domain_strict_0_to_99(grade1_doc: GradeDocument, grade1_raw_text: str):
    """Strictly enforces that every integer in questions, contexts, operations, and bold answers is <= 99."""
    for num, prob in grade1_doc.problems.items():
        # conftest.parse_grade_document lookahead stops at '###', so Problem 100 captures '## Parte 1B: ...'
        clean_question = re.split(r"\n+\s*##\s+Parte\s+1B:", prob.question, maxsplit=1)[0].strip()
        for field_name, text in [("question", clean_question), ("context", prob.pokemon_context)]:
            for val_str in re.findall(r"\b\d+\b", text):
                assert int(val_str) <= 99, f"Problem {num} {field_name} has integer {val_str} > 99"

    for num, sol in grade1_doc.solutions.items():
        for val_str in re.findall(r"\b\d+\b", f"{sol.identified_data} {sol.operations} {sol.final_answer}"):
            assert int(val_str) <= 99, f"Solution {num} has integer {val_str} > 99"
        bolds = re.findall(r"\*\*([^*]+)\*\*", sol.final_answer)
        for b in bolds:
            for val_str in re.findall(r"\b\d+\b", b):
                assert int(val_str) <= 99, f"Solution {num} bold answer has integer {val_str} > 99"

    retos, reto_solutions = parse_retos_and_solutions(grade1_raw_text)
    for num in range(101, 121):
        r = retos[num]
        rs = reto_solutions[num]
        for field_name, text in [("question", r["question"]), ("context", r["context"])]:
            for val_str in re.findall(r"\b\d+\b", text):
                assert int(val_str) <= 99, f"Reto {num} {field_name} has integer {val_str} > 99"
        for val_str in re.findall(r"\b\d+\b", f"{rs['datos']} {rs['operaciones']} {rs['respuesta']}"):
            assert int(val_str) <= 99, f"Reto Sol {num} has integer {val_str} > 99"


def test_grade1_zero_placeholders_and_crlf_lf_invariance(grade1_raw_text: str):
    """Verifies zero placeholder tokens and byte-for-byte CRLF/LF parser invariance."""
    for pat in FORBIDDEN_PLACEHOLDER_PATTERNS:
        matches = re.findall(pat, grade1_raw_text)
        assert not matches, f"Found forbidden placeholder matching '{pat}': {matches[:5]}"

    content_lf = grade1_raw_text.replace("\r\n", "\n")
    content_crlf = content_lf.replace("\n", "\r\n")
    with tempfile.TemporaryDirectory() as tmpdir:
        p_lf = Path(tmpdir) / "problemas_1_lf.md"
        p_crlf = Path(tmpdir) / "problemas_1_crlf.md"
        p_lf.write_bytes(content_lf.encode("utf-8"))
        p_crlf.write_bytes(content_crlf.encode("utf-8"))

        doc_lf = parse_grade_document(p_lf, grade=1)
        doc_crlf = parse_grade_document(p_crlf, grade=1)
        assert len(doc_lf.problems) == len(doc_crlf.problems) == 100
        assert len(doc_lf.solutions) == len(doc_crlf.solutions) == 100
        for i in range(1, 101):
            assert doc_lf.problems[i].question.strip() == doc_crlf.problems[i].question.strip()
            assert doc_lf.solutions[i].final_answer.strip() == doc_crlf.solutions[i].final_answer.strip()


def test_grade1_single_line_preguntas_and_grade1_operations_appropriate(grade1_doc: GradeDocument, grade1_raw_text: str):
    """Checks single-line **Pregunta** tags (for build_html.py) and no multiplication/division operators."""
    part1_all = grade1_raw_text.split("## Parte 2:")[0]
    for line in part1_all.splitlines():
        if "**Pregunta**" in line:
            assert re.match(r"^\*\*Pregunta\*\*:\s*\S.+", line), f"Malformed Pregunta line: {line}"

    # Verify 1º Primaria uses sums/subtractions rather than × or ÷
    for num, sol in grade1_doc.solutions.items():
        assert "×" not in sol.operations and "÷" not in sol.operations, (
            f"Solution {num} uses ×/÷ which is beyond 1º Primaria"
        )
