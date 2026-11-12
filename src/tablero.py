
import csv
import json

from pathlib import Path
from html import escape
from datetime import timedelta

from src.calendario import cargar_ventana

def agrupar_publicaciones_por_fecha(calendario):
    """Agrupa las publicaciones según su fecha."""

    publicaciones_por_fecha = {}

    for publicacion in calendario:
        fecha = publicacion["fecha"]

        if fecha not in publicaciones_por_fecha:
            publicaciones_por_fecha[fecha] = []

        publicaciones_por_fecha[fecha].append(publicacion)

    return dict(sorted(publicaciones_por_fecha.items()))


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


def generar_tarjetas_puntuacion(resumen):
    """Genera las tarjetas con las puntuaciones históricas."""

    puntuaciones = resumen["puntuaciones"]

    tarjetas = ""

    for formato, datos in puntuaciones.items():

        if datos is None:
            puntuacion = "Sin datos"
            evidencia = "Sin evidencia histórica"

        else:
            puntuacion = f"{datos['puntuacion']:.2f}/100"
            evidencia = datos["nivel_evidencia"]

        tarjetas += f"""
        <article class="tarjeta-puntuacion">
            <h3>{escape(formato)}</h3>
            <p class="puntuacion">{escape(puntuacion)}</p>
            <p>{escape(evidencia)}</p>
        </article>
        """

    return tarjetas

def generar_vista_dos_semanas(calendario):
    """Genera una vista completa de los días de la ventana."""

    grupos = agrupar_publicaciones_por_fecha(calendario)

    ventana = cargar_ventana()

    fecha_actual = ventana["inicio"]
    fecha_final = ventana["fin"]

    vista = ""

    while fecha_actual <= fecha_final:

        fecha = fecha_actual.strftime("%Y-%m-%d")

        publicaciones = grupos.get(fecha, [])

        tarjetas = ""

        for publicacion in publicaciones:

            formato = publicacion["formato"]

            clases = {
                "post_linkedin": "formato-post",
                "carrusel_linkedin": "formato-carrusel",
                "newsletter": "formato-newsletter",
                "guion_video_corto": "formato-video",
                "infografia": "formato-infografia"
            }

            clase = clases.get(formato, "formato-otro")

            tarjetas += f"""
            <article class="publicacion {clase}">
                <strong>{escape(publicacion["hora"])}</strong>
                <h4>{escape(formato)}</h4>
                <p>{escape(publicacion["titulo"])}</p>
                <small>{escape(publicacion["tema"])}</small>
                <p class="revision">Pendiente de revisión humana</p>
            </article>
            """

        if not tarjetas:
            tarjetas = '<p class="dia-vacio">Sin publicaciones programadas</p>'

        vista += f"""
        <div class="dia-calendario">
            <h3>{escape(fecha)}</h3>
            <div class="publicaciones-dia">
                {tarjetas}
            </div>
        </div>
        """

        fecha_actual += timedelta(days=1)

    return vista
def generar_filas_calendario(calendario):
    """Genera las filas de publicaciones del calendario."""

    filas = ""

    for publicacion in calendario:

        fecha = escape(publicacion["fecha"])
        hora = escape(publicacion["hora"])
        canal = escape(publicacion["canal"])
        formato = escape(publicacion["formato"])
        tema = escape(publicacion["tema"])
        titulo = escape(publicacion["titulo"])
        estado = escape(publicacion["estado"])

        filas += f"""
        <tr>
            <td>{fecha}</td>
            <td>{hora}</td>
            <td>{canal}</td>
            <td>{formato}</td>
            <td>{tema}</td>
            <td>{titulo}</td>
            <td><span class="estado">{estado}</span></td>
        </tr>
        """

    return filas


def generar_seccion_pendientes(resumen):
    """Muestra las publicaciones que no pudieron programarse."""

    pendientes = resumen.get(
        "publicaciones_sin_programar",
        resumen.get("sin_programar", [])
    )

    if not pendientes:
        return """
        <section>
            <h2>Publicaciones pendientes y conflictos</h2>
            <p>No hay publicaciones sin programar.</p>
            <p>No se registran conflictos pendientes de resolver.</p>
        </section>
        """

    filas = ""

    for publicacion in pendientes:
        titulo = escape(str(publicacion.get("titulo", "Sin título")))
        formato = escape(str(publicacion.get("formato", "No definido")))
        tema = escape(str(publicacion.get("tema", "No definido")))
        motivo = escape(str(publicacion.get("motivo", "Requiere revisión")))

        filas += f"""
        <tr>
            <td>{titulo}</td>
            <td>{formato}</td>
            <td>{tema}</td>
            <td>{motivo}</td>
        </tr>
        """

    return f"""
    <section>
        <h2>Publicaciones pendientes y conflictos</h2>
        <p>Publicaciones que necesitan revisión antes de programarse.</p>
        <table>
            <thead>
                <tr>
                    <th>Título</th>
                    <th>Formato</th>
                    <th>Tema</th>
                    <th>Motivo</th>
                </tr>
            </thead>
            <tbody>
                {filas}
            </tbody>
        </table>
    </section>
    """

def generar_tablero():
    """Construye el tablero visual de automatización."""

    calendario, resumen = cargar_datos_tablero()

    seccion_pendientes = generar_seccion_pendientes(resumen)

    tarjetas = generar_tarjetas_puntuacion(resumen)

    filas = generar_filas_calendario(calendario)

    vista_calendario = generar_vista_dos_semanas(calendario)

    historial = resumen["analisis_historico"]

    total_unicos = historial["total_unicos"]
    total_duplicados = historial["total_duplicados"]

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Trycore | Tablero de Mercadeo</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f3f6fa;
                color: #263445;
                margin: 0;
                padding: 30px;
            }}

            h1 {{
                color: #174a7e;
            }}

            section {{
                background: white;
                padding: 22px;
                margin: 20px 0;
                border-radius: 10px;
                box-shadow: 0 2px 8px #00000010;
            }}

            .tarjeta-puntuacion {{
                display: inline-block;
                background: #eaf2fa;
                padding: 18px;
                margin: 8px;
                border-radius: 8px;
                min-width: 180px;
            }}

            .puntuacion {{
                font-size: 28px;
                font-weight: bold;
                color: #174a7e;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
            }}

            th, td {{
                padding: 12px;
                border-bottom: 1px solid #e1e6ed;
                text-align: left;
                white-space: nowrap;

            }}

            th {{
                background: #174a7e;
                color: white;
            }}

            tr:nth-child(even) {{
                background: #f7f9fc;
            }}

            .calendario-dos-semanas {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
            }}

            .dia-calendario {{
                background: #f7f9fc;
                border: 1px solid #e1e6ed;
                border-radius: 8px;
                padding: 15px;
            }}

            .dia-calendario h3 {{
                color: #174a7e;
                border-bottom: 1px solid #dce4ed;
                padding-bottom: 10px;
            }}

            .publicacion {{
                background: white;
                border-left: 5px solid #64748b;
                border-radius: 6px;
                padding: 12px;
                margin-bottom: 10px;
            }}

            .publicacion h4 {{
                margin: 8px 0;
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

            .formato-otro {{
                border-left-color: #64748b;
            }}

            .revision {{
                color: #9a6700;
                font-size: 12px;
                font-weight: bold;
            }}


            .estado {{
                background: #e3f5e9;
                color: #246b3b;
                padding: 5px 9px;
                border-radius: 12px;
            }}
        </style>
    </head>

    <body>

        <h1>Tablero de automatización de mercadeo</h1>

        <p>Panel de seguimiento de publicaciones de Trycore.</p>

        <section>
            <h2>Indicadores históricos</h2>
            <p>Publicaciones únicas: {total_unicos}</p>
            <p>Duplicados detectados: {total_duplicados}</p>
        </section>

        <section>
            <h2>Puntuaciones por formato</h2>
            <div>
                {tarjetas}
            </div>
        </section>

{seccion_pendientes}

        <section>
            <h2>Calendario de publicaciones</h2>

           <p>Vista de las dos semanas de programación.</p>

<div class="calendario-dos-semanas">
    {vista_calendario}
</div>

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
        </section>

    </body>
    </html>
    """

    return html


def guardar_tablero():
    """Genera y guarda el tablero HTML."""

    contenido = generar_tablero()

    ruta_salida = Path("salidas/tablero.html")

    ruta_salida.write_text(
        contenido,
        encoding="utf-8"
    )

    return ruta_salida
