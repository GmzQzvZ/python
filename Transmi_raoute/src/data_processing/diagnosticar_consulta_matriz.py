import json
from urllib.request import urlopen


URL_MATRIZ = (
    "https://gis.transmilenio.gov.co/arcgis/rest/services/"
    "Troncal/consulta_trazados_troncales_estaciones/"
    "FeatureServer/2"
)


def main():

    print("Consultando configuración de la matriz...")
    print("-----------------------------------")

    try:

        with urlopen(URL_MATRIZ + "?f=pjson") as respuesta:

            datos = json.loads(
                respuesta.read().decode("utf-8")
            )

    except Exception as error:

        print("\n❌ Error:")
        print(error)
        return

    print("\nInformación de la capa:\n")

    campos = [
        "name",
        "type",
        "displayField",
        "maxRecordCount",
        "capabilities",
        "supportedQueryFormats",
        "advancedQueryCapabilities"
    ]

    for campo in campos:

        print(f"{campo}:")

        valor = datos.get(campo)

        print(
            json.dumps(
                valor,
                ensure_ascii=False,
                indent=4
            )
        )

        print()


if __name__ == "__main__":
    main()