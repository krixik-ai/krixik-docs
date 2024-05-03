### Useful pipeline data properties

Let's look at some valuable data properties and apis of our pipeline `text_search_pipeline`. 

To view the module chain of your pipeline, use the `.module_chain` property.


```python
# view the module chain of your pipeline using the .module_chain property
text_search_pipeline.module_chain
```




    ['parser', 'text-embedder', 'vector-db']



For a more detailed view of your pipeline, including details on permissible input/output data types and extensions, use the `.config` property.  This essentially centralizes your pipeline's module configs in one place.

Your pipeline config file is also how you save / load your pipeline (so you do not need to go through the pythonic steps of building it each time you want to use it).


```python
# examine a pipeline's high level data by using the .config property
# print a dictionary nicely in an ide or notebook
json_print(text_search_pipeline.config)
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
