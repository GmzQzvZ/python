from urllib.request import urlopen, Request
import re

URL = "https://tramites.transmilenio.gov.co/public-static-pages/mapa-interactivo/mapa/reference_data.js"

request = Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153.0.0.0 Safari/537.36",
        "Accept": "text/javascript, application/javascript, */*",
        "Referer": "https://tramites.transmilenio.gov.co/mapa-interactivo"
    }
)

try:
    with urlopen(request, timeout=30) as respuesta:
        texto = respuesta.read().decode("utf-8", errors="replace")

except Exception as e:
    print("========================================")
    print("ERROR AL DESCARGAR reference_data.js")
    print("========================================")
    print(e)
    exit()


lineas = texto.splitlines()

print("========================================")
print("ARCHIVO DESCARGADO CORRECTAMENTE")
print("========================================")

print(f"Tamaño: {len(texto)} caracteres")
print(f"Líneas: {len(lineas)}")


# ============================================================
# BUSCAR DEFINICIONES DE TRAYECTOS
# ============================================================

print("\n========================================")
print("BUSCANDO DEFINICIONES DE TRAYECTOS")
print("========================================")

encontradas = 0

for i, linea in enumerate(lineas):

    if "trayectos[" in linea.lower():

        print(f"{i + 1}: {linea.strip()}")

        encontradas += 1

        if encontradas >= 30:
            break


if encontradas == 0:
    print("No se encontraron definiciones directas.")


# ============================================================
# BUSCAR TRAYECTO 18
# ============================================================

print("\n========================================")
print("BUSCANDO TRAYECTO 18")
print("========================================")

encontrado = False

for i, linea in enumerate(lineas):

    if re.search(r"trayectos\s*\[\s*['\"]?18['\"]?\s*\]", linea, re.IGNORECASE):

        print(f"\nEncontrado en línea {i + 1}:")

        for siguiente in lineas[i:i + 25]:
            print(siguiente)

        encontrado = True
        break


if not encontrado:
    print("No se encontró una definición directa de trayectos[18].")


# ============================================================
# BUSCAR POSIBLE DEFINICIÓN DEL ID 18
# ============================================================

print("\n========================================")
print("BUSCANDO POSIBLES DEFINICIONES DEL ID 18")
print("========================================")

encontrado = False

for i, linea in enumerate(lineas):

    if re.search(r"\b18\s*=", linea):

        print(f"\nPosible coincidencia en línea {i + 1}:")

        for siguiente in lineas[i:i + 20]:
            print(siguiente)

        encontrado = True


if not encontrado:
    print("No se encontraron coincidencias.")