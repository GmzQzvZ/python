import json
from pathlib import Path


# Obtenemos la carpeta raíz del proyecto
ROOT_DIR = Path(__file__).resolve().parents[2]

# Ubicación del archivo de datos
ARCHIVO_DATOS = ROOT_DIR / "data" / "raw" / "rutas_troncales_raw.json"


def cargar_datos():
    if not ARCHIVO_DATOS.exists():
        print("❌ No se encontró el archivo:")
        print(ARCHIVO_DATOS)
        return None

    with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
        return json.load(f)


def mostrar_informacion(datos):

    if datos is None:
        return

    print("\n===================================")
    print("      INSPECCIÓN DE DATOS")
    print("===================================\n")

    print("Archivo:")
    print(ARCHIVO_DATOS)

    print("\nTipo de dato:")
    print(type(datos).__name__)

    if isinstance(datos, dict):

        print("\nClaves principales:")

        for clave in datos.keys():
            print(f"  - {clave}")

        if "features" in datos:

            print("\nCantidad de registros:")
            print(len(datos["features"]))

            if datos["features"]:

                primer_registro = datos["features"][0]

                print("\nEstructura del primer registro:")
                print("-----------------------------------")

                print("\nClaves:")

                for clave in primer_registro.keys():
                    print(f"  - {clave}")

                if "attributes" in primer_registro:

                    print("\nAtributos:")

                    for clave, valor in primer_registro["attributes"].items():
                        print(f"  {clave}: {valor}")


def main():

    datos = cargar_datos()

    mostrar_informacion(datos)


if __name__ == "__main__":
    main()