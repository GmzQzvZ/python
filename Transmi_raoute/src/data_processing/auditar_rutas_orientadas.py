import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

ARCHIVO = (
    BASE_DIR
    / "data"
    / "processed"
    / "rutas_orientadas.json"
)


def main():

    print("=" * 70)
    print("AUDITORÍA DE RUTAS ORIENTADAS")
    print("=" * 70)

    print()
    print("Archivo:")
    print(ARCHIVO)

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

    rutas = data.get("rutas", {})

    total_direcciones = 0
    construidas = 0
    pendientes = 0
    puntos_especiales = 0

    problemas = []

    for servicio, ruta in rutas.items():

        direcciones = ruta.get(
            "direcciones",
            []
        )

        for direccion in direcciones:

            total_direcciones += 1

            estado = direccion.get(
                "estado"
            )

            if estado == "construida":

                construidas += 1

            elif estado == "punto_especial_pendiente":

                puntos_especiales += 1

                problemas.append({
                    "servicio": servicio,
                    "origen": direccion.get(
                        "origen"
                    ),
                    "destino": direccion.get(
                        "destino"
                    ),
                    "estado": estado,
                    "origen_info":
                        direccion.get(
                            "origen_info"
                        ),
                    "destino_info":
                        direccion.get(
                            "destino_info"
                        )
                })

            else:

                pendientes += 1

                problemas.append({
                    "servicio": servicio,
                    "origen": direccion.get(
                        "origen"
                    ),
                    "destino": direccion.get(
                        "destino"
                    ),
                    "estado": estado,
                    "origen_info":
                        direccion.get(
                            "origen_info"
                        ),
                    "destino_info":
                        direccion.get(
                            "destino_info"
                        )
                })

    print()
    print("=" * 70)
    print("RESULTADO")
    print("=" * 70)

    print()
    print(
        f"Direcciones encontradas: "
        f"{total_direcciones}"
    )

    print(
        f"Direcciones construidas: "
        f"{construidas}"
    )

    print(
        f"Puntos especiales pendientes: "
        f"{puntos_especiales}"
    )

    print(
        f"Otros pendientes: "
        f"{pendientes}"
    )

    print()

    if problemas:

        print("=" * 70)
        print("DETALLE DE PENDIENTES")
        print("=" * 70)

        for numero, problema in enumerate(
            problemas,
            start=1
        ):

            print()
            print(
                f"PROBLEMA #{numero}"
            )

            print(
                f"SERVICIO: "
                f"{problema['servicio']}"
            )

            print(
                f"ORIGEN:   "
                f"{problema['origen']}"
            )

            print(
                f"DESTINO:  "
                f"{problema['destino']}"
            )

            print(
                f"ESTADO:   "
                f"{problema['estado']}"
            )

            print(
                f"ORIGEN INFO: "
                f"{problema['origen_info']}"
            )

            print(
                f"DESTINO INFO: "
                f"{problema['destino_info']}"
            )

    else:

        print(
            "No existen direcciones pendientes."
        )

    print()
    print("=" * 70)
    print("FIN")
    print("=" * 70)


if __name__ == "__main__":
    main()

