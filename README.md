# Proyecto ABP · MCDI500 Programación para la Ciencia de Datos

Repositorio del proyecto transversal del curso MCDI500 (Magíster en Ciencia de Datos e Inteligencia Artificial, Universidad Andrés Bello).

## Descripción del proyecto

> **Por desarrollar:** problemática, objetivo general y dataset utilizado (resumen de `F1/F1_Definición.ipynb`).

## Estructura

```
F1/                  Fase 1 · definición del proyecto y mapa conceptual técnico
F2/                  Fase 2 · pipeline de datos (obtención → validación)
src/pipeline/        módulos reutilizables del pipeline (importables desde los notebooks)
tests/               pruebas automatizadas con pytest
data/raw/            datos originales (no se modifican)
data/processed/      datos generados por el pipeline (se regeneran, no se versionan)
docs/                entorno, decisiones técnicas, trazabilidad y evidencias de ejecución
scripts/             verificación del entorno y ejecución completa
```

## Requisitos

- Python 3.14 (declarado en `.python-version`; funciona desde 3.12).
- Dependencias con versiones fijadas en `requirements.txt`.

## Instalación del entorno

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
python scripts/check_environment.py
```

Windows (PowerShell):

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e .
python scripts/check_environment.py
```

`pip install -e .` instala el paquete `pipeline` en modo editable, para que los notebooks y las pruebas lo importen sin modificar rutas. `check_environment.py` confirma que cada dependencia quedó con la versión exacta; con `--write` deja el registro en `docs/entorno.md`.
