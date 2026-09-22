import json
from urllib.parse import urlencode
from urllib.request import urlopen


URL_MATRIZ = (
    "https://gis.transmilenio.gov.co/arcgis/rest/services/"
    "Troncal/consulta_trazados_troncales_estaciones/"
    "FeatureServer/2/query"
)


def main():

    parametros = {
        "objectIds": "1",
        "outFields": "*",
        "returnGeometry": "false",
        "f": "json"
    }

    url = URL_MATRIZ + "?" + urlencode(parametros)

    print("Probando consulta de un solo registro...")

    try:

        with urlopen(url) as respuesta:

            datos = json.loads(
                respuesta.read().decode("utf-8")
            )

    except Exception as error:

        print("\n❌ Error:")
        print(error)
        return

    print("\nRespuesta del servidor:")
    print("-----------------------------------")

    print(
        json.dumps(
            datos,
            ensure_ascii=False,
            indent=4
        )
    )


if __name__ == "__main__":
    main() 