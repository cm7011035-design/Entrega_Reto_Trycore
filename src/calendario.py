import csv
import json

from datetime import date, datetime, timedelta
from pathlib import Path

from src.configuracion import cargar_configuracion


# Ubicación principal del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Archivos de entrada del calendario
RUTA_VENTANA = (
    BASE_DIR
    / "02_insumos"
    / "calendario"
    / "ventana.json"
)

RUTA_CALENDARIO_OCUPADO = (
    BASE_DIR
    / "02_insumos"
    / "calendario"
    / "calendario_ocupado.csv"
)

def cargar_ventana():
    """
    Lee las fechas de inicio y fin del calendario.
    """

    if not RUTA_VENTANA.exists():
        raise FileNotFoundError(
            f"No se encontró la ventana: {RUTA_VENTANA}"
        )

    with RUTA_VENTANA.open(
        "r",
        encoding="utf-8"
    ) as archivo:
        ventana = json.load(archivo)

    inicio = date.fromisoformat(ventana["inicio"])
    fin = date.fromisoformat(ventana["fin"])

    if inicio > fin:
        raise ValueError(
            "La fecha de inicio no puede ser posterior a la fecha final."
        )

    return {
        "variante": ventana.get("variante"),
        "inicio": inicio,
        "fin": fin,
    }

def cargar_calendario_ocupado():
    """
    Lee las publicaciones que ya están programadas.
    """

    if not RUTA_CALENDARIO_OCUPADO.exists():
        raise FileNotFoundError(
            f"No se encontró el calendario ocupado: "
            f"{RUTA_CALENDARIO_OCUPADO}"
        )

    with RUTA_CALENDARIO_OCUPADO.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as archivo:
        lector = csv.DictReader(archivo)
        publicaciones = list(lector)

    campos_obligatorios = {
        "fecha",
        "hora",
        "canal",
        "formato",
        "tema",
        "titulo",
        "estado",
    }

    if not campos_obligatorios.issubset(
        lector.fieldnames or []
    ):
        raise ValueError(
            "El calendario ocupado no contiene todas las columnas necesarias."
        )

    return publicaciones

def cargar_reglas_calendario():
    """
    Obtiene las reglas de programación desde config.json.
    """

    configuracion = cargar_configuracion()

    reglas = configuracion.get("calendario")

    reglas["limites_por_formato"] = {
        formato["id"]: formato["max_por_semana"]
        for formato in configuracion.get("matriz_formatos", [])
        if "id" in formato and "max_por_semana" in formato
    }

    if not isinstance(reglas, dict):
        raise ValueError(
            "No se encontraron las reglas del calendario."
        )

    campos_obligatorios = [
        "zona_horaria",
        "dias_habiles",
        "franjas_de_publicacion",
        "capacidad_max_por_dia",
        "capacidad_max_por_semana",
        "separacion_minima_mismo_tema_horas",
        "festivos",
    ]

    for campo in campos_obligatorios:
        if campo not in reglas:
            raise ValueError(
                f"Falta la regla obligatoria: {campo}"
            )

    return reglas

def cargar_festivos(reglas):
    """
    Convierte los festivos configurados en fechas de Python.
    """

    festivos = set()

    for festivo in reglas["festivos"]:
        fecha = date.fromisoformat(festivo["fecha"])
        festivos.add(fecha)

    return festivos

def es_dia_habil(fecha, reglas, festivos):
    """
    Comprueba si una fecha permite programar publicaciones.
    """

    nombres_dias = {
        0: "lunes",
        1: "martes",
        2: "miércoles",
        3: "jueves",
        4: "viernes",
        5: "sábado",
        6: "domingo",
    }

    nombre_dia = nombres_dias[fecha.weekday()]

    if nombre_dia not in reglas["dias_habiles"]:
        return False

    if fecha in festivos:
        return False

    return True

def contar_publicaciones_por_dia(publicaciones, fecha):
    """
    Cuenta las publicaciones existentes en una fecha.
    """

    return sum(
        1
        for publicacion in publicaciones
        if publicacion["fecha"] == fecha
        and publicacion["estado"].lower() == "programada"
    )

def contar_publicaciones_por_semana(publicaciones, fecha):
    """
    Cuenta las publicaciones programadas durante la semana.
    La semana comienza el lunes y termina el domingo.
    """

    inicio_semana = fecha - timedelta(
        days=fecha.weekday()
    )

    fin_semana = inicio_semana + timedelta(days=6)

    return sum(
        1
        for publicacion in publicaciones
        if inicio_semana <= publicacion["fecha"] <= fin_semana
        and publicacion["estado"].lower() == "programada"
    )

def contar_publicaciones_por_formato_semana(
    publicaciones,
    fecha,
    formato
):
    """
    Cuenta las publicaciones de un formato durante una semana.
    La semana comienza el lunes y termina el domingo.
    """

    inicio_semana = fecha - timedelta(
        days=fecha.weekday()
    )

    fin_semana = inicio_semana + timedelta(days=6)

    return sum(
        1
        for publicacion in publicaciones
        if inicio_semana <= publicacion["fecha"] <= fin_semana
        and publicacion["estado"].lower() == "programada"
        and publicacion["formato"] == formato
    )

def horario_ocupado(publicaciones, fecha, hora):
    """
    Comprueba si una fecha y hora ya están ocupadas.
    """

    for publicacion in publicaciones:
        if (
            publicacion["fecha"] == fecha
            and publicacion["hora"] == hora
            and publicacion["estado"].lower() == "programada"
        ):
            return True

    return False

def tema_respetar_separacion(
    publicaciones,
    fecha,
    hora,
    tema,
    horas_minimas
):
    """
    Comprueba que un tema respete la separación mínima
    respecto a sus publicaciones anteriores o posteriores.
    """

    nueva_fecha_hora = datetime.combine(fecha, hora)

    for publicacion in publicaciones:
        if (
            publicacion["tema"].strip().lower()
            != tema.strip().lower()
            or publicacion["estado"].lower() != "programada"
        ):
            continue

        fecha_hora_existente = datetime.combine(
            publicacion["fecha"],
            publicacion["hora"]
        )

        diferencia = abs(
            nueva_fecha_hora - fecha_hora_existente
        )

        if diferencia < timedelta(hours=horas_minimas):
            return False

    return True

def validar_horario(
    fecha,
    hora,
    tema,
    publicaciones,
    reglas,
    festivos
):
    """
    Comprueba si una publicación puede ocupar un horario.
    """

    if not es_dia_habil(fecha, reglas, festivos):
        return False

    if hora.strftime("%H:%M") not in reglas["franjas_de_publicacion"]:
        return False

    if horario_ocupado(publicaciones, fecha, hora):
        return False

    if contar_publicaciones_por_dia(
        publicaciones, fecha
    ) >= reglas["capacidad_max_por_dia"]:
        return False

    if contar_publicaciones_por_semana(
        publicaciones, fecha
    ) >= reglas["capacidad_max_por_semana"]:
        return False

    if not tema_respetar_separacion(
        publicaciones,
        fecha,
        hora,
        tema,
        reglas["separacion_minima_mismo_tema_horas"]
    ):
        return False

    return True

def generar_horarios_disponibles(
    ventana,
    publicaciones,
    reglas,
    tema
):
    """
    Busca todos los horarios válidos dentro de la ventana.
    """

    festivos = cargar_festivos(reglas)

    horarios_disponibles = []
    fecha_actual = ventana["inicio"]

    while fecha_actual <= ventana["fin"]:

        for franja in reglas["franjas_de_publicacion"]:
            hora = datetime.strptime(
                franja,
                "%H:%M"
            ).time()

            if validar_horario(
                fecha_actual,
                hora,
                tema,
                publicaciones,
                reglas,
                festivos
            ):
                horarios_disponibles.append({
                    "fecha": fecha_actual,
                    "hora": hora,
                    "tema": tema,
                })

        fecha_actual += timedelta(days=1)

    return horarios_disponibles

def programar_publicacion(
    publicacion,
    publicaciones,
    ventana,
    reglas
):
    """
    Asigna el primer horario válido a una publicación.
    """

    tema = publicacion["tema"]

    horarios = generar_horarios_disponibles(
        ventana,
        publicaciones,
        reglas,
        tema
    )

    if not horarios:
        return None

    horario_elegido = horarios[0]

    nueva_publicacion = {
        "fecha": horario_elegido["fecha"],
        "hora": horario_elegido["hora"],
        "canal": publicacion["canal"],
        "formato": publicacion["formato"],
        "tema": tema,
        "titulo": publicacion["titulo"],
        "estado": "programada",
    }

    publicaciones.append(nueva_publicacion)

    return nueva_publicacion

def guardar_calendario(publicaciones, ruta_salida):
    """
    Guarda el calendario generado en un archivo CSV.
    """

    campos = [
        "fecha",
        "hora",
        "canal",
        "formato",
        "tema",
        "titulo",
        "estado",
    ]

    with Path(ruta_salida).open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=campos
        )

        escritor.writeheader()

        for publicacion in publicaciones:
            registro = publicacion.copy()

            if isinstance(registro["fecha"], date):
                registro["fecha"] = registro["fecha"].isoformat()

            if hasattr(registro["hora"], "strftime"):
                registro["hora"] = registro["hora"].strftime("%H:%M")

            escritor.writerow(registro)

def programar_publicaciones(
    publicaciones_nuevas,
    publicaciones_ocupadas,
    ventana,
    reglas
):
    """
    Programa varias publicaciones respetando los límites
    generales y los límites semanales por formato.
    """

    calendario = publicaciones_ocupadas.copy()
    publicaciones_programadas = []
    publicaciones_sin_programar = []

    limites_por_formato = reglas.get(
        "limites_por_formato",
        {}
    )

    for publicacion in publicaciones_nuevas:

        formato = publicacion["formato"]
        limite_formato = limites_por_formato.get(formato)

        # Probamos el horario sobre una copia del calendario.
        calendario_prueba = calendario.copy()

        resultado = programar_publicacion(
            publicacion,
            calendario_prueba,
            ventana,
            reglas
        )

        if resultado is None:
            publicacion_pendiente = publicacion.copy()
            publicacion_pendiente["motivo"] = (
                "No se encontró un horario disponible."
            )
            publicaciones_sin_programar.append(
                publicacion_pendiente
            )
            continue

        fecha_propuesta = resultado["fecha"]

        cantidad_formato = contar_publicaciones_por_formato_semana(
            calendario,
            fecha_propuesta,
            formato
        )

        if (
            limite_formato is not None
            and cantidad_formato >= limite_formato
        ):
            publicacion_pendiente = publicacion.copy()
            publicacion_pendiente["motivo"] = (
                f"Se alcanzó el límite semanal de "
                f"{limite_formato} publicaciones para {formato}."
            )
            publicaciones_sin_programar.append(
                publicacion_pendiente
            )
            continue

        calendario = calendario_prueba
        publicaciones_programadas.append(resultado)

    return {
        "calendario": calendario,
        "programadas": publicaciones_programadas,
        "sin_programar": publicaciones_sin_programar,
    }
def normalizar_publicaciones_ocupadas(publicaciones):
    """
    Convierte las fechas y horas ocupadas a formatos comparables.
    """

    publicaciones_normalizadas = []

    for numero, publicacion in enumerate(publicaciones, start=2):
        try:
            fecha = date.fromisoformat(
                publicacion["fecha"].strip()
            )

            hora = datetime.strptime(
                publicacion["hora"].strip(),
                "%H:%M"
            ).time()

        except (ValueError, AttributeError) as error:
            raise ValueError(
                f"Fecha u hora inválida en la fila {numero} "
                f"del calendario ocupado."
            ) from error

        registro = {
            "fecha": fecha,
            "hora": hora,
            "canal": publicacion["canal"].strip(),
            "formato": publicacion["formato"].strip(),
            "tema": publicacion["tema"].strip(),
            "titulo": publicacion["titulo"].strip(),
            "estado": publicacion["estado"].strip(),
        }

        publicaciones_normalizadas.append(registro)

    return publicaciones_normalizadas