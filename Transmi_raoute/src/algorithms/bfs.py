from collections import deque

from src.knowledge.reglas import (
    CAMPO_DIRECCIONES,
    CAMPO_ESTACIONES_ORIENTADAS,
    CAMPO_RUTAS,
    ESTADO_DIRECCION_VALIDA,
)
from src.utils.helpers import limpiar_nombre_estacion


class GrafoTransmilenio:
    """Grafo dirigido construido desde estaciones_orientadas."""

    def __init__(self):
        self.estaciones = {}
        self.adyacencias = {}
        self.servicios_por_estacion = {}
        self.indice_nombres = {}

    def agregar_estacion(self, estacion, servicio=None):
        estacion_id = estacion["id"]
        if estacion_id not in self.estaciones:
            self.estaciones[estacion_id] = {
                "id": estacion_id,
                "nombre": estacion["nombre"],
                "x": estacion.get("x"),
                "y": estacion.get("y"),
            }
            self.adyacencias[estacion_id] = []
            nombre_normalizado = limpiar_nombre_estacion(estacion["nombre"])
            self.indice_nombres.setdefault(nombre_normalizado, set()).add(estacion_id)
            self.servicios_por_estacion[estacion_id] = set()

        if servicio is not None:
            self.servicios_por_estacion[estacion_id].add(servicio)

        return estacion_id

    def agregar_arista(self, origen, destino, servicio, direccion):
        origen_id = self.agregar_estacion(origen, servicio)
        destino_id = self.agregar_estacion(destino, servicio)
        self.adyacencias[origen_id].append(
            {
                "destino": destino_id,
                "servicio": servicio,
                "origen_servicio": direccion.get("origen"),
                "destino_servicio": direccion.get("destino"),
                "variante": direccion.get("variante"),
            }
        )

    def resolver_estacion_detalle(self, estacion):
        if isinstance(estacion, int):
            if estacion in self.estaciones:
                return estacion, "ok"
            return None, "no_existe"

        texto = str(estacion).strip()
        if texto.isdigit():
            estacion_id = int(texto)
            if estacion_id in self.estaciones:
                return estacion_id, "ok"
            return None, "no_existe"

        coincidencias = self.indice_nombres.get(limpiar_nombre_estacion(texto), set())
        if len(coincidencias) == 1:
            return next(iter(coincidencias)), "ok"
        if len(coincidencias) > 1:
            return None, "ambiguo"
        return None, "no_existe"

    def resolver_estacion(self, estacion):
        estacion_id, estado = self.resolver_estacion_detalle(estacion)
        if estado == "ok":
            return estacion_id
        return None


def construir_grafo(datos_rutas):
    """Construye un grafo dirigido usando pares consecutivos de estaciones orientadas."""
    grafo = GrafoTransmilenio()

    for servicio, ruta in datos_rutas.get(CAMPO_RUTAS, {}).items():
        for direccion in ruta.get(CAMPO_DIRECCIONES, []):
            if direccion.get("estado") != ESTADO_DIRECCION_VALIDA:
                continue

            estaciones = direccion.get(CAMPO_ESTACIONES_ORIENTADAS, [])
            for estacion in estaciones:
                grafo.agregar_estacion(estacion, servicio)

            for origen, destino in zip(estaciones, estaciones[1:]):
                grafo.agregar_arista(origen, destino, servicio, direccion)

    return grafo


def identificar_transbordos(tramos, estaciones):
    """Identifica cambios de servicio entre tramos consecutivos de una ruta."""
    transbordos = []

    for indice in range(1, len(tramos)):
        tramo_anterior = tramos[indice - 1]
        tramo_actual = tramos[indice]

        if tramo_anterior["servicio"] == tramo_actual["servicio"]:
            continue

        estacion_transbordo = estaciones[indice]
        transbordos.append(
            {
                "estacion": estacion_transbordo,
                "desde_servicio": tramo_anterior["servicio"],
                "hacia_servicio": tramo_actual["servicio"],
                "indice_estacion": indice,
            }
        )

    return transbordos


def construir_respuesta_ruta(grafo, ids_ruta, tramos):
    estaciones = [grafo.estaciones[estacion_id] for estacion_id in ids_ruta]
    transbordos = identificar_transbordos(tramos, estaciones)

    return {
        "encontrada": True,
        "estaciones": estaciones,
        "tramos": tramos,
        "transbordos": transbordos,
        "cantidad_estaciones": len(ids_ruta),
        "cantidad_transbordos": len(transbordos),
    }


def buscar_ruta_bfs(grafo, origen, destino):
    """Busca una ruta con BFS entre dos estaciones identificadas por id o nombre."""
    origen_id, estado_origen = grafo.resolver_estacion_detalle(origen)
    destino_id, estado_destino = grafo.resolver_estacion_detalle(destino)

    if estado_origen != "ok" or estado_destino != "ok":
        if estado_origen == "ambiguo":
            motivo = "origen_ambiguo"
        elif estado_destino == "ambiguo":
            motivo = "destino_ambiguo"
        elif estado_origen != "ok":
            motivo = "origen_no_existe"
        else:
            motivo = "destino_no_existe"
        return {
            "encontrada": False,
            "motivo": motivo,
            "estaciones": [],
            "tramos": [],
            "transbordos": [],
        }

    if origen_id == destino_id:
        return construir_respuesta_ruta(grafo, [origen_id], [])

    visitados = {origen_id}
    cola = deque([(origen_id, [], [])])

    while cola:
        actual, camino_estaciones, camino_tramos = cola.popleft()

        for arista in grafo.adyacencias.get(actual, []):
            siguiente = arista["destino"]
            if siguiente in visitados:
                continue

            tramo = {
                "origen": actual,
                "destino": siguiente,
                "servicio": arista["servicio"],
                "origen_servicio": arista["origen_servicio"],
                "destino_servicio": arista["destino_servicio"],
                "variante": arista["variante"],
            }
            nuevas_estaciones = camino_estaciones + [actual]
            nuevos_tramos = camino_tramos + [tramo]

            if siguiente == destino_id:
                ids_ruta = nuevas_estaciones + [siguiente]
                return construir_respuesta_ruta(grafo, ids_ruta, nuevos_tramos)

            visitados.add(siguiente)
            cola.append((siguiente, nuevas_estaciones, nuevos_tramos))

    return {
        "encontrada": False,
        "motivo": "sin_ruta",
        "estaciones": [],
        "tramos": [],
        "transbordos": [],
    }
