import unittest

from src.historial import (
    normalizar_fecha,
    normalizar_numero,
    eliminar_duplicados,
    detectar_anomalias,
    detectar_valores_extremos,
    calcular_mediana,
    analizar_historial,
)


class PruebasHistorial(unittest.TestCase):

    def test_normalizar_fecha_iso(self):
        resultado = normalizar_fecha("2026-12-01")
        self.assertEqual(str(resultado), "2026-12-01")

    def test_normalizar_fecha_espanola(self):
        resultado = normalizar_fecha("01-dic-2026")
        self.assertEqual(str(resultado), "2026-12-01")

    def test_normalizar_numero_decimal_coma(self):
        resultado = normalizar_numero("0,0338")
        self.assertEqual(resultado, 0.0338)

    def test_normalizar_numero_vacio(self):
        resultado = normalizar_numero("")
        self.assertIsNone(resultado)

    def test_eliminar_duplicados(self):
        registros = [
            {"id_publicacion": "P001"},
            {"id_publicacion": "P002"},
            {"id_publicacion": "P001"},
        ]

        unicos, duplicados = eliminar_duplicados(registros)

        self.assertEqual(len(unicos), 2)
        self.assertEqual(len(duplicados), 1)

    def test_detectar_anomalias(self):
        registros = [
            {
                "id_publicacion": "P001",
                "fecha_normalizada": None,
                "impresiones": None,
                "reacciones": 10,
                "comentarios": 5,
                "clics": 2,
            }
        ]

        resultado = detectar_anomalias(registros)

        self.assertEqual(len(resultado), 1)
        self.assertGreater(len(resultado[0]["problemas"]), 0)

    def test_detectar_valor_extremo(self):
        registros = [
            {"id_publicacion": "P001", "impresiones": 100},
            {"id_publicacion": "P002", "impresiones": 120},
            {"id_publicacion": "P003", "impresiones": 110},
            {"id_publicacion": "P004", "impresiones": 2000},
        ]

        resultado = detectar_valores_extremos(registros)

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["id_publicacion"], "P004")

    def test_mediana_con_valor_extremo(self):
        resultado = calcular_mediana([10, 12, 14, 16, 1000])
        self.assertEqual(resultado, 14)

    def test_analisis_historial_completo(self):
        resultado = analizar_historial()

        self.assertEqual(resultado["total_unicos"], 60)
        self.assertEqual(resultado["total_duplicados"], 3)
        self.assertIn("medianas_temas", resultado)


if __name__ == "__main__":
    unittest.main()