# Registro de decisiones técnicas

Cada decisión relevante del proyecto queda registrada aquí con su motivo, las alternativas descartadas y su impacto, para mantener la trazabilidad entre el informe, los notebooks y el historial de commits.

| Campo | Qué registrar |
|---|---|
| Fecha | AAAA-MM-DD |
| Fase | F1, F2, F3 o F4 |
| Decisión | Qué se decidió |
| Alternativas descartadas | Qué otras opciones se evaluaron y por qué no se eligieron |
| Justificación | Razón técnica (calidad de datos, rendimiento, reproducibilidad, coherencia con los objetivos) |
| Impacto | Qué cambia en el pipeline, el dataset o los resultados |
| Evidencia | Notebook, archivo o commit donde se implementa |

## Fase 1 · Definición

| Fecha | Decisión | Alternativas descartadas | Justificación | Impacto | Evidencia |
|---|---|---|---|---|---|
| 2026-11-02 | Estructura con carpetas por fase (F1, F2) y lógica reutilizable en `src/pipeline/` | Todo el código dentro de los notebooks | Separar la exploración (notebooks) de la lógica probada (módulos) facilita las pruebas y la reutilización en F3–F4 | Los notebooks importan funciones de `pipeline`; las pruebas viven en `tests/` | `README.md`, `src/pipeline/` |

## Fase 2 · Datos

| Fecha | Decisión | Alternativas descartadas | Justificación | Impacto | Evidencia |
|---|---|---|---|---|---|
