
import re

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

    if not isinstance(titulo_pieza, str) or not titulo_pieza.strip():
        raise ValueError("El título de la pieza es obligatorio.")

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

    post = generar_post_automatico(seccion, titulo)

    return generar_post_linkedin(
        gancho=post["gancho"],
        desarrollo=post["desarrollo"],
        llamado_accion=post["llamado_accion"],
        enlace_utm=enlace_utm
    )


def extraer_pasos_implementacion(elementos):
    """Extrae pasos numerados de un documento estructurado."""

    secciones = obtener_secciones(elementos)
    pasos = []

    for seccion in secciones:
        titulo = seccion.get("titulo", "").strip()

        coincidencia = re.match(
            r"^(\d+)\.\s+(.+)",
            titulo
        )

        if not coincidencia:
            continue

        parrafos = seccion.get("parrafos", [])

        if not parrafos:
            continue

        descripcion = parrafos[0]

        if not isinstance(descripcion, str) or not descripcion.strip():
            continue

        pasos.append({
            "numero": int(coincidencia.group(1)),
            "titulo": coincidencia.group(2).strip(),
            "descripcion": descripcion.strip()
        })

    return pasos


def generar_carrusel(pasos, tema=""):
    """Construye un carrusel basado en contenido de la fuente."""

    if not isinstance(pasos, list) or not 5 <= len(pasos) <= 8:
        raise ValueError(
            "El carrusel requiere entre cinco y ocho pasos."
        )

    def resumir(texto, limite=25):
        """Prioriza oraciones completas sin superar el límite."""

        if not isinstance(texto, str):
            return "Consulta este paso en la guía original."

        texto = " ".join(texto.split())

        if not texto:
            return "Consulta este paso en la guía original."

        oraciones = re.split(r"(?<=[.!?])\s+", texto)
        resultado = ""

        for oracion in oraciones:
            propuesta = (resultado + " " + oracion).strip()

            if len(propuesta.split()) <= limite:
                resultado = propuesta
            else:
                break

        if resultado:
            return resultado

        for oracion in oraciones:
            if len(oracion.split()) <= limite:
                return oracion.strip()

        for oracion in oraciones:
            fragmentos = re.split(r"[,;:]", oracion)

            for fragmento in fragmentos:
                fragmento = fragmento.strip()

                if (
                    fragmento
                    and len(fragmento.split()) <= limite
                ):
                    return fragmento.rstrip(".,;:!?") + "."

        palabras = texto.split()

        return " ".join(
            palabras[:limite]
        ).rstrip(".,;:!?") + "."

    titulo_portada = (
        tema.strip()
        if isinstance(tema, str) and tema.strip()
        else "Ideas principales"
    )

    palabras_titulo = titulo_portada.split()

    if len(palabras_titulo) > 18:
        titulo_portada = " ".join(palabras_titulo[:17]) + "..."

    diapositivas = [
        {
            "numero": 1,
            "tipo": "portada",
            "titulo": titulo_portada,
            "texto": (
                "Conoce los principales pasos y recomendaciones "
                "extraídos de esta pieza de contenido."
            )
        }
    ]

    for paso in pasos:
        if not isinstance(paso, dict):
            raise ValueError(
                "Cada paso del carrusel debe ser un diccionario."
            )

        titulo = paso.get("titulo", "").strip()
        descripcion = paso.get("descripcion", "")

        if not titulo:
            raise ValueError(
                "Cada paso del carrusel necesita un título."
            )

        palabras_disponibles = 30 - len(titulo.split())

        if palabras_disponibles < 1:
            raise ValueError(
                "El título de una lámina supera el límite de palabras."
            )

        texto_resumido = resumir(
            descripcion,
            limite=palabras_disponibles
        )

        diapositivas.append({
            "numero": len(diapositivas) + 1,
            "tipo": "contenido",
            "titulo": titulo,
            "texto": texto_resumido,
            "fuente": descripcion
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
    """Construye un post de LinkedIn respetando 1300 caracteres
    y evitando cortar párrafos o recomendaciones a la mitad.
    """

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

    separador = "\n\n"
    limite = 1300

    espacio_desarrollo = (
        limite
        - len(gancho)
        - len(llamado_accion)
        - len(enlace_utm)
        - len(separador) * 3
    )

    if espacio_desarrollo < 1:
        raise ValueError(
            "El gancho, llamado a la acción y enlace UTM "
            "superan el límite permitido."
        )

    bloques = [
        bloque.strip()
        for bloque in desarrollo.split(separador)
        if bloque.strip()
    ]

    bloques_finales = []
    indice = 0

    while indice < len(bloques):
        bloque = bloques[indice]

        # Agrupa el encabezado con sus recomendaciones.
        if (
            bloque.endswith(":")
            and indice + 1 < len(bloques)
            and bloques[indice + 1].startswith("• ")
        ):
            encabezado = bloque
            recomendaciones = []
            siguiente = indice + 1

            while (
                siguiente < len(bloques)
                and bloques[siguiente].startswith("• ")
            ):
                recomendacion = bloques[siguiente]

                candidato = "\n\n".join(
                    bloques_finales
                    + [encabezado]
                    + recomendaciones
                    + [recomendacion]
                )

                if len(candidato) > espacio_desarrollo:
                    break

                recomendaciones.append(recomendacion)
                siguiente += 1

            if recomendaciones:
                bloques_finales.append(encabezado)
                bloques_finales.extend(recomendaciones)

            indice = siguiente if recomendaciones else indice + 1
            continue

        candidato = "\n\n".join(
            bloques_finales + [bloque]
        )

        if len(candidato) > espacio_desarrollo:
            break

        bloques_finales.append(bloque)
        indice += 1

    desarrollo_final = "\n\n".join(bloques_finales)

    if not desarrollo_final:
        raise ValueError(
            "No hay espacio suficiente para incluir un desarrollo completo."
        )

    texto = separador.join([
        gancho,
        desarrollo_final,
        llamado_accion,
        enlace_utm
    ])

    if len(texto) > limite:
        raise ValueError(
            "El post supera el límite de 1300 caracteres."
        )

    return {
        "formato": "post_linkedin",
        "gancho": gancho,
        "desarrollo": desarrollo_final,
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
    """Construye el desarrollo con información disponible de la fuente."""

    if not seccion:
        raise ValueError(
            "No existe una sección principal para generar el post."
        )

    if not isinstance(max_recomendaciones, int) or max_recomendaciones < 0:
        raise ValueError(
            "El máximo de recomendaciones debe ser un entero no negativo."
        )

    parrafos = [
        " ".join(texto.split())
        for texto in seccion.get("parrafos", [])
        if isinstance(texto, str)
        and texto.strip()
        and "te podría interesar" not in texto.lower()
    ]

    listas = [
        " ".join(texto.split())
        for texto in seccion.get("listas", [])
        if isinstance(texto, str) and texto.strip()
    ]

    if not parrafos and not listas:
        raise ValueError(
            "La sección no contiene información suficiente para el post."
        )

    parrafos_unicos = list(dict.fromkeys(parrafos))
    listas_unicas = list(dict.fromkeys(listas))

    partes = []

    partes.extend(parrafos_unicos[:2])

    if listas_unicas and max_recomendaciones > 0:
        partes.append("Recomendaciones clave:")

        partes.extend(
            f"• {recomendacion}"
            for recomendacion in listas_unicas[:max_recomendaciones]
        )

    elif len(parrafos_unicos) > 2:
        partes.append("Otros aspectos del contenido:")

        partes.extend(
            parrafos_unicos[2:2 + max_recomendaciones]
        )

    return "\n\n".join(partes)



def generar_gancho_post(seccion):
    """Genera un gancho natural basado en el título de la fuente."""

    if not seccion:
        raise ValueError(
            "Se necesita una sección para generar el gancho."
        )

    titulo = seccion.get("titulo", "").strip()

    if not titulo:
        raise ValueError(
            "La sección necesita un título."
        )

    titulo = titulo.rstrip(" .!?")

    return (
        f"¿Quieres conocer las claves de {titulo}? "
        "Descubre sus aspectos más importantes y recomendaciones."
    )


def generar_llamado_accion(titulo):
    """Genera una invitación relacionada con el contenido."""

    if not isinstance(titulo, str) or not titulo.strip():
        raise ValueError(
            "Se necesita un título para generar el llamado."
        )

    titulo = titulo.strip().rstrip(" .!?")

    return (
        f"¿Quieres conocer más sobre {titulo}? "
        "Consulta el contenido completo y descubre sus recomendaciones."
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

    llamado_accion = generar_llamado_accion(titulo_referencia)

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
