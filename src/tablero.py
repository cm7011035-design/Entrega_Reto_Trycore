
import csv
import json

from pathlib import Path
from html import escape
from datetime import timedelta

from src.calendario import cargar_ventana


def agrupar_publicaciones_por_fecha(calendario):
    """Agrupa las publicaciones por fecha y las ordena por hora."""

    publicaciones_por_fecha = {}

    publicaciones_ordenadas = sorted(
        calendario,
        key=lambda elemento: (
            elemento.get("fecha", ""),
            elemento.get("hora", "")
        )
    )

    for publicacion in publicaciones_ordenadas:
        fecha = publicacion.get("fecha", "")

        if fecha not in publicaciones_por_fecha:
            publicaciones_por_fecha[fecha] = []

        publicaciones_por_fecha[fecha].append(publicacion)

    return publicaciones_por_fecha


def cargar_datos_tablero():
    """Carga el calendario y el resumen de la automatización."""

    ruta_calendario = Path("salidas/calendario.csv")
    ruta_resumen = Path("salidas/resumen.json")

    with ruta_calendario.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as archivo:
        calendario = list(csv.DictReader(archivo))

    resumen = json.loads(
        ruta_resumen.read_text(encoding="utf-8")
    )

    return calendario, resumen


def generar_seccion_alertas(resumen):
    """Muestra las alertas detectadas durante el diagnóstico."""

    diagnostico = resumen.get("diagnostico", {})
    alertas = diagnostico.get("alertas", [])
    cifras = diagnostico.get("cifras", [])

    cifras_revision = [
        cifra for cifra in cifras
        if cifra.get("requiere_revision")
    ]

    if not alertas and not cifras_revision:
        return ""

    elementos = ""

    for alerta in alertas:
        elementos += f"<li>{escape(str(alerta))}</li>"

    for cifra in cifras_revision:
        valor = escape(str(cifra.get("valor", "Sin valor")))
        contexto = escape(
            str(cifra.get("contexto", "Sin contexto"))
        )

        elementos += f"""
        <li>
            <strong>Cifra por verificar: {valor}</strong>
            <p>{contexto}</p>
        </li>
        """

    return f"""
    <section>
        <h2>Alertas del diagnóstico</h2>

        <div class="aviso-humano">
            <strong>Revisión de contenido necesaria</strong>

            <ul>
                {elementos}
            </ul>
        </div>
    </section>
    """


def generar_tarjetas_puntuacion(resumen):
    """Genera tarjetas con puntuaciones históricas."""

    puntuaciones = resumen.get("puntuaciones", {})

    tarjetas = ""

    if not puntuaciones:
        return "<p>No hay puntuaciones disponibles.</p>"

    for formato, datos in puntuaciones.items():

        if datos is None or datos.get("puntuacion") is None:
            puntuacion = "Sin datos históricos"
            evidencia = (
                datos.get(
                    "explicacion",
                    "Sin evidencia histórica"
                )
                if datos else "Sin evidencia histórica"
            )
            fuente = ""
        else:
            puntuacion = f"{datos['puntuacion']:.2f}/100"
            evidencia = datos.get(
                "nivel_evidencia",
                "No definida"
            )
            fuente = datos.get(
                "fuente_puntuacion",
                "No especificada"
            )

        tarjetas += f"""
        <article class="tarjeta-puntuacion">
            <h3>{escape(str(formato))}</h3>

            <p class="puntuacion">
                {escape(str(puntuacion))}
            </p>

            <p class="evidencia">
                Evidencia: {escape(str(evidencia))}
            </p>

            <p class="evidencia">
                Base: {escape(str(fuente))}
            </p>
        </article>
        """

    return tarjetas




def generar_vista_dos_semanas(
    calendario,
    puntuaciones=None,
    tema_puntuacion=None
):
    """Genera la vista de dos semanas con puntuaciones aplicables."""

    grupos = agrupar_publicaciones_por_fecha(calendario)
    puntuaciones = puntuaciones or {}

    ventana = cargar_ventana()

    fecha_actual = ventana["inicio"]
    fecha_final = ventana["fin"]

    vista = ""

    nombres_dias = [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo"
    ]

    clases = {
        "post_linkedin": "formato-post",
        "carrusel_linkedin": "formato-carrusel",
        "newsletter": "formato-newsletter",
        "guion_video_corto": "formato-video",
        "infografia": "formato-infografia",
        "caso_de_exito": "formato-caso"
    }

    while fecha_actual <= fecha_final:

        fecha = fecha_actual.strftime("%Y-%m-%d")
        nombre_dia = nombres_dias[fecha_actual.weekday()]

        publicaciones = grupos.get(fecha, [])

        tarjetas = ""

        for publicacion in publicaciones:

            formato = publicacion.get("formato", "")
            tema = publicacion.get("tema", "")

            clase = clases.get(
                formato,
                "formato-otro"
            )

            titulo = escape(
                str(publicacion.get("titulo", "Sin título"))
            )

            tema_html = escape(
                str(tema or "No definido")
            )

            hora = escape(
                str(publicacion.get("hora", "Sin hora"))
            )

            es_tema_evaluado = (
                tema_puntuacion is not None
                and tema == tema_puntuacion
            )

            datos_puntuacion = (
                puntuaciones.get(formato)
                if es_tema_evaluado
                else None
            )

            if (
                datos_puntuacion
                and datos_puntuacion.get("puntuacion") is not None
            ):
                valor = float(
                    datos_puntuacion["puntuacion"]
                )

                puntuacion_html = (
                    f"<p class='puntuacion-publicacion'>"
                    f"Referencia histórica del formato: "
                    f"{valor:.2f}/100"
                    f"</p>"
                )

                fuente = datos_puntuacion.get(
                    "fuente_puntuacion",
                    "No especificada"
                )

                fuente_html = (
                    f"<small>Base: {escape(str(fuente))}</small>"
                )

            else:
                puntuacion_html = (
                    "<p class='puntuacion-publicacion'>"
                    "Sin puntuación individual disponible"
                    "</p>"
                )

                fuente_html = ""

            tarjetas += f"""
            <article class="publicacion {clase}">
                <strong class="hora">{hora}</strong>

                <h4>{escape(str(formato))}</h4>

                <p>{titulo}</p>

                <small>Tema: {tema_html}</small>

                {puntuacion_html}

                {fuente_html}

                <p class="revision">
                    Pendiente de revisión humana
                </p>
            </article>
            """

        if not tarjetas:
            tarjetas = """
            <p class="dia-vacio">
                Sin publicaciones programadas
            </p>
            """

        vista += f"""
        <div class="dia-calendario">
            <div class="encabezado-dia">
                <h3>{escape(nombre_dia)}</h3>
                <small>{escape(fecha)}</small>
            </div>

            <div class="publicaciones-dia">
                {tarjetas}
            </div>
        </div>
        """

        fecha_actual += timedelta(days=1)

    return vista


def generar_filas_calendario(calendario):
    """Genera las filas ordenadas de publicaciones."""

    filas = ""

    publicaciones_ordenadas = sorted(
        calendario,
        key=lambda elemento: (
            elemento.get("fecha", ""),
            elemento.get("hora", "")
        )
    )

    for publicacion in publicaciones_ordenadas:

        fecha = escape(str(publicacion.get("fecha", "")))
        hora = escape(str(publicacion.get("hora", "")))
        canal = escape(str(publicacion.get("canal", "")))
        formato = escape(str(publicacion.get("formato", "")))
        tema = escape(str(publicacion.get("tema", "")))
        titulo = escape(str(publicacion.get("titulo", "")))
        estado = escape(str(publicacion.get("estado", "")))

        filas += f"""
        <tr>
            <td>{fecha}</td>
            <td>{hora}</td>
            <td>{canal}</td>
            <td>{formato}</td>
            <td>{tema}</td>
            <td>{titulo}</td>
            <td>
                <span class="estado">{estado}</span>
            </td>
        </tr>
        """

    return filas


def generar_seccion_pendientes(resumen):
    """Muestra rechazos de validación y publicaciones sin horario."""

    pendientes = resumen.get(
        "publicaciones_sin_programar",
        resumen.get("sin_programar", [])
    )

    if not pendientes:
        return """
        <section>
            <h2>Publicaciones pendientes y conflictos</h2>

            <p>
                No hay publicaciones rechazadas ni pendientes
                de programación.
            </p>
        </section>
        """

    filas = ""

    rechazadas = 0
    sin_horario = 0

    for publicacion in pendientes:

        titulo = escape(
            str(publicacion.get("titulo", "Sin título"))
        )

        formato = escape(
            str(publicacion.get("formato", "No definido"))
        )

        tema = escape(
            str(publicacion.get("tema", "No definido"))
        )

        estado = publicacion.get("estado", "")

        if estado == "rechazada_por_validacion":
            tipo = "Rechazada por validación"
            rechazadas += 1
        else:
            tipo = "Sin horario disponible"
            sin_horario += 1

        tipo = escape(tipo)

        motivo = escape(
            str(publicacion.get("motivo", "Requiere revisión"))
        )

        filas += f"""
        <tr>
            <td>{titulo}</td>
            <td>{formato}</td>
            <td>{tema}</td>
            <td>{tipo}</td>
            <td>{motivo}</td>
        </tr>
        """

    return f"""
    <section>
        <h2>Publicaciones pendientes y conflictos</h2>

        <p>
            Rechazadas por validación: <strong>{rechazadas}</strong>
        </p>

        <p>
            Sin horario disponible: <strong>{sin_horario}</strong>
        </p>

        <div class="tabla-contenedor">
            <table>
                <thead>
                    <tr>
                        <th>Título</th>
                        <th>Formato</th>
                        <th>Tema</th>
                        <th>Tipo de incidencia</th>
                        <th>Motivo</th>
                    </tr>
                </thead>

                <tbody>
                    {filas}
                </tbody>
            </table>
        </div>
    </section>
    """


def generar_tablero():
    """Construye el tablero visual de automatización."""

    calendario, resumen = cargar_datos_tablero()

    seccion_pendientes = generar_seccion_pendientes(resumen)

    seccion_alertas = generar_seccion_alertas(resumen)

    tarjetas = generar_tarjetas_puntuacion(resumen)

    filas = generar_filas_calendario(calendario)

    vista_calendario = generar_vista_dos_semanas(
    calendario,
    resumen.get("puntuaciones", {}),
    resumen.get("tema_detectado")
)

    historial = resumen.get("analisis_historico", {})

    total_unicos = historial.get("total_unicos", 0)
    total_duplicados = historial.get("total_duplicados", 0)

    html = f"""
    <!DOCTYPE html>
    <html lang="es">

    <head>
        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <title>Trycore | Tablero de Mercadeo</title>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                font-family: Arial, sans-serif;
                background: #f3f6fa;
                color: #263445;
                margin: 0;
                padding: 30px;
            }}

            .contenedor {{
                max-width: 1450px;
                margin: auto;
            }}

            h1 {{
                color: #174a7e;
                margin-bottom: 8px;
            }}

            h2 {{
                color: #174a7e;
                margin-top: 0;
            }}

            section {{
                background: white;
                padding: 22px;
                margin: 20px 0;
                border-radius: 10px;
                box-shadow: 0 2px 8px #00000010;
            }}

            .descripcion {{
                color: #64748b;
                margin-bottom: 24px;
            }}

            .aviso-humano {{
                background: #fff8e6;
                border-left: 5px solid #d69e2e;
                padding: 16px 20px;
                border-radius: 6px;
                margin: 20px 0;
            }}

            .aviso-humano strong {{
                color: #805b13;
            }}

            .indicadores {{
                display: grid;
                grid-template-columns: repeat(
                    auto-fit,
                    minmax(200px, 1fr)
                );
                gap: 15px;
            }}

            .indicador {{
                background: #f7f9fc;
                border: 1px solid #e1e6ed;
                padding: 18px;
                border-radius: 8px;
            }}

            .indicador strong {{
                display: block;
                font-size: 27px;
                color: #174a7e;
                margin-top: 8px;
            }}

            .tarjetas-puntuacion {{
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
            }}

            .tarjeta-puntuacion {{
                background: #f7f9fc;
                border: 1px solid #e1e6ed;
                padding: 18px;
                border-radius: 8px;
                min-width: 220px;
                flex: 1;
            }}

            .tarjeta-puntuacion h3 {{
                overflow-wrap: anywhere;
            }}

            .puntuacion {{
                font-size: 28px;
                font-weight: bold;
                color: #174a7e;
                margin: 10px 0;
            }}

            .evidencia {{
                color: #64748b;
                font-size: 13px;
            }}

            .nota-puntuacion {{
                color: #64748b;
                font-size: 13px;
                margin-top: 15px;
            }}

            .calendario-dos-semanas {{
                display: grid;
                grid-template-columns: repeat(
                    auto-fit,
                    minmax(240px, 1fr)
                );
                gap: 15px;
            }}

            .dia-calendario {{
                background: #f7f9fc;
                border: 1px solid #e1e6ed;
                border-radius: 8px;
                padding: 15px;
                min-width: 0;
            }}

            .encabezado-dia {{
                border-bottom: 1px solid #dce4ed;
                padding-bottom: 10px;
                margin-bottom: 12px;
            }}

            .encabezado-dia h3 {{
                color: #174a7e;
                margin: 0 0 5px;
            }}

            .encabezado-dia small {{
                color: #64748b;
            }}

            .publicacion {{
                background: white;
                border-left: 5px solid #64748b;
                border-radius: 6px;
                padding: 12px;
                margin-bottom: 10px;
                overflow-wrap: anywhere;
            }}

            .publicacion h4 {{
                margin: 8px 0;
            }}

            .hora {{
                color: #174a7e;
                font-size: 13px;
            }}

            .puntuacion-publicacion {{
                color: #174a7e;
                font-weight: bold;
                font-size: 13px;
                margin-bottom: 5px;
            }}

            .publicacion small {{
                color: #64748b;
            }}

            .formato-post {{
                border-left-color: #2563eb;
            }}

            .formato-carrusel {{
                border-left-color: #7c3aed;
            }}

            .formato-newsletter {{
                border-left-color: #059669;
            }}

            .formato-video {{
                border-left-color: #d97706;
            }}

            .formato-infografia {{
                border-left-color: #0891b2;
            }}

            .formato-caso {{
                border-left-color: #64748b;
            }}

            .formato-otro {{
                border-left-color: #94a3b8;
            }}

            .revision {{
                color: #9a6700;
                font-size: 12px;
                font-weight: bold;
                margin-bottom: 0;
            }}

            .dia-vacio {{
                color: #94a3b8;
                font-size: 13px;
                padding: 10px 0;
            }}

            .leyenda {{
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                margin: 15px 0 20px;
                font-size: 13px;
                color: #475569;
            }}

            .leyenda span {{
                display: flex;
                align-items: center;
                gap: 6px;
            }}

            .color-leyenda {{
                width: 12px;
                height: 12px;
                display: inline-block;
                border-radius: 3px;
            }}

            .tabla-contenedor {{
                width: 100%;
                overflow-x: auto;
            }}

            table {{
                width: 100%;
                min-width: 750px;
                border-collapse: collapse;
                background: white;
            }}

            th, td {{
                padding: 12px;
                border-bottom: 1px solid #e1e6ed;
                text-align: left;
            }}

            th {{
                background: #174a7e;
                color: white;
            }}

            tr:nth-child(even) {{
                background: #f7f9fc;
            }}

            .estado {{
                display: inline-block;
                background: #e3f5e9;
                color: #246b3b;
                padding: 5px 9px;
                border-radius: 12px;
                font-size: 12px;
            }}

            footer {{
                text-align: center;
                color: #94a3b8;
                font-size: 12px;
                padding: 20px;
            }}

            @media (max-width: 600px) {{

                body {{
                    padding: 14px;
                }}

                section {{
                    padding: 16px;
                }}

                h1 {{
                    font-size: 23px;
                }}

            }}

        </style>

    </head>

    <body>

        <main class="contenedor">

            <h1>Tablero de automatización de mercadeo</h1>

            <p class="descripcion">
                Panel de seguimiento de publicaciones de Trycore.
            </p>

            <div class="aviso-humano">

                <strong>Revisión humana obligatoria</strong>

                <p>
                    Las publicaciones generadas deben revisarse y
                    aprobarse antes de su publicación.
                    Estar programada en este calendario no significa
                    que haya sido publicada o aprobada.
                </p>

            </div>

            <section>

                <h2>Indicadores históricos</h2>

                <div class="indicadores">

                    <article class="indicador">
                        Publicaciones únicas
                        <strong>{total_unicos}</strong>
                    </article>

                    <article class="indicador">
                        Duplicados detectados
                        <strong>{total_duplicados}</strong>
                    </article>

                </div>

            </section>

            <section>

                <h2>Puntuaciones por formato</h2>

                <div class="tarjetas-puntuacion">
                    {tarjetas}
                </div>

                <p class="nota-puntuacion">
                    Las puntuaciones son indicadores relativos basados
                    en las medianas del historial. No representan
                    probabilidades de éxito ni garantizan resultados.
                </p>

            </section>

            {seccion_alertas}

            {seccion_pendientes}

            <section>

                <h2>Calendario de publicaciones</h2>

                <p>
                    Vista de las dos semanas de programación.
                </p>

                <div class="leyenda">

                    <span>
                        <i class="color-leyenda"
                           style="background:#2563eb"></i>
                        Post LinkedIn
                    </span>

                    <span>
                        <i class="color-leyenda"
                           style="background:#7c3aed"></i>
                        Carrusel
                    </span>

                    <span>
                        <i class="color-leyenda"
                           style="background:#059669"></i>
                        Newsletter
                    </span>

                    <span>
                        <i class="color-leyenda"
                           style="background:#d97706"></i>
                        Video
                    </span>

                    <span>
                        <i class="color-leyenda"
                           style="background:#0891b2"></i>
                        Infografía
                    </span>

                </div>

                <div class="calendario-dos-semanas">
                    {vista_calendario}
                </div>

            </section>

            <section>

                <h2>Detalle de publicaciones</h2>

                <div class="tabla-contenedor">

                    <table>

                        <thead>
                            <tr>
                                <th>Fecha</th>
                                <th>Hora</th>
                                <th>Canal</th>
                                <th>Formato</th>
                                <th>Tema</th>
                                <th>Título</th>
                                <th>Estado</th>
                            </tr>
                        </thead>

                        <tbody>
                            {filas}
                        </tbody>

                    </table>

                </div>

            </section>

            <footer>
                Trycore | Tablero de automatización de mercadeo
            </footer>

        </main>

    </body>

    </html>
    """

    return html


def guardar_tablero():
    """Genera y guarda el tablero HTML."""

    contenido = generar_tablero()

    contenido = "\n".join(
        linea.rstrip()
        for linea in contenido.splitlines()
    ) + "\n"

    ruta_salida = Path("salidas/tablero.html")

    ruta_salida.write_text(
        contenido,
        encoding="utf-8"
    )

    return ruta_salida
