import json
from pathlib import Path


# Ubicación principal del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Ubicación del archivo de configuración
RUTA_CONFIG = (
    BASE_DIR
    / "02_insumos"
    / "configuracion"
    / "config.json"
)


def cargar_configuracion():
    """
    Lee las reglas de Mercadeo desde config.json.
    """

    if not RUTA_CONFIG.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {RUTA_CONFIG}"
        )

    with RUTA_CONFIG.open("r", encoding="utf-8") as archivo:
        configuracion = json.load(archivo)

    if not isinstance(configuracion, dict):
        raise ValueError(
            "El archivo de configuración debe contener un objeto JSON."
        )

    return configuracion