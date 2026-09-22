import unittest

from src.knowledge.reglas import seleccionar_ruta


def ruta(ids_estaciones, servicios, transbordos=None):
    estaciones = [
        {"id": estacion_id, "nombre": f"E{estacion_id}"}
        for estacion_id in ids_estaciones
    ]
    tramos = [
        {
            "origen": ids_estaciones[indice],
            "destino": ids_estaciones[indice + 1],
            "servicio": servicio,
            "origen_servicio": f"O{servicio}",
            "destino_servicio": f"D{servicio}",
            "variante": None,
        }
        for indice, servicio in enumerate(servicios)
    ]

    return {
        "encontrada": True,
        "estaciones": estaciones,
        "tramos": tramos,
        "transbordos": transbordos or [],
        "cantidad_estaciones": len(estaciones),
        "cantidad_transbordos": len(transbordos or []),
    }


def transbordo(estacion_id, desde, hacia, indice_estacion):
    return {
        "estacion": {"id": estacion_id, "nombre": f"E{estacion_id}"},
        "desde_servicio": desde,
        "hacia_servicio": hacia,
        "indice_estacion": indice_estacion,
    }


class TestReglasSeleccion(unittest.TestCase):
    def test_selecciona_menor_cantidad_de_transbordos(self):
        con_transbordo = ruta(
            [1, 2, 3],
            ["A", "B"],
            [transbordo(2, "A", "B", 1)],
        )
        sin_transbordo = ruta([1, 4, 5, 6], ["C", "C", "C"])

        resultado = seleccionar_ruta([con_transbordo, sin_transbordo])

        self.assertEqual(resultado["seleccionada"]["indice"], 1)
        self.assertFalse(resultado["empate"])

    def test_desempata_por_menor_cantidad_de_estaciones(self):
        larga = ruta([1, 2, 3, 4], ["A", "A", "A"])
        corta = ruta([1, 5, 4], ["B", "B"])

        resultado = seleccionar_ruta([larga, corta])

        self.assertEqual(resultado["seleccionada"]["indice"], 1)
        self.assertEqual(
            resultado["explicacion"]["valores_por_ruta"][1]["valores"][
                "cantidad_estaciones"
            ],
            3,
        )

    def test_desempata_por_menor_cantidad_de_servicios(self):
        dos_servicios_sin_transbordo = ruta([1, 2, 3], ["A", "B"])
        un_servicio = ruta([1, 4, 3], ["C", "C"])

        resultado = seleccionar_ruta([dos_servicios_sin_transbordo, un_servicio])

        self.assertEqual(resultado["seleccionada"]["indice"], 1)

    def test_empate_completo_conserva_orden_original(self):
        primera = ruta([1, 2, 3], ["A", "A"])
        segunda = ruta([4, 5, 6], ["B", "B"])

        resultado = seleccionar_ruta([primera, segunda])

        self.assertEqual(resultado["seleccionada"]["indice"], 0)
        self.assertTrue(resultado["empate"])
        self.assertEqual(resultado["indices_empatados"], [0, 1])

    def test_lista_vacia(self):
        resultado = seleccionar_ruta([])

        self.assertIsNone(resultado["seleccionada"])
        self.assertEqual(resultado["estado"], "lista_vacia")

    def test_ninguna_ruta_encontrada(self):
        resultado = seleccionar_ruta(
            [
                {"encontrada": False, "motivo": "sin_ruta"},
                {"encontrada": False, "motivo": "origen_no_existe"},
            ]
        )

        self.assertIsNone(resultado["seleccionada"])
        self.assertEqual(resultado["estado"], "sin_rutas_encontradas")

    def test_rutas_invalidas(self):
        resultado = seleccionar_ruta(
            [
                {"encontrada": True, "estaciones": [], "tramos": []},
                "no es ruta",
            ]
        )

        self.assertIsNone(resultado["seleccionada"])
        self.assertEqual(resultado["estado"], "sin_rutas_validas")
        self.assertEqual(
            [error["motivo"] for error in resultado["errores"]],
            ["falta_transbordos", "ruta_no_es_diccionario"],
        )

    def test_cambiar_orden_de_criterios_cambia_decision(self):
        menos_transbordos_mas_estaciones = ruta([1, 2, 3, 4], ["A", "A", "A"])
        mas_transbordos_menos_estaciones = ruta(
            [1, 5, 4],
            ["B", "C"],
            [transbordo(5, "B", "C", 1)],
        )

        politica_inicial = seleccionar_ruta(
            [menos_transbordos_mas_estaciones, mas_transbordos_menos_estaciones]
        )
        politica_por_estaciones = seleccionar_ruta(
            [menos_transbordos_mas_estaciones, mas_transbordos_menos_estaciones],
            criterios=("cantidad_estaciones", "cantidad_transbordos"),
        )

        self.assertEqual(politica_inicial["seleccionada"]["indice"], 0)
        self.assertEqual(politica_por_estaciones["seleccionada"]["indice"], 1)
        self.assertEqual(
            politica_por_estaciones["criterios_utilizados"],
            ["cantidad_estaciones", "cantidad_transbordos"],
        )


if __name__ == "__main__":
    unittest.main()
