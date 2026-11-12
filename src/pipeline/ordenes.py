"""Limpieza, transformación y validación de las órdenes de compra de ChileCompra.

Cada función hace una sola tarea y devuelve un DataFrame nuevo, sin modificar el
que recibe. Los notebooks de F2 las llaman en orden:

    load_orders -> normalize_missing -> cast_types -> classify_modality
    -> aggregate_orders -> validate_orders
"""

from pathlib import Path

import numpy as np
import pandas as pd

from . import chilecompra as cc

# Textos con que la fuente marca un dato ausente.
MISSING_MARKERS = ("", "NA")

AMOUNT_COLUMNS = ("MontoTotalOC", "MontoTotalOC_PesosChilenos", "TotalNetoOC", "Impuestos", "totalLineaNeto")
DATE_COLUMNS = ("FechaCreacion", "FechaEnvio", "FechaAceptacion")
BOOLEAN_COLUMNS = ("EsTratoDirecto", "EsCompraAgil")

MODALITIES = ("Compra ágil", "Trato directo", "Convenio marco", "Licitación", "Otra")

# Columnas que describen a la orden completa (se repiten en cada una de sus líneas).
ORDER_COLUMNS = (
    "periodo",
    "Codigo",
    "FechaEnvio",
    "Estado",
    "modalidad",
    "TipoMonedaOC",
    "MontoTotalOC_PesosChilenos",
    "CodigoUnidadCompra",
    "UnidadCompra",
    "OrganismoPublico",
    "CodigoProveedor",
    "NombreProveedor",
)


def load_orders(raw_dir: Path, months: tuple[str, ...] = cc.DEFAULT_MONTHS) -> pd.DataFrame:
    """Une los subconjuntos mensuales de órdenes y marca cada fila con su período (AAAA-MM).

    Las columnas que solo existen en un mes quedan vacías en el otro.
    """
    parts = []
    for month in months:
        path = Path(raw_dir) / f"oc_{month}_salud_valparaiso.csv"
        if not path.exists():
            raise FileNotFoundError(f"No existe {path.name}: ejecute scripts/fetch_data.py")
        part = cc.read_subset(path)
        part.insert(0, "periodo", month)
        parts.append(part)
    return pd.concat(parts, ignore_index=True).fillna("")


def normalize_missing(orders: pd.DataFrame) -> pd.DataFrame:
    """Quita espacios sobrantes y convierte los marcadores de ausencia ('' y 'NA') en NA reales."""
    clean = orders.apply(lambda column: column.str.strip())
    return clean.mask(clean.isin(MISSING_MARKERS))


def parse_amount(values: pd.Series) -> pd.Series:
    """Convierte montos escritos con coma decimal ('408039,1') en números.

    Lo que no sea un número queda como NaN en lugar de detener el proceso.
    """
    return pd.to_numeric(values.str.replace(",", ".", regex=False), errors="coerce")


def cast_types(orders: pd.DataFrame) -> pd.DataFrame:
    """Asigna a cada variable su tipo: montos numéricos, fechas y Sí/No como booleanos."""
    typed = orders.copy()
    for column in AMOUNT_COLUMNS:
        typed[column] = parse_amount(typed[column])
    for column in DATE_COLUMNS:
        typed[column] = pd.to_datetime(typed[column], format="%Y-%m-%d", errors="coerce")
    for column in BOOLEAN_COLUMNS:
        typed[column] = typed[column].map({"Si": True, "No": False}).astype("boolean")
    return typed


def classify_modality(orders: pd.DataFrame) -> pd.DataFrame:
    """Agrega 'modalidad', comparable entre 2024 y 2025.

    Desde la Ley 21.634 la compra ágil dejó de registrarse como trato directo, y en
    2025 esas órdenes traen EsTratoDirecto vacío. Por eso la compra ágil se evalúa
    primero: así una misma orden recibe la misma etiqueta en ambos años.
    """
    conditions = [
        orders["EsCompraAgil"].fillna(False).astype(bool),
        orders["EsTratoDirecto"].fillna(False).astype(bool),
        orders["Tipo"].eq("CM").fillna(False),
        orders["CodigoLicitacion"].notna(),
    ]
    labeled = orders.copy()
    labeled["modalidad"] = np.select(conditions, MODALITIES[:4], default=MODALITIES[4])
    return labeled


def aggregate_orders(lines: pd.DataFrame) -> pd.DataFrame:
    """Deja una fila por orden de compra.

    El archivo trae una fila por producto, y el monto total de la orden se repite
    en cada una: sumarlo directamente lo inflaría.
    """
    orders = lines.groupby("Codigo", sort=False)[list(ORDER_COLUMNS)].first()
    orders["lineas"] = lines.groupby("Codigo", sort=False).size()
    return orders.reset_index(drop=True)


def validate_orders(orders: pd.DataFrame, months: tuple[str, ...] = cc.DEFAULT_MONTHS) -> pd.DataFrame:
    """Comprueba las reglas de calidad del dataset final y devuelve una fila por regla."""
    amount = orders["MontoTotalOC_PesosChilenos"]
    sent_month = orders["FechaEnvio"].dt.strftime("%Y-%m")
    rules = {
        "Hay al menos una orden": len(orders) > 0,
        "Cada orden aparece una sola vez": orders["Codigo"].is_unique,
        "Ningún monto falta ni es negativo": bool(amount.notna().all() and (amount >= 0).all()),
        "Todas las órdenes tienen proveedor y unidad de compra": bool(
            orders[["CodigoProveedor", "CodigoUnidadCompra"]].notna().all().all()
        ),
        "La modalidad solo toma valores conocidos": bool(orders["modalidad"].isin(MODALITIES).all()),
        "El período es uno de los meses del estudio": bool(orders["periodo"].isin(months).all()),
        "La fecha de envío cae en su período": bool((sent_month == orders["periodo"]).all()),
    }
    return pd.DataFrame({"regla": list(rules), "cumple": list(rules.values())})
