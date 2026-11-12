"""Descarga y congela los datos del proyecto (ChileCompra: órdenes de compra y licitaciones).

Por cada conjunto y mes: descarga el archivo nacional a data/external/ (no se versiona),
conserva las filas del sector y la región, guarda el subconjunto en data/raw/ y registra
su procedencia y SHA-256 en data/raw/manifest.json.

Uso:
    python scripts/fetch_data.py                          # oc y lic, sept. 2024 y sept. 2025
    python scripts/fetch_data.py --sources lic --months 2025-01 2025-02
    python scripts/fetch_data.py --region Biob --region-label biobio
    python scripts/fetch_data.py --verify                 # solo comprueba las huellas

Si un subconjunto ya existe, no se vuelve a descargar (use --force para reemplazarlo):
la fuente regenera los meses recientes y una nueva descarga puede traer otros datos.
"""

import argparse
import sys
from pathlib import Path

from pipeline import chilecompra as cc
from pipeline.config import DATA_DIR, RAW_DATA_DIR

EXTERNAL_DIR = DATA_DIR / "external"  # archivos nacionales descargados (no se versionan)
MANIFEST_PATH = RAW_DATA_DIR / "manifest.json"


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--sources", nargs="+", choices=sorted(cc.SOURCES), default=sorted(cc.SOURCES))
    parser.add_argument("--months", nargs="+", default=list(cc.DEFAULT_MONTHS), help="Meses AAAA-MM")
    parser.add_argument("--sector", default=cc.DEFAULT_SECTOR)
    parser.add_argument("--region", default=cc.DEFAULT_REGION, help="Texto que debe contener la región")
    parser.add_argument("--region-label", default="valparaiso", help="Región en el nombre del archivo")
    parser.add_argument("--force", action="store_true", help="Reemplaza subconjuntos existentes")
    parser.add_argument("--keep-zips", action="store_true", help="Conserva los zip nacionales")
    parser.add_argument("--verify", action="store_true", help="Solo verifica el manifiesto")
    return parser.parse_args(argv)


def verify() -> int:
    results = cc.verify_manifest(RAW_DATA_DIR, MANIFEST_PATH)
    if not results:
        print(f"No hay archivos registrados en {MANIFEST_PATH}.")
        return 1
    for name, ok in results.items():
        print(f"{'OK   ' if ok else 'FALLA'} {name}")
    return 0 if all(results.values()) else 1


def fetch(args) -> int:
    months = [cc.parse_month(text) for text in args.months]  # valida antes de descargar nada
    manifest = cc.load_manifest(MANIFEST_PATH)
    for key in args.sources:
        source = cc.SOURCES[key]
        for year, month in months:
            name = cc.subset_filename(source, year, month, args.sector, args.region_label)
            subset_path = RAW_DATA_DIR / name
            if subset_path.exists() and not args.force:
                print(f"[omitido] {name} ya existe (use --force para reemplazarlo)")
                continue
            url = cc.source_url(source, year, month)
            zip_path = EXTERNAL_DIR / f"{source.container}_{year}-{month}.zip"
            if not zip_path.exists():
                print(f"[descarga] {url}", flush=True)
                cc.download(url, zip_path)
            print(f"[filtro]   {zip_path.name}: {args.sector} · región contiene {args.region!r}", flush=True)
            subset, total, skipped = cc.filter_zip(zip_path, source, args.sector, args.region)
            if subset.empty:
                print(f"[aviso]    {name}: el filtro no dejó filas; no se guarda", file=sys.stderr)
                continue
            cc.save_subset(subset, subset_path)
            record = cc.build_record(
                source, url, zip_path, subset_path, subset, total, skipped, args.sector, args.region
            )
            manifest["files"][name] = record
            cc.write_manifest(manifest, MANIFEST_PATH)
            print(
                f"[listo]    {name}: {record['rows']:,} filas × {record['columns']} columnas "
                f"de {total:,} nacionales · líneas omitidas: {skipped} · sha256 {record['sha256'][:12]}…",
                flush=True,
            )
            if not args.keep_zips:
                zip_path.unlink()
    return 0


def main(argv=None) -> int:
    args = parse_args(argv)
    return verify() if args.verify else fetch(args)


if __name__ == "__main__":
    sys.exit(main())
