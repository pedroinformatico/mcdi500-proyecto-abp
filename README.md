# Proyecto ABP · MCDI500 Programación para la Ciencia de Datos

[![Ejecución completa](https://github.com/pedroinformatico/mcdi500-proyecto-abp/actions/workflows/ejecucion.yml/badge.svg)](https://github.com/pedroinformatico/mcdi500-proyecto-abp/actions/workflows/ejecucion.yml)

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

## Ejecución

Ejecución completa, de inicio a fin, con registro de evidencia:

```bash
python scripts/run_all.py
```

El script verifica el entorno, corre las pruebas (`pytest`) y ejecuta los notebooks de F1 y F2 en orden, guardando sus salidas. Cada corrida deja un log con fecha y hora en `docs/evidencias/`. Opciones: `--skip-notebooks` (solo entorno y pruebas) y `--no-log`.

Para trabajar un notebook de forma interactiva:

```bash
jupyter lab
```

| Notebook | Propósito | Entrada | Salida |
|---|---|---|---|
| `F1/F1_Definición.ipynb` | Definición del problema, objetivos y configuración del flujo reproducible | — | — |
| `F2/01_obtencion.ipynb` | Obtención del dataset y verificación de integridad | Fuente del dataset | `data/raw/` |
| `F2/02_exploracion.ipynb` | Exploración inicial: estructura, calidad y distribuciones | `data/raw/` | Hallazgos |
| `F2/03_limpieza.ipynb` | Limpieza y manejo de valores NA | `data/raw/` | Dataset limpio |
| `F2/04_transformacion.ipynb` | Casting, normalización y escalamiento | Dataset limpio | `data/processed/` |
| `F2/05_validacion.ipynb` | Validación del dataset resultante | `data/processed/` | Dataset validado |

## Pruebas

```bash
python -m pytest
```

Las pruebas de `tests/` cubren los módulos de `src/pipeline/` en casos normales, límite y excepciones.

## Integración continua

Cada `push` y `pull request` ejecuta `scripts/run_all.py` en GitHub Actions sobre un equipo limpio (`.github/workflows/ejecucion.yml`). El log y los notebooks ejecutados quedan como artefacto `evidencia-ejecucion` en cada corrida.
