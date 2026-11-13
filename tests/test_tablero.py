
import unittest
from datetime import date
from unittest.mock import patch

from src.tablero import (
    generar_tarjetas_puntuacion,
    agrupar_publicaciones_por_fecha,
    generar_vista_dos_semanas,
)


class PruebasTablero(unittest.TestCase):

    def setUp(self):
        self.ventana_prueba = {
            "variante": "prueba",
            "inicio": date(2026, 11, 30),
            "fin": date(2026, 12, 1),
        }

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

    @patch("src.tablero.cargar_ventana")
    def test_05_puntuacion_especifica_por_formato_y_tema(
        self,
        mock_ventana
    ):
        mock_ventana.return_value = self.ventana_prueba

        calendario = [
            {
                "fecha": "2026-11-30",
                "hora": "08:30",
                "formato": "post_linkedin",
                "tema": "rpa",
                "titulo": "Publicación RPA"
            }
        ]

        puntuaciones_calendario = {
            "post_linkedin|rpa": {
                "puntuacion": 61.87,
                "fuente_puntuacion": "formato y tema"
            }
        }

        resultado = generar_vista_dos_semanas(
            calendario,
            puntuaciones_calendario=puntuaciones_calendario
        )

        self.assertIn("61.87/100", resultado)
        self.assertIn("formato y tema", resultado)

    @patch("src.tablero.cargar_ventana")
    def test_06_usar_referencia_general_del_formato(
        self,
        mock_ventana
    ):
        mock_ventana.return_value = self.ventana_prueba

        calendario = [
            {
                "fecha": "2026-11-30",
                "hora": "08:30",
                "formato": "post_linkedin",
                "tema": "automatizacion",
                "titulo": "Publicación general"
            }
        ]

        puntuaciones = {
            "post_linkedin": {
                "puntuacion": 48.81,
                "fuente_puntuacion": "solo formato"
            }
        }

        resultado = generar_vista_dos_semanas(
            calendario,
            puntuaciones=puntuaciones,
            tema_puntuacion="automatizacion"
        )

        self.assertIn("48.81/100", resultado)
        self.assertIn("solo formato", resultado)

    @patch("src.tablero.cargar_ventana")
    def test_07_no_inventar_puntuacion_sin_historial(
        self,
        mock_ventana
    ):
        mock_ventana.return_value = self.ventana_prueba

        calendario = [
            {
                "fecha": "2026-11-30",
                "hora": "08:30",
                "formato": "newsletter",
                "tema": "marca",
                "titulo": "Novedades"
            }
        ]

        puntuaciones_calendario = {
            "newsletter|marca": {
                "puntuacion": None,
                "explicacion": "No existe historial para este formato."
            }
        }

        resultado = generar_vista_dos_semanas(
            calendario,
            puntuaciones_calendario=puntuaciones_calendario
        )

        self.assertIn(
            "Sin datos históricos suficientes para este formato",
            resultado
        )
        self.assertIn(
            "No existe historial para este formato.",
            resultado
        )

    @patch("src.tablero.cargar_ventana")
    def test_08_cada_publicacion_usa_su_puntuacion(
        self,
        mock_ventana
    ):
        mock_ventana.return_value = self.ventana_prueba

        calendario = [
            {
                "fecha": "2026-11-30",
                "hora": "08:30",
                "formato": "post_linkedin",
                "tema": "rpa",
                "titulo": "Publicación RPA"
            },
            {
                "fecha": "2026-12-01",
                "hora": "08:30",
                "formato": "carrusel_linkedin",
                "tema": "docfly",
                "titulo": "Publicación Docfly"
            }
        ]

        puntuaciones_calendario = {
            "post_linkedin|rpa": {
                "puntuacion": 61.87,
                "fuente_puntuacion": "formato y tema"
            },
            "carrusel_linkedin|docfly": {
                "puntuacion": 90.38,
                "fuente_puntuacion": "formato y tema"
            }
        }

        resultado = generar_vista_dos_semanas(
            calendario,
            puntuaciones_calendario=puntuaciones_calendario
        )

        self.assertIn("61.87/100", resultado)
        self.assertIn("90.38/100", resultado)

        self.assertLess(
            resultado.index("61.87/100"),
            resultado.index("90.38/100")
        )


if __name__ == "__main__":
    unittest.main()
