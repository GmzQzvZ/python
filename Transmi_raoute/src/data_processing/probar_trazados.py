import json
from urllib.parse import urlencode
from urllib.request import urlopen


URL = (
    "https://gis.transmilenio.gov.co/arcgis/rest/services/"
    "Troncal/consulta_trazados_troncales_estaciones/"
    "FeatureServer/1/query"
)


def main():

    parametros = {
        "where": "1=1",
        "outFields": "id_trazado,ori_traz,fin_traz,nom_traz,le_troncal,nom_tronc,esta_oper",
        "returnGeometry": "false",
        "resultRecordCount": "20",
        "f": "json"
    }

    url = URL + "?" + urlencode(parametros)

    print("Consultando trazados troncales...")
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

    print(
        json.dumps(
            datos,
            ensure_ascii=False,
            indent=4
        )
    )


if __name__ == "__main__":
    main()