
import re
from collections import Counter


def contar_palabras(texto):
    """Cuenta las palabras del contenido."""

    return len(re.findall(r"\b[\wáéíóúÁÉÍÓÚñÑüÜ]+\b", texto))


def contar_oraciones(texto):
    """Cuenta las oraciones identificadas por su puntuación."""

    oraciones = re.split(r"[.!?]+", texto)
    return sum(1 for oracion in oraciones if oracion.strip())


def contar_parrafos(texto):
    """Cuenta los bloques de texto no vacíos."""

    parrafos = [
        linea.strip()
        for linea in texto.splitlines()
        if linea.strip()
    ]

    return len(parrafos)


def extraer_cifras(texto):
    """Identifica cifras relevantes y conserva su oración completa."""

    patron = (
        r"(?<!\w)"
        r"\d+(?:[.,]\d+)?"
        r"\s*(?:%|por ciento|años|meses|días|horas|"
        r"minutos|segundos|semanas|personas|empresas|"
        r"usuarios|procesos|tareas|pesos|dólares)?"
        r"(?!\w)"
    )

    resultados = []

    for coincidencia in re.finditer(
        patron,
        texto,
        flags=re.IGNORECASE
    ):
        cifra = coincidencia.group().strip()

        unidad = re.search(
            r"(?:%|por ciento|años|meses|días|horas|"
            r"minutos|segundos|semanas|personas|empresas|"
            r"usuarios|procesos|tareas|pesos|dólares)$",
            cifra,
            flags=re.IGNORECASE
        )

        # Evita números aislados que suelen ser metadatos.
        if not unidad:
            continue

        # Busca el inicio de la oración.
        delimitadores = ".!?\n"

        posiciones_inicio = [
            texto.rfind(signo, 0, coincidencia.start())
            for signo in delimitadores
        ]

        inicio = max(posiciones_inicio) + 1

        # Busca el final de la oración.
        siguiente_delimitador = re.search(
            r"[.!?\n]",
            texto[coincidencia.end():]
        )

        if siguiente_delimitador:
            fin = (
                coincidencia.end()
                + siguiente_delimitador.end()
            )
        else:
            fin = len(texto)

        contexto = texto[inicio:fin].strip()

        resultados.append({
            "valor": cifra,
            "contexto": contexto,
            "requiere_revision": True
        })

    return resultados


def detectar_temas(texto):
    """Identifica temas mediante palabras clave."""

    temas = {
        "automatizacion": [
            "automatización", "automatizar", "automático"
        ],
        "rpa": [
            "rpa", "robotic process automation", "bots"
        ],
        "productividad": [
            "productividad", "eficiencia", "tiempo"
        ],
        "procesos": [
            "procesos", "tareas", "operaciones"
        ],
        "tecnologia": [
            "tecnología", "software", "digital"
        ],
        "medicion": [
            "medir", "indicadores", "resultados", "roi"
        ]
    }

    texto_normalizado = texto.lower()
    encontrados = []

    for tema, palabras_clave in temas.items():
        cantidad = sum(
            texto_normalizado.count(palabra)
            for palabra in palabras_clave
        )

        if cantidad > 0:
            encontrados.append({
                "tema": tema,
                "menciones": cantidad
            })

    return sorted(
        encontrados,
        key=lambda elemento: elemento["menciones"],
        reverse=True
    )


def diagnosticar_contenido(texto):
    """Analiza una pieza madre y genera indicadores y alertas."""

    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("No hay contenido para diagnosticar.")

    palabras = contar_palabras(texto)
    caracteres = len(texto)
    parrafos = contar_parrafos(texto)
    oraciones = contar_oraciones(texto)
    cifras = extraer_cifras(texto)
    temas = detectar_temas(texto)

    alertas = []

    if palabras < 100:
        alertas.append(
            "El contenido tiene poca extensión para una reutilización amplia."
        )

    if not cifras:
        alertas.append(
            "No se identificaron cifras. No deben inventarse datos."
        )

    if any(cifra.get("requiere_revision") for cifra in cifras):
        alertas.append(
            "Se identificaron cifras que requieren verificación de su fuente."
        )

    if not temas:
        alertas.append(
            "No se identificaron temas mediante las palabras clave definidas."
        )

    if oraciones > 0 and palabras / oraciones > 35:
        alertas.append(
            "Se detectaron oraciones posiblemente demasiado extensas."
        )

    if parrafos < 3:
        alertas.append(
            "El contenido tiene poca división en párrafos."
        )

    return {
        "indicadores": {
            "palabras": palabras,
            "caracteres": caracteres,
            "parrafos": parrafos,
            "oraciones": oraciones,
            "cifras_identificadas": len(cifras),
        },
        "cifras": cifras,
        "temas": temas,
        "alertas": alertas,
    }
