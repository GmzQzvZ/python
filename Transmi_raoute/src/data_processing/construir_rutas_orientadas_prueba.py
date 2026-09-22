import json
import re
import unicodedata
from pathlib import Path


# ============================================================
# ARCHIVOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

ARCHIVO = (
    BASE_DIR
    / "data"
    / "processed"
    / "rutas_transmi.json"
)

ARCHIVO_SALIDA = (
    BASE_DIR
    / "data"
    / "processed"
    / "rutas_orientadas_prueba.json"
)


# ============================================================
# SERVICIOS EXCLUIDOS DEL BFS
# ============================================================

SERVICIOS_EXCLUIDOS = {
    "M86",
    "K86",
    "M82",
    "L82",
    "D81",
    "L81",
    "M84",
    "C84",
}


# ============================================================
# ALIAS YA VALIDADOS
# ============================================================

ALIAS = {
    "portal del sur": "portal sur jfk coop. financiera",

    "portal de la 80": "portal 80",

    "portal del norte": "portal norte",

    "toberin": "toberin foundever",

    "las aguas": "las aguas centro colombo americano",

    "universidades": "universidades - cityu",

    "san mateo": "san mateo c.c. unisur",

    "museo nacional": "museo nacional fng",

    "flores": "flores areandina",

    "alcala": "alcala - colegio s. tomas dominicos",

    "calle 76": "calle 76 - san felipe",

    "portal eldorado": (
        "&nbsp &nbsp &nbsp portal eldorado "
        "&nbsp &nbsp &nbsp cc nuestro bogota"
    ),

    "portal de las americas": "portal americas",

    "portal calle 80": "portal 80",

    "guatoque veraguas": "guatoque - veraguas",

    "nqs": "nqs calle 75 - zona m",

    "nqs a calle 75": "nqs calle 75 - zona m",

    "calle 75 a portal de las americas": "portal americas",

    "portal ume": "portal ume",

    "portal usme": "portal usme",
}


# ============================================================
# PUNTOS ESPECIALES
# ============================================================

PUNTOS_ESPECIALES = {
    "aeropuerto eldorado",
    "hacienda santa barbara",
    "clinica el bosque",
    "ginebra norte",
    "puente de guadua",
    "cl 80 pte de guadua",
    "etb tibabuyes",
    "k7 con calle 72",
}


# ============================================================
# NORMALIZAR
# ============================================================

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


# ============================================================
# OBTENER TODAS LAS ESTACIONES
# ============================================================

def obtener_estaciones(data):

    estaciones = {}

    rutas = data.get("rutas", {})

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

        for estacion in ruta.get(
            "estaciones",
            []
        ):

            if not isinstance(estacion, dict):
                continue

            estacion_id = estacion.get("id")
            nombre = estacion.get("nombre")

            if estacion_id is None:
                continue

            if not nombre:
                continue

            estaciones[
                normalizar(nombre)
            ] = {
                "id": estacion_id,
                "nombre": nombre
            }

    return estaciones


# ============================================================
# RESOLVER
# ============================================================

def resolver(nombre, estaciones):

    clave = normalizar(nombre)

    # --------------------------------------------------------
    # Coincidencia exacta
    # --------------------------------------------------------

    if clave in estaciones:

        return {
            "tipo": "estacion",
            "id": estaciones[clave]["id"],
            "nombre": estaciones[clave]["nombre"],
            "fuente": "coincidencia_exacta"
        }

    # --------------------------------------------------------
    # Alias
    # --------------------------------------------------------

    if clave in ALIAS:

        destino = normalizar(
            ALIAS[clave]
        )

        if destino in estaciones:

            return {
                "tipo": "estacion",
                "id": estaciones[destino]["id"],
                "nombre": estaciones[destino]["nombre"],
                "fuente": "alias_validado"
            }

    # --------------------------------------------------------
    # Punto especial
    # --------------------------------------------------------

    if clave in PUNTOS_ESPECIALES:

        return {
            "tipo": "punto_especial",
            "id": None,
            "nombre": nombre,
            "fuente": "servicio_especial"
        }

    return None


# ============================================================
# EXTRAER DIRECCIONES
# ============================================================

def extraer_direcciones(horario):

    if not horario:
        return []

    horario = str(horario)

    horario = horario.replace(
        "&nbsp;",
        " "
    )

    horario = re.sub(
        r"\s+",
        " ",
        horario
    )

    patron = (
        r"De\s+(.+?)\s+a\s+(.+?):"
    )

    encontrados = re.findall(
        patron,
        horario,
        flags=re.IGNORECASE
    )

    direcciones = []

    for origen, destino in encontrados:

        origen = origen.strip()
        destino = destino.strip()

        variante = None

        # ----------------------------------------------------
        # Detectar Ciclovía
        # ----------------------------------------------------

        if "[Ciclovía]" in origen:

            origen = origen.replace(
                "[Ciclovía]",
                ""
            ).strip()

            variante = "Ciclovía"

        if "[Ciclov├¡a]" in origen:

            origen = origen.replace(
                "[Ciclov├¡a]",
                ""
            ).strip()

            variante = "Ciclovía"

        if "[Ciclovía]" in destino:

            destino = destino.replace(
                "[Ciclovía]",
                ""
            ).strip()

            variante = "Ciclovía"

        if "[Ciclov├¡a]" in destino:

            destino = destino.replace(
                "[Ciclov├¡a]",
                ""
            ).strip()

            variante = "Ciclovía"

        direcciones.append({
            "origen": origen,
            "destino": destino,
            "variante": variante
        })

    return direcciones


# ============================================================
# CONSTRUIR SECUENCIA ORIENTADA
# ============================================================

def construir_secuencia(
    estaciones_base,
    origen_info,
    destino_info
):

    if (
        origen_info is None
        or destino_info is None
    ):
        return None

    if (
        origen_info["tipo"] != "estacion"
        or destino_info["tipo"] != "estacion"
    ):
        return None

    origen_id = origen_info["id"]
    destino_id = destino_info["id"]

    indice_origen = None
    indice_destino = None

    for indice, estacion in enumerate(
        estaciones_base
    ):

        if estacion.get("id") == origen_id:
            indice_origen = indice

        if estacion.get("id") == destino_id:
            indice_destino = indice

    if (
        indice_origen is None
        or indice_destino is None
    ):
        return None

    if indice_origen <= indice_destino:

        return estaciones_base[
            indice_origen:indice_destino + 1
        ]

    return list(
        reversed(
            estaciones_base[
                indice_destino:indice_origen + 1
            ]
        )
    )


# ============================================================
# CONSTRUIR UNA RUTA
# ============================================================

def construir_ruta(
    clave,
    ruta,
    estaciones_globales
):

    servicio = ruta.get("ruta")

    if not servicio:
        servicio = ruta.get("servicio")

    if not servicio:
        servicio = clave

    if servicio in (
        "Paradas",
        "Recorridos"
    ):
        return None

    if servicio in SERVICIOS_EXCLUIDOS:
        return None

    estaciones_base = []

    for estacion in ruta.get(
        "estaciones",
        []
    ):

        if not isinstance(estacion, dict):
            continue

        estaciones_base.append(
            dict(estacion)
        )

    resultado = {
        "servicio": servicio,
        "horario": ruta.get("horario"),
        "estaciones_base": estaciones_base,
        "direcciones": []
    }

    direcciones = extraer_direcciones(
        ruta.get("horario")
    )

    for direccion in direcciones:

        origen = direccion["origen"]
        destino = direccion["destino"]
        variante = direccion["variante"]

        # ----------------------------------------------------
        # Ignorar Ciclovía
        # ----------------------------------------------------

        if variante == "Ciclovía":
            continue

        origen_info = resolver(
            origen,
            estaciones_globales
        )

        destino_info = resolver(
            destino,
            estaciones_globales
        )

        direccion_resultado = {
            "origen": origen,
            "destino": destino,
            "variante": variante,
            "origen_info": origen_info,
            "destino_info": destino_info
        }

        # ----------------------------------------------------
        # Ambos extremos son estaciones
        # ----------------------------------------------------

        if (
            origen_info is not None
            and destino_info is not None
            and origen_info["tipo"] == "estacion"
            and destino_info["tipo"] == "estacion"
        ):

            estaciones_orientadas = construir_secuencia(
                estaciones_base,
                origen_info,
                destino_info
            )

            if estaciones_orientadas is not None:

                direccion_resultado[
                    "estado"
                ] = "construida"

                direccion_resultado[
                    "estaciones_orientadas"
                ] = estaciones_orientadas

            else:

                direccion_resultado[
                    "estado"
                ] = "estacion_no_encontrada_en_ruta"

        # ----------------------------------------------------
        # Hay puntos especiales
        # ----------------------------------------------------

        elif (
            origen_info is not None
            and destino_info is not None
            and (
                origen_info["tipo"] == "punto_especial"
                or destino_info["tipo"] == "punto_especial"
            )
        ):

            direccion_resultado[
                "estado"
            ] = "punto_especial_pendiente"

        # ----------------------------------------------------
        # Algún extremo no pudo resolverse
        # ----------------------------------------------------

        else:

            direccion_resultado[
                "estado"
            ] = "pendiente"

        resultado[
            "direcciones"
        ].append(
            direccion_resultado
        )

    return resultado


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("CONSTRUCCIÓN DE RUTAS ORIENTADAS")
    print("=" * 70)

    print()
    print("Archivo de entrada:")
    print(ARCHIVO)

    print()
    print("Archivo de salida:")
    print(ARCHIVO_SALIDA)

    if not ARCHIVO.exists():

        print()
        print("ERROR: archivo de entrada no encontrado.")
        return

    with open(
        ARCHIVO,
        "r",
        encoding="utf-8"
    ) as archivo:

        data = json.load(archivo)

    estaciones_globales = obtener_estaciones(
        data
    )

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

    rutas_salida = {}

    direcciones_encontradas = 0
    direcciones_construidas = 0
    puntos_especiales = 0
    pendientes = 0

    # ========================================================
    # RECORRER SERVICIOS
    # ========================================================

    for clave, ruta in elementos:

        if not isinstance(ruta, dict):
            continue

        servicio = ruta.get("ruta")

        if not servicio:
            servicio = ruta.get("servicio")

        if not servicio:
            servicio = clave

        if servicio in (
            "Paradas",
            "Recorridos"
        ):
            continue

        if servicio in SERVICIOS_EXCLUIDOS:
            continue

        direcciones = extraer_direcciones(
            ruta.get("horario")
        )

        # Contar solamente las direcciones válidas
        # que no son Ciclovía.

        for direccion in direcciones:

            if direccion["variante"] == "Ciclovía":
                continue

            direcciones_encontradas += 1

        resultado = construir_ruta(
            clave,
            ruta,
            estaciones_globales
        )

        if resultado is None:
            continue

        rutas_salida[
            resultado["servicio"]
        ] = resultado

        for direccion in resultado[
            "direcciones"
        ]:

            estado = direccion["estado"]

            if estado == "construida":

                direcciones_construidas += 1

            elif estado == "punto_especial_pendiente":

                puntos_especiales += 1

            else:

                pendientes += 1

    # ========================================================
    # ESTRUCTURA FINAL
    # ========================================================

    salida = {
        "fuente": (
            "TransMilenio - reference_data.js"
        ),
        "descripcion": (
            "Rutas de TransMilenio con "
            "secuencias orientadas según "
            "el origen y destino declarados "
            "por cada servicio."
        ),
        "rutas": rutas_salida
    }

    # ========================================================
    # GUARDAR
    # ========================================================

    with open(
        ARCHIVO_SALIDA,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            salida,
            archivo,
            ensure_ascii=False,
            indent=2
        )

    # ========================================================
    # RESULTADO
    # ========================================================

    print()
    print("=" * 70)
    print("RESULTADO")
    print("=" * 70)

    print()
    print(
        f"Rutas generadas:              {len(rutas_salida)}"
    )

    print(
        f"Direcciones encontradas:      {direcciones_encontradas}"
    )

    print(
        f"Direcciones construidas:      {direcciones_construidas}"
    )

    print(
        f"Puntos especiales pendientes: {puntos_especiales}"
    )

    print(
        f"Otros pendientes:             {pendientes}"
    )

    print()
    print(
        "Archivo generado correctamente."
    )

    print()
    print("=" * 70)
    print("FIN")
    print("=" * 70)


if __name__ == "__main__":
    main()