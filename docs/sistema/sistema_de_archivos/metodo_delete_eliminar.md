<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/file_system/delete_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>


```python
import os
import sys
import json
import importlib
from pathlib import Path

# preparación de demo - incuye instanciación de secretos, instalación de requerimientos, y definición de rutas
if os.getenv("COLAB_RELEASE_TAG"):
    # si estás usando este notebook en Google Colab, ingresa tus secretos acá
    MY_API_KEY = "TU_API_KEY_VA_AQUI"
    MY_API_URL = "TU_API_URL_VA_AQUI"

    # si estás usando este notebook en Google Colab, instala requerimientos y descarga los subdirectorios requeridos
    # instala el cliente Python de Krixik
    !pip install krixik

    # instala github-clone, que permite clonación fácil de los subdirectorios del repositorio de documentación XXX
    !pip install github-clone

    # clona los conjuntos de datos
    if not Path("data").is_dir():
        !ghclone XXXX #(in english it's https://github.com/krixik-ai/krixik-docs/tree/main/data)
    else:
        print("ya se clonaron los conjuntos de datos de documentación!")

    # define la variable 'data_dir' para tus rutas
    data_dir = "./data/"

    # crea directorio de salidas
    from pathlib import Path

    Path(data_dir + "/salidas").mkdir(parents=True, exist_ok=True)

    # descarga utilidades
    if not Path("utilities").is_dir():
        !ghclone XXXX # (in english it's https://github.com/krixik-ai/krixik-docs/tree/main/utilities)
    else:
        print("ya has clonado las utilidades de documentación!")
else:
    # si estás usando una descarga local de la documentación, define las rutas relativas a la estructura local de la documentación
    # importa utilidades
    sys.path.append("../../../")

    # define la variable 'data_dir' para tus rutas
    data_dir = "../../../data/"

    # si estás usando este notebook localmente desde el repositorio de documentación Krixik, carga tus secretos de un archivo .env ubicado en la base del repositorio de documentación
    from dotenv import load_dotenv

    load_dotenv("../../../.env")

    MY_API_KEY = os.getenv("MY_API_KEY")
    MY_API_URL = os.getenv("MY_API_URL")


# carga 'reset'
reset = importlib.import_module("utilities.reset")
reset_pipeline = reset.reset_pipeline


# importa Krixik e inicializa sesión con tus secretos personales
from krixik import krixik

krixik.init(api_key=MY_API_KEY, api_url=MY_API_URL)
```

    SUCCESS: You are now authenticated.


## El Método `delete` (Eliminar)

Puedes borrar todo registro de un archivo procesado del sistema Krixik con el método `delete` (eliminar). Esta es la versión manual de permitir que se venza el [`expire_time`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#argumentos-principales-del-metodo-process) de un archivo.

Esta introducción del método `delete` se divide en las siguientes secciones:

- [Argumentos del Método `delete`](#argumentos-del-metodo-delete)
- [Ejemplo del Método `delete`](#ejemplo-del-metodo-delete)

### Argumentos del Metodo `delete`

El método `delete` toma un argumento (requerido):

- `file_id` (str) - El `file_id` (identificador único) del archivo procesado cuyo registro quieres totalmente borrar de los servidores Krixik.

### Ejemplo del Metodo `delete`

Primero debes crear un *pipeline* sobre el cual puedas ejecutar este ejemplo. Un *pipeline* que consiste de un solo módulo [`parser`](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md) funciona bien.


```python
# crea un pipeline de módulo único con un módulo parser
pipeline = krixik.create_pipeline(name="metodo_delete_1_parser",
                                  module_chain=["parser"])
```

Ahora usa el método [`process`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) para procesar un archivo a través del *pipeline*:


```python
# procesa un breve archivo de entrada
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_muy_corto.txt",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False, # no mostrar actualizaciones de proceso al ejecutar el código
    symbolic_directory_path="/novelas/siglo-20",
    file_name="1984_muestra.txt",
    file_tags=[{"escritor": "Orwell"}, {"categoria": "distopia"}, {"siglo": "20"}],
)
```

Detalla el registro del archivo con el método [`list`](metodo_list_lista.md):


```python
# ve el registro del archivo con el método list
list_output = pipeline.list(symbolic_directory_paths=["/novelas/siglo-20"])

# nítidamente reproduce la salida de esta lista
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "46faf749-b758-42d7-8b82-f1f8e8dcb54d",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:31:35",
          "process_id": "0db7cc1d-06c9-13e3-483d-82255c145dd2",
          "created_at": "2024-06-05 15:31:35",
          "file_metadata": {
            "modules": {
              "module_1": {
                "parser": {
                  "model": "sentence"
                }
              }
            },
            "modules_data": {
              "module_1": {
                "parser": {
                  "data_files_extensions": [
                    ".json"
                  ],
                  "num_lines": 2
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "orwell"
            },
            {
              "category": "dystopian"
            },
            {
              "century": "20"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/20th-century",
          "pipeline": "delete_method_1_parser",
          "file_id": "ad927578-a8f1-4ace-acbc-3dee2391075c",
          "expire_time": "2024-06-05 16:01:35",
          "file_name": "1984_sample.txt"
        }
      ]
    }


El registro del archivo se refleja de manera adecuada.

Ahora usa el método `delete` y el `file_id` del archivo para borrar ese archivo:


```python
# elimina el registro y salida del archivo procesado con su file_id
delete_output = pipeline.delete(file_id=process_output["file_id"])

# nítidamente reproduce la salida de este proceso
print(json.dumps(delete_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "delete_method_1_parser",
      "request_id": "6e59e916-4233-4088-b85c-2dbe96425383",
      "message": "Successfully deleted file_id: ad927578-a8f1-4ace-acbc-3dee2391075c",
      "warnings": []
    }


Puedes confirmar que el archivo se ha eliminado con el método [`list`](metodo_list_lista.md) sobre el mismo `symbolic_directory_path`:


```python
#  usa list para confirmar que el archivo ha sido eliminado
list_output = pipeline.list(symbolic_directory_paths=["/novelas/siglo-20"])

# nítidamente reproduce la salida de este proceso
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "542fe670-ce77-4d33-b1ab-a6024c7360be",
      "message": "No files were found for the given query arguments",
      "warnings": [
        {
          "WARNING: the following arguments returned zero results": [
            {
              "symbolic_directory_paths": [
                "/novels/20th-century"
              ]
            }
          ]
        }
      ],
      "items": []
    }


Verás que el archivo previamente [`procesado`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) ya no aparece, pues ha sido eliminado.


```python
# elimina todos los datos procesados pertenecientes a este pipeline
reset_pipeline(pipeline)
```
