<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/pipeline_creation/pipeline_config.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>


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


## Configuración de *Pipelines*

El método `config` te permite ver la configuración de un *pipeline*. Este método muestra, para cada módulo en el *pipeline*, formatos de entrada aceptables, formatos de salida, modelos disponibles, y todos los parámetros de los modelos disponibles. Podría decirse que la configuración de un *pipeline* es su descripción completa y a fondo.

Usar el método `config` es muy simple. Primero crea un *pipeline* sobre el que lo puedas usar:


```python
# primero crea un pipeline válido
pipeline = krixik.create_pipeline(name="pipeline_config_1_translate_sentiment",
                                  module_chain=["translate", "sentiment"])
```

Ahora mira la configuración de este *pipeline* con el método `config`:


```python
# ver el archivo de configuración del pipeline
pipeline.config
```




    {'pipeline': {'name': 'pipeline_config_1_parser_translate_sentiment',
      'modules': [{'name': 'translate',
        'models': [{'name': 'opus-mt-de-en'},
         {'name': 'opus-mt-en-es'},
         {'name': 'opus-mt-es-en'},
         {'name': 'opus-mt-en-fr'},
         {'name': 'opus-mt-fr-en'},
         {'name': 'opus-mt-it-en'},
         {'name': 'opus-mt-zh-en'}],
        'defaults': {'model': 'opus-mt-en-es'},
        'input': {'type': 'json', 'permitted_extensions': ['.json']},
        'output': {'type': 'json'}},
       {'name': 'sentiment',
        'models': [{'name': 'distilbert-base-uncased-finetuned-sst-2-english'},
         {'name': 'bert-base-multilingual-uncased-sentiment'},
         {'name': 'distilbert-base-multilingual-cased-sentiments-student'},
         {'name': 'distilroberta-finetuned-financial-news-sentiment-analysis'}],
        'defaults': {'model': 'distilbert-base-uncased-finetuned-sst-2-english'},
        'input': {'type': 'json', 'permitted_extensions': ['.json']},
        'output': {'type': 'json'}}]}}



Como puedes ver, el método `config` devuelve todos los detalles relevantes sobre los módulos de este *pipeline*, que son un módulo [`translate`](../../modulos/modulos_ia/modulo_translate_traduccion.md) y un módulo [`sentiment`](../../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md). Se ha reproducido un esquema, o plano, de cada módulo.


```python
# elimina todos los datos procesados pertenecientes a este pipeline
reset_pipeline(pipeline)
```
