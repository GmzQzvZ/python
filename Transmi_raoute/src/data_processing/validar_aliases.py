import re
import unicodedata
from urllib.request import urlopen, Request


URL = (
    "https://tramites.transmilenio.gov.co/"
    "public-static-pages/mapa-interactivo/mapa/reference_data.js"
)


# =========================================================
# NORMALIZACIÓN
# =========================================================

def normalizar(texto):

    if texto is None:
        return ""

    texto = texto.replace("&nbsp;", " ")

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


# =========================================================
# DESCARGAR FUENTE
# =========================================================

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


# =========================================================
# ESTACIONES
# =========================================================

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


indice = {}

for estacion in estaciones.values():

    nombre = normalizar(
        estacion["nombre"]
    )

    indice.setdefault(
        nombre,
        []
    ).append(estacion)


# =========================================================
# ALIAS CONFIRMADOS POR LA AUDITORÍA
# =========================================================

ALIAS = {

    "portal del sur":
        "portal sur jfk coop. financiera",

    "portal de la 80":
        "portal 80",

    "portal del norte":
        "portal norte",

    "toberin":
        "toberin foundever",

    "las aguas":
        "las aguas centro colombo americano",

    "universidades":
        "universidades - cityu",

    "san mateo":
        "san mateo c.c. unisur",

    "museo nacional":
        "museo nacional fng",

    "flores":
        "flores areandina",

    "alcala":
        "alcala - colegio s. tomas dominicos",

    "calle 76":
        "calle 76 - san felipe",

    "portal el dorado":
        "portal el dorado",

    "portal eldorado":
        "&nbsp &nbsp &nbsp portal eldorado &nbsp &nbsp &nbsp cc nuestro bogota",

}


# =========================================================
# FUNCIÓN DE RESOLUCIÓN
# =========================================================

def resolver_nombre(nombre):

    nombre_normalizado = normalizar(
        nombre
    )

    # 1. Coincidencia exacta
    if nombre_normalizado in indice:

        resultados = indice[
            nombre_normalizado
        ]

        if len(resultados) == 1:

            return {
                "estado": "EXACTO",
                "estacion": resultados[0]
            }

    # 2. Alias explícito
    if nombre_normalizado in ALIAS:

        nombre_alias = ALIAS[
            nombre_normalizado
        ]

        resultados = indice.get(
            nombre_alias,
            []
        )

        if len(resultados) == 1:

            return {
                "estado": "ALIAS",
                "estacion": resultados[0]
            }

    # 3. No resolver automáticamente
    return {
        "estado": "NO_RESUELTO",
        "estacion": None
    }


# =========================================================
# PRUEBAS
# =========================================================

pruebas = [

    "Portal del Sur",
    "Portal de la 80",
    "Portal del Norte",
    "Toberín",
    "Las Aguas",
    "Universidades",
    "San Mateo",
    "Museo Nacional",
    "Flores",
    "Alcalá",
    "Calle 76",
    "Portal Eldorado",

    # Casos que NO debemos resolver automáticamente
    "Aeropuerto Eldorado",
    "Hacienda Santa Bárbara",
    "Fundación Santa Fe",
    "Clínica El Bosque",
    "Ginebra Norte",
    "Puente de Guadua",
    "ETB Tibabuyes",
    "K7 con Calle 72",
]


print()
print("=" * 70)
print("VALIDACIÓN DE ALIAS")
print("=" * 70)


for nombre in pruebas:

    resultado = resolver_nombre(
        nombre
    )

    print()
    print(f"NOMBRE: {nombre}")
    print(f"ESTADO: {resultado['estado']}")

    if resultado["estacion"]:

        print(
            f"ID:     {resultado['estacion']['id']}"
        )

        print(
            f"FUENTE: {resultado['estacion']['nombre']}"
        )


print()
print("=" * 70)
print("FIN")
print("=" * 70)