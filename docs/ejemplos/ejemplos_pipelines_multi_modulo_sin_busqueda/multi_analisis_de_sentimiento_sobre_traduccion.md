<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/multi_module_non_search_pipeline_examples/multi_sentiment_analysis_on_translation.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>


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


## *Pipeline* Multimodular: Análisis de Sentimiento sobre Traducción

Este documento detalla un *pipeline* multimodular que recibe un archivo de texto, lo [`traduce`](../../modulos/modulos_ia/modulo_translate_traduccion.md) (por lo pronto a inglés), y hace [análisis de sentimiento](../../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md) sobre cada frase traducida.

El documento está dividido en las siguientes secciones:

- [Monta tu *Pipeline*](#monta-tu-pipeline)
- [Procesa un Archivo de Entrada](#procesa-un-archivo-de-entrada)

### Monta tu *Pipeline*

Para lograr lo arriba descrito, monta un pipeline que consiste de los siguientes módulos en secuencia:

- Un módulo [`parser` (fragmentación de texto)](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md).

- Un módulo [`translate` (traducción)](../../modulos/modulos_ia/modulo_translate_traduccion.md).

- Un módulo [`sentiment` (análisis de sentimiento)](../../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md).

Para crear el pipeline usarás el método [`create_pipeline`](../../sistema/creacion_de_pipelines/creacion_de_pipelines.md) de la siguiente manera:


```python
# creación del pipeline descrito
pipeline = krixik.create_pipeline(name="multi_analisis_de_sentimiento_sobre_traduccion",
                                  module_chain=["parser", "translate", "sentiment"])
```

### Procesa un Archivo de Entrada

Dado que vas a [`traducir`](../../modulos/modulos_ia/modulo_translate_traduccion.md) y luego hacer [`análisis de sentimiento`](../../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md)—y dado que los modelos de este segundo módulo están por lo pronto para inglés—usa un archivo inicial en español. Para traducirlo de español al inglés puedes usar el modelo (no-predeterminado) [`opus-mt-es-en`](https://huggingface.co/Helsinki-NLP/opus-mt-es-en) del módulo [`translate` (traducción)](../../modulos/modulos_ia/modulo_translate_traduccion.md).

Como usarás los modelos predeterminados para todo otro módulo en el *pipeline*, no tendrás que especificarlos en el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).


```python
# procesa el archivo a través del pipeline según lo arriba descrito
process_output = pipeline.process(
    local_file_path=data_dir + "input/resena_espanol.txt",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False, # no mostrar actualizaciones de proceso al ejecutar el código
    modules={"module_2": {"model": "opus-mt-es-en"}} # especifica un modelo no-predeterminado para usar en el segundo módulo
)
```

La salida del proceso se reproduce con el siguiente código. Para aprender más sobre cada componente de esta salida, revisa la documentación del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).

Dado que la salida de este modelo/módulo es un archivo JSON, la salida también se incluye en el objeto (esto solo ese el caso para salidas JSON). Además, el archivo de salida se ha guardado en la ubicación indicada bajo `process_output_files`. El `file_id` del archivo procesado es el prefijo del nombre del archivo de salida en esta ubicación.


```python
# nítidamente reproduce la salida de este proceso
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "multi_sentiment_analysis_on_translation",
      "request_id": "0719e2d3-24cc-4a12-9f84-d90d1a9e964e",
      "file_id": "ed5b8fa4-3f4b-4e10-b61d-05536db5e929",
      "message": "SUCCESS - output fetched for file_id ed5b8fa4-3f4b-4e10-b61d-05536db5e929.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "For the jobs I'm doing I turned out very good.",
          "positive": 1.0,
          "negative": 0.0,
          "neutral": 0.0
        },
        {
          "snippet": "In one hour load the battery and last more than 3 hours of continuous work.",
          "positive": 0.008,
          "negative": 0.992,
          "neutral": 0.0
        },
        {
          "snippet": "A golasse to have a second batter.",
          "positive": 0.023,
          "negative": 0.977,
          "neutral": 0.0
        },
        {
          "snippet": "Cmodo and with good torque.",
          "positive": 1.0,
          "negative": 0.0,
          "neutral": 0.0
        },
        {
          "snippet": "I agree.",
          "positive": 1.0,
          "negative": 0.0,
          "neutral": 0.0
        }
      ],
      "process_output_files": [
        "../../../data/output/ed5b8fa4-3f4b-4e10-b61d-05536db5e929.json"
      ]
    }


Para confirmar que todo salió como esperabas, carga el archivo de `process_output_files`:


```python
# carga la salida del proceso del archivo
with open(process_output["process_output_files"][0]) as f:
    print(json.dumps(json.load(f), indent=2))
```

    [
      {
        "snippet": "For the jobs I'm doing I turned out very good.",
        "positive": 1.0,
        "negative": 0.0,
        "neutral": 0.0
      },
      {
        "snippet": "In one hour load the battery and last more than 3 hours of continuous work.",
        "positive": 0.008,
        "negative": 0.992,
        "neutral": 0.0
      },
      {
        "snippet": "A golasse to have a second batter.",
        "positive": 0.023,
        "negative": 0.977,
        "neutral": 0.0
      },
      {
        "snippet": "Cmodo and with good torque.",
        "positive": 1.0,
        "negative": 0.0,
        "neutral": 0.0
      },
      {
        "snippet": "I agree.",
        "positive": 1.0,
        "negative": 0.0,
        "neutral": 0.0
      }
    ]


Notarás que, en el primer fragmento devuelto, la palabra "sillón" carece de su segunda vocal y es reproducida como "silln". Este es un problema de modelo: el modelo seleccionado del módulo [`translate` (traducción)](../../modulos/modulos_ia/modulo_translate_traduccion.md) puede tener dificultades con caracteres acentuados y/o puede simplemente eliminarlos. Es importante que te familiarices con las peculiaridades de los modelos IA que piensas usar con frecuencia.


```python
# elimina todos los datos procesados pertenecientes a este pipeline
reset_pipeline(pipeline)
```
