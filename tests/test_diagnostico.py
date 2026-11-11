import unittest

from src.diagnostico import diagnosticar_contenido


class PruebasDiagnostico(unittest.TestCase):

    def test_diagnostico_rechaza_contenido_vacio(self):
        with self.assertRaises(ValueError):
            diagnosticar_contenido("")

    def test_diagnostico_genera_indicadores(self):
        texto = (
            "La automatización mejora los procesos. "
            "Permite analizar tareas y medir resultados. "
            "También ayuda a identificar oportunidades."
        )

        resultado = diagnosticar_contenido(texto)

        self.assertIn("indicadores", resultado)
        self.assertIn("temas", resultado)
        self.assertIn("alertas", resultado)

    def test_diagnostico_cuenta_palabras(self):
        texto = "Automatización de procesos empresariales."

        resultado = diagnosticar_contenido(texto)

        self.assertEqual(
            resultado["indicadores"]["palabras"],
            4
        )

    def test_diagnostico_identifica_cifras(self):
        texto = (
            "La empresa ahorra 20 horas de trabajo "
            "y mejora sus procesos."
        )

        resultado = diagnosticar_contenido(texto)

        self.assertGreater(
            resultado["indicadores"]["cifras_identificadas"],
            0
        )

    def test_diagnostico_detecta_tema_automatizacion(self):
        texto = (
            "La automatización permite mejorar "
            "los procesos de una empresa."
        )

        resultado = diagnosticar_contenido(texto)

        temas_detectados = [
            tema["tema"]
            for tema in resultado["temas"]
        ]

        self.assertIn("automatizacion", temas_detectados)


if __name__ == "__main__":
    unittest.main()