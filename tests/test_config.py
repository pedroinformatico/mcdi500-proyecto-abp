"""Pruebas de la configuración compartida.

Verifican que las rutas del proyecto existen y quedan dentro del repositorio,
para que notebooks y scripts trabajen sobre las mismas carpetas en cualquier equipo.
"""

from pipeline import config


def test_project_root_contains_phase_folders():
    # Caso normal: la raíz calculada es la del repositorio (tiene F1 y F2).
    assert (config.PROJECT_ROOT / "F1").is_dir()
    assert (config.PROJECT_ROOT / "F2").is_dir()


def test_data_dirs_exist_inside_project():
    # Las carpetas de datos existen y no apuntan fuera del repositorio.
    for path in (config.RAW_DATA_DIR, config.PROCESSED_DATA_DIR, config.EVIDENCE_DIR):
        assert path.is_dir()
        assert config.PROJECT_ROOT in path.parents


def test_random_seed_is_fixed_integer():
    assert isinstance(config.RANDOM_SEED, int)
