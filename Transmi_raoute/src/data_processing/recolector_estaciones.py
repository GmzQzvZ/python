import json
from pathlib import Path
from urllib.request import urlopen


# Carpeta raíz del proyecto
ROOT_DIR = Path(__file__).resolve().parents[2]


# Servicio oficial de TransMilenio
URL_ESTACIONES = (
    "https://gis.transmilenio.gov.co/arcgis/rest/services/"
    "Troncal/consulta_estaciones_troncales/FeatureServer/0/query"
)


def descargar_estaciones():
    """
    Descarga las estaciones troncales desde
    el servicio GIS oficial de TransMilenio.
    """

    parametros = (
        "?where=1%3D1"
        "&outFields=*"
        "&returnGeometry=true"
        "&f=json"
    )

    url = URL_ESTACIONES + parametros

    print("Descargando estaciones de TransMilenio...")

    with urlopen(url) as respuesta:
        datos = json.loads(
            respuesta.read().decode("utf-8")
        )

    return datos


def guardar_datos(datos):
    """
    Guarda las estaciones originales en data/raw/.
    """

    carpeta = ROOT_DIR / "data" / "raw"
    carpeta.mkdir(parents=True, exist_ok=True)

    archivo = carpeta / "estaciones_troncales_raw.json"

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(
            datos,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(f"Datos guardados en: {archivo}")


def main():

    datos = descargar_estaciones()

    guardar_datos(datos)

    print("\n✅ Recolección de estaciones terminada.")


if __name__ == "__main__":
    main()