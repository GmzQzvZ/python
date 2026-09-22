from urllib.request import urlopen, Request

URL = "https://tramites.transmilenio.gov.co/public-static-pages/mapa-interactivo/mapa/reference_data.js"

request = Request(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urlopen(request, timeout=30) as respuesta:
    texto = respuesta.read().decode("utf-8", errors="replace")

lineas = texto.splitlines()

print("Tamaño:", len(texto), "caracteres")
print("Líneas:", len(lineas))

print("\n========================================")
print("VARIABLES / ESTRUCTURAS EN EL ARCHIVO")
print("========================================\n")

palabras = [
    "var ",
    "const ",
    "let ",
    "ruta",
    "rutas",
    "route",
    "routes",
    "servicio",
    "servicios",
    "service",
    "services",
    "estacionesGlobal",
]

encontradas = 0

for numero, linea in enumerate(lineas, start=1):

    linea_minuscula = linea.lower()

    # Mostrar declaraciones de variables
    if (
        linea.strip().startswith("var ")
        or linea.strip().startswith("const ")
        or linea.strip().startswith("let ")
    ):
        print(f"{numero}: {linea[:500]}")
        encontradas += 1

    # Mostrar variables que parezcan relacionadas con rutas
    elif any(palabra in linea_minuscula for palabra in [
        "ruta",
        "rutas",
        "route",
        "routes",
        "servicio",
        "servicios",
        "service",
        "services",
    ]):
        print(f"{numero}: {linea[:500]}")
        encontradas += 1

print("\n========================================")
print("TOTAL DE COINCIDENCIAS:", encontradas)
print("========================================")