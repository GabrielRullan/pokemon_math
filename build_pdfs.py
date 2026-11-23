#!/usr/bin/env python3
"""
Genera los 18 PDFs listos para imprimir y encuadernar (1º a 6º de Primaria) en html/pdf/:
  1. cuadernillo_X_primaria_alumno.pdf           (Cuadernillo A4 encuadernable, solo alumno)
  2. cuadernillo_X_primaria_alumno_a5_folleto.pdf (Cuadernillo A5 impuesto 2-up en A4 apaisado
                                                   para imprimir a doble cara por el borde corto
                                                   y doblar por la mitad)
  3. apendice_X_primaria_docente.pdf              (Apéndice del Docente: Ficha del Profesor Oak
                                                   + Solucionario, sin páginas del alumno)
"""

from __future__ import annotations

import math
import shutil
import subprocess
import sys
from pathlib import Path

from pypdf import PageObject, PdfReader, PdfWriter, Transformation

ROOT_DIR = Path(__file__).resolve().parent
HTML_DIR = ROOT_DIR / "html"
PDF_DIR = HTML_DIR / "pdf"

# A4 apaisado (297mm x 210mm) en puntos tipográficos (1 pt = 1/72 in)
A4_LANDSCAPE_W = 841.89
A4_LANDSCAPE_H = 595.28
HALF_W = A4_LANDSCAPE_W / 2.0

BROWSER_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
]


def find_browser() -> Path:
    for candidate in BROWSER_CANDIDATES:
        if candidate.exists():
            return candidate
    for name in ("chrome", "google-chrome", "chromium", "msedge"):
        resolved = shutil.which(name)
        if resolved:
            return Path(resolved)
    raise FileNotFoundError(
        "No se encontró Google Chrome ni Microsoft Edge para exportar los PDF."
    )


def render_pdf(browser: Path, target_uri: str, out_pdf: Path) -> None:
    cmd = [
        str(browser),
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--allow-file-access-from-files",
        "--virtual-time-budget=8000",
        f"--print-to-pdf={out_pdf}",
        target_uri,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if res.returncode != 0:
        raise RuntimeError(
            f"Fallo al generar {out_pdf.name} (código {res.returncode}): {res.stderr.strip()}"
        )
    if not out_pdf.exists() or out_pdf.stat().st_size < 1024:
        raise RuntimeError(f"PDF vacío o no generado: {out_pdf}")
    header = out_pdf.read_bytes()[:5]
    if header != b"%PDF-":
        raise RuntimeError(f"Cabecera PDF inválida en {out_pdf.name}: {header!r}")


def impose_a5_booklet_on_a4(a5_pdf: Path, out_booklet_pdf: Path) -> tuple[int, int]:
    """Impone un PDF A5 en folleto (saddle-stitch) sobre hojas A4 apaisadas (2-up).

    Devuelve (paginas_a5_originales, caras_a4_apaisadas).
    Imprimir a doble cara volteando por el borde corto y doblar por la mitad.
    """
    reader = PdfReader(str(a5_pdf))
    orig_pages = list(reader.pages)
    n_orig = len(orig_pages)
    total_slots = max(4, math.ceil(n_orig / 4) * 4)

    writer = PdfWriter()

    def get_page(idx: int):
        return orig_pages[idx] if idx < n_orig else None

    def place_half(sheet: PageObject, src_page, x_offset: float) -> None:
        if src_page is None:
            return
        w = float(src_page.mediabox.width)
        h = float(src_page.mediabox.height)
        scale = min(HALF_W / w, A4_LANDSCAPE_H / h)
        tx = x_offset + (HALF_W - w * scale) / 2.0
        ty = (A4_LANDSCAPE_H - h * scale) / 2.0
        op = Transformation().scale(scale, scale).translate(tx, ty)
        sheet.merge_transformed_page(src_page, op)

    num_sheets = total_slots // 4
    for k in range(num_sheets):
        # Cara frontal de la hoja k: [última - 2k | 2k + 1] (0-indexed: total_slots-1-2k, 2k)
        front = PageObject.create_blank_page(width=A4_LANDSCAPE_W, height=A4_LANDSCAPE_H)
        place_half(front, get_page(total_slots - 1 - 2 * k), 0.0)
        place_half(front, get_page(2 * k), HALF_W)
        writer.add_page(front)

        # Cara trasera de la hoja k: [2k + 2 | última - 2k - 1] (0-indexed: 2k+1, total_slots-2-2k)
        back = PageObject.create_blank_page(width=A4_LANDSCAPE_W, height=A4_LANDSCAPE_H)
        place_half(back, get_page(2 * k + 1), 0.0)
        place_half(back, get_page(total_slots - 2 - 2 * k), HALF_W)
        writer.add_page(back)

    with out_booklet_pdf.open("wb") as fh:
        writer.write(fh)

    return n_orig, len(writer.pages)


def main() -> int:
    browser = find_browser()
    print(f"Usando navegador headless: {browser}")
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    # Eliminar antiguos cuadernillo_*_primaria_docente.pdf sustituidos por apendice_*_primaria_docente.pdf
    for old_pdf in PDF_DIR.glob("cuadernillo_*_primaria_docente.pdf"):
        old_pdf.unlink()
        print(f"[CLEAN] Eliminado obsoleto: {old_pdf.name}")

    generated: list[Path] = []
    for grade in range(1, 7):
        src_html = HTML_DIR / f"problemas_{grade}_primaria.html"
        if not src_html.exists():
            raise FileNotFoundError(
                f"Falta {src_html}. Ejecuta primero: python build_html.py"
            )

        base_uri = src_html.resolve().as_uri()
        student_a4_pdf = PDF_DIR / f"cuadernillo_{grade}_primaria_alumno.pdf"
        student_a5_tmp = PDF_DIR / f"_tmp_a5_{grade}.pdf"
        student_a5_booklet = PDF_DIR / f"cuadernillo_{grade}_primaria_alumno_a5_folleto.pdf"
        teacher_appendix_pdf = PDF_DIR / f"apendice_{grade}_primaria_docente.pdf"

        # 1. Cuadernillo A4 Alumno (encuadernable)
        render_pdf(browser, f"{base_uri}?mode=alumno", student_a4_pdf)

        # 2. Cuadernillo A5 Alumno impuesto en folleto A4 apaisado
        try:
            render_pdf(browser, f"{base_uri}?mode=alumno&size=a5", student_a5_tmp)
            a5_orig, a4_faces = impose_a5_booklet_on_a4(student_a5_tmp, student_a5_booklet)
        finally:
            if student_a5_tmp.exists():
                student_a5_tmp.unlink()

        # 3. Apéndice del Docente (solo Ficha Oak + Solucionario, sin páginas del alumno)
        render_pdf(browser, f"{base_uri}?mode=docente", teacher_appendix_pdf)

        a4_pages = len(PdfReader(str(student_a4_pdf)).pages)
        doc_pages = len(PdfReader(str(teacher_appendix_pdf)).pages)

        print(
            f"[OK] {grade}º Primaria -> "
            f"A4 Alumno: {a4_pages} págs ({student_a4_pdf.stat().st_size / (1024*1024):.2f} MB) | "
            f"A5 Folleto: {a5_orig} págs A5 -> {a4_faces} caras A4 ({student_a5_booklet.stat().st_size / (1024*1024):.2f} MB) | "
            f"Apéndice Docente: {doc_pages} págs ({teacher_appendix_pdf.stat().st_size / (1024*1024):.2f} MB)"
        )
        generated.extend([student_a4_pdf, student_a5_booklet, teacher_appendix_pdf])

    print(f"Total PDFs generados y verificados: {len(generated)} / 18")
    return 0


if __name__ == "__main__":
    sys.exit(main())
