import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]

ARCHIVO_DATOS = (
    ROOT_DIR
    / "data"
    / "raw"
    / "equivalencias_estaciones_rutas_raw.json"
)


def main():

    with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    print("\n===================================")
    print(" CAMPOS DE EQUIVALENCIAS")
    print("===================================\n")

    campos = datos.get("fields", [])

    print(f"Cantidad de campos: {len(campos)}\n")

    for campo in campos:

        print(f"Nombre : {campo.get('name')}")
        print(f"Tipo   : {campo.get('type')}")
        print(f"Alias  : {campo.get('alias')}")
        print("-----------------------------------")


if __name__ == "__main__":
    main()