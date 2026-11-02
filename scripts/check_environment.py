"""Verifica que el entorno coincide con el declarado en el repositorio.

Comprueba la versión de Python (.python-version) y que cada dependencia de
requirements.txt esté instalada con la versión exacta. Con --write registra
el entorno verificado en docs/entorno.md como evidencia de reproducibilidad.

Uso:
    python scripts/check_environment.py          # solo verificar
    python scripts/check_environment.py --write  # verificar y registrar
"""

import argparse
import platform
import sys
from datetime import datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"
PYTHON_VERSION_FILE = PROJECT_ROOT / ".python-version"
ENVIRONMENT_REPORT = PROJECT_ROOT / "docs" / "entorno.md"


def read_requirements(path):
    """Devuelve una lista de (paquete, versión) a partir de líneas 'paquete==versión'."""
    pins = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()  # ignora comentarios y líneas vacías
        if not line:
            continue
        if "==" not in line:
            raise ValueError(f"Dependencia sin versión fijada: {line!r}")
        name, pinned = (part.strip() for part in line.split("==", 1))
        pins.append((name, pinned))
    return pins


def check_packages(pins):
    """Compara cada dependencia con la versión instalada. Devuelve filas (paquete, esperada, instalada, ok)."""
    rows = []
    for name, expected in pins:
        try:
            installed = version(name)
        except PackageNotFoundError:
            installed = None
        rows.append((name, expected, installed, installed == expected))
    return rows


def check_python(path):
    """Compara la versión mayor.menor de Python con la declarada en .python-version."""
    expected = path.read_text(encoding="utf-8").strip()
    current = f"{sys.version_info.major}.{sys.version_info.minor}"
    return expected, current, current == expected


def write_report(rows, python_info):
    """Escribe docs/entorno.md con el detalle del entorno verificado."""
    expected_py, current_py, _ = python_info
    lines = [
        "# Registro del entorno",
        "",
        f"Generado por `scripts/check_environment.py --write` el {datetime.now():%Y-%m-%d %H:%M}.",
        "",
        "| Elemento | Valor |",
        "|---|---|",
        f"| Sistema operativo | {platform.system()} {platform.release()} ({platform.machine()}) |",
        f"| Python declarado (`.python-version`) | {expected_py} |",
        f"| Python en uso | {platform.python_version()} |",
        "| Ambiente virtual | `.venv` (venv de la biblioteca estándar) |",
        "",
        "| Paquete | Versión fijada | Versión instalada | Estado |",
        "|---|---|---|---|",
    ]
    for name, expected, installed, ok in rows:
        lines.append(f"| {name} | {expected} | {installed or 'no instalado'} | {'ok' if ok else 'DIFERENTE'} |")
    ENVIRONMENT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Verifica el entorno reproducible del proyecto.")
    parser.add_argument("--write", action="store_true", help="registrar el resultado en docs/entorno.md")
    args = parser.parse_args()

    python_info = check_python(PYTHON_VERSION_FILE)
    rows = check_packages(read_requirements(REQUIREMENTS_FILE))

    expected_py, current_py, python_ok = python_info
    status = "ok" if python_ok else f"aviso: se declaró {expected_py}"
    print(f"Python {platform.python_version()} ({status})")
    for name, expected, installed, ok in rows:
        print(f"  {'ok ' if ok else 'ERR'} {name}=={expected} (instalado: {installed or 'no'})")

    failures = [row for row in rows if not row[3]]
    if args.write:
        write_report(rows, python_info)
        print(f"Registro escrito en {ENVIRONMENT_REPORT.relative_to(PROJECT_ROOT)}")
    if failures:
        print(f"{len(failures)} dependencia(s) no coinciden con requirements.txt")
        return 1
    print("Entorno verificado: todas las dependencias coinciden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
