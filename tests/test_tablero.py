import unittest

from src.tablero import (
    generar_tarjetas_puntuacion,
    agrupar_publicaciones_por_fecha
)


class PruebasTablero(unittest.TestCase):

    def test_01_generar_tarjetas_con_puntuaciones(self):
        resumen = {
            "puntuaciones": {
                "post_linkedin": {
                    "puntuacion": 61.87,
                    "nivel_evidencia": "moderada"
                },
                "carrusel_linkedin": {
                    "puntuacion": 87.46,
                    "nivel_evidencia": "moderada"
                }
            }
        }

        resultado = generar_tarjetas_puntuacion(resumen)

        self.assertIn("61.87", resultado)
        self.assertIn("87.46", resultado)

    def test_02_mostrar_sin_datos_historicos(self):
        resumen = {
            "puntuaciones": {
                "post_linkedin": None,
                "carrusel_linkedin": None
            }
        }

        resultado = generar_tarjetas_puntuacion(resumen)

        self.assertIn("Sin datos", resultado)
        self.assertIn("Sin evidencia histórica", resultado)

    def test_03_generar_tablero_html(self):
        from src.tablero import generar_tablero

        resultado = generar_tablero()

        self.assertIn(
            "Tablero de automatización de mercadeo",
            resultado
        )

        self.assertIn("<table>", resultado)
        self.assertIn("</html>", resultado)

    def test_04_agrupar_publicaciones_por_fecha(self):
        calendario = [
            {"fecha": "2026-12-03", "titulo": "Post"},
            {"fecha": "2026-12-01", "titulo": "Carrusel"},
            {"fecha": "2026-12-03", "titulo": "Newsletter"}
        ]

        resultado = agrupar_publicaciones_por_fecha(calendario)

        self.assertEqual(len(resultado), 2)
        self.assertEqual(len(resultado["2026-12-03"]), 2)
        self.assertEqual(
            list(resultado.keys()),
            ["2026-12-01", "2026-12-03"]
        )


if __name__ == "__main__":
    unittest.main()