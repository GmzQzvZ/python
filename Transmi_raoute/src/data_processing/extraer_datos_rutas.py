from urllib.request import urlopen, Request

URL = "https://tramites.transmilenio.gov.co/public-static-pages/mapa-interactivo/mapa/reference_data.js"

request = Request(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urlopen(request, timeout=30) as respuesta:
    texto = respuesta.read().decode("utf-8", errors="replace")

lineas = texto.splitlines()

inicio = None
fin = None

for i, linea in enumerate(lineas):

    if "//Creación de Rutas con paraderos" in linea:
        inicio = i

    if inicio is not None and "//Servicios Duales" in linea:
        fin = i
        break

if inicio is None:
    print("No se encontró el inicio de Datos.")
    exit()

if fin is None:
    fin = len(lineas)

print("Inicio:", inicio + 1)
print("Fin:", fin + 1)
print("Líneas encontradas:", fin - inicio)

print("\n========================================")
print("DATOS DE RUTAS CON PARADEROS")
print("========================================\n")

for numero, linea in enumerate(lineas[inicio:fin], start=inicio + 1):
    print(f"{numero}: {linea}")