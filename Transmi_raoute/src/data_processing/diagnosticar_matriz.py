import json
from pathlib import Path
from urllib.request import urlopen


ROOT_DIR = Path(__file__).resolve().parents[2]

URL_MATRIZ = (
    "https://gis.transmilenio.gov.co/arcgis/rest/services/"
    "Troncal/consulta_trazados_troncales_estaciones/"
    "FeatureServer/2"
)


def main():

    url = URL_MATRIZ + "?f=json"

    print("Consultando información del servicio...")

    try:

        with urlopen(url) as respuesta:
            datos = json.loads(
                respuesta.read().decode("utf-8")
            )

    except Exception as error:

        print("\n❌ Error de conexión:")
        print(error)
        return

    if "error" in datos:

        print("\n❌ El servicio devolvió un error:")
        print(json.dumps(
            datos["error"],
            ensure_ascii=False,
            indent=4
        ))
        return

    print("\n===================================")
    print(" INFORMACIÓN DE LA CAPA")
    print("===================================\n")

    print("Nombre:")
    print(datos.get("name"))

    print("\nTipo:")
    print(datos.get("type"))

    print("\nMáximo de registros:")
    print(datos.get("maxRecordCount"))

    print("\nFormato de consulta:")
    print(datos.get("supportedQueryFormats"))

    print("\nCantidad de campos:")
    print(len(datos.get("fields", [])))

    print("\nCAMPOS:")
    print("-----------------------------------")

    for campo in datos.get("fields", []):

        print(
            f"{campo.get('name')} "
            f"| {campo.get('type')} "
            f"| {campo.get('alias')}"
        )


if __name__ == "__main__":
    main()