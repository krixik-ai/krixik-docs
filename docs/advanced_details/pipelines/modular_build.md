
### Building a pipeline one module at a time

You can build and ad modules one-at-a-time as well using the `.add` api.  Each time a module is added the same sort of connection test described above is performed on the entire module chain.


```python
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# define a module
module_1 = Module(module_type='transcribe')

# instantiate an empty custom pipeline
pipeline = CreatePipeline(name='my-custom-pipeline')

# add the first module to the pipeline
pipeline.add(module_1)
```


```python
# define another module
module_2 = Module(module_type='sentiment')

# add the second module to the pipeline
pipeline.add(module_2)
```


```python
# define another module
module_3 = Module(module_type='translate')

# add the third module to the pipeline
pipeline.add(module_3)
```

You can now use all of the previously detailed attributes to view your pipelines configuration.  For example the `.config` attribute.


```python
# examine a pipeline's config
# print a dictionary nicely in an ide or notebook
json_print(pipeline.config)

```

    {
      "pipeline": {
        "name": "my-custom-pipeline",
        "modules": [
          {
            "name": "transcribe",
            "models": [
              {
                "name": "whisper-tiny"
              },
              {
                "name": "whisper-base"
              },
              {
                "name": "whisper-small"
              },
              {
                "name": "whisper-medium"
              },
              {
                "name": "whisper-large-v3"
              }
            ],
            "defaults": {
              "model": "whisper-tiny"
            },
            "input": {
              "type": "audio",
              "permitted_extensions": [
                ".mp3",
                ".mp4"
              ]
            },
            "output": {
              "type": "json"
            }
          },
          {
            "name": "sentiment",
            "models": [
              {
                "name": "distilbert-base-uncased-finetuned-sst-2-english"
              },
              {
                "name": "bert-base-multilingual-uncased-sentiment"
              },
              {
                "name": "distilbert-base-multilingual-cased-sentiments-student"
              },
              {
                "name": "distilroberta-finetuned-financial-news-sentiment-analysis"
              }
            ],
            "defaults": {
              "model": "distilbert-base-uncased-finetuned-sst-2-english"
            },
            "input": {
              "type": "json",
              "permitted_extensions": [
                ".json"
              ]
            },
            "output": {
              "type": "json"
            }
          },
          {
            "name": "translate",
            "models": [
              {
                "name": "opus-mt-de-en"
              },
              {
                "name": "opus-mt-en-es"
              },
              {
                "name": "opus-mt-es-en"
              },
              {
                "name": "opus-mt-en-fr"
              },
              {
                "name": "opus-mt-fr-en"
              },
              {
                "name": "opus-mt-it-en"
              },
              {
                "name": "opus-mt-zh-en"
              }
            ],
            "defaults": {
              "model": "opus-mt-en-es"
            },
            "input": {
              "type": "json",
              "permitted_extensions": [
                ".json"
              ]
            },
            "output": {
              "type": "json"
            }
          }
        ]
      }
    }

