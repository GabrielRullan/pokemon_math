#!/usr/bin/env python3
"""
Genera los 12 cuadernillos anuales en formato PDF A4 listos para imprimir
(Edición Alumno y Edición Docente, de 1º a 6º de Primaria) en html/pdf/
utilizando Chrome o Microsoft Edge en modo headless.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

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

    generated: list[Path] = []
    for grade in range(1, 7):
        src_html = HTML_DIR / f"problemas_{grade}_primaria.html"
        if not src_html.exists():
            raise FileNotFoundError(
                f"Falta {src_html}. Ejecuta primero: python build_html.py"
            )

        base_uri = src_html.resolve().as_uri()
        student_pdf = PDF_DIR / f"cuadernillo_{grade}_primaria_alumno.pdf"
        teacher_pdf = PDF_DIR / f"cuadernillo_{grade}_primaria_docente.pdf"

        # Edición Alumno (?mode=alumno con fallback a archivo temporal si el tamaño no difiere)
        render_pdf(browser, f"{base_uri}?mode=alumno", student_pdf)
        render_pdf(browser, base_uri, teacher_pdf)

        # Verificar que el PDF de alumno realmente ocultó solucionario + Ficha Oak
        if student_pdf.stat().st_size >= teacher_pdf.stat().st_size * 0.95:
            tmp_html = HTML_DIR / f"_tmp_problemas_{grade}_alumno.html"
            try:
                raw_html = src_html.read_text(encoding="utf-8")
                if '<body class="' in raw_html:
                    patched = raw_html.replace('<body class="', '<body class="hide-solutions ', 1)
                else:
                    patched = raw_html.replace("<body>", '<body class="hide-solutions">', 1)
                tmp_html.write_text(patched, encoding="utf-8")
                render_pdf(browser, tmp_html.resolve().as_uri(), student_pdf)
            finally:
                if tmp_html.exists():
                    tmp_html.unlink()

        s_mb = student_pdf.stat().st_size / (1024 * 1024)
        t_mb = teacher_pdf.stat().st_size / (1024 * 1024)
        print(
            f"[OK] {grade}º Primaria -> "
            f"{student_pdf.name} ({s_mb:.2f} MB) | "
            f"{teacher_pdf.name} ({t_mb:.2f} MB)"
        )
        generated.extend([student_pdf, teacher_pdf])

    print(f"Total PDFs generados y verificados: {len(generated)} / 12")
    return 0


if __name__ == "__main__":
    sys.exit(main())
