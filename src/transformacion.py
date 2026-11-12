
from src.estructura_contenido import obtener_secciones
from src.validador import crear_slug, generar_enlace_utm

def generar_post_con_utm(seccion, titulo_pieza, url_original, configuracion, fecha, numero=1):
    """Genera un post de LinkedIn completo con enlace UTM."""

    titulo = titulo_pieza.strip()

    slug = crear_slug(titulo)

    enlace_utm = generar_enlace_utm(
        url=url_original,
        canal="linkedin",
        slug_pieza_madre=slug,
        fecha=fecha,
        formato="post_linkedin",
        numero=numero,
        configuracion=configuracion
    )

    post = generar_post_automatico(
        seccion,
        titulo_pieza
    )

    return generar_post_linkedin(
        gancho=post["gancho"],
        desarrollo=post["desarrollo"],
        llamado_accion=post["llamado_accion"],
        enlace_utm=enlace_utm
    )

def extraer_pasos_implementacion(elementos):
    """Extrae pasos numerados de cualquier documento estructurado."""

    import re

    secciones = obtener_secciones(elementos)
    pasos = []

    for seccion in secciones:
        titulo = seccion["titulo"].strip()

        # Reconoce títulos que comienzan con un número seguido de punto.
        coincidencia = re.match(r"^(\d+)\.\s+(.+)", titulo)

        if not coincidencia:
            continue

        if not seccion["parrafos"]:
            continue

        pasos.append({
            "numero": int(coincidencia.group(1)),
            "titulo": coincidencia.group(2).strip(),
            "descripcion": seccion["parrafos"][0]
        })

    return pasos


def generar_carrusel(pasos, tema=""):
    """Construye un carrusel adaptable a los pasos extraídos del documento."""

    if not 5 <= len(pasos) <= 8:
        raise ValueError(
"El carrusel requiere entre cinco y ocho pasos."        )

    def resumir(texto, limite=25):
        """Obtiene un resumen extractivo de máximo 25 palabras."""

        palabras = texto.split()

        if len(palabras) <= limite:
            return texto.strip()

        return " ".join(palabras[:limite]).rstrip(".,;:") + "..."

    titulo_tema = tema.strip() or "Ideas principales"

    diapositivas = [
        {
            "numero": 1,
            "tipo": "portada",
            "titulo": titulo_tema,
            "texto": "Conoce los pasos y conceptos principales de este contenido."
        }
    ]

    for paso in pasos:
        titulo = paso["titulo"]

        palabras_disponibles = 30 - len(titulo.split())

        texto_resumido = resumir(
            paso["descripcion"],
            limite=palabras_disponibles
        )

        diapositivas.append({
            "numero": len(diapositivas) + 1,
            "tipo": "contenido",
            "titulo": titulo,
            "texto": texto_resumido,
            "fuente": paso["descripcion"]
        })

    diapositivas.append({
        "numero": len(diapositivas) + 1,
        "tipo": "cierre",
        "titulo": "El siguiente paso comienza contigo",
        "texto": "Analiza la información y decide cómo aplicarla a tu contexto."
    })

    return diapositivas

def generar_post_linkedin(gancho, desarrollo, llamado_accion, enlace_utm):
    """Construye un post de LinkedIn con estructura y saltos de línea."""

    partes = {
        "gancho": gancho,
        "desarrollo": desarrollo,
        "llamado_accion": llamado_accion,
        "enlace_utm": enlace_utm
    }

    for nombre, valor in partes.items():
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                f"El campo '{nombre}' es obligatorio y debe contener texto."
            )

    gancho = gancho.strip()
    desarrollo = desarrollo.strip()
    llamado_accion = llamado_accion.strip()
    enlace_utm = enlace_utm.strip()

    texto = "\n\n".join([
        gancho,
        desarrollo,
        llamado_accion,
        enlace_utm
    ])

    return {
        "formato": "post_linkedin",
        "gancho": gancho,
        "desarrollo": desarrollo,
        "llamado_accion": llamado_accion,
        "texto": texto,
        "enlace_utm": enlace_utm,
        "requiere_revision_humana": True
    }


def seleccionar_seccion_principal(elementos):
    """Selecciona la sección con mayor contenido útil del artículo."""

    secciones = obtener_secciones(elementos)
    secciones_validas = []

    for seccion in secciones:
        titulo = seccion["titulo"].strip()

        if titulo.lower() == "contenido inicial":
            continue

        if not seccion["parrafos"] and not seccion["listas"]:
            continue

        cantidad_palabras = sum(
            len(texto.split())
            for texto in seccion["parrafos"] + seccion["listas"]
        )

        if cantidad_palabras < 20:
            continue

        secciones_validas.append({
            **seccion,
            "cantidad_palabras": cantidad_palabras
        })

    if not secciones_validas:
        return None

    return max(
        secciones_validas,
        key=lambda seccion: (
            seccion["cantidad_palabras"]
            + len(seccion["listas"]) * 20
        )
    )

def generar_desarrollo_post(seccion, max_recomendaciones=3):
    """Construye el desarrollo de un post a partir de una sección."""

    parrafos = [
        texto.strip()
        for texto in seccion["parrafos"]
        if texto.strip()
        and "te podría interesar" not in texto.lower()
    ]

    listas = [
        texto.strip()
        for texto in seccion["listas"]
        if texto.strip()
    ]

    if not parrafos:
        raise ValueError(
            "La sección no contiene párrafos para desarrollar el post."
        )

    if not listas:
        raise ValueError(
            "La sección no contiene recomendaciones o elementos de apoyo."
        )

    introduccion = parrafos[0]

    explicacion = (
        parrafos[1]
        if len(parrafos) > 1
        else ""
    )

    recomendaciones = listas[:max_recomendaciones]

    partes = [
        introduccion,
        explicacion,
        "Aspectos que conviene considerar:",
    ]

    partes.extend(
        f"• {recomendacion}"
        for recomendacion in recomendaciones
    )

    return "\n\n".join(
        parte for parte in partes if parte
    )

def generar_gancho_post(seccion):
    """Genera un gancho a partir del título de una sección."""

    titulo = seccion["titulo"].strip()

    if not titulo:
        raise ValueError("La sección necesita un título.")

    titulo = titulo.replace("rpa", "RPA")
    titulo = titulo.replace("roi", "ROI")

    return (
    f"¿Qué debes saber sobre {titulo}? "
    "Analiza estas recomendaciones."
)
def generar_llamado_accion(titulo):
    """Genera un llamado a la acción basado en la pieza madre."""

    if not titulo or not titulo.strip():
        raise ValueError("Se necesita un título para generar el llamado.")

    return (
        f"¿Cómo aplicarías estas recomendaciones en tu organización? "
        f"Consulta la guía completa: {titulo.strip()}."
    )
def generar_llamado_accion(titulo):
    """Genera un llamado a la acción basado en la pieza madre."""

    if not titulo or not titulo.strip():
        raise ValueError("Se necesita un título para generar el llamado.")

    titulo = titulo.strip().rstrip(".")

    return (
        f"¿Cómo aplicarías estas recomendaciones en tu organización? "
        f"Consulta la guía completa: {titulo}."
    )
def generar_post_automatico(seccion, titulo_pieza=None):
    """Genera un post completo a partir de una sección."""

    gancho = generar_gancho_post(seccion)

    desarrollo = generar_desarrollo_post(seccion)

    titulo = titulo_pieza or seccion["titulo"]

    llamado_accion = generar_llamado_accion(titulo)

    return {
        "formato": "post_linkedin",
        "gancho": gancho,
        "desarrollo": desarrollo,
        "llamado_accion": llamado_accion,
        "requiere_revision_humana": True
    }
def extraer_titulo_pieza(elementos):
    """Obtiene el título principal de la pieza madre."""

    for elemento in elementos:
        if elemento["tipo"] == "titulo":
            titulo = elemento["texto"].strip()

            if titulo:
                return titulo

    raise ValueError(
        "No se encontró un título en la pieza madre."
    )
