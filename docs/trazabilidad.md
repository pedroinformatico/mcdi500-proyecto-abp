# Trazabilidad: rúbrica de la Sumativa 1 → evidencia

Lista de verificación de los 15 criterios de la rúbrica (99 puntos). Cada fila indica dónde está la evidencia en el repositorio o en el informe. Se actualiza en cada avance y se revisa completa antes de la entrega.

| # | Criterio (pts) | Qué exige el nivel Excelente | Evidencia (archivo · commit · sección del informe) | Estado |
|---|---|---|---|---|
| 1 | Portada e índice (3) | Portada institucional completa e índice automático coherente | Informe I | pendiente |
| 2 | Introducción y contextualización (6) | Contexto, situación que origina el análisis, relevancia, propósito y relación con F1–F4 | Informe II · `F1/F1_Definición.ipynb` §1 | pendiente |
| 3 | Problemática y objetivos (6) | Problemática delimitada, pregunta técnica, objetivos, alcance, restricciones y supuestos | Informe III · `F1/F1_Definición.ipynb` §2–5 | pendiente |
| 4 | Herramientas científicas (9) | NumPy, Pandas, Jupyter y Git integrados de forma coherente con el problema | Informe IV · notebooks F2 · `src/pipeline/` | pendiente |
| 5 | Reproducibilidad técnica (6) | Ambiente virtual, dependencias completas, instalación verificada, ejecución sin errores | `requirements.txt` · `docs/entorno.md` · `scripts/run_all.py` · CI | pendiente |
| 6 | Control de versiones (6) | Commits descriptivos y frecuentes, ramas, historial verificable | Historial de `git log --graph` · ramas `feature/*` | pendiente |
| 7 | Documentación del proceso (6) | Decisiones justificadas, flujo explicado, cambios con motivo e impacto | `docs/decisiones.md` · markdown de notebooks | pendiente |
| 8 | Repositorio GitHub (6) | Carpetas F1 y F2, README estructurado, commits por integrante | `README.md` · `F1/` · `F2/` · sección Contribuciones | pendiente |
| 9 | Codificación funcional (9) | Funciones con parámetros claros, flujo verificable, código limpio | `src/pipeline/` · `tests/` | pendiente |
| 10 | Preprocesamiento y transformación (6) | Limpieza exhaustiva, NA, casting, normalización, escalamiento y validación justificados | `F2/03_limpieza.ipynb` · `F2/04_transformacion.ipynb` | pendiente |
| 11 | Validación técnica (6) | Casos normales, límite y excepciones con evidencia trazable | `F2/05_validacion.ipynb` · `tests/` · `docs/evidencias/` | pendiente |
| 12 | Notebook F1 (9) | Problemática, objetivos, narrativa, código base, ejecución sin errores, coherencia con el informe | `F1/F1_Definición.ipynb` | pendiente |
| 13 | Notebook F2 (9) | Ejecución sin errores, orden obtención→validación, explicación por bloque, resultados intermedios | `F2/01`–`05` | pendiente |
| 14 | Vinculación con el mapa conceptual (6) | Cada elemento del mapa materializado o proyectado, con justificación | Informe VIII · `F1/mapa-conceptual/` · `F1/F1_Definición.ipynb` §6 | pendiente |
| 15 | Aspectos formales (6) | Formato institucional, APA 7 (≥ 5 fuentes), redacción formal | Informe completo | pendiente |

## Verificación final antes de entregar
- [ ] Ninguna celda o documento conserva el marcador "Por desarrollar".
- [ ] `python scripts/run_all.py` termina sin errores en un clon limpio y su log queda en `docs/evidencias/`.
- [ ] La ejecución en GitHub Actions está en verde en `main`.
- [ ] Cada integrante tiene commits propios identificables.
- [ ] El informe cita los mismos archivos, notebooks y commits que este documento.
