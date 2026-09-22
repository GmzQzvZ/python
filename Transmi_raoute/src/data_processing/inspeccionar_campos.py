import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]

ARCHIVO_DATOS = (
    ROOT_DIR
    / "data"
    / "raw"
    / "rutas_troncales_raw.json"
)


def main():

    with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    print("\n===================================")
    print("       CAMPOS DE TRANSMILENIO")
    print("===================================\n")

    campos = datos.get("fields", [])

    print(f"Cantidad de campos: {len(campos)}\n")

    for campo in campos:

        nombre = campo.get("name")
        tipo = campo.get("type")
        alias = campo.get("alias")

        print(f"Nombre : {nombre}")
        print(f"Tipo   : {tipo}")
        print(f"Alias  : {alias}")
        print("-----------------------------------")


if __name__ == "__main__":
    main()