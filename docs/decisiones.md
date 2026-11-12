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
| 2026-11-08 | Dataset: datos abiertos de ChileCompra, órdenes de compra y licitaciones del sector salud en la Región de Valparaíso, septiembre 2024 y septiembre 2025 (período confirmado el 2026-11-11) | Egresos hospitalarios del DEIS (ya asignado a otro equipo), atenciones de urgencia del DEIS, despachos EMS de Nueva York | Fuente oficial con términos de uso, dentro de los últimos cinco años y sin datos personales; ambos conjuntos pasan `validar_dataset.py`. El tema es contingente: la Ley 21.634 (vigente desde el 12-dic-2024) da un antes y un después en el mismo mes del año. Las dos fuentes se vinculan por el código de licitación | Dos conjuntos relacionados en `data/raw/`. El informe debe declarar los límites: dos meses, una región, montos nominales | `data/README.md` · `data/raw/manifest.json` · `docs/validacion/` |

## Fase 2 · Datos

| Fecha | Decisión | Alternativas descartadas | Justificación | Impacto | Evidencia |
|---|---|---|---|---|---|
| 2026-11-08 | Obtención por script (`scripts/fetch_data.py`) y subconjunto congelado en `data/raw/` con SHA-256 | Descargar la fuente en cada ejecución; versionar el archivo nacional completo | ChileCompra regenera los meses recientes (el mismo archivo de septiembre 2026 cambió entre el 02 y el 06-nov-2026), así que una nueva descarga no garantiza los mismos datos; el archivo nacional pesa cerca de 100 MB por mes | Los notebooks leen `data/raw/` y pueden verificar las huellas; ampliar meses o cambiar región es un parámetro del script | `scripts/fetch_data.py` · `src/pipeline/chilecompra.py` · `tests/test_chilecompra.py` |
| 2026-11-11 | Conservar las filas con datos ausentes y convertir los marcadores (`''` y `'NA'`) en NA reales | Eliminar las filas con NA; imputar valores | El 38 % sin dato de `EsTratoDirecto` en 2025 corresponde a compras ágiles: eliminarlas borraría una modalidad completa. Imputar datos del proveedor distorsionaría un análisis territorial | Ninguna fila se pierde en la limpieza | `F2/03_limpieza.ipynb` · `ordenes.normalize_missing` |
| 2026-11-11 | Crear la variable `modalidad`, que evalúa primero la compra ágil | Usar `EsTratoDirecto` tal como viene | Desde la Ley 21.634 la compra ágil dejó de registrarse como trato directo: el campo original mostraría una caída falsa entre 2024 y 2025 | Los dos períodos quedan comparables | `F2/04_transformacion.ipynb` · `ordenes.classify_modality` |
| 2026-11-11 | Agregar a una fila por orden antes de sumar montos | Sumar sobre las líneas de detalle | El monto total de la orden se repite en cada línea: sumar líneas infla el gasto 3,9 veces | El dataset procesado tiene 10.285 órdenes | `F2/04_transformacion.ipynb` · `ordenes.aggregate_orders` |
| 2026-11-11 | Usar `MontoTotalOC_PesosChilenos` y no aplicar normalización ni escalamiento | Convertir monedas con valores propios; escalar los montos | La fuente ya entrega en pesos las 25 líneas emitidas en UF, UTM o dólares. Los indicadores son proporciones y sumas, que deben conservar su unidad | Montos nominales en pesos; el escalamiento se evalúa en F3 | `F2/04_transformacion.ipynb` |
| 2026-11-11 | Procesar solo órdenes de compra en este avance | Cruzar órdenes con licitaciones | Una licitación y sus órdenes casi nunca caen en el mismo mes: el cruce exige descargar meses previos | Las licitaciones quedan en `data/raw/` para una fase posterior | `data/README.md` · `F2/05_validacion.ipynb` |
