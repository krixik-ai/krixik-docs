<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/pipeline_creation/pipeline_config.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

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
