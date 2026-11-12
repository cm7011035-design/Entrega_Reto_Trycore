from pathlib import Path
import json

from src.configuracion import cargar_configuracion
from src.lector_fuente import leer_html_url, extraer_texto_html

from src.estructura_contenido import extraer_estructura_html
from src.diagnostico import diagnosticar_contenido

from src.transformacion import (
    extraer_titulo_pieza,
    extraer_pasos_implementacion,
    seleccionar_seccion_principal,
    generar_carrusel,
    generar_post_con_utm
)
from src.validador_formatos import validar_formato

from src.calendario import (
    cargar_ventana,
    cargar_calendario_ocupado,
    cargar_reglas_calendario,
    normalizar_publicaciones_ocupadas,
    programar_publicaciones,
    guardar_calendario
)

from src.puntuacion import calificar_publicacion

from src.historial import analizar_historial
from src.tablero import guardar_tablero

def cargar_pieza_madre():
    """Lee y prepara la pieza madre desde la URL configurada."""

    ruta_url = Path("02_insumos/pieza_madre/url.txt")

    url = ruta_url.read_text(
        encoding="utf-8"
    ).strip()

    html = leer_html_url(url)

    texto = extraer_texto_html(html)

    elementos = extraer_estructura_html(html)

    titulo = extraer_titulo_pieza(elementos)

    diagnostico = diagnosticar_contenido(texto)

    seccion = seleccionar_seccion_principal(elementos)

    pasos = extraer_pasos_implementacion(elementos)

    return {
        "url": url,
        "html": html,
        "texto": texto,
        "elementos": elementos,
        "titulo": titulo,
        "diagnostico": diagnostico,
        "seccion_principal": seccion,
        "pasos": pasos
    }

def generar_formatos(pieza, configuracion, fecha):
    """Genera y valida los formatos derivados de la pieza madre."""

    titulo = pieza["titulo"]
    url = pieza["url"]
    seccion = pieza["seccion_principal"]
    pasos = pieza["pasos"]

    post = generar_post_con_utm(
        seccion,
        titulo,
        url,
        configuracion,
        fecha
    )

    carrusel = generar_carrusel(
        pasos,
        titulo
    )

    validacion_post = validar_formato(
        "post_linkedin",
        post,
        configuracion
    )

    validacion_carrusel = validar_formato(
        "carrusel_linkedin",
        {
            "laminas": [
                diapositiva["titulo"] + " " + diapositiva["texto"]
                for diapositiva in carrusel
            ]
        },
        configuracion
    )

    return {
        "post": post,
        "carrusel": carrusel,
        "validacion_post": validacion_post,
        "validacion_carrusel": validacion_carrusel
    }

def preparar_publicaciones(formato_generado, tema):
    """Prepara los contenidos para enviarlos al calendario."""

    return [
        {
            "tema": tema,
            "canal": "linkedin",
            "formato": "post_linkedin",
            "titulo": "Post: " + formato_generado["post"]["gancho"]
        },
        {
            "tema": tema,
            "canal": "linkedin",
            "formato": "carrusel_linkedin",
            "titulo": "Carrusel: " + formato_generado["carrusel"][0]["titulo"]
        }
    ]

def programar_y_guardar(publicaciones_nuevas):
    """Programa las publicaciones y guarda el calendario resultante."""

    ventana = cargar_ventana()

    originales = cargar_calendario_ocupado()

    ocupadas = normalizar_publicaciones_ocupadas(
        originales
    )

    reglas = cargar_reglas_calendario()

    resultado = programar_publicaciones(
        publicaciones_nuevas,
        ocupadas,
        ventana,
        reglas
    )

    ruta_salida = Path("salidas/calendario.csv")

    guardar_calendario(
        resultado["calendario"],
        ruta_salida
    )

    return resultado

def calificar_formatos(tema):
    """Calcula las puntuaciones históricas de los formatos generados."""

    puntuacion_post = calificar_publicacion(
        "post_linkedin",
        tema
    )

    puntuacion_carrusel = calificar_publicacion(
        "carrusel_linkedin",
        tema
    )

    return {
        "post_linkedin": puntuacion_post,
        "carrusel_linkedin": puntuacion_carrusel
    }

def generar_resumen(pieza, formatos, programacion, puntuaciones):
    """Reúne los resultados principales del proceso."""

    return {
        "titulo_pieza_madre": pieza["titulo"],
        "diagnostico": pieza["diagnostico"],
        "formatos_generados": {
            "post_linkedin": formatos["post"],
            "carrusel_linkedin": formatos["carrusel"]
        },
        "validaciones": {
            "post_linkedin": formatos["validacion_post"],
            "carrusel_linkedin": formatos["validacion_carrusel"]
        },
        "puntuaciones": puntuaciones,
        "publicaciones_programadas": programacion["programadas"],
        "publicaciones_sin_programar": programacion["sin_programar"],
        "total_publicaciones_calendario": len(
            programacion["calendario"]
        )
    }

def ejecutar_proceso():
    """Ejecuta el flujo completo de automatización de mercadeo."""

    print("\nINICIANDO AUTOMATIZACIÓN DE MERCADEO")

    configuracion = cargar_configuracion()

    pieza = cargar_pieza_madre()

    ventana = cargar_ventana()

    fecha = ventana["inicio"].strftime("%Y-%m-%d")

    formatos = generar_formatos(
        pieza,
        configuracion,
        fecha
    )

    publicaciones = preparar_publicaciones(
        formatos,
        "rpa"
    )

    programacion = programar_y_guardar(
        publicaciones
    )

    puntuaciones = calificar_formatos("rpa")

    historial = analizar_historial()

    resumen = generar_resumen(
        pieza,
        formatos,
        programacion,
        puntuaciones
    )

    resumen["analisis_historico"] = historial

    ruta_resumen = Path("salidas/resumen.json")

    ruta_resumen.write_text(
        json.dumps(
            resumen,
            ensure_ascii=False,
            indent=4,
            default=str
        ),
        encoding="utf-8"
    )

    ruta_tablero = guardar_tablero()

    print("Tablero generado:", ruta_tablero)

    print("\nPROCESO FINALIZADO")
    print("Formatos generados:", len(resumen["formatos_generados"]))
    print("Publicaciones programadas:", len(programacion["programadas"]))
    print("Publicaciones pendientes:", len(programacion["sin_programar"]))
    print("Total en calendario:", resumen["total_publicaciones_calendario"])

    return resumen

if __name__ == "__main__":
    ejecutar_proceso()