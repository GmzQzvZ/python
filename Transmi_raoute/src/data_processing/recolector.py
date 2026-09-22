import json
from pathlib import Path
from urllib.request import urlopen


# URL oficial del servicio GIS de TransMilenio
URL_RUTAS = (
    "https://gis.transmilenio.gov.co/arcgis/rest/services/"
    "Troncal/consulta_rutas_troncales/FeatureServer/0/query"
)


def descargar_rutas():
    """
    Descarga las rutas troncales desde el servicio GIS oficial
    de TransMilenio.
    """

    parametros = (
        "?where=1%3D1"
        "&outFields=*"
        "&returnGeometry=true"
        "&f=json"
    )

    url = URL_RUTAS + parametros

    print("Descargando rutas de TransMilenio...")

    with urlopen(url) as respuesta:
        datos = json.loads(respuesta.read().decode("utf-8"))

    return datos


def guardar_datos(datos, nombre_archivo):
    """
    Guarda los datos originales en data/raw/.
    """

    carpeta = Path("data/raw")
    carpeta.mkdir(parents=True, exist_ok=True)

    archivo = carpeta / nombre_archivo

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    print(f"Datos guardados en: {archivo}")


def main():
    datos_rutas = descargar_rutas()

    guardar_datos(
        datos_rutas,
        "rutas_troncales_raw.json"
    )


if __name__ == "__main__":
    main()