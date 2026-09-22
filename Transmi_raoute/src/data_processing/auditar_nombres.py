import re
import unicodedata
from urllib.request import urlopen, Request


URL = (
    "https://tramites.transmilenio.gov.co/"
    "public-static-pages/mapa-interactivo/mapa/reference_data.js"
)


def normalizar(texto):

    if texto is None:
        return ""

    texto = texto.replace("&nbsp;", " ")

    # Quitamos variantes que aparecen en algunos servicios.
    texto = re.sub(
        r"\s*\[Ciclovía\]\s*$",
        "",
        texto,
        flags=re.IGNORECASE
    )

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


def palabras(texto):

    texto = normalizar(texto)

    return set(
        palabra
        for palabra in re.findall(
            r"[a-z0-9]+",
            texto
        )
        if len(palabra) >= 2
    )


def similitud_palabras(nombre_a, nombre_b):

    palabras_a = palabras(nombre_a)
    palabras_b = palabras(nombre_b)

    if not palabras_a or not palabras_b:
        return 0

    comunes = palabras_a.intersection(palabras_b)

    return len(comunes) / len(palabras_a.union(palabras_b))


# ---------------------------------------------------------
# DESCARGAR FUENTE OFICIAL
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# ESTACIONES
# ---------------------------------------------------------

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


lista_estaciones = list(
    estaciones.values()
)


# ---------------------------------------------------------
# SERVICIOS
# ---------------------------------------------------------

patron_ruta = re.compile(
    r"Datos\['([^']+)'\]\s*=\s*\{(.*?)\n\};",
    re.DOTALL
)


problemas = []


for coincidencia in patron_ruta.finditer(texto):

    servicio = coincidencia.group(1)
    contenido = coincidencia.group(2)

    if servicio in [
        "Paradas",
        "Recorridos"
    ]:
        continue

    horario_match = re.search(
        r"'horario'\s*:\s*\"(.*?)\"",
        contenido,
        re.DOTALL
    )

    if not horario_match:
        continue

    horario = horario_match.group(1)

    direcciones = re.findall(
        r"De\s+(.+?)\s+a\s+(.+?):",
        horario
    )

    for origen, destino in direcciones:

        origen = origen.strip()
        destino = destino.strip()

        origen_normalizado = normalizar(origen)
        destino_normalizado = normalizar(destino)

        origen_encontrado = False
        destino_encontrado = False

        for estacion in lista_estaciones:

            nombre_normalizado = normalizar(
                estacion["nombre"]
            )

            if nombre_normalizado == origen_normalizado:
                origen_encontrado = True

            if nombre_normalizado == destino_normalizado:
                destino_encontrado = True

        if origen_encontrado and destino_encontrado:
            continue

        problemas.append({
            "servicio": servicio,
            "origen": origen,
            "destino": destino,
            "origen_ok": origen_encontrado,
            "destino_ok": destino_encontrado
        })


# ---------------------------------------------------------
# MOSTRAR AUDITORÍA
# ---------------------------------------------------------

print()
print("=" * 70)
print("AUDITORÍA DE NOMBRES DE SERVICIOS")
print("=" * 70)

print()
print(f"Estaciones disponibles: {len(lista_estaciones)}")
print(f"Direcciones con problemas: {len(problemas)}")


for problema in problemas:

    print()
    print("-" * 70)

    print(
        f"SERVICIO: {problema['servicio']}"
    )

    print(
        f"ORIGEN:   {problema['origen']}"
    )

    print(
        f"DESTINO:  {problema['destino']}"
    )

    print(
        f"Origen encontrado exactamente: "
        f"{problema['origen_ok']}"
    )

    print(
        f"Destino encontrado exactamente: "
        f"{problema['destino_ok']}"
    )


    # -----------------------------------------------------
    # CANDIDATOS PARA EL ORIGEN
    # -----------------------------------------------------

    if not problema["origen_ok"]:

        candidatos_origen = []

        for estacion in lista_estaciones:

            puntuacion = similitud_palabras(
                problema["origen"],
                estacion["nombre"]
            )

            if puntuacion > 0:

                candidatos_origen.append(
                    (
                        puntuacion,
                        estacion["id"],
                        estacion["nombre"]
                    )
                )

        candidatos_origen.sort(
            reverse=True
        )

        print()
        print("Posibles candidatos para ORIGEN:")

        for puntuacion, estacion_id, nombre in candidatos_origen[:5]:

            print(
                f"  {puntuacion:.2f} | "
                f"{estacion_id} | "
                f"{nombre}"
            )


    # -----------------------------------------------------
    # CANDIDATOS PARA EL DESTINO
    # -----------------------------------------------------

    if not problema["destino_ok"]:

        candidatos_destino = []

        for estacion in lista_estaciones:

            puntuacion = similitud_palabras(
                problema["destino"],
                estacion["nombre"]
            )

            if puntuacion > 0:

                candidatos_destino.append(
                    (
                        puntuacion,
                        estacion["id"],
                        estacion["nombre"]
                    )
                )

        candidatos_destino.sort(
            reverse=True
        )

        print()
        print("Posibles candidatos para DESTINO:")

        for puntuacion, estacion_id, nombre in candidatos_destino[:5]:

            print(
                f"  {puntuacion:.2f} | "
                f"{estacion_id} | "
                f"{nombre}"
            )


print()
print("=" * 70)
print("FIN DE LA AUDITORÍA")
print("=" * 70)