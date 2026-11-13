
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

from src.puntuacion import (
    calificar_publicacion,
    obtener_datos_historicos
)

from src.historial import analizar_historial
from src.tablero import guardar_tablero


def cargar_pieza_madre():
    """Lee la pieza madre desde la URL o utiliza el HTML de respaldo."""

    ruta_url = Path("02_insumos/pieza_madre/url.txt")
    ruta_respaldo = Path(
        "02_insumos/pieza_madre/guia_rpa_respaldo.html"
    )

    url = ruta_url.read_text(
        encoding="utf-8"
    ).strip()

    if not url:
        raise ValueError("El archivo url.txt está vacío.")

    fuente_utilizada = "url"

    try:
        html = leer_html_url(url)
        texto = extraer_texto_html(html)

        if not texto.strip():
            raise RuntimeError(
                "La URL no contiene texto extraíble."
            )

    except (RuntimeError, ValueError, OSError) as error:

        print("\nAVISO: No fue posible utilizar la URL.")
        print("Motivo:", error)
        print("Intentando utilizar el archivo de respaldo...")

        if not ruta_respaldo.exists():
            raise FileNotFoundError(
                "La URL falló y no existe el archivo de respaldo."
            )

        html = ruta_respaldo.read_text(
            encoding="utf-8",
            errors="replace"
        )

        texto = extraer_texto_html(html)

        if not texto.strip():
            raise ValueError(
                "El archivo de respaldo no contiene texto extraíble."
            )

        fuente_utilizada = "respaldo"

        print("Respaldo cargado correctamente.")

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
        "pasos": pasos,
        "fuente_utilizada": fuente_utilizada
    }


def seleccionar_tema_principal(diagnostico):
    """
    Selecciona el tema con más menciones en el diagnóstico.
    No utiliza un tema fijo.
    """

    temas = diagnostico.get("temas", [])

    if not temas:
        return "sin_clasificar"

    tema_principal = max(
        temas,
        key=lambda elemento: elemento["menciones"]
    )

    return tema_principal["tema"]


def consultar_disponibilidad_historica(tema):
    """
    Comprueba si el tema detectado existe en el historial.
    No reemplaza el tema si no encuentra coincidencias.
    """

    datos = obtener_datos_historicos()

    disponible = tema in datos["temas"]

    if disponible:
        publicaciones = datos["temas"][tema]["publicaciones"]
    else:
        publicaciones = 0

    return {
        "disponible": disponible,
        "publicaciones": publicaciones,
        "mensaje": (
            "Existe información histórica para este tema."
            if disponible
            else "No existe historial para este tema."
        )
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


def preparar_publicaciones(
    formato_generado,
    tema,
    titulo_pieza=None
):
    """Separa los formatos válidos de los rechazados."""

    publicaciones_validas = []
    publicaciones_rechazadas = []

    titulo_post = (
        titulo_pieza
        or formato_generado["post"]["gancho"]
    )

    titulo_carrusel = (
        titulo_pieza
        or formato_generado["carrusel"][0]["titulo"]
    )

    candidatos = [
        {
            "tema": tema,
            "canal": "linkedin",
            "formato": "post_linkedin",
            "titulo": titulo_post,
            "validacion": formato_generado["validacion_post"]
        },
        {
            "tema": tema,
            "canal": "linkedin",
            "formato": "carrusel_linkedin",
            "titulo": titulo_carrusel,
            "validacion": formato_generado["validacion_carrusel"]
        }
    ]

    for publicacion in candidatos:

        validacion = publicacion["validacion"]

        if validacion["valido"]:

            publicacion.pop("validacion")

            publicaciones_validas.append(publicacion)

        else:

            errores = [
                resultado["mensaje"]
                for resultado in validacion["resultados"]
                if not resultado["valido"]
            ]

            publicaciones_rechazadas.append({
                "tema": publicacion["tema"],
                "canal": publicacion["canal"],
                "formato": publicacion["formato"],
                "titulo": publicacion["titulo"],
                "estado": "rechazada_por_validacion",
                "motivo": " | ".join(errores)
            })

    return {
        "publicaciones_validas": publicaciones_validas,
        "publicaciones_rechazadas": publicaciones_rechazadas
    }


def programar_y_guardar(
    publicaciones_nuevas,
    publicaciones_rechazadas=None
):
    """Programa solamente publicaciones que superaron la validación."""

    if publicaciones_rechazadas is None:
        publicaciones_rechazadas = []

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

    resultado["sin_programar"].extend(
        publicaciones_rechazadas
    )

    resultado["total_publicaciones_existentes"] = len(
        originales
    )

    resultado["total_publicaciones_nuevas"] = len(
        resultado["programadas"]
    )

    ruta_salida = Path("salidas/calendario.csv")

    guardar_calendario(
        resultado["calendario"],
        ruta_salida
    )

    return resultado


def calificar_formatos(tema):
    """Calcula las puntuaciones históricas del tema detectado."""

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


def calificar_publicaciones_calendario(calendario):
    """
    Calcula una referencia histórica para cada combinación
    de formato y tema presente en el calendario.
    """

    puntuaciones = {}

    for publicacion in calendario:
        formato = publicacion.get("formato", "")
        tema = publicacion.get("tema", "")

        if not formato or not tema:
            continue

        clave = f"{formato}|{tema}"

        if clave not in puntuaciones:
            puntuaciones[clave] = calificar_publicacion(
                formato,
                tema
            )

    return puntuaciones


def generar_resumen(
    pieza,
    formatos,
    programacion,
    puntuaciones,
    tema,
    disponibilidad_historica
):
    """Reúne los resultados principales del proceso."""

    return {
        "titulo_pieza_madre": pieza["titulo"],
        "fuente_utilizada": pieza["fuente_utilizada"],
        "tema_detectado": tema,
        "disponibilidad_historica": disponibilidad_historica,
        "diagnostico": pieza["diagnostico"],
        "formatos_generados": {
            "post_linkedin": formatos["post"],
            "carrusel_linkedin": formatos["carrusel"]
        },
        "validaciones": {
            "post_linkedin": formatos["validacion_post"],
            "carrusel_linkedin": formatos["validacion_carrusel"]
        },
                "publicaciones_programadas": programacion["programadas"],
        "publicaciones_sin_programar": programacion["sin_programar"],
        "total_publicaciones_existentes": programacion[
            "total_publicaciones_existentes"
        ],
        "total_publicaciones_nuevas": programacion[
            "total_publicaciones_nuevas"
        ],
        "total_publicaciones_calendario": len(
            programacion["calendario"]
        )
    }


def ejecutar_proceso():
    """Ejecuta el flujo completo de automatización de mercadeo."""

    print("\nINICIANDO AUTOMATIZACIÓN DE MERCADEO")

    configuracion = cargar_configuracion()

    pieza = cargar_pieza_madre()

    tema = seleccionar_tema_principal(
        pieza["diagnostico"]
    )

    disponibilidad_historica = consultar_disponibilidad_historica(
        tema
    )

    print("Tema detectado:", tema)
    print(
        "Historial disponible:",
        disponibilidad_historica["disponible"]
    )

    ventana = cargar_ventana()

    fecha = ventana["inicio"].strftime("%Y-%m-%d")

    formatos = generar_formatos(
        pieza,
        configuracion,
        fecha
    )

    publicaciones = preparar_publicaciones(
        formatos,
        tema,
        pieza["titulo"]
    )

    programacion = programar_y_guardar(
        publicaciones["publicaciones_validas"],
        publicaciones["publicaciones_rechazadas"]
    )

    puntuaciones = calificar_formatos(tema)

    puntuaciones_calendario = calificar_publicaciones_calendario(
        programacion["calendario"]
    )

    historial = analizar_historial()

    resumen = generar_resumen(
        pieza,
        formatos,
        programacion,
        puntuaciones,
        tema,
        disponibilidad_historica
    )

    resumen["analisis_historico"] = historial
    resumen["puntuaciones_calendario"] = puntuaciones_calendario

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
    print("Tema utilizado:", tema)
    print("Formatos generados:", len(resumen["formatos_generados"]))
    print("Publicaciones programadas:", len(programacion["programadas"]))
    print("Publicaciones pendientes:", len(programacion["sin_programar"]))
    print("Total en calendario:", resumen["total_publicaciones_calendario"])

    return resumen


if __name__ == "__main__":
    ejecutar_proceso()
