import json
import re
import unicodedata
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

ARCHIVO = (
    BASE_DIR
    / "data"
    / "processed"
    / "rutas_transmi.json"
)


BUSCAR = [
    "Portal Ume",
    "CL 80 Pte de Guadua",
]


def normalizar(texto):

    if texto is None:
        return ""

    texto = str(texto)

    texto = texto.replace("&nbsp;", " ")
    texto = texto.replace("&nbsp", " ")

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        c
        for c in texto
        if unicodedata.category(c) != "Mn"
    )

    texto = texto.lower()

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()


def main():

    print("=" * 70)
    print("BÚSQUEDA DE PUNTOS PENDIENTES")
    print("=" * 70)

    if not ARCHIVO.exists():

        print()
        print("ERROR: archivo no encontrado.")
        return

    with open(
        ARCHIVO,
        "r",
        encoding="utf-8"
    ) as archivo:

        data = json.load(archivo)

    estaciones_encontradas = []

    rutas = data.get(
        "rutas",
        {}
    )

    if isinstance(rutas, dict):

        elementos = rutas.items()

    else:

        elementos = [
            (None, ruta)
            for ruta in rutas
        ]

    for clave, ruta in elementos:

        if not isinstance(ruta, dict):
            continue

        servicio = ruta.get(
            "ruta"
        )

        if not servicio:
            servicio = clave

        estaciones = ruta.get(
            "estaciones",
            []
        )

        for estacion in estaciones:

            if not isinstance(estacion, dict):
                continue

            nombre = estacion.get(
                "nombre"
            )

            if not nombre:
                continue

            for buscado in BUSCAR:

                if normalizar(
                    buscado
                ) == normalizar(
                    nombre
                ):

                    registro = {
                        "buscado": buscado,
                        "servicio": servicio,
                        "id": estacion.get(
                            "id"
                        ),
                        "nombre": nombre
                    }

                    if registro not in estaciones_encontradas:

                        estaciones_encontradas.append(
                            registro
                        )

    print()

    for buscado in BUSCAR:

        print("=" * 70)
        print(
            f"BUSCANDO: {buscado}"
        )
        print("=" * 70)

        resultados = [
            resultado
            for resultado in estaciones_encontradas
            if resultado["buscado"] == buscado
        ]

        if not resultados:

            print(
                "NO ENCONTRADO"
            )

        else:

            for resultado in resultados:

                print(
                    f"Servicio: "
                    f"{resultado['servicio']}"
                )

                print(
                    f"ID: "
                    f"{resultado['id']}"
                )

                print(
                    f"Nombre: "
                    f"{resultado['nombre']}"
                )

                print()

    print()
    print("=" * 70)
    print("FIN")
    print("=" * 70)


if __name__ == "__main__":
    main()