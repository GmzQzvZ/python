import unittest

from src.algorithms.bfs import construir_grafo
from src.knowledge.base_conocimiento import cargar_rutas_orientadas
from src.routing.evaluador import buscar_ruta


def datos_integracion():
    return {
        "rutas": {
            "T1": {
                "direcciones": [
                    {
                        "origen": "A",
                        "destino": "C",
                        "estado": "construida",
                        "variante": None,
                        "estaciones_orientadas": [
                            {"id": 1, "nombre": "A"},
                            {"id": 2, "nombre": "B"},
                            {"id": 3, "nombre": "C"},
                        ],
                    }
                ]
            },
            "T2": {
                "direcciones": [
                    {
                        "origen": "B",
                        "destino": "E",
                        "estado": "construida",
                        "variante": "expresa",
                        "estaciones_orientadas": [
                            {"id": 2, "nombre": "B"},
                            {"id": 4, "nombre": "D"},
                            {"id": 5, "nombre": "E"},
                        ],
                    }
                ]
            },
            "AISLADA": {
                "direcciones": [
                    {
                        "origen": "X",
                        "destino": "Y",
                        "estado": "construida",
                        "variante": None,
                        "estaciones_orientadas": [
                            {"id": 6, "nombre": "X"},
                            {"id": 7, "nombre": "Y"},
                        ],
                    }
                ]
            },
        }
    }


def datos_con_nombre_ambiguo():
    datos = datos_integracion()
    datos["rutas"]["AMBIGUA"] = {
        "direcciones": [
            {
                "origen": "Otra Central",
                "destino": "Final",
                "estado": "construida",
                "variante": None,
                "estaciones_orientadas": [
                    {"id": 8, "nombre": "A"},
                    {"id": 9, "nombre": "Z"},
                ],
            }
        ]
    }
    return datos


class TestIntegracionBusqueda(unittest.TestCase):
    def test_buscar_ruta_flujo_completo_encontrada(self):
        resultado = buscar_ruta("A", "E", ruta_datos=datos_integracion())

        self.assertTrue(resultado["encontrada"])
        self.assertIsNone(resultado["motivo"])
        self.assertEqual(resultado["seleccion"]["estado"], "seleccionada")
        self.assertEqual(resultado["seleccion"]["seleccionada"]["indice"], 0)
        self.assertEqual(
            resultado["evaluacion"]["metricas"]["servicios_utilizados"],
            ["T1", "T2"],
        )
        self.assertEqual(resultado["evaluacion"]["metricas"]["cantidad_transbordos"], 1)
        self.assertEqual(
            [estacion["nombre"] for estacion in resultado["ruta"]["estaciones"]],
            ["A", "B", "D", "E"],
        )

    def test_buscar_ruta_origen_igual_destino(self):
        resultado = buscar_ruta("A", "A", ruta_datos=datos_integracion())

        self.assertTrue(resultado["encontrada"])
        self.assertIsNone(resultado["motivo"])
        self.assertEqual(resultado["evaluacion"]["metricas"]["cantidad_estaciones"], 1)
        self.assertEqual(resultado["evaluacion"]["metricas"]["cantidad_tramos"], 0)
        self.assertEqual(resultado["evaluacion"]["metricas"]["cantidad_transbordos"], 0)

    def test_buscar_ruta_origen_no_existe(self):
        resultado = buscar_ruta("NO_EXISTE", "A", ruta_datos=datos_integracion())

        self.assertFalse(resultado["encontrada"])
        self.assertEqual(resultado["motivo"], "origen_no_existe")
        self.assertEqual(resultado["seleccion"]["estado"], "sin_rutas_encontradas")

    def test_buscar_ruta_destino_no_existe(self):
        resultado = buscar_ruta("A", "NO_EXISTE", ruta_datos=datos_integracion())

        self.assertFalse(resultado["encontrada"])
        self.assertEqual(resultado["motivo"], "destino_no_existe")
        self.assertEqual(resultado["seleccion"]["estado"], "sin_rutas_encontradas")

    def test_buscar_ruta_origen_ambiguo(self):
        resultado = buscar_ruta("A", "E", ruta_datos=datos_con_nombre_ambiguo())

        self.assertFalse(resultado["encontrada"])
        self.assertEqual(resultado["motivo"], "origen_ambiguo")
        self.assertEqual(resultado["seleccion"]["estado"], "sin_rutas_encontradas")

    def test_buscar_ruta_destino_ambiguo(self):
        resultado = buscar_ruta("B", "A", ruta_datos=datos_con_nombre_ambiguo())

        self.assertFalse(resultado["encontrada"])
        self.assertEqual(resultado["motivo"], "destino_ambiguo")
        self.assertEqual(resultado["seleccion"]["estado"], "sin_rutas_encontradas")

    def test_buscar_ruta_sin_camino(self):
        resultado = buscar_ruta("C", "X", ruta_datos=datos_integracion())

        self.assertFalse(resultado["encontrada"])
        self.assertEqual(resultado["motivo"], "sin_ruta")
        self.assertEqual(resultado["seleccion"]["estado"], "sin_rutas_encontradas")

    def test_buscar_ruta_reutiliza_grafo(self):
        grafo = construir_grafo(datos_integracion())

        resultado = buscar_ruta("A", "C", grafo=grafo)

        self.assertTrue(resultado["encontrada"])
        self.assertEqual(resultado["grafo"]["cantidad_estaciones"], 7)
        self.assertEqual(resultado["grafo"]["cantidad_aristas"], 5)

    def test_grafo_real_conserva_conteos_esperados(self):
        resultado = buscar_ruta(116, 103)

        self.assertEqual(resultado["grafo"]["cantidad_estaciones"], 134)
        self.assertEqual(resultado["grafo"]["cantidad_aristas"], 919)

        datos = cargar_rutas_orientadas()
        grafo = construir_grafo(datos)
        self.assertEqual(len(grafo.estaciones), 134)
        self.assertEqual(sum(len(aristas) for aristas in grafo.adyacencias.values()), 919)


if __name__ == "__main__":
    unittest.main()
