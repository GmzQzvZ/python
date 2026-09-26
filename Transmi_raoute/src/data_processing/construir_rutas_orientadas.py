import json
import re
import unicodedata
from pathlib import Path


# ============================================================
# ARCHIVO
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

ARCHIVO = (
    BASE_DIR
    / "data"
    / "processed"
    / "rutas_transmi.json"
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
        " portal eldorado "
        " cc nuestro bogota"
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

    # Coincidencia exacta
    if clave in estaciones:
        return estaciones[clave]

    # Alias
    if clave in ALIAS:

        destino = normalizar(
            ALIAS[clave]
        )

        if destino in estaciones:
            return estaciones[destino]

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

    return [
        (
            origen.strip(),
            destino.strip()
        )
        for origen, destino in encontrados
        
    ]


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("AUDITORÍA DE DIRECCIONES")
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

    estaciones = obtener_estaciones(data)

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

    total = 0
    resueltas = 0
    pendientes = []


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

        # ----------------------------------------------------
        # IGNORAR ELEMENTOS ESPECIALES
        # ----------------------------------------------------

        if servicio in (
            "Paradas",
            "Recorridos"
        ):
            continue

        # ----------------------------------------------------
        # EXCLUIR SERVICIOS CON TRAMOS EN CARRIL MIXTO
        # ----------------------------------------------------

        if servicio in SERVICIOS_EXCLUIDOS:
            continue

        direcciones = extraer_direcciones(
            ruta.get("horario")
        )

        for origen, destino in direcciones:

            # ------------------------------------------------
            # IGNORAR VARIANTES DE CICLOVÍA
            # ------------------------------------------------

            if (
                "[Ciclovía]" in origen
                or "[Ciclovía]" in destino
            ):
                continue

            total += 1

            origen_info = resolver(
                origen,
                estaciones
            )

            destino_info = resolver(
                destino,
                estaciones
            )

            # ------------------------------------------------
            # VERIFICAR SI AMBOS EXTREMOS ESTÁN RESUELTOS
            # ------------------------------------------------

            if (
                origen_info is not None
                and destino_info is not None
            ):

                resueltas += 1

            else:

                pendientes.append({
                    "servicio": servicio,
                    "origen": origen,
                    "destino": destino,
                    "origen_resuelto": (
                        origen_info is not None
                    ),
                    "destino_resuelto": (
                        destino_info is not None
                    )
                })


    # ========================================================
    # RESULTADO
    # ========================================================

    print()
    print("=" * 70)
    print("RESULTADO")
    print("=" * 70)

    print()
    print(
        f"Direcciones encontradas: {total}"
    )

    print(
        f"Direcciones resueltas:   {resueltas}"
    )

    print(
        f"Direcciones pendientes:  {len(pendientes)}"
    )

    # ========================================================
    # MOSTRAR PENDIENTES
    # ========================================================

    print()

    if pendientes:

        print("=" * 70)
        print("PENDIENTES")
        print("=" * 70)

        for i, p in enumerate(
            pendientes,
            start=1
        ):

            print()
            print(
                f"PROBLEMA #{i}"
            )

            print(
                f"SERVICIO: {p['servicio']}"
            )

            estado_origen = (
                "RESUELTO"
                if p["origen_resuelto"]
                else "NO_RESUELTO"
            )

            estado_destino = (
                "RESUELTO"
                if p["destino_resuelto"]
                else "NO_RESUELTO"
            )

            print(
                f"ORIGEN:   {p['origen']}"
                f" [{estado_origen}]"
            )

            print(
                f"DESTINO:  {p['destino']}"
                f" [{estado_destino}]"
            )

    else:

        print(
            "No hay direcciones pendientes."
        )

    print()
    print("=" * 70)
    print("FIN")
    print("=" * 70)


if __name__ == "__main__":
    main()