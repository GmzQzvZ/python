import json
import re
import unicodedata
from pathlib import Path


def cargar_json(ruta_archivo):
    """Carga un archivo JSON usando UTF-8."""
    with Path(ruta_archivo).open(encoding="utf-8") as archivo:
        return json.load(archivo)


def limpiar_nombre_estacion(nombre):
    """Normaliza nombres para busquedas sencillas por texto."""
    texto = re.sub(r"&nbsp;?", " ", str(nombre), flags=re.IGNORECASE)
    texto = re.sub(r"\s+", " ", texto).strip().casefold()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(caracter for caracter in texto if not unicodedata.combining(caracter))
