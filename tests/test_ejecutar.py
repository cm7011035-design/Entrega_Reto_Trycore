
import unittest
from unittest.mock import MagicMock, patch

from ejecutar import (
    preparar_publicaciones,
    cargar_pieza_madre
)


class PruebasPrepararPublicaciones(unittest.TestCase):

    def setUp(self):
        self.formatos = {
            "post": {
                "gancho": "Una nueva forma de mejorar procesos"
            },
            "carrusel": [
                {
                    "titulo": "Portada del carrusel"
                }
            ],
            "validacion_post": {
                "valido": True,
                "resultados": []
            },
            "validacion_carrusel": {
                "valido": True,
                "resultados": []
            }
        }

    def test_01_programar_dos_formatos_validos(self):
        resultado = preparar_publicaciones(
            self.formatos,
            "rpa"
        )

        self.assertEqual(len(resultado["publicaciones_validas"]), 2)
        self.assertEqual(len(resultado["publicaciones_rechazadas"]), 0)

    def test_02_rechazar_post_no_valido(self):
        self.formatos["validacion_post"] = {
            "valido": False,
            "resultados": [
                {
                    "valido": False,
                    "mensaje": "El post supera el límite de caracteres."
                }
            ]
        }

        resultado = preparar_publicaciones(self.formatos, "rpa")

        self.assertEqual(len(resultado["publicaciones_validas"]), 1)
        self.assertEqual(
            resultado["publicaciones_validas"][0]["formato"],
            "carrusel_linkedin"
        )
        self.assertEqual(len(resultado["publicaciones_rechazadas"]), 1)
        self.assertEqual(
            resultado["publicaciones_rechazadas"][0]["formato"],
            "post_linkedin"
        )

    def test_03_rechazar_carrusel_no_valido(self):
        self.formatos["validacion_carrusel"] = {
            "valido": False,
            "resultados": [
                {
                    "valido": False,
                    "mensaje": "El carrusel no cumple el número de láminas."
                }
            ]
        }

        resultado = preparar_publicaciones(self.formatos, "rpa")

        self.assertEqual(len(resultado["publicaciones_validas"]), 1)
        self.assertEqual(
            resultado["publicaciones_validas"][0]["formato"],
            "post_linkedin"
        )
        self.assertEqual(len(resultado["publicaciones_rechazadas"]), 1)
        self.assertEqual(
            resultado["publicaciones_rechazadas"][0]["formato"],
            "carrusel_linkedin"
        )


class PruebasRespaldoFuente(unittest.TestCase):

    def setUp(self):
        self.html = """
        <html>
            <body>
                <h1>Guía de prueba de automatización</h1>
                <h2>Introducción</h2>
                <p>Este contenido permite comprobar la lectura de una fuente
                HTML y verificar que el sistema puede recuperar información
                cuando ocurre un problema con la conexión a Internet.</p>
            </body>
        </html>
        """

        self.ruta_url = MagicMock()
        self.ruta_url.read_text.return_value = "https://ejemplo.com"

        self.ruta_respaldo = MagicMock()
        self.ruta_respaldo.exists.return_value = True
        self.ruta_respaldo.read_text.return_value = self.html

    def ejecutar_con_rutas_simuladas(self, error_url=False, respaldo=True):

        self.ruta_respaldo.exists.return_value = respaldo

        if error_url:
            respuesta_url = patch(
                "ejecutar.leer_html_url",
                side_effect=RuntimeError("Fallo de conexión")
            )
        else:
            respuesta_url = patch(
                "ejecutar.leer_html_url",
                return_value=self.html
            )

        with patch(
            "ejecutar.Path",
            side_effect=[self.ruta_url, self.ruta_respaldo]
        ):
            with respuesta_url:
                return cargar_pieza_madre()

    def test_04_utilizar_respaldo_si_falla_url(self):

        resultado = self.ejecutar_con_rutas_simuladas(
            error_url=True
        )

        self.assertEqual(
            resultado["fuente_utilizada"],
            "respaldo"
        )

        self.assertEqual(
            resultado["titulo"],
            "Guía de prueba de automatización"
        )

        self.assertTrue(resultado["texto"])

    def test_05_utilizar_url_si_funciona(self):

        resultado = self.ejecutar_con_rutas_simuladas()

        self.assertEqual(
            resultado["fuente_utilizada"],
            "url"
        )

        self.assertEqual(
            resultado["titulo"],
            "Guía de prueba de automatización"
        )

    def test_06_informar_error_si_no_existe_respaldo(self):

        with self.assertRaises(FileNotFoundError):

            self.ejecutar_con_rutas_simuladas(
                error_url=True,
                respaldo=False
            )


if __name__ == "__main__":
    unittest.main()
