import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]

ARCHIVO_DATOS = (
    ROOT_DIR
    / "data"
    / "raw"
    / "matriz_distancia_troncal_raw.json"
)


def main():

    if not ARCHIVO_DATOS.exists():
        print("❌ No se encontró el archivo:")
        print(ARCHIVO_DATOS)
        return

    with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    print("\n===================================")
    print("      INSPECCIÓN DE MATRIZ")
    print("===================================\n")

    print("Archivo:")
    print(ARCHIVO_DATOS)

    print("\nTipo de dato:")
    print(type(datos).__name__)

    print("\nClaves principales:")

    for clave in datos.keys():
        print(f"  - {clave}")

    if "features" not in datos:
        print("\n❌ No se encontró 'features'.")
        return

    registros = datos["features"]

    print("\nCantidad de registros:")
    print(len(registros))

    if not registros:
        print("\n❌ No hay registros.")
        return

    primero = registros[0]

    print("\nEstructura del primer registro:")
    print("-----------------------------------")

    print("\nClaves:")

    for clave in primero.keys():
        print(f"  - {clave}")

    print("\nAtributos:")

    atributos = primero.get("attributes", {})

    for clave, valor in atributos.items():
        print(f"  {clave}: {valor}")


if __name__ == "__main__":
    main()