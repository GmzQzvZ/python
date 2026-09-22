from urllib.request import urlopen, Request
import re


URL = "https://tramites.transmilenio.gov.co/public-static-pages/mapa-interactivo/mapa/reference_data.js"


# ============================================================
# DESCARGAR ARCHIVO
# ============================================================

request = Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/javascript, application/javascript, */*",
        "Referer": "https://tramites.transmilenio.gov.co/mapa-interactivo"
    }
)

with urlopen(request, timeout=30) as respuesta:
    texto = respuesta.read().decode("utf-8", errors="replace")


# ============================================================
# DICCIONARIO DE ESTACIONES
# ============================================================

estaciones = {}

patron_estacion = re.compile(
    r"estacionesGlobal\['(\d+)'\]\s*=\s*\{(.*?)\n\};",
    re.DOTALL
)

for coincidencia in patron_estacion.finditer(texto):

    estacion_id = int(coincidencia.group(1))
    contenido = coincidencia.group(2)

    x_match = re.search(r'"x"\s*:\s*(\d+)', contenido)
    y_match = re.search(r'"y"\s*:\s*(\d+)', contenido)
    nombre_match = re.search(r'"text"\s*:\s*\'([^\']*)\'', contenido)

    if x_match and y_match:

        estaciones[estacion_id] = {
            "x": int(x_match.group(1)),
            "y": int(y_match.group(1)),
            "nombre": nombre_match.group(1) if nombre_match else "Sin nombre"
        }


# ============================================================
# ESTACIONES DE D22
# ============================================================

ids_d22 = [
    63, 64, 68, 69, 71,
    74, 78, 81, 84,
    92, 94, 96, 97, 98, 102
]


print("========================================")
print("ESTACIONES D22")
print("========================================")

for posicion, estacion_id in enumerate(ids_d22, start=1):

    estacion = estaciones.get(estacion_id)

    if estacion:

        print(
            f"{posicion:02d}. "
            f"ID {estacion_id}: "
            f"{estacion['nombre']} "
            f"→ ({estacion['x']}, {estacion['y']})"
        )

    else:
        print(f"{posicion:02d}. ID {estacion_id}: NO ENCONTRADA")


# ============================================================
# BUSCAR TRAYECTOS 18-27
# ============================================================

print("\n========================================")
print("TRAYECTOS DE D22")
print("========================================")


trayectos = {}

ids_trayectos_d22 = [
    18, 19, 20, 21, 22, 23,
    24, 25, 26, 27, 38, 39
]

for trayecto_id in ids_trayectos_d22:

    patron = rf"trayectos\[{trayecto_id}\]\s*=\s*\{{(.*?)\n\}};"

    encontrado = re.search(
        patron,
        texto,
        re.DOTALL
    )

    if encontrado:

        contenido = encontrado.group(1)

        coordenadas = re.findall(
            r"x\s*:\s*(\d+).*?y\s*:\s*(\d+)",
            contenido,
            re.DOTALL
        )

        if len(coordenadas) >= 2:

            inicio = (
                int(coordenadas[0][0]),
                int(coordenadas[0][1])
            )

            fin = (
                int(coordenadas[1][0]),
                int(coordenadas[1][1])
            )

            trayectos[trayecto_id] = {
                "inicio": inicio,
                "fin": fin
            }

            print(
                f"Trayecto {trayecto_id}: "
                f"{inicio} → {fin}"
            )


# ============================================================
# COMPARAR EXTREMOS CON ESTACIONES
# ============================================================

print("\n========================================")
print("COMPARACIÓN CON ESTACIONES")
print("========================================")


for trayecto_id, datos in trayectos.items():

    inicio = datos["inicio"]
    fin = datos["fin"]

    print(f"\nTrayecto {trayecto_id}")

    print(f"  Inicio: {inicio}")
    print(f"  Fin:    {fin}")

    for estacion_id in ids_d22:

        estacion = estaciones.get(estacion_id)

        if not estacion:
            continue

        ex = estacion["x"]
        ey = estacion["y"]

        distancia_inicio = (
            (ex - inicio[0]) ** 2 +
            (ey - inicio[1]) ** 2
        ) ** 0.5

        distancia_fin = (
            (ex - fin[0]) ** 2 +
            (ey - fin[1]) ** 2
        ) ** 0.5

        if distancia_inicio <= 40 or distancia_fin <= 40:

            print(
                f"  Cerca de estación "
                f"{estacion_id} - {estacion['nombre']} "
                f"(inicio={distancia_inicio:.2f}, "
                f"fin={distancia_fin:.2f})"
            )