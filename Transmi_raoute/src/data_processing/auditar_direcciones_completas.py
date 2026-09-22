import re
from urllib.request import urlopen, Request


# ============================================================
# CONFIGURACIÓN
# ============================================================

URL = (
    "https://tramites.transmilenio.gov.co/"
    "public-static-pages/mapa-interactivo/mapa/reference_data.js"
)


# ============================================================
# DESCARGAR FUENTE
# ============================================================

request = Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

with urlopen(request, timeout=30) as respuesta:

    texto = respuesta.read().decode(
        "utf-8",
        errors="replace"
    )


# ============================================================
# PATRÓN DE SERVICIOS
# ============================================================

patron_ruta = re.compile(
    r"Datos\['([^']+)'\]\s*=\s*\{(.*?)\n\};",
    re.DOTALL
)


# ============================================================
# CONTADORES
# ============================================================

total = 0
correctos = 0
problemas = 0
sin_direccion = 0
sin_estaciones = 0


# ============================================================
# ANALIZAR TODOS LOS SERVICIOS
# ============================================================

for coincidencia in patron_ruta.finditer(texto):

    nombre_servicio = coincidencia.group(1)
    contenido = coincidencia.group(2)

    # --------------------------------------------------------
    # Excluir elementos que no son servicios
    # --------------------------------------------------------

    if nombre_servicio in [
        "Paradas",
        "Recorridos"
    ]:
        continue

    total += 1

    # --------------------------------------------------------
    # HORARIO
    # --------------------------------------------------------

    horario_match = re.search(
        r"'horario'\s*:\s*\"(.*?)\"",
        contenido,
        re.DOTALL
    )

    if not horario_match:

        sin_direccion += 1

        print(
            f"[SIN HORARIO] {nombre_servicio}"
        )

        continue

    horario = horario_match.group(1)

    # --------------------------------------------------------
    # DIRECCIONES
    # --------------------------------------------------------

    direcciones = re.findall(
        r"De\s+(.+?)\s+a\s+(.+?):",
        horario
    )

    if not direcciones:

        sin_direccion += 1

        print(
            f"[SIN DIRECCIÓN] {nombre_servicio}"
        )

        continue

    # --------------------------------------------------------
    # ESTACIONES
    # --------------------------------------------------------

    estaciones_match = re.search(
        r"'estaciones'\s*:\s*\[(.*?)\]",
        contenido,
        re.DOTALL
    )

    if not estaciones_match:

        sin_estaciones += 1

        print(
            f"[SIN ESTACIONES] {nombre_servicio}"
        )

        continue

    ids_estaciones = [
        int(numero)
        for numero in re.findall(
            r"\d+",
            estaciones_match.group(1)
        )
    ]

    if not ids_estaciones:

        sin_estaciones += 1

        print(
            f"[SIN ESTACIONES] {nombre_servicio}"
        )

        continue

    # --------------------------------------------------------
    # ANALIZAR CADA DIRECCIÓN
    # --------------------------------------------------------

    servicio_tiene_problema = False

    for origen, destino in direcciones:

        origen = origen.strip()
        destino = destino.strip()

        # ----------------------------------------------------
        # NORMALIZACIÓN BÁSICA
        # ----------------------------------------------------

        origen_limpio = (
            origen
            .replace("&nbsp;", " ")
            .strip()
        )

        destino_limpio = (
            destino
            .replace("&nbsp;", " ")
            .strip()
        )

        # ----------------------------------------------------
        # AQUÍ SOLO TENEMOS IDs.
        #
        # Para comparar nombres necesitaríamos la tabla
        # estacionesGlobal.
        #
        # Por ahora mostramos los datos.
        # ----------------------------------------------------

        print("\n----------------------------------------")
        print(f"SERVICIO: {nombre_servicio}")
        print(f"ORIGEN:   {origen_limpio}")
        print(f"DESTINO:  {destino_limpio}")
        print(
            f"ESTACIONES: {len(ids_estaciones)}"
        )

    # --------------------------------------------------------
    # CONTADOR
    # --------------------------------------------------------

    if servicio_tiene_problema:

        problemas += 1

    else:

        correctos += 1


# ============================================================
# RESUMEN
# ============================================================

print("\n")
print("========================================")
print("RESUMEN DE AUDITORÍA")
print("========================================")

print(f"Servicios analizados: {total}")
print(f"Servicios normales:   {correctos}")
print(f"Con problemas:        {problemas}")
print(f"Sin dirección:         {sin_direccion}")
print(f"Sin estaciones:        {sin_estaciones}")