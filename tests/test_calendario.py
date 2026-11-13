
import unittest

from datetime import date, time

from src.calendario import (
    cargar_ventana,
    cargar_calendario_ocupado,
    normalizar_publicaciones_ocupadas,
    cargar_reglas_calendario,
    cargar_festivos,
    es_dia_habil,
    contar_publicaciones_por_dia,
    contar_publicaciones_por_semana,
    horario_ocupado,
    tema_respetar_separacion,
    validar_horario,
    generar_horarios_disponibles,
    programar_publicaciones,
)


class PruebasCalendario(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ventana = cargar_ventana()
        cls.reglas = cargar_reglas_calendario()
        cls.festivos = cargar_festivos(cls.reglas)

        ocupadas = cargar_calendario_ocupado()
        cls.publicaciones = normalizar_publicaciones_ocupadas(ocupadas)

    def test_01_cargar_ventana(self):
        self.assertEqual(
            self.ventana["inicio"],
            date(2026, 11, 30)
        )
        self.assertEqual(
            self.ventana["fin"],
            date(2026, 12, 11)
        )

    def test_02_detectar_dia_habil(self):
        self.assertTrue(
            es_dia_habil(
                date(2026, 12, 7),
                self.reglas,
                self.festivos
            )
        )

    def test_03_detectar_festivo(self):
        self.assertFalse(
            es_dia_habil(
                date(2026, 12, 8),
                self.reglas,
                self.festivos
            )
        )

    def test_04_contar_publicaciones_diarias(self):
        cantidad = contar_publicaciones_por_dia(
            self.publicaciones,
            date(2026, 12, 1)
        )

        self.assertEqual(cantidad, 1)

    def test_05_detectar_horario_ocupado(self):
        ocupado = horario_ocupado(
            self.publicaciones,
            date(2026, 12, 1),
            time(8, 30)
        )

        self.assertTrue(ocupado)

    def test_06_respetar_separacion_por_tema(self):
        resultado = tema_respetar_separacion(
            self.publicaciones,
            date(2026, 12, 2),
            time(8, 30),
            "rpa",
            48
        )

        self.assertFalse(resultado)

    def test_07_generar_horarios_disponibles(self):
        horarios = generar_horarios_disponibles(
            self.ventana,
            self.publicaciones,
            self.reglas,
            "docfly"
        )

        self.assertGreater(len(horarios), 0)

    def test_08_identificar_publicaciones_pendientes(self):
        nuevas = [
            {
                "canal": "linkedin",
                "formato": "post_linkedin",
                "tema": "tema_" + str(i),
                "titulo": "Prueba " + str(i)
            }
            for i in range(1, 8)
        ]

        resultado = programar_publicaciones(
            nuevas,
            self.publicaciones.copy(),
            self.ventana,
            self.reglas
        )

        self.assertEqual(len(resultado["programadas"]), 4)
        self.assertEqual(len(resultado["sin_programar"]), 3)

    def test_09_respetar_limite_semanal_por_formato(self):
        nueva = [
            {
                "canal": "newsletter",
                "formato": "newsletter",
                "tema": "marca",
                "titulo": "Segundo newsletter de prueba"
            }
        ]

        ventana_prueba = {
            "inicio": date(2026, 12, 7),
            "fin": date(2026, 12, 11)
        }

        resultado = programar_publicaciones(
            nueva,
            self.publicaciones.copy(),
            ventana_prueba,
            self.reglas
        )

        self.assertEqual(
            len(resultado["programadas"]),
            0
        )

        self.assertEqual(
            len(resultado["sin_programar"]),
            1
        )

        self.assertIn(
            "límite semanal",
            resultado["sin_programar"][0]["motivo"]
        )

    def test_10_buscar_segunda_semana_si_formato_ya_alcanzo_limite(self):
        ocupadas = [
            {
                "fecha": date(2026, 11, 30),
                "hora": time(8, 30),
                "canal": "newsletter",
                "formato": "newsletter",
                "tema": "otro_tema",
                "titulo": "Newsletter ya programado",
                "estado": "programada",
            }
        ]

        nueva = [
            {
                "canal": "newsletter",
                "formato": "newsletter",
                "tema": "tema_nuevo",
                "titulo": "Newsletter de la segunda semana",
            }
        ]

        resultado = programar_publicaciones(
            nueva,
            ocupadas,
            self.ventana,
            self.reglas,
        )

        self.assertEqual(len(resultado["programadas"]), 1)
        self.assertEqual(len(resultado["sin_programar"]), 0)
        self.assertEqual(
            resultado["programadas"][0]["fecha"],
            date(2026, 12, 7),
        )

if __name__ == "__main__":
    unittest.main()
()