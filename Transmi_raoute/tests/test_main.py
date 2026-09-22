import importlib
import unittest


class TestMain(unittest.TestCase):
    def test_main_puede_importarse_sin_ejecutar_interfaz(self):
        modulo = importlib.import_module("main")

        self.assertTrue(callable(modulo.main))
        self.assertTrue(callable(modulo.mostrar_resultado))


if __name__ == "__main__":
    unittest.main()
