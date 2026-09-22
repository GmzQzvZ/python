import json
import re
from urllib.request import urlopen, Request


# ============================================================
# CONFIGURACIÓN
# ============================================================

URL = (
    "https://tramites.transmilenio.gov.co/"
    "public-static-pages/mapa-interactivo/mapa/reference_data.js"
)

ARCHIVO_DATA = "data/processed/rutas_transmi.json"

SERVICIOS = [
    "1",
    "2",
    "B11",
    "G11",
    "D22",
    "G22",
    "B13",
    "H13"
]


# ============================================================
# CARGAR DATA PROCESADA
# ============================================================

with open(
    ARCHIVO_DATA,
    "r",
    encoding="utf-8"
) as archivo:

    data = json.load(archivo)


# ============================================================
# DESCARGAR REFERENCE_DATA.JS
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
# EXTRAER BLOQUES DE SERVICIO
# ============================================================

patron_ruta = re.compile(
    r"Datos\['([^']+)'\]\s*=\s*\{(.*?)\n\};",
    re.DOTALL
)


bloques = {}

for coincidencia in patron_ruta.finditer(texto):

    nombre = coincidencia.group(1)

    if nombre in SERVICIOS:

        bloques[nombre] = coincidencia.group(2)


# ============================================================
# ANALIZAR
# ============================================================

for nombre in SERVICIOS:

    print("\n")
    print("========================================")
    print(f"SERVICIO {nombre}")
    print("========================================")

    if nombre not in bloques:

        print("No encontrado.")
        continue

    contenido = bloques[nombre]

    # --------------------------------------------------------
    # HORARIO / DIRECCIÓN
    # --------------------------------------------------------

    horario_match = re.search(
        r"'horario'\s*:\s*\"(.*?)\"",
        contenido,
        re.DOTALL
    )

    if horario_match:

        horario = horario_match.group(1)

        print("\nDirección(es):")

        direcciones = re.findall(
            r"De\s+(.+?)\s+a\s+(.+?):",
            horario
        )

        for origen, destino in direcciones:

            print(
                f"  {origen.strip()} "
                f"→ {destino.strip()}"
            )

    # --------------------------------------------------------
    # ESTACIONES
    # --------------------------------------------------------

    estaciones_match = re.search(
        r"'estaciones'\s*:\s*\[(.*?)\]",
        contenido,
        re.DOTALL
    )

    if not estaciones_match:

        print("\nNo tiene estaciones.")
        continue

    ids = [
        int(numero)
        for numero in re.findall(
            r"\d+",
            estaciones_match.group(1)
        )
    ]

    print("\nIDs de estaciones:")
    print(ids)

    # --------------------------------------------------------
    # COMPARAR CON DATA PROCESADA
    # --------------------------------------------------------

    if nombre in data["rutas"]:

        estaciones = data["rutas"][nombre]["estaciones"]

        print("\nEstaciones con nombre:")

        for posicion, estacion in enumerate(
            estaciones,
            start=1
        ):

            print(
                f"{posicion:02d}. "
                f"{estacion['id']} - "
                f"{estacion['nombre']}"
            )