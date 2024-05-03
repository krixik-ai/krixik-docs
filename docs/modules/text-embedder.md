## the `text-embedder` module

This document reviews the `text-embedder` module - which takes as input a json of text snippets, transforms each into a vector, and returns an array of those vectors in a .npy flie.

This document includes an overview of custom pipeline setup, current model set, parameters, and `.process` usage for this module.

To follow along with this demonstration be sure to initialize your krixik session with your api key and url as shown below. 

We illustrate loading these required secrets in via [python-dotenv](https://pypi.org/project/python-dotenv/), storing those secrets in a `.env` file.  This is always good practice for storing / loading secrets (e.g., doing so will reduce the chance you inadvertantly push secrets to a repo).


```python
# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os
load_dotenv("../.env")
MY_API_KEY = os.getenv('MY_API_KEY')
MY_API_URL = os.getenv('MY_API_URL')

# import krixik and initialize it with your personal secrets
from krixik import krixik
krixik.init(api_key = MY_API_KEY, 
            api_url = MY_API_URL)
```


This small function prints dictionaries very nicely in notebooks / markdown.


```python
# print dictionaries / json nicely in notebooks / markdown
import json
def json_print(data):
    print(json.dumps(data, indent=2))
```

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [using the default model](#using-the-default-model)
- [examining process output locally](#examining-process-output-locally)
- [processing with a non-default model](#processing-with-a-non-default-model)


## Pipeline setup

Below we setup a simple one module pipeline using the `text-embedder` module. 


```python
# import custom module creation tools
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# instantiate module
module_1 = Module(module_type="text-embedder")

# create custom pipeline object
custom = CreatePipeline(name='text-embedder-pipeline-1', 
                        module_chain=[module_1])

# pass the custom object to the krixik operator (note you can also do this by passing its config)
pipeline = krixik.load_pipeline(pipeline=custom)
```

The `text-embedder` module comes with a five very popular models from huggingface.  Each model functions in the same general manner - transforming text into dense vectors.

- [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) (default)
- [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2)
- [all-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2)
- [multi-qa-MiniLM-L6-cos-v1](https://huggingface.co/sentence-transformers/multi-qa-MiniLM-L6-cos-v1) 
- [msmarco-distilbert-dot-v5](https://huggingface.co/sentence-transformers/msmarco-distilbert-dot-v5)

Quantized versions of each are also available for use.

These available modeling options and parameters are stored in our custom pipeline's configuration (described further in LINK HERE).  We can examine this configuration as shown below.

Notice each model has a single parameter - `quantize` - that can be set to a boolean value `True/False`.  By default the `quantize` is `True`.


```python
# nicely print the configuration of uor custom pipeline
json_print(custom.config)
```

    {
      "pipeline": {
        "name": "text-embedder-pipeline-1",
        "modules": [
          {
            "name": "text-embedder",
            "models": [
              {
                "name": "all-MiniLM-L6-v2",
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
                "name": "all-MiniLM-L12-v2",
                "params": {
                  "quantize": {
                    "type": "bool",
                    "default": true
                  }
                }
              },
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
              }
            ],
            "defaults": {
              "model": "all-MiniLM-L6-v2",
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
          }
        ]
      }
    }


Here we can see the models and their associated parameters available for use.

## using the default model

We first define a path to a local input file.


```python
# define path to an input file from examples directory
test_file = "../input_data/1984_very_short.json"
```

Lets take a quick look at this file before processing.


```python
# examine contents of input file
json_print(json.load(open(test_file)))
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


Two sentences and their associated line numbers in the original text.

Now let's process it using our `default` model: .  Because [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) (quantized) is the default model we need not input the optional `modules` argument into `.process`.  Afterwords we will process the same file again, but select our model and quantization explicitly.


```python
# define path to an input file from examples directory
test_file = "../input_data/1984_very_short.json"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*3,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  

Because the output of this particular module-model is a `.npy` file embedding vectors of the input, the process output is provided in this object is null.  However these files have been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed file is used as a filename prefix for both output files.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "text-embedder-pipeline-1",
      "request_id": "597806e7-f56b-4f3b-9f76-a6f474ad3046",
      "file_id": "bac4fa57-33ea-43dd-bfc6-ef01fcbb1a7a",
      "message": "SUCCESS - output fetched for file_id bac4fa57-33ea-43dd-bfc6-ef01fcbb1a7a.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "./bac4fa57-33ea-43dd-bfc6-ef01fcbb1a7a.npy"
      ]
    }


### examining process output locally

The `.npy` containing embedding vectors of our input data can be examined as follows.  For the sake of clarity we will simply print the shape of the returned array.


```python
# examine vector output
import numpy as np
vectors = np.load(process_output['process_output_files'][0])
print(vectors.shape)
```

    (2, 384)


 Each row of the returned array is an individual vector matching the index of the input.

 e.g., the first row is the vectorized form of our first input snippet shown above: "It was a bright cold day in April, and the clocks were striking thirteen.".

### processing with a non-default model

To process with a non-default model include the `modules` input argument defining your choice of model and quantization.

For example if we wish to process with [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) un-quantized this would new input argument would take the form

```
modules={
        "text-embedder":
            {
                "model": "all-mpnet-base-v2",
                "params":{"quantize": False}
                }
            }
```


```python
# define path to an input file from examples directory
test_file = "../input_data/1984_very_short.json"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*3,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,            # set verbosity to False
                                  modules={"text-embedder":
                                            {"model": "all-mpnet-base-v2",
                                             "params":{"quantize": False}}})
```

Now we can examine the output as we did above.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "text-embedder-pipeline-1",
      "request_id": "551e99e7-765d-4a7a-b388-7c165e2457e0",
      "file_id": "da28bb6a-dc12-4f9f-a96d-59f09a63a136",
      "message": "SUCCESS - output fetched for file_id da28bb6a-dc12-4f9f-a96d-59f09a63a136.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "./da28bb6a-dc12-4f9f-a96d-59f09a63a136.npy"
      ]
    }

