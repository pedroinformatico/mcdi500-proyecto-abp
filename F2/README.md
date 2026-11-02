# Fase 2 · Búsqueda y recopilación activa de información

Pipeline de datos en cinco notebooks, que se ejecutan en orden:

| Notebook | Etapa | Salida |
|---|---|---|
| `01_obtencion.ipynb` | Obtención y verificación de integridad del dataset | `data/raw/` |
| `02_exploracion.ipynb` | Exploración inicial: estructura, calidad y distribuciones | Hallazgos que guían la limpieza |
| `03_limpieza.ipynb` | Limpieza, manejo de valores NA y depuración | Dataset limpio intermedio |
| `04_transformacion.ipynb` | Casting, normalización y escalamiento | `data/processed/` |
| `05_validacion.ipynb` | Validación del dataset resultante | Dataset apto para análisis posteriores |

La lógica reutilizable vive en `src/pipeline/` y se prueba en `tests/`.
