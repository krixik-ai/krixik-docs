<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/modules/ai_modules/text-embedder_module.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>


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


## El Módulo `text-embedder` (Encaje Léxico)

El módulo `text-embedder` (encaje léxico) toma como entrada uno o varios fragmentos de texto, convierte cada uno en un vector (una representación matemática del fragmento que conserva su significado) y devuelve un arreglo que contiene todos los vectores generados. Estos arreglos vectoriales pueden luego ser ingresados en una base de datos vectorial para habilitar búsqueda semántica (también conocida como búsqueda vectorial).

Mucho se ha escrito sobre las incrustaciones de vectores (*vector embeddings*). Si quieres aprender más al respecto, puedes (por ejemplo) arrancar con este [artículo en Medium](https://devjaime.medium.com/qu%C3%A9-son-las-incrustaciones-de-vectores-en-ia-y-llm-5e4a4bce454e) o este [video en YouTube](https://www.youtube.com/watch?v=Vy7WwP5ULPg).

Esta introducción al módulo `text-embedder` se divide en las siguientes secciones:

- [Entradas y Salidas del Módulo `text-embedder`](#entradas-y-salidas-del-modulo-text-embedder)
- [Modelos Disponibles en el Módulo `text-embedder`](#modelos-disponibles-en-el-modulo-text-embedder)
- [Parámetros de los Modelos en el Módulo `text-embedder`](#parametros-de-los-modelos-en-el-modulo-text-embedder)
- [Un *Pipeline* de Módulo Único para el Módulo `text-embedder`](#un-pipeline-de-modulo-unico-para-el-modulo-text-embedder)
- [Más Información sobre el Módulo `text-embedder`: IO y Conectabilidad](#mas-informacion-sobre-el-modulo-text-embedder-io-y-conectabilidad)

### Entradas y Salidas del Modulo `text-embedder`

El módulo `text-embedder` (encaje léxico) recibe entradas en formato JSON. Las entradas JSON deben respetar [este formato](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/formato_JSON_entrada.md).

El archivo JSON de entrada también puede incluir, acompañando a cada fragmento, un par clave-valor en el que la clave es el *string* `"line numbers"` y el valor es una lista de *int* que indica cada número de línea en el documento original sobre el que yacía ese fragmento de texto. Esto te puede ayudar a identificar qué línea del documento original está incrustada en cada vector. 

El módulo `text-embedder` devuelve un arreglo vectorial en un archivo NPY.

Para ver un ejemplo del formato que debe seguir un archivo de entrada al módulo `text-embedder`, detalla el contenido de la salida JSON reproducida después del siguiente código. Así se debe estructurar un archivo de entrada para este módulo (ten en cuenta que la clave `line numbers` es opcional):


```python
# detalla el contenido de un archivo de entrada válido para este módulo
test_file = data_dir + "input/1984_fragmentos.json"
with open(test_file, "r") as file:
    print(json.dumps(json.load(file), indent=2))
```

    [
      {
        "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
        "line_numbers": [
          1
        ]
      },
      {
        "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
        "line_numbers": [
          2,
          3,
          4,
          5
        ]
      }
    ]


### Modelos Disponibles en el Modulo `text-embedder`

Puedes activar cualquiera de los siguientes modelos al usar el módulo `text-embedder`:

- [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) (predeterminado)

- [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2)

- [all-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2)

- [multi-qa-MiniLM-L6-cos-v1](https://huggingface.co/sentence-transformers/multi-qa-MiniLM-L6-cos-v1)

- [msmarco-distilbert-dot-v5](https://huggingface.co/sentence-transformers/msmarco-distilbert-dot-v5)

Usa el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) en el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) para determinar qué modelo quieres activo al procesar archivos a través del módulo `text-embedder`.

### Parametros de los Modelos en el Modulo `text-embedder`

Todos los modelos del módulo `text-embedder` son parametrizables. Toman un parámetro:

- `quantize` (bool) - Si su valor es `True`, reduce el número de puntos decimales en los vectores. Esto brinda mejoras en velocidad y memoria a cambio de cierta pérdida en precisión (esta es una explicación muy simplificada de lo que es la cuantificación vectorial). Su valor predeterminado es `True`.

Por ende, al elegir qué modelo usar a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), `params` puede incluir un valor para `quantize`. Por ejemplo:

```python
# ejemplo de selección de modelo para el módulo text-embedder en el método process
modules={'text-embedder': {"model": "all-mpnet-base-v2",
                           "params": {"quantize": False}}}
```

### Un *Pipeline* de Modulo Unico para el Modulo `text-embedder`

Haz [clic aquí](../../ejemplos/ejemplos_pipelines_modulo_unico/unico_text-embedder_encaje_lexico.md) para detallar un ejemplo de un *pipeline* de módulo único con un módulo `text-embedder`.

Ten en cuenta que toda salida de este *pipeline* será en formato NPY, el cual no es legible para humanos (es un arreglo de vectores).

### Mas Informacion sobre el Modulo `text-embedder`: IO y Conectabilidad

Haz [clic aquí](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md) para visitar documentación Krixik titulada `Métodos de Conveniencia (¡y Más!)`. Allí encontrarás dos herramientas con las que puedes aprender más sobre el módulo `text-embedder`: 

- [Ve Ejemplos de Entradas y Salidas de un Módulo](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-ejemplos-de-entradas-y-salidas-de-un-modulo)

- [Ve Data de Conectividad de un Módulo con el Método `click_data`](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-data-de-conectividad-de-un-modulo-con-el-metodo-click_data)
