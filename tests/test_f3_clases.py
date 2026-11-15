"""Pruebas de la Fase 3: las clases del pipeline deben hacer lo mismo que las funciones de la Fase 2.

Cubre los tres escenarios que pide la rúbrica (II.c): caso normal, caso límite y excepción,
más la prueba de regresión contra el resultado de la Fase 2.

Cómo funciona
-------------
La referencia es la cadena de funciones de la Fase 2 (`pipeline.ordenes`), que ya existe.
Las clases de la Fase 3 se buscan solas en los módulos de `CANDIDATOS_MODULOS`. Mientras no
existan, las pruebas de clases se saltan (skip) y las de la referencia sí corren.

Para adaptarlas a la interfaz acordada basta con editar el bloque ADAPTAR:
nombre del módulo, nombre de la clase base y la función que arma el pipeline.
"""

from __future__ import annotations

import importlib
import inspect

import pandas as pd
import pytest

from pipeline import config, ordenes
from test_ordenes import make_lines  # helper de las pruebas de la Fase 2

# ---------------------------------------------------------------------------
# ADAPTAR: lo único que hay que tocar cuando Pedro fije la interfaz
# ---------------------------------------------------------------------------
CANDIDATOS_MODULOS = (
    "pipeline.transformadores",
    "pipeline.clases",
    "pipeline.core",
    "pipeline.flujo",
)
NOMBRE_CLASE_BASE = "Transformador"
NOMBRE_CLASE_PIPELINE = "Pipeline"
NOMBRE_FUNCION_FABRICA = "construir_pipeline"  # opcional: devuelve el pipeline ya armado

# Si una clase hija necesita argumentos para construirse, indicarlos aquí:
#   FABRICAS_HIJAS = {"CodificadorModalidad": lambda cls: cls(columna="modalidad")}
FABRICAS_HIJAS: dict = {}

# Cada paso espera la salida del paso anterior. Si una hija no acepta las líneas crudas,
# indicar qué entrada recibe:
#   ENTRADAS_HIJAS = {"Agregador": lambda: referencia_hasta_modalidad(make_lines())}
ENTRADAS_HIJAS: dict = {}
# ---------------------------------------------------------------------------


def referencia_f2(lines: pd.DataFrame) -> pd.DataFrame:
    """El resultado de la Fase 2: la cadena de funciones tal como está en `ordenes.py`."""
    typed = ordenes.cast_types(ordenes.normalize_missing(lines))
    return ordenes.aggregate_orders(ordenes.classify_modality(typed))


def _modulos_disponibles():
    for nombre in CANDIDATOS_MODULOS:
        try:
            yield importlib.import_module(nombre)
        except ModuleNotFoundError:
            continue


def _buscar_clase(nombre: str):
    for modulo in _modulos_disponibles():
        if hasattr(modulo, nombre):
            return getattr(modulo, nombre)
    return None


def _hijas(base: type) -> list[type]:
    """Todas las subclases (directas o no) de la clase base, en los módulos candidatos."""
    encontradas = []
    for modulo in _modulos_disponibles():
        for _, cls in inspect.getmembers(modulo, inspect.isclass):
            if cls is not base and issubclass(cls, base) and cls not in encontradas:
                encontradas.append(cls)
    return encontradas


@pytest.fixture(scope="module")
def clase_base():
    base = _buscar_clase(NOMBRE_CLASE_BASE)
    if base is None:
        pytest.skip(f"Aún no existe la clase base '{NOMBRE_CLASE_BASE}' en {CANDIDATOS_MODULOS}")
    return base


@pytest.fixture()
def pipeline_clases():
    """Arma el pipeline de clases. Primero busca una función fábrica, luego la clase Pipeline."""
    for modulo in _modulos_disponibles():
        fabrica = getattr(modulo, NOMBRE_FUNCION_FABRICA, None)
        if callable(fabrica):
            return fabrica()
    cls = _buscar_clase(NOMBRE_CLASE_PIPELINE)
    if cls is None:
        pytest.skip("Aún no existe el pipeline de clases (ni función fábrica ni clase Pipeline)")
    try:
        return cls()
    except TypeError:
        pytest.skip(
            f"'{NOMBRE_CLASE_PIPELINE}' necesita argumentos: definir '{NOMBRE_FUNCION_FABRICA}()' "
            "en el módulo de clases o ajustar este fixture"
        )


@pytest.fixture(scope="module")
def lineas_reales() -> pd.DataFrame:
    return ordenes.load_orders(config.RAW_DATA_DIR)


# ===========================================================================
# 0. La referencia de la Fase 2 (corre desde ya, sin depender de las clases)
# ===========================================================================


def test_referencia_f2_deja_una_fila_por_orden(lineas_reales):
    resultado = referencia_f2(lineas_reales)
    assert resultado["Codigo"].is_unique
    assert len(resultado) == lineas_reales["Codigo"].nunique()


def test_referencia_f2_cumple_todas_las_reglas_de_calidad(lineas_reales):
    reglas = ordenes.validate_orders(referencia_f2(lineas_reales))
    assert reglas["cumple"].all(), reglas[~reglas["cumple"]]


def test_referencia_f2_no_modifica_la_entrada():
    lineas = make_lines()
    copia = lineas.copy(deep=True)
    referencia_f2(lineas)
    pd.testing.assert_frame_equal(lineas, copia)


# ===========================================================================
# 1. Caso normal
# ===========================================================================


def test_normal_pipeline_de_clases_igual_a_f2_sobre_datos_reales(pipeline_clases, lineas_reales):
    """La prueba que más rinde: la reorganización no cambió el resultado."""
    esperado = referencia_f2(lineas_reales)
    obtenido = pipeline_clases.ajustar(lineas_reales).transformar(lineas_reales)
    pd.testing.assert_frame_equal(
        obtenido.reset_index(drop=True), esperado.reset_index(drop=True), check_like=True
    )


def test_normal_no_pierde_ni_duplica_ordenes(pipeline_clases, lineas_reales):
    obtenido = pipeline_clases.ajustar(lineas_reales).transformar(lineas_reales)
    assert len(obtenido) == lineas_reales["Codigo"].nunique()


def test_normal_ajustar_devuelve_self(pipeline_clases):
    """Permite encadenar: pipeline.ajustar(df).transformar(df)."""
    assert pipeline_clases.ajustar(make_lines()) is pipeline_clases


def test_normal_resultado_valido_segun_reglas_de_calidad(pipeline_clases, lineas_reales):
    obtenido = pipeline_clases.ajustar(lineas_reales).transformar(lineas_reales)
    reglas = ordenes.validate_orders(obtenido)
    assert reglas["cumple"].all(), reglas[~reglas["cumple"]]


# ===========================================================================
# 2. Casos límite: situaciones extremas pero válidas
# ===========================================================================


def test_limite_una_sola_orden(pipeline_clases):
    una = make_lines().iloc[[2]].reset_index(drop=True)  # solo la orden B-2
    obtenido = pipeline_clases.ajustar(una).transformar(una)
    assert len(obtenido) == 1


def test_limite_sin_ningun_dato_ausente(pipeline_clases):
    """Columnas completas: el pipeline no debe fallar ni alterar valores."""
    lineas = make_lines(FechaAceptacion=["2025-09-03"] * 3, EsTratoDirecto=["No"] * 3)
    esperado = referencia_f2(lineas)
    obtenido = pipeline_clases.ajustar(lineas).transformar(lineas)
    pd.testing.assert_frame_equal(
        obtenido.reset_index(drop=True), esperado.reset_index(drop=True), check_like=True
    )


def test_limite_una_sola_modalidad(pipeline_clases):
    lineas = make_lines(EsCompraAgil=["Si"] * 3, EsTratoDirecto=["NA"] * 3)
    obtenido = pipeline_clases.ajustar(lineas).transformar(lineas)
    assert set(obtenido["modalidad"]) == {"Compra ágil"}


def test_limite_todo_ajustado_con_entrenamiento_se_aplica_a_otro_conjunto(pipeline_clases):
    """Ajustar con un conjunto y transformar otro no debe fallar (el esquema se conserva)."""
    entrenamiento = make_lines()
    otro = make_lines(Codigo=["C-3", "C-3", "D-4"], MontoTotalOC_PesosChilenos=["50", "50", "70"])
    pipeline_clases.ajustar(entrenamiento)
    obtenido = pipeline_clases.transformar(otro)
    assert len(obtenido) == 2


# ===========================================================================
# 3. Excepciones: entradas que deben fallar, y fallar bien
# ===========================================================================


def test_excepcion_transformar_antes_de_ajustar(pipeline_clases):
    with pytest.raises(RuntimeError):
        pipeline_clases.transformar(make_lines())


def test_excepcion_columna_ausente(pipeline_clases):
    sin_monto = make_lines().drop(columns=["MontoTotalOC_PesosChilenos"])
    with pytest.raises((KeyError, ValueError)):
        pipeline_clases.ajustar(sin_monto).transformar(sin_monto)


# ===========================================================================
# 4. Contrato de las clases: encapsulamiento, herencia y polimorfismo (III.a)
# ===========================================================================


def test_herencia_existen_al_menos_dos_hijas(clase_base):
    hijas = _hijas(clase_base)
    assert len(hijas) >= 2, f"La guía pide una base y al menos dos hijas; hay {len(hijas)}: {hijas}"


def _instanciar(cls):
    fabrica = FABRICAS_HIJAS.get(cls.__name__)
    try:
        return fabrica(cls) if fabrica else cls()
    except TypeError:
        pytest.skip(f"{cls.__name__} necesita argumentos: agregarla a FABRICAS_HIJAS")


def _todas_las_hijas():
    base = _buscar_clase(NOMBRE_CLASE_BASE)
    return _hijas(base) if base is not None else []


@pytest.mark.parametrize("cls", _todas_las_hijas() or [None], ids=lambda c: getattr(c, "__name__", "sin-clases-aun"))
def test_polimorfismo_todas_las_hijas_ofrecen_ajustar_y_transformar(cls):
    if cls is None:
        pytest.skip("Aún no hay clases hijas")
    for metodo in ("ajustar", "transformar"):
        assert callable(getattr(cls, metodo, None)), f"{cls.__name__} no ofrece {metodo}()"


@pytest.mark.parametrize("cls", _todas_las_hijas() or [None], ids=lambda c: getattr(c, "__name__", "sin-clases-aun"))
def test_encapsulamiento_hija_falla_si_no_se_ajusto(cls):
    if cls is None:
        pytest.skip("Aún no hay clases hijas")
    with pytest.raises(RuntimeError):
        _instanciar(cls).transformar(make_lines())


def referencia_hasta_modalidad(lines: pd.DataFrame) -> pd.DataFrame:
    """Entrada típica de un paso intermedio: líneas ya normalizadas, tipadas y clasificadas."""
    typed = ordenes.cast_types(ordenes.normalize_missing(lines))
    return ordenes.classify_modality(typed)


@pytest.mark.parametrize("cls", _todas_las_hijas() or [None], ids=lambda c: getattr(c, "__name__", "sin-clases-aun"))
def test_encapsulamiento_hija_no_modifica_la_entrada(cls):
    if cls is None:
        pytest.skip("Aún no hay clases hijas")
    entrada = ENTRADAS_HIJAS.get(cls.__name__, lambda: make_lines())()
    copia = entrada.copy(deep=True)
    paso = _instanciar(cls)
    try:
        paso.ajustar(entrada).transformar(entrada)
    except (AttributeError, KeyError, TypeError, ValueError):
        pytest.skip(f"{cls.__name__} no acepta esta entrada: definirla en ENTRADAS_HIJAS")
    pd.testing.assert_frame_equal(entrada, copia)
