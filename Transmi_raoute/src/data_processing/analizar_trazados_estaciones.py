import json
from collections import defaultdict


ARCHIVO = "data/raw/estaciones_troncales_raw.json"


def main():

    print("Analizando estaciones por trazado...")
    print("-----------------------------------")

    try:

        with open(
            ARCHIVO,
            "r",
            encoding="utf-8"
        ) as archivo:

            datos = json.load(archivo)

    except FileNotFoundError:

        print("\n❌ No se encontró:")
        print(ARCHIVO)
        return

    features = datos.get("features", [])

    if not features:

        print("\n❌ No se encontraron estaciones.")
        return

    trazados = defaultdict(list)

    for elemento in features:

        atributos = elemento.get("attributes", {})

        id_trazado = atributos.get(
            "id_trazado_troncal"
        )

        trazados[id_trazado].append(
            atributos
        )

    print(
        f"\nTotal de estaciones: {len(features)}"
    )

    print(
        f"Total de trazados diferentes: {len(trazados)}"
    )

    print("\nEstaciones por trazado:")
    print("-----------------------------------")

    for id_trazado, estaciones in sorted(
        trazados.items(),
        key=lambda x: str(x[0])
    ):

        print(
            f"\n{id_trazado}: "
            f"{len(estaciones)} estaciones"
        )

        for estacion in estaciones:

            print(
                f"  - "
                f"{estacion.get('numero_estacion')} | "
                f"{estacion.get('nombre_estacion')} | "
                f"Nodo: {estacion.get('codigo_nodo_estacion')}"
            )


if __name__ == "__main__":
    main()