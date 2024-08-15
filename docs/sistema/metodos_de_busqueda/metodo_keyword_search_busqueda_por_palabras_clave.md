<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/search_methods/keyword_search_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## El Método `keyword_search` (Búsqueda por Palabras Clave)

El método `keyword_search` de Krixik habilita búsqueda por palabras clave sobre documentos procesados a través de ciertos *pipelines*. La búsqueda por palabras clave es algo que los usuarios de internet conocen hace mucho tiempo: una serie de palabras es enviado como la consulta (*the query*), y la búsqueda devuelve toda aparición de cada una de esas palabras. Es muy diferente a [búsqueda semántica](metodo_semantic_search_busqueda_semantica.md).

El método `keyword_search` solo se puede usar con *pipelines* que terminan con el módulo [`keyword-db`](../../modulos/modulos_de_bases_de_datos/modulo_keyword-db_base_de_datos_de_palabras_clave.md).

Esta introducción al método `keyword_search` se divide en las siguientes secciones:

- [Argumentos del Método keyword_search](#argumentos-del-metodo-keyword_search)
- [Ejemplo de Montaje de Pipeline y Procesamiento de Archivo](#ejemplo-de-montaje-de-pipeline-y-procesamiento-de-archivo)
- [Ejemplos de Búsquedas por Palabras Clave](#ejemplos-de-busquedas-por-palabras-clave)
- [Límite de Tamaño de Salidas](#limite-de-tamano-de-salidas)
- [Stop Words (Palabras Ignoradas)](#stop-words-palabras-ignoradas)

### Argumentos del Metodo `keyword_search`

El método `keyword_search` toma un argumento requerido y al menos uno de varios argumentos opcionales. El argumento requerido es:

- `query` (str) - Un *string* que contiene una o más palabras clave separadas por espacios o guiones. Estas palabras se buscarán individualmente en el documento señalado.

Los argumentos opcionales son los mismos argumentos que el método [`list`](../sistema_de_archivos/metodo_list_lista.md) recibe—tanto los de metadata como las marcas de tiempo—así que [detállalos aquí](../sistema_de_archivos/metodo_list_lista.md#argumentos-del-metodo-list-lista) si es necesario. Al igual que con el método [`list`](../sistema_de_archivos/metodo_list_lista.md), puedes hacer `keyword_search` sobre varios archivos a la vez porque todos los argumentos de metadata se envían al método `keyword_search` en formato de lista. Todos los elementos de los argumentos opcionales son iguales que para el método [`list`](../sistema_de_archivos/metodo_list_lista.md), incluyendo el operador comodín * y la raíz global.

Si no está presente ninguno de estos argumentos opcionales, el método `keyword_search` no funcionará porque no hay dónde buscar.

Como el método [`list`](../sistema_de_archivos/metodo_list_lista.md), el método `keyword_search` acepta los argumentos opcionales `max_files` y `sort_order`, aunque su función cambia un poco:

- `max_files` especifica en hasta cuántos archivos se debe buscar. Su valor predeterminado no existe; no habría un máximo.

- `sort_order` acá toma dos valores posibles: 'ascending' y 'descending'. Esto determina en qué orden se devuelven los archivos sobre los que se ha buscado (en cuanto a su marca de tiempo de creación), pero los resultados de palabra clave dentro de cada archivo se devuelven siempre en el orden en que aparecen en el texto. Su valor predeterminado es 'descending'.

### Ejemplo de Montaje de Pipeline y Procesamiento de Archivo

Para los ejemplos de este documento usarás un *pipeline* que consiste de un solo módulo [`keyword-db`](../../modulos/modulos_de_bases_de_datos/modulo_keyword-db_base_de_datos_de_palabras_clave.md). Este es el *pipeline* básico de búsqueda por palabras clave. Usa el método [`create_pipeline`](../creacion_de_pipelines/creacion_de_pipelines.md) para crear el *pipeline*:


```python
# crea el pipeline básico para búsqueda por palabras clave
pipeline = krixik.create_pipeline(name="metodo_keyword_search_1_keyword-db",
                                  module_chain=["keyword-db"])
```

Ahora que el *pipeline* está listo puedes [`procesar`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) algunos archivos de texto a través de él para que tengas documentos sobre los cuales puedas hacer búsquedas:


```python
# agrega cuatro archivos al pipeline que acabas de crear
salida_1 = pipeline.process(
    local_file_path=data_dir + "input/frankenstein_muy_corto.txt",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False, # no mostrar actualizaciones de proceso al ejecutar el código
    symbolic_directory_path="/novelas/gotica",
    file_name="Frankenstein.txt",
)

salida_2 = pipeline.process(
    local_file_path=data_dir + "input/orgullo_y_prejuicio_muy_corto.txt",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False, # no mostrar actualizaciones de proceso al ejecutar el código
    symbolic_directory_path="/novelas/romance",
    file_name="Pride and Prejudice.txt",
)

salida_3 = pipeline.process(
    local_file_path=data_dir + "input/moby_dick_muy_corto.txt",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False, # no mostrar actualizaciones de proceso al ejecutar el código
    symbolic_directory_path="/novelas/aventura",
    file_name="Moby Dick.txt",
)

salida_4 = pipeline.process(
    local_file_path=data_dir + "input/mujercitas_muy_corto.txt",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False, # no mostrar actualizaciones de proceso al ejecutar el código
    symbolic_directory_path="/novelas/bildungsroman",
    file_name="Little Women.txt",
)
```

Examina la salida de uno de estos:


```python
# nítidamente reproduce la salida de este proceso
print(json.dumps(salida_3, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "keyword_search_method_1_keyword-db",
      "request_id": "4763d881-46e0-4d34-857b-bdd4cdf43aab",
      "file_id": "ae071414-7192-4f78-a431-1a13c0f0bc4a",
      "message": "SUCCESS - output fetched for file_id ae071414-7192-4f78-a431-1a13c0f0bc4a.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/ae071414-7192-4f78-a431-1a13c0f0bc4a.db"
      ]
    }


Dado que la salida de este modelo/módulo es un archivo de base de datos `SQLlite`, `process_output` se muestra como "null". Esa base de datos consiste de todas las tuplas de palabras claves (palabra clave, número de línea, número de palabra) identificadas en el archivo, así que no se puede reproducir aquí. Sin embargo, el archivo de salida se ha guardado en la ubicación indicada bajo `process_output_files`. El `file_id` del archivo procesado es el prefijo del nombre del archivo de salida en esta ubicación.

### Ejemplos de Busquedas por Palabras Clave

Ahora que has procesado archivos por el *pipeline* puedes usar el método `keyword_search` sobre él.

Con el siguiente código puedes buscar una serie de palabras en uno de los archivos:


```python
# haz keyword_search sobre un archivo
keyword_output = pipeline.keyword_search(query="mansion adolescence party enemy romance",
                                         file_names=["Little Women.txt"])

# nítidamente reproduce la salida de este proceso
print(json.dumps(keyword_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "5b252162-6ee5-4a48-ae62-f9954f4107f5",
      "message": "",
      "warnings": [
        {
          "WARNING: the following file_ids returned no results for the given query": [
            "001dd7c5-87f6-4ffa-a647-060291d9679d"
          ]
        }
      ],
      "items": []
    }


El método `keyword_search` devuelve cada aparición de cada palabra clave buscada. Como puedes ver, para cada archivo sobre el que buscaste hay un registro para cada aparición de palabra clave. El registro indica el número de línea y el número de palabra dentro de esa línea.

Funciona igual de bien cuando buscas sobre varios archivos con el [operador comodín](../sistema_de_archivos/metodo_list_lista.md#argumentos-con-el-operador-comodin):


```python
# hacer keyword_search sobre varios archivos
keyword_output = pipeline.keyword_search(query="mansion adolescence party enemy romance",
                                         symbolic_directory_paths=["/novelas*"])

# nítidamente reproduce la salida de este proceso
print(json.dumps(keyword_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "5e53f349-ed65-4735-a288-d2effbb447a5",
      "message": "Successfully queried the first 1 user file out of 4 defined by input query arguments.",
      "warnings": [
        {
          "WARNING: the following file_ids returned no results for the given query": [
            "ae071414-7192-4f78-a431-1a13c0f0bc4a",
            "f59be5e9-2bd3-4a07-8a7e-1a52064c6ee1",
            "001dd7c5-87f6-4ffa-a647-060291d9679d"
          ]
        }
      ],
      "items": [
        {
          "file_id": "786baed5-66ff-4bf4-941f-0baa562e9666",
          "file_metadata": {
            "file_name": "pride and prejudice.txt",
            "symbolic_directory_path": "/novels/romance",
            "file_tags": [],
            "num_lines": 40,
            "created_at": "2024-06-05 16:18:15",
            "last_updated": "2024-06-05 16:18:15"
          },
          "search_results": [
            {
              "keyword": "party",
              "line_number": 23,
              "keyword_number": 8
            }
          ]
        }
      ]
    }


### Limite de Tamano de Salidas

El límite actual sobre salidas generadas por el método `list` es 5MB.

### Stop Words (Palabras Ignoradas)

"Stop words", o "palabras ignoradas", son las palabras que la búsqueda por palabras clave ignora. Hay palabras en los idiomas que son tan comunes y frecuentemente usadas (p.ej. en inglés "the" y "and") que asumimos que el usuario no las buscará. Por ende, el método `keyword_search` se las salta si están en la consulta (*the query*), lo cual produce resultados más enfocados. Por ahora no hay manera de hacer búsqueda por palabras clave por cualquier palabra en la lista de "stop words", lista que puedes ver en la salida del siguiente código:


```python
with open(data_dir + "other/stop_words.txt", "r") as file:
    print(file.read())
```

    stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

