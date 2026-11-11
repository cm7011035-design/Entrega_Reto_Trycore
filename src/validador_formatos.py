import re
from src.validador import validar_contenido


def obtener_reglas_formato(formato_id, configuracion):
    """
    Busca las reglas de un formato dentro de la configuración.
    """

    matriz = configuracion["matriz_formatos"]

    for formato in matriz:
        if formato["id"] == formato_id:
            return formato

    raise ValueError(
        f"El formato '{formato_id}' no existe en la configuración."
    )


def contar_palabras(texto):
    """
    Cuenta las palabras de un texto, incluyendo palabras con tildes.
    """

    patron = r"\b[\wáéíóúÁÉÍÓÚñÑüÜ]+\b"

    palabras = re.findall(patron, texto)

    return len(palabras)


def validar_longitud(texto, reglas):
    """
    Comprueba si el contenido cumple los límites de extensión.
    """

    longitud = reglas.get("longitud")

    if longitud:
        cantidad = len(texto)

        minimo = longitud.get("min_caracteres")
        maximo = longitud.get("max_caracteres")

        if minimo is not None and cantidad < minimo:
            return {
                "valido": False,
                "mensaje": (
                    f"El contenido tiene {cantidad} caracteres. "
                    f"El mínimo permitido es {minimo}."
                )
            }

        if maximo is not None and cantidad > maximo:
            return {
                "valido": False,
                "mensaje": (
                    f"El contenido tiene {cantidad} caracteres. "
                    f"El máximo permitido es {maximo}."
                )
            }

        minimo = longitud.get("min_palabras")
        maximo = longitud.get("max_palabras")

        if minimo is not None or maximo is not None:
            cantidad = contar_palabras(texto)

            if minimo is not None and cantidad < minimo:
                return {
                    "valido": False,
                    "mensaje": (
                        f"El contenido tiene {cantidad} palabras. "
                        f"El mínimo permitido es {minimo}."
                    )
                }

            if maximo is not None and cantidad > maximo:
                return {
                    "valido": False,
                    "mensaje": (
                        f"El contenido tiene {cantidad} palabras. "
                        f"El máximo permitido es {maximo}."
                    )
                }

    return {
        "valido": True,
        "mensaje": "La extensión cumple las reglas del formato."
    }

def validar_gancho(gancho, reglas):
    """
    Comprueba que el gancho no supere el límite configurado.
    """

    maximo = reglas.get("gancho_max_caracteres")

    if maximo is None:
        return {
            "valido": True,
            "mensaje": "Este formato no tiene límite de gancho configurado."
        }

    cantidad = len(gancho.strip())

    if cantidad > maximo:
        return {
            "valido": False,
            "mensaje": (
                f"El gancho tiene {cantidad} caracteres. "
                f"El máximo permitido es {maximo}."
            )
        }

    if cantidad == 0:
        return {
            "valido": False,
            "mensaje": "El gancho no puede estar vacío."
        }

    return {
        "valido": True,
        "mensaje": "El gancho cumple el límite de caracteres."
    }


def validar_cantidad_elementos(elementos, reglas, clave):
    """
    Comprueba la cantidad de elementos permitidos
    para carruseles e infografías.
    """

    configuracion = reglas.get(clave)

    if not configuracion:
        return {
            "valido": False,
            "mensaje": f"No existen reglas para '{clave}'."
        }

    cantidad = len(elementos)
    minimo = configuracion["min"]
    maximo = configuracion["max"]

    if cantidad < minimo:
        return {
            "valido": False,
            "mensaje": (
                f"Hay {cantidad} elementos. "
                f"El mínimo permitido es {minimo}."
            )
        }

    if cantidad > maximo:
        return {
            "valido": False,
            "mensaje": (
                f"Hay {cantidad} elementos. "
                f"El máximo permitido es {maximo}."
            )
        }

    return {
        "valido": True,
        "mensaje": "La cantidad de elementos cumple las reglas."
    }

def validar_palabras_por_elemento(elementos, reglas, clave):
    """
    Comprueba que ningún elemento supere el máximo
    de palabras permitido.
    """

    maximo = reglas.get(clave)

    if maximo is None:
        return {
            "valido": False,
            "mensaje": f"No existe el límite configurado: {clave}."
        }

    errores = []

    for numero, elemento in enumerate(elementos, start=1):
        cantidad = contar_palabras(elemento)

        if cantidad > maximo:
            errores.append(
                f"El elemento {numero} tiene {cantidad} palabras. "
                f"El máximo permitido es {maximo}."
            )

    return {
        "valido": len(errores) == 0,
        "mensaje": (
            "Todos los elementos cumplen el límite de palabras."
            if not errores
            else " | ".join(errores)
        )
    }

def validar_asunto(asunto, reglas):
    """
    Comprueba que el asunto del newsletter cumpla
    el límite de caracteres configurado.
    """

    maximo = reglas.get("asunto_max_caracteres")

    if maximo is None:
        return {
            "valido": False,
            "mensaje": "No existe un límite configurado para el asunto."
        }

    cantidad = len(asunto.strip())

    if cantidad == 0:
        return {
            "valido": False,
            "mensaje": "El asunto no puede estar vacío."
        }

    if cantidad > maximo:
        return {
            "valido": False,
            "mensaje": (
                f"El asunto tiene {cantidad} caracteres. "
                f"El máximo permitido es {maximo}."
            )
        }

    return {
        "valido": True,
        "mensaje": "El asunto cumple el límite de caracteres."
    }



def validar_secciones(secciones, minimo=3):
    """
    Comprueba que existan al menos tres secciones
    y que ninguna esté vacía.
    """

    if not isinstance(secciones, list):
        return {
            "valido": False,
            "mensaje": "Las secciones deben entregarse en una lista."
        }

    secciones_validas = [
        seccion
        for seccion in secciones
        if isinstance(seccion, str) and seccion.strip()
    ]

    if len(secciones_validas) < minimo:
        return {
            "valido": False,
            "mensaje": (
                f"Hay {len(secciones_validas)} secciones desarrolladas. "
                f"Se requieren al menos {minimo}."
            )
        }

    return {
        "valido": True,
        "mensaje": "El newsletter tiene al menos tres secciones desarrolladas."
    }


def validar_duracion_video(duracion, reglas):
    """
    Comprueba que la duración del video esté
    dentro del rango configurado.
    """

    limites = reglas.get("duracion_segundos")

    if not limites:
        return {
            "valido": False,
            "mensaje": "No hay límites de duración configurados."
        }

    minimo = limites["min"]
    maximo = limites["max"]

    if not isinstance(duracion, (int, float)) or isinstance(duracion, bool):
        return {
            "valido": False,
            "mensaje": "La duración debe ser un número."
        }

    if duracion < minimo:
        return {
            "valido": False,
            "mensaje": (
                f"El video dura {duracion} segundos. "
                f"El mínimo permitido es {minimo}."
            )
        }

    if duracion > maximo:
        return {
            "valido": False,
            "mensaje": (
                f"El video dura {duracion} segundos. "
                f"El máximo permitido es {maximo}."
            )
        }

    return {
        "valido": True,
        "mensaje": "La duración del video cumple las reglas."
    }


def validar_rango_palabras(texto, reglas):
    """
    Comprueba que un texto cumpla el rango de palabras
    definido en la configuración.
    """

    minimo = reglas["min"]
    maximo = reglas["max"]

    cantidad = contar_palabras(texto)

    if cantidad < minimo:
        return {
            "valido": False,
            "mensaje": (
                f"El contenido tiene {cantidad} palabras. "
                f"El mínimo permitido es {minimo}."
            )
        }

    if cantidad > maximo:
        return {
            "valido": False,
            "mensaje": (
                f"El contenido tiene {cantidad} palabras. "
                f"El máximo permitido es {maximo}."
            )
        }

    return {
        "valido": True,
        "mensaje": "La cantidad de palabras cumple las reglas."
    }


def validar_requisitos_caso_exito(
    cliente,
    testimonio,
    nombre,
    cargo,
    resultados_medibles
):
    """
    Comprueba que existan los datos necesarios para
    elaborar un caso de éxito.
    """

    faltantes = []

    if not cliente or not cliente.strip():
        faltantes.append("No se ha identificado al cliente.")

    if not testimonio or not testimonio.strip():
        faltantes.append("Falta el testimonio del cliente.")

    if not nombre or not nombre.strip():
        faltantes.append("Falta el nombre de quien da el testimonio.")

    if not cargo or not cargo.strip():
        faltantes.append("Falta el cargo de quien da el testimonio.")

    if not resultados_medibles:
        faltantes.append("No hay resultados medibles del cliente.")

    if faltantes:
        return {
            "valido": False,
            "requiere_revision_humana": True,
            "faltantes": faltantes
        }

    return {
        "valido": True,
        "requiere_revision_humana": True,
        "mensaje": (
            "Los campos obligatorios están presentes. "
            "Se debe verificar la autenticidad del testimonio "
            "y el respaldo de los resultados."
        )
    }


def validar_formato(formato_id, contenido, configuracion):
    """
    Coordina las validaciones según el formato recibido.
    """

    reglas = obtener_reglas_formato(formato_id, configuracion)
    resultados = []
    def recopilar_textos(valor):
        textos = []

        if isinstance(valor, str):
            if valor.strip():
                textos.append(valor)

        elif isinstance(valor, dict):
            for elemento in valor.values():
                textos.extend(recopilar_textos(elemento))

        elif isinstance(valor, (list, tuple)):
            for elemento in valor:
                textos.extend(recopilar_textos(elemento))

        return textos

    textos_generales = recopilar_textos(contenido)
    texto_general = " ".join(textos_generales)

    if texto_general.strip():
        resultado_general = validar_contenido(
            texto_general,
            configuracion
        )

        resultados.append({
            "validacion": "reglas_generales",
            "valido": resultado_general["valido"],
            "mensaje": (
                "El contenido cumple las reglas generales."
                if resultado_general["valido"]
                else " | ".join(resultado_general["alertas"])
            )
        })

    def agregar_resultado(nombre, resultado):
        resultados.append({
            "validacion": nombre,
            **resultado
        })

    if formato_id == "post_linkedin":
        texto = contenido.get("texto", "")
        gancho = contenido.get("gancho", "")

        agregar_resultado(
            "longitud",
            validar_longitud(texto, reglas)
        )

        agregar_resultado(
            "gancho",
            validar_gancho(gancho, reglas)
        )

    elif formato_id == "carrusel_linkedin":
        laminas = contenido.get("laminas", [])

        agregar_resultado(
            "cantidad_laminas",
            validar_cantidad_elementos(
                laminas, reglas, "laminas"
            )
        )

        agregar_resultado(
            "palabras_por_lamina",
            validar_palabras_por_elemento(
                laminas, reglas, "max_palabras_por_lamina"
            )
        )

    elif formato_id == "newsletter":
        texto = contenido.get("texto", "")
        asunto = contenido.get("asunto", "")
        secciones = contenido.get("secciones", [])

        agregar_resultado(
            "longitud",
            validar_longitud(texto, reglas)
        )

        agregar_resultado(
            "asunto",
            validar_asunto(asunto, reglas)
        )

        agregar_resultado(
            "secciones",
            validar_secciones(secciones)
        )

    elif formato_id == "guion_video_corto":
        texto = contenido.get("texto", "")
        duracion = contenido.get("duracion_segundos")

        agregar_resultado(
            "cantidad_palabras",
            validar_rango_palabras(
                texto, reglas["palabras"]
            )
        )

        if duracion is None:
            agregar_resultado(
                "duracion",
                {
                    "valido": False,
                    "mensaje": "No se indicó la duración del video."
                }
            )
        else:
            agregar_resultado(
                "duracion",
                validar_duracion_video(duracion, reglas)
            )

    elif formato_id == "caso_de_exito":
        texto = contenido.get("texto", "")

        agregar_resultado(
            "longitud",
            validar_longitud(texto, reglas)
        )

        agregar_resultado(
            "requisitos",
            validar_requisitos_caso_exito(
                contenido.get("cliente", ""),
                contenido.get("testimonio", ""),
                contenido.get("nombre", ""),
                contenido.get("cargo", ""),
                contenido.get("resultados_medibles", [])
            )
        )

    elif formato_id == "infografia":
        elementos = contenido.get("elementos", [])

        agregar_resultado(
            "cantidad_elementos",
            validar_cantidad_elementos(
                elementos, reglas, "elementos"
            )
        )

        agregar_resultado(
            "palabras_por_elemento",
            validar_palabras_por_elemento(
                elementos, reglas, "max_palabras_por_elemento"
            )
        )

    return {
        "formato": formato_id,
        "valido": all(
            resultado["valido"]
            for resultado in resultados
        ),
        "resultados": resultados,
        "requiere_revision_humana": True
    }

