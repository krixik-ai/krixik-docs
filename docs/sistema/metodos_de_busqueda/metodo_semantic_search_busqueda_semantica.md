<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/search_methods/semantic_search_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>


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


## El Método `semantic_search` (Búsqueda Semántica)

El método `semantic_search` de Krixik habilita búsqueda semántica sobre documentos procesados a través de ciertos *pipelines*. Mucho se ha escrito sobre la búsqueda semántica, pero en breve, en vez de buscar palabras clave en un documento, este método busca texto que es similar en _significado_ al *string* que se ha enviado. Esto es diferente a lo que ofrece el [`keyword_search`](metodo_keyword_search_busqueda_por_palabras_clave.md).

Dado que el método `semantic_search` hace [`encaje léxico`](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md) con el *string* enviado (*the query*) y también hace la búsqueda, solo se puede usar con *pipelines* que contienen un módulo [`text embedder` (encaje léxico)](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md) y un módulo [`vector-db` (base de datos vectorial)](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md) en secuencia inmediata.

Esta introducción al método `semantic_search` está dividida en las siguientes secciones:

- [Argumentos del Método `semantic_search`](#argumentos-del-metodo-semantic_search)
- [Ejemplo de Montaje de Pipeline y Procesamiento de Archivo](#ejemplo-de-montaje-de-pipeline-y-procesamiento-de-archivo)
- [Ejemplos de Búsqueda Semántica](#ejemplos-de-busqueda-semantica)
- [Límite de Tamaño de Salidas](#limite-de-tamano-de-salidas)

### Argumentos del Metodo `semantic_search`

El método `semantic_search` toma un argumento requerido y al menos uno de varios argumentos opcionales. El argumento requerido es:

- `query` (str) - Un *string* cuyo significado será el objeto de búsqueda en el documento señalado. Las coincidencias más cercanas (es decir, los fragmentos que más se acercan al query en su significado) serán devueltas.

Los argumentos opcionales son los mismos argumentos que el método [`list`](../sistema_de_archivos/metodo_list_lista.md) recibe—tanto los de metadata como las marcas de tiempo—así que [detállalos aquí](../sistema_de_archivos/metodo_list_lista.md#argumentos-del-metodo-list-lista) si es necesario. Al igual que con el método [`list`](../sistema_de_archivos/metodo_list_lista.md), puedes hacer búsqueda semántica sobre varios archivos a la vez porque todos los argumentos de metadata se envían al método `semantic_search` en formato de lista. Todos los elementos de los argumentos opcionales son iguales que para el método [`list`](../sistema_de_archivos/metodo_list_lista.md), incluyendo el operador comodín * y la raíz global.

Si no está presente ninguno de estos argumentos opcionales, el método `semantic_search` no funcionará porque no hay dónde buscar.

Al igual que el método [`list`](../sistema_de_archivos/metodo_list_lista.md), el método `semantic_search` acepta los argumentos opcionales `max_files` y `sort_order`, aunque su función cambia un poco:

- `max_files` especifica en hasta cuántos archivos se debe buscar. Su valor predeterminado no existe; no habría un máximo.

- `sort_order` acá toma tres valores posibles: 'ascending', 'descending', y 'global'. Los primeros dos ordenan los resultados por el archivo en el que están (los archivos se ordenan por su marca de tiempo de creación), y 'global' combina todos los archivos y devuelve los mejores resultados de entre la totalidad de archivos. Su valor predeterminado es 'descending'.

El método `semantic_search` recibe un argumento opcional que es único a este método:

- `k` (int) - Especifica hasta cuántos resultados se deben devolver por archivo consultado. Su valor predeterminado es 5.

### Ejemplo de Montaje de Pipeline y Procesamiento de Archivo

Para los ejemplos de este documento usarás un *pipeline* que consiste de tres módulos: un módulo [`parser`](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md), un módulo [`text-embedder`](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md) y un módulo [`vector-db`](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md). Este es el [*pipeline* básico de búsqueda semántica](../../ejemplos/ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_basica.md). Usa el método [`create_pipeline`](../creacion_de_pipelines/creacion_de_pipelines.md) para crearlo:


```python
# crea el pipeline básico de búsqueda semántica
pipeline = krixik.create_pipeline(
    name="metodo_semantic_search_1",
    module_chain=["parser", "text-embedder", "vector-db"]
)
```

Una vez creado el *pipeline*, puedes [`procesar`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) algunos archivos de texto a través de él para tener sobre qué buscar:


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
print(json.dumps(salida_2, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "semantic_search_method_1_parser_text-embedder_vector-db",
      "request_id": "4197e750-0560-43b9-b7e3-0ea5c8f15151",
      "file_id": "a94765c2-0250-4b3d-98af-20fc167640e8",
      "message": "SUCCESS - output fetched for file_id a94765c2-0250-4b3d-98af-20fc167640e8.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/a94765c2-0250-4b3d-98af-20fc167640e8.faiss"
      ]
    }


El valor de `process_output` es `null` porque el objeto devuelto es una base de datos, así que no se puede reproducir aquí. Puedes encontrar ese archivo de base de datos en la ubicación local indicada en `process_output_files`.

### Ejemplos de Busqueda Semantica

Ahora que has procesado archivos por el *pipeline* puedes usar el método `semantic_search` sobre él.

Con el siguiente código puedes buscar semánticamente sobre uno de los archivos:


```python
# haz semantic_search sobre un archivo
semantic_output = pipeline.semantic_search(query="It was cold night.",
                                           file_names=["Little Women.txt"])

# nítidamente reproduce la salida de este proceso
print(json.dumps(semantic_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "c1b9116f-0eaa-489d-a8f4-86ca7238e744",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "853f498f-4b1c-439b-bbd4-ccc47c44d254",
          "file_metadata": {
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_vectors": 43,
            "created_at": "2024-06-05 16:19:43",
            "last_updated": "2024-06-05 16:19:43"
          },
          "search_results": [
            {
              "snippet": "The four young faces on which the firelight shone brightened at the\ncheerful words, but darkened again as Jo said sadly,--\n\n\"We haven't got father, and shall not have him for a long time.\"",
              "line_numbers": [
                19,
                20,
                21,
                22,
                23
              ],
              "distance": 0.351
            },
            {
              "snippet": "Nobody spoke for a minute; then Meg said in an altered tone,--\n\n\"You know the reason mother proposed not having any presents this\nChristmas was because it is going to be a hard winter for every one; and\nshe thinks we ought not to spend money for pleasure, when our men are\nsuffering so in the army.",
              "line_numbers": [
                26,
                27,
                28,
                29,
                30,
                31,
                32
              ],
              "distance": 0.363
            },
            {
              "snippet": "said Meg, who could remember better times.",
              "line_numbers": [
                82
              ],
              "distance": 0.402
            },
            {
              "snippet": "\"It's so dreadful to be poor!\"",
              "line_numbers": [
                9,
                10
              ],
              "distance": 0.402
            },
            {
              "snippet": "\"How would you\nlike to be shut up for hours with a nervous, fussy old lady, who keeps\nyou trotting, is never satisfied, and worries you till you're ready to\nfly out of the window or cry?\"",
              "line_numbers": [
                58,
                59,
                60,
                61
              ],
              "distance": 0.403
            }
          ]
        }
      ]
    }


Además de devolver los fragmentos cuyo significado más se acercan al string enviado (*the query*), el método `semantic_search` también devuelve la distancia calculada entre vectores (que puede entenderse como la "distancia entre significados") de resultado y *query*. Mientras más corta es esta distancia, más se acerca el significado de este fragmento al del *query*. El método `semantic_search` devuelve los fragmentos con la distancia de vector más corta al *query*, ordenado de manera ascendiente dentro de cada archivo.

Cuando el argumento `sort_order` tiene el valor 'global', los resultados de todos los archivos se combinan y el método devuelve los fragmentos con la distancia más corta al *query*, ordenados de manera ascendiente, sin importar en qué archivo estén. Inténtalo haciéndo una búsqueda semántica sobre varios archivos con el [operador comodín](../sistema_de_archivos/metodo_list_lista.md#argumentos-con-el-operador-comodin):


```python
# haz búsqueda semántica sobre varios archivos
semantic_output_2 = pipeline.semantic_search(query="It was cold night.",
                                             symbolic_directory_paths=["/novelas*"],
                                             sort_order="global",
                                             k=4)

# nicely print the output of this search
print(json.dumps(semantic_output_2, indent=2))
```

    {
      "status_code": 200,
      "request_id": "ba1b7b85-8e36-49e5-8734-68c80d19e433",
      "message": "Successfully queried 4 user files.",
      "warnings": [],
      "items": [
        {
          "snippet": "I am already far north of London, and as I walk in the streets of\nPetersburgh, I feel a cold northern breeze play upon my cheeks, which\nbraces my nerves and fills me with delight.",
          "distance": 0.33,
          "line_numbers": [
            14,
            15,
            16,
            17
          ],
          "file_metadata": {
            "file_id": "f4720361-f94f-4f48-a4bf-0177dd91ba18",
            "file_name": "frankenstein.txt",
            "symbolic_directory_path": "/novels/gothic",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:17:58",
            "last_updated": "2024-06-05 16:17:58"
          }
        },
        {
          "snippet": "This breeze, which has travelled from the regions towards\nwhich I am advancing, gives me a foretaste of those icy climes.",
          "distance": 0.336,
          "line_numbers": [
            18,
            19
          ],
          "file_metadata": {
            "file_id": "f4720361-f94f-4f48-a4bf-0177dd91ba18",
            "file_name": "frankenstein.txt",
            "symbolic_directory_path": "/novels/gothic",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:17:58",
            "last_updated": "2024-06-05 16:17:58"
          }
        },
        {
          "snippet": "The four young faces on which the firelight shone brightened at the\ncheerful words, but darkened again as Jo said sadly,--\n\n\"We haven't got father, and shall not have him for a long time.\"",
          "distance": 0.351,
          "line_numbers": [
            19,
            20,
            21,
            22,
            23
          ],
          "file_metadata": {
            "file_id": "853f498f-4b1c-439b-bbd4-ccc47c44d254",
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:43",
            "last_updated": "2024-06-05 16:19:43"
          }
        },
        {
          "snippet": "There\u2014for with your leave, my sister, I will put\nsome trust in preceding navigators\u2014there snow and frost are banished;\nand, sailing over a calm sea, we may be wafted to a land surpassing in\nwonders and in beauty every region hitherto discovered on the habitable\nglobe.",
          "distance": 0.362,
          "line_numbers": [
            25,
            26,
            27,
            28,
            29
          ],
          "file_metadata": {
            "file_id": "f4720361-f94f-4f48-a4bf-0177dd91ba18",
            "file_name": "frankenstein.txt",
            "symbolic_directory_path": "/novels/gothic",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:17:58",
            "last_updated": "2024-06-05 16:17:58"
          }
        },
        {
          "snippet": "Nobody spoke for a minute; then Meg said in an altered tone,--\n\n\"You know the reason mother proposed not having any presents this\nChristmas was because it is going to be a hard winter for every one; and\nshe thinks we ought not to spend money for pleasure, when our men are\nsuffering so in the army.",
          "distance": 0.363,
          "line_numbers": [
            26,
            27,
            28,
            29,
            30,
            31,
            32
          ],
          "file_metadata": {
            "file_id": "853f498f-4b1c-439b-bbd4-ccc47c44d254",
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:43",
            "last_updated": "2024-06-05 16:19:43"
          }
        },
        {
          "snippet": "There, Margaret, the sun is for ever\nvisible, its broad disk just skirting the horizon and diffusing a\nperpetual splendour.",
          "distance": 0.377,
          "line_numbers": [
            23,
            24,
            25
          ],
          "file_metadata": {
            "file_id": "f4720361-f94f-4f48-a4bf-0177dd91ba18",
            "file_name": "frankenstein.txt",
            "symbolic_directory_path": "/novels/gothic",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:17:58",
            "last_updated": "2024-06-05 16:17:58"
          }
        },
        {
          "snippet": "Far from it.",
          "distance": 0.389,
          "line_numbers": [
            11
          ],
          "file_metadata": {
            "file_id": "d9e477d5-9b2c-4bf3-aa25-b6c739b83b86",
            "file_name": "moby dick.txt",
            "symbolic_directory_path": "/novels/adventure",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:31",
            "last_updated": "2024-06-05 16:19:31"
          }
        },
        {
          "snippet": "said Meg, who could remember better times.",
          "distance": 0.402,
          "line_numbers": [
            82
          ],
          "file_metadata": {
            "file_id": "853f498f-4b1c-439b-bbd4-ccc47c44d254",
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:43",
            "last_updated": "2024-06-05 16:19:43"
          }
        },
        {
          "snippet": "\"It's so dreadful to be poor!\"",
          "distance": 0.402,
          "line_numbers": [
            9,
            10
          ],
          "file_metadata": {
            "file_id": "853f498f-4b1c-439b-bbd4-ccc47c44d254",
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:43",
            "last_updated": "2024-06-05 16:19:43"
          }
        },
        {
          "snippet": "But gulp down your tears and hie aloft to the\n  royal-mast with your hearts; for your friends who have gone before\n  are clearing out the seven-storied heavens, and making refugees of\n  long-pampered Gabriel, Michael, and Raphael, against your coming.",
          "distance": 0.41,
          "line_numbers": [
            27,
            28,
            29,
            30
          ],
          "file_metadata": {
            "file_id": "d9e477d5-9b2c-4bf3-aa25-b6c739b83b86",
            "file_name": "moby dick.txt",
            "symbolic_directory_path": "/novels/adventure",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:31",
            "last_updated": "2024-06-05 16:19:31"
          }
        },
        {
          "snippet": "It will be seen that this mere painstaking burrower and grub-worm of\n  a poor devil of a Sub-Sub appears to have gone through the long\n  Vaticans and street-stalls of the earth, picking up whatever random\n  allusions to whales he could anyways find in any book whatsoever,\n  sacred or profane.",
          "distance": 0.433,
          "line_numbers": [
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9
          ],
          "file_metadata": {
            "file_id": "d9e477d5-9b2c-4bf3-aa25-b6c739b83b86",
            "file_name": "moby dick.txt",
            "symbolic_directory_path": "/novels/adventure",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:31",
            "last_updated": "2024-06-05 16:19:31"
          }
        },
        {
          "snippet": "Would that I could clear out Hampton Court and the\n  Tuileries for ye!",
          "distance": 0.438,
          "line_numbers": [
            26,
            27
          ],
          "file_metadata": {
            "file_id": "d9e477d5-9b2c-4bf3-aa25-b6c739b83b86",
            "file_name": "moby dick.txt",
            "symbolic_directory_path": "/novels/adventure",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:31",
            "last_updated": "2024-06-05 16:19:31"
          }
        },
        {
          "snippet": "On the other hand,\nI, for my part, declare for_ Pride and Prejudice _unhesitatingly.",
          "distance": 0.438,
          "line_numbers": [
            35,
            36
          ],
          "file_metadata": {
            "file_id": "a94765c2-0250-4b3d-98af-20fc167640e8",
            "file_name": "pride and prejudice.txt",
            "symbolic_directory_path": "/novels/romance",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:18",
            "last_updated": "2024-06-05 16:19:18"
          }
        },
        {
          "snippet": "The catastrophe of_ Mansfield Park _is admittedly\ntheatrical, the hero and heroine are insipid, and the author has almost\nwickedly destroyed all romantic interest by expressly admitting that\nEdmund only took Fanny because Mary shocked him, and that Fanny might\nvery likely have taken Crawford if he had been a little more assiduous;\nyet the matchless rehearsal-scenes and the characters of Mrs. Norris and\nothers have secured, I believe, a considerable party for it._ Sense and\nSensibility _has perhaps the fewest out-and-out admirers; but it dos\nnot want them._\n\n_I suppose, however, that the majority of at least competent votes\nwould, all things considered, be divided between_ Emma _and the present\nbook; and perhaps the vulgar verdict (if indeed a fondness for Miss\nAusten be not of itself a patent of exemption from any possible charge\nof vulgarity) would go for_ Emma.",
          "distance": 0.465,
          "line_numbers": [
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31
          ],
          "file_metadata": {
            "file_id": "a94765c2-0250-4b3d-98af-20fc167640e8",
            "file_name": "pride and prejudice.txt",
            "symbolic_directory_path": "/novels/romance",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:18",
            "last_updated": "2024-06-05 16:19:18"
          }
        },
        {
          "snippet": "To some the delightful freshness and humour of_ Northanger\nAbbey, _its completeness, finish, and_ entrain, _obscure the undoubted\ncritical facts that its scale is small, and its scheme, after all, that\nof burlesque or parody, a kind in which the first rank is reached with\ndifficulty._ Persuasion, _relatively faint in tone, and not enthralling\nin interest, has devotees who exalt above all the others its exquisite\ndelicacy and keeping.",
          "distance": 0.468,
          "line_numbers": [
            11,
            12,
            13,
            14,
            15,
            16,
            17
          ],
          "file_metadata": {
            "file_id": "a94765c2-0250-4b3d-98af-20fc167640e8",
            "file_name": "pride and prejudice.txt",
            "symbolic_directory_path": "/novels/romance",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:18",
            "last_updated": "2024-06-05 16:19:18"
          }
        },
        {
          "snippet": "And in the sect--fairly large and yet\nunusually choice--of Austenians or Janites, there would probably be\nfound partisans of the claim to primacy of almost every one of the\nnovels.",
          "distance": 0.479,
          "line_numbers": [
            8,
            9,
            10,
            11
          ],
          "file_metadata": {
            "file_id": "a94765c2-0250-4b3d-98af-20fc167640e8",
            "file_name": "pride and prejudice.txt",
            "symbolic_directory_path": "/novels/romance",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:18",
            "last_updated": "2024-06-05 16:19:18"
          }
        }
      ]
    }


Puedes ver que los resultados de todos los archivos se han combinado, y que el fragmento en el primer lugar tiene la distancia más corta entre *query* y fragmento de todos los archivos incluidos.

### Limite de Tamano de Salidas

El límite actual sobre salidas generadas por el método `semantic_search` es 5MB.


```python
# elimina todos los datos procesados pertenecientes a este pipeline
reset_pipeline(pipeline)
```
