<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/search_pipeline_examples/multi_keyword_searchable_transcription.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## *Pipeline* Multimodular: Búsqueda por Palabras Clave sobre Transcripción

Este documento detalla un *pipeline* multimodular que recibe un archivo de audio como entrada, lo [`transcribe`](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md), y habilita [`búsqueda por palabras clave`](../../sistema/metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md) sobre la transcripción.

El documento se divide en las siguientes secciones:

- [Monta tu *Pipeline*](#monta-tu-pipeline)
- [Procesa un Archivo de Entrada](#procesa-un-archivo-de-entrada)
- [Búsqueda por Palabras Clave](#busqueda-por-palabras-clave)

### Monta tu *Pipeline*

Para lograr lo arriba descrito, monta un pipeline que consiste de los siguientes módulos en secuencia:

- Un módulo [`transcribe` (transcripción)](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md).

- Un módulo [`json-to-txt`](../../modulos/modulos_de_funciones_de_apoyo/modulo_json-to-txt.md).

- Un módulo [`keyword-db` (base de datos de palabras clave)](../../modulos/modulos_de_bases_de_datos/modulo_keyword-db_base_de_datos_de_palabras_clave.md).

Para esto usarás el método [`create_pipeline`](../../sistema/creacion_de_pipelines/creacion_de_pipelines.md) de la siguiente manera:


```python
# creación del pipeline descrito
pipeline = krixik.create_pipeline(name="multi_busqueda_por_palabras_clave_transcripcion",
                                  module_chain=["transcribe", "json-to-txt", "keyword-db"])
```

### Procesa un Archivo de Entrada

Examina el archivo de prueba antes de continuar:


```python
# examina el archivo de entrada
import IPython

IPython.display.Audio(data_dir + "input/video_Colombia.mp3")
```





<audio  controls="controls" >
    Your browser does not support the audio element.
</audio>




Usarás los modelos predeterminados en este *pipeline*, así que el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) no hará falta.


```python
# procesa el archivo a través del pipeline según lo arriba descrito
process_output = pipeline.process(
    local_file_path=data_dir + "input/video_Colombia.mp3",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False, # no mostrar actualizaciones de proceso al ejecutar el código
)
```

Reproduce la salida de este proceso con el siguiente código. Para aprender más sobre cada componente de la salida, estudia la documentación del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).

Dado que la salida de este modelo/módulo es un archivo de base de datos `SQLlite`, `process_output` se muestra como "null". Sin embargo, el archivo de salida se ha guardado en la ubicación indicada bajo `process_output_files`. El `file_id` del archivo procesado es el prefijo del nombre del archivo de salida en esta ubicación.


```python
# nítidamente reproduce la salida de este proceso
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "multi_keyword_searchable_transcription",
      "request_id": "4932e263-585e-47e2-859f-6a65c7b23d53",
      "file_id": "6b4d7dc2-4010-4f8b-9a18-9b54ed8c14dd",
      "message": "SUCCESS - output fetched for file_id 6b4d7dc2-4010-4f8b-9a18-9b54ed8c14dd.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/6b4d7dc2-4010-4f8b-9a18-9b54ed8c14dd.db"
      ]
    }


### Busqueda por Palabras Clave

El método [`keyword_search` (búsqueda por palabras clave)](../../sistema/metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md) de Krixik habilita búsqueda por palabras clave sobre documentos procesados a través de *pipelines* que terminan con el módulo [`keyword-db` (base de datos de palabras clave)](../../modulos/modulos_de_bases_de_datos/modulo_keyword-db_base_de_datos_de_palabras_clave.md).

Dado que tu *pipeline* satisface esta condición tiene acceso al método [`keyword_search`](../../sistema/metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md). Úsalo de la siguiente manera para buscar palabras clave en la transcripción que se generó con base en el audio:


```python
# haz búsqueda por palabras clave sobre la transcripción generada con base en el audio procesado por el pipeline
keyword_output = pipeline.keyword_search(query="lets talk about the country of Colombia",
                                         file_ids=[process_output["file_id"]])

# nítidamente reproduce la salida de esta búsqueda
print(json.dumps(keyword_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "c63d8207-0c12-43ca-8f87-cbc3c00c0883",
      "message": "Successfully queried 1 user file.",
      "warnings": [
        {
          "WARNING: the following words in the query are in the stop_words list and thus no results will be returned for them": [
            "about",
            "the",
            "of"
          ]
        }
      ],
      "items": [
        {
          "file_id": "6b4d7dc2-4010-4f8b-9a18-9b54ed8c14dd",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_yngkbbnerk.mp3",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_lines": 1,
            "created_at": "2024-06-05 14:50:54",
            "last_updated": "2024-06-05 14:50:54"
          },
          "search_results": [
            {
              "keyword": "country",
              "line_number": 1,
              "keyword_number": 7
            },
            {
              "keyword": "talk",
              "line_number": 1,
              "keyword_number": 118
            },
            {
              "keyword": "countries",
              "line_number": 1,
              "keyword_number": 142
            }
          ]
        }
      ]
    }
