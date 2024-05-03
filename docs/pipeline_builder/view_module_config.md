### Viewing a module's `config` metadata

To see the highest level metadata on this module can be viewed via the `.config` property.

This high level information is especially useful when *processing* data with a module in a pipeline, but its also a great place to get started in understanding current module offerings.  

Specifically, `.config` tells you about a module's defaults, available models, and what kind of input/output data you need / should expect as output from the module.

Lets take a look at our first module's `.config`.


```python
# print a dictionary nicely in an ide or notebook
json_print(module_1.config)
```

    {
      "module": {
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
        "input": {
          "type": "audio",
          "permitted_extensions": [
            ".mp3",
            ".mp4"
          ]
        },
        "output": {
          "type": "json",
          "permitted_extensions": [
            ".json"
          ]
        },
        "defaults": {
          "model": "whisper-tiny"
        }
      }
    }


And the second module's.  In this case we see that each module has a `quantize` parameter that can be set at processing time.


```python
# print a dictionary nicely in an ide or notebook
json_print(module_2.config)
```

    {
      "module": {
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
        "input": {
          "type": "json",
          "permitted_extensions": [
            ".json"
          ]
        },
        "output": {
          "type": "npy",
          "permitted_extensions": [
            ".npy"
          ]
        },
        "defaults": {
          "model": "multi-qa-MiniLM-L6-cos-v1",
          "params": {
            "quantize": true
          }
        }
      }
    }


Advanced module data properties are described in Sectino 2.  Their knowledge is not pre-requisite to building pipelines. 