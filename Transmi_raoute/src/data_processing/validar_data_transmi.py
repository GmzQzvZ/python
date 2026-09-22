import json


ARCHIVO = "data/processed/rutas_transmi.json"


# ============================================================
# CARGAR DATA
# ============================================================

with open(
    ARCHIVO,
    "r",
    encoding="utf-8"
) as archivo:

    data = json.load(archivo)


estaciones = {}

for ruta in data["rutas"].values():

    for estacion in ruta["estaciones"]:

        estaciones[estacion["id"]] = estacion


rutas = data["rutas"]


# ============================================================
# RESUMEN
# ============================================================

print("========================================")
print("VALIDACIÓN DE DATA TRANSMILENIO")
print("========================================")

print(f"Rutas:      {len(rutas)}")
print(f"Estaciones: {len(estaciones)}")


# ============================================================
# ESTACIONES SIN NOMBRE
# ============================================================

print("\n========================================")
print("ESTACIONES SIN NOMBRE")
print("========================================")

sin_nombre = [
    estacion
    for estacion in estaciones.values()
    if not estacion["nombre"]
]

print(f"Cantidad: {len(sin_nombre)}")

for estacion in sin_nombre:

    print(
        f"ID {estacion['id']} "
        f"- nombre={estacion['nombre']}"
    )


# ============================================================
# RUTAS SIN ESTACIONES
# ============================================================

print("\n========================================")
print("RUTAS SIN ESTACIONES")
print("========================================")

rutas_sin_estaciones = []

for nombre, ruta in rutas.items():

    if not ruta["estaciones"]:

        rutas_sin_estaciones.append(nombre)


print(
    f"Cantidad: "
    f"{len(rutas_sin_estaciones)}"
)

for nombre in rutas_sin_estaciones:

    print(nombre)


# ============================================================
# RUTAS CON ESTACIONES NO ENCONTRADAS
# ============================================================

print("\n========================================")
print("ESTACIONES NO RESUELTAS")
print("========================================")

no_resueltas = []

for nombre, ruta in rutas.items():

    for estacion in ruta["estaciones"]:

        if estacion["nombre"] is None:

            no_resueltas.append(
                (
                    nombre,
                    estacion["id"]
                )
            )


print(
    f"Cantidad: "
    f"{len(no_resueltas)}"
)

for ruta, estacion_id in no_resueltas:

    print(
        f"Ruta {ruta} "
        f"-> estación {estacion_id}"
    )


# ============================================================
# CANTIDAD DE ESTACIONES POR RUTA
# ============================================================

print("\n========================================")
print("ESTACIONES POR SERVICIO")
print("========================================")

for nombre, ruta in sorted(rutas.items()):

    print(
        f"{nombre:5} -> "
        f"{len(ruta['estaciones']):2} estaciones"
    )


# ============================================================
# PROBAR SERVICIOS ESPECÍFICOS
# ============================================================

for nombre in ["1", "D22", "G22"]:

    print("\n========================================")
    print(f"DETALLE SERVICIO {nombre}")
    print("========================================")

    if nombre not in rutas:

        print("NO ENCONTRADO")
        continue

    ruta = rutas[nombre]

    print(f"Servicio: {ruta['servicio']}")
    print(f"Horario:  {ruta['horario']}")

    print("\nSecuencia:")

    nombres = [
        estacion["nombre"]
        for estacion in ruta["estaciones"]
    ]

    print(
        " -> ".join(
            str(nombre)
            for nombre in nombres
        )
    )


# ============================================================
# COMPARAR D22 Y G22
# ============================================================

print("\n========================================")
print("COMPARACIÓN D22 vs G22")
print("========================================")

if "D22" in rutas and "G22" in rutas:

    d22 = [
        estacion["id"]
        for estacion in rutas["D22"]["estaciones"]
    ]

    g22 = [
        estacion["id"]
        for estacion in rutas["G22"]["estaciones"]
    ]

    print("D22:")
    print(d22)

    print("\nG22:")
    print(g22)

    print("\n¿G22 es la inversa de D22?")

    print(
        g22 == list(reversed(d22))
    )


# ============================================================
# RUTAS DUPLICADAS POR SECUENCIA
# ============================================================

print("\n========================================")
print("SECUENCIAS DUPLICADAS")
print("========================================")

secuencias = {}

for nombre, ruta in rutas.items():

    secuencia = tuple(
        estacion["id"]
        for estacion in ruta["estaciones"]
    )

    secuencias.setdefault(
        secuencia,
        []
    ).append(nombre)


duplicadas = [
    nombres
    for nombres in secuencias.values()
    if len(nombres) > 1
]


print(
    f"Grupos de secuencias iguales: "
    f"{len(duplicadas)}"
)

for nombres in duplicadas:

    print(
        " -> ".join(nombres)
    )


# ============================================================
# FINAL
# ============================================================

print("\n========================================")
print("VALIDACIÓN TERMINADA")
print("========================================")