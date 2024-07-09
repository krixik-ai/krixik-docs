<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/search_pipeline_examples/multi_snippet_semantic_search.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>


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


## *Pipeline* Multimodular: Búsqueda Semántica Sobre Fragmentos

Este documento detalla un *pipeline* multimodular que recibe fragmentos de texto en un archivo JSON y habilita [`búsqueda semántica`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) sobre ellos.

El documento se divide en las siguientes secciones:

- [Monta tu *Pipeline*](#monta-tu-pipeline)
- [Procesa un Archivo de Entrada](#procesa-un-archivo-de-entrada)
- [Búsqueda Semántica](#busqueda-semantica)

### Monta tu *Pipeline*

Para lograr lo arriba descrito, monta un pipeline que consiste de los siguientes módulos en secuencia:

- Un módulo [`text-embedder` (encaje léxico)](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md).

- Un módulo [`vector-db` (base de datos vectorial)](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md).

Para esto usarás el método [`create_pipeline`](../../sistema/creacion_de_pipelines/creacion_de_pipelines.md) de la siguiente manera:


```python
# crear el pipeline descrito
pipeline = krixik.create_pipeline(name="multi_busqueda_semantica_sobre_fragmentos",
                                  module_chain=["text-embedder", "vector-db"])
```

### Procesa un Archivo de Entrada

El formato de entrada de este *pipeline* es un archivo JSON (dado que ese es el formato de entrada de su [primer módulo](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md)). Las entradas JSON siempre deben seguir un [formato específico](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/formato_JSON_entrada.md); de lo contrario, el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) no funcionará.

Examina el archivo de prueba antes de continuar:


```python
# examina el archivo de entrada
with open(data_dir + "input/1984_fragmentos.json", "r") as file:
    print(file.read())
```

    [{"snippet": "It was a bright cold day in April, and the clocks were striking thirteen.", "line_numbers": [1]}, {"snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.", "line_numbers": [2, 3, 4, 5]}]


Usarás los modelos predeterminados en este *pipeline*, así que el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) no hará falta.


```python
# procesa el archivo a través del pipeline según lo arriba descrito
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_fragmentos.json",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False, # no mostrar actualizaciones de proceso al ejecutar el código
)
```

Reproduce la salida de este proceso con el siguiente código. Para aprender más sobre cada componente de la salida, estudia la documentación del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).

Dado que la salida de este modelo/módulo es un archivo de base de datos [FAISS](https://github.com/facebookresearch/faiss), `process_output` se muestra como "null". Sin embargo, el archivo de salida se ha guardado en la ubicación indicada bajo `process_output_files`. El `file_id` del archivo procesado es el prefijo del nombre del archivo de salida en esta ubicación.


```python
# nítidamente reproduce la salida de este proceso
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "multi_snippets_semantic_search",
      "request_id": "df80b7bd-d593-4cdd-bc39-4d2bdd18788e",
      "file_id": "f52906bb-eca6-408c-a929-504ea8954e76",
      "message": "SUCCESS - output fetched for file_id f52906bb-eca6-408c-a929-504ea8954e76.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/f52906bb-eca6-408c-a929-504ea8954e76.faiss"
      ]
    }


### Busqueda Semantica

El método [`semantic_search`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) de Krixik habilita búsqueda semántica sobre documentos procesados a través de ciertos *pipelines*. Dado que el método [`semantic_search`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) hace [`embedding` (encaje léxico)](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md) con la consulta y luego lleva a cabo la búsqueda, solo se puede usar con *pipelines* que de manera consecutiva contienen los módulos [`text-embedder` (encaje léxico)](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md) y [`vector-db` (base de datos vectorial)](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md).

Ya que tu *pipeline* satisface esta condición tiene acceso al método [`semantic_search`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md). Úsalo de la siguiente manera para consultar el texto con lengua natural:


```python
# haz búsqueda semántica sobre el texto procesado por el pipeline
semantic_output = pipeline.semantic_search(query="it was cold night", file_ids=[process_output["file_id"]])

# nítidamente reproduce la salida de esta búsqueda
print(json.dumps(semantic_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "4df32bdf-bb82-44d4-8151-ffaf2fc99c18",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "f52906bb-eca6-408c-a929-504ea8954e76",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_xongatwbce.json",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 2,
            "created_at": "2024-06-05 15:31:41",
            "last_updated": "2024-06-05 15:31:41"
          },
          "search_results": [
            {
              "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
              "line_numbers": [
                1
              ],
              "distance": 0.236
            },
            {
              "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
              "line_numbers": [
                2,
                3,
                4,
                5
              ],
              "distance": 0.429
            }
          ]
        }
      ]
    }



```python
# elimina todos los datos procesados pertenecientes a este pipeline
reset_pipeline(pipeline)
```
