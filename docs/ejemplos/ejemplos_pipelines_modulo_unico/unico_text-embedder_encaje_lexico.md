<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/single_module_pipelines/single_text-embedder.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## *Pipeline* de Módulo Único: `text-embedder` (Encaje Léxico)
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/examples/single_module_pipelines/single_text-embedder/)

Este documento presenta una guía de cómo ensamblar y consumir un *pipeline* de módulo único que solo incluye un módulo [`text-embedder` (encaje léxico)](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md). Se divide en las siguientes secciones:

- [Monta tu *Pipeline*](#monta-tu-pipeline)
- [Formato de Entrada Requerido](#formato-de-entrada-requerido)
- [Cómo Usar el Modelo Predeterminado](#como-usar-el-modelo-predeterminado)
- [Examina Salidas de Proceso Localmente](#examina-salidas-de-proceso-localmente)
- [Cómo Usar un Modelo No-Predeterminado](#como-usar-un-modelo-no-predeterminado)

### Monta tu *Pipeline*

Primero crea un *pipeline* de módulo único con un módulo [`text-embedder` (encaje léxico)](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md).

Usa el método [`create_pipeline`](../../sistema/creacion_de_pipelines/creacion_de_pipelines.md) para esto, incluyendo solamente una referencia de módulo [`text-embedder`](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md) en el argumento `module_chain`.


```python
# crea un pipeline con un solo módulo text-embedder
pipeline = krixik.create_pipeline(name="unico_text-embedder_1", module_chain=["text-embedder"])
```

### Formato de Entrada Requerido

El módulo [`text-embedder` (encaje léxico)](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md) recibe entradas con formato JSON. Las entradas JSON deben respetar [esta estructura](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/formato_JSON_entrada.md).

El archivo JSON de entrada también puede incluir, acompañando a cada fragmento, un par clave-valor en el que la clave es el *string* `"line numbers"` y el valor es una lista de *int* que indica cada número de línea en el documento original en el que yacía ese fragmento de texto. Esto te puede ayudar a identificar qué línea del documento original está incrustada en cada vector.

Antes de procesar un archivo de entrada—uno válido para este *pipeline*—examínalo con el siguiente código:


```python
# examina el contenido de un archivo de entrada válido
with open(data_dir + "input/1984_fragmentos.json", "r") as file:
    print(json.dumps(json.load(file), indent=2))
```

    [
      {
        "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
        "line_numbers": [
          1
        ]
      },
      {
        "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
        "line_numbers": [
          2,
          3,
          4,
          5
        ]
      }
    ]


### Como Usar el Modelo Predeterminado

Ahora procesa el archivo usando el modelo [predeterminado](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md#modelos-disponibles-en-el-modulo-text-embedder) del módulo [`text embedder` (encaje léxico)](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md): [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).

Dado que este es el modelo predeterminado, no hace falta que especifiques qué modelo quieres usar a través del argumento opcional [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).

Más adelante en este documento procesarás el mismo archivo, pero ahí especificando si el proceso será o no con cuantificación vectorial.


```python
# procesa el archivo con el modelo predeterminado
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_fragmentos.json",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False,  # no mostrar actualizaciones de proceso al ejecutar el código
)
```

La salida del proceso se reproduce con el siguiente código. Para aprender más sobre cada componente de esta salida, revisa la documentación del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).

El archivo de salida se ha guardado en la ubicación indicada bajo `process_output_files`. El `file_id` del archivo procesado es el prefijo del nombre del archivo de salida en esta ubicación.


```python
# nítidamente reproduce la salida de este proceso
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_text-embedder-1",
      "request_id": "ce2e57ce-c2be-49ac-8d43-59e6db2bcf25",
      "file_id": "ce4ddfa5-12c6-4dcb-86af-4f6d30ed6188",
      "message": "SUCCESS - output fetched for file_id ce4ddfa5-12c6-4dcb-86af-4f6d30ed6188.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/ce4ddfa5-12c6-4dcb-86af-4f6d30ed6188.npy"
      ]
    }


### Examina Salidas de Proceso Localmente

Los archivos de salida en formato NPY que contienen incrustaciones de vectores de los datos de entrada se pueden examinar con el siguiente código. Para que el ejercicio sea claro, en este ejemplo sólo se imprimirá la forma, y no el contenido, del arreglo devuelto.


```python
# examina la salida vectorial
import numpy as np

vectors = np.load(process_output["process_output_files"][0])
print(vectors.shape)
```

    (2, 384)


Esta salida significa que el arreglo tiene 2 filas con 384 valores en cada fila.

En el contexto del archivo de entrada, la primera fila es la forma vectorizada del primer fragmento: "It was a bright cold day in April, and the clocks were striking thirteen."

### Como Usar un Modelo No-Predeterminado

Para usar un modelo [no-predeterminado](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md#modelos-disponibles-en-el-modulo-text-embedder) como [`all-mpnet-base-v2`](https://huggingface.co/sentence-transformers/all-mpnet-base-v2), debes especificarlo a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) al usar el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md). Como indica la [documentación](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md) de este módulo, también puedes especificar si quieres usar la versión del modelo con o sin cuantificación vectorial:


```python
# procesa el archivo con un modelo no-predeterminado
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_fragmentos.json",  # todos los argumentos (salvo modules) son iguales que antes
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,
    wait_for_process=True,
    verbose=False,
    modules={
        "text-embedder": {"model": "all-mpnet-base-v2", "params": {"quantize": False}}
    },  # especifica un modelo no-predeterminado (y sus parámetros) para este proceso
)
```

Puedes usar código como el anterior para reproducir y revisar la salida de este proceso:


```python
# nítidamente reproduce la salida de este proceso
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_text-embedder-1",
      "request_id": "f53c93da-cf1b-41e0-a578-16dc62736ed4",
      "file_id": "1dcbde04-d4f2-414f-acaf-577c355bbb88",
      "message": "SUCCESS - output fetched for file_id 1dcbde04-d4f2-414f-acaf-577c355bbb88.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/1dcbde04-d4f2-414f-acaf-577c355bbb88.npy"
      ]
    }

