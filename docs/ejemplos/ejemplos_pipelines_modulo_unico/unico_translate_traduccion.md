<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/single_module_pipelines/single_translate.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## *Pipeline* de Módulo Único: `translate` (Traducción)
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/examples/single_module_pipelines/single_translate/)

Este documento presenta una guía de cómo ensamblar y consumir un *pipeline* de módulo único que solo incluye un módulo [`translate` (traducción)](../../modulos/modulos_ia/modulo_translate_traduccion.md). Se divide en las siguientes secciones:

- [Monta tu *Pipeline*](#monta-tu-pipeline)
- [Formato de Entrada Requerido](#formato-de-entrada-requerido)
- [Cómo Usar el Modelo Predeterminado](#como-usar-el-modelo-predeterminado)
- [Cómo Usar un Modelo No-Predeterminado](#como-usar-un-modelo-no-predeterminado)

### Monta tu *Pipeline*

Primero crea un *pipeline* de módulo único con un módulo [`translate` (traducción)](../../modulos/modulos_ia/modulo_translate_traduccion.md).

Usa el método [`create_pipeline`](../../sistema/creacion_de_pipelines/creacion_de_pipelines.md) para esto, incluyendo solamente una referencia de módulo [`translate`](../../modulos/modulos_ia/modulo_translate_traduccion.md) en el argumento `module_chain`.


```python
# crea un pipeline con un solo módulo translate
pipeline = krixik.create_pipeline(name="unico_translate_1", module_chain=["translate"])
```

### Formato de Entrada Requerido

El módulo [`translate` (traducción)](../../modulos/modulos_ia/modulo_translate_traduccion.md) recibe entradas con formato JSON. Las entradas JSON deben respetar [esta estructura](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/formato_JSON_entrada.md).

Antes de procesar un archivo de entrada—uno válido para este *pipeline*—examínalo con el siguiente código:


```python
# examina el contenido de un archivo de entrada válido
with open(data_dir + "input/valido.json", "r") as file:
    print(json.dumps(json.load(file), indent=2))
```

    [
      {
        "snippet": "I love this movie and i would watch it again and again!"
      },
      {
        "snippet": "Operating profit totaled EUR 9.4 mn, down from EUR 11.7 mn in 2004."
      }
    ]


### Como Usar el Modelo Predeterminado

Ahora procesa el archivo usando el modelo [predeterminado](../../modulos/modulos_ia/modulo_translate_traduccion.md#modelos-disponibles-en-el-modulo-translate) del módulo [`translate` (traducción)](../../modulos/modulos_ia/modulo_translate_traduccion.md), que traduce de inglés a español: [`opus-mt-en-es`](https://huggingface.co/Helsinki-NLP/opus-mt-en-es).

Dado que este es el modelo predeterminado, no hace falta que especifiques qué modelo quieres usar por medio del argumento opcional [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).


```python
# procesa el archivo con el modelo predeterminado
process_output = pipeline.process(
    local_file_path=data_dir + "input/valido.json",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False,  # no mostrar actualizaciones de proceso al ejecutar el código
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
      "pipeline": "single_translate_1",
      "request_id": "6e87fa96-3fea-49f9-9ef3-897cc226f94c",
      "file_id": "a2439789-e57d-4cd1-a91e-ab1907edd2a5",
      "message": "SUCCESS - output fetched for file_id a2439789-e57d-4cd1-a91e-ab1907edd2a5.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "Me encanta esta pelcula y la vea una y otra vez!"
        },
        {
          "snippet": "El beneficio de explotacin ascendi a 9,4 millones EUR, frente a 11,7 millones EUR en 2004."
        }
      ],
      "process_output_files": [
        "../../../data/output/a2439789-e57d-4cd1-a91e-ab1907edd2a5.json"
      ]
    }


Para confirmar que todo salió como esperabas, carga el archivo de `process_output_files`:


```python
# load in process output from file
with open(process_output["process_output_files"][0]) as f:
    print(json.dumps(json.load(f), indent=2))
```

    [
      {
        "snippet": "Me encanta esta pelcula y la vea una y otra vez!"
      },
      {
        "snippet": "El beneficio de explotacin ascendi a 9,4 millones EUR, frente a 11,7 millones EUR en 2004."
      }
    ]


### Como Usar un Modelo No-Predeterminado

Para usar un modelo [no-predeterminado](../../modulos/modulos_ia/modulo_translate_traduccion.md#modelos-disponibles-en-el-modulo-translate) como [`opus-mt-es-en`](https://huggingface.co/Helsinki-NLP/opus-mt-es-en), que traduce de español a inglés, debes especificarlo a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) al usar el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md):


```python
# procesa el archivo con un modelo no-predeterminado
process_output = pipeline.process(
    local_file_path=data_dir + "input/espanol_valido.json",  # todos los argumentos (salvo modules) son iguales que antes
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,
    wait_for_process=True,
    verbose=False,
    modules={"translate": {"model": "opus-mt-es-en"}},  # especifica un modelo no-predeterminado para este proceso
)
```

Puedes usar código como el anterior para reproducir y revisar la salida de este proceso:


```python
# nítidamente reproduce la salida de este proceso
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_translate_1",
      "request_id": "b65ab7cf-7aee-4c95-95da-d2d0f9c78679",
      "file_id": "cd6a91a1-a82d-4e16-be6c-18ce71fdd3f0",
      "message": "SUCCESS - output fetched for file_id cd6a91a1-a82d-4e16-be6c-18ce71fdd3f0.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "I love this movie and see it over and over again!"
        },
        {
          "snippet": "The operating profit amounted to EUR 9,4 million, compared with EUR 11,7 million in 2004."
        }
      ],
      "process_output_files": [
        "../../../data/output/cd6a91a1-a82d-4e16-be6c-18ce71fdd3f0.json"
      ]
    }



```python
# elimina todos los datos procesados pertenecientes a este pipeline
krixik.reset_pipeline(pipeline)
```
