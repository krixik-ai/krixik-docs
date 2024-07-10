<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/pipeline_creation/pipeline_config.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Pipeline `.config`

The `.config` method allows you to view a pipeline's configuration. For each module in the pipeline it displays acceptable input formats, output formats, models available, and any parameters of the available models.  In other words, a pipeline's configuration is its complete "under the hood" description.

Using the `.config` method is very simple. First let's create a pipeline to try it on:


```python
# first create a valid pipeline
pipeline = krixik.create_pipeline(name="pipeline_config_1_parser_translate_sentiment", module_chain=["translate", "sentiment"])
```

Now let's view this pipeline's configuration with the `.config` method:


```python
# view the pipeline's configuration file
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



As you can see, the `.config` method has provided all relevant details for this pipeline's modules, which are a [`translate module`](../../modules/ai_modules/translate_module.md) and a [`sentiment module`](../../modules/ai_modules/sentiment_module.md). A blueprint of sorts has been displayed.
