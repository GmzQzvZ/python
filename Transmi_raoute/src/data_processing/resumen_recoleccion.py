import json
from pathlib import Path
from collections import Counter


# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def cargar_json(nombre_archivo, carpeta):
    """Carga un archivo JSON desde la carpeta indicada."""
    ruta = carpeta / nombre_archivo

    if not ruta.exists():
        print(f"⚠️ No se encontró: {ruta}")
        return None

    with ruta.open(encoding="utf-8") as archivo:
        return json.load(archivo)


def obtener_features(datos):
    """Obtiene la lista de registros de un JSON de ArcGIS."""
    if not datos:
        return []

    if isinstance(datos, dict):
        return datos.get("features", [])

    if isinstance(datos, list):
        return datos

    return []


def obtener_atributos(feature):
    """Obtiene los atributos de un registro."""
    if isinstance(feature, dict):
        return feature.get("attributes", feature)

    return {}


# ============================================================
# ESTACIONES
# ============================================================

def analizar_estaciones(datos):
    features = obtener_features(datos)
    registros = [obtener_atributos(f) for f in features]

    nombres = []
    troncales = []
    trazados = []

    for registro in registros:
        nombre = registro.get("nombre_estacion")
        troncal = registro.get("troncal_estacion")
        trazado = registro.get("trazado_estacion")

        if nombre:
            nombres.append(nombre)

        if troncal:
            troncales.append(troncal)

        if trazado:
            trazados.append(trazado)

    return {
        "total": len(registros),
        "nombres_unicos": len(set(nombres)),
        "troncales": Counter(troncales),
        "trazados": Counter(trazados),
    }


# ============================================================
# RUTAS
# ============================================================

def analizar_rutas(datos):
    features = obtener_features(datos)
    registros = [obtener_atributos(f) for f in features]

    nombres_rutas = []
    servicios = []
    tipos = []
    operaciones = []
    buses = []
    origenes = []
    destinos = []

    for registro in registros:

        ruta = registro.get("route_name_ruta_troncal")
        servicio = registro.get("servicio_unico_ruta_troncal")
        tipo = registro.get("tipo_ruta_troncal")
        operacion = registro.get("operacion_ruta_troncal")
        bus = registro.get("tipo_bus_ruta_troncal")
        origen = registro.get("origen_ruta_troncal")
        destino = registro.get("destino_ruta_troncal")

        if ruta:
            nombres_rutas.append(ruta)

        if servicio:
            servicios.append(servicio)

        if tipo:
            tipos.append(tipo)

        if operacion:
            operaciones.append(operacion)

        if bus:
            buses.append(bus)

        if origen:
            origenes.append(origen)

        if destino:
            destinos.append(destino)

    return {
        "total": len(registros),
        "rutas_unicas": len(set(nombres_rutas)),
        "servicios": Counter(servicios),
        "tipos": Counter(tipos),
        "operaciones": Counter(operaciones),
        "buses": Counter(buses),
        "origenes": Counter(origenes),
        "destinos": Counter(destinos),
    }


# ============================================================
# EQUIVALENCIAS
# ============================================================

def analizar_equivalencias(datos):
    features = obtener_features(datos)
    registros = [obtener_atributos(f) for f in features]

    return {
        "total": len(registros)
    }


# ============================================================
# RUTAS PROCESADAS
# ============================================================

def analizar_rutas_procesadas(datos):
    if not isinstance(datos, dict):
        return {
            "rutas": 0,
            "direcciones": 0,
            "construidas": 0,
            "pendientes": 0,
        }

    rutas = datos.get("rutas", {})

    total_rutas = len(rutas)
    total_direcciones = 0
    construidas = 0
    pendientes = 0

    for ruta in rutas.values():

        direcciones = ruta.get("direcciones", [])

        total_direcciones += len(direcciones)

        for direccion in direcciones:

            if direccion.get("estado") == "construida":
                construidas += 1
            else:
                pendientes += 1

    return {
        "rutas": total_rutas,
        "direcciones": total_direcciones,
        "construidas": construidas,
        "pendientes": pendientes,
    }


# ============================================================
# MOSTRAR RESUMEN
# ============================================================

def imprimir_resumen():

    print()
    print("=" * 65)
    print("🚍 TRANSmi ROUTE - RESUMEN DE RECOLECCIÓN DE INFORMACIÓN")
    print("=" * 65)

    # --------------------------------------------------------
    # ESTACIONES
    # --------------------------------------------------------

    estaciones = cargar_json(
        "estaciones_troncales_raw.json",
        RAW_DIR
    )

    info_estaciones = analizar_estaciones(estaciones)

    print()
    print("📍 ESTACIONES")
    print("-" * 65)

    print(f"Total de estaciones recolectadas: {info_estaciones['total']}")
    print(f"Nombres únicos: {info_estaciones['nombres_unicos']}")

    if info_estaciones["troncales"]:
        print("\n🚏 Estaciones por troncal:")

        for troncal, cantidad in sorted(
            info_estaciones["troncales"].items()
        ):
            print(f"   • {troncal}: {cantidad}")

    if info_estaciones["trazados"]:
        print("\n🛤️ Estaciones por trazado:")

        for trazado, cantidad in sorted(
            info_estaciones["trazados"].items()
        ):
            print(f"   • {trazado}: {cantidad}")

    # --------------------------------------------------------
    # RUTAS
    # --------------------------------------------------------

    rutas = cargar_json(
        "rutas_troncales_raw.json",
        RAW_DIR
    )

    info_rutas = analizar_rutas(rutas)

    print()
    print("🚌 RUTAS")
    print("-" * 65)

    print(f"Total de registros de rutas: {info_rutas['total']}")
    print(f"Rutas únicas: {info_rutas['rutas_unicas']}")

    if info_rutas["servicios"]:
        print("\n🔢 Servicios:")

        for servicio, cantidad in sorted(
            info_rutas["servicios"].items()
        ):
            print(f"   • {servicio}: {cantidad}")

    if info_rutas["tipos"]:
        print("\n🚍 Tipos de ruta:")

        for tipo, cantidad in sorted(
            info_rutas["tipos"].items()
        ):
            print(f"   • {tipo}: {cantidad}")

    if info_rutas["operaciones"]:
        print("\n⚙️ Estado de operación:")

        for estado, cantidad in sorted(
            info_rutas["operaciones"].items()
        ):
            print(f"   • {estado}: {cantidad}")

    if info_rutas["buses"]:
        print("\n🚌 Tipo de bus:")

        for bus, cantidad in sorted(
            info_rutas["buses"].items()
        ):
            print(f"   • {bus}: {cantidad}")

    # --------------------------------------------------------
    # EQUIVALENCIAS
    # --------------------------------------------------------

    equivalencias = cargar_json(
        "equivalencias_estaciones_rutas_raw.json",
        RAW_DIR
    )

    info_equivalencias = analizar_equivalencias(equivalencias)

    print()
    print("🔗 EQUIVALENCIAS")
    print("-" * 65)

    print(
        f"Registros de equivalencias recolectados: "
        f"{info_equivalencias['total']}"
    )

    # --------------------------------------------------------
    # DATOS PROCESADOS
    # --------------------------------------------------------

    rutas_procesadas = cargar_json(
        "rutas_orientadas.json",
        PROCESSED_DIR
    )

    info_procesadas = analizar_rutas_procesadas(
        rutas_procesadas
    )

    print()
    print("🧠 DATOS PROCESADOS")
    print("-" * 65)

    print(f"Rutas procesadas: {info_procesadas['rutas']}")
    print(f"Direcciones: {info_procesadas['direcciones']}")
    print(f"Direcciones construidas: {info_procesadas['construidas']}")
    print(f"Direcciones pendientes: {info_procesadas['pendientes']}")

    # --------------------------------------------------------
    # RESUMEN FINAL
    # --------------------------------------------------------

    print()
    print("=" * 65)
    print("📊 RESUMEN GENERAL")
    print("=" * 65)

    print(
        f"📍 Estaciones recolectadas: "
        f"{info_estaciones['total']}"
    )

    print(
        f"🚌 Registros de rutas: "
        f"{info_rutas['total']}"
    )

    print(
        f"🔗 Equivalencias: "
        f"{info_equivalencias['total']}"
    )

    print(
        f"🧠 Rutas procesadas: "
        f"{info_procesadas['rutas']}"
    )

    print(
        f"➡️ Direcciones construidas: "
        f"{info_procesadas['construidas']}"
    )

    print(
        f"⚠️ Direcciones pendientes: "
        f"{info_procesadas['pendientes']}"
    )

    print()
    print("=" * 65)
    print("✅ Fin del resumen")
    print("=" * 65)
    print()


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    imprimir_resumen()