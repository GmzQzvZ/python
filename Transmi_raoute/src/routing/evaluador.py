from src.algorithms.bfs import buscar_ruta_bfs, construir_grafo
from src.knowledge.base_conocimiento import (
    cargar_rutas_orientadas,
    resolver_estacion_con_alias,
) 
from src.knowledge.reglas import CRITERIOS_EVALUACION_DISPONIBLES


def obtener_grafo(ruta_datos=None, grafo=None):
    """Obtiene un grafo construido desde datos cargados, ruta de archivo o grafo existente."""
    if grafo is not None:
        return grafo

    if isinstance(ruta_datos, dict):
        datos = ruta_datos
    else:
        datos = cargar_rutas_orientadas(ruta_datos)

    return construir_grafo(datos)


def buscar_ruta(origen, destino, ruta_datos=None, grafo=None):
    """Ejecuta el flujo completo: conocimiento, BFS, evaluacion y reglas."""
    from src.knowledge.reglas import seleccionar_ruta

    grafo_red = obtener_grafo(ruta_datos, grafo)

    origen_resuelto, estado_origen = resolver_estacion_con_alias(
        grafo_red, origen
    )
    destino_resuelto, estado_destino = resolver_estacion_con_alias(
        grafo_red, destino
    )

    if estado_origen == "ambiguo":
        ruta = {
            "encontrada": False,
            "motivo": "origen_ambiguo",
        }
        evaluacion = evaluar_ruta(ruta)
        seleccion = seleccionar_ruta([ruta])
        return {
            "encontrada": False,
            "motivo": "origen_ambiguo",
            "origen": origen,
            "destino": destino,
            "ruta": ruta,
            "evaluacion": evaluacion,
            "seleccion": seleccion,
            "grafo": {
                "cantidad_estaciones": len(grafo_red.estaciones),
                "cantidad_aristas": sum(
                    len(aristas) for aristas in grafo_red.adyacencias.values()
                ),
            },
        }

    if estado_destino == "ambiguo":
        ruta = {
            "encontrada": False,
            "motivo": "destino_ambiguo",
        }
        evaluacion = evaluar_ruta(ruta)
        seleccion = seleccionar_ruta([ruta])
        return {
            "encontrada": False,
            "motivo": "destino_ambiguo",
            "origen": origen,
            "destino": destino,
            "ruta": ruta,
            "evaluacion": evaluacion,
            "seleccion": seleccion,
            "grafo": {
                "cantidad_estaciones": len(grafo_red.estaciones),
                "cantidad_aristas": sum(
                    len(aristas) for aristas in grafo_red.adyacencias.values()
                ),
            },
        }

    if estado_origen == "no_existe":
        ruta = {
            "encontrada": False,
            "motivo": "origen_no_existe",
        }
        evaluacion = evaluar_ruta(ruta)
        seleccion = seleccionar_ruta([ruta])
        return {
            "encontrada": False,
            "motivo": "origen_no_existe",
            "origen": origen,
            "destino": destino,
            "ruta": ruta,
            "evaluacion": evaluacion,
            "seleccion": seleccion,
            "grafo": {
                "cantidad_estaciones": len(grafo_red.estaciones),
                "cantidad_aristas": sum(
                    len(aristas) for aristas in grafo_red.adyacencias.values()
                ),
            },
        }

    if estado_destino == "no_existe":
        ruta = {
            "encontrada": False,
            "motivo": "destino_no_existe",
        }
        evaluacion = evaluar_ruta(ruta)
        seleccion = seleccionar_ruta([ruta])
        return {
            "encontrada": False,
            "motivo": "destino_no_existe",
            "origen": origen,
            "destino": destino,
            "ruta": ruta,
            "evaluacion": evaluacion,
            "seleccion": seleccion,
            "grafo": {
                "cantidad_estaciones": len(grafo_red.estaciones),
                "cantidad_aristas": sum(
                    len(aristas) for aristas in grafo_red.adyacencias.values()
                ),
            },
        }

    ruta = buscar_ruta_bfs(
        grafo_red,
        origen_resuelto,
        destino_resuelto,
    )
    evaluacion = evaluar_ruta(ruta)
    seleccion = seleccionar_ruta([ruta])

    return {
        "encontrada": ruta.get("encontrada", False),
        "motivo": ruta.get("motivo"),
        "origen": origen,
        "destino": destino,
        "ruta": ruta,
        "evaluacion": evaluacion,
        "seleccion": seleccion,
        "grafo": {
            "cantidad_estaciones": len(grafo_red.estaciones),
            "cantidad_aristas": sum(
                len(aristas) for aristas in grafo_red.adyacencias.values()
            ),
        },
    }

def evaluar_ruta(ruta):
    """Calcula metricas objetivas de una ruta encontrada."""
    estaciones = ruta.get("estaciones", [])
    tramos = ruta.get("tramos", [])
    transbordos = ruta.get("transbordos", [])
    servicios_utilizados = []

    for tramo in tramos:
        servicio = tramo.get("servicio")
        if servicio is not None and servicio not in servicios_utilizados:
            servicios_utilizados.append(servicio)

    return {
        "encontrada": ruta.get("encontrada", False),
        "motivo": ruta.get("motivo"),
        "metricas": {
            "cantidad_estaciones": len(estaciones),
            "cantidad_tramos": len(tramos),
            "cantidad_transbordos": len(transbordos),
            "servicios_utilizados": servicios_utilizados,
            "cantidad_servicios": len(servicios_utilizados),
            "estaciones_transbordo": [
                transbordo.get("estacion") for transbordo in transbordos
            ],
            "servicios_transbordo": [
                {
                    "desde_servicio": transbordo.get("desde_servicio"),
                    "hacia_servicio": transbordo.get("hacia_servicio"),
                }
                for transbordo in transbordos
            ],
        },
        "criterios_disponibles": list(CRITERIOS_EVALUACION_DISPONIBLES),
    }


def comparar_rutas(rutas):
    """Evalua varias rutas sin ordenarlas ni elegir una ganadora."""
    return {
        "cantidad_rutas": len(rutas),
        "criterios_disponibles": list(CRITERIOS_EVALUACION_DISPONIBLES),
        "evaluaciones": [
            {
                "indice": indice,
                "evaluacion": evaluar_ruta(ruta),
            }
            for indice, ruta in enumerate(rutas)
        ],
    }
