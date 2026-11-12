# Datos del proyecto

## Fuente

Datos abiertos de ChileCompra (Dirección de Compras y Contratación Pública), descarga masiva mensual. Términos de uso: <https://www.chilecompra.cl/terminos-y-condiciones-de-uso/>.

| Conjunto | Archivo mensual (mes sin cero: `2025-9`) | Unidad de cada fila |
|---|---|---|
| Órdenes de compra | `https://transparenciachc.blob.core.windows.net/oc-da/AAAA-M.zip` | Una línea (ítem) de una orden; la orden es `Codigo` |
| Licitaciones con ofertas | `https://transparenciachc.blob.core.windows.net/lic-da/AAAA-M.zip` | Formato largo: varias filas por licitación (`CodigoExterno`) |

## Subconjuntos en `data/raw/`

Filtro: `sector == "Salud"` y región de la unidad compradora que contiene `"Valpara"` (Región de Valparaíso). Solo se filtran filas: **los valores no se transforman**. Todo queda como texto, con el separador `;` y la codificación `latin-1` de la fuente, así que la limpieza y el *casting* se hacen y se justifican en los notebooks de F2.

| Archivo | Conjunto | Filas | Órdenes o licitaciones | Columnas | MB | Filas nacionales | SHA-256 |
|---|---|---:|---:|---:|---:|---:|---|
| `lic_2024-09_salud_valparaiso.csv` | Licitaciones | 2.726 | 136 | 110 | 4,8 | 178.603 | `e4f556a37611…` |
| `lic_2025-09_salud_valparaiso.csv` | Licitaciones | 2.361 | 130 | 110 | 4,3 | 124.680 | `d943f722f90c…` |
| `oc_2024-09_salud_valparaiso.csv` | Órdenes de compra | 12.025 | 4.598 | 78 | 20,8 | 396.516 | `fe068e328115…` |
| `oc_2025-09_salud_valparaiso.csv` | Órdenes de compra | 13.855 | 5.687 | 79 | 23,9 | 407.358 | `e33bc2d595d8…` |

Descargados el 2026-11-08. Ninguna línea mal formada. Los cuatro cumplen los requisitos de `validar_dataset.py`; el único aviso común es que hay columnas con más de 60 % de faltantes, y `lic_2024-09` tiene además 3 filas duplicadas exactas.

El detalle de cada archivo (URL, fecha de descarga, SHA-256 del zip nacional y del subconjunto, filas nacionales y líneas mal formadas) está en [`raw/manifest.json`](raw/manifest.json). El resultado del validador del curso está en [`../docs/validacion/`](../docs/validacion/).

## Cómo leerlos

```python
from pipeline.chilecompra import read_subset
from pipeline.config import RAW_DATA_DIR

oc = read_subset(RAW_DATA_DIR / "oc_2025-09_salud_valparaiso.csv")
# equivale a: pd.read_csv(ruta, sep=";", encoding="latin-1", dtype=str, keep_default_na=False)
```

## Cómo verificarlos, regenerarlos o ampliarlos

```bash
python scripts/fetch_data.py --verify                                  # huellas SHA-256
python scripts/fetch_data.py --months 2025-08 2025-10                  # agrega meses
python scripts/fetch_data.py --sources lic --months 2025-01 2025-02    # solo licitaciones
python scripts/fetch_data.py --region Biob --region-label biobio       # otra región
```

El script no reemplaza un subconjunto que ya existe salvo con `--force`. Los zip nacionales quedan en `data/external/`, que no se versiona, y se borran al terminar salvo con `--keep-zips`.

`scripts/validar_dataset.py` es copia sin cambios del validador del curso (`magistercienciadatos/Material_Didactico_Semana1`, commit `829c55e`):

```bash
python scripts/validar_dataset.py data/raw/<archivo>.csv --sep ";" --encoding latin-1 --informe docs/validacion/<archivo>.md
```

## Cuidados para F2 y el informe

- **La fuente cambia.** ChileCompra regenera los meses recientes: el archivo de órdenes de septiembre 2026 cambió entre el 02 y el 06-nov-2026. Por eso el subconjunto se versiona con su SHA-256 y no se vuelve a bajar en cada ejecución.
- **Cambio de definición por la Ley 21.634**, vigente desde el 12-dic-2024. La compra ágil subió su tope de 30 a 100 UTM y dejó de ser una causal de trato directo, así que `EsTratoDirecto` no significa lo mismo en septiembre 2024 que en septiembre 2025. Para comparar, hay que cruzarlo con `EsCompraAgil`.
- **Licitaciones sin ofertas.** El archivo `lic-da` parece excluir las licitaciones que no recibieron ofertas, lo que va en las restricciones.
- **Unir las dos fuentes.** `CodigoLicitacion` de la orden corresponde a `CodigoExterno` de la licitación. Una licitación y sus órdenes casi nunca caen en el mismo mes, así que para unirlas hay que agregar los meses previos de licitaciones con `--months`.
- **Montos.** Están en valores nominales, con coma decimal. Unas pocas órdenes están en UF (`CLF`), UTM o USD (`TipoMonedaOC`); `MontoTotalOC_PesosChilenos` las lleva a pesos.
- **Las columnas cambian entre años.** Las órdenes de septiembre 2025 traen `CodigoProyectoPlanAnualCompras`, que no existe en septiembre 2024. Las licitaciones tienen las mismas 110 columnas en ambos meses.
- **Fechas de relleno.** Las licitaciones usan `1900-01-01` en fechas que no aplican: hay que tratarlas como faltantes.
