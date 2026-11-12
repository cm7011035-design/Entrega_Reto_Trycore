
from html.parser import HTMLParser


class ExtractorEstructura(HTMLParser):
    """Identifica títulos, párrafos y listas dentro de un HTML."""

    ETIQUETAS_TITULO = {
        "h1", "h2", "h3", "h4", "h5", "h6"
    }

    def __init__(self):
        super().__init__()
        self.elementos = []
        self.etiqueta_actual = None
        self.texto_actual = []
        self.profundidad_ignorada = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "nav", "footer", "header"}:
            self.profundidad_ignorada += 1
            return

        if self.profundidad_ignorada:
            return

        if tag in self.ETIQUETAS_TITULO:
            self.etiqueta_actual = "titulo"
            self.texto_actual = []

        elif tag == "p":
            self.etiqueta_actual = "parrafo"
            self.texto_actual = []

        elif tag == "li":
            self.etiqueta_actual = "elemento_lista"
            self.texto_actual = []

    def handle_endtag(self, tag):
        if tag in {"script", "style", "nav", "footer", "header"}:
            if self.profundidad_ignorada:
                self.profundidad_ignorada -= 1
            return

        if self.profundidad_ignorada:
            return

        etiquetas = {
            "titulo": self.ETIQUETAS_TITULO,
            "parrafo": {"p"},
            "elemento_lista": {"li"},
        }

        if self.etiqueta_actual:
            tipo = self.etiqueta_actual

            if tag in etiquetas[tipo]:
                texto = " ".join("".join(self.texto_actual).split())

                if texto:
                    self.elementos.append({
                        "tipo": tipo,
                        "texto": texto
                    })

                self.etiqueta_actual = None
                self.texto_actual = []

    def handle_data(self, data):
        if not self.profundidad_ignorada and self.etiqueta_actual:
            self.texto_actual.append(data)


def extraer_estructura_html(html):
    """Devuelve títulos, párrafos y elementos de lista."""

    extractor = ExtractorEstructura()
    extractor.feed(html)
    extractor.close()

    return extractor.elementos


def obtener_secciones(elementos):
    """Agrupa los párrafos y listas bajo cada título."""

    secciones = []
    seccion_actual = {
        "titulo": "Contenido inicial",
        "parrafos": [],
        "listas": []
    }

    for elemento in elementos:
        if elemento["tipo"] == "titulo":
            if seccion_actual["parrafos"] or seccion_actual["listas"]:
                secciones.append(seccion_actual)

            seccion_actual = {
                "titulo": elemento["texto"],
                "parrafos": [],
                "listas": []
            }

        elif elemento["tipo"] == "parrafo":
            seccion_actual["parrafos"].append(elemento["texto"])

        elif elemento["tipo"] == "elemento_lista":
            seccion_actual["listas"].append(elemento["texto"])

    if seccion_actual["parrafos"] or seccion_actual["listas"]:
        secciones.append(seccion_actual)

    return secciones
