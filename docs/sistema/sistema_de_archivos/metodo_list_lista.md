<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/file_system/list_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## El Método `list` (Lista)
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/system/file_system/list_method/)

Tras usar el método [`process`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) para procesar uno o varios archivos a través de un *pipeline* puedes recuperar el registro de cualquiera de esos archivos con el método `list` (lista). Puedes `list` por `file_id` o por cualquier otro metadato que incluiste al inicialmente procesar el archivo.

Esta introducción al método `list` (lista) se divide en las siguientes secciones:

- [Argumentos del Método `list` (Lista)](#argumentos-del-metodo-list-lista)
- [Ejemplo de Montaje de Pipeline y Procesamiento de Archivo](#ejemplo-de-montaje-de-pipeline-y-procesamiento-de-archivo)
- [`list` por `file_ids` (Identificadores de Archivo)](#list-por-file_ids-identificadores-de-archivo)
- [`list` por `file_names` (Nombres de Archivo)](#list-por-file_names-nombres-de-archivo)
- [`list` por `symbolic_directory_paths` (Rutas de Directorio Krixik)](#list-por-symbolic_directory_paths-rutas-de-directorio-krixik)
- [`list` por `file_tags` (Etiquetas de Archivo)](#list-por-file_tags-etiquetas-de-archivo)
- [`list` por Marcas de Tiempo `created_at` (Creación) y `updated_at` (Ultima Actualización)](#list-por-marcas-de-tiempo-created_at-creacion-y-updated_at-ultima-actualizacion)
- [Argumentos con el Operador Comodín](#argumentos-con-el-operador-comodin)
- [La Raíz Global](#la-raiz-global)
- [Usa Varios Argumentos con el Método `list`](#usa-varios-argumentos-con-el-metodo-list)
- [Límite de Tamaño de Salidas](#limite-de-tamano-de-salidas)

### Argumentos del Metodo `list` (Lista)

El método `list` es muy versátil. Te permite listar por varios elementos de metadata diferentes y por combinaciones de los mismos.

Todos los argumentos a seguir son opcionales. Sin embargo, debes usar al menos un agumento para que el método `list` funcione.

Si quieres repasar los argumentos de metadata del sistema de archivos Krixik, detalla la [introducción del método `process`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md). Los argumentos de metadata que puedes usar con el método `list` son:

- `file_ids` (Identificadores de archivo): Una lista de uno o varios `file_id`s (identificadores de archivo) cuyos registros buscas.

- `file_names` (Nombres de archivo): Una lista de uno o varios `file_name`s (nombres de archivo) cuyos registros buscas.

- `symbolic_directory_paths` (Rutas de directorio Krixik): Una lista de una o varias `symbolic_directory_paths` (rutas de directorio en el sistema Krixik). Usar una de estas devuelve todos los archivos en esta ubicación.

- `symbolic_file_paths` (Rutas de archivo Krixik): Una lista de una o varias `symbolic_file_paths` (rutas de archivo en el sistema Krixik) cuyos registros buscas.

- `file_tags` (Etiquetas de archivo): Una lista de una o varias `file_tag`s (etiquetas de archivo). Usar una de estas devuelve todos los archivos con esa etiqueta. Ten en cuenta que basta con un solo `file_tag`; si un archivo tiene varias etiquetas e incluyes al menos una como argumento del método `list`, el registro de ese archivo será devuelto.

Puedes usar operadores comodín con `file_names`, `symbolic_directory_paths`,`symbolic_file_paths` y `file_tags` para recuperar registros cuya metadata exacta no recuerdas, o si buscas recuperar registros para un grupo de archivos que comparten metadata similar. [En breve](#argumentos-con-el-operador-comodin) encontrarás más detalle sobre los operadores comodines.

Puedes también listar por marcas de tiempo. El método `list` acepta marcas de tiempo tanto de creación como de última actualización del archivo. Estas son *strings* con formato `"AAAA-MM-DD HH:MM:SS"`, o pueden tener simplemente formato `"AAAA-MM-DD"`.

- `created_at_start`: Excluye todos los archivos cuya marca de tiempo `created_at` (creación) es antes de lo que especificas.

- `created_at_end`: Excluye todos los archivos cuya marca de tiempo `created_at` (creación) es después de lo que especificas.

- `last_updated_start`: Excluye todos los archivos cuya marca de tiempo `last_updated` (última actualización) es antes de lo que especificas.

- `last_updated_end`: Excluye todos los archivos cuya marca de tiempo `last_updated` (última actualización) es después de lo que especificas.

En breve encontrarás ejemplos de cómo usar metadata y marcas de tiempo en el método `list`.

Ten en cuenta que los argumentos de metadata del sistema de archivos operan con lógica **OR**: por ejemplo, si haces `list` por `file_names`, `file_ids` o `file_tags` cualquier archivo que coincida será devuelto. Sin embargo, los argumentos de marcas de tiempo operan con lógica **AND**; los archivos devueltos deben respetar todas las marcas de tiempo indicadas. Si se indican dos marcas de tiempo y no hay tiempo compartido entre ellas, el método `list` no devolverá nada.

El método `list` toma dos argumentos opcionales de metadata para ayudarte a organizar tus salidas:

- `max_files` (int): Determina el máximo número de registros de archivo que `list` puede devolver. Su valor predeterminado es nulo; no hay máximo.

- `sort_order` (str): Especifica cómo ordenar los resultados. Los dos valores válidos para este argumento son 'ascending' y 'descending' (en cuanto a las marcas de tiempo de creación). Su valor predeterminado es 'descending'.

### Ejemplo de Montaje de Pipeline y Procesamiento de Archivo

Tendrás que crear un *pipeline* y [`procesar`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) algunos archivos a través de él para ver la versatilidad de `list`. Crea un *pipeline* de módulo único con un módulo [`parser`](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md) y [`procesa`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) unos archivos TXT que continenen el texto de clásicos literarios de la lengua inglesa. Define metadata opcional como `file_name`, `file_tags`, y `symbolic_directory_path` para cada proceso para luego ilustrar cómo se usa cada uno con el método `list`:


```python
# crea un pipeline de módulo único
pipeline = krixik.create_pipeline(name="metodo_list_1_parser", module_chain=["parser"])
```


```python
# procesa archivos a través del pipeline que acabas de crear
# define metadata opcional como file_name, file_tags y symbolic_directory_path para cada uno para luego ver cómo se usan con el método list
archivos = [
    {
        "local_file_path": data_dir + "input/frankenstein_muy_corto.txt",
        "file_name": "Frankenstein.txt",
        "file_tags": [{"escritor": "Shelley"}, {"categoria": "gotica"}, {"siglo": "19"}],
        "symbolic_directory_path": "/novelas/gotica",
    },
    {
        "local_file_path": data_dir + "input/orgullo_y_prejuicio_muy_corto.txt",
        "file_name": "Pride and Prejudice.txt",
        "symbolic_directory_path": "/novelas/romance",
        "file_tags": [{"escritor": "Austen"}, {"categoria": "romance"}, {"siglo": "19"}],
    },
    {
        "local_file_path": data_dir + "input/moby_dick_muy_corto.txt",
        "file_name": "Moby Dick.txt",
        "symbolic_directory_path": "/novelas/aventura",
        "file_tags": [{"escritor": "Melville"}, {"categoria": "aventura"}, {"siglo": "19"}],
    },
]

# procesa cada archivo
all_process_output = []
for entry in archivos:
    process_output = pipeline.process(
        local_file_path=entry["local_file_path"],  # la ruta de archivo inicial en la que yace el archivo de entrada
        local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
        expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
        wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
        verbose=False,  # no mostrar actualizaciones de proceso al ejecutar el código
        file_name=entry["file_name"],
        symbolic_directory_path=entry["symbolic_directory_path"],
        file_tags=entry["file_tags"],
    )
    all_process_output.append(process_output)
```

Detalla la salida de el último archivo procesado antes de continuar:


```python
# nítidamente reproduce la salida de este proceso
print(json.dumps(all_process_output[-1], indent=2))
```

    {
      "status_code": 200,
      "pipeline": "list_method_1_parser",
      "request_id": "96c60151-9e74-40c1-a904-af10e03b2f3c",
      "file_id": "60d6e243-91bd-4561-a17d-291539cd651a",
      "message": "SUCCESS - output fetched for file_id 60d6e243-91bd-4561-a17d-291539cd651a.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "\ufeff  EXTRACTS.",
          "line_numbers": [
            1
          ]
        },
        {
          "snippet": "(Supplied by a Sub-Sub-Librarian).",
          "line_numbers": [
            1
          ]
        },
        {
          "snippet": "It will be seen that this mere painstaking burrower and grub-worm of\n  a poor devil of a Sub-Sub appears to have gone through the long\n  Vaticans and street-stalls of the earth, picking up whatever random\n  allusions to whales he could anyways find in any book whatsoever,\n  sacred or profane.",
          "line_numbers": [
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9
          ]
        },
        {
          "snippet": "Therefore you must not, in every case at least,\n  take the higgledy-piggledy whale statements, however authentic, in\n  these extracts, for veritable gospel cetology.",
          "line_numbers": [
            9,
            10,
            11
          ]
        },
        {
          "snippet": "Far from it.",
          "line_numbers": [
            11
          ]
        },
        {
          "snippet": "As\n  touching the ancient authors generally, as well as the poets here\n  appearing, these extracts are solely valuable or entertaining, as\n  affording a glancing bird\u2019s eye view of what has been promiscuously\n  said, thought, fancied, and sung of Leviathan, by many nations and\n  generations, including our own.",
          "line_numbers": [
            11,
            12,
            13,
            14,
            15,
            16
          ]
        },
        {
          "snippet": "So fare thee well, poor devil of a Sub-Sub, whose commentator I am.",
          "line_numbers": [
            17,
            18
          ]
        },
        {
          "snippet": "Thou belongest to that hopeless, sallow tribe which no wine of this\n  world will ever warm; and for whom even Pale Sherry would be too\n  rosy-strong; but with whom one sometimes loves to sit, and feel\n  poor-devilish, too; and grow convivial upon tears; and say to them\n  bluntly, with full eyes and empty glasses, and in not altogether\n  unpleasant sadness\u2014Give it up, Sub-Subs!",
          "line_numbers": [
            19,
            20,
            21,
            22,
            23,
            24
          ]
        },
        {
          "snippet": "For by how much the more\n  pains ye take to please the world, by so much the more shall ye for\n  ever go thankless!",
          "line_numbers": [
            24,
            25,
            26
          ]
        },
        {
          "snippet": "Would that I could clear out Hampton Court and the\n  Tuileries for ye!",
          "line_numbers": [
            26,
            27
          ]
        },
        {
          "snippet": "But gulp down your tears and hie aloft to the\n  royal-mast with your hearts; for your friends who have gone before\n  are clearing out the seven-storied heavens, and making refugees of\n  long-pampered Gabriel, Michael, and Raphael, against your coming.",
          "line_numbers": [
            27,
            28,
            29,
            30
          ]
        },
        {
          "snippet": "Here ye strike but splintered hearts together\u2014there, ye shall strike\n  unsplinterable glasses!",
          "line_numbers": [
            31,
            32
          ]
        }
      ],
      "process_output_files": [
        "../../../data/output/60d6e243-91bd-4561-a17d-291539cd651a.json"
      ]
    }


### `list` por `file_ids` (Identificadores de Archivo)


Intenta listar por `file_id`s (identificadores de archivo).

Tienes el `file_id` de cada uno de los tres archivos que procesaste, pues estos se devolvieron al final de cada proceso.

Puedes listar por varios `file_id`s. Para ello, debes presentarle al método `list` una lista de los `file_id`s que buscas.

Por ejemplo, para ver la metadata asociada a cada archivo arriba procesado simplemente extrae el `file_id` de las respectivas salidas:


```python
# lista registros de por file_ids
list_output = pipeline.list(file_ids=[v["file_id"] for v in all_process_output])

# nítidamente reproduce la salida de este proceso
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "06a926de-267a-48df-90fe-3e0b8e6f3e29",
      "message": "Successfully returned 3 items.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:28:06",
          "process_id": "0131ae96-424f-350e-eede-b9b9f6e60a7c",
          "created_at": "2024-06-05 15:28:06",
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
                  "num_lines": 12
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "melville"
            },
            {
              "category": "adventure"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/adventure",
          "pipeline": "list_method_1_parser",
          "file_id": "60d6e243-91bd-4561-a17d-291539cd651a",
          "expire_time": "2024-06-05 15:58:05",
          "file_name": "moby dick.txt"
        },
        {
          "last_updated": "2024-06-05 15:27:58",
          "process_id": "f6ae9e98-bec4-2314-3d20-9116ec2a4baf",
          "created_at": "2024-06-05 15:27:58",
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
                  "num_lines": 9
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "austen"
            },
            {
              "category": "romance"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/romance",
          "pipeline": "list_method_1_parser",
          "file_id": "5b90a7c0-ccf8-4abf-b8ff-9eb7b755c2d2",
          "expire_time": "2024-06-05 15:57:58",
          "file_name": "pride and prejudice.txt"
        },
        {
          "last_updated": "2024-06-05 15:27:43",
          "process_id": "06cd2d57-22df-5d94-36e4-3133c4d757f7",
          "created_at": "2024-06-05 15:27:43",
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
          "pipeline": "list_method_1_parser",
          "file_id": "8abc402e-57ed-459d-af9c-918ae9dad038",
          "expire_time": "2024-06-05 15:57:41",
          "file_name": "frankenstein.txt"
        }
      ]
    }


Como puedes ver, se ha devuelto un registro completo para cada archivo. Para aprender más sobre cada elemento de metadata, detalla la documentación del método [`process`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), pues ahí se describen a fondo.

### `list` por `file_names` (Nombres de Archivo)

También puedes listar por `file_name`s (nombres de archivo). Funciona como listar por `file_id`s, lo cual acabas de hacer, pero con `file_name` en vez de `file_id`. Lista <u>Orgullo y Prejuicio</u> por `file_name`s de la siguiente manera:


```python
# lista uno de los registros por su file_name
list_output = pipeline.list(file_names=["Pride and Prejudice.txt"])

# nítidamente reproduce la salida de este proceso
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "a5b399fe-a0e9-4a78-a4eb-2bbc3a7311b7",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:27:58",
          "process_id": "f6ae9e98-bec4-2314-3d20-9116ec2a4baf",
          "created_at": "2024-06-05 15:27:58",
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
                  "num_lines": 9
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "austen"
            },
            {
              "category": "romance"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/romance",
          "pipeline": "list_method_1_parser",
          "file_id": "5b90a7c0-ccf8-4abf-b8ff-9eb7b755c2d2",
          "expire_time": "2024-06-05 15:57:58",
          "file_name": "pride and prejudice.txt"
        }
      ]
    }


Se ha devuelto un registro completo del archivo. Para aprender más sobre cada elemento de metadata, detalla la documentación del método [`process`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), pues ahí se describen a fondo.

### `list` por `symbolic_directory_paths` (Rutas de Directorio Krixik)

También puedes listar por `symbolic_directory_path`s (rutas de directorio Krixik). Funciona como listar por `file_id`s y `file_name`s (como acabas de hacer), pero con `symbolic_directory_path` en vez de esos argumentos. Lista <u>Frankenstein</u> y <u>Moby Dick</u> por `symbolic_directory_path` de la siguiente manera:


```python
# lista dos de los registros por su symbolic_directory_path
list_output = pipeline.list(symbolic_directory_paths=["/novelas/gotica", "/novelas/aventura"])

# nítidamente reproduce la salida de este proceso
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "300cf157-a441-47e7-b36e-a3f63856533d",
      "message": "Successfully returned 2 items.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:28:06",
          "process_id": "0131ae96-424f-350e-eede-b9b9f6e60a7c",
          "created_at": "2024-06-05 15:28:06",
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
                  "num_lines": 12
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "melville"
            },
            {
              "category": "adventure"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/adventure",
          "pipeline": "list_method_1_parser",
          "file_id": "60d6e243-91bd-4561-a17d-291539cd651a",
          "expire_time": "2024-06-05 15:58:05",
          "file_name": "moby dick.txt"
        },
        {
          "last_updated": "2024-06-05 15:27:43",
          "process_id": "06cd2d57-22df-5d94-36e4-3133c4d757f7",
          "created_at": "2024-06-05 15:27:43",
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
          "pipeline": "list_method_1_parser",
          "file_id": "8abc402e-57ed-459d-af9c-918ae9dad038",
          "expire_time": "2024-06-05 15:57:41",
          "file_name": "frankenstein.txt"
        }
      ]
    }


Se ha devuelto un registro completo de los archivos que concuerdan. Para aprender más sobre cada elemento de metadata, detalla la documentación del método [`process`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), pues ahí se describen a fondo.

### `list` por `file_tags` (Etiquetas de Archivo)

También puedes listar por `file_tags` (etiquetas de archivo). Dado que ya incorporaste las etiquetas al [procesar](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) los archivos, lista novelas del siglo 19 y novelas escritas por Herman Melville de la siguiente manera:


```python
# lista registros por sus file_tags
list_output = pipeline.list(file_tags=[{"escritor": "Melville"}, {"siglo": "19"}])

# nítidamente reproduce la salida de este proceso
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "11bcf2d1-6c09-403d-8138-9c642fb3f4c2",
      "message": "Successfully returned 3 items.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:28:06",
          "process_id": "0131ae96-424f-350e-eede-b9b9f6e60a7c",
          "created_at": "2024-06-05 15:28:06",
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
                  "num_lines": 12
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "melville"
            },
            {
              "category": "adventure"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/adventure",
          "pipeline": "list_method_1_parser",
          "file_id": "60d6e243-91bd-4561-a17d-291539cd651a",
          "expire_time": "2024-06-05 15:58:05",
          "file_name": "moby dick.txt"
        },
        {
          "last_updated": "2024-06-05 15:27:58",
          "process_id": "f6ae9e98-bec4-2314-3d20-9116ec2a4baf",
          "created_at": "2024-06-05 15:27:58",
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
                  "num_lines": 9
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "austen"
            },
            {
              "category": "romance"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/romance",
          "pipeline": "list_method_1_parser",
          "file_id": "5b90a7c0-ccf8-4abf-b8ff-9eb7b755c2d2",
          "expire_time": "2024-06-05 15:57:58",
          "file_name": "pride and prejudice.txt"
        },
        {
          "last_updated": "2024-06-05 15:27:43",
          "process_id": "06cd2d57-22df-5d94-36e4-3133c4d757f7",
          "created_at": "2024-06-05 15:27:43",
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
          "pipeline": "list_method_1_parser",
          "file_id": "8abc402e-57ed-459d-af9c-918ae9dad038",
          "expire_time": "2024-06-05 15:57:41",
          "file_name": "frankenstein.txt"
        }
      ]
    }


Dado que todos los archivos incluyeron la etiqueta `{"siglo": 19}` cuando incialmente fueron [procesados](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), registros para los tres archivos son devueltos. <u>Moby Dick</u> también incluye la etiqueta `{"escritor": "Melville"}`, pero como no hay duplicación de resultados, el registro de ese archivo solo aparece una vez.

### `list` por Marcas de Tiempo `created_at` (Creacion) y `updated_at` (Ultima Actualizacion)

Para ver cómo listar por marcas de tiempo, primero [procesa](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) un archivo adicional por el *pipeline*:


```python
# ver tiempo actual
from datetime import datetime, timezone

hora_actual = datetime.now(tz=timezone.utc).strftime(format="%Y-%m-%d %H:%M:%S")

# procesa un archivo adicional a través del pipeline que ya creaste
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_muy_corto.txt",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False,  # no mostrar actualizaciones de proceso al ejecutar el código
    symbolic_directory_path="/novelas/distopia",
    file_name="1984.txt",
    file_tags=[{"escritor": "Orwell"}, {"categoria": "distopia"}, {"siglo": "20"}],
)
```

Listar por marcas de tiempo es tan fácil como hacerlo por metadata del sistema de archivos. El siguiente ejemplo solo usa un tipo de marca de tiempo (`last_updated_start`), pero ten en cuenta que todas funcionan de la misma manera.

Con base en la salida del archivo que acabas de procesar y la salida de los tres archivos anteriores, elige una fecha y hora que caiga en la mitad de las cuatro marcas de tiempo `last_updated`:


```python
# lista registros por su marca de tiempo last_updated
list_output = pipeline.list(created_at_start=hora_actual)

# nítidamente reproduce la salida de este proceso
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "f090a0e5-cfe6-42fb-b8ed-3272cda048c6",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:28:19",
          "process_id": "c3968a8c-c9de-f5dd-ea16-d81e80b3ef3f",
          "created_at": "2024-06-05 15:28:19",
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
            },
            "pipeline_ordered_modules": [
              "parser"
            ],
            "pipeline_output_process_keys": [
              "snippet"
            ]
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
          "symbolic_directory_path": "/novels/dystopian",
          "pipeline": "list_method_1_parser",
          "file_id": "c3b610f7-1c22-4a7d-b2a1-4cb4ee7d5a6e",
          "expire_time": "2024-06-05 15:58:19",
          "file_name": "1984.txt"
        }
      ]
    }


Ten en cuenta que las marcas de tiempo operan con lógica **AND**: para ser listado, el registro de un archivo debe caer dentro de la ventana temporal especificada. Esto también significa que si se usan dos argumentos de marca de tiempo y no hay tiempo compartido (superpuesto) entre ellos, el método `list` no devolverá nada.

### Argumentos con el Operador Comodin

El operador comodín es el asterisco: *

Puedes usar el operador comodín * para usar `list` con registros cuya metadata exacta no recuerdas, o si quieres `list` registros para un grupo de archivos que compartan metadata similar.

Para `file_names` y `symbolic_directory_paths`, un comodín se puede usar como prefijo o como sufijo:

- Ejemplo de * como prefijo: `*reportado.txt`
- Ejemplo de * como sufijo: `/principal/archivado/estudio*`

Ten en cuenta que no tienes que necesariamente adjuntar palabras completas al operador comodín *. Los dos ejemplos anteriores podrían también ser:

- Ejemplo de * como prefijo: `*tado.txt`
- Ejemplo de * como sufijo: `/principal/archivado/estu*`

En `file_tags` puedes usar un comodín como el valor en un diccionario con par clave-valor. Esto devolverá todo registro con la clave correspondiente:

- Ejemplo de * en file_tags: `{"categoria_recibo": "*"}`

Detalla ejemplos del método `list` para cada uno de estos. Primero, un comodín prefijo en `file_names`:


```python
# lista registros usando un comodín prefijo en file_names
list_output = pipeline.list(file_names=["*o.txt"])

# nítidamente reproduce la salida de este proceso
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "0d5eff98-3c4a-4419-b306-c57638549f4a",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:27:58",
          "process_id": "f6ae9e98-bec4-2314-3d20-9116ec2a4baf",
          "created_at": "2024-06-05 15:27:58",
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
                  "num_lines": 9
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "austen"
            },
            {
              "category": "romance"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/romance",
          "pipeline": "list_method_1_parser",
          "file_id": "5b90a7c0-ccf8-4abf-b8ff-9eb7b755c2d2",
          "expire_time": "2024-06-05 15:57:58",
          "file_name": "pride and prejudice.txt"
        }
      ]
    }


El código anterior devuelve el registro de todo archivo cuyo `file_name` termina con "o.txt".

Ahora un sufijo comodín en `symbolic_directory_paths`:


```python
# lista registros usando un comodín sufijo en symbolic_directory_paths
list_output = pipeline.list(symbolic_directory_paths=["/poemas/*"])

# nítidamente reproduce la salida de este proceso
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "b6485d2e-5c54-4843-a454-8b2e363a96cc",
      "message": "No files were found for the given query arguments",
      "warnings": [
        {
          "WARNING: the following arguments returned zero results": [
            {
              "symbolic_directory_paths": [
                "/my/*"
              ]
            }
          ]
        }
      ],
      "items": []
    }


El código anterior devuelve el registro de todo archivo cuyo `symbolic_directory_path` empieza con "/poemas/".

Ahora un operador comodín en `file_tags`:


```python
# lista registros usando el operador comodín en file_tags
list_output = pipeline.list(file_tags=[{"escritor": "*"}])

# nítidamente reproduce la salida de este proceso
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "820bedaa-dba3-44d4-9677-433dfa902395",
      "message": "Successfully returned 4 items.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:28:19",
          "process_id": "c3968a8c-c9de-f5dd-ea16-d81e80b3ef3f",
          "created_at": "2024-06-05 15:28:19",
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
          "symbolic_directory_path": "/novels/dystopian",
          "pipeline": "list_method_1_parser",
          "file_id": "c3b610f7-1c22-4a7d-b2a1-4cb4ee7d5a6e",
          "expire_time": "2024-06-05 15:58:19",
          "file_name": "1984.txt"
        },
        {
          "last_updated": "2024-06-05 15:28:06",
          "process_id": "0131ae96-424f-350e-eede-b9b9f6e60a7c",
          "created_at": "2024-06-05 15:28:06",
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
                  "num_lines": 12
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "melville"
            },
            {
              "category": "adventure"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/adventure",
          "pipeline": "list_method_1_parser",
          "file_id": "60d6e243-91bd-4561-a17d-291539cd651a",
          "expire_time": "2024-06-05 15:58:05",
          "file_name": "moby dick.txt"
        },
        {
          "last_updated": "2024-06-05 15:27:58",
          "process_id": "f6ae9e98-bec4-2314-3d20-9116ec2a4baf",
          "created_at": "2024-06-05 15:27:58",
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
                  "num_lines": 9
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "austen"
            },
            {
              "category": "romance"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/romance",
          "pipeline": "list_method_1_parser",
          "file_id": "5b90a7c0-ccf8-4abf-b8ff-9eb7b755c2d2",
          "expire_time": "2024-06-05 15:57:58",
          "file_name": "pride and prejudice.txt"
        },
        {
          "last_updated": "2024-06-05 15:27:43",
          "process_id": "06cd2d57-22df-5d94-36e4-3133c4d757f7",
          "created_at": "2024-06-05 15:27:43",
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
          "pipeline": "list_method_1_parser",
          "file_id": "8abc402e-57ed-459d-af9c-918ae9dad038",
          "expire_time": "2024-06-05 15:57:41",
          "file_name": "frankenstein.txt"
        }
      ]
    }


El código anterior devuelve el registro de todo archivo con `file_tag` cuya clave es "escritor", sin importar su valor.

Puedes también usar el operador comodín con el método [`show_tree`](metodo_show_tree_mostrar_arbol.md), el método [`semantic_search`](../metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) y el método [`keyword_search`](../metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md).

### La Raiz Global

Como habrás sospechado, hay una manera muy especial de usar el operador comodín en `symbolic_directory_paths` que llamamos "la raíz global". Se usa de la siguiente manera: pon un operador comodín * justo después de la barra raíz y nada más, así:

```python
# línea de código ejemplo con la raíz global
symbolic_directory_paths=['/*']
```

Listar con la raíz global devuelve registros para <u>todos</u> los archivos en tu *pipeline*. La raíz global se puede usar también con el método [`show_tree`](metodo_show_tree_mostrar_arbol.md), el método [`semantic_search`](../metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) y el método [`keyword_search`](../metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md).

### Usa Varios Argumentos con el Metodo `list`

Como ya se dijo, puedes combinar varios argumentos en el método `list`. Los argumentos múltiples se combinan con un **OR** lógico (si son argumentos de metadata) o **AND** (si son marcas de tiempo) para recuperar registros que satisfacen lo que has solicitado.

Por ejemplo, combina una marca de tiempo, un `symbolic_file_path` y `file_tags` en un solo uso del método `list`:


```python
# obtener tiempo actual
from datetime import datetime, timezone

hora_actual_2 = datetime.now(tz=timezone.utc).strftime(format="%Y-%m-%d %H:%M:%S")

# lista registros combinando argumentos
list_output = pipeline.list(
    created_at_end=hora_actual_2, symbolic_file_paths=["/novelas/gotica/Pride and Prejudice.txt"], file_tags=[({"escritor": "Orwell"})]
)

# nítidamente reproduce la salida de este proceso
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "cf82edeb-51a1-4c77-8f1e-53a647660b9f",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [
        {
          "WARNING: the following arguments returned zero results": [
            {
              "symbolic_file_paths": [
                "/novels/gothic/pride and prejudice.txt"
              ]
            }
          ]
        }
      ],
      "items": [
        {
          "last_updated": "2024-06-05 15:28:19",
          "process_id": "c3968a8c-c9de-f5dd-ea16-d81e80b3ef3f",
          "created_at": "2024-06-05 15:28:19",
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
          "symbolic_directory_path": "/novels/dystopian",
          "pipeline": "list_method_1_parser",
          "file_id": "c3b610f7-1c22-4a7d-b2a1-4cb4ee7d5a6e",
          "expire_time": "2024-06-05 15:58:19",
          "file_name": "1984.txt"
        }
      ]
    }


Aunque <u>Orgullo y Prejuicio</u> y <u>1984</u> cuadran respectivamente con los argumentos `symbolic_file_paths` y `file_tags`, ninguno de ellos concuerda con la marca de tiempo indicada. Por ende, ambos son excluidos del resultado de esta lista.

### Limite de Tamano de Salidas

El límite actual sobre salidas generadas por el método `list` es 5MB.
