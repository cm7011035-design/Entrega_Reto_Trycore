
from src.estructura_contenido import obtener_secciones
from src.validador import crear_slug, generar_enlace_utm


def generar_post_con_utm(
    seccion,
    titulo_pieza,
    url_original,
    configuracion,
    fecha,
    numero=1
):
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
    """Extrae pasos numerados de un documento estructurado."""

    import re

    secciones = obtener_secciones(elementos)
    pasos = []

    for seccion in secciones:
        titulo = seccion["titulo"].strip()

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
    """Construye un carrusel con resúmenes de máximo 30 palabras."""

    import re

    if not 5 <= len(pasos) <= 8:
        raise ValueError(
            "El carrusel requiere entre cinco y ocho pasos."
        )

    def resumir(texto, limite=25):
        """Prioriza oraciones completas sin superar el límite."""

        texto = texto.strip()

        if not texto:
            return "Consulta este paso en la guía original."

        oraciones = re.split(
            r'(?<=[.!?])\s+',
            texto
        )

        resultado = ""

        # Primero intenta conservar varias oraciones completas.
        for oracion in oraciones:
            propuesta = (
                resultado + " " + oracion
            ).strip()

            if len(propuesta.split()) <= limite:
                resultado = propuesta
            else:
                break

        if resultado:
            return resultado

        # Busca otra oración completa que pueda utilizarse.
        for oracion in oraciones:
            if len(oracion.split()) <= limite:
                return oracion.strip()

        # Si ninguna oración cabe, busca una idea completa
        # separada por comas, punto y coma o dos puntos.
        for oracion in oraciones:
            fragmentos = re.split(r"[,;:]", oracion)

            for fragmento in fragmentos:
                fragmento = fragmento.strip()

                if len(fragmento.split()) <= limite:
                    if fragmento:
                        return fragmento.rstrip(".,;:!?") + "."

        # Último recurso: utiliza las primeras palabras disponibles.
        palabras = texto.split()

        return " ".join(
            palabras[:limite]
        ).rstrip(".,;:!?") + "."

    titulo_tema = tema.strip() or "Ideas principales"

    diapositivas = [
        {
            "numero": 1,
            "tipo": "portada",
            "titulo": titulo_tema,
            "texto": (
                "Conoce los pasos y conceptos principales "
                "de este contenido."
            )
        }
    ]

    for paso in pasos:
        titulo = paso["titulo"].strip()

        palabras_disponibles = 30 - len(titulo.split())

        if palabras_disponibles < 1:
            raise ValueError(
                "El título de una lámina supera el límite de palabras."
            )

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
        "texto": (
            "Analiza la información y decide cómo aplicarla "
            "a tu contexto."
        )
    })

    return diapositivas


def generar_post_linkedin(
    gancho,
    desarrollo,
    llamado_accion,
    enlace_utm
):
    """Construye un post de LinkedIn con saltos de línea."""

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
        "Aspectos que conviene considerar:"
    ]

    partes.extend(
        f"• {recomendacion}"
        for recomendacion in recomendaciones
    )

    return "\n\n".join(
        parte for parte in partes if parte
    )


def generar_gancho_post(seccion):
    """Genera un gancho atractivo para LinkedIn."""

    titulo = seccion["titulo"].strip()

    if not titulo:
        raise ValueError("La sección necesita un título.")

    return (
        "¿Tu empresa está preparada para implementar RPA? "
        "Estas prácticas pueden ayudarte a dar el primer paso."
    )


def generar_llamado_accion(titulo):
    """Genera un llamado a la acción breve y natural."""

    if not titulo or not titulo.strip():
        raise ValueError(
            "Se necesita un título para generar el llamado."
        )

    return (
        "¿Qué proceso de tu empresa podría beneficiarse de RPA? "
        "Consulta la guía completa y descubre cómo empezar."
    )


def generar_post_automatico(seccion, titulo_pieza=None):
    """Genera los componentes de un post sin crear todavía el enlace UTM."""

    gancho = generar_gancho_post(seccion)
    desarrollo = generar_desarrollo_post(seccion)

    titulo_referencia = (
        titulo_pieza
        if titulo_pieza
        else seccion["titulo"]
    )

    llamado_accion = generar_llamado_accion(
        titulo_referencia
    )

    return {
        "gancho": gancho,
        "desarrollo": desarrollo,
        "llamado_accion": llamado_accion
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
