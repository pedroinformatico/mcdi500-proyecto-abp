"""Pruebas de la limpieza y transformación de órdenes: casos normales, límite y errores."""

import pandas as pd
import pytest

from pipeline import ordenes


def make_lines(**overrides) -> pd.DataFrame:
    """Dos líneas de una misma orden y una de otra, como texto, igual que en la fuente."""
    base = {
        "periodo": ["2025-09"] * 3,
        "Codigo": ["A-1", "A-1", "B-2"],
        "Tipo": ["AG", "AG", "SE"],
        "EsTratoDirecto": ["NA", "NA", "Si"],
        "EsCompraAgil": ["Si", "Si", "No"],
        "CodigoLicitacion": ["", "", ""],
        "FechaCreacion": ["2025-09-01"] * 3,
        "FechaEnvio": ["2025-09-02", "2025-09-02", "2025-09-15"],
        "FechaAceptacion": ["2025-09-03", "2025-09-03", "NA"],
        "Estado": ["Aceptada"] * 3,
        "TipoMonedaOC": ["CLP"] * 3,
        "MontoTotalOC": ["1000,5", "1000,5", "200"],
        "MontoTotalOC_PesosChilenos": ["1000,5", "1000,5", "200"],
        "TotalNetoOC": ["840,8", "840,8", "168"],
        "Impuestos": ["159,7", "159,7", "32"],
        "totalLineaNeto": ["500", "340,8", "168"],
        "CodigoUnidadCompra": ["10", "10", "20"],
        "UnidadCompra": [" Hospital A ", " Hospital A ", "Cesfam B"],
        "OrganismoPublico": ["Servicio X"] * 3,
        "CodigoProveedor": ["7", "7", "8"],
        "NombreProveedor": ["Prov 7", "Prov 7", "Prov 8"],
    }
    base.update(overrides)
    return pd.DataFrame(base)


def run_pipeline(lines: pd.DataFrame) -> pd.DataFrame:
    typed = ordenes.cast_types(ordenes.normalize_missing(lines))
    return ordenes.aggregate_orders(ordenes.classify_modality(typed))


# --- Casos normales ---


def test_normalize_missing_convierte_marcadores_y_quita_espacios():
    clean = ordenes.normalize_missing(make_lines())
    assert clean["EsTratoDirecto"].isna().sum() == 2
    assert clean["CodigoLicitacion"].isna().all()
    assert clean.loc[0, "UnidadCompra"] == "Hospital A"


def test_parse_amount_acepta_coma_decimal():
    result = ordenes.parse_amount(pd.Series(["408039,1", "14280000"]))
    assert result.tolist() == [408039.1, 14280000.0]


def test_cast_types_asigna_tipos():
    typed = ordenes.cast_types(ordenes.normalize_missing(make_lines()))
    assert typed["MontoTotalOC_PesosChilenos"].dtype == float
    assert pd.api.types.is_datetime64_any_dtype(typed["FechaEnvio"])
    assert typed["EsCompraAgil"].tolist() == [True, True, False]


def test_aggregate_orders_no_infla_el_monto():
    orders = run_pipeline(make_lines())
    assert len(orders) == 2
    assert orders["MontoTotalOC_PesosChilenos"].sum() == pytest.approx(1200.5)
    assert orders["lineas"].tolist() == [2, 1]


def test_validate_orders_aprueba_datos_correctos():
    assert ordenes.validate_orders(run_pipeline(make_lines()))["cumple"].all()


# --- Casos límite ---


def test_compra_agil_tiene_prioridad_sobre_trato_directo():
    # En 2024 la compra ágil venía marcada además como trato directo.
    lines = make_lines(EsTratoDirecto=["Si", "Si", "Si"])
    assert run_pipeline(lines)["modalidad"].tolist() == ["Compra ágil", "Trato directo"]


def test_modalidad_convenio_marco_licitacion_y_otra():
    lines = make_lines(
        Codigo=["A-1", "B-2", "C-3"],
        Tipo=["CM", "SE", "SE"],
        EsTratoDirecto=["No", "No", "NA"],
        EsCompraAgil=["No", "No", "No"],
        CodigoLicitacion=["", "123-4-LE25", ""],
    )
    assert run_pipeline(lines)["modalidad"].tolist() == ["Convenio marco", "Licitación", "Otra"]


def test_parse_amount_deja_nan_si_no_es_numero():
    result = ordenes.parse_amount(pd.Series(["abc", None]))
    assert result.isna().all()


# --- Errores ---


def test_load_orders_avisa_si_falta_el_archivo(tmp_path):
    with pytest.raises(FileNotFoundError, match="fetch_data"):
        ordenes.load_orders(tmp_path, months=("2025-09",))


def test_validate_orders_detecta_duplicados_y_montos_negativos():
    orders = run_pipeline(make_lines())
    broken = pd.concat([orders, orders.iloc[[0]]], ignore_index=True)
    broken.loc[1, "MontoTotalOC_PesosChilenos"] = -5
    result = ordenes.validate_orders(broken).set_index("regla")["cumple"]
    assert not result["Cada orden aparece una sola vez"]
    assert not result["Ningún monto falta ni es negativo"]


def test_validate_orders_detecta_fecha_fuera_del_periodo():
    orders = run_pipeline(make_lines(FechaEnvio=["2025-08-31", "2025-08-31", "2025-09-15"]))
    result = ordenes.validate_orders(orders).set_index("regla")["cumple"]
    assert not result["La fecha de envío cae en su período"]
