## Single-Module Pipeline: `text-embedder`

This document is a walkthrough of how to assemble and use a single-module pipeline that only includes a [`text-embedder`](../../modules/ai_model_modules/text-embedder_module.md) module. It's divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Required Input Format](#required-input-format)
- [Using the Default Model](#using-the-default-model)
- [Examining Process Output Locally](#examining-process-output-locally)
- [Using a Non-Default Model](#using-a-non-default-model)


```python
# import utilities
import sys 
import json
import importlib
sys.path.append('../../../')
reset = importlib.import_module("utilities.reset")
reset_pipeline = reset.reset_pipeline

# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os
load_dotenv("../../../.env")
MY_API_KEY = os.getenv('MY_API_KEY')
MY_API_URL = os.getenv('MY_API_URL')

# import krixik and initialize it with your personal secrets
from krixik import krixik
krixik.init(api_key = MY_API_KEY, 
            api_url = MY_API_URL)
```

    SUCCESS: You are now authenticated.


### Pipeline Setup

Let's first instantiate a single-module [`text-embedder`](../../modules/ai_model_modules/text-embedder_module.md) pipeline.

We use the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method for this, passing only the [`text-embedder`](../../modules/ai_model_modules/text-embedder_module.md) module name into `module_chain`.


```python
# create a pipeline with a single text-embedder module

pipeline_1 = krixik.create_pipeline(name="single_text-embedder-1",
                                    module_chain=["text-embedder"])
```

### Required Input Format

The [`text-embedder`](../../modules/ai_model_modules/text-embedder_module.md) module accepts JSON file input. The input JSON must respect [this format](../../system/parameters_processing_files_through_pipelines/JSON_input_format.md).

The JSON file may optionally also include, along with each snippet, a key-value pair in which the key is the string `"line numbers"` and the value is an integer list of every line number of the original document that the snippet is on. This will make it easier for you to identify what document line each vector is an embedding of.

Let's take a quick look at a valid input file, and then process it.


```python
# examine contents of a valid input file

with open("../../../data/input/1984_snippets.json", "r") as file:
    print(json.dumps(json.load(file), indent=2))
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


### Using the Default Model

Let's process our test input file using the [`text-embedder`](../../modules/ai_model_modules/text-embedder_module.md) module's [default model](../../modules/ai_model_modules/text-embedder_module.md#available-models-in-the-text-embedder-module): [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).

Given that this is the default model, we need not specify model selection through the optional [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

In a later section of this document we will process the same file again, but select our model and the quantization thereof explicitly.


```python
# process the file with the default model

process_output_1 = pipeline_1.process(local_file_path="../../../data/input/1984_snippets.json", # the initial local filepath where the input file is stored
                                      local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                      expire_time=60 * 30, # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True, # wait for process to complete before returning IDE control to user
                                      verbose=False) # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Moreover, the output file itself has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process

print(json.dumps(process_output_1, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_text-embedder-1",
      "request_id": "1f16bcaa-1d08-4286-91c3-6fac2bbf17b3",
      "file_id": "ebd43e63-0f3a-41ba-9db9-f768d11a048a",
      "message": "SUCCESS - output fetched for file_id ebd43e63-0f3a-41ba-9db9-f768d11a048a.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/ebd43e63-0f3a-41ba-9db9-f768d11a048a.npy"
      ]
    }


### Examining Process Output Locally

The outputted NPY file containing embedding vectors of our input data can be examined as follows. For the sake of clarity, in this example we will simply print the shape, and not any of the contents, of the returned array:


```python
# examine vector output
import numpy as np

vectors = np.load(process_output_1["process_output_files"][0])
print(vectors.shape)
```

    (2, 384)


In other words, the array has 2 rows with 384 values in each row. 

In the context of the input file, the first row is the vectorized form of our first snippet: "It was a bright cold day in April, and the clocks were striking thirteen."

### Using a Non-Default Model

To use a [non-default model](../../modules/ai_model_modules/text-embedder_module.md#available-models-in-the-text-embedder-module) like [`all-mpnet-base-v2`](https://huggingface.co/sentence-transformers/all-mpnet-base-v2), we must enter it explicitly through the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument when invoking the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method. As [module documentation](../../modules/ai_model_modules/text-embedder_module.md) indicates, you can also specify whether or not you wish to use the quantized version of the model.


```python
# process the file with a non-default model

process_output_2 = pipeline_1.process(local_file_path="../../../data/input/1984_snippets.json", # all parameters save 'modules' as above
                                      local_save_directory="../../../data/output",
                                      expire_time=60 * 30,
                                      wait_for_process=True,
                                      verbose=False,
                                      modules={"text-embedder": {"model": "all-mpnet-base-v2", "params": {"quantize": False}}}) # specify a non-default model for this process
```

Now we can examine the output as we did above.


```python
# nicely print the output of this process

print(json.dumps(process_output_2, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_text-embedder-1",
      "request_id": "35c58c69-cb16-486b-970d-b1817c3671be",
      "file_id": "b541407f-134a-4e45-9c2a-360c3cc759e9",
      "message": "SUCCESS - output fetched for file_id b541407f-134a-4e45-9c2a-360c3cc759e9.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/b541407f-134a-4e45-9c2a-360c3cc759e9.npy"
      ]
    }



```python
# delete all processed datapoints belonging to this pipeline

reset_pipeline(pipeline_1)
```