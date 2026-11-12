# Proyecto ABP · MCDI500 Programación para la Ciencia de Datos

[![Ejecución completa](https://github.com/pedroinformatico/mcdi500-proyecto-abp/actions/workflows/ejecucion.yml/badge.svg)](https://github.com/pedroinformatico/mcdi500-proyecto-abp/actions/workflows/ejecucion.yml)

Repositorio del proyecto transversal del curso MCDI500 (Magíster en Ciencia de Datos e Inteligencia Artificial, Universidad Andrés Bello).

## Grupo 5

| Integrante | GitHub |
|---|---|
| Felipe Contreras | _(por confirmar)_ |
| Cristián Cordero | [@Isonauta](https://github.com/Isonauta) |
| Pedro Hernández | [@pedroinformatico](https://github.com/pedroinformatico) |

## Descripción del proyecto

> **Por desarrollar:** problemática, objetivo general y dataset utilizado (resumen de `F1/F1_Definición.ipynb`).

## Estructura

```
F1/                  Fase 1 · definición del proyecto y mapa conceptual técnico
F2/                  Fase 2 · pipeline de datos (obtención → validación)
F3/                  Fase 3 · núcleo algorítmico, eficiencia y POO (Sumativa 2)
F4/                  Fase 4 · presentación y comunicación (Sumativa 3)
src/pipeline/        módulos reutilizables del pipeline (importables desde los notebooks)
tests/               pruebas automatizadas con pytest
data/raw/            subconjuntos congelados de la fuente y su manifiesto con SHA-256 (no se modifican)
data/processed/      datos generados por el pipeline (se regeneran, no se versionan)
data/external/       archivos nacionales descargados (temporales, no se versionan)
docs/                entorno, decisiones técnicas, trazabilidad, validación del dataset y evidencias
scripts/             obtención de datos, validador del curso, verificación del entorno y ejecución completa
```

## Datos

Datos abiertos de ChileCompra: **órdenes de compra** y **licitaciones** del sector salud en la Región de Valparaíso, septiembre 2024 y septiembre 2025. Los subconjuntos ya están en `data/raw/`, con su huella SHA-256 en `data/raw/manifest.json`. Fuente, licencia, filtro y cuidados de lectura: [`data/README.md`](data/README.md).

```bash
python scripts/fetch_data.py --verify     # comprueba que data/raw/ no cambió
python scripts/fetch_data.py --months 2025-08 2025-10 --sources oc   # agrega meses
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

## Flujo de trabajo con Git

Se usa un GitFlow adaptado a ciencia de datos:

| Rama | Uso |
|---|---|
| `main` | Versión estable; cada entrega queda marcada con un tag (`entrega-s1`, `entrega-s2`, `entrega-s3`) |
| `feature/<tema>` | Nuevas funciones, módulos o notebooks (por ejemplo `feature/f2-pipeline`) |
| `experiment/<tema>` | Pruebas de enfoques alternativos que pueden descartarse |
| `hotfix/<tema>` | Correcciones urgentes sobre `main` |

**Regla del equipo: nadie trabaja directo en `main`.** Todo cambio, también los pequeños, sigue estos pasos:

1. Actualizar `main` (`git pull`) y crear una rama para la tarea: `git checkout -b docs/f1-objetivos`.
2. Hacer commits descriptivos en esa rama y subirla: `git push -u origin docs/f1-objetivos`.
3. Abrir un pull request hacia `main` y pedir la revisión de otro integrante.
4. Unirlo con *merge commit* (no *squash*) cuando esté revisado y la ejecución automática esté en verde. Así el historial conserva los commits de cada integrante.

Convención de commits: `tipo(alcance): descripción en español`, un cambio verificable por commit.

| Tipo | Cuándo |
|---|---|
| `feat` | Nueva funcionalidad (módulo, función, notebook) |
| `fix` | Corrección de un error |
| `test` | Pruebas nuevas o ajustadas |
| `docs` | Documentación, README, decisiones |
| `build` | Entorno, dependencias, scripts de ejecución |
| `ci` | Integración continua |
| `chore` | Mantenimiento y estructura |

## Uso de IA generativa

La declaración del equipo, con el formato que completa cada integrante, está en [`DECLARACION-USO-IA.md`](DECLARACION-USO-IA.md).

## Contribuciones

| Integrante | Aportes principales |
|---|---|
| Pedro Hernández | Estructura del repositorio, entorno reproducible y ejecución automatizada |
| Cristián Cordero (usuario de GitHub: Isonauta) | Contexto del caso del F1 y redacción del informe |
