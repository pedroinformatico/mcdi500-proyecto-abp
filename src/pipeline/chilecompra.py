"""Obtención reproducible de datos abiertos de ChileCompra.

Descarga los archivos mensuales de la descarga masiva de ChileCompra (órdenes de
compra y licitaciones), conserva solo las filas de un sector y una región, y guarda
el subconjunto sin transformar sus valores. Cada archivo queda registrado con su
huella SHA-256 en un manifiesto, para que cualquier integrante verifique que trabaja
exactamente con los mismos datos.

La fuente regenera los archivos recientes (el mismo mes cambia entre descargas), por
eso el subconjunto se congela en data/raw/ y el manifiesto guarda también la huella
del archivo nacional descargado.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import urllib.request
import warnings
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

BASE_URL = "https://transparenciachc.blob.core.windows.net"
TERMS_URL = "https://www.chilecompra.cl/terminos-y-condiciones-de-uso/"

# Formato de los CSV de la descarga masiva. Se leen todos los campos como texto para
# no alterar montos con coma decimal, códigos con ceros a la izquierda ni fechas.
CSV_SEPARATOR = ";"
CSV_ENCODING = "latin-1"

DEFAULT_SECTOR = "Salud"
DEFAULT_REGION = "Valpara"  # sin tilde: evita depender de la codificación del texto
DEFAULT_MONTHS = ("2024-09", "2025-09")  # antes y después de la Ley 21.634 (dic. 2024)

CHUNK_ROWS = 100_000
DOWNLOAD_BLOCK_BYTES = 1 << 20


@dataclass(frozen=True)
class Source:
    """Conjunto de la descarga masiva y las columnas que se usan para filtrarlo."""

    key: str
    container: str
    region_column: str
    description: str
    sector_column: str = "sector"


SOURCES = {
    "oc": Source("oc", "oc-da", "RegionUnidadCompra", "Órdenes de compra"),
    "lic": Source("lic", "lic-da", "RegionUnidad", "Licitaciones con ofertas"),
}


def parse_month(text: str) -> tuple[int, int]:
    """Convierte 'AAAA-MM' en (año, mes) y rechaza cualquier otro formato."""
    match = re.fullmatch(r"(\d{4})-(\d{2})", text.strip())
    if not match:
        raise ValueError(f"Mes inválido: {text!r}. Use el formato AAAA-MM, por ejemplo 2025-09.")
    year, month = int(match.group(1)), int(match.group(2))
    if not 1 <= month <= 12:
        raise ValueError(f"Mes fuera de rango en {text!r}: debe estar entre 01 y 12.")
    return year, month


def source_url(source: Source, year: int, month: int) -> str:
    """URL del archivo mensual. La fuente no usa cero a la izquierda en el mes (2025-9)."""
    return f"{BASE_URL}/{source.container}/{year}-{month}.zip"


def subset_filename(source: Source, year: int, month: int, sector: str, region_label: str) -> str:
    """Nombre del subconjunto, por ejemplo oc_2025-09_salud_valparaiso.csv."""
    return f"{source.key}_{year}-{month:02d}_{_slug(sector)}_{_slug(region_label)}.csv"


def sha256_file(path: Path) -> str:
    """Huella SHA-256 de un archivo, leída por bloques para no cargarlo entero en memoria."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(DOWNLOAD_BLOCK_BYTES), b""):
            digest.update(block)
    return digest.hexdigest()


def download(url: str, destination: Path, timeout: int = 120) -> Path:
    """Descarga un archivo por bloques y lo deja en su lugar solo si llegó completo.

    El archivo se escribe primero como .part: si la conexión se corta, no queda un zip
    truncado con el nombre definitivo. `timeout` aplica a cada lectura, no al total,
    porque los archivos nacionales tardan varios minutos en bajar.
    """
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_name(destination.name + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": "mcdi500-proyecto-abp"})
    with urllib.request.urlopen(request, timeout=timeout) as response, open(partial, "wb") as out:
        expected = response.headers.get("Content-Length")
        shutil.copyfileobj(response, out, DOWNLOAD_BLOCK_BYTES)
    received = partial.stat().st_size
    if expected is not None and received != int(expected):
        partial.unlink()
        raise OSError(f"Descarga incompleta de {url}: {received} de {expected} bytes.")
    if not zipfile.is_zipfile(partial):
        partial.unlink()
        raise OSError(f"El archivo descargado de {url} no es un zip válido.")
    partial.replace(destination)
    return destination


def filter_zip(
    zip_path: Path,
    source: Source,
    sector: str = DEFAULT_SECTOR,
    region: str = DEFAULT_REGION,
) -> tuple[pd.DataFrame, int, int]:
    """Lee los CSV del zip por partes y conserva las filas del sector y la región.

    Devuelve el subconjunto (todas las columnas como texto), el total de filas
    nacionales leídas y la cantidad de líneas mal formadas que pandas omitió, para
    informarlas en vez de perderlas en silencio.
    """
    with zipfile.ZipFile(zip_path) as archive:
        members = [info for info in archive.infolist() if info.filename.lower().endswith(".csv")]
        if not members:
            raise ValueError(f"{zip_path} no contiene archivos CSV.")
        parts, total_rows, skipped = [], 0, 0
        for member in members:
            with archive.open(member) as handle, warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                reader = pd.read_csv(
                    handle,
                    sep=CSV_SEPARATOR,
                    encoding=CSV_ENCODING,
                    dtype=str,
                    keep_default_na=False,
                    chunksize=CHUNK_ROWS,
                    on_bad_lines="warn",
                )
                for chunk in reader:
                    missing = {source.sector_column, source.region_column} - set(chunk.columns)
                    if missing:
                        raise KeyError(f"Faltan columnas en {member.filename}: {sorted(missing)}")
                    total_rows += len(chunk)
                    keep = chunk[source.sector_column].str.strip().eq(sector) & chunk[
                        source.region_column
                    ].str.contains(region, regex=False)
                    parts.append(chunk[keep])
            skipped += sum(str(w.message).count("Skipping line") for w in caught)
    subset = pd.concat(parts, ignore_index=True)
    return subset, total_rows, skipped


def save_subset(subset: pd.DataFrame, path: Path) -> Path:
    """Guarda el subconjunto con el mismo separador y codificación de la fuente."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    subset.to_csv(path, sep=CSV_SEPARATOR, encoding=CSV_ENCODING, index=False)
    return path


def read_subset(path: Path) -> pd.DataFrame:
    """Lee un subconjunto guardado, con todas las columnas como texto (sin conversiones)."""
    return pd.read_csv(path, sep=CSV_SEPARATOR, encoding=CSV_ENCODING, dtype=str, keep_default_na=False)


def load_manifest(path: Path) -> dict:
    """Manifiesto de data/raw/: un registro por subconjunto, indexado por nombre de archivo."""
    path = Path(path)
    if not path.exists():
        return {"files": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def write_manifest(manifest: dict, path: Path) -> None:
    manifest["files"] = dict(sorted(manifest["files"].items()))
    Path(path).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_record(
    source: Source,
    url: str,
    zip_path: Path,
    subset_path: Path,
    subset: pd.DataFrame,
    total_rows: int,
    skipped_lines: int,
    sector: str,
    region: str,
) -> dict:
    """Registro de procedencia de un subconjunto: de dónde salió, cómo y con qué huella."""
    return {
        "dataset": source.description,
        "url": url,
        "license": TERMS_URL,
        "downloaded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_zip_sha256": sha256_file(zip_path),
        "source_zip_bytes": Path(zip_path).stat().st_size,
        "national_rows": total_rows,
        "skipped_malformed_lines": skipped_lines,
        "filter": {
            source.sector_column: f"== {sector!r} (sin espacios al inicio ni al final)",
            source.region_column: f"contiene {region!r}",
        },
        "rows": len(subset),
        "columns": subset.shape[1],
        "sha256": sha256_file(subset_path),
    }


def verify_manifest(raw_dir: Path, manifest_path: Path) -> dict[str, bool]:
    """Comprueba que cada archivo del manifiesto existe y conserva su SHA-256."""
    manifest = load_manifest(manifest_path)
    results = {}
    for name, record in manifest["files"].items():
        path = Path(raw_dir) / name
        results[name] = path.exists() and sha256_file(path) == record["sha256"]
    return results


def _slug(text: str) -> str:
    """Texto en minúsculas, sin tildes ni espacios, para usarlo en nombres de archivo."""
    table = str.maketrans("áéíóúüñ", "aeiouun")
    return re.sub(r"[^a-z0-9]+", "-", text.lower().translate(table)).strip("-")
