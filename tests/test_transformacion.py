
import unittest

from src.transformacion import (
    generar_gancho_post,
    generar_desarrollo_post,
    generar_llamado_accion
)


class PruebasTransformacion(unittest.TestCase):

    def setUp(self):
        self.seccion = {
            "titulo": "Mejores prácticas de implementación de RPA",
            "parrafos": [
                "La automatización permite optimizar procesos empresariales.",
                "Es importante evaluar el impacto comercial antes de automatizar."
            ],
            "listas": [
                "Combina RPA atendido y desatendido.",
                "Define y enfócate en el ROI deseado.",
                "Céntrate en procesos correctos y viables para automatizar."
            ]
        }

    def test_01_generar_gancho_relacionado_con_titulo(self):
        resultado = generar_gancho_post(self.seccion)

        self.assertIn("RPA", resultado.upper())
        self.assertTrue(resultado.startswith("¿"))

    def test_02_generar_desarrollo_con_parrafos(self):
        resultado = generar_desarrollo_post(self.seccion)

        self.assertIn(
            "La automatización permite optimizar procesos empresariales.",
            resultado
        )

    def test_03_generar_desarrollo_con_recomendaciones(self):
        resultado = generar_desarrollo_post(self.seccion)

        self.assertIn("Recomendaciones clave:", resultado)
        self.assertIn("Combina RPA atendido y desatendido.", resultado)

    def test_04_limitar_numero_de_recomendaciones(self):
        resultado = generar_desarrollo_post(
            self.seccion,
            max_recomendaciones=2
        )

        self.assertIn("Combina RPA atendido y desatendido.", resultado)
        self.assertIn("Define y enfócate en el ROI deseado.", resultado)
        self.assertNotIn(
            "Céntrate en procesos correctos y viables para automatizar.",
            resultado
        )

    def test_05_generar_llamado_accion(self):
        resultado = generar_llamado_accion(
            self.seccion["titulo"]
        )

        self.assertIn("RPA", resultado.upper())
        self.assertIn("Consulta el contenido completo", resultado)

    def test_06_rechazar_seccion_vacia_en_gancho(self):
        with self.assertRaises(ValueError):
            generar_gancho_post(None)

    def test_07_rechazar_seccion_sin_titulo(self):
        with self.assertRaises(ValueError):
            generar_gancho_post({"titulo": ""})

    def test_08_rechazar_desarrollo_sin_contenido(self):
        with self.assertRaises(ValueError):
            generar_desarrollo_post({
                "titulo": "Prueba",
                "parrafos": [],
                "listas": []
            })

    def test_09_rechazar_llamado_sin_titulo(self):
        with self.assertRaises(ValueError):
            generar_llamado_accion("")


if __name__ == "__main__":
    unittest.main()
