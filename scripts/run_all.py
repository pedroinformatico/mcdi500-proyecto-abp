"""Ejecuta el proyecto de inicio a fin y registra la evidencia.

Pasos, en orden:
    1. Verificación del entorno (scripts/check_environment.py).
    2. Pruebas automatizadas (pytest).
    3. Ejecución de los notebooks de F1 y F2 en orden, guardando sus salidas.

Cada ejecución deja un log con fecha y hora en docs/evidencias/, que sirve como
evidencia de que el proyecto corre sin errores en el entorno declarado.

Uso:
    python scripts/run_all.py                    # todo, con log
    python scripts/run_all.py --skip-notebooks   # solo entorno y pruebas
    python scripts/run_all.py --no-log           # sin escribir log
"""

import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = PROJECT_ROOT / "docs" / "evidencias"
NOTEBOOK_DIRS = ("F1", "F2")  # orden de ejecución: fase 1 y luego fase 2
CELL_TIMEOUT_SECONDS = 600
PENDING_MARKER = "Por desarrollar"


class RunLog:
    """Escribe cada mensaje en pantalla y, si corresponde, en el archivo de log."""

    def __init__(self, path=None):
        self.path = path
        self.lines = []

    def write(self, message=""):
        stamped = f"[{datetime.now():%H:%M:%S}] {message}" if message else ""
        print(stamped, flush=True)
        self.lines.append(stamped)

    def save(self):
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text("\n".join(self.lines) + "\n", encoding="utf-8")


def run_command(log, label, command):
    """Ejecuta un comando externo, registra su salida y devuelve True si terminó bien."""
    log.write(f"== {label}: {' '.join(command[1:])}")
    started = time.perf_counter()
    result = subprocess.run(command, cwd=PROJECT_ROOT, capture_output=True, text=True)
    for line in (result.stdout + result.stderr).splitlines():
        log.write(f"   {line}")
    elapsed = time.perf_counter() - started
    log.write(f"   -> {'OK' if result.returncode == 0 else 'ERROR'} ({elapsed:.1f} s)")
    return result.returncode == 0


def list_notebooks():
    """Notebooks a ejecutar, por fase y en orden alfabético (01_, 02_, ...)."""
    notebooks = []
    for folder in NOTEBOOK_DIRS:
        notebooks += sorted((PROJECT_ROOT / folder).glob("*.ipynb"))
    return notebooks


def execute_notebook(log, path):
    """Ejecuta un notebook en su propia carpeta y guarda las salidas en el mismo archivo."""
    relative = path.relative_to(PROJECT_ROOT)
    log.write(f"== Notebook {relative}")
    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=CELL_TIMEOUT_SECONDS,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    started = time.perf_counter()
    try:
        client.execute()
    except CellExecutionError as error:
        # Se registra solo el final del error: suele contener la excepción y la línea que falló.
        for line in str(error).strip().splitlines()[-8:]:
            log.write(f"   {line}")
        log.write(f"   -> ERROR ({time.perf_counter() - started:.1f} s)")
        return False
    nbformat.write(notebook, path)
    code_cells = sum(1 for cell in notebook.cells if cell.cell_type == "code")
    log.write(f"   -> OK: {code_cells} celdas de código ejecutadas ({time.perf_counter() - started:.1f} s)")
    if PENDING_MARKER in path.read_text(encoding="utf-8"):
        log.write(f"   aviso: aún contiene secciones marcadas '{PENDING_MARKER}'")
    return True


def main():
    parser = argparse.ArgumentParser(description="Ejecución completa del proyecto con registro de evidencia.")
    parser.add_argument("--skip-notebooks", action="store_true", help="omitir la ejecución de notebooks")
    parser.add_argument("--no-log", action="store_true", help="no escribir el log en docs/evidencias/")
    args = parser.parse_args()

    log_path = None if args.no_log else EVIDENCE_DIR / f"ejecucion_{datetime.now():%Y-%m-%d_%H%M%S}.log"
    log = RunLog(log_path)
    log.write(f"Ejecución completa del proyecto · Python {sys.version.split()[0]}")

    results = {
        "entorno": run_command(log, "Entorno", [sys.executable, "scripts/check_environment.py"]),
        "pruebas": run_command(log, "Pruebas", [sys.executable, "-m", "pytest", "-q"]),
    }
    if not args.skip_notebooks:
        for notebook in list_notebooks():
            results[str(notebook.relative_to(PROJECT_ROOT))] = execute_notebook(log, notebook)

    failed = [step for step, ok in results.items() if not ok]
    log.write()
    log.write(f"Resumen: {len(results) - len(failed)}/{len(results)} pasos correctos")
    for step in failed:
        log.write(f"   falló: {step}")
    log.save()
    if log_path:
        print(f"Log guardado en {log_path.relative_to(PROJECT_ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
