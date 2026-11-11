import csv
import re

from datetime import datetime
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent

RUTA_HISTORIAL = (
    BASE_DIR
    / "02_insumos"
    / "historial"
    / "historial_publicaciones.csv"
)

def leer_historial():
    """Lee el historial original sin modificarlo."""

    if not RUTA_HISTORIAL.exists():
        raise FileNotFoundError(
            f"No se encontró el historial: {RUTA_HISTORIAL}"
        )

    with RUTA_HISTORIAL.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as archivo:

        lector = csv.DictReader(archivo)

        if not lector.fieldnames:
            raise ValueError(
                "El historial no contiene encabezados."
            )

        registros = list(lector)

    return registros

def normalizar_fecha(valor):
    """Convierte diferentes formatos de fecha a datetime."""

    if not valor or not valor.strip():
        return None

    formatos = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%b-%Y",
        "%d-%B-%Y",
    ]

    meses = {
        "ene": "Jan",
        "feb": "Feb",
        "mar": "Mar",
        "abr": "Apr",
        "may": "May",
        "jun": "Jun",
        "jul": "Jul",
        "ago": "Aug",
        "sep": "Sep",
        "oct": "Oct",
        "nov": "Nov",
        "dic": "Dec",
    }

    fecha_texto = valor.strip().lower()

    for espanol, ingles in meses.items():
        fecha_texto = re.sub(
            espanol,
            ingles,
            fecha_texto,
            flags=re.IGNORECASE
        )

    for formato in formatos:
        try:
            return datetime.strptime(
                fecha_texto,
                formato
            ).date()

        except ValueError:
            continue

    return None

def normalizar_numero(valor):
    """Convierte valores numéricos a float sin inventar datos."""

    if valor is None or not str(valor).strip():
        return None

    valor = str(valor).strip()

    valor = valor.replace(",", ".")

    try:
        return float(valor)

    except ValueError:
        return None

def eliminar_duplicados(registros):
    """Elimina registros repetidos usando el ID de publicación."""

    registros_unicos = []
    ids_encontrados = set()
    duplicados = []

    for registro in registros:
        identificador = registro.get(
            "id_publicacion", ""
        ).strip()

        if not identificador:
            duplicados.append(registro)
            continue

        if identificador in ids_encontrados:
            duplicados.append(registro)
            continue

        ids_encontrados.add(identificador)
        registros_unicos.append(registro)

    return registros_unicos, duplicados

def normalizar_registros(registros):
    """Normaliza fechas y métricas de las publicaciones."""

    campos_numericos = [
        "palabras",
        "impresiones",
        "reacciones",
        "comentarios",
        "clics",
        "tasa_interaccion",
    ]

    registros_normalizados = []

    for registro in registros:
        nuevo = registro.copy()

        nuevo["fecha_normalizada"] = normalizar_fecha(
            nuevo.get("fecha", "")
        )

        for campo in campos_numericos:
            nuevo[campo] = normalizar_numero(
                nuevo.get(campo, "")
            )

        registros_normalizados.append(nuevo)

    return registros_normalizados

def detectar_anomalias(registros):
    """Identifica registros con información incompleta o sospechosa."""

    anomalias = []

    for registro in registros:
        problemas = []

        if registro.get("fecha_normalizada") is None:
            problemas.append("Fecha vacía o inválida")

        for campo in [
            "impresiones",
            "reacciones",
            "comentarios",
            "clics",
        ]:
            valor = registro.get(campo)

            if valor is None:
                problemas.append(
                    f"Métrica faltante: {campo}"
                )

            elif valor < 0:
                problemas.append(
                    f"Métrica negativa: {campo}"
                )

        if problemas:
            anomalias.append({
                "id_publicacion": registro.get(
                    "id_publicacion", "SIN_ID"
                ),
                "problemas": problemas,
            })

    return anomalias

def detectar_valores_extremos(registros):
    """Marca publicaciones con impresiones muy superiores al promedio."""

    valores = [
        registro["impresiones"]
        for registro in registros
        if registro.get("impresiones") is not None
        and registro["impresiones"] >= 0
    ]

    if len(valores) < 3:
        return []

    promedio = sum(valores) / len(valores)

    extremos = []

    for registro in registros:
        impresiones = registro.get("impresiones")

        if impresiones is None:
            continue

        if impresiones > promedio * 3:
            extremos.append({
                "id_publicacion": registro.get(
                    "id_publicacion", "SIN_ID"
                ),
                "impresiones": impresiones,
                "promedio_historial": round(promedio, 2),
                "requiere_revision": True,
            })

    return extremos
def calcular_estadisticas_por_formato(registros):
    """Calcula el rendimiento histórico de cada formato."""

    grupos = defaultdict(list)

    for registro in registros:
        formato = registro.get("formato", "").strip()

        if not formato:
            continue

        grupos[formato].append(registro)

    estadisticas = []

    for formato, publicaciones in grupos.items():

        impresiones = [
            r["impresiones"]
            for r in publicaciones
            if r.get("impresiones") is not None
        ]

        reacciones = [
            r["reacciones"]
            for r in publicaciones
            if r.get("reacciones") is not None
        ]

        clics = [
            r["clics"]
            for r in publicaciones
            if r.get("clics") is not None
        ]

        estadisticas.append({
            "formato": formato,
            "publicaciones": len(publicaciones),
            "promedio_impresiones": (
                round(sum(impresiones) / len(impresiones), 2)
                if impresiones else None
            ),
            "promedio_reacciones": (
                round(sum(reacciones) / len(reacciones), 2)
                if reacciones else None
            ),
            "promedio_clics": (
                round(sum(clics) / len(clics), 2)
                if clics else None
            ),
        })

    return estadisticas

def calcular_estadisticas_por_tema(registros):
    """Calcula el rendimiento histórico de cada tema."""

    grupos = defaultdict(list)

    for registro in registros:
        tema = registro.get("tema", "").strip().lower()

        if not tema:
            continue

        grupos[tema].append(registro)

    estadisticas = []

    for tema, publicaciones in grupos.items():

        impresiones = [
            r["impresiones"]
            for r in publicaciones
            if r.get("impresiones") is not None
        ]

        reacciones = [
            r["reacciones"]
            for r in publicaciones
            if r.get("reacciones") is not None
        ]

        clics = [
            r["clics"]
            for r in publicaciones
            if r.get("clics") is not None
        ]

        estadisticas.append({
            "tema": tema,
            "publicaciones": len(publicaciones),
            "promedio_impresiones": (
                round(sum(impresiones) / len(impresiones), 2)
                if impresiones else None
            ),
            "promedio_reacciones": (
                round(sum(reacciones) / len(reacciones), 2)
                if reacciones else None
            ),
            "promedio_clics": (
                round(sum(clics) / len(clics), 2)
                if clics else None
            ),
        })

    return estadisticas

def analizar_historial():
    """Ejecuta el proceso completo de análisis del historial."""

    registros_originales = leer_historial()

    registros_unicos, duplicados = eliminar_duplicados(
        registros_originales
    )

    registros = normalizar_registros(registros_unicos)

    anomalias = detectar_anomalias(registros)

    valores_extremos = detectar_valores_extremos(registros)

    estadisticas_formatos = calcular_estadisticas_por_formato(
        registros
    )

    estadisticas_temas = calcular_estadisticas_por_tema(
        registros
    )

    medianas_temas = calcular_mediana_por_tema(
        registros
    )

    return {
        "total_originales": len(registros_originales),
        "total_unicos": len(registros),
        "total_duplicados": len(duplicados),
        "duplicados": duplicados,
        "anomalias": anomalias,
        "valores_extremos": valores_extremos,
        "estadisticas_formatos": estadisticas_formatos,
        "estadisticas_temas": estadisticas_temas,
        "medianas_temas": medianas_temas,
    }
def calcular_mediana(valores):
    """Calcula la mediana de una lista de valores numéricos."""

    valores_validos = sorted(
        valor
        for valor in valores
        if valor is not None
    )

    cantidad = len(valores_validos)

    if cantidad == 0:
        return None

    mitad = cantidad // 2

    if cantidad % 2 == 1:
        return round(valores_validos[mitad], 2)

    mediana = (
        valores_validos[mitad - 1]
        + valores_validos[mitad]
    ) / 2

    return round(mediana, 2)

def calcular_mediana_por_tema(registros):
    """Calcula medianas de métricas agrupadas por tema."""

    grupos = defaultdict(list)

    for registro in registros:
        tema = registro.get("tema", "").strip().lower()

        if tema:
            grupos[tema].append(registro)

    resultados = []

    for tema, publicaciones in grupos.items():

        impresiones = [
            r["impresiones"]
            for r in publicaciones
            if r.get("impresiones") is not None
        ]

        reacciones = [
            r["reacciones"]
            for r in publicaciones
            if r.get("reacciones") is not None
        ]

        clics = [
            r["clics"]
            for r in publicaciones
            if r.get("clics") is not None
        ]

        resultados.append({
            "tema": tema,
            "publicaciones": len(publicaciones),
            "mediana_impresiones": calcular_mediana(impresiones),
            "mediana_reacciones": calcular_mediana(reacciones),
            "mediana_clics": calcular_mediana(clics),
        })

    return resultados

