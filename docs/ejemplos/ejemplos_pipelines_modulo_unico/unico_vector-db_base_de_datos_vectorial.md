<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/single_module_pipelines/single_vector-db.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## *Pipeline* de Módulo Único: `vector-db` (Base de Datos Vectorial)

Este documento presenta una guía de cómo ensamblar y consumir un *pipeline* de módulo único que solo incluye un módulo [`vector-db` (base de datos vectorial)](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md).

Ten en cuenta que usar este módulo como módulo único no genera un *pipeline* particularmente fácil de usar, dado que por separado debes tener los archivos NPY que procesarás. Sugerimos detallar este [ejemplo de *pipeline*](../ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_basica.md) y este [otro ejemplo de *pipeline*](../ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_sobre_fragmentos.md), que respectivamente toman archivos de entrada TXT y JSON y habilitan [búsqueda semántica](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) (también llamada búsqueda vectorial) sobre ellos.

El documento se divide en las siguientes secciones:

- [Monta tu *Pipeline*](#monta-tu-pipeline)
- [Formato de Entrada Requerido](#formato-de-entrada-requerido)
- [Cómo Usar el Modelo Predeterminado](#como-usar-el-modelo-predeterminado)
- [El Método `semantic_search`](#el-metodo-semantic_search)
- [Consulta Bases de Datos de Salida Localmente](#consulta-bases-de-datos-de-salida-localmente)

### Monta tu *Pipeline*

Primero crea un *pipeline* de módulo único con un módulo [`vector-db` (base de datos vectorial)](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md).

Usa el método [`create_pipeline`](../../sistema/creacion_de_pipelines/creacion_de_pipelines.md) para esto, incluyendo solamente una referencia de módulo [`vector-db`](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md) en el argumento `module_chain`.


```python
# crea un pipeline con un solo módulo vector-db
pipeline = krixik.create_pipeline(name="unico_vector-db_1",
                                  module_chain=["vector-db"])
```

### Formato de Entrada Requerido

El módulo [`vector-db` (base de datos vectorial)](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md) acepta archivos NPY como entradas. Estos archivos consisten de un solo arreglo NumPy. Cada fila del arreglo es un vector que el módulo [`vector-db`](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md) luego indexa para búsqueda semántica (también conocida como búsqueda vectorial).

Antes de procesar un archivo de entrada—uno válido para este *pipeline*—examínalo con el siguiente código:


```python
# examina el contenido de un archivo de entrada válido
import numpy as np

np.load(data_dir + "input/vectores.npy")
```




    array([[0, 1],
           [1, 0],
           [1, 1]])



### Como Usar el Modelo Predeterminado

Ahora procesa el archivo usando el modelo [predeterminado](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md#modelos-disponibles-en-el-modulo-vector-db) del módulo [`vector-db`](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md): [`faiss`](https://github.com/facebookresearch/faiss). Por lo pronto, este es el único modelo en este módulo.

Dado que este es el modelo predeterminado, no hace falta que especifiques qué modelo quieres usar a través del argumento opcional [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).


```python
# procesa el archivo con el modelo predeterminado
process_output = pipeline.process(
    local_file_path=data_dir + "input/vectores.npy",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False, # no mostrar actualizaciones de proceso al ejecutar el código
)
```

La salida del proceso se reproduce con el siguiente código. Para aprender más sobre cada componente de esta salida, revisa la documentación del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).

Dado que la salida de este modelo/módulo es un archivo de base de datos [FAISS](https://github.com/facebookresearch/faiss), `process_output` se muestra como "null". Sin embargo, el archivo de salida se ha guardado en la ubicación indicada bajo `process_output_files`. El `file_id` del archivo procesado es el prefijo del nombre del archivo de salida en esta ubicación.


```python
# nítidamente reproduce la salida de este proceso
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "modules-vector-db-docs",
      "request_id": "536c9e0b-41ed-4c41-99dc-11cdabf32ecc",
      "file_id": "63c88fdc-8b62-4f74-af20-c4816ee0bb88",
      "message": "SUCCESS - output fetched for file_id 63c88fdc-8b62-4f74-af20-c4816ee0bb88.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/63c88fdc-8b62-4f74-af20-c4816ee0bb88.faiss"
      ]
    }


### El Metodo `semantic_search`

Cualquier *pipeline* que contiene un módulo [`vector-db`](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md) precedido de un módulo [`text-embedder`](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md) tiene acceso al método [`semantic_search`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md). Este te permite hacer búsqueda semántica sobre las bases de datos vectoriales que has creado.

Dado que el *pipeline* de módulo único que acabas de crear carece de un módulo [`text-embedder`](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md), el método [`semantic_search`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) no funcionará con él. Revisa la documentación de [este ejemplo](../../ejemplos/ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_basica.md) de *pipeline* o de [este otro ejemplo](../../ejemplos/ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_sobre_fragmentos.md) de *pipeline*, los cuales cumplen los requerimientos para este método: el primero recibe archivos TXT, y el segundo recibe archivos JSON.

### Consulta Bases de Datos de Salida Localmente

Además de lo que ofrece el método [`semantic_search`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md), puedes  hacer consultas **localmente** sobre las bases de datos vectoriales que has generado y que cuya ubicación está indicada en `process_output_files`.

La siguiente es una función para localmente hacer búsquedas semánticas sobre el archivo de base de datos antes devuelto.

Nota: Para ejecutar el siguiente código tendrás que instalar la librería `FAISS`. Dependiendo de tus especificaciones locales, instala [faiss-cpu](https://pypi.org/project/faiss-cpu/) o [faiss-gpu](https://pypi.org/project/faiss-gpu/).


```python
# asegúrate que has instalado faiss (faiss-cpu or faiss-gpu)
!pip install faiss-cpu
import faiss
import numpy as np
from typing import Tuple


def query_vector_db(query_vector: np.ndarray, k: int, db_file_path: str) -> Tuple[list, list]:
    # subir base de datos vectorial
    faiss_index = faiss.read_index(db_file_path)

    # ejecutar consulta
    similarities, indices = faiss_index.search(query_vector, k)
    distances = 1 - similarities
    return distances, indices
```

    Requirement already satisfied: faiss-cpu in /Users/jeremywatt/Desktop/krixik/code/krixik-docs/docs_venv/lib/python3.10/site-packages (1.8.0)
    Requirement already satisfied: numpy in /Users/jeremywatt/Desktop/krixik/code/krixik-docs/docs_venv/lib/python3.10/site-packages (from faiss-cpu) (1.26.4)
    
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip is available: [0m[31;49m23.3.1[0m[39;49m -> [0m[32;49m24.0[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m


Ahora consulta tu base de datos con la función anterior y un pequeño arreglo de prueba. Los resultados están reproducidos tras el siguiente código:


```python
# haz una búsqueda de prueba con la funcion de búsqueda arriba presentada
original_vectors = np.load(data_dir + "input/vectores.npy")
query_vector = np.array([[0, 1]])
distances, indices = query_vector_db(query_vector, 2, process_output["process_output_files"][0])
print(f"vector de entrada de consulta: {query_vector[0]}")
print(f"vector más cercano al original: {original_vectors[indices[0][0]]}")
print(f"distancia del vector de búsqueda a este vector: {distances[0][0]}")
print(f"segundo vector más cercano al original: {original_vectors[indices[0][1]]}")
print(f"distancia del vector de búsqueda a este vector: {distances[0][1]}")
```

    input query vector: [0 1]
    closest vector from original: [0 1]
    distance from query to this vector: 0.0
    second closest vector from original: [1 1]
    distance from query to this vector: 0.2928932309150696

