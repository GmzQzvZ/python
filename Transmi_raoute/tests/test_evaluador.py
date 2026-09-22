import unittest

from src.algorithms.bfs import buscar_ruta_bfs, construir_grafo
from src.routing.evaluador import comparar_rutas, evaluar_ruta
from tests.test_bfs import datos_de_prueba


class TestEvaluador(unittest.TestCase):
    def setUp(self):
        self.grafo = construir_grafo(datos_de_prueba())

    def test_evaluar_ruta_sin_transbordos(self):
        ruta = buscar_ruta_bfs(self.grafo, "A", "D")

        evaluacion = evaluar_ruta(ruta)
        metricas = evaluacion["metricas"]

        self.assertTrue(evaluacion["encontrada"])
        self.assertEqual(metricas["cantidad_estaciones"], 4)
        self.assertEqual(metricas["cantidad_tramos"], 3)
        self.assertEqual(metricas["cantidad_transbordos"], 0)
        self.assertEqual(metricas["servicios_utilizados"], ["T1"])
        self.assertEqual(metricas["estaciones_transbordo"], [])
        self.assertEqual(metricas["servicios_transbordo"], [])

    def test_evaluar_ruta_con_un_transbordo(self):
        ruta = buscar_ruta_bfs(self.grafo, "A", "F")

        metricas = evaluar_ruta(ruta)["metricas"]

        self.assertEqual(metricas["cantidad_estaciones"], 4)
        self.assertEqual(metricas["cantidad_tramos"], 3)
        self.assertEqual(metricas["cantidad_transbordos"], 1)
        self.assertEqual(metricas["servicios_utilizados"], ["T1", "T2"])
        self.assertEqual(
            [estacion["nombre"] for estacion in metricas["estaciones_transbordo"]],
            ["B"],
        )
        self.assertEqual(
            metricas["servicios_transbordo"],
            [{"desde_servicio": "T1", "hacia_servicio": "T2"}],
        )

    def test_evaluar_ruta_con_varios_transbordos(self):
        ruta = buscar_ruta_bfs(self.grafo, "A", "H")

        metricas = evaluar_ruta(ruta)["metricas"]

        self.assertEqual(metricas["cantidad_estaciones"], 6)
        self.assertEqual(metricas["cantidad_tramos"], 5)
        self.assertEqual(metricas["cantidad_transbordos"], 2)
        self.assertEqual(metricas["servicios_utilizados"], ["T1", "T2", "T3"])
        self.assertEqual(
            [estacion["nombre"] for estacion in metricas["estaciones_transbordo"]],
            ["B", "F"],
        )
        self.assertEqual(
            metricas["servicios_transbordo"],
            [
                {"desde_servicio": "T1", "hacia_servicio": "T2"},
                {"desde_servicio": "T2", "hacia_servicio": "T3"},
            ],
        )

    def test_comparar_rutas_muestra_metricas_sin_ranking(self):
        rutas = [
            buscar_ruta_bfs(self.grafo, "A", "D"),
            buscar_ruta_bfs(self.grafo, "A", "F"),
            buscar_ruta_bfs(self.grafo, "A", "H"),
        ]

        comparacion = comparar_rutas(rutas)

        self.assertEqual(comparacion["cantidad_rutas"], 3)
        self.assertNotIn("ganador", comparacion)
        self.assertNotIn("ranking", comparacion)
        self.assertEqual(
            [
                item["evaluacion"]["metricas"]["cantidad_transbordos"]
                for item in comparacion["evaluaciones"]
            ],
            [0, 1, 2],
        )
        self.assertEqual(
            [
                item["evaluacion"]["metricas"]["cantidad_estaciones"]
                for item in comparacion["evaluaciones"]
            ],
            [4, 4, 6],
        )


if __name__ == "__main__":
    unittest.main()
