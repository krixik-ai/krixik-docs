<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/pipeline_creation/pipeline_config.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>


```python
import os
import sys
import json
import importlib
from pathlib import Path

# demo setup - including secrets instantiation, requirements installation, and path setting
if os.getenv("COLAB_RELEASE_TAG"):
    # if running this notebook in collab - make sure to enter your secrets
    MY_API_KEY = "YOUR_API_KEY_HERE"
    MY_API_URL = "YOUR_API_URL_HERE"

    # if running this notebook on collab - install requirements and pull required subdirectories
    # install krixik python client
    !pip install krixik

    # install github clone - allows for easy cloning of subdirectories from docs repo: https://github.com/krixik-ai/krixik-docs
    !pip install github-clone

    # clone datasets
    if not Path("data").is_dir():
        !ghclone https://github.com/krixik-ai/krixik-docs/tree/main/data
    else:
        print("docs datasets already cloned!")

    # define data dir
    data_dir = "./data/"

    # create output dir
    from pathlib import Path

    Path(data_dir + "/output").mkdir(parents=True, exist_ok=True)

    # pull utilities
    if not Path("utilities").is_dir():
        !ghclone https://github.com/krixik-ai/krixik-docs/tree/main/utilities
    else:
        print("docs utilities already cloned!")
else:
    # if running local pull of docs - set paths relative to local docs structure
    # import utilities
    sys.path.append("../../../")

    # define data_dir
    data_dir = "../../../data/"

    # if running this notebook locally from krixik docs repo - load secrets from a .env placed at the base of the docs repo
    from dotenv import load_dotenv

    load_dotenv("../../../.env")

    MY_API_KEY = os.getenv("MY_API_KEY")
    MY_API_URL = os.getenv("MY_API_URL")


# load in reset
reset = importlib.import_module("utilities.reset")
reset_pipeline = reset.reset_pipeline


# import krixik and initialize it with your personal secrets
from krixik import krixik

krixik.init(api_key=MY_API_KEY, api_url=MY_API_URL)
```

    SUCCESS: You are now authenticated.


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


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
