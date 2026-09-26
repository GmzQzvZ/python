import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.routing.evaluador import buscar_ruta


MENSAJES_ERROR = {
    "origen_no_existe": "No se encontro la estacion de origen.",
    "destino_no_existe": "No se encontro la estacion de destino.",
    "origen_ambiguo": "El nombre de la estacion de origen es ambiguo. Usa el ID.",
    "destino_ambiguo": "El nombre de la estacion de destino es ambiguo. Usa el ID.",
    "sin_ruta": "No se encontro una ruta entre el origen y el destino.",
}


def formatear_estacion(estacion):
    nombre = re.sub(r"&nbsp;?", " ", estacion["nombre"])
    nombre = re.sub(r"\s+", " ", nombre).strip()
    return f"{nombre} (ID {estacion['id']})"


def mostrar_resultado(resultado):
    ruta = resultado["ruta"]
    evaluacion = resultado["evaluacion"]
    metricas = evaluacion["metricas"]

    print("\nResultado")
    print("-" * 40)

    if not resultado["encontrada"]:
        motivo = resultado.get("motivo")
        print(MENSAJES_ERROR.get(motivo, f"No fue posible buscar la ruta: {motivo}"))
        return

    estaciones = ruta["estaciones"]
    print(f"Origen resuelto: {formatear_estacion(estaciones[0])}")
    print(f"Destino resuelto: {formatear_estacion(estaciones[-1])}")
    print("Existe ruta: si")

    print("\nEstaciones de la ruta:")
    for indice, estacion in enumerate(estaciones, start=1):
        print(f"{indice}. {formatear_estacion(estacion)}")

    print("\nServicios utilizados:")
    servicios = metricas["servicios_utilizados"]
    print(", ".join(servicios) if servicios else "Ninguno")

    print("\nMetricas:")
    print(f"Cantidad de estaciones: {metricas['cantidad_estaciones']}")
    print(f"Cantidad de tramos: {metricas['cantidad_tramos']}")
    print(f"Cantidad de transbordos: {metricas['cantidad_transbordos']}")

    print("\nEstaciones de transbordo:")
    estaciones_transbordo = metricas["estaciones_transbordo"]
    if estaciones_transbordo:
        for estacion in estaciones_transbordo:
            print(f"- {formatear_estacion(estacion)}")
    else:
        print("No hay transbordos.")


def main():
    print("Buscador de rutas TransMilenio")
    print("-" * 40)
    origen = input("Estacion de origen: ").strip()
    destino = input("Estacion de destino: ").strip()

    if not origen or not destino:
        print("Debes ingresar origen y destino.")
        return

    resultado = buscar_ruta(origen, destino)
    mostrar_resultado(resultado)


if __name__ == "__main__":
    main()
