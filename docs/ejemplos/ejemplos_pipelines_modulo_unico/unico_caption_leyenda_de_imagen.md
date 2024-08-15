<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/single_module_pipelines/single_caption.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## *Pipeline* de Módulo Único: `caption` (Leyenda de Imagen)
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/examples/single_module_pipelines/single_caption/)

Este documento presenta una guía de cómo ensamblar y consumir un *pipeline* de módulo único que solo incluye un módulo [`caption` (leyenda de imagen)](../../modulos/modulos_ia/modulo_caption_leyenda_de_imagen.md). Se divide en las siguientes secciones:

- [Monta tu *Pipeline*](#monta-tu-pipeline)
- [Formato de Entrada Requerido](#formato-de-entrada-requerido)
- [Cómo Usar el Modelo Predeterminado](#como-usar-el-modelo-predeterminado)
- [Cómo Usar un Modelo No-Predeterminado](#como-usar-un-modelo-no-predeterminado)

### Monta tu *Pipeline*

Primero crea un *pipeline* de módulo único con un módulo [`caption` (leyenda de imagen)](../../modulos/modulos_ia/modulo_caption_leyenda_de_imagen.md).

Usa el método [`create_pipeline`](../../sistema/creacion_de_pipelines/creacion_de_pipelines.md) para esto, incluyendo solamente una referencia de módulo [`caption`](../../modulos/modulos_ia/modulo_caption_leyenda_de_imagen.md) en el argumento `module_chain`.


```python
# crea un pipeline con un solo módulo caption
pipeline = krixik.create_pipeline(name="unico_caption_1", module_chain=["caption"])
```

### Formato de Entrada Requerido

El módulo [`caption` (leyenda de imagen)](../../modulos/modulos_ia/modulo_caption_leyenda_de_imagen.md) recibe como [entradas](../../modulos/modulos_ia/modulo_caption_leyenda_de_imagen.md#entradas-y-salidas-del-modulo-caption) archivos de imagen con formato PNG, JPG y JPEG.

Antes de procesar un archivo de entrada—uno válido para este *pipeline*—examínalo con el siguiente código:


```python
# examina el contenido de un archivo de entrada válido
from IPython.display import Image

Image(filename=data_dir + "input/restaurante.png")
```




    
![png](unico_caption_leyenda_de_imagen_files/unico_caption_leyenda_de_imagen_5_0.png)
    



### Como Usar el Modelo Predeterminado

Ahora procesa el archivo usando el modelo [predeterminado](../../modulos/modulos_ia/modulo_caption_leyenda_de_imagen.md#modelos-disponibles-en-el-modulo-caption) del módulo [`caption` (leyenda de imagen)](../../modulos/modulos_ia/modulo_caption_leyenda_de_imagen.md): [`vit-gpt2-image-captioning`](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning).

Dado que este es el modelo predeterminado, no hace falta que especifiques qué modelo quieres usar a través del argumento opcional [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).


```python
# procesa el archivo con el modelo predeterminado
process_output = pipeline.process(
    local_file_path=data_dir + "input/restaurante.png",  # la ruta de archivo inicial en la que yace el archivo de entrada
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
      "pipeline": "single_caption_1",
      "request_id": "db5e8352-fc0f-42f3-88e4-1b6388a42309",
      "file_id": "ab32fe99-5bf8-4712-aa39-b7af9fac27f6",
      "message": "SUCCESS - output fetched for file_id ab32fe99-5bf8-4712-aa39-b7af9fac27f6.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "caption": "a large group of people are in a restaurant"
        }
      ],
      "process_output_files": [
        "../../../data/output/ab32fe99-5bf8-4712-aa39-b7af9fac27f6.json"
      ]
    }


Para confirmar que todo salió como esperabas, carga el archivo de `process_output_files`:


```python
# carga la salida del proceso del archivo
with open(process_output["process_output_files"][0]) as f:
    print(json.dumps(json.load(f), indent=2))
```

    [
      {
        "caption": "a large group of people are in a restaurant"
      }
    ]


### Como Usar un Modelo No-Predeterminado

Para usar un modelo [no-predeterminado](../../modulos/modulos_ia/modulo_caption_leyenda_de_imagen.md#modelos-disponibles-en-el-modulo-caption) como [`blip-image-captioning-base`](https://huggingface.co/Salesforce/blip-image-captioning-base), debes especificarlo a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) al usar el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md):


```python
# procesa el archivo con un modelo no-predeterminado
process_output = pipeline.process(
    local_file_path=data_dir + "input/restaurante.png",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False,  # no mostrar actualizaciones de proceso al ejecutar el código
    modules={"caption": {"model": "blip-image-captioning-base"}},  # especifica un modelo no-predeterminado para este proceso
)
```

La salida del proceso se reproduce con el siguiente código.

Dado que la salida de este modelo/módulo es un archivo JSON, la salida también se incluye en el objeto (esto solo ese el caso para salidas JSON). Además, el archivo de salida se ha guardado en la ubicación indicada bajo `process_output_files`. El `file_id` del archivo procesado es el prefijo del nombre del archivo de salida en esta ubicación.


```python
# nítidamente reproduce la salida de este proceso
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_caption_1",
      "request_id": "c64ba8a0-4c19-4513-bf32-509b3be0319a",
      "file_id": "c290b26b-d02b-40f3-8112-06a595f3b924",
      "message": "SUCCESS - output fetched for file_id c290b26b-d02b-40f3-8112-06a595f3b924.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "caption": "a group of people sitting around a bar"
        }
      ],
      "process_output_files": [
        "../../../data/output/c290b26b-d02b-40f3-8112-06a595f3b924.json"
      ]
    }

