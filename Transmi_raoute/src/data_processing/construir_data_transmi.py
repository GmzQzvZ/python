from urllib.request import urlopen, Request
import re
import json
import os


# ============================================================
# CONFIGURACIÓN
# ============================================================

URL = (
    "https://tramites.transmilenio.gov.co/"
    "public-static-pages/mapa-interactivo/mapa/reference_data.js"
)

ARCHIVO_SALIDA = "data/processed/rutas_transmi.json"


# ============================================================
# DESCARGAR reference_data.js
# ============================================================

print("========================================")
print("DESCARGANDO DATOS DE TRANSMILENIO")
print("========================================")

request = Request(
    URL,
    headers={
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "Chrome/153.0.0.0 Safari/537.36"
        ),
        "Accept": "text/javascript, application/javascript, */*",
        "Referer": (
            "https://tramites.transmilenio.gov.co/"
            "mapa-interactivo"
        )
    }
)

try:

    with urlopen(request, timeout=30) as respuesta:
        texto = respuesta.read().decode(
            "utf-8",
            errors="replace"
        )

except Exception as error:

    print("ERROR al descargar reference_data.js")
    print(error)
    exit()


print(f"Caracteres descargados: {len(texto)}")


# ============================================================
# EXTRAER ESTACIONES
# ============================================================

print("\n========================================")
print("PROCESANDO ESTACIONES")
print("========================================")

estaciones = {}

patron_estaciones = re.compile(
    r"estacionesGlobal\['(\d+)'\]\s*=\s*\{(.*?)\n\};",
    re.DOTALL
)

for coincidencia in patron_estaciones.finditer(texto):

    estacion_id = int(coincidencia.group(1))
    contenido = coincidencia.group(2)

    x_match = re.search(
        r'"x"\s*:\s*(-?\d+(?:\.\d+)?)',
        contenido
    )

    y_match = re.search(
        r'"y"\s*:\s*(-?\d+(?:\.\d+)?)',
        contenido
    )

    nombre_match = re.search(
        r'"text"\s*:\s*\'(.*?)\'',
        contenido
    )

    rutas_match = re.search(
        r'"conteoRutas"\s*:\s*\'(.*?)\'',
        contenido
    )

    url_match = re.search(
        r'"url"\s*:\s*\'(.*?)\'',
        contenido
    )

    estacion = {
        "id": estacion_id,
        "nombre": (
            nombre_match.group(1)
            if nombre_match
            else None
        ),
        "x": (
            float(x_match.group(1))
            if x_match
            else None
        ),
        "y": (
            float(y_match.group(1))
            if y_match
            else None
        ),
        "rutas_texto": (
            rutas_match.group(1)
            if rutas_match
            else None
        ),
        "url": (
            url_match.group(1)
            if url_match
            else None
        )
    }

    estaciones[estacion_id] = estacion


print(f"Estaciones encontradas: {len(estaciones)}")


# ============================================================
# EXTRAER RUTAS / SERVICIOS
# ============================================================

print("\n========================================")
print("PROCESANDO RUTAS")
print("========================================")

rutas = {}

patron_ruta = re.compile(
    r"Datos\['([^']+)'\]\s*=\s*\{(.*?)\n\};",
    re.DOTALL
)

for coincidencia in patron_ruta.finditer(texto):

    nombre_ruta = coincidencia.group(1)
    contenido = coincidencia.group(2)

    # --------------------------------------------------------
    # Ignorar la estructura general "Paradas"
    # --------------------------------------------------------

    if nombre_ruta == "Paradas":
        continue

    # --------------------------------------------------------
    # Extraer estaciones
    # --------------------------------------------------------

    estaciones_match = re.search(
        r"'estaciones'\s*:\s*\[(.*?)\]",
        contenido,
        re.DOTALL
    )

    ids_estaciones = []

    if estaciones_match:

        numeros = re.findall(
            r"\d+",
            estaciones_match.group(1)
        )

        ids_estaciones = [
            int(numero)
            for numero in numeros
        ]

    # --------------------------------------------------------
    # Extraer trayectos
    # --------------------------------------------------------

    trayectos_match = re.search(
        r"'trayectos'\s*:\s*\[(.*?)\]",
        contenido,
        re.DOTALL
    )

    ids_trayectos = []

    if trayectos_match:

        numeros = re.findall(
            r"\d+",
            trayectos_match.group(1)
        )

        ids_trayectos = [
            int(numero)
            for numero in numeros
        ]

    # --------------------------------------------------------
    # Extraer horario
    # --------------------------------------------------------

    horario_match = re.search(
        r"'horario'\s*:\s*\"(.*?)\"",
        contenido,
        re.DOTALL
    )

    if horario_match:
        horario = horario_match.group(1)
    else:
        horario = None

    # --------------------------------------------------------
    # Construir estaciones completas
    # --------------------------------------------------------

    estaciones_ruta = []

    for posicion, estacion_id in enumerate(
        ids_estaciones,
        start=1
    ):

        datos_estacion = estaciones.get(estacion_id)

        if datos_estacion:

            estaciones_ruta.append({
                "orden": posicion,
                "id": estacion_id,
                "nombre": datos_estacion["nombre"],
                "x": datos_estacion["x"],
                "y": datos_estacion["y"]
            })

        else:

            estaciones_ruta.append({
                "orden": posicion,
                "id": estacion_id,
                "nombre": None,
                "x": None,
                "y": None
            })

    # --------------------------------------------------------
    # Guardar ruta
    # --------------------------------------------------------

    rutas[nombre_ruta] = {
        "servicio": nombre_ruta,
        "horario": horario,
        "estaciones": estaciones_ruta,
        "trayectos": ids_trayectos
    }


print(f"Rutas encontradas: {len(rutas)}")


# ============================================================
# CREAR CARPETA DE SALIDA
# ============================================================

os.makedirs(
    os.path.dirname(ARCHIVO_SALIDA),
    exist_ok=True
)


# ============================================================
# CREAR ARCHIVO FINAL
# ============================================================

data_final = {
    "fuente": URL,
    "total_estaciones": len(estaciones),
    "total_rutas": len(rutas),
    "rutas": rutas
}


with open(
    ARCHIVO_SALIDA,
    "w",
    encoding="utf-8"
) as archivo:

    json.dump(
        data_final,
        archivo,
        ensure_ascii=False,
        indent=4
    )


# ============================================================
# RESULTADO
# ============================================================

print("\n========================================")
print("DATA CONSTRUIDA")
print("========================================")

print(f"Estaciones: {len(estaciones)}")
print(f"Rutas:      {len(rutas)}")

print(f"\nArchivo generado:")
print(ARCHIVO_SALIDA)


# ============================================================
# MOSTRAR D22 COMO PRUEBA
# ============================================================

print("\n========================================")
print("PRUEBA CON D22")
print("========================================")

if "D22" in rutas:

    d22 = rutas["D22"]

    print(f"Servicio: {d22['servicio']}")
    print(f"Horario:  {d22['horario']}")

    print("\nEstaciones:")

    for estacion in d22["estaciones"]:

        print(
            f"{estacion['orden']:02d}. "
            f"{estacion['id']} - "
            f"{estacion['nombre']}"
        )

    print("\nTrayectos:")
    print(d22["trayectos"])

else:

    print("No se encontró D22.")