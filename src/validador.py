import re
import unicodedata


def normalizar_texto(texto):
    """Convierte el texto a minúsculas y elimina tildes."""
    texto = str(texto).lower()
    texto = unicodedata.normalize("NFD", texto)

    return "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )


def buscar_coincidencias(texto, lista_terminos):
    """Busca términos completos sin distinguir mayúsculas ni tildes."""

    texto_normalizado = normalizar_texto(texto)
    encontrados = []

    for termino in lista_terminos:
        termino_normalizado = normalizar_texto(termino)

        patron = (
            r"(?<!\w)"
            + r"\s+".join(
                re.escape(parte).replace("%", r"\s*%")
                for parte in termino_normalizado.split()
            )
            + r"(?!\w)"
        )

        if re.search(patron, texto_normalizado):
            encontrados.append(termino)

    return encontrados


def validar_contenido(texto, configuracion):
    """Valida productos, términos prohibidos y nombres confidenciales."""

    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("El contenido que se va a validar está vacío.")

    productos = configuracion["productos_vigentes"]

    prohibidos = [
        elemento["termino"]
        for elemento in configuracion["terminos_prohibidos"]
    ]

    confidenciales = configuracion["nombres_confidenciales"]

    productos_encontrados = buscar_coincidencias(
        texto, productos
    )

    terminos_encontrados = buscar_coincidencias(
        texto, prohibidos
    )

    nombres_encontrados = buscar_coincidencias(
        texto, confidenciales
    )

    alertas = []

    for termino in terminos_encontrados:
        alertas.append(
            f"Término prohibido detectado: {termino}"
        )

    for nombre in nombres_encontrados:
        alertas.append(
            f"Nombre confidencial detectado: {nombre}"
        )

    return {
        "valido": len(alertas) == 0,
        "productos_vigentes_detectados": productos_encontrados,
        "terminos_prohibidos_detectados": terminos_encontrados,
        "nombres_confidenciales_detectados": nombres_encontrados,
        "alertas": alertas,
    }

from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from datetime import datetime


def crear_slug(texto):
    """Convierte un texto en un identificador para una URL."""

    texto = normalizar_texto(texto)
    texto = re.sub(r"[^a-z0-9]+", "-", texto)
    return texto.strip("-")


def generar_enlace_utm(
    url,
    canal,
    slug_pieza_madre,
    fecha,
    formato,
    numero,
    configuracion
):
    """Genera un enlace con parámetros UTM según config.json."""

    reglas = configuracion["utm"]

    if canal not in reglas["utm_source"]:
        raise ValueError(f"Canal sin configuración UTM: {canal}")

    if canal not in reglas["utm_medium"]:
        raise ValueError(f"Medio sin configuración UTM: {canal}")

    if not isinstance(fecha, datetime):
        fecha = datetime.strptime(fecha, "%Y-%m-%d")

    slug = crear_slug(slug_pieza_madre)
    campana = fecha.strftime("%Y%m")

    parametros = {
        "utm_source": reglas["utm_source"][canal],
        "utm_medium": reglas["utm_medium"][canal],
        "utm_campaign": reglas["utm_campaign"].format(
            slug_pieza_madre=slug,
            aaaamm=campana
        ),
        "utm_content": reglas["utm_content"].format(
            formato=crear_slug(formato),
            numero=numero
        )
    }

    partes = urlparse(url)

    if partes.scheme not in ("http", "https") or not partes.netloc:
        raise ValueError("La URL proporcionada no es válida.")

    parametros_existentes = parse_qsl(
        partes.query,
        keep_blank_values=True
    )

    nombres_utm = set(parametros)

    parametros_existentes = [
        (clave, valor)
        for clave, valor in parametros_existentes
        if clave not in nombres_utm
    ]

    nueva_consulta = urlencode(
        parametros_existentes + list(parametros.items())
    )

    return urlunparse(
        partes._replace(query=nueva_consulta)
    )
def validar_enlace_utm(
    enlace, canal, slug_pieza_madre, fecha,
    formato, numero, configuracion
):
    """Comprueba que un enlace tenga los parámetros UTM correctos."""

    from urllib.parse import urlparse, parse_qs

    partes_url = urlparse(enlace)

    enlace_base = partes_url._replace(
        query="",
        fragment=""
    ).geturl()

    enlace_esperado = generar_enlace_utm(
        enlace_base,
        canal,
        slug_pieza_madre,
        fecha,
        formato,
        numero,
        configuracion
    )

    parametros_reales = parse_qs(
        partes_url.query,
        keep_blank_values=True
    )

    parametros_esperados = parse_qs(
        urlparse(enlace_esperado).query,
        keep_blank_values=True
    )

    errores = []

    for parametro, valores_esperados in parametros_esperados.items():

        valores_reales = parametros_reales.get(parametro)

        if valores_reales != valores_esperados:
            errores.append(
                f"El parámetro {parametro} falta, está duplicado "
                "o tiene un valor incorrecto."
            )

    for parametro in parametros_reales:

        if parametro.startswith("utm_") and parametro not in parametros_esperados:
            errores.append(
                f"El parámetro UTM adicional no está autorizado: {parametro}."
            )

    return {
        "valido": len(errores) == 0,
        "errores": errores,
        "mensaje": (
            "El enlace cumple las reglas UTM."
            if not errores
            else "El enlace no cumple las reglas UTM."
        )
    }
