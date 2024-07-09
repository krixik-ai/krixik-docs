<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/file_system/update_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>


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


## El Método `update` (Actualizar)

Puedes actualizar cualquier metadato de un archivo procesado con el método `update`.

Esta introducción al método `update` se divide en las siguientes secciones:

- [Argumentos del Método `update`](#argumentos-del-metodo-update)
- [Ejemplo del Método `update`](#ejemplo-del-metodo-update)
- [Observaciones Sobre el Método `update`](#observaciones-sobre-el-metodo-update)

### Argumentos del Metodo `update`

El método `update` toma un argumento requerido y al menos uno de varios argumentos opcionales:

- `file_id` (**requerido**, str) - El identificador único del archivo cuya metadata deseas actualizar.

- `expire_time` (opcional, int) - La cantidad de tiempo (en segundos) que los datos del archivo permanecerán en los servidores de Krixik, contando desde que se ejecuta el método `update`.

- `symbolic_directory_path` (opcional, str) - La ruta de directorio con formato UNIX en la que se encuentra el archivo en el sistema Krixik bajo tu cuenta.

- `file_name` (opcional, str) - El nombre de archivo personalizado del archivo en el sistema Krixik. Debe terminar con la extensión de archivo del archivo original de entrada. **No puedes cambiar la extensión de archivo.**

- `symbolic_file_path` (opcional, str) - La combinación de `symbolic_directory_path` y `file_name` en un solo argumento.

- `file_tags` (opcional, list) - Una lista de etiquetas de archivo personalizadas. Cada una es un par clave-valor. Ten en cuenta que debes actualizar todo el conjunto de etiquetas, así que si un archivo tiene tres de ellas y quieres actualizar solo una, excluir las otras dos del argumento `file_tags` en el método `update` resultará en la eliminación de las otras dos etiquetas.

- `file_description` (opcional, str) - Una descripción personalizada del archivo.

Si ninguno de los argumentos opcionales están presentes, el método `update` no funcionará porque no hay nada para actualizar.

### Ejemplo del Metodo `update`

Primero debes crear un *pipeline* sobre el cual puedas ejecutar este ejemplo. Un *pipeline* que consiste de un solo módulo [`parser`](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md) funcionará bien. Usa el método [`create_pipeline`](../creacion_de_pipelines/creacion_de_pipelines.md) para crearlo:


```python
# crea un pipeline de módulo único con un módulo parser
pipeline = krixik.create_pipeline(name="update_method_1_parser", module_chain=["parser"])
```

Ahora usa el método [`process`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) para procesar un archivo por el *pipeline*:


```python
# procesa un breve archivo de entrada
process_output = pipeline.process(
    local_file_path=data_dir + "input/frankenstein_muy_corto.txt",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False, # no mostrar actualizaciones de proceso al ejecutar el código
    symbolic_directory_path="/novelas/gotica",
    file_name="Draculas.txt",
    file_tags=[{"escritor": "Shelley"}, {"categoria": "gotica"}, {"siglo": "19"}],
)
```

Detalla el registro del archivo con el método [`list`](metodo_list_lista.md):


```python
# ve el registro del archivo con el método list
list_output = pipeline.list(symbolic_directory_paths=["/novelas/gotica"])

# nítidamente reproduce la salida de esta lista
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "6ccb47ec-574d-4d48-9dcb-7d0fe91f23b8",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:20:51",
          "process_id": "d99653b8-d16a-981a-41ab-1a2a86e99e9f",
          "created_at": "2024-06-05 15:20:51",
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
                  "num_lines": 26
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "shelley"
            },
            {
              "category": "gothic"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/gothic",
          "pipeline": "update_method_1_parser",
          "file_id": "e53d3c35-6f4c-466f-ab7c-6971a6312a09",
          "expire_time": "2024-06-05 15:50:50",
          "file_name": "frankenstein.txt"
        }
      ]
    }


Ahora puedes usar el método `update` para actualizar la metadata del archivo.

Puedes, por ejemplo, actualizar su `file_name` (dado que está incorrecto!) cambiar la etiqueta `{"categoria": "gotica"}` por algo diferente, agregarle un `file_description`—y dejar su `symbolic_directory_path` inalterado, pues ¿por qué modificarlo todo?


```python
# actualizar la metadata del archivo procesado
update_output = pipeline.update(
    file_id=process_output["file_id"],
    file_name="Frankenstein.txt",
    file_tags=[{"escritor": "Shelley"}, {"país": "Reino Unido"}, {"siglo": "19"}],
    file_description="¿Es el villano el monstruo o el doctor?",
)

# nítidamente reproduce la salida de esta lista
print(json.dumps(process_output, indent=2))
```

    INFO: lower casing file_name Frankenstein.txt to frankenstein.txt
    INFO: lower casing file tag {'author': 'Shelley'} to {'author': 'shelley'}
    INFO: lower casing file tag {'country': 'UK'} to {'country': 'uk'}
    {
      "status_code": 200,
      "pipeline": "update_method_1_parser",
      "request_id": "3c82cde3-dc63-431f-bf68-1a33b998c272",
      "file_id": "e53d3c35-6f4c-466f-ab7c-6971a6312a09",
      "message": "SUCCESS - output fetched for file_id e53d3c35-6f4c-466f-ab7c-6971a6312a09.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "\ufeffLetter 1\n\n_To Mrs. Saville, England._\n\n\nSt. Petersburgh, Dec. 11th, 17\u2014.",
          "line_numbers": [
            1,
            2,
            3,
            4,
            5,
            6
          ]
        },
        {
          "snippet": "You will rejoice to hear that no disaster has accompanied the\ncommencement of an enterprise which you have regarded with such evil\nforebodings.",
          "line_numbers": [
            7,
            8,
            9,
            10,
            11
          ]
        },
        {
          "snippet": "I arrived here yesterday, and my first task is to assure\nmy dear sister of my welfare and increasing confidence in the success\nof my undertaking.",
          "line_numbers": [
            11,
            12,
            13
          ]
        },
        {
          "snippet": "I am already far north of London, and as I walk in the streets of\nPetersburgh, I feel a cold northern breeze play upon my cheeks, which\nbraces my nerves and fills me with delight.",
          "line_numbers": [
            14,
            15,
            16,
            17
          ]
        },
        {
          "snippet": "Do you understand this\nfeeling?",
          "line_numbers": [
            17,
            18
          ]
        },
        {
          "snippet": "This breeze, which has travelled from the regions towards\nwhich I am advancing, gives me a foretaste of those icy climes.",
          "line_numbers": [
            18,
            19
          ]
        },
        {
          "snippet": "Inspirited by this wind of promise, my daydreams become more fervent\nand vivid.",
          "line_numbers": [
            20,
            21
          ]
        },
        {
          "snippet": "I try in vain to be persuaded that the pole is the seat of\nfrost and desolation; it ever presents itself to my imagination as the\nregion of beauty and delight.",
          "line_numbers": [
            21,
            22,
            23
          ]
        },
        {
          "snippet": "There, Margaret, the sun is for ever\nvisible, its broad disk just skirting the horizon and diffusing a\nperpetual splendour.",
          "line_numbers": [
            23,
            24,
            25
          ]
        },
        {
          "snippet": "There\u2014for with your leave, my sister, I will put\nsome trust in preceding navigators\u2014there snow and frost are banished;\nand, sailing over a calm sea, we may be wafted to a land surpassing in\nwonders and in beauty every region hitherto discovered on the habitable\nglobe.",
          "line_numbers": [
            25,
            26,
            27,
            28,
            29
          ]
        },
        {
          "snippet": "Its productions and features may be without example, as the\nphenomena of the heavenly bodies undoubtedly are in those undiscovered\nsolitudes.",
          "line_numbers": [
            29,
            30,
            31
          ]
        },
        {
          "snippet": "What may not be expected in a country of eternal light?",
          "line_numbers": [
            31
          ]
        },
        {
          "snippet": "I\nmay there discover the wondrous power which attracts the needle and may\nregulate a thousand celestial observations that require only this\nvoyage to render their seeming eccentricities consistent for ever.",
          "line_numbers": [
            31,
            32,
            33,
            34
          ]
        },
        {
          "snippet": "I\nshall satiate my ardent curiosity with the sight of a part of the world\nnever before visited, and may tread a land never before imprinted by\nthe foot of man.",
          "line_numbers": [
            34,
            35,
            36,
            37
          ]
        },
        {
          "snippet": "These are my enticements, and they are sufficient to\nconquer all fear of danger or death and to induce me to commence this\nlaborious voyage with the joy a child feels when he embarks in a little\nboat, with his holiday mates, on an expedition of discovery up his\nnative river.",
          "line_numbers": [
            37,
            38,
            39,
            40,
            41
          ]
        },
        {
          "snippet": "But supposing all these conjectures to be false, you\ncannot contest the inestimable benefit which I shall confer on all\nmankind, to the last generation, by discovering a passage near the pole\nto those countries, to reach which at present so many months are\nrequisite; or by ascertaining the secret of the magnet, which, if at\nall possible, can only be effected by an undertaking such as mine.",
          "line_numbers": [
            41,
            42,
            43,
            44,
            45,
            46
          ]
        },
        {
          "snippet": "These reflections have dispelled the agitation with which I began my\nletter, and I feel my heart glow with an enthusiasm which elevates me\nto heaven, for nothing contributes so much to tranquillise the mind as\na steady purpose\u2014a point on which the soul may fix its intellectual\neye.",
          "line_numbers": [
            47,
            48,
            49,
            50,
            51,
            52
          ]
        },
        {
          "snippet": "This expedition has been the favourite dream of my early years.",
          "line_numbers": [
            52
          ]
        },
        {
          "snippet": "I\nhave read with ardour the accounts of the various voyages which have\nbeen made in the prospect of arriving at the North Pacific Ocean\nthrough the seas which surround the pole.",
          "line_numbers": [
            52,
            53,
            54,
            55
          ]
        },
        {
          "snippet": "You may remember that a\nhistory of all the voyages made for purposes of discovery composed the\nwhole of our good Uncle Thomas\u2019 library.",
          "line_numbers": [
            55,
            56,
            57
          ]
        },
        {
          "snippet": "My education was neglected,\nyet I was passionately fond of reading.",
          "line_numbers": [
            57,
            58
          ]
        },
        {
          "snippet": "These volumes were my study\nday and night, and my familiarity with them increased that regret which\nI had felt, as a child, on learning that my father\u2019s dying injunction\nhad forbidden my uncle to allow me to embark in a seafaring life.",
          "line_numbers": [
            58,
            59,
            60,
            61
          ]
        },
        {
          "snippet": "These visions faded when I perused, for the first time, those poets\nwhose effusions entranced my soul and lifted it to heaven.",
          "line_numbers": [
            62,
            63,
            64
          ]
        },
        {
          "snippet": "I also\nbecame a poet and for one year lived in a paradise of my own creation;\nI imagined that I also might obtain a niche in the temple where the\nnames of Homer and Shakespeare are consecrated.",
          "line_numbers": [
            64,
            65,
            66,
            67
          ]
        },
        {
          "snippet": "You are well\nacquainted with my failure and how heavily I bore the disappointment.",
          "line_numbers": [
            67,
            68
          ]
        },
        {
          "snippet": "But just at that time I inherited the fortune of my cousin, and my\nthoughts were turned into the channel of their earlier bent.",
          "line_numbers": [
            69,
            70
          ]
        }
      ],
      "process_output_files": [
        "../../../data/output/e53d3c35-6f4c-466f-ab7c-6971a6312a09.json"
      ]
    }


Ahora vuelve a usar el método [`list`](metodo_list_lista.md) para confirmar que toda la metadata se ha actualizado según tu indicación:


```python
# usa el método list para confirmar que la metadata se ha actualizado
list_output = pipeline.list(symbolic_file_paths=["/novelas/gotica/Frankenstein.txt"])

# nítidamente reproduce la salida de esta lista
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "396b969f-2aeb-4952-bd6a-67e1ccca14f1",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:21:10",
          "process_id": "d99653b8-d16a-981a-41ab-1a2a86e99e9f",
          "created_at": "2024-06-05 15:20:51",
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
                  "num_lines": 26
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "shelley"
            },
            {
              "country": "uk"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "Is the villain the monster or the doctor?",
          "symbolic_directory_path": "/novels/gothic",
          "pipeline": "update_method_1_parser",
          "file_id": "e53d3c35-6f4c-466f-ab7c-6971a6312a09",
          "expire_time": "2024-06-05 15:50:50",
          "file_name": "frankenstein.txt"
        }
      ]
    }


### Observaciones Sobre el Metodo `update`

Cuatro observaciones finales sobre el método `update`:

- Verás que en el ejemplo anterior al actualizar `file_tags` incluiste el grupo completo de etiquetas: `[{"escritor": "Shelley"}, {"país": "Reino Unido"}, {"siglo": "19"}]`. Si hubieras usado solamente `[{"país": "Reino Unido"}]`, que era el único que buscabas actualizar, las otras dos se habrían eliminado.

- No puedes actualizar la combinación `symbolic_directory_path`/`file_name` (el `symbolic_file_path`) para que sea idéntica a la de otro archivo. Krixik no lo permite.

- Tampoco puedes actualizar la extensión de archivo de un archivo. Por ejemplo, un archivo `.txt` no puede convertirse en un archivo `.pdf` a través del método `update`.

- El método `update` te permite extender el [`expire_time`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#argumentos-principales-del-metodo-process) de un archivo indefinidamente. Al inicialmente [procesar](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) un archivo, su [`expire_time`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#argumentos-principales-del-metodo-process) no puede ser mayor a 2,592,000 segundos (30 días). Sin embargo, si periódicamente usas `update` sobre este archivo y vuelves a especificar su [`expire_time`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#argumentos-principales-del-metodo-process) como 2,592,000 segundos (o cuantos segundos desees), ese archivo permanecerá en el sistema esa cantidad de tiempo adicional desde ese momento, y así sucesivamente.


```python
# elimina todos los datos procesados pertenecientes a este pipeline
reset_pipeline(pipeline)
```
