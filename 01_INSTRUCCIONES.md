---
title: "Reto técnico: agentiza un proceso de Mercadeo"
subtitle: "Caso ficticio con fines de evaluación · Aprendiz de Operaciones y Automatización de Marketing"
---

> **Caso ficticio con fines de evaluación.** Este reto es un caso de estudio, como los que se usan en una escuela de negocios. El escenario, la reunión, el calendario, el historial de publicaciones, las cifras y los nombres de clientes son inventados y no describen una situación real de Trycore. La Guía de automatización con RPA es un documento público que se usa solo como texto de ejemplo. Tu trabajo se usa únicamente para evaluar tus capacidades en este proceso de selección: no se te pide resolver un problema real de la empresa y Trycore no lo usará ni lo publicará en su operación.

## Bienvenido al reto

En este caso ficticio vas a resolver un problema como los que enfrenta la operación de contenidos de un área de Mercadeo: cómo una sola pieza de contenido se diagnostica, se transforma en los formatos que usa el área, se programa en un calendario y se califica según su probabilidad de éxito. Tu trabajo es entender qué se necesita, diseñar un sistema con agentes y construir su núcleo.

Lo que queremos que aportes es lo que el marketing tradicional no suele tener: pensamiento de sistemas, algoritmos y matemáticas aplicados a decisiones que hoy se toman a mano o por intuición.

No buscamos perfección ni que ya lo sepas todo. Buscamos cómo piensas: si ves el proceso completo, si cuestionas lo que te dan, si verificas lo que produce una IA y si aprendes rápido. El reto está diseñado para resolverse en **menos de 5 horas**, y tú decides cuánto tiempo dedicas a cada parte. Si no alcanzas a terminar todo, entrega lo que tengas y cuéntanos en tu video qué harías con más tiempo.

## No necesitas conocer Trycore

Este reto no mide cuánto sabes de la empresa ni de marketing. Mide lo que ya aprendiste en tu programa de Desarrollo de Software y cómo lo aplicarías a un problema. Todo lo que necesitas viene en este documento y en los materiales del paquete.

Contexto mínimo: Trycore es una empresa colombiana que automatiza procesos de negocio para bancos y grandes empresas en Latinoamérica. Para este caso, imagina que su área de Mercadeo produce contenidos en varios formatos y que buena parte del trabajo táctico se hace a mano.

| Fase de tu programa | Cómo la usas en este reto |
| --- | --- |
| Análisis | Convertir unas notas desordenadas en requisitos claros |
| Planeación | Diseñar qué hace el programa, qué hace la persona y cómo se comunican |
| Ejecución | Construir el programa, su vista de calendario y mostrar tu proceso en el repositorio |
| Evaluación y despliegue | Demostrar con pruebas que funciona y que otra persona puede usarlo |

| Término | Qué significa aquí |
| --- | --- |
| Pieza madre | El contenido original del que salen los demás: la Guía de automatización con RPA |
| Formato | Cada forma en que se publica un contenido (post, carrusel, newsletter...). Cada uno tiene partes y técnicas de redacción propias |
| Contenido estructurado | El texto de una pieza dividido en las partes de su formato (de un carrusel: portada, láminas internas y cierre), sin diseño gráfico |
| Gancho | La primera frase de una pieza, la que hace que alguien siga leyendo |
| Tasa de interacción | Reacciones, comentarios y clics divididos por las veces que se vio la pieza |
| Agente | Un programa, con o sin IA, que hace una tarea por su cuenta con reglas y permisos definidos |
| UTM | Parámetros que se agregan al final de un enlace para saber de dónde llegó la visita |

## Cómo funciona

Puedes usar IA, y esperamos que lo hagas. Lo que importa es que la dirijas bien, verifiques lo que te responde y entiendas lo que entregas.

| Tema | Cómo funciona |
| --- | --- |
| Uso de IA | Permitido (Gemini gratuito u otra). En tu video cuéntanos dónde la usaste y qué corregiste o descartaste |
| Herramientas | Solo gratuitas. Tú eliges el lenguaje, las librerías y el entorno, y explicas por qué. Tu código va en un repositorio de GitHub. No necesitas licencias de pago, n8n, Make ni APIs de pago |
| Publicación | No publiques nada real. Todo queda en archivos de prueba |
| Tiempo | El reto está diseñado para resolverse en menos de 5 horas. Tú decides cuánto tiempo dedicas a cada parte |
| Qué entregas | El enlace a tu repositorio de GitHub con el programa, y un video donde explicas tu trabajo |
| Sustentación | 30 minutos por Meet con cámara encendida, después de recibir tu entrega |
| Confidencialidad | Los materiales son solo para este reto. No los compartas ni los publiques |

**Fechas y tiempos.** Las fechas y los tiempos de este reto (cuándo recibes el paquete, la fecha límite de entrega y la sustentación) son los que acordaste con Talento Humano al momento de recibir este material.

## El caso: el sistema táctico de contenidos

En este caso, Mercadeo tiene una estrategia de contenidos, pero la parte táctica, la que convierte esa estrategia en publicaciones, se sufre:

1. **No hay diagnóstico.** Nadie mide si una pieza está bien construida ni para qué formatos sirve.
2. **La transformación es manual.** Convertir una pieza en un carrusel, un post o un newsletter se hace a mano, y cada formato tiene reglas propias que es fácil romper.
3. **El calendario se arma a mano.** Aparecen choques, piezas del mismo tema muy juntas y publicaciones en días no hábiles.
4. **Se decide por intuición.** No hay forma de estimar qué pieza funcionará mejor, aunque existe un historial de resultados.

Tu sistema tiene un trabajo concreto: **cuando Mercadeo le entregue cualquier contenido nuevo (la pieza madre), debe tomarlo y hacer el resto solo.** Es decir, diagnosticarlo, transformarlo en piezas redactadas y estructuradas según su formato (sin diseño gráfico), programarlas en un calendario de dos semanas sin conflictos, calificar su probabilidad de éxito y mostrarlo todo en una página propia. La persona solo revisa y aprueba.

Para este caso, tu pieza madre de prueba es la Guía de automatización con RPA, un documento público del sitio de Trycore (https://trycore.com/guia-de-automatizacion-con-rpa/), tal como está publicada. Pero tu sistema debe funcionar con cualquier otra pieza madre, no solo con esta: en la sustentación lo probaremos con otra.

**Tu ventana de calendario: del 30 de noviembre de 2026 al 11 de diciembre de 2026.**

La pregunta central: **¿cómo harías que los agentes hagan el trabajo táctico repetitivo, y que las personas conserven las decisiones que importan?**

## Reglas que tu sistema debe cumplir

No tienes que conocerlas de antes: vienen en `config.json` y tu sistema debe leerlas de ahí, no escribirlas dentro del código. La guía `guia_configuracion.md` explica cada sección.

1. Solo se mencionan productos de la lista de productos vigentes.
2. No se inventan cifras: toda cifra de una pieza derivada debe existir en la pieza madre, y si allí no tiene fuente, se marca para revisión.
3. No aparecen los términos ni los nombres que el archivo marca como prohibidos o confidenciales.
4. Cada enlace lleva parámetros UTM según la convención del archivo.
5. Cada pieza derivada cumple la ficha de su formato: canal, longitud, estructura, técnicas de redacción y lo que necesita de la pieza madre. Si la pieza madre no tiene lo que un formato exige, el sistema lo dice; no lo inventa.
6. El calendario respeta las franjas, los días no hábiles, la capacidad por día y por semana, y la separación mínima entre piezas del mismo tema.

## Qué debes entregar

Entregas dos cosas: un programa y un video donde lo explicas. El reto está diseñado para resolverse en menos de 5 horas; tú decides cuánto tiempo dedicas a cada parte. Si no alcanzas a terminar todo, entrega lo que tengas.

**1. Un programa que haga el trabajo solo.** En el lenguaje que mejor domines de tu formación, con cuatro funciones:

1. **Diagnóstico.** Obtiene la pieza madre directamente desde su URL y entrega una ficha con indicadores medibles que tú defines (al menos 4) y las alertas que encuentre según las reglas.
2. **Transformación de formatos.** Para al menos 2 formatos de la matriz que apliquen, entrega el contenido de cada pieza derivada redactado y estructurado según su formato. Por ejemplo, de un carrusel entregas la portada, el texto de cada lámina interna y el cierre; de un newsletter, el asunto, la introducción, las secciones y el llamado a la acción. Aplica las técnicas de redacción de cada formato que indica la matriz. No se espera ningún diseño gráfico: ni imágenes, ni maquetación, ni plantillas visuales; eso corresponde a un diseñador. Puedes usar IA para redactar, pero tu sistema debe validar cada pieza contra su ficha y las reglas.
3. **Calendario.** Programa las piezas derivadas en tu ventana de dos semanas y muéstralas en una página web propia que tu programa genera: una vista semanal con cada pieza por día, su formato (por color), tema, estado y puntaje, con los conflictos y lo que no se pudo ubicar resaltados. No es una integración con Google Calendar, Outlook ni otro calendario externo. La vista es una interfaz de software que tú construyes; lo que no se pide es diseño gráfico de las piezas.
4. **Puntaje de éxito.** Con el historial de publicaciones, calcula un puntaje de 0 a 100 para cada pieza programada. Puede ser simple, pero debe apoyarse en los datos, y debes explicar cómo lo calculaste y cuáles son sus límites.

Requisitos técnicos:

- Funciona con cualquier pieza madre: la recibe como entrada (por ejemplo, una URL) y no deja nada de la guía de RPA escrito en el código. La ventana de calendario, el historial y el archivo de configuración también son entradas.
- Lee la URL, el historial y el archivo de configuración tal como te los entregamos, sin limpiarlos a mano.
- Cada función vive en una parte distinta del código.
- Se ejecuta con un solo comando y deja los resultados en archivos.
- Incluye pruebas automatizadas que se corren con un comando, con al menos 5 casos, y que fallan cuando una regla se rompe.
- No guarda claves ni contraseñas dentro del código.
- Muestra tu proceso en el historial del repositorio: al menos 3 commits con avances, no uno solo al final.
- Trae un README breve que diga cómo instalarlo y ejecutarlo.

**2. Un video (hasta 15 minutos).** Grábate explicando tu trabajo, con tu voz y tu pantalla; no necesitas editarlo ni mostrar tu cara. Debe cubrir cinco cosas:

En primer lugar, los requisitos. A partir de las notas de la reunión, cuéntanos los que necesita el sistema, ordenados por prioridad. Separa lo que se necesita de lo que se desea, señala las contradicciones que encuentres y di qué preguntas habrías hecho a Mercadeo antes de construir.

Después, el diseño: un diagrama simple del sistema (a mano frente a la cámara o en pantalla) que muestre qué hace cada agente o programa, qué hace la persona y qué datos pasan entre ellos, y los 3 riesgos que más te preocupan con el control con el que los enfrentarías.

Luego, una demostración: ejecuta tu programa con la pieza madre y muestra sus resultados, incluida la vista del calendario.

También tus decisiones técnicas: qué herramientas elegiste, qué alternativas descartaste, cómo calculaste el puntaje y cuáles son sus límites.

Por último, cómo usaste la IA: en qué momentos, qué te dio bien y qué tuviste que corregir.

**Reto extra (voluntario, suma hasta 10 puntos).** Elige una opción si te sobra tiempo: comprobar tu puntaje con datos que no usaste para construirlo, agregar filtros por formato y estado a la vista del calendario, exponer tu sistema como una API REST, empaquetarlo en un contenedor, o guardar los resultados en una base de datos. No se espera que lo hagas.

## Qué hay en este paquete

| Carpeta o archivo | Qué es |
| --- | --- |
| `02_insumos/notas_reunion.md` | Las notas de la reunión con Mercadeo |
| `02_insumos/pieza_madre/url.txt` | La URL de la Guía de automatización con RPA |
| `02_insumos/pieza_madre/guia_rpa_respaldo.html` | Copia del HTML de la guía, por si tu programa no logra descargarla. Si eso pasa, tu programa debe detectarlo y decirlo |
| `02_insumos/configuracion/` | `config.json` (reglas de Mercadeo) y `guia_configuracion.md` (explicación de cada sección) |
| `02_insumos/calendario/` | `ventana.json` (tus fechas) y `calendario_ocupado.csv` (lo que ya está agendado) |
| `02_insumos/historial/` | Unas 60 publicaciones pasadas de LinkedIn, ficticias, con su formato, fecha, hora, tema y resultados |

Todos los materiales son ficticios o de uso público. Pueden traer errores o datos incompletos, como pasa en el trabajo real. Parte de tu tarea es notarlos y decidir qué hacer con ellos.

**Cómo entregar.** Entrega el enlace a tu repositorio de GitHub (con el programa, las pruebas y un README breve) y el enlace a tu video (en Drive o en YouTube como no listado), con acceso para quien te indique Talento Humano. Para grabar puedes usar la grabadora de pantalla de tu sistema o OBS Studio, que es gratuito. Si tienes dudas sobre el reto, escríbele a Talento Humano.

## Cómo se evalúa

Miramos más cómo piensas y cómo aprendes que cuánto código entregas.

| Qué miramos | Peso |
| --- | --- |
| Requisitos y diseño (los explicas en tu video) | 15 |
| Diagnóstico y transformación de formatos | 20 |
| Calendario: algoritmo y vista | 15 |
| Puntaje de éxito y uso de los datos | 10 |
| Que funcione con otra pieza madre, calidad técnica y uso de la IA | 15 |
| Tu video y la sustentación en vivo | 25 |

El reto extra suma hasta 10 puntos y no te penaliza si no lo haces.

**La sustentación en vivo (30 minutos)**

Por Meet, con cámara encendida y puntualidad:

1. Conversamos sobre tu video: por qué elegiste esas herramientas, qué pasa si un agente se equivoca y dónde queda la persona (5 minutos).
2. Trabajas sobre tu propio código, sin IA: te damos una entrada y explicas qué hará tu programa, y luego encuentras un fallo que introdujimos en una copia de tu repositorio. Puedes consultar documentación oficial (10 minutos).
3. Resuelves un cambio en vivo, compartiendo pantalla: ejecutamos tu sistema con otra pieza madre y le hacemos un cambio de requerimiento. Aquí sí puedes usar IA, pero explica lo que haces (10 minutos).
4. Recibes retroalimentación y la aplicas en un ajuste rápido (5 minutos).

No necesitas saberlo todo. Pregunta lo que no entiendas, deja claros tus supuestos y reconoce lo que no sabes. Eso cuenta a tu favor.

¡Mucha suerte!
