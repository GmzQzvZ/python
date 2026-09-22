from urllib.request import urlopen, Request
import re

URL = "https://tramites.transmilenio.gov.co/public-static-pages/mapa-interactivo/mapa/reference_data.js"

request = Request(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urlopen(request, timeout=30) as respuesta:
    texto = respuesta.read().decode("utf-8", errors="replace")

lineas = texto.splitlines()

# ============================================================
# BUSCAR D22
# ============================================================

inicio = None

for i, linea in enumerate(lineas):
    if 'Datos[\'D22\']' in linea:
        inicio = i
        break

if inicio is None:
    print("No se encontró D22.")
    exit()

print("========================================")
print("INFORMACIÓN DEL SERVICIO D22")
print("========================================")

for linea in lineas[inicio:inicio + 10]:
    print(linea)

# ============================================================
# BUSCAR estacionesGlobal
# ============================================================

print("\n========================================")
print("BUSCANDO ESTACIONES 63, 64, 68...")
print("========================================\n")

ids_buscar = [63, 64, 68, 69, 71, 74, 78, 81, 84, 92, 94, 96, 97, 98, 102]

for estacion_id in ids_buscar:

    patron = rf"estacionesGlobal\['{estacion_id}'\]\s*=\s*\{{"

    encontrada = False

    for i, linea in enumerate(lineas):

        if re.search(patron, linea):

            print(f"\n--- ESTACIÓN ID {estacion_id} ---")

            for linea_estacion in lineas[i:i + 15]:
                print(linea_estacion)

            encontrada = True
            break

    if not encontrada:
        print(f"\nNo se encontró estación ID {estacion_id}")