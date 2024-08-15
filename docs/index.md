# ¡Bienvenidos a Krixik!

Ensamblar un *pipeline* secuencialmente compuesto de varios modelos de IA puede ser difícil y costoso. Incluso consumir un solo modelo es a menudo una tarea desgastante.

Por eso estamos acá. **Bienvenidos a Krixik**, donde puedes fácilmente ensamblar y consumir sin servidor pipelines modulares de IA a través de APIs seguros.

### Table of Contents

- [Guía de Inicio Rápido](#guía-de-inicio-rápido)
- [¿Qué Puedes Construir con Krixik?](#qué-puedes-construir-con-krixik)
- [Más Detalles - Documentación](#más-detalles---documentación)

## Guía de Inicio Rápido

### Registra tu Cuenta

Krixik está en beta, por lo cual acceso al cliente de Krixik actualmente solo se puede obtener a través de solicitud directa.

Si te gustaría participar en nuestras pruebas beta por favor llena [este breve Google Form](https://forms.gle/RyBAvjN1HEWPScb67).

### Instalación de Krixik

Ejecuta el siguiente comando para [instalar](https://krixik-docs.readthedocs.io/es-main/sistema/inicializacion/instalacion_del_cliente/) el cliente Python de Krixik:

```pip
pip install krixik
```

Nota: Se requiere la versión 3.10 (o mayor) de Python.


### Inicializa tu Sesión

Para [inicializar](https://krixik-docs.readthedocs.io/es-main/sistema/inicializacion/inicializacion_y_autenticacion/) tu sesión en el cliente de Krixik necesitarás tus secretos únicos `api_key` y `api_url`. Los administradores de Krixik enviarán secretos individuales a cada participante en nuestras pruebas beta.

En vez de manejar tus secretos directamente, enfáticamente recomendamos guardarlos en un archivo `.env` y cargarlos a través de [python-dotenv](https://pypi.org/project/python-dotenv/).

Una vez tengas tus secretos, [inicializa](https://krixik-docs.readthedocs.io/es-main/sistema/inicializacion/inicializacion_y_autenticacion/) tu sesión de la siguiente manera:


```python
from krixik import krixik
krixik.init(api_key=MY_API_KEY, 
            api_url=MY_API_URL)
```

...donde  `MY_API_KEY` y `MY_API_URL` son los secretos de tu cuenta.

Si has perdido tus secretos, por favor escríbenos directamente.

### Construye tu Primer *Pipeline*

[Construye un simple *pipeline* de transcripción que consiste de un solo módulo `transcribe` (transcripción).](https://krixik-docs.readthedocs.io/es-main/ejemplos/ejemplos_pipelines_modulo_unico/unico_transcribe_transcripcion/) Puedes [crear](https://krixik-docs.readthedocs.io/es-main/sistema/creacion_de_pipelines/creacion_de_pipelines/) el *pipeline* con una sola línea de código:

```python
# crear un simple pipeline de transcripción
pipeline = krixik.create_pipeline(name='mi-pipeline-de-transcripcion-1', 
                                  module_chain=["transcribe"])
```

¡El pipeline está listo! Ahora puedes [procesar](https://krixik-docs.readthedocs.io/es-main/sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar/) archivos de audio a través de él para generar transcripciones de ellos.

```python
pipeline.process(local_file_path='./camino/a/mi/archivo/mp3')
```

Las salidas de [este pipeline](https://krixik-docs.readthedocs.io/es-main/ejemplos/ejemplos_pipelines_modulo_unico/unico_transcribe_transcripcion/) serán una transcripción de tu audio con anotaciones de fecha/hora, un `file_id` que sirve de identificación única para el archivo procesado, y un `request_id` que sirve de identificación única para el proceso mismo.


### Extiende tu *Pipeline*

[Supón que quieres hacer búsqueda semántica sobre toda salida de un módulo `transcribe` (transcripción).](https://krixik-docs.readthedocs.io/es-main/ejemplos/ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_sobre_transcripcion/)

Tendrías que hacer lo siguiente después de la transcripción:

1. *Convertir* la transcripción en un archivo de texto
2. *Fragmentar* el texto usando una ventana movible, segmentándolo en fragmentos que posiblemente se sobreponen entre sí
3. *Encaje léxico* para convertir cada fragmento en un vector
4. *Guardar* los vectores resultantes en una base de datos vectorial
5. *Indexar* esta base de datos
6. *Habilitar* búsqueda semántica sobre la base de datos

Localmente crear y hacerle pruebas a esta secuencia de pasos sería demorado, y hacerlo en producción de manera segura aún más. Eso dejando de lado la intención de hacerlo con arquitectura sin servidor.

Con **Krixik**, por fortuna, puedes rápidamente incorporar esta funcionalidad a tu *pipeline* anterior con solo agregar un par de módulos. La sintaxis se mantiene igual que antes, así que [crear](https://krixik-docs.readthedocs.io/es-main/sistema/creacion_de_pipelines/creacion_de_pipelines/) el nuevo pipeline se sigue haciendo con una sola línea de código:

```python
# crear pipeline con los módulos arriba insinuados
pipeline_2 = krixik.create_pipeline(name='transcripcion-y-busqueda-semantica', 
                                    module_chain=["transcribe",
                                                "json-to-txt",
                                                "parser", 
                                                "text-embedder", 
                                                "vector-db"])
```

[Procesa](https://krixik-docs.readthedocs.io/es-main/sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar/) un archivo a través de tu nuevo *pipeline*.

```python
pipeline_2.process(local_file_path='./camino/a/mi/archivo/mp3')
```

Ahora que hay al menos un archivo en [el pipeline](https://krixik-docs.readthedocs.io/es-main/ejemplos/ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_sobre_transcripcion/), puedes usar el `file_id` del archivo—que te fue devuelto al finalizar el proceso anterior—para hacer búsqueda semántica sobre su transcripción con el método [`semantic_search`](https://krixik-docs.readthedocs.io/es-main/sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica/):

```python
pipeline_2.semantic_search(query="El texto que quieres semánticamente buscar va acá",
                           file_ids=['el_file_id_de_arriba'])
```

¡Eso es todo! Has transcrito el archivo, procesado la transcripción, hecho búsqueda semántica sobre ella, y puedes reutilizar [el pipeline](https://krixik-docs.readthedocs.io/es-main/ejemplos/ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_sobre_transcripcion/) para cuantos archivos y búsquedas desees... todo en un par de minutos y con pocas líneas de código.

### Opcional: Haz *pull* al repositorio de Krixik Docs en Español

Si deseas hacerle seguimiento al ejemplo anterior, o a cualquier ejemplo de las docenas que compartimos en esta documentación, simplemente hazle *pull* a todo el [repositorio de Krixik Docs en Español](https://github.com/krixik-ai/krixik-docs/tree/es-main).

Hacer esto te proporcionará todos los archivos necesarios, y el código ya está configurado para correr en esa estructura de directorios.

## ¿Qué Puedes Construir con Krixik?

La [gama de ejemplos](https://krixik-docs.readthedocs.io/es-main/ejemplos/introduccion_ejemplos_de_pipelines/) que hemos documentado incluye *pipelines* para:

- ...generarle leyendas a una serie de imágenes y luego hacer búsqueda de palabras claves sobre todas las leyendas.
  - [Pipeline: [Caption (leyenda de imagen) → JSON-to-TXT → Keyword Database (base de datos de palabras claves)]](https://krixik-docs.readthedocs.io/es-main/ejemplos/ejemplos_pipelines_de_busqueda/multi_busqueda_por_palabras_clave_sobre_leyendas_de_imagen/)
- ...transcribir un conjunto de grabaciones, traducirlas al inglés, y luego hacer análisis de sentimiento sobre cada una.
  - [Pipeline: [Transcribe (transcripción) → Translate (traducción) → JSON-to-TXT → Parser (fragmentación de texto) → Sentiment Analysis (análisis de sentimiento)]](https://krixik-docs.readthedocs.io/es-main/ejemplos/ejemplos_pipelines_multi_modulo_sin_busqueda/multi_analisis_de_sentimiento_sobre_transcripcion_traducida/)
- ...fácilmente y sin servidor consumir tu modelo predilecto ROC de fuente abierta.
  - [Pipeline: [OCR (ROC)]](https://krixik-docs.readthedocs.io/es-main/ejemplos/ejemplos_pipelines_modulo_unico/unico_ocr_roc/)

Esto es apenas la punta del iceberg. Muchos más *pipelines* son posibles hoy ([ve más ejemplos acá](https://krixik-docs.readthedocs.io/es-main/ejemplos/introduccion_ejemplos_de_pipelines/)), y la librería Krixik de módulos y modelos siempre estará en expansión—tal vez incluso pronto incluya módulos/modelos que [tú contribuyas](https://krixik-docs.readthedocs.io/es-main/modulos/agrega_tus_propios_modulos_o_modelos/).

## Más Detalles - Documentación

Lo anterior no es más que una pequeña idea del verdadero poder de Krixik. Además de todos los parámetros que puedes ajustar (tema que ni tocamos en este README), la caja de herramientas Krixik es una colección siempre creciente de modelos y módulos con los que puedes construir.

Si te gustaría aprender más, por favor visita la [Documentación de Krixik](https://krixik-docs.readthedocs.io/es-main/), donde se entra en detalle sobre:

- [Cómo Arrancar y Más: El Sistema Krixik](https://krixik-docs.readthedocs.io/es-main/sistema/introduccion_al_sistema/)
- [La Librería de Módulos Krixik](https://krixik-docs.readthedocs.io/es-main/modulos/introduccion_modulos/)
- [Ejemplos de *Pipelines* Krixik](https://krixik-docs.readthedocs.io/es-main/ejemplos/introduccion_ejemplos_de_pipelines/)

## Fecha de Lanzamiento de Krixik y *Newsletter* (Boletín Informativo)

¿Te emociona que Krixik se gradúe de beta? ¡A nosotros también! Estamos seguros de que este producto va a ser algo realmente fantástico, y nos encantaría tenerte a bordo durante ese viaje.

Si quieres que te mantengamos al tanto sobre el lanzamiento y otros temas (prometemos no enviarte *spam*), por favor suscríbete a correspondencia ocasional de nosotros [acá](https://forms.gle/Lp38U1UDpkppqoCD9).

Gracias por tu tiempo, y ¡bienvenidos a Krixik!