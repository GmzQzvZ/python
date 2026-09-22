import json
from urllib.request import urlopen


URL = (
    "https://gis.transmilenio.gov.co/arcgis/rest/services/"
    "Troncal/consulta_estaciones_troncales/"
    "FeatureServer/0"
)


def main():

    print("Consultando configuración de estaciones...")
    print("-----------------------------------")

    try:

        with urlopen(URL + "?f=pjson") as respuesta:

            datos = json.loads(
                respuesta.read().decode("utf-8")
            )

    except Exception as error:

        print("\n❌ Error:")
        print(error)
        return

    print("\nNombre:")
    print(datos.get("name"))

    print("\nTipo:")
    print(datos.get("type"))

    print("\nRelaciones:")
    print(
        json.dumps(
            datos.get("relationships"),
            ensure_ascii=False,
            indent=4
        )
    )

    print("\nCampos:")
    for campo in datos.get("fields", []):
        print(
            f"- {campo.get('name')} | "
            f"{campo.get('alias')} | "
            f"{campo.get('type')}"
        )


if __name__ == "__main__":
    main()