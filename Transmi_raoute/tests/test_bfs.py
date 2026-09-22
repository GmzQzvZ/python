import unittest

from src.algorithms.bfs import buscar_ruta_bfs, construir_grafo


def datos_de_prueba():
    return {
        "rutas": {
            "T1": {
                "direcciones": [
                    {
                        "origen": "A",
                        "destino": "D",
                        "estado": "construida",
                        "variante": None,
                        "estaciones_orientadas": [
                            {"id": 1, "nombre": "A"},
                            {"id": 2, "nombre": "B"},
                            {"id": 3, "nombre": "C"},
                            {"id": 4, "nombre": "D"},
                        ],
                    }
                ]
            },
            "T2": {
                "direcciones": [
                    {
                        "origen": "E",
                        "destino": "F",
                        "estado": "construida",
                        "variante": "expresa",
                        "estaciones_orientadas": [
                            {"id": 2, "nombre": "B"},
                            {"id": 5, "nombre": "E"},
                            {"id": 6, "nombre": "F"},
                        ],
                    }
                ]
            },
            "T3": {
                "direcciones": [
                    {
                        "origen": "F",
                        "destino": "H",
                        "estado": "construida",
                        "variante": None,
                        "estaciones_orientadas": [
                            {"id": 6, "nombre": "F"},
                            {"id": 7, "nombre": "G"},
                            {"id": 8, "nombre": "H"},
                        ],
                    }
                ]
            },
        }
    }


class TestBfs(unittest.TestCase):
    def test_construir_grafo_crea_aristas_dirigidas_consecutivas(self):
        grafo = construir_grafo(datos_de_prueba())

        destinos_desde_a = [arista["destino"] for arista in grafo.adyacencias[1]]
        destinos_desde_b = [arista["destino"] for arista in grafo.adyacencias[2]]

        self.assertEqual(destinos_desde_a, [2])
        self.assertIn(3, destinos_desde_b)
        self.assertNotIn(1, destinos_desde_b)

    def test_buscar_ruta_bfs_encuentra_camino_por_nombre(self):
        grafo = construir_grafo(datos_de_prueba())

        resultado = buscar_ruta_bfs(grafo, "A", "D")

        self.assertTrue(resultado["encontrada"])
        self.assertEqual(
            [estacion["nombre"] for estacion in resultado["estaciones"]],
            ["A", "B", "C", "D"],
        )
        self.assertEqual(
            [tramo["servicio"] for tramo in resultado["tramos"]],
            ["T1", "T1", "T1"],
        )
        self.assertEqual(resultado["transbordos"], [])
        self.assertEqual(resultado["cantidad_transbordos"], 0)
        self.assertEqual(resultado["tramos"][0]["origen"], 1)
        self.assertEqual(resultado["tramos"][0]["destino"], 2)
        self.assertEqual(resultado["tramos"][0]["origen_servicio"], "A")
        self.assertEqual(resultado["tramos"][0]["destino_servicio"], "D")

    def test_buscar_ruta_bfs_respeta_direccion(self):
        grafo = construir_grafo(datos_de_prueba())

        resultado = buscar_ruta_bfs(grafo, "D", "A")

        self.assertFalse(resultado["encontrada"])
        self.assertEqual(resultado["motivo"], "sin_ruta")

    def test_buscar_ruta_bfs_reporta_origen_inexistente(self):
        grafo = construir_grafo(datos_de_prueba())

        resultado = buscar_ruta_bfs(grafo, "Z", "A")

        self.assertFalse(resultado["encontrada"])
        self.assertEqual(resultado["motivo"], "origen_no_existe")

    def test_buscar_ruta_bfs_reporta_destino_inexistente(self):
        grafo = construir_grafo(datos_de_prueba())

        resultado = buscar_ruta_bfs(grafo, "A", "Z")

        self.assertFalse(resultado["encontrada"])
        self.assertEqual(resultado["motivo"], "destino_no_existe")

    def test_buscar_ruta_bfs_origen_igual_destino(self):
        grafo = construir_grafo(datos_de_prueba())

        resultado = buscar_ruta_bfs(grafo, "A", "A")

        self.assertTrue(resultado["encontrada"])
        self.assertEqual([estacion["id"] for estacion in resultado["estaciones"]], [1])
        self.assertEqual(resultado["tramos"], [])
        self.assertEqual(resultado["transbordos"], [])
        self.assertEqual(resultado["cantidad_estaciones"], 1)
        self.assertEqual(resultado["cantidad_transbordos"], 0)

    def test_estacion_compartida_conserva_multiples_servicios(self):
        grafo = construir_grafo(datos_de_prueba())

        self.assertEqual(grafo.servicios_por_estacion[2], {"T1", "T2"})
        self.assertEqual(grafo.servicios_por_estacion[6], {"T2", "T3"})

    def test_buscar_ruta_bfs_identifica_un_transbordo(self):
        grafo = construir_grafo(datos_de_prueba())

        resultado = buscar_ruta_bfs(grafo, "A", "F")

        self.assertTrue(resultado["encontrada"])
        self.assertEqual(
            [estacion["nombre"] for estacion in resultado["estaciones"]],
            ["A", "B", "E", "F"],
        )
        self.assertEqual(
            [tramo["servicio"] for tramo in resultado["tramos"]],
            ["T1", "T2", "T2"],
        )
        self.assertEqual(resultado["cantidad_transbordos"], 1)
        self.assertEqual(resultado["transbordos"][0]["estacion"]["nombre"], "B")
        self.assertEqual(resultado["transbordos"][0]["desde_servicio"], "T1")
        self.assertEqual(resultado["transbordos"][0]["hacia_servicio"], "T2")
        self.assertEqual(resultado["transbordos"][0]["indice_estacion"], 1)

    def test_buscar_ruta_bfs_identifica_mas_de_un_transbordo(self):
        grafo = construir_grafo(datos_de_prueba())

        resultado = buscar_ruta_bfs(grafo, "A", "H")

        self.assertTrue(resultado["encontrada"])
        self.assertEqual(
            [estacion["nombre"] for estacion in resultado["estaciones"]],
            ["A", "B", "E", "F", "G", "H"],
        )
        self.assertEqual(
            [tramo["servicio"] for tramo in resultado["tramos"]],
            ["T1", "T2", "T2", "T3", "T3"],
        )
        self.assertEqual(resultado["cantidad_transbordos"], 2)
        self.assertEqual(
            [
                (
                    transbordo["estacion"]["nombre"],
                    transbordo["desde_servicio"],
                    transbordo["hacia_servicio"],
                )
                for transbordo in resultado["transbordos"]
            ],
            [("B", "T1", "T2"), ("F", "T2", "T3")],
        )

    def test_metadatos_de_tramo_se_preservan_en_ruta_con_transbordo(self):
        grafo = construir_grafo(datos_de_prueba())

        resultado = buscar_ruta_bfs(grafo, "A", "F")

        tramo_t2 = resultado["tramos"][1]
        self.assertEqual(tramo_t2["origen"], 2)
        self.assertEqual(tramo_t2["destino"], 5)
        self.assertEqual(tramo_t2["servicio"], "T2")
        self.assertEqual(tramo_t2["origen_servicio"], "E")
        self.assertEqual(tramo_t2["destino_servicio"], "F")
        self.assertEqual(tramo_t2["variante"], "expresa")

    def test_nombre_ambiguo_no_se_resuelve_arbitrariamente(self):
        datos = {
            "rutas": {
                "T1": {
                    "direcciones": [
                        {
                            "origen": "Uno",
                            "destino": "Dos",
                            "estado": "construida",
                            "variante": None,
                            "estaciones_orientadas": [
                                {"id": 1, "nombre": "Central"},
                                {"id": 2, "nombre": "Final"},
                            ],
                        }
                    ]
                },
                "T2": {
                    "direcciones": [
                        {
                            "origen": "Tres",
                            "destino": "Cuatro",
                            "estado": "construida",
                            "variante": None,
                            "estaciones_orientadas": [
                                {"id": 3, "nombre": "CENTRAL"},
                                {"id": 4, "nombre": "Otra"},
                            ],
                        }
                    ]
                },
            }
        }
        grafo = construir_grafo(datos)

        resultado = buscar_ruta_bfs(grafo, "central", "Final")

        self.assertFalse(resultado["encontrada"])
        self.assertEqual(resultado["motivo"], "origen_ambiguo")


if __name__ == "__main__":
    unittest.main()
