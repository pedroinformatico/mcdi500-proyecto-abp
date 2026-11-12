"""Pruebas de la obtención de datos de ChileCompra.

No usan la red: construyen zips pequeños con el mismo formato de la descarga masiva
(separador ';', codificación latin-1) para probar el filtro, las huellas y el manifiesto.
"""

import zipfile

import pytest

from pipeline import chilecompra as cc

OC = cc.SOURCES["oc"]
HEADER = "Codigo;sector;RegionUnidadCompra;MontoTotalOC\n"


def make_zip(tmp_path, body, name="2025-9.csv", header=HEADER):
    path = tmp_path / "fuente.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(name, (header + body).encode("latin-1"))
    return path


# --- Meses y URL -------------------------------------------------------------

def test_parse_month_accepts_year_and_month():
    assert cc.parse_month("2025-09") == (2025, 9)
    assert cc.parse_month(" 2024-12 ") == (2024, 12)


@pytest.mark.parametrize("text", ["2025-13", "2025-00", "25-09", "2025/09", "septiembre"])
def test_parse_month_rejects_invalid_text(text):
    with pytest.raises(ValueError):
        cc.parse_month(text)


def test_source_url_has_no_leading_zero_in_month():
    # La fuente publica 2025-9.zip, no 2025-09.zip.
    assert cc.source_url(OC, 2025, 9).endswith("/oc-da/2025-9.zip")
    assert cc.source_url(cc.SOURCES["lic"], 2024, 11).endswith("/lic-da/2024-11.zip")


def test_subset_filename_is_ascii_and_zero_padded():
    assert cc.subset_filename(OC, 2024, 9, "Salud", "Valparaíso") == "oc_2024-09_salud_valparaiso.csv"


# --- Filtro ------------------------------------------------------------------

def test_filter_keeps_only_sector_and_region(tmp_path):
    body = (
        "1;Salud;Región de Valparaíso;100,5\n"
        "2; Salud ;Región de Valparaíso;200\n"  # espacios alrededor del sector
        "3;Salud;Región Metropolitana de Santiago;300\n"
        "4;Educación;Región de Valparaíso;400\n"
    )
    subset, total, skipped = cc.filter_zip(make_zip(tmp_path, body), OC)
    assert list(subset["Codigo"]) == ["1", "2"]
    assert total == 4 and skipped == 0


def test_filter_preserves_values_as_text(tmp_path):
    # Montos con coma decimal y códigos con ceros a la izquierda no se convierten.
    subset, _, _ = cc.filter_zip(make_zip(tmp_path, "0012;Salud;Región de Valparaíso;100,5\n"), OC)
    assert subset.loc[0, "Codigo"] == "0012"
    assert subset.loc[0, "MontoTotalOC"] == "100,5"


def test_filter_returns_empty_frame_when_nothing_matches(tmp_path):
    subset, total, _ = cc.filter_zip(make_zip(tmp_path, "1;Salud;Región del Biobío;1\n"), OC)
    assert subset.empty and total == 1


def test_filter_counts_malformed_lines(tmp_path):
    body = "1;Salud;Región de Valparaíso;1\n2;Salud;Región de Valparaíso;1;sobra;otra\n"
    subset, _, skipped = cc.filter_zip(make_zip(tmp_path, body), OC)
    assert len(subset) == 1 and skipped == 1


def test_filter_fails_when_region_column_is_missing(tmp_path):
    path = make_zip(tmp_path, "1;Salud;x\n", header="Codigo;sector;OtraColumna\n")
    with pytest.raises(KeyError, match="RegionUnidadCompra"):
        cc.filter_zip(path, OC)


def test_filter_fails_when_zip_has_no_csv(tmp_path):
    path = tmp_path / "vacio.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("LEAME.txt", "sin datos")
    with pytest.raises(ValueError, match="no contiene archivos CSV"):
        cc.filter_zip(path, OC)


# --- Huellas y manifiesto ----------------------------------------------------

def test_sha256_matches_known_value(tmp_path):
    path = tmp_path / "abc.txt"
    path.write_bytes(b"abc")
    assert cc.sha256_file(path) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_saved_subset_round_trips_and_manifest_detects_changes(tmp_path):
    zip_path = make_zip(tmp_path, "1;Salud;Región de Valparaíso;100,5\n")
    subset, total, skipped = cc.filter_zip(zip_path, OC)
    raw_dir = tmp_path / "raw"
    subset_path = cc.save_subset(subset, raw_dir / "oc_2025-09_salud_valparaiso.csv")
    assert cc.read_subset(subset_path).equals(subset)

    record = cc.build_record(OC, "url", zip_path, subset_path, subset, total, skipped, "Salud", "Valpara")
    manifest_path = raw_dir / "manifest.json"
    cc.write_manifest({"files": {subset_path.name: record}}, manifest_path)
    assert cc.verify_manifest(raw_dir, manifest_path) == {subset_path.name: True}

    subset_path.write_text("alterado", encoding="latin-1")
    assert cc.verify_manifest(raw_dir, manifest_path) == {subset_path.name: False}


def test_verify_reports_missing_file(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    cc.write_manifest({"files": {"falta.csv": {"sha256": "0" * 64}}}, manifest_path)
    assert cc.verify_manifest(tmp_path, manifest_path) == {"falta.csv": False}


def test_load_manifest_without_file_returns_empty(tmp_path):
    assert cc.load_manifest(tmp_path / "no-existe.json") == {"files": {}}
