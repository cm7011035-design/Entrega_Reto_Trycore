
import unittest

from src.puntuacion import (
    normalizar_puntuacion,
    calcular_puntuacion_final,
    calificar_publicacion,
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
