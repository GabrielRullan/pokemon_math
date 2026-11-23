#!/usr/bin/env python3
"""
Genera los 12 PDFs A4 listos para imprimir y encuadernar (1º a 6º de Primaria) en html/pdf/:
  1. cuadernillo_X_primaria_alumno.pdf  (Cuadernillo A4 encuadernable, solo alumno)
  2. apendice_X_primaria_docente.pdf    (Apéndice del Docente: Ficha del Profesor Oak
                                         + Solucionario, sin páginas del alumno)
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT_DIR = Path(__file__).resolve().parent
HTML_DIR = ROOT_DIR / "html"
PDF_DIR = HTML_DIR / "pdf"

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


def main() -> int:
    browser = find_browser()
    print(f"Usando navegador headless: {browser}")
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    # Eliminar antiguos PDFs obsoletos (docente antiguo y folletos A5 descartados)
    for pattern in ("cuadernillo_*_primaria_docente.pdf", "cuadernillo_*_primaria_alumno_a5_folleto.pdf"):
        for old_pdf in PDF_DIR.glob(pattern):
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
        teacher_appendix_pdf = PDF_DIR / f"apendice_{grade}_primaria_docente.pdf"

        # 1. Cuadernillo A4 Alumno (encuadernable, solo ejercicios)
        render_pdf(browser, f"{base_uri}?mode=alumno", student_a4_pdf)

        # 2. Apéndice del Docente (solo Ficha Oak + Solucionario, sin páginas del alumno)
        render_pdf(browser, f"{base_uri}?mode=docente", teacher_appendix_pdf)

        a4_pages = len(PdfReader(str(student_a4_pdf)).pages)
        doc_pages = len(PdfReader(str(teacher_appendix_pdf)).pages)

        print(
            f"[OK] {grade}º Primaria -> "
            f"A4 Alumno: {a4_pages} págs ({student_a4_pdf.stat().st_size / (1024*1024):.2f} MB) | "
            f"Apéndice Docente: {doc_pages} págs ({teacher_appendix_pdf.stat().st_size / (1024*1024):.2f} MB)"
        )
        generated.extend([student_a4_pdf, teacher_appendix_pdf])

    print(f"Total PDFs generados y verificados: {len(generated)} / 12")
    return 0


if __name__ == "__main__":
    sys.exit(main())
