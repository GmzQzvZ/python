import json
from urllib.parse import urlencode
from urllib.request import urlopen


URL = (
    "https://gis.transmilenio.gov.co/arcgis/rest/services/"
    "Troncal/consulta_conexiones_troncales/"
    "FeatureServer/0/query"
)


def main():

    parametros = {
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "false",
        "f": "json"
    }

    url = URL + "?" + urlencode(parametros)

    print("Consultando conexiones troncales...")
    print("-----------------------------------")

    try:

        with urlopen(url) as respuesta:

            datos = json.loads(
                respuesta.read().decode("utf-8")
            )

    except Exception as error:

        print("\n❌ Error:")
        print(error)
        return

    if "error" in datos:

        print("\n❌ El servidor devolvió un error:")
        print(
            json.dumps(
                datos,
                ensure_ascii=False,
                indent=4
            )
        )
        return

    features = datos.get("features", [])

    print(f"\nRegistros encontrados: {len(features)}")

    if not features:
        print("\n⚠️ No se encontraron registros.")
        return

    archivo = (
        "data/raw/conexiones_troncales_raw.json"
    )

    with open(
        archivo,
        "w",
        encoding="utf-8"
    ) as salida:

        json.dump(
            datos,
            salida,
            ensure_ascii=False,
            indent=4
        )

    print(f"\n✅ Datos guardados en:")
    print(archivo)

    print("\nPrimeros registros:")
    print("-----------------------------------")

    for feature in features[:10]:

        print(
            json.dumps(
                feature.get("attributes", {}),
                ensure_ascii=False,
                indent=4
            )
        )


if __name__ == "__main__":
    main()