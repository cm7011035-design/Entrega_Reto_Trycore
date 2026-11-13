# AutomatizaciÃ³n de Mercadeo - Trycore

## 1. DescripciÃ³n del proyecto

Este proyecto desarrolla una soluciÃ³n en Python para automatizar parte del proceso de mercadeo de Trycore.

La herramienta recibe una pieza de contenido desde una fuente web o un archivo de respaldo, analiza su estructura, identifica temas relevantes y genera propuestas de publicaciones para diferentes formatos.

TambiÃ©n analiza el historial de publicaciones para calcular indicadores de rendimiento y utiliza las reglas de un calendario para programar nuevas publicaciones.

El proceso mantiene la revisiÃ³n humana como requisito obligatorio antes de aprobar o publicar cualquier contenido.

## 2. Objetivos

- Leer una pieza madre desde una fuente web.
- Analizar el contenido e identificar sus temas principales.
- Generar publicaciones para LinkedIn y carruseles.
- Validar los contenidos segÃºn las reglas de configuraciÃ³n.
- Analizar y normalizar el historial de publicaciones.
- Detectar registros duplicados, anomalÃ­as y valores extremos.
- Calcular puntuaciones de referencia basadas en resultados histÃ³ricos.
- Programar publicaciones respetando las restricciones del calendario.
- Generar un tablero visual de seguimiento.
- Ejecutar pruebas automatizadas para verificar las reglas principales.

## 3. TecnologÃ­as utilizadas

- Python.
- HTML.
- CSS.
- JSON.
- CSV.
- Git y GitHub.
- `unittest` para pruebas automatizadas.
- Biblioteca estÃ¡ndar de Python para el procesamiento de datos y la lectura de fuentes web.

## 4. Estructura del proyecto

```text
Reto_Aprendiz_Mercadeo_Trycore/
â”‚
â”œâ”€â”€ 02_insumos/
â”‚   â”œâ”€â”€ calendario/
â”‚   â”œâ”€â”€ configuracion/
â”‚   â”œâ”€â”€ historial/
â”‚   â””â”€â”€ pieza_madre/
â”‚
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ configuracion.py
â”‚   â”œâ”€â”€ lector_fuente.py
â”‚   â”œâ”€â”€ estructura_contenido.py
â”‚   â”œâ”€â”€ diagnostico.py
â”‚   â”œâ”€â”€ transformacion.py
â”‚   â”œâ”€â”€ validador.py
â”‚   â”œâ”€â”€ validador_formatos.py
â”‚   â”œâ”€â”€ historial.py
â”‚   â”œâ”€â”€ puntuacion.py
â”‚   â”œâ”€â”€ calendario.py
â”‚   â””â”€â”€ tablero.py
â”‚
â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ test_calendario.py
â”‚   â”œâ”€â”€ test_diagnostico.py
â”‚   â”œâ”€â”€ test_ejecutar.py
â”‚   â”œâ”€â”€ test_historial.py
â”‚   â”œâ”€â”€ test_puntuacion.py
â”‚   â”œâ”€â”€ test_tablero.py
â”‚   â””â”€â”€ test_transformacion.py
â”‚
â”œâ”€â”€ salidas/
â”‚   â”œâ”€â”€ calendario.csv
â”‚   â”œâ”€â”€ resumen.json
â”‚   â””â”€â”€ tablero.html
â”‚
â”œâ”€â”€ ejecutar.py
â”œâ”€â”€ README.md
â”œâ”€â”€ requirements.txt
â””â”€â”€ .gitignore
```

## 5. Funcionamiento general

El sistema ejecuta las siguientes etapas:

1. Carga la configuraciÃ³n y los insumos del proyecto.
2. Lee el contenido de la pieza madre desde una URL.
3. Utiliza un archivo de respaldo si no es posible acceder a la fuente web.
4. Extrae la estructura y el texto del contenido.
5. Realiza un diagnÃ³stico mediante indicadores medibles.
6. Identifica informaciÃ³n relevante para la transformaciÃ³n.
7. Genera un post de LinkedIn y un carrusel.
8. Valida los formatos generados.
9. Analiza y normaliza el historial de publicaciones.
10. Calcula puntuaciones de referencia segÃºn los datos histÃ³ricos disponibles.
11. Programa las publicaciones respetando las restricciones del calendario.
12. Genera los archivos de resultados y el tablero HTML.

## 6. Requisitos e instalaciÃ³n

Se requiere:

- Python 3.10 o superior.
- Git (opcional, para control de versiones).

El proyecto utiliza módulos de la biblioteca estÃ¡ndar de Python, por lo que no requiere instalar dependencias externas adicionales.

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

El archivo `requirements.txt` se conserva para facilitar la gestiÃ³n de dependencias futuras. Actualmente no se requieren paquetes externos.

```cmd
python -m pip install -r requirements.txt
```

## 7. EjecuciÃ³n del proyecto

Desde la carpeta principal, ejecutar:

```cmd
python ejecutar.py
```

El proceso realiza la automatizaciÃ³n completa y genera los resultados en la carpeta `salidas`.

Los resultados principales son:

- `calendario.csv`
- `resumen.json`
- `tablero.html`

Para visualizar el tablero en Windows:

```cmd
start salidas\tablero.html
```

## 8. EjecuciÃ³n de pruebas automatizadas

El proyecto cuenta con 55 pruebas automatizadas para verificar los módulos y las reglas principales.

Para ejecutar todas las pruebas:

```cmd
python -m unittest discover -s tests -v
```

Las pruebas cubren:

- Reglas y restricciones del calendario.
- DiagnÃ³stico del contenido.
- Lectura de fuentes y manejo de respaldos.
- AnÃ¡lisis y normalizaciÃ³n del historial.
- CÃ¡lculo de puntuaciones.
- GeneraciÃ³n del tablero.
- TransformaciÃ³n y validaciÃ³n de contenidos.

## 9. Resultados generados

Los archivos se almacenan en la carpeta `salidas`.

| Archivo | DescripciÃ³n |
|---|---|
| `calendario.csv` | Contiene las publicaciones programadas y sus datos de calendario. |
| `resumen.json` | Contiene el diagnÃ³stico, los formatos generados, las validaciones, las puntuaciones y los resultados de programaciÃ³n. |
| `tablero.html` | Panel visual con indicadores histÃ³ricos, alertas, publicaciones pendientes y calendario de dos semanas. |

## 10. RevisiÃ³n humana obligatoria

Los contenidos generados son propuestas que deben ser revisadas por una persona antes de su aprobaciÃ³n y publicaciÃ³n.

El sistema no realiza publicaciones automÃ¡ticas en LinkedIn ni utiliza credenciales de redes sociales.

La programaciÃ³n en el calendario no significa que una publicaciÃ³n haya sido aprobada o publicada.

Las cifras identificadas durante el diagnÃ³stico pueden requerir verificaciÃ³n de sus fuentes.

## 11. MÃ©todo de puntuaciÃ³n y limitaciones

Las puntuaciones se calculan utilizando estadÃ­sticas del historial de publicaciones, considerando las mÃ©tricas disponibles:

- Impresiones.
- Reacciones.
- Clics.

El algoritmo utiliza medianas histÃ³ricas para reducir el efecto de valores extremos y aplica ponderaciones para combinar las mÃ©tricas.

Cuando existe informaciÃ³n del formato y del tema, se consideran ambas referencias. Cuando no existe historial especÃ­fico del tema, se utiliza Ãºnicamente el historial del formato.

La cantidad de datos disponibles se utiliza para clasificar el nivel de evidencia.

Las puntuaciones son indicadores relativos de comparaciÃ³n histÃ³rica. No representan probabilidades de Ã©xito, predicciones ni garantÃ­as de rendimiento futuro.

Cuando no existe informaciÃ³n suficiente, el sistema debe indicar que no dispone de una puntuaciÃ³n individual vÃ¡lida.

## 12. Consideraciones y limitaciones

- Los formatos implementados actualmente son el post de LinkedIn y el carrusel.
- La calidad del contenido generado requiere revisiÃ³n humana.
- La puntuaciÃ³n depende de la disponibilidad y calidad del historial.
- Los temas sin registros histÃ³ricos suficientes no pueden recibir una comparaciÃ³n temÃ¡tica confiable.
- Las cifras extraÃ­das de la pieza madre deben verificarse antes de su utilizaciÃ³n.
- El tablero presenta el calendario y los resultados del proceso; no reemplaza la aprobaciÃ³n humana.
- La generaciÃ³n de contenido no incluye diseÃ±o grÃ¡fico ni publicaciÃ³n directa en redes sociales.
- El sistema genera archivos locales y no publica contenido en plataformas externas.

## 13. Control de versiones

El proyecto utiliza Git para registrar los avances y cambios realizados durante el desarrollo.

El historial de commits permite identificar la evoluciÃ³n de la estructura, el diagnÃ³stico, el anÃ¡lisis histÃ³rico, el algoritmo de puntuaciÃ³n, el calendario, las pruebas y el tablero visual.
