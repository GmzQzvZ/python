import re
from urllib.request import urlopen, Request


URL = (
    "https://tramites.transmilenio.gov.co/"
    "public-static-pages/mapa-interactivo/mapa/reference_data.js"
)


# ============================================================
# DESCARGAR ARCHIVO
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
# BUSCAR SERVICIOS
# ============================================================

patron_ruta = re.compile(
    r"Datos\['([^']+)'\]\s*=\s*\{(.*?)\n\};",
    re.DOTALL
)


servicios = [
    "D22",
    "G22",
    "1",
    "2",
    "B11",
    "G11"
]


for coincidencia in patron_ruta.finditer(texto):

    nombre = coincidencia.group(1)

    if nombre not in servicios:
        continue

    contenido = coincidencia.group(2)

    print("\n========================================")
    print(f"SERVICIO: {nombre}")
    print("========================================")

    # ========================================================
    # BUSCAR HORARIO
    # ========================================================

    horario_match = re.search(
        r"'horario'\s*:\s*\"(.*?)\"",
        contenido,
        re.DOTALL
    )

    if not horario_match:

        print("No se encontró horario")
        continue

    horario = horario_match.group(1)

    print("\nTexto original:")
    print(horario)

    # ========================================================
    # BUSCAR DIRECCIONES
    # ========================================================

    direcciones = re.findall(
        r"De\s+(.+?)\s+a\s+(.+?):",
        horario
    )

    print("\nDirecciones detectadas:")

    if not direcciones:

        print("No se detectaron direcciones.")

    else:

        for origen, destino in direcciones:

            print(
                f"ORIGEN : {origen.strip()}"
            )

            print(
                f"DESTINO: {destino.strip()}"
            )