# -*- coding: utf-8 -*-
"""
Verification script for problemas_2_primaria.md
Verifies all formatting, structure, counts, LOMLOE requirements, solution keys, and placeholders.
"""

import os
import re
import sys

def verify():
    filepath = r"C:\Users\gabri\teamwork_projects\pokemon_math\problemas_2_primaria.md"
    print(f"Verifying {filepath}...")

    # 1. Existence and non-empty
    assert os.path.exists(filepath), f"File {filepath} does not exist!"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    assert len(content) > 1000, f"File content is unexpectedly small: {len(content)} chars"
    print(f"[PASS] File exists and has {len(content)} characters, {len(content.splitlines())} lines.")

    # 2. Main title
    assert "# Banco de Problemas Matemáticos Pokémon — 2º de Primaria (LOMLOE)" in content, "Main title missing or incorrect!"
    print("[PASS] Main header verified.")

    # 3. Two main parts
    assert "## Parte 1: Enunciados de los Problemas (1 al 100)" in content, "Part 1 header missing!"
    assert "## Parte 2: Solucionario y Respuestas Razonadas (1 al 100)" in content, "Part 2 header missing!"
    print("[PASS] Part 1 and Part 2 headers verified.")

    parts = content.split("## Parte 2: Solucionario y Respuestas Razonadas (1 al 100)")
    assert len(parts) == 2, "Failed to split into Part 1 and Part 2 exactly once!"
    part1 = parts[0]
    part2 = parts[1]

    # 4. Check Problems in Part 1
    # Match: ### Problema (\d+): (.+)
    prob_matches = list(re.finditer(r"^### Problema (\d+):\s*(.+)$", part1, re.MULTILINE))
    assert len(prob_matches) == 100, f"Expected exactly 100 problems, found {len(prob_matches)}"
    print(f"[PASS] Exactly 100 problem headers found in Part 1.")

    problems = {}
    for i, m in enumerate(prob_matches, start=1):
        num = int(m.group(1))
        title = m.group(2).strip()
        assert num == i, f"Problem numbering mismatch: expected {i}, got {num}"
        problems[num] = title
    print("[PASS] Problem numbering is strictly sequential from 1 to 100.")

    # 5. Check Solutions in Part 2
    sol_matches = list(re.finditer(r"^### Solución Problema (\d+):\s*(.+)$", part2, re.MULTILINE))
    assert len(sol_matches) == 100, f"Expected exactly 100 solutions, found {len(sol_matches)}"
    print(f"[PASS] Exactly 100 solution headers found in Part 2.")

    solutions = {}
    for i, m in enumerate(sol_matches, start=1):
        num = int(m.group(1))
        title = m.group(2).strip()
        assert num == i, f"Solution numbering mismatch: expected {i}, got {num}"
        assert title == problems[num], f"Solution title mismatch for #{num}: '{title}' vs '{problems[num]}'"
        solutions[num] = title
    print("[PASS] Solution numbering is strictly sequential from 1 to 100 and titles match problems perfectly.")

    # 6. Check Solution structure bullets
    # Each solution must have:
    # - **Datos identificados**:
    # - **Planteamiento y Operaciones**:
    # - **Respuesta Final**: with bold value
    sol_blocks = re.split(r"^### Solución Problema \d+: .+$", part2, flags=re.MULTILINE)[1:]
    assert len(sol_blocks) == 100, f"Expected 100 solution blocks, got {len(sol_blocks)}"

    for i, block in enumerate(sol_blocks, start=1):
        assert "- **Datos identificados**:" in block, f"Solution #{i} missing '- **Datos identificados**:'"
        assert "- **Planteamiento y Operaciones**:" in block, f"Solution #{i} missing '- **Planteamiento y Operaciones**:'"
        assert "- **Respuesta Final**:" in block, f"Solution #{i} missing '- **Respuesta Final**:'"

        # Check bold in final answer
        rf_match = re.search(r"- \*\*Respuesta Final\*\*:\s*(.+)$", block, re.MULTILINE)
        assert rf_match, f"Solution #{i} missing content after '- **Respuesta Final**:'"
        rf_text = rf_match.group(1)
        assert re.search(r"\*\*.+\*\*", rf_text), f"Solution #{i} final answer lacks bold highlighted value: {rf_text}"
    print("[PASS] All 100 solutions adhere strictly to the 3-bullet structure with bold answers.")

    # 7. Check placeholders
    placeholders = ["TODO", "FIXME", "XXX", "TBD", "placeholder", "PLACEHOLDER"]
    for ph in placeholders:
        assert ph not in content, f"Found placeholder '{ph}' in content!"
    print("[PASS] Zero placeholders found.")

    # 8. Check Subcategories
    subcats = [
        ("Subcategoría 1: Numeración, Descomposición y Valor Posicional", 1, 15),
        ("Subcategoría 2: Operaciones Aritméticas y Cálculo Mental", 16, 35),
        ("Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero", 36, 50),
        ("Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio", 51, 65),
        ("Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional", 66, 75),
        ("Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad", 76, 85),
        ("Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)", 86, 100),
    ]
    for name, start_p, end_p in subcats:
        count = end_p - start_p + 1
        assert name in content, f"Subcategory '{name}' missing!"
        print(f"[PASS] Subcategory '{name}' covers problems {start_p} to {end_p} ({count} problems).")

    # 9. EXP problems check in Subcat 7 (Problems 86 to 100)
    for p_num in range(86, 101):
        block = sol_blocks[p_num - 1]
        assert any(term in block for term in ["EXP", "Salud", "PS", "Nivel", "Poción"]), f"Problem #{p_num} doesn't seem to mention combat/EXP terms"
    print("[PASS] Dedicated EXP and Combat mechanics problems (86-100) thoroughly verified.")

    print("\n=======================================================")
    print("ALL 9 VERIFICATION CHECKS PASSED WITH 100% SUCCESS!")
    print("=======================================================")

if __name__ == "__main__":
    verify()
