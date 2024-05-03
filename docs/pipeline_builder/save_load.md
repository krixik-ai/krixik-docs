###  Save and load your pipeline config

Once your pipeline is built, connection tested, and input tested, it's a good idea to save its config.  This allows you to load your pipeline directly from file in the future, saving the hassle of having to rebuild it pythonically each time you want to use it. 

To save the config file of a pipeline use the `.save` method, providing a path to a local `.yml`.


```python
# save your pipeline config to a .yaml file
text_search_pipeline.save('text_search_pipeline.yaml')
```

Load your pipeline either directly on instantiation or by using the `.load` method.


```python
from krixik.pipeline_builder.pipeline import CreatePipeline

# load pipeline directly on instantiation
reloaded_pipeline = CreatePipeline(config_path = 'text_search_pipeline.yaml')
```


```python
# examine a pipeline's high level data by using the .config property
# print a dictionary nicely in an ide or notebook
json_print(reloaded_pipeline.config)
```

    {
      "pipeline": {
        "name": "my-text-search-pipeline",
        "modules": [
          {
            "name": "parser",
            "models": [
              {
                "name": "sentence"
              },
              {
                "name": "fixed",
                "params": {
                  "chunk_size": {
                    "type": "int",
                    "default": 10
                  },
                  "overlap_size": {
                    "type": "int",
                    "default": 2
                  }
                }
              }
            ],
            "defaults": {
              "model": "sentence"
            },
            "input": {
              "type": "text",
              "permitted_extensions": [
                ".txt",
                ".pdf",
                ".docx",
                ".pptx"
              ]
            },
            "output": {
              "type": "json"
            }
          },
          {
            "name": "text-embedder",
            "models": [
              {
                "name": "multi-qa-MiniLM-L6-cos-v1",
                "params": {
                  "quantize": {
                    "type": "bool",
                    "default": true
                  }
                }
              },
              {
                "name": "msmarco-distilbert-dot-v5",
                "params": {
                  "quantize": {
                    "type": "bool",
                    "default": true
                  }
                }
              },
              {
                "name": "all-MiniLM-L12-v2",
                "params": {
                  "quantize": {
                    "type": "bool",
                    "default": true
                  }
                }
              },
              {
                "name": "all-mpnet-base-v2",
                "params": {
                  "quantize": {
                    "type": "bool",
                    "default": true
                  }
                }
              },
              {
                "name": "all-MiniLM-L6-v2",
                "params": {
                  "quantize": {
                    "type": "bool",
                    "default": true
                  }
                }
              }
            ],
            "defaults": {
              "model": "multi-qa-MiniLM-L6-cos-v1",
              "params": {
                "quantize": true
              }
            },
            "input": {
              "type": "json",
              "permitted_extensions": [
                ".json"
              ]
            },
            "output": {
              "type": "npy"
            }
          },
          {
            "name": "vector-db",
            "models": [
              {
                "name": "faiss"
              }
            ],
            "defaults": {
              "model": "faiss"
            },
            "input": {
              "type": "npy",
              "permitted_extensions": [
                ".npy"
              ]
            },
            "output": {
              "type": "faiss"
            }
          }
        ]
      }
    }
