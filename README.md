# Automatización de Mercadeo - Trycore

## 1. Descripción del proyecto

Este proyecto desarrolla una solución en Python para automatizar parte del proceso de mercadeo de Trycore.

La herramienta recibe una pieza de contenido desde una fuente web o un archivo de respaldo, analiza su estructura, identifica temas relevantes y genera propuestas de publicaciones para diferentes formatos.

También analiza el historial de publicaciones para calcular indicadores de rendimiento y utiliza las reglas de un calendario para programar nuevas publicaciones.

El proceso mantiene la revisión humana como requisito obligatorio antes de aprobar o publicar cualquier contenido.

## 2. Objetivos

- Leer una pieza madre desde una fuente web.
- Analizar el contenido e identificar sus temas principales.
- Generar publicaciones para LinkedIn y carruseles.
- Validar los contenidos según las reglas de configuración.
- Analizar y normalizar el historial de publicaciones.
- Detectar registros duplicados, anomalías y valores extremos.
- Calcular puntuaciones de referencia basadas en resultados históricos.
- Programar publicaciones respetando las restricciones del calendario.
- Generar un tablero visual de seguimiento.
- Ejecutar pruebas automatizadas para verificar las reglas principales.

## 3. Tecnologías utilizadas

- Python.
- HTML.
- CSS.
- JSON.
- CSV.
- Git y GitHub.
- `unittest` para pruebas automatizadas.
- Biblioteca estándar de Python para el procesamiento de datos y la lectura de fuentes web.

## 4. Estructura del proyecto

```text
Reto_Aprendiz_Mercadeo_Trycore/
│
├── 02_insumos/
│   ├── calendario/
│   ├── configuracion/
│   ├── historial/
│   └── pieza_madre/
│
├── src/
│   ├── configuracion.py
│   ├── lector_fuente.py
│   ├── estructura_contenido.py
│   ├── diagnostico.py
│   ├── transformacion.py
│   ├── validador.py
│   ├── validador_formatos.py
│   ├── historial.py
│   ├── puntuacion.py
│   ├── calendario.py
│   └── tablero.py
│
├── tests/
│   ├── test_calendario.py
│   ├── test_diagnostico.py
│   ├── test_ejecutar.py
│   ├── test_historial.py
│   ├── test_puntuacion.py
│   ├── test_tablero.py
│   └── test_transformacion.py
│
├── salidas/
│   ├── calendario.csv
│   ├── resumen.json
│   └── tablero.html
│
├── ejecutar.py
├── README.md
├── requirements.txt
└── .gitignore
```

## 5. Funcionamiento general

El sistema ejecuta las siguientes etapas:

1. Carga la configuración y los insumos del proyecto.
2. Lee el contenido de la pieza madre desde una URL.
3. Utiliza un archivo de respaldo si no es posible acceder a la fuente web.
4. Extrae la estructura y el texto del contenido.
5. Realiza un diagnóstico mediante indicadores medibles.
6. Identifica información relevante para la transformación.
7. Genera un post de LinkedIn y un carrusel.
8. Valida los formatos generados.
9. Analiza y normaliza el historial de publicaciones.
10. Calcula puntuaciones de referencia según los datos históricos disponibles.
11. Programa las publicaciones respetando las restricciones del calendario.
12. Genera los archivos de resultados y el tablero HTML.

## 6. Requisitos e instalación

Se requiere:

- Python 3.10 o superior.
- Git (opcional, para control de versiones).

El proyecto utiliza módulos de la biblioteca estándar de Python, por lo que no requiere instalar dependencias externas adicionales.

### Crear y activar el entorno virtual

Desde la carpeta principal del proyecto:

```cmd
python -m venv .venv
```

Activar el entorno virtual:

```cmd
.venv\Scripts\activate
```

### Instalar dependencias

El archivo `requirements.txt` se conserva para facilitar la gestión de dependencias futuras. Actualmente no se requieren paquetes externos.

```cmd
python -m pip install -r requirements.txt
```

## 7. Ejecución del proyecto

Desde la carpeta principal, ejecutar:

```cmd
python ejecutar.py
```

El proceso realiza la automatización completa y genera los resultados en la carpeta `salidas`.

Los resultados principales son:

- `calendario.csv`
- `resumen.json`
- `tablero.html`

Para visualizar el tablero en Windows:

```cmd
start salidas\tablero.html
```

## 8. Ejecución de pruebas automatizadas

El proyecto cuenta con 50 pruebas automatizadas para verificar los módulos y las reglas principales.

Para ejecutar todas las pruebas:

```cmd
python -m unittest discover -s tests -v
```

Las pruebas cubren:

- Reglas y restricciones del calendario.
- Diagnóstico del contenido.
- Lectura de fuentes y manejo de respaldos.
- Análisis y normalización del historial.
- Cálculo de puntuaciones.
- Generación del tablero.
- Transformación y validación de contenidos.

## 9. Resultados generados

Los archivos se almacenan en la carpeta `salidas`.

| Archivo | Descripción |
|---|---|
| `calendario.csv` | Contiene las publicaciones programadas y sus datos de calendario. |
| `resumen.json` | Contiene el diagnóstico, los formatos generados, las validaciones, las puntuaciones y los resultados de programación. |
| `tablero.html` | Panel visual con indicadores históricos, alertas, publicaciones pendientes y calendario de dos semanas. |

## 10. Revisión humana obligatoria

Los contenidos generados son propuestas que deben ser revisadas por una persona antes de su aprobación y publicación.

El sistema no realiza publicaciones automáticas en LinkedIn ni utiliza credenciales de redes sociales.

La programación en el calendario no significa que una publicación haya sido aprobada o publicada.

Las cifras identificadas durante el diagnóstico pueden requerir verificación de sus fuentes.

## 11. Método de puntuación y limitaciones

Las puntuaciones se calculan utilizando estadísticas del historial de publicaciones, considerando las métricas disponibles:

- Impresiones.
- Reacciones.
- Clics.

El algoritmo utiliza medianas históricas para reducir el efecto de valores extremos y aplica ponderaciones para combinar las métricas.

Cuando existe información del formato y del tema, se consideran ambas referencias. Cuando no existe historial específico del tema, se utiliza únicamente el historial del formato.

La cantidad de datos disponibles se utiliza para clasificar el nivel de evidencia.

Las puntuaciones son indicadores relativos de comparación histórica. No representan probabilidades de éxito, predicciones ni garantías de rendimiento futuro.

Cuando no existe información suficiente, el sistema debe indicar que no dispone de una puntuación individual válida.

## 12. Consideraciones y limitaciones

- Los formatos implementados actualmente son el post de LinkedIn y el carrusel.
- La calidad del contenido generado requiere revisión humana.
- La puntuación depende de la disponibilidad y calidad del historial.
- Los temas sin registros históricos suficientes no pueden recibir una comparación temática confiable.
- Las cifras extraídas de la pieza madre deben verificarse antes de su utilización.
- El tablero presenta el calendario y los resultados del proceso; no reemplaza la aprobación humana.
- La generación de contenido no incluye diseño gráfico ni publicación directa en redes sociales.
- El sistema genera archivos locales y no publica contenido en plataformas externas.

## 13. Control de versiones

El proyecto utiliza Git para registrar los avances y cambios realizados durante el desarrollo.

El historial de commits permite identificar la evolución de la estructura, el diagnóstico, el análisis histórico, el algoritmo de puntuación, el calendario, las pruebas y el tablero visual.
