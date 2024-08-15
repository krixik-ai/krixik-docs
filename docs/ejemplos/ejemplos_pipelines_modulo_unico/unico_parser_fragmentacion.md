<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/single_module_pipelines/single_parser.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## *Pipeline* de Módulo Único: `parser` (Fragmentación de Texto)
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/examples/single_module_pipelines/single_parser/)

Este documento presenta una guía de cómo ensamblar y consumir un *pipeline* de módulo único que solo incluye un módulo [`parser` (fragmentación de texto)](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md). Se divide en las siguientes secciones:

- [Monta tu *Pipeline*](#monta-tu-pipeline)
- [Formato de Entrada Requerido](#formato-de-entrada-requerido)
- [Cómo Usar el Modelo Predeterminado](#como-usar-el-modelo-predeterminado)
- [Cómo Usar un Modelo No-Predeterminado](#como-usar-un-modelo-no-predeterminado)

### Monta tu *Pipeline*

Primero crea un *pipeline* de módulo único con un módulo [`parser` (fragmentación de texto)](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md).

Usa el método [`create_pipeline`](../../sistema/creacion_de_pipelines/creacion_de_pipelines.md) para esto, incluyendo solamente una referencia de módulo [`parser`](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md) en el argumento `module_chain`.


```python
# crea un pipeline con un solo módulo parser
pipeline = krixik.create_pipeline(name="unico_parser_1", module_chain=["parser"])
```

### Formato de Entrada Requerido

El módulo [`parser` (fragmentación de texto)](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md) recibe como entradas documentos textuales con formato TXT, PDF, DOCX y PPTX, aunque estos últimos tres formatos son automáticamente convertidos a TXT al iniciar proceso.

Antes de procesar un archivo de entrada—uno válido para este *pipeline*—examínalo con el siguiente código:


```python
# examina el contenido de un archivo de entrada válido
with open(data_dir + "input/1984_muy_corto.txt", "r") as file:
    print(file.read())
```

    It was a bright cold day in April, and the clocks were striking thirteen.
    Winston Smith, his chin nuzzled into his breast in an effort to escape the
    vile wind, slipped quickly through the glass doors of Victory Mansions,
    though not quickly enough to prevent a swirl of gritty dust from entering
    along with him.


### Como Usar el Modelo Predeterminado

Ahora procesa el archivo usando el modelo [predeterminado](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md#modelos-disponibles-en-el-modulo-parser) del módulo [`parser` (fragmentación de texto)](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md): [`sentence`](https://www.nltk.org/api/nltk.tokenize.html).

Dado que este es el modelo predeterminado, no hace falta que especifiques qué modelo quieres usar a través del argumento opcional [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).


```python
# procesa el archivo con el modelo predeterminado
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_muy_corto.txt",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # wait for process to complete before returning IDE control to user
    verbose=False,  # do not display process update printouts upon running code
)
```

La salida del proceso se reproduce con el siguiente código. Para aprender más sobre cada componente de esta salida, revisa la documentación del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).

Dado que la salida de este modelo/módulo es un archivo JSON, la salida también se incluye en el objeto (esto solo ese el caso para salidas JSON). Además, el archivo de salida se ha guardado en la ubicación indicada bajo `process_output_files`. El `file_id` del archivo procesado es el prefijo del nombre del archivo de salida en esta ubicación.


```python
# nítidamente reproduce la salida de este proceso
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_parser_1",
      "request_id": "07569a36-93d8-47bb-b487-bba25ccc1348",
      "file_id": "60542629-7470-476f-b94e-40e2c53608bf",
      "message": "SUCCESS - output fetched for file_id 60542629-7470-476f-b94e-40e2c53608bf.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
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
      ],
      "process_output_files": [
        "../../../data/output/60542629-7470-476f-b94e-40e2c53608bf.json"
      ]
    }


Puedes ver en `process_output` que el párrafo de dos oraciones en el archivo de entrada se ha separado correctamente. Cada oración va acompañada de sus números de línea correspondientes.

Para confirmar que todo salió como esperabas, carga el archivo de `process_output_files`:


```python
# carga la salida del proceso del archivo
with open(process_output["process_output_files"][0]) as f:
    print(json.dumps(json.load(f), indent=2))
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


### Como Usar un Modelo No-Predeterminado

Para usar un modelo [no-predeterminado](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md#modelos-disponibles-en-el-modulo-parser) como `fixed` debes especificarlo a través del argumento opcional [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) al usar el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md). Ten en cuenta que si no especificas parámetros para el modelo `fixed`, que sí es parametrizable, se usarán valores predeterminados:


```python
# procesa el archivo con un modelo no-predeterminado
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_muy_corto.txt",  # todos los argumentos (salvo modules) son iguales que antes
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,
    wait_for_process=True,
    verbose=False,
    modules={
        "parser": {"model": "fixed", "params": {"chunk_size": 9, "overlap_size": 3}}
    },  # especifica un modelo no-predeterminado (y sus parámetros) para este proceso
)
```

Puedes detallar el texto ahora fragmentado si cargas el archivo de salida. El código que sigue es un ejemplo de cómo hacerlo.

Al examinar la salida puedes ver que el documento de entrada no se dividió en oraciones completas sino en fragmentos de texto según los parámetros definidos. Cada fragmento tiene nueve palabras, y los fragmentos consecutivos se superponen por tres palabras. El modelo parametrizado funcionó correctamente.


```python
# cargar la salida del proceso del archivo
with open(process_output["process_output_files"][0]) as f:
    print(json.dumps(json.load(f), indent=2))
```

    [
      {
        "snippet": "It was a bright cold day in April, and",
        "line_numbers": [
          1
        ]
      },
      {
        "snippet": "in April, and the clocks were striking thirteen. Winston",
        "line_numbers": [
          1,
          2
        ]
      },
      {
        "snippet": "striking thirteen. Winston Smith, his chin nuzzled into his",
        "line_numbers": [
          1,
          2
        ]
      },
      {
        "snippet": "nuzzled into his breast in an effort to escape",
        "line_numbers": [
          2
        ]
      },
      {
        "snippet": "effort to escape the vile wind, slipped quickly through",
        "line_numbers": [
          2,
          3
        ]
      },
      {
        "snippet": "slipped quickly through the glass doors of Victory Mansions,",
        "line_numbers": [
          3
        ]
      },
      {
        "snippet": "of Victory Mansions, though not quickly enough to prevent",
        "line_numbers": [
          3,
          4
        ]
      },
      {
        "snippet": "enough to prevent a swirl of gritty dust from",
        "line_numbers": [
          4
        ]
      },
      {
        "snippet": "gritty dust from entering along with him.",
        "line_numbers": [
          4,
          5
        ]
      }
    ]

