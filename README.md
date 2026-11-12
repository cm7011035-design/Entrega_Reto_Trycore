

\# Automatización de Mercadeo - Trycore



\## 1. Descripción del proyecto



Este proyecto desarrolla una solución en Python para automatizar parte del proceso de mercadeo de Trycore.



La herramienta recibe una pieza de contenido, analiza su estructura, identifica temas relevantes y genera propuestas de publicaciones para diferentes formatos.



También analiza el historial de publicaciones para calcular indicadores de rendimiento y utiliza las reglas de un calendario para programar las nuevas publicaciones.



El proceso mantiene la revisión humana como requisito antes de aprobar o publicar cualquier contenido.



\## 2. Objetivos



\- Leer una pieza madre desde una fuente web.

\- Analizar el contenido y detectar sus temas principales.

\- Generar publicaciones para LinkedIn y carruseles.

\- Validar los contenidos según las reglas de configuración.

\- Analizar el historial de publicaciones.

\- Calcular puntuaciones basadas en resultados históricos.

\- Programar publicaciones respetando las restricciones del calendario.

\- Generar un tablero visual de seguimiento.

\- Ejecutar pruebas automatizadas para verificar las reglas principales.



\## 3. Tecnologías utilizadas



\- Python.

\- HTML.

\- CSS.

\- JSON.

\- CSV.

\- Git y GitHub.

\- unittest para pruebas automatizadas.



\## 4. Estructura del proyecto



```text

Reto\_Aprendiz\_Mercadeo\_Trycore/

│

├── 02\_insumos/

│   ├── calendario/

│   ├── configuracion/

│   ├── historial/

│   └── pieza\_madre/

│

├── src/

│   ├── configuracion.py

│   ├── lector\_fuente.py

│   ├── estructura\_contenido.py

│   ├── diagnostico.py

│   ├── transformacion.py

│   ├── validador.py

│   ├── validador\_formatos.py

│   ├── historial.py

│   ├── puntuacion.py

│   ├── calendario.py

│   └── tablero.py

│

├── tests/

│   ├── test\_calendario.py

│   ├── test\_diagnostico.py

│   ├── test\_historial.py

│   ├── test\_puntuacion.py

│   └── test\_tablero.py

│

├── salidas/

│   ├── resumen.json

│   ├── calendario\_prueba.csv

│   └── tablero.html

│

├── ejecutar.py

├── README.md

└── .gitignore

```



\## 5. Funcionamiento general



El sistema ejecuta las siguientes etapas:



1\. Carga la configuración y los insumos entregados.

2\. Lee el contenido de la pieza madre.

3\. Extrae su estructura y texto.

4\. Realiza un diagnóstico del contenido.

5\. Selecciona información relevante.

6\. Genera un post de LinkedIn y un carrusel.

7\. Valida los formatos generados.

8\. Analiza el historial de publicaciones.

9\. Calcula puntuaciones de referencia.

10\. Programa las publicaciones según las reglas del calendario.

11\. Genera los archivos de resultados y el tablero HTML.



\## 6. Ejecución del proyecto



Se requiere Python instalado.



Desde la carpeta principal del proyecto, activar el entorno virtual:



```cmd

.venv\\Scripts\\activate

```



Instalar las dependencias registradas en el proyecto:



```cmd

python -m pip install -r requirements.txt

```



Ejecutar la automatización:



```cmd

python ejecutar.py

```



El proceso genera los resultados en la carpeta `salidas`.



\## 7. Ejecución de pruebas



Para ejecutar todas las pruebas automatizadas:



```cmd

python -m unittest discover -s tests -v

```



Actualmente, el proyecto cuenta con 32 pruebas automatizadas aprobadas.



\## 8. Resultados generados



\- `resumen.json`: contiene el diagnóstico, formatos generados, validaciones, puntuaciones y resultados de programación.

\- `calendario.csv`: contiene el calendario de publicaciones generado por el proceso.

\- `tablero.html`: tablero visual con las publicaciones, fechas, formatos y puntuaciones históricas.



Los archivos se generan en la carpeta `salidas`.

\## 9. Revisión humana



Los contenidos generados son propuestas que deben ser revisadas por una persona antes de su aprobación y publicación.



El sistema no realiza publicaciones automáticas en LinkedIn ni utiliza credenciales de redes sociales.



Las puntuaciones son indicadores comparativos basados en datos históricos. No representan probabilidades ni garantizan resultados futuros.



\## 10. Consideraciones y limitaciones



\- Los formatos implementados actualmente son el post de LinkedIn y el carrusel.

\- La calidad del contenido generado requiere revisión humana.

\- La puntuación depende de la información disponible en el historial.

\- Los temas utilizados para comparar resultados deben contar con datos históricos suficientes.

\- El tablero presenta el calendario y los resultados del proceso; no reemplaza la aprobación humana.

\- La generación de contenido no incluye diseño gráfico ni publicación directa en redes sociales.



\## 11. Control de versiones



El proyecto utiliza Git para registrar los avances y cambios realizados durante el desarrollo.



