import unittest

from src.puntuacion import (
    normalizar_puntuacion,
    calcular_puntuacion_final,
    calcular_puntuaciones_metricas,
    comparar_rendimiento,
    clasificar_evidencia,
)


class PruebasPuntuacion(unittest.TestCase):

    def test_normalizar_puntuacion(self):
        resultado = normalizar_puntuacion(500, 1000)
        self.assertEqual(resultado, 50.0)

    def test_normalizar_puntuacion_maxima(self):
        resultado = normalizar_puntuacion(1500, 1000)
        self.assertEqual(resultado, 100)

    def test_normalizar_puntuacion_sin_datos(self):
        resultado = normalizar_puntuacion(None, 1000)
        self.assertIsNone(resultado)

    def test_calcular_puntuacion_final(self):
        puntuaciones = {
            "impresiones": 80,
            "reacciones": 70,
            "clics": 90,
        }

        resultado = calcular_puntuacion_final(puntuaciones)

        self.assertEqual(resultado, 80.0)

    def test_calcular_puntuacion_final_sin_metrica(self):
        puntuaciones = {
            "impresiones": 80,
            "reacciones": None,
            "clics": 90,
        }

        resultado = calcular_puntuacion_final(puntuaciones)

        self.assertIsNone(resultado)

    def test_puntuacion_solo_con_historial_formato(self):
        datos = {
            "formato": {
                "impresiones": 50,
                "reacciones": 40,
                "clics": 30,
            },
            "tema": None,
        }

        referencias = {
            "formatos": {
                "impresiones": 100,
                "reacciones": 100,
                "clics": 100,
            },
            "temas": {
                "impresiones": None,
                "reacciones": None,
                "clics": None,
            },
        }

        resultado = calcular_puntuaciones_metricas(
            datos,
            referencias,
        )

        self.assertEqual(resultado["impresiones"], 50.0)
        self.assertEqual(resultado["reacciones"], 40.0)
        self.assertEqual(resultado["clics"], 30.0)

    def test_comparacion_sin_historial_tema(self):
        medianas = {
            "formatos": {
                "post_linkedin": {
                    "impresiones": 100,
                    "reacciones": 20,
                    "clics": 10,
                }
            },
            "temas": {},
        }

        resultado, mensaje = comparar_rendimiento(
            medianas,
            "post_linkedin",
            "automatizacion",
        )

        self.assertIsNotNone(resultado)
        self.assertIsNone(resultado["tema"])
        self.assertIn("únicamente", mensaje)

    def test_evidencia_solo_formato(self):
        resultado = clasificar_evidencia(10)

        self.assertEqual(resultado, "moderada")


if __name__ == "__main__":
    unittest.main()