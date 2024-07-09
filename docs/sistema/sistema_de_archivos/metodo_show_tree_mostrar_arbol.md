<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/file_system/show_tree_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>


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


## El Método `show_tree` (Mostrar Árbol)

El método `show_tree` te permite visualizar, ya sea por tu terminal o como salida en tu IDE, todos los archivos actualmente en tu *pipeline*. Está diseñado como una versión simple y análoga del comando ['tree' de UNIX](https://www.tecmint.com/linux-tree-command-examples/).

Esta introducción al método `show_tree` está dividida en las siguientes secciones:

- [Argumentos del Método `show_tree`](#argumentos-del-metodo-show_tree)
- [Ejemplo del Método `show_tree`](#ejemplo-del-metodo-show_tree)
- [El Operador Comodín y la Raíz Global](#el-operador-comodin-y-la-raiz-global)

### Argumentos del Metodo `show_tree`

El método `show_tree` toma un argumento (requerido):

- `symbolic_directory_path` (str) - El directorio en el sistema Krixik cuyo contenido quieres visualizar. Si se usa el [operador comodín](#el-operador-comodin-y-la-raiz-global) como sufijo, este directorio se convierte en la raíz del árbol visualizado.

### Ejemplo del Metodo `show_tree`

Primero debes crear un *pipeline* sobre el cual puedas ejecutar este ejemplo. Un *pipeline* que consiste de un solo módulo [`parser`](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md) funcionará bien. Usa el método [`create_pipeline`](../creacion_de_pipelines/creacion_de_pipelines.md) para crearlo:


```python
# crea un pipeline para este ejemplo con un módulo parser
pipeline = krixik.create_pipeline(name="metodo_show_tree_1_parser",
                                  module_chain=["parser"])
```

Para facilitar las cosas, establece la ubicación de un archivo y guárdalo como una variable; luego usarás el mismo archivo varias veces pero con diferentes nombres. Lo haces de la siguiente manera:


```python
# define la ruta a un archivo de entrada en tu directorio de ejemplos
test_file = data_dir + "input/1984_muy_corto.txt"
```

Ahora usa el método [`process`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) para procesar el archivo por el *pipeline* varias veces, pero con `file_name` diferente cada vez. Observa la estructura de `symbolic_directory_path`s que se va creando:


```python
# procesa el mismo archivo por el pipeline varias veces
process_output = pipeline.process(
    local_file_path=test_file, # indícale a Krixik que quieres el archivo antes definido y guardado en una variable
    local_save_directory=data_dir + "output", # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False, # no mostrar actualizaciones de proceso al ejecutar el código
    symbolic_directory_path="/mi/ruta/personalizada",
    file_name="archivo_num_uno.txt",
)

process_output = pipeline.process(
    local_file_path=test_file, # indícale a Krixik que quieres el archivo antes definido y guardado en una variable
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False, # no mostrar actualizaciones de proceso al ejecutar el código
    symbolic_directory_path="/mi/ruta/personalizada",
    file_name="archivo_num_dos.txt",
)

process_output = pipeline.process(
    local_file_path=test_file, # indícale a Krixik que quieres el archivo antes definido y guardado en una variable
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False, # no mostrar actualizaciones de proceso al ejecutar el código
    symbolic_directory_path="/mi/ruta/personalizada/subdir",
    file_name="archivo_num_tres.txt",
)
```

Ahora puedes visualizar la estructura de directorios de tu *pipeline* con el método `show_tree`.

En este ejemplo usarás el operador comodín * para crear la raíz global en `symbolic_directory_path`, cosa que será explicada en breve.


```python
# visualiza la estructura de directorios de tu pipeline con la raíz global
show_tree_output = pipeline.show_tree(symbolic_directory_path="/*")
```

    /
    └── /my
        └── /custom
            └── /path
                ├── file_num_one.txt
                ├── file_num_two.txt
                └── /subpath
                    └── file_num_three.txt


Verás que los nombres de directorios están precedidos por el símbolo barra (`/`) y que los nombres de los archivos no. Esto te permite fácilmente diferenciar entre el uno y el otro en la salida de este método.

### El Operador Comodin y la Raiz Global

El operador comodín es el asterisco: *

Al igual que con el método [`list` (lista)](metodo_list_lista.md), el método [`semantic_search` (búsqueda semántica)](../metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) y el método [`keyword_search`](../metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md), puedes usar el operador comodín * en el argumento `symbolic_directory_path` para el método `show_tree`.

El operador comodín * puede usarse como sufijo en el método `show_tree` si deseas mostrar la estructura del árbol debajo de cierto directorio. La sintaxis de esto se vería así:

```python
# uso del operador comodín * en symbolic_direcctory_path
symbolic_directory_path='/home/files/studies*'
```

Usar este `symbolic_directory_path` con el método `show_tree` generaría una visualización de la estructura de directorios bajo `/home/files/studies`.

La máxima expresión del operador comodín * en `symbolic_directory_path` se llama "la raíz global". Es simplemente una barra seguida de un operador comodín * (`/*`), incluye todos los archivos en tu *pipeline*, y se ve así:


```python
# ejemplo de cómo se ve la raíz global
symbolic_directory_path='/*'
```

Como puedes ver en la salida de código anterior, usar la raíz global con el método `show_tree` devuelve una visualización de la estructura de directorio completa de tu *pipeline*.


```python
# elimina todos los datos procesados pertenecientes a este pipeline
reset_pipeline(pipeline)
```
