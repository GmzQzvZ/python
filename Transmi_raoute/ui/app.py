import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.routing.evaluador import buscar_ruta


class TransmiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TransMi Route")
        self.root.geometry("800x700")
        self.root.minsize(700, 600)

        self.colores = {
            "rojo": "#C62828",
            "amarillo": "#F9A825",
            "azul": "#1565C0",
            "morado": "#7B1FA2",
            "naranja": "#EF6C00",
            "gris": "#555555",
            "verde": "#2E7D32",
        }

        self.crear_interfaz()

    def crear_interfaz(self):
        titulo = tk.Label(
            self.root,
            text="🚍 TransMi Route",
            font=("Arial", 24, "bold"),
        )
        titulo.pack(pady=(20, 5))

        subtitulo = tk.Label(
            self.root,
            text="Encuentra una ruta entre estaciones de TransMilenio",
            font=("Arial", 11),
        )
        subtitulo.pack(pady=(0, 15))

        self.crear_leyenda()

        formulario = tk.Frame(self.root)
        formulario.pack(pady=15)

        tk.Label(
            formulario,
            text="📍 Origen:",
            font=("Arial", 11, "bold"),
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=8,
            sticky="e",
        )

        self.entrada_origen = tk.Entry(
            formulario,
            width=42,
            font=("Arial", 11),
        )
        self.entrada_origen.grid(
            row=0,
            column=1,
            padx=10,
            pady=8,
        )

        tk.Label(
            formulario,
            text="🏁 Destino:",
            font=("Arial", 11, "bold"),
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=8,
            sticky="e",
        )

        self.entrada_destino = tk.Entry(
            formulario,
            width=42,
            font=("Arial", 11),
        )
        self.entrada_destino.grid(
            row=1,
            column=1,
            padx=10,
            pady=8,
        )

        boton_buscar = tk.Button(
            self.root,
            text="🔎 Buscar ruta",
            command=self.buscar,
            font=("Arial", 11, "bold"),
            padx=25,
            pady=9,
            cursor="hand2",
        )
        boton_buscar.pack(pady=10)

        marco_resultado = tk.Frame(self.root)
        marco_resultado.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True,
        )

        scrollbar = tk.Scrollbar(marco_resultado)
        scrollbar.pack(side="right", fill="y")

        self.resultado = tk.Text(
            marco_resultado,
            width=85,
            height=25,
            font=("Consolas", 10),
            state="disabled",
            wrap="word",
            yscrollcommand=scrollbar.set,
        )
        self.resultado.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.config(command=self.resultado.yview)

        self.configurar_estilos_texto()

    def crear_leyenda(self):
        marco = tk.LabelFrame(
            self.root,
            text="  🎨 Leyenda  ",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=8,
        )
        marco.pack(
            padx=25,
            fill="x",
        )

        etiquetas = [
            ("🔴 Troncal", self.colores["rojo"]),
            ("🟡 Biarticulado", self.colores["amarillo"]),
            ("🔵 Alimentador", self.colores["azul"]),
            ("🟣 Portal", self.colores["morado"]),
            ("⚪ Estación", self.colores["gris"]),
            ("🔄 Transbordo", self.colores["naranja"]),
        ]

        for texto, color in etiquetas:
            tk.Label(
                marco,
                text=texto,
                font=("Arial", 9, "bold"),
                fg=color,
            ).pack(
                side="left",
                padx=10,
            )

    def configurar_estilos_texto(self):
        self.resultado.tag_configure(
            "titulo",
            font=("Arial", 15, "bold"),
        )

        self.resultado.tag_configure(
            "seccion",
            font=("Arial", 11, "bold"),
        )

        self.resultado.tag_configure(
            "portal",
            foreground=self.colores["morado"],
            font=("Consolas", 10, "bold"),
        )

        self.resultado.tag_configure(
            "estacion",
            foreground=self.colores["gris"],
        )

        self.resultado.tag_configure(
            "troncal",
            foreground=self.colores["rojo"],
            font=("Consolas", 10, "bold"),
        )

        self.resultado.tag_configure(
            "transbordo",
            foreground=self.colores["naranja"],
            font=("Consolas", 10, "bold"),
        )

        self.resultado.tag_configure(
            "resumen",
            foreground=self.colores["verde"],
            font=("Consolas", 10, "bold"),
        )

    def insertar_linea(self, texto="", etiqueta=None):
        self.resultado.config(state="normal")

        if etiqueta:
            self.resultado.insert(
                tk.END,
                texto + "\n",
                etiqueta,
            )
        else:
            self.resultado.insert(
                tk.END,
                texto + "\n",
            )

        self.resultado.config(state="disabled")

    def limpiar_resultado(self):
        self.resultado.config(state="normal")
        self.resultado.delete("1.0", tk.END)
        self.resultado.config(state="disabled")

    def es_portal(self, nombre):
        nombre_normalizado = nombre.lower()

        return (
            "portal" in nombre_normalizado
            or "portal del" in nombre_normalizado
        )

    def mostrar_resultado(self, resultado, origen, destino):
        self.limpiar_resultado()

        ruta = resultado["ruta"]
        evaluacion = resultado["evaluacion"]
        metricas = evaluacion["metricas"]

        self.insertar_linea(
            "🚍 RUTA ENCONTRADA",
            "titulo",
        )

        self.insertar_linea()

        self.insertar_linea(
            f"📍 Origen: {origen}",
        )

        self.insertar_linea(
            f"🏁 Destino: {destino}",
        )

        self.insertar_linea()

        self.insertar_linea(
            "🛤️ RECORRIDO",
            "seccion",
        )

        self.insertar_linea(
            "La ruta encontrada utiliza las siguientes estaciones:"
        )

        self.insertar_linea()

        for indice, estacion in enumerate(
            ruta["estaciones"],
            start=1,
        ):
            nombre = estacion["nombre"]
            estacion_id = estacion["id"]

            if indice == 1:
                icono = "📍"
            elif indice == len(ruta["estaciones"]):
                icono = "🏁"
            elif self.es_portal(nombre):
                icono = "🟣"
            else:
                icono = "⚪"

            etiqueta = (
                "portal"
                if self.es_portal(nombre)
                else "estacion"
            )

            self.insertar_linea(
                f"{icono} {indice}. {nombre} "
                f"(ID: {estacion_id})",
                etiqueta,
            )

        self.insertar_linea()

        self.insertar_linea(
            "📊 RESUMEN DEL RECORRIDO",
            "seccion",
        )

        self.insertar_linea(
            f"🚉 Estaciones:     "
            f"{metricas['cantidad_estaciones']}",
            "resumen",
        )

        self.insertar_linea(
            f"🛤️ Tramos:         "
            f"{metricas['cantidad_tramos']}",
            "resumen",
        )

        self.insertar_linea(
            f"🔄 Transbordos:    "
            f"{metricas['cantidad_transbordos']}",
            "resumen",
        )

        self.insertar_linea(
            f"🚌 Servicios:      "
            f"{metricas['cantidad_servicios']}",
            "resumen",
        )

        self.insertar_linea()

        self.insertar_linea(
            "🚌 SERVICIOS UTILIZADOS",
            "seccion",
        )

        cantidad_servicios = metricas["cantidad_servicios"]

        self.insertar_linea(
            f"La ruta utiliza {cantidad_servicios} "
            f"servicio(s) troncal(es) durante el recorrido."
        )

        self.insertar_linea(
            "El número mostrado corresponde al identificador "
            "interno del servicio en los datos del sistema."
        )

        self.insertar_linea()

        for indice, servicio in enumerate(
            metricas["servicios_utilizados"],
            start=1,
        ):
            if indice == 1:
                descripcion = "Inicio del recorrido"
            else:
                descripcion = (
                    "Se utiliza después de un transbordo"
                )

            self.insertar_linea(
                f"🔴 Servicio troncal — ID {servicio}",
                "troncal",
            )

            self.insertar_linea(
                f"   ➜ {descripcion}"
            )

            if indice < cantidad_servicios:
                self.insertar_linea()

        self.insertar_linea()

        if ruta.get("transbordos"):
            self.insertar_linea(
                "🔄 TRANSBORDOS",
                "seccion",
            )

            self.insertar_linea(
                "En estos puntos debes cambiar de un "
                "servicio a otro:"
            )

            self.insertar_linea()

            for indice, transbordo in enumerate(
                ruta["transbordos"],
                start=1,
            ):
                estacion = transbordo["estacion"]
                desde = transbordo["desde_servicio"]
                hacia = transbordo["hacia_servicio"]

                self.insertar_linea(
                    f"🔄 Transbordo {indice}",
                    "transbordo",
                )

                self.insertar_linea(
                    f"   🚉 Estación: {estacion['nombre']}"
                )

                self.insertar_linea(
                    f"   🔴 Servicio {desde}"
                )

                self.insertar_linea(
                    f"          ↓"
                )

                self.insertar_linea(
                    f"   🟠 CAMBIO DE SERVICIO"
                )

                self.insertar_linea(
                    f"          ↓"
                )

                self.insertar_linea(
                    f"   🔴 Servicio {hacia}"
                )

                self.insertar_linea()

        else:
            self.insertar_linea(
                "✅ No se necesitan transbordos.",
                "resumen",
            )

        self.insertar_linea()

        self.insertar_linea(
            "💡 ¿Cómo leer esta ruta?",
            "seccion",
        )

        self.insertar_linea(
            "🔴 Troncal: servicio troncal utilizado "
            "en el recorrido."
        )

        self.insertar_linea(
            "🟣 Portal: estación terminal o portal."
        )

        self.insertar_linea(
            "⚪ Estación: estación intermedia del recorrido."
        )

        self.insertar_linea(
            "🔄 Transbordo: punto donde debes cambiar "
            "de servicio."
        )

    def buscar(self):
        origen = self.entrada_origen.get().strip()
        destino = self.entrada_destino.get().strip()

        if not origen or not destino:
            messagebox.showwarning(
                "Datos incompletos",
                "Ingresa el origen y el destino.",
            )
            return

        try:
            resultado = buscar_ruta(
                origen,
                destino,
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Ocurrió un error al buscar la ruta:\n\n"
                f"{error}",
            )
            return

        if not resultado["encontrada"]:
            self.limpiar_resultado()

            self.insertar_linea(
                "❌ NO SE ENCONTRÓ UNA RUTA",
                "titulo",
            )

            self.insertar_linea()

            self.insertar_linea(
                f"📍 Origen: {origen}"
            )

            self.insertar_linea(
                f"🏁 Destino: {destino}"
            )

            self.insertar_linea()

            self.insertar_linea(
                f"Motivo: {resultado['motivo']}"
            )

            return

        self.mostrar_resultado(
            resultado,
            origen,
            destino,
        )


def main():
    root = tk.Tk()
    TransmiApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()