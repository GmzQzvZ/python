import json
from pathlib import Path
from urllib.request import urlopen


ROOT_DIR = Path(__file__).resolve().parents[2]


URL_EQUIVALENCIAS = (
    "https://gis.transmilenio.gov.co/arcgis/rest/services/"
    "Troncal/consultaEquivalenciaEstaciones/"
    "FeatureServer/1/query"
)


def descargar_equivalencias():
    """
    Descarga la relación entre estaciones y rutas
    desde el servicio GIS oficial de TransMilenio.
    """

    parametros = (
        "?where=1%3D1"
        "&outFields=*"
        "&returnGeometry=false"
        "&f=json"
    )

    url = URL_EQUIVALENCIAS + parametros

    print("Descargando equivalencias estación-ruta...")

    with urlopen(url) as respuesta:
        datos = json.loads(
            respuesta.read().decode("utf-8")
        )

    return datos


def guardar_datos(datos):
    """
    Guarda los datos originales en data/raw/.
    """

    carpeta = ROOT_DIR / "data" / "raw"
    carpeta.mkdir(parents=True, exist_ok=True)

    archivo = (
        carpeta
        / "equivalencias_estaciones_rutas_raw.json"
    )

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(
            datos,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(f"Datos guardados en: {archivo}")


def main():

    datos = descargar_equivalencias()

    guardar_datos(datos)

    print("\n✅ Recolección de equivalencias terminada.")


if __name__ == "__main__":
    main()