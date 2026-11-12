
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from pathlib import Path


class ExtractorHTML(HTMLParser):
    """Extrae texto HTML conservando palabras y párrafos."""

    ETIQUETAS_BLOQUE = {
        "address", "article", "aside", "blockquote", "br",
        "div", "h1", "h2", "h3", "h4", "h5", "h6",
        "li", "main", "ol", "p", "section", "table",
        "tr", "ul"
    }

    ETIQUETAS_IGNORADAS = {
        "script", "style", "noscript", "svg",
        "nav", "footer", "header"
    }

    def __init__(self):
        super().__init__()
        self.textos = []
        self.pila_ignorada = []

    def handle_starttag(self, tag, attrs):
        if tag in self.ETIQUETAS_IGNORADAS:
            self.pila_ignorada.append(tag)

        elif not self.pila_ignorada and tag in self.ETIQUETAS_BLOQUE:
            self.textos.append("\n")

    def handle_endtag(self, tag):
        if tag in self.ETIQUETAS_IGNORADAS:
            if tag in self.pila_ignorada:
                posicion = len(self.pila_ignorada) - 1 - self.pila_ignorada[::-1].index(tag)
                del self.pila_ignorada[posicion:]

        elif not self.pila_ignorada and tag in self.ETIQUETAS_BLOQUE:
            self.textos.append("\n")

    def handle_data(self, data):
        if not self.pila_ignorada:
            self.textos.append(data)

    def obtener_texto(self):
        texto = "".join(self.textos)
        lineas = []

        for linea in texto.splitlines():
            linea = " ".join(linea.split())

            if linea:
                lineas.append(linea)

        return "\n".join(lineas)


def extraer_texto_html(html):
    """Convierte el HTML en texto legible."""

    extractor = ExtractorHTML()
    extractor.feed(html)
    extractor.close()

    return extractor.obtener_texto()


def leer_url(url, timeout=20):
    """Descarga una página web y extrae su contenido."""

    if not url.startswith(("http://", "https://")):
        raise ValueError(
            "La URL debe comenzar con http:// o https://"
        )

    solicitud = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    try:
        with urlopen(solicitud, timeout=timeout) as respuesta:
            contenido = respuesta.read()
            codificacion = (
                respuesta.headers.get_content_charset() or "utf-8"
            )

        html = contenido.decode(codificacion, errors="replace")
        texto = extraer_texto_html(html)

        if not texto.strip():
            raise ValueError(
                "La página no contiene texto extraíble."
            )

        return texto

    except HTTPError as error:
        raise RuntimeError(
            f"Error HTTP al consultar la página: {error.code}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            f"No fue posible conectar con la página: {error.reason}"
        ) from error


def leer_archivo_local(ruta):
    """Lee un archivo HTML local como respaldo."""

    ruta = Path(ruta)

    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta}"
        )

    html = ruta.read_text(
        encoding="utf-8",
        errors="replace"
    )

    texto = extraer_texto_html(html)

    if not texto.strip():
        raise ValueError(
            "El archivo no contiene texto extraíble."
        )

    return texto

def leer_html_url(url, timeout=20):
    """Descarga una página web y devuelve su HTML original."""

    if not url.startswith(("http://", "https://")):
        raise ValueError(
            "La URL debe comenzar con http:// o https://"
        )

    solicitud = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    try:
        with urlopen(solicitud, timeout=timeout) as respuesta:
            contenido = respuesta.read()
            codificacion = (
                respuesta.headers.get_content_charset() or "utf-8"
            )

        return contenido.decode(codificacion, errors="replace")

    except HTTPError as error:
        raise RuntimeError(
            f"Error HTTP al consultar la página: {error.code}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            f"No fue posible conectar con la página: {error.reason}"
        ) from error
