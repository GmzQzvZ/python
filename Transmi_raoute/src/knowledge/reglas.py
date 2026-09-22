CAMPO_RUTAS = "rutas"
CAMPO_DIRECCIONES = "direcciones"
CAMPO_ESTACIONES_ORIENTADAS = "estaciones_orientadas"
ESTADO_DIRECCION_VALIDA = "construida"

CRITERIOS_EVALUACION_DISPONIBLES = (
    "cantidad_estaciones",
    "cantidad_tramos",
    "cantidad_transbordos",
    "servicios_utilizados",
    "cantidad_servicios",
)

POLITICA_SELECCION_INICIAL = (
    "cantidad_transbordos",
    "cantidad_estaciones",
    "cantidad_servicios",
)


def validar_ruta_candidata(ruta):
    """Valida la forma minima necesaria para evaluar una ruta candidata."""
    if not isinstance(ruta, dict):
        return "ruta_no_es_diccionario"
    if ruta.get("encontrada") is not True:
        return None

    for campo in ("estaciones", "tramos", "transbordos"):
        if campo not in ruta:
            return f"falta_{campo}"
        if not isinstance(ruta[campo], list):
            return f"{campo}_no_es_lista"

    return None


def validar_metricas(metricas, criterios):
    for criterio in criterios:
        if criterio not in metricas:
            return f"falta_metrica_{criterio}"
        if not isinstance(metricas[criterio], int):
            return f"metrica_{criterio}_no_es_numerica"
    return None


def seleccionar_ruta(rutas, criterios=None):
    """Selecciona una ruta aplicando una politica configurable y determinista."""
    from src.routing.evaluador import evaluar_ruta

    if not isinstance(rutas, list):
        return {
            "seleccionada": None,
            "estado": "entrada_invalida",
            "errores": [{"indice": None, "motivo": "rutas_no_es_lista"}],
        }

    if not rutas:
        return {
            "seleccionada": None,
            "estado": "lista_vacia",
            "errores": [],
        }

    criterios_usados = tuple(criterios or POLITICA_SELECCION_INICIAL)
    candidatos = []
    errores = []
    rutas_no_encontradas = 0

    for indice, ruta in enumerate(rutas):
        motivo_invalido = validar_ruta_candidata(ruta)
        if motivo_invalido is not None:
            errores.append({"indice": indice, "motivo": motivo_invalido})
            continue

        if not isinstance(ruta, dict) or ruta.get("encontrada") is not True:
            rutas_no_encontradas += 1
            continue

        evaluacion = evaluar_ruta(ruta)
        metricas = evaluacion.get("metricas", {})
        motivo_metricas = validar_metricas(metricas, criterios_usados)
        if motivo_metricas is not None:
            errores.append({"indice": indice, "motivo": motivo_metricas})
            continue

        clave = tuple(metricas[criterio] for criterio in criterios_usados)
        candidatos.append(
            {
                "indice": indice,
                "ruta": ruta,
                "evaluacion": evaluacion,
                "clave": clave,
            }
        )

    if not candidatos:
        if errores:
            estado = "sin_rutas_validas"
        elif rutas_no_encontradas:
            estado = "sin_rutas_encontradas"
        else:
            estado = "sin_rutas_validas"
        return {
            "seleccionada": None,
            "estado": estado,
            "criterios_utilizados": list(criterios_usados),
            "errores": errores,
        }

    mejor = min(candidatos, key=lambda candidato: candidato["clave"])
    empatadas = [
        candidato for candidato in candidatos if candidato["clave"] == mejor["clave"]
    ]

    return {
        "seleccionada": {
            "indice": mejor["indice"],
            "ruta": mejor["ruta"],
            "evaluacion": mejor["evaluacion"],
        },
        "estado": "seleccionada",
        "criterios_utilizados": list(criterios_usados),
        "empate": len(empatadas) > 1,
        "indices_empatados": [candidato["indice"] for candidato in empatadas],
        "explicacion": {
            "politica": [
                {"prioridad": prioridad + 1, "criterio": criterio}
                for prioridad, criterio in enumerate(criterios_usados)
            ],
            "valores_por_ruta": [
                {
                    "indice": candidato["indice"],
                    "valores": {
                        criterio: candidato["evaluacion"]["metricas"][criterio]
                        for criterio in criterios_usados
                    },
                }
                for candidato in candidatos
            ],
        },
        "errores": errores,
    }
