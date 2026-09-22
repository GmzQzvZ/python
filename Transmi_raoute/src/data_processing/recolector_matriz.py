import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


ROOT_DIR = Path(__file__).resolve().parents[2]

URL_MATRIZ = (
    "https://gis.transmilenio.gov.co/arcgis/rest/services/"
    "Troncal/consulta_trazados_troncales_estaciones/"
    "FeatureServer/2/query"
)


def probar_consulta():

    parametros = {
        "where": "1=1",
        "outFields": "id_unico,ruta,direction,posicion,nombre_parada",
        "returnGeometry": "false",
        "resultRecordCount": 10,
        "f": "json"
    }

    url = URL_MATRIZ + "?" + urlencode(parametros)

    print("Probando consulta...")

    with urlopen(url) as respuesta:

        datos = json.loads(
            respuesta.read().decode("utf-8")
        )

    if "error" in datos:

        print("\n❌ El servidor devolvió un error:")
        print(json.dumps(
            datos["error"],
            ensure_ascii=False,
            indent=4
        ))

        return

    registros = datos.get("features", [])

    print("\n✅ Consulta exitosa")
    print(f"Registros recibidos: {len(registros)}")

    print("\nPrimeros registros:")
    print("-----------------------------------")

    for registro in registros:

        atributos = registro.get("attributes", {})

        print(
            f"ID: {atributos.get('id_unico')} | "
            f"Ruta: {atributos.get('ruta')} | "
            f"Dirección: {atributos.get('direction')} | "
            f"Posición: {atributos.get('posicion')} | "
            f"Parada: {atributos.get('nombre_parada')}"
        )


def main():
    probar_consulta()


if __name__ == "__main__":
    main()