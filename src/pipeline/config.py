"""Rutas y parámetros compartidos del proyecto.

Centraliza las ubicaciones de datos y evidencias para que notebooks, scripts y
pruebas usen las mismas rutas, sin depender del directorio desde donde se ejecuten.
"""

from pathlib import Path

# Raíz del repositorio: src/pipeline/config.py -> subir tres niveles.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"  # datos originales: nunca se modifican
PROCESSED_DATA_DIR = DATA_DIR / "processed"  # salidas del pipeline: se regeneran
EVIDENCE_DIR = PROJECT_ROOT / "docs" / "evidencias"  # logs y capturas de ejecución

# Semilla única para que cualquier operación aleatoria sea reproducible.
RANDOM_SEED = 42
