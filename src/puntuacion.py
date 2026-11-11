
from src.historial import (
    analizar_historial,
    calcular_mediana,
    leer_historial,
    eliminar_duplicados,
    normalizar_registros,
)


PESOS_METRICAS = {
    "impresiones": 0.40,
    "reacciones": 0.30,
    "clics": 0.30,
}


def obtener_datos_historicos():
    """Obtiene estadísticas históricas limpias para la puntuación."""

    analisis = analizar_historial()

    registros_originales = leer_historial()

    registros_unicos, duplicados = eliminar_duplicados(
        registros_originales
    )

    registros = normalizar_registros(registros_unicos)

    medianas_temas = {}

    for registro in analisis["medianas_temas"]:
        tema = registro["tema"]

        medianas_temas[tema] = {
            "impresiones": registro["mediana_impresiones"],
            "reacciones": registro["mediana_reacciones"],
            "clics": registro["mediana_clics"],
            "publicaciones": registro["publicaciones"],
        }

    return {
        "registros": registros,
        "formatos": calcular_medianas_por_formato(registros),
        "temas": medianas_temas,
        "total_publicaciones": analisis["total_unicos"],
        "total_duplicados": analisis["total_duplicados"],
        "valores_extremos": analisis["valores_extremos"],
    }


def normalizar_puntuacion(valor, referencia):
    """Convierte una métrica en una puntuación de 0 a 100."""

    if valor is None or referencia is None:
        return None

    if referencia <= 0 or valor < 0:
        return None

    puntuacion = (valor / referencia) * 100

    return round(min(puntuacion, 100), 2)


def calcular_medianas_por_formato(registros):
    """Calcula las medianas de rendimiento de cada formato."""

    formatos = {}

    for registro in registros:
        formato = registro.get("formato", "").strip()

        if not formato:
            continue

        if formato not in formatos:
            formatos[formato] = {
                "impresiones": [],
                "reacciones": [],
                "clics": [],
                "publicaciones": 0,
            }

        formatos[formato]["publicaciones"] += 1

        for metrica in ["impresiones", "reacciones", "clics"]:
            valor = registro.get(metrica)

            if valor is not None:
                formatos[formato][metrica].append(valor)

    resultados = {}

    for formato, metricas in formatos.items():
        resultados[formato] = {
            "impresiones": calcular_mediana(metricas["impresiones"]),
            "reacciones": calcular_mediana(metricas["reacciones"]),
            "clics": calcular_mediana(metricas["clics"]),
            "publicaciones": metricas["publicaciones"],
        }

    return resultados


def obtener_referencias(medianas):
    """Obtiene el mayor valor histórico de cada métrica."""

    referencias = {}

    for metrica in PESOS_METRICAS:
        valores = [
            datos[metrica]
            for datos in medianas.values()
            if datos.get(metrica) is not None
        ]

        referencias[metrica] = max(valores) if valores else None

    return referencias


def comparar_rendimiento(medianas, formato, tema):
    """Compara un formato y un tema frente a su historial."""

    datos_formato = medianas["formatos"].get(formato)
    datos_tema = medianas["temas"].get(tema)

    if datos_formato is None:
        return None, "No existe historial para este formato."

    if datos_tema is None:
        return None, "No existe historial para este tema."

    return {
        "formato": datos_formato,
        "tema": datos_tema,
    }, "Comparación histórica disponible."


def calcular_puntuaciones_metricas(datos, referencias):
    """Calcula las puntuaciones históricas de cada métrica."""

    puntuaciones = {}

    for metrica in PESOS_METRICAS:
        valor_formato = datos["formato"].get(metrica)
        valor_tema = datos["tema"].get(metrica)

        referencia_formato = referencias["formatos"].get(metrica)
        referencia_tema = referencias["temas"].get(metrica)

        puntuacion_formato = normalizar_puntuacion(
            valor_formato,
            referencia_formato,
        )

        puntuacion_tema = normalizar_puntuacion(
            valor_tema,
            referencia_tema,
        )

        if puntuacion_formato is None or puntuacion_tema is None:
            puntuaciones[metrica] = None
            continue

        puntuaciones[metrica] = round(
            (puntuacion_formato * 0.5)
            + (puntuacion_tema * 0.5),
            2,
        )

    return puntuaciones


def calcular_puntuacion_final(puntuaciones):
    """Combina las métricas y devuelve una puntuación de 0 a 100."""

    if any(
        puntuaciones.get(metrica) is None
        for metrica in PESOS_METRICAS
    ):
        return None

    resultado = sum(
        puntuaciones[metrica] * peso
        for metrica, peso in PESOS_METRICAS.items()
    )

    return round(resultado, 2)


def clasificar_evidencia(cantidad_formato, cantidad_tema):
    """Clasifica la cantidad de publicaciones disponibles."""

    cantidad = min(cantidad_formato, cantidad_tema)

    if cantidad >= 15:
        return "sólida"

    if cantidad >= 8:
        return "moderada"

    if cantidad >= 5:
        return "limitada"

    return "insuficiente"


def contar_publicaciones_por_formato_y_tema(registros, formato, tema):
    """Cuenta las publicaciones que coinciden con el formato y el tema."""

    cantidad_formato = sum(
        1 for registro in registros
        if registro.get("formato") == formato
    )

    cantidad_tema = sum(
        1 for registro in registros
        if registro.get("tema") == tema
    )

    return cantidad_formato, cantidad_tema


def preparar_referencias(datos):
    """Prepara los valores máximos para normalizar las métricas."""

    referencias_formatos = obtener_referencias(datos["formatos"])
    referencias_temas = obtener_referencias(datos["temas"])

    return {
        "formatos": referencias_formatos,
        "temas": referencias_temas,
    }


def calificar_publicacion(formato, tema):
    """Calcula el rendimiento histórico relativo de una publicación."""

    datos = obtener_datos_historicos()

    comparacion, mensaje = comparar_rendimiento(
        datos,
        formato,
        tema,
    )

    if comparacion is None:
        return {
            "formato": formato,
            "tema": tema,
            "puntuacion": None,
            "estado": "sin datos suficientes",
            "explicacion": mensaje,
        }

    referencias = preparar_referencias(datos)

    puntuaciones = calcular_puntuaciones_metricas(
        comparacion,
        referencias,
    )

    puntuacion_final = calcular_puntuacion_final(puntuaciones)

    cantidad_formato, cantidad_tema = (
        contar_publicaciones_por_formato_y_tema(
            datos["registros"],
            formato,
            tema,
        )
    )

    evidencia = clasificar_evidencia(
        cantidad_formato,
        cantidad_tema,
    )

    if puntuacion_final is None:
        return {
            "formato": formato,
            "tema": tema,
            "puntuacion": None,
            "puntuaciones_metricas": puntuaciones,
            "estado": "sin datos suficientes",
            "explicacion": "No fue posible calcular todas las métricas.",
        }

    return {
        "formato": formato,
        "tema": tema,
        "puntuacion": puntuacion_final,
        "puntuaciones_metricas": puntuaciones,
        "publicaciones_formato": cantidad_formato,
        "publicaciones_tema": cantidad_tema,
        "nivel_evidencia": evidencia,
        "estado": "calculado",
        "explicacion": (
            "Puntuación relativa basada en las medianas históricas "
            "del formato y del tema."
        ),
    }
