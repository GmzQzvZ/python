import re
import unicodedata
from urllib.request import urlopen, Request


# ============================================================
# CONFIGURACIÓN
# ============================================================

URL = (
    "https://tramites.transmilenio.gov.co/"
    "public-static-pages/mapa-interactivo/mapa/reference_data.js"
)


# ============================================================
# NORMALIZAR TEXTO SOLO PARA COMPARAR
# ============================================================

def normalizar(texto):

    if texto is None:
        return ""

    texto = texto.replace("&nbsp;", " ")

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    texto = texto.strip().lower()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    return texto


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
# EXTRAER ESTACIONES
# ============================================================

estaciones = {}

patron_estaciones = re.compile(
    r"estacionesGlobal\['(\d+)'\]\s*=\s*\{(.*?)\n\};",
    re.DOTALL
)

for coincidencia in patron_estaciones.finditer(texto):

    estacion_id = int(
        coincidencia.group(1)
    )

    contenido = coincidencia.group(2)

    nombre_match = re.search(
        r'"text"\s*:\s*\'(.*?)\'',
        contenido
    )

    if nombre_match:

        nombre = nombre_match.group(1)

        estaciones[estacion_id] = {
            "id": estacion_id,
            "nombre": nombre
        }


# ============================================================
# CREAR ÍNDICE DE NOMBRES
# ============================================================

indice_estaciones = {}

for estacion in estaciones.values():

    nombre_normalizado = normalizar(
        estacion["nombre"]
    )

    indice_estaciones.setdefault(
        nombre_normalizado,
        []
    ).append(estacion)


# ============================================================
# EXTRAER SERVICIOS
# ============================================================

patron_ruta = re.compile(
    r"Datos\['([^']+)'\]\s*=\s*\{(.*?)\n\};",
    re.DOTALL
)


total_servicios = 0
direcciones_ok = 0
problemas = 0


for coincidencia in patron_ruta.finditer(texto):

    servicio = coincidencia.group(1)
    contenido = coincidencia.group(2)

    if servicio in [
        "Paradas",
        "Recorridos"
    ]:
        continue

    total_servicios += 1

    # ========================================================
    # HORARIO
    # ========================================================

    horario_match = re.search(
        r"'horario'\s*:\s*\"(.*?)\"",
        contenido,
        re.DOTALL
    )

    if not horario_match:

        problemas += 1

        print(
            f"[SIN HORARIO] {servicio}"
        )

        continue

    horario = horario_match.group(1)

    # ========================================================
    # DIRECCIONES
    # ========================================================

    direcciones = re.findall(
        r"De\s+(.+?)\s+a\s+(.+?):",
        horario
    )

    # ========================================================
    # ESTACIONES
    # ========================================================

    estaciones_match = re.search(
        r"'estaciones'\s*:\s*\[(.*?)\]",
        contenido,
        re.DOTALL
    )

    if not estaciones_match:

        problemas += 1

        print(
            f"[SIN ESTACIONES] {servicio}"
        )

        continue

    ids = [
        int(numero)
        for numero in re.findall(
            r"\d+",
            estaciones_match.group(1)
        )
    ]

    nombres_estaciones = []

    for estacion_id in ids:

        if estacion_id in estaciones:

            nombres_estaciones.append(
                estaciones[estacion_id]["nombre"]
            )

        else:

            nombres_estaciones.append(
                None
            )

    # ========================================================
    # ANALIZAR DIRECCIONES
    # ========================================================

    for origen, destino in direcciones:

        origen = origen.strip()
        destino = destino.strip()

        origen_normalizado = normalizar(
            origen
        )

        destino_normalizado = normalizar(
            destino
        )

        posiciones_origen = []

        posiciones_destino = []

        for posicion, nombre_estacion in enumerate(
            nombres_estaciones
        ):

            nombre_normalizado = normalizar(
                nombre_estacion
            )

            if (
                nombre_normalizado == origen_normalizado
                or origen_normalizado in nombre_normalizado
                or nombre_normalizado in origen_normalizado
            ):

                posiciones_origen.append(
                    posicion
                )

            if (
                nombre_normalizado == destino_normalizado
                or destino_normalizado in nombre_normalizado
                or nombre_normalizado in destino_normalizado
            ):

                posiciones_destino.append(
                    posicion
                )

        print("\n----------------------------------------")
        print(f"SERVICIO: {servicio}")
        print(f"ORIGEN:   {origen}")
        print(f"DESTINO:  {destino}")

        print(
            f"Posiciones origen:  "
            f"{posiciones_origen}"
        )

        print(
            f"Posiciones destino: "
            f"{posiciones_destino}"
        )

        if posiciones_origen and posiciones_destino:

            direcciones_ok += 1

            origen_pos = posiciones_origen[0]
            destino_pos = posiciones_destino[0]

            if origen_pos < destino_pos:

                print(
                    "RESULTADO: SECUENCIA DIRECTA"
                )

            elif origen_pos > destino_pos:

                print(
                    "RESULTADO: SECUENCIA INVERSA"
                )

            else:

                print(
                    "RESULTADO: ORIGEN Y DESTINO "
                    "EN LA MISMA POSICIÓN"
                )

                problemas += 1

        else:

            print(
                "RESULTADO: NO SE PUDO UBICAR "
                "ORIGEN O DESTINO"
            )

            problemas += 1


# ============================================================
# RESUMEN
# ============================================================

print("\n")
print("========================================")
print("RESUMEN")
print("========================================")

print(
    f"Servicios analizados: {total_servicios}"
)

print(
    f"Direcciones ubicadas:  {direcciones_ok}"
)

print(
    f"Problemas:             {problemas}"
)