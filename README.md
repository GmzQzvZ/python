# 🚍 TransMi Route

Sistema inteligente desarrollado en Python para encontrar rutas entre estaciones del sistema TransMilenio mediante **representación del conocimiento, grafos, reglas de decisión y búsqueda en amplitud (BFS)**.

## 📌 Descripción

TransMi Route permite ingresar una estación de origen y una estación de destino para encontrar un recorrido dentro de la red modelada.

El sistema:

- Representa las estaciones como nodos de un grafo.
- Representa las conexiones entre estaciones como aristas dirigidas.
- Utiliza **BFS (Breadth-First Search)** para buscar recorridos.
- Reconoce estaciones mediante ID, nombre y algunos alias validados.
- Identifica los servicios utilizados durante el recorrido.
- Detecta transbordos entre servicios.
- Calcula métricas de la ruta.
- Aplica una política configurable de selección.
- Presenta los resultados mediante una interfaz gráfica desarrollada con **Tkinter**.

> **Nota:** la política de selección es una decisión académica configurable. No representa una definición universal de la "mejor ruta".

## 🎯 Objetivo

Desarrollar un sistema inteligente en Python que represente la red de estaciones del componente troncal de TransMilenio como un grafo, utilice búsqueda en amplitud (BFS) para encontrar recorridos entre dos estaciones y aplique criterios configurables para evaluar y presentar los resultados.

## 🧠 Conceptos utilizados

### Representación del conocimiento
La información del sistema se organiza mediante estaciones, rutas, direcciones, servicios y conexiones.

### Grafo
- **Nodo:** estación física.
- **Arista:** conexión dirigida entre dos estaciones consecutivas.
- **Metadatos:** información relacionada con el servicio y el recorrido.

### Búsqueda BFS
BFS explora el grafo por niveles hasta encontrar el destino y posteriormente reconstruye el recorrido.

### Reglas
La política inicial utiliza, en este orden:

1. Menor cantidad de transbordos.
2. Menor cantidad de estaciones.
3. Menor cantidad de servicios.

## 🏗️ Arquitectura

```text
Datos de referencia
        ↓
Procesamiento de datos
        ↓
Rutas orientadas
        ↓
Base de conocimiento
        ↓
Construcción del grafo
        ↓
Búsqueda BFS
        ↓
Evaluación de la ruta
        ↓
Reglas de selección
        ↓
Interfaz gráfica
```

## 📁 Estructura

```text
Transmi_raoute/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── algorithms/
│   │   └── bfs.py
│   ├── knowledge/
│   │   ├── base_conocimiento.py
│   │   └── reglas.py
│   ├── routing/
│   │   └── evaluador.py
│   ├── utils/
│   └── data_processing/
│
├── tests/
│   ├── test_bfs.py
│   ├── test_evaluador.py
│   ├── test_integracion.py
│   ├── test_main.py
│   └── test_reglas.py
│
├── ui/
│   ├── __init__.py
│   └── app.py
│
├── main.py
├── .gitignore
└── README.md
```

## 📊 Datos validados

La versión validada del proyecto cuenta con:

- **90 rutas**
- **99 direcciones**
- **99 direcciones construidas**
- **0 direcciones pendientes**
- **0 errores de orientación**
- **134 estaciones en el grafo**
- **919 aristas dirigidas**

La cantidad de aristas coincide con las conexiones consecutivas calculadas a partir de las rutas orientadas.

## 🔎 Ejemplos

### Portal Eldorado → Calle 76

```text
Origen: Portal Eldorado
Destino: Calle 76

Resultado: Ruta encontrada
Cantidad de estaciones: 7
```

### ID 103 → ID 116

```text
Origen: 103
Destino: 116

Resultado: Ruta encontrada
Cantidad de estaciones: 6
```

### Portal del Sur → Portal del Norte

```text
Origen: Portal del Sur
Destino: Portal del Norte

Resultado: Ruta encontrada
Cantidad de estaciones: 5
```

También se probaron alias, entradas inexistentes y casos de ambigüedad.

## 🚌 Servicios y transbordos

El sistema diferencia la estación física del servicio que circula por ella.

Cuando el servicio cambia durante el recorrido, se registra un **transbordo**:

```text
Servicio A
    ↓
🚉 Estación de transbordo
    ↓
Servicio B
```

## 🖥️ Interfaz gráfica

La interfaz fue desarrollada con **Tkinter** y permite:

- Ingresar origen.
- Ingresar destino.
- Buscar una ruta.
- Visualizar las estaciones.
- Consultar cantidad de estaciones y tramos.
- Consultar servicios utilizados.
- Identificar transbordos.
- Mostrar mensajes cuando no existe una ruta o la entrada no puede resolverse.

La presentación utiliza una leyenda visual para diferenciar elementos del recorrido:

- 🔴 Troncal
- 🟡 Biarticulado
- 🔵 Alimentador
- 🟣 Portal
- ⚪ Estación
- 🔄 Transbordo

## ▶️ Ejecución

### Requisitos

- Python 3.x
- Tkinter

### Interfaz gráfica

Desde la raíz del proyecto:

```bash
python -m ui.app
```

### Versión de consola

```bash
python main.py
```

## 🧪 Pruebas

El proyecto cuenta con pruebas para:

- Construcción del grafo.
- Búsqueda BFS.
- Evaluación de rutas.
- Reglas de selección.
- Integración.
- Entrada principal.

Estado validado:

## 💻 text
33 pruebas 
OK ✔️
```

## 🛡️ Manejo de errores

El sistema contempla:

```text
origen_no_existe
destino_no_existe
origen_ambiguo
destino_ambiguo
sin_ruta
```

Cuando existe ambigüedad, el sistema informa el estado correspondiente en lugar de seleccionar arbitrariamente una estación.

## 📦 Datos procesados

Los principales archivos utilizados son:

```text
data/processed/rutas_transmi.json
data/processed/rutas_orientadas.json
```

## 🔗 Fuentes de información

Los datos de referencia provienen de información abierta publicada por **TRANSMILENIO S.A.**, incluyendo información relacionada con rutas troncales, estaciones troncales, trazados y equivalencias de estaciones.

## ⚠️ Limitaciones

Actualmente el proyecto:

- Trabaja con datos procesados localmente.
- No utiliza tráfico en tiempo real.
- No calcula tiempos reales de llegada.
- No considera congestión en tiempo real.
- No incorpora todavía criterios de accesibilidad.
- Utiliza una política de selección configurable definida para el proyecto.

## 🚀 Posibles mejoras

- Integración de información en tiempo real.
- Tiempos estimados de viaje.
- Visualización sobre un mapa.
- Información de horarios.
- Criterios de accesibilidad.
- Mayor detalle de los tipos de servicio.
- Comparación de recorridos.

## 🛠️ Tecnologías

- Python
- Tkinter
- JSON
- Git / GitHub
- Breadth-First Search (BFS)
- Grafos
- `unittest`

## 📚 Propósito académico

El proyecto aplica conceptos de **Inteligencia Artificial**, especialmente:

- Sistemas basados en conocimiento.
- Representación del conocimiento.
- Reglas.
- Estrategias de búsqueda.
- Grafos.
- Algoritmos de búsqueda en Python.

## 📄 Documentación

La documentación detallada se encuentra en:

**TransMi Route - Especificaciones del Proyecto**

Incluye problema, objetivos, fundamentación conceptual, arquitectura, algoritmo, reglas, pruebas, resultados, limitaciones y conclusiones.

## 👥 Equipo

**Integrantes:**

- Julian David Sanchez
- Juan Sebastian Gomez

## 📌 Estado

**Estado:** Funcional para el alcance académico definido.

La versión validada incluye construcción del grafo, búsqueda BFS, evaluación, reglas, resolución de alias, pruebas automatizadas e interfaz gráfica.
