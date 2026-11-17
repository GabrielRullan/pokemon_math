"""
conftest.py - Global pytest configuration, fixtures, and markdown parsers
for the Pokemon Primary Math LOMLOE project.

Interface Contracts & Specifications:
- Validates 5 grade files: problemas_2_primaria.md to problemas_6_primaria.md
- Validates 3 reference files: referencia_tabla_tipos.md, referencia_ps_evoluciones.md, guia_recursos_activos.md
- Provides structured models (Problem, Solution, GradeDocument) and parsing utilities.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import pytest

# ---------------------------------------------------------------------------
# Path Configuration
# ---------------------------------------------------------------------------

DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = Path(os.environ.get("POKEMON_MATH_ROOT", DEFAULT_PROJECT_ROOT)).resolve()

GRADE_NUMBERS = [2, 3, 4, 5, 6]

GRADE_FILENAME_MAP: Dict[int, str] = {
    grade: f"problemas_{grade}_primaria.md" for grade in GRADE_NUMBERS
}

REFERENCE_FILENAME_MAP: Dict[str, str] = {
    "types": "referencia_tabla_tipos.md",
    "hp": "referencia_ps_evoluciones.md",
    "assets": "guia_recursos_activos.md",
}

# ---------------------------------------------------------------------------
# Canonical Domain Constants (LOMLOE & Pokemon Mechanics)
# ---------------------------------------------------------------------------

CANONICAL_18_TYPES_ES: List[str] = [
    "Normal", "Fuego", "Agua", "Planta", "Eléctrico", "Hielo",
    "Lucha", "Veneno", "Tierra", "Volador", "Psíquico", "Bicho",
    "Roca", "Fantasma", "Dragón", "Siniestro", "Acero", "Hada",
]

CANONICAL_18_TYPES_EN: List[str] = [
    "Normal", "Fire", "Water", "Grass", "Electric", "Ice",
    "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug",
    "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy",
]

LOMLOE_MATHEMATICAL_SENSES: List[str] = [
    "Sentido Numérico",
    "Sentido de la Medida",
    "Sentido Espacial",
    "Sentido Algebraico",
    "Sentido Estocástico",
]

EXP_KEYWORDS: List[str] = [
    "exp", "experiencia", "puntos de experiencia", "puntos exp",
    "subir de nivel", "sube de nivel", "curva de experiencia",
    "repartir exp", "exp. share", "lucky egg",
]

# Canonical subcategory metadata mapping for 100-problem documents
CANONICAL_SUBCATEGORIES: Dict[int, Tuple[str, str]] = {
    1: ("Subcategoría 1: Numeración, Descomposición y Valor Posicional", "Sentido Numérico"),
    2: ("Subcategoría 2: Operaciones Aritméticas y Cálculo Mental", "Sentido Numérico"),
    3: ("Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero", "Sentido de la Medida"),
    4: ("Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio", "Sentido Espacial"),
    5: ("Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional", "Sentido Algebraico"),
    6: ("Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad", "Sentido Estocástico"),
    7: ("Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)", "Sentido Numérico"),
}


def get_canonical_subcat_and_sense(prob_num: int) -> Tuple[str, str]:
    """Returns canonical (subcategory, LOMLOE sense) based on problem index (1..100)."""
    if 1 <= prob_num <= 15:
        return CANONICAL_SUBCATEGORIES[1]
    elif 16 <= prob_num <= 35:
        return CANONICAL_SUBCATEGORIES[2]
    elif 36 <= prob_num <= 50:
        return CANONICAL_SUBCATEGORIES[3]
    elif 51 <= prob_num <= 65:
        return CANONICAL_SUBCATEGORIES[4]
    elif 66 <= prob_num <= 75:
        return CANONICAL_SUBCATEGORIES[5]
    elif 76 <= prob_num <= 85:
        return CANONICAL_SUBCATEGORIES[6]
    elif 86 <= prob_num <= 100:
        return CANONICAL_SUBCATEGORIES[7]
    return ("", "")

# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class Problem:
    """Represents a single parsed math problem."""
    number: int
    raw_text: str
    subcategory: str
    lomloe_sense: str
    pokemon_context: str
    question: str
    grade: int = 0

    @property
    def is_exp_problem(self) -> bool:
        """Determines if this problem belongs to dedicated EXP mechanics."""
        # Dedicated Subcategoría 7 (problems 86-100 in canonical 100-problem bank)
        if self.number in range(86, 101):
            return True
        subcat_lower = self.subcategory.lower()
        if "7" in subcat_lower or "experiencia" in subcat_lower:
            return True
        # Outside Subcat 7, match explicit multi-word experience / leveling phrases
        full_text = f"{self.raw_text} {self.question}".lower()
        strict_exp_pattern = (
            r"\b(puntos\s+de\s+experiencia|subir\s+de\s+nivel|curva\s+de\s+experiencia|"
            r"exp\.?\s*share|repartir\s+exp|puntos\s+exp)\b"
        )
        return bool(re.search(strict_exp_pattern, full_text))


@dataclass
class Solution:
    """Represents a single parsed problem solution."""
    number: int
    raw_text: str
    identified_data: str
    operations: str
    final_answer: str
    grade: int = 0

    @property
    def has_bold_answer(self) -> bool:
        """Checks if final answer contains bold markdown (**...**)."""
        return bool(re.search(r"\*\*[^*]+\*\*", self.final_answer))

    @property
    def has_numeric_value(self) -> bool:
        """Checks if final answer contains at least one numeric digit."""
        return bool(re.search(r"\d+", self.final_answer))

    @property
    def has_units(self) -> bool:
        """Checks if final answer contains physical or in-game units."""
        # Non-word symbols without \b boundaries
        symbols = r"(?:€|%|\$|₽|°\s*C|°)"
        word_units = [
            r"exp", r"experiencia", r"puntos\s*(?:de\s*)?exp(?:eriencia)?",
            r"ps", r"hp", r"puntos\s*de\s*salud",
            r"(?:pok[ée]|super|ultra|master|safari)\s*balls?",
            r"bayas?", r"caramelos?", r"poci[óo]n(?:es)?", r"revivir", r"ant[íi]dotos?", r"antipar[áa]lisis",
            r"monedas?", r"pok[ée]monedas?", r"pok[ée]cuartos?", r"pok[ée]cupones?",
            r"euros?", r"c[ée]ntimos?",
            r"grados?", r"segundos?", r"minutos?", r"min", r"horas?", r"h", r"d[íi]as?", r"semanas?", r"meses?", r"a[ñn]os?",
            r"metros?", r"m", r"kil[óo]metros?", r"km", r"cent[íi]metros?", r"cm", r"mil[íi]metros?", r"mm", r"dec[íi]metros?", r"dm", r"hect[óo]metros?", r"hm",
            r"gramos?", r"g", r"kilogramos?", r"kilos?", r"kg", r"hectogramos?", r"hg", r"miligramos?", r"mg",
            r"litros?", r"l", r"mililitros?", r"ml", r"centilitros?", r"cl", r"decilitros?", r"dl",
            r"pasos?", r"turnos?", r"rondas?", r"baldosas?", r"tatamis?", r"tatami",
            r"combates?", r"victorias?", r"derrotas?", r"asalto(?:s)?",
            r"puntos?", r"da[ñn]o", r"nivel(?:es)?", r"voltios?", r"v", r"w", r"vatios?", r"mah", r"kilojulios?", r"kj", r"kwh",
            r"atq", r"def", r"vel", r"dosis",
            r"fichas?", r"visitantes?", r"raciones?", r"estuches?", r"medallas?", r"cajas?", r"tarros?", r"cartas?", r"bolsas?", r"bengalas?", r"brotes?",
            r"caras?", r"v[ée]rtices?", r"aristas?", r"lados?", r"ejes?(?:\s+de\s+simetr[íi]a)?", r"casillas?", r"cuadros?", r"piedras?",
            r"encuestados?", r"votos?", r"espec[íi]menes?", r"pok[ée]mon", r"huevos?", r"trozos?", r"fracci[óo]n(?:es)?", r"unidades?", r"decenas?", r"centenas?",
            r"veces?", r"amigos?", r"frascos?", r"[áa]rboles?", r"alumnos?", r"puestos?", r"posici[óo]n(?:es)?", r"lugares?",
            r"galletas?", r"pegatinas?", r"por\s*ciento", r"porcentaje",
            r"n[úu]meros?", r"pares?", r"impares?", r"cifras?",
        ]
        joined_words = "|".join(word_units)
        # Supports symbols, whitelisted word units, or numeric quantity followed by named entity
        units_pattern = rf"(?i)(?:{symbols}|\b(?:{joined_words})\b|\b\d+\s+[A-ZÁÉÍÓÚ][a-zñáéíóú]+)"
        return bool(re.search(units_pattern, self.final_answer))


@dataclass
class GradeDocument:
    """Represents a completely parsed grade document with problems and solutions."""
    grade: int
    path: Path
    title: str
    raw_content: str
    problems: Dict[int, Problem] = field(default_factory=dict)
    solutions: Dict[int, Solution] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Robust Parsing Functions
# ---------------------------------------------------------------------------

def normalize_text(text: str) -> str:
    """Strips leading/trailing whitespace and normalizes line endings."""
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def parse_grade_document(path: Path, grade: Optional[int] = None) -> GradeDocument:
    """
    Parses a grade problem bank file (problemas_X_primaria.md) into structured
    Problem and Solution objects.
    """
    if not path.exists():
        raise FileNotFoundError(f"Grade problem document not found at: {path}")

    raw_content = path.read_text(encoding="utf-8")
    content = normalize_text(raw_content)

    # Infer grade if not provided
    if grade is None:
        grade_match = re.search(r"problemas_(\d+)_primaria", path.name)
        if grade_match:
            grade = int(grade_match.group(1))
        else:
            grade = 0

    # Extract Document Title
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else path.stem

    # Split into Parte 1 (Enunciados) and Parte 2 (Solucionario)
    part2_split = re.split(
        r"(?mi)^\s*##\s+(?:Parte\s+2[:\s]+)?Solucionario", content, maxsplit=1
    )
    if len(part2_split) == 2:
        problems_text = part2_split[0]
        solutions_text = part2_split[1]
    else:
        # Fallback: search for first solution heading
        sol_match = re.search(
            r"(?mi)^\s*###?\s+(?:\*\*)?Soluci[óo]n\s+(?:(?:al|del)\s+)?(?:Problema\s+)?\d+", content
        )
        if sol_match:
            problems_text = content[: sol_match.start()]
            solutions_text = content[sol_match.start() :]
        else:
            problems_text = content
            solutions_text = ""

    # Parse Problems
    problems: Dict[int, Problem] = {}
    problem_splits = re.split(
        r"(?mi)^\s*###?\s+(?:\*\*)?Problema\s+(\d+)\b[^\n]*", problems_text
    )

    # re.split with one capture group yields: [preamble, num1, body1, num2, body2, ...]
    if len(problem_splits) > 1:
        for i in range(1, len(problem_splits), 2):
            prob_num = int(problem_splits[i])
            body = problem_splits[i + 1]

            # Strip any trailing subcategory headers or next-section headings from body
            clean_body = re.sub(
                r"(?mi)\n\s*###?\s+Subcategor[íi]a[^\n]*", "", body
            ).strip()

            subcat_match = re.search(
                r"(?i)[-*]?\s*\*\*Subcategor[íi]a:?\*\*:?\s*([^\n]+)", clean_body
            )
            subcat = subcat_match.group(1).strip() if subcat_match else ""

            sense_match = re.search(
                r"(?i)[-*]?\s*\*\*Sentido(?:\s+LOMLOE)?:?\*\*:?\s*([^\n]+)", clean_body
            )
            sense = sense_match.group(1).strip() if sense_match else ""

            context_match = re.search(
                r"(?i)[-*]?\s*\*\*Contexto(?:\s+Pok[ée]mon)?:?\*\*:?\s*([^\n]+)", clean_body
            )
            context = context_match.group(1).strip() if context_match else ""

            # Resilient fallback to canonical mapping if document uses section-level groupings
            canonical_subcat, canonical_sense = get_canonical_subcat_and_sense(prob_num)
            if not subcat:
                subcat = canonical_subcat
            if not sense:
                sense = canonical_sense

            question_match = re.search(
                r"(?i)\*\*Pregunta:?\*\*:?\s*([\s\S]+?)(?=\n\s*###|\Z)", clean_body
            )
            if question_match:
                question = question_match.group(1).strip()
            else:
                # If no explicit **Pregunta**: tag, capture remaining text after metadata lines
                lines = [
                    line for line in clean_body.splitlines()
                    if not re.search(r"^\s*[-*]?\s*\*\*(?:Subcategor[íi]a|Sentido|Contexto)", line, re.IGNORECASE)
                ]
                question = "\n".join(lines).strip()

            problems[prob_num] = Problem(
                number=prob_num,
                raw_text=clean_body,
                subcategory=subcat,
                lomloe_sense=sense,
                pokemon_context=context,
                question=question,
                grade=grade,
            )

    # Parse Solutions
    solutions: Dict[int, Solution] = {}
    sol_splits = re.split(
        r"(?mi)^\s*###?\s+(?:\*\*)?Soluci[óo]n\s+(?:(?:al|del)\s+)?(?:Problema\s+)?(\d+)\b[^\n]*",
        solutions_text,
    )

    if len(sol_splits) > 1:
        for i in range(1, len(sol_splits), 2):
            sol_num = int(sol_splits[i])
            body = sol_splits[i + 1]

            # Use [ \t]*([\s\S]*?) with lookahead to prevent overshooting empty sections
            data_match = re.search(
                r"(?i)[-*]?\s*\*\*Datos(?:\s+identificados)?:?\*\*:?[ \t]*([\s\S]*?)(?=\n\s*[-*]?\s*\*\*Planteamiento|\Z)",
                body,
            )
            datos = data_match.group(1).strip() if data_match else ""

            ops_match = re.search(
                r"(?i)[-*]?\s*\*\*Planteamiento(?:\s*y\s*Operaciones)?:?\*\*:?[ \t]*([\s\S]*?)(?=\n\s*[-*]?\s*\*\*Respuesta|\Z)",
                body,
            )
            operaciones = ops_match.group(1).strip() if ops_match else ""

            resp_match = re.search(
                r"(?i)[-*]?\s*\*\*Respuesta(?:\s*Final)?:?\*\*:?[ \t]*([\s\S]*?)(?=\n\s*###|\Z)",
                body,
            )
            respuesta = resp_match.group(1).strip() if resp_match else ""

            solutions[sol_num] = Solution(
                number=sol_num,
                raw_text=body.strip(),
                identified_data=datos,
                operations=operaciones,
                final_answer=respuesta,
                grade=grade,
            )

    return GradeDocument(
        grade=grade,
        path=path,
        title=title,
        raw_content=content,
        problems=problems,
        solutions=solutions,
    )


def extract_markdown_tables(content: str) -> List[List[List[str]]]:
    """
    Extracts all markdown tables in a document.
    Returns a list of tables, where each table is a list of rows,
    and each row is a list of stripped cell strings.
    Handles escaped pipes (\|) and flexible pipe delimiters.
    """
    tables: List[List[List[str]]] = []
    lines = content.splitlines()
    current_table: List[List[str]] = []

    for line in lines:
        stripped = line.strip()
        if "|" in stripped and not stripped.startswith("#"):
            # Check if it's a delimiter row (e.g. |---|:---:|---| or ---|---)
            if re.match(r"^\|?(?:\s*:?-+:?\s*\|?)+\|?$", stripped) and "-" in stripped:
                continue
            # Split by pipe not preceded by backslash to preserve escaped pipes
            cells = [c.strip().replace(r"\|", "|") for c in re.split(r"(?<!\\)\|", stripped.strip("|"))]
            if len(cells) >= 2:
                current_table.append(cells)
                continue
        if current_table:
            if len(current_table) >= 2:  # Header + at least one data row
                tables.append(current_table)
            current_table = []

    if current_table and len(current_table) >= 2:
        tables.append(current_table)

    return tables


def extract_urls(content: str) -> List[str]:
    """Extracts all markdown link destinations and bare HTTP/HTTPS URLs."""
    markdown_links = re.findall(r"\[[^\]]*\]\((https?://[^\s)]+)\)", content)
    bare_urls = re.findall(r"(?<!\()(https?://[^\s)\]\"'>]+)", content)
    all_urls = sorted(list(set(markdown_links + bare_urls)))
    return all_urls


# ---------------------------------------------------------------------------
# Pytest Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def project_root() -> Path:
    """Fixture providing the absolute path to the project root directory."""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def grade_file_paths(project_root: Path) -> Dict[int, Path]:
    """Fixture returning mapping of grade number (2..6) to Path."""
    return {
        grade: project_root / GRADE_FILENAME_MAP[grade]
        for grade in GRADE_NUMBERS
    }


@pytest.fixture(scope="session")
def reference_file_paths(project_root: Path) -> Dict[str, Path]:
    """Fixture returning mapping of reference doc keys to Path."""
    return {
        key: project_root / filename
        for key, filename in REFERENCE_FILENAME_MAP.items()
    }


@pytest.fixture(scope="session")
def type_table_path(reference_file_paths: Dict[str, Path]) -> Path:
    return reference_file_paths["types"]


@pytest.fixture(scope="session")
def hp_evolution_path(reference_file_paths: Dict[str, Path]) -> Path:
    return reference_file_paths["hp"]


@pytest.fixture(scope="session")
def sourcing_guide_path(reference_file_paths: Dict[str, Path]) -> Path:
    return reference_file_paths["assets"]


@pytest.fixture(scope="session")
def grade_documents(grade_file_paths: Dict[int, Path]) -> Dict[int, GradeDocument]:
    """
    Session fixture that parses all existing grade documents.
    If a file is missing, records FileNotFoundError in the dictionary.
    """
    docs: Dict[int, GradeDocument] = {}
    for grade, path in grade_file_paths.items():
        if path.exists():
            docs[grade] = parse_grade_document(path, grade=grade)
    return docs
