<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/parameters_processing_files_through_pipelines/process_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## El Método `process` (Procesar) y Sus Parámetros
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/system/parameters_processing_files_through_pipelines/process_method/)

El método `process`, disponible para todo *pipeline* Krixik, se usa cuando deseas procesar archivos a través de un *pipeline*.

Esta introducción al método `process` se divide en las siguientes secciones:

- [Argumentos Principales del Método `process`](#argumentos-principales-del-metodo-process)
- [Uso Básico y Desglose de Salida](#uso-basico-y-desglose-de-salida)
- [Selección de Modelo por Medio del Argumento `modules`](#seleccion-de-modelo-por-medio-del-argumento-modules)
- [Usa tus Propios Modelos](#usa-tus-propios-modelos)
- [Argumentos de Metadata Opcionales](#argumentos-de-metadata-opcionales)
- [Valores Predeterminados de Argumentos de Metadata](#valores-predeterminados-de-argumentos-de-metadata)
- [Conversiones Automáticas de Tipo de Archivo](#conversiones-automaticas-de-tipo-de-archivo)
- [Límite de Tamaño de Salidas](#limite-de-tamano-de-salidas)

### Argumentos Principales del Metodo `process`

El método `process` toma cinco argumentos básicos (además del argumento `modules` y de una serie de argumentos opcionales de metadata que detallaremos en breve). Estos cinco argumentos son:

- `local_file_path`: (obligatorio, str) La ruta de archivo local del archivo que deseas procesar a través del *pipeline*.

- `local_save_directory`: (opcional, str) La ruta del directorio local en el que deseas que se guarden las salidas de tu proceso. El valor predeterminado de este argumento es el actual directorio del que estás operando.

- `expire_time`: (opcional, int) La cantidad de tiempo (en segundos) que la salida de un proceso permanece en los servidores de Krixik. El valor predeterminado de este argumento es 1800 segundos, que equivale a 30 minutos. Una vez se acaba este tiempo, el archivo se 'vence' y es completamente eliminado del sistema.

- `wait_for_process`: (opcional, bool) Le indica a Krixik si debe esperar que tu proceso termine antes de devolverte control de tu IDE o *notebook*. `True` le dice a Krixik que espere hasta que el proceso termine, así que no podrás ejecutar nada más mientras tanto. `False` le dice a Krixik que deseas recuperar control apenas se suba todo el archivo al sistema Krixik. Cuando su valor es `False` el estado del proceso se puede detallar con el método [`process_status`](metodo_process_status_estado_de_proceso.md). El valor predeterminado de este argumento es `True`.

- `verbose`: (opcional, bool) Determina si Krixik debe inmediatamente mostrar/imprimir actualizaciones de proceso en tu terminal o notebook. El valor predeterminado de este argumento es `True`.

### Uso Basico y Desglose de Salida

Primero crea un *pipeline* de módulo único para esta demostración del método `process`. Puedes usar un módulo [`sentiment` (análisis de sentimiento)](../../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md).


```python
# crea un pipeline de módulo único para esta demostración del método process
pipeline = krixik.create_pipeline(name="metodo_process_1_sentiment", module_chain=["sentiment"])
```

En el directorio local hemos creado un archivo JSON que contiene tres fragmentos de texto que simulan reseñas de productos. Los fragmentos dicen lo siguiente [la traducción no está en el archivo]:

- This recliner is the best damn seat I've ever come across. When I fall asleep on it, which is often, I sleep like a baby. [Esta reclinadora es la mejor reclinadora que he encontrado. Cuando me quedo dormido sobre ella, lo cual ocurre a menudo, duermo como un bebé.]

- This recliner is terrible. It broke on its way out of the box, and no matter what I try, it doesn't recline. Avoid at all costs. [Esta reclinadora es pésima. Se rompió cuando la saqué de la caja y se rehusa a reclinar, intente lo que intente. Evitar a toda costa.]

- I've sat on a lot of recliners in my life. I've forgotten about most of them. I'll forget about this one as well. [Me he sentado sobre muchas reclinadoras en mi vida. He olvidado la mayoría. Olvidaré esta también.]

Ten en cuenta que las entradas JSON _deben_ seguir un [formato específico](formato_JSON_entrada.md). Si no lo siguen serán rechazadas por Krixik.


```python
# procesa un pequeño archivo de entrada
process_demo_output = pipeline.process(
    local_file_path=data_dir + "input/resenas_de_reclinadora.json",  # la ruta de archivo inicial en la que yace el archivo JSON
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False,  # no mostrar actualizaciones de proceso al ejecutar el código
)
```

Ahora reproduce la salida del proceso. Dado que la salida de este módulo/modelo es en formato JSON, puedes reproducirla nítidamente con el siguiente código:


```python
# reproduce la salida del proceso anterior nítidamente
import json

print(json.dumps(process_demo_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "process_method_1_sentiment",
      "request_id": "339ef4dd-5c97-4822-b450-aea700bc6021",
      "file_id": "6a314cdb-6938-4663-aef5-a0258341c120",
      "message": "SUCCESS - output fetched for file_id 6a314cdb-6938-4663-aef5-a0258341c120.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "This recliner is the best damn seat I've ever come across. When I fall asleep on it, which is often, I sleep like a baby.",
          "positive": 0.871,
          "negative": 0.129,
          "neutral": 0.0
        },
        {
          "snippet": "This recliner is terrible. It broke on its way out of the box, and no matter what I try, it doesn't recline. Avoid at all costs.",
          "positive": 0.001,
          "negative": 0.999,
          "neutral": 0.0
        },
        {
          "snippet": "I've sat on a lot of recliners in my life. I've forgotten about most of them. I'll forget about this one as well.",
          "positive": 0.001,
          "negative": 0.999,
          "neutral": 0.0
        }
      ],
      "process_output_files": [
        "../../../data/output/6a314cdb-6938-4663-aef5-a0258341c120.json"
      ]
    }


Desglosa esta salida:

- `status_code`: El código de estado HTTP para este proceso (p.ej. "200", "500")

- `pipeline`: El nombre (`name`) del *pipeline* con el que acabas de usar el método `process`.

- `request_id`: El identificador único de esta ejecución del método `process`.

- `file_id`: El identificador único (del lado del servidor) de este archivo procesado, y por ende de la salida asociada.

- `message`: Este mensaje indica "SUCCESS" (éxito) o "FAILURE" (fracaso) para la ejecución de este método y ofrece detalle al respecto.

- `warnings`: Una lista de mensajes que incluye toda advertencia relacionada a la ejecución del método.

- `process_output`: La salida del proceso. En este caso, dado que está en formato JSON, es fácilmente reproducible en un *notebook* de código.

- `process_output_files`: Una lista de nombres de archivo y rutas de archivo generadas como salidas del proceso y guardadas localmente.


Puedes ver en `process_output` que el *pipeline* de [`análisis de sentimiento`](../../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md) ha funcionado correctamente. A cada reseña de producto se le han asignado valores de sentimiento desglosados entre positivo, negativo, y neutral.

Además de que está acá reproducida, esta salida de proceso también se ha guardado en el archivo indicado en `process_output_files`. Para cargarlo y confirmar que este contiene la misma salida de proceso que vimos arriba usa el siguiente código:


```python
# cargar la salida de proceso en el archivo
import json

with open(process_demo_output["process_output_files"][0], "r") as file:
    print(json.dumps(json.load(file), indent=2))
```

    [
      {
        "snippet": "This recliner is the best damn seat I've ever come across. When I fall asleep on it, which is often, I sleep like a baby.",
        "positive": 0.871,
        "negative": 0.129,
        "neutral": 0.0
      },
      {
        "snippet": "This recliner is terrible. It broke on its way out of the box, and no matter what I try, it doesn't recline. Avoid at all costs.",
        "positive": 0.001,
        "negative": 0.999,
        "neutral": 0.0
      },
      {
        "snippet": "I've sat on a lot of recliners in my life. I've forgotten about most of them. I'll forget about this one as well.",
        "positive": 0.001,
        "negative": 0.999,
        "neutral": 0.0
      }
    ]


### Seleccion de Modelo por Medio del Argumento `modules`

El argumento `modules` del método `process` es opcional, pero a través de él puedes acceder a una multitud de opciones de parametrización. Este argumento te permite parametrizar la operación de cada módulo, **INCLUYENDO** (cuando aplica) la definición de qué modelo está activo dentro de él.

El argumento `modules` se presenta como un diccionario con diccionarios dentro de él. En un *pipeline* de módulo único se ve así:

```python
modules={'<nombre de modelo>': {'model':'<modelo seleccionado>', 'params': <diccionario de parámetros>}}
```

Ten en cuenta que los nombres de los modelos son sensibles a mayúsculas y minúsculas.

Por ejemplo, en un *pipeline* de módulo único que contiene un módulo [`caption` (leyenda de imagen)](../../modulos/modulos_ia/modulo_caption_leyenda_de_imagen.md), el argumento `modules` se vería así si quisieras usar el modelo disponble `blip-image-captioning-base`:

```python
modules={'caption': {'model':'blip-image-captioning-base', 'params': {}}}
```

En este ejemplo, `params` es un diccionario vacío porque los modelos del módulo [`caption` (leyenda de imagen)](../../modulos/modulos_ia/modulo_caption_leyenda_de_imagen.md) no toman ningún parámetro. Otros tipos de modelos sí toman parámetros, como los modelos del módulo [`text-embedder` (encaje léxico)](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md). Así se vería el argumento `modules` para un *pipeline* de módulo unico con un módulo [`text-embedder`](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md):

```python
modules={'text-embedder': {'model':'multi-qa-MiniLM-L6-cos-v1', 'params': {'quantize': False}}}
```

`quantize` es un parámetro que puedes definir para modelos del módulo [`text-embedder` (encaje léxico)](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md) y *solamente* para modelos de ese módulo.

La sintaxis para el argumento `modules` en *pipelines* multimodulares es similar a lo anterior, pero en ese caso hay un subdiccionario para cada módulo. Por ejemplo, el argumento `modules` para un *pipeline* de [búsqueda semántica](../../ejemplos/ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_basica.md) que secuencia módulos [`parser` (fragmentación de texto)](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md), [`text-embedder` (encaje léxico)](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md), y [`vector-db` (base de datos vectorial)](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md) se vería así:

```python
modules={'parser': {'model':'fixed', 'params': {"chunk_size": 10, "overlap_size": 5}},
         'text-embedder': {'model':'all-MiniLM-L6-v2', 'params': {}},
         'vector-db': {'model':'faiss', 'params': {}}}
```

Ten en cuenta que cualquier módulo no explícitamente parametrizado tomará sus valores predeterminados. Si necesitas especificar el modelo de un solo módulo o sus parámetros, eso no significa que debes especificar los parámetros de todos los módulos del *pipeline* al ejecutar el método `process`. Por ende, dado que en el código arriba indicado los módulos [`text-embedder`](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md) y [`vector-db`](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md) se están usando con sus modelos predeterminados, podrías lograr exactamente lo mismo si los quitas del código y solo dejas el módulo [`parser`](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md):

```python
modules={'parser': {'model':'fixed', 'params': {"chunk_size": 10, "overlap_size": 5}}}
```

Encuentra una descripción detallada de nuestros módulos actuales, incluyendo una lista de los modelos disponibles para cada uno, [aquí](../../modulos/introduccion_modulos.md).

### Usa tus Propios Modelos

¿Tienes un modelo—ya sea uno que has desarrollado o uno al que le has hecho *fine-tuning*—que te gustaría usar en Krixik?

¡Haz clic aquí para aprender cómo hacerlo!

### Argumentos de Metadata Opcionales

El método `process` también toma varios argumentos de metadata opcionales. Estos no cambian la operación o tratamiento de datos de `process`. En cambio, hacen que tus archivos procesados sean más fáciles de recuperar y organizar. Puedes pensar en esto como un sistema de archivos para archivos que has procesado a través de tus *pipelines*.

Los argumentos de metadata opcionales incluyen:

- `symbolic_directory_path` (str) - Una ruta de directorio con formato UNIX bajo tu cuenta en el sistema Krixik. Su valor predeterminado es `/etc`.

- `file_name` (str) - Un nombre de archivo personalizado que debe terminar con la extensión de archivo del archivo de entrada original. Su valor predeterminado es un *string* aleatoriamente generado (detallado en breve).

- `symbolic_file_path` (str) - La combinación de `symbolic_directory_path` y `file_name` en un solo argumento. Su valor predeterminado es una concatenación del valor predeterminado de sus dos componentes.

- `file_tags` (list) - Una lista de etiquetas de archivo personalizadas (cada etiqueta es un par clave-valor). Su valor predeterminado es una lista vacía.

- `file_description` (str) - Una descripción de archivo personalizada. Su valor predeterminado es un *string* vacío.

Los primeros cuatro—`symbolic_directory_path`, `file_name`, `symbolic_directory_path` y `file_tags`—pueden usarse como argumentos del método [`list` (lista)](../sistema_de_archivos/metodo_list_lista.md) y para los métodos [`keyword_search` (búsqueda por palabras clave)](../metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md) y [`semantic_search` (búsqueda semántica o vectorial)](../metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md).

Ten en cuenta que un archivo que procesas a través de un *pipeline* solo está disponible para ese *pipeline*. Por ejemplo, si subes un archivo a un `symbolic_directory_path` en un *pipeline* no podrás verlo en otro *pipeline* a través de [`list`](../sistema_de_archivos/metodo_list_lista.md), [búsqueda](../../ejemplos/ejemplos_pipelines_de_busqueda/introduccion_pipelines_de_busqueda.md), o cualquier otra herramienta, así especifiques ese mismo `symbolic_directory_path`.

También ten en cuenta que un `symbolic_file_path` no se puede duplicar dentro de un *pipeline*. Si en un *pipeline* usas `process` con un archivo y especificas ciertos `symbolic_directory_path` y `file_name`, Krixik no te permitirá usar `process` con ningún otro archivo con esa misma combinación de `symbolic_directory_path` y `file_name`.

Para poner todo esto en práctica, usa el método `process` una vez más. El archivo será el mismo de reseñas de una reclinadora, pero el código será una versión expandida con algunos de estos argumentos de metadata opcionales:


```python
# procesa un pequeño archivo de entrada con argumentos de metadata opcionales
process_demo_output = pipeline.process(
    local_file_path=data_dir + "input/resenas_de_reclinadora.json",
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,
    wait_for_process=True,
    verbose=False,
    symbolic_directory_path="/mi/ruta/de/archivo/personalizada",
    file_name="observaciones_reclinadora.json",
    file_tags=[{"categoria": "muebles"}, {"codigo producto": "reclinadora-47b-u11"}],
    file_description="Tres reseñas de producto para la reclinadora Orwell Cloq.",
)
```

### Valores Predeterminados de Argumentos de Metadata

- Si no proporcionas un `file_name` se generará uno al azar. Este tendrá el siguiente formato: `krixik_generated_file_name_{10 caracteres aleatorios}.ext`, donde `.ext` es la extensión del archivo de entrada indicado en `local_file_path`.

- Si no proporcionas un `symbolic_directory_path`, el valor predefindo que tomará es `/etc`.

- Ten en cuenta que no puedes definir subdirectorios bajo el `symbolic_directory_path` `/etc`. Este es el directorio comodín, y la idea es que no se le construya nada debajo.

### Conversiones Automaticas de Tipo de Archivo

Para ciertos módulos, el método `process` automáticamente convierte el formato de algunos archivos de entrada presentados en `local_file_path`. Las conversiones actualmente llevadas a cabo por Krixik son:

- `pdf` -> `txt`
- `docx` -> `txt`
- `pptx` -> `txt`

### Limite de Tamano de Salidas

El límite de tamaño permitido de las salidas generadas por el método `process` es actualmente 5MB.
