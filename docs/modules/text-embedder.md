## The `text-embedder` module

This document reviews the `text-embedder` module - which takes as input a json of text snippets, transforms each into a vector, and returns an array of those vectors in a .npy flie.

This document includes an overview of custom pipeline setup, current model set, parameters, and `.process` usage for this module.

To follow along with this demonstration be sure to initialize your krixik session with your api key and url as shown below. 

We illustrate loading these required secrets in via [python-dotenv](https://pypi.org/project/python-dotenv/), storing those secrets in a `.env` file.  This is always good practice for storing / loading secrets (e.g., doing so will reduce the chance you inadvertantly push secrets to a repo).

A table of contents for the remainder of this document is shown below.

- [pipeline setup](#pipeline-setup)
- [required input format](#required-input-format)
- [using the default model](#using-the-default-model)
- [examining process output locally](#examining-process-output-locally)
- [processing with a non-default model](#processing-with-a-non-default-model)
- [using a non-default model](#using-a-non-default-model)

## Pipeline setup

Below we setup a simple one module pipeline using the `text-embedder` module.

We do this by passing the module name to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(name="modules-text-embedder-docs",
                                  module_chain=["text-embedder"])
```

The `text-embedder` module comes with a five very popular models from huggingface.  Each model functions in the same general manner - transforming text into dense vectors.

- [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) (default)
- [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2)
- [all-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2)
- [multi-qa-MiniLM-L6-cos-v1](https://huggingface.co/sentence-transformers/multi-qa-MiniLM-L6-cos-v1) 
- [msmarco-distilbert-dot-v5](https://huggingface.co/sentence-transformers/msmarco-distilbert-dot-v5)

Quantized versions of each are also available for use.

Each model has a single parameter - `quantize` - that can be set to a boolean value `True/False`.  By default the `quantize` is `True`.

These available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).

## Required input format

The `text-embedder` module accepts as input `.json` files consisting of a *list of dictionaries*.  Each dictionary may have as many key-value pairs as desired, but *must* contain the key name *snippet*.  This is the key `text-embedder` will act on.

Optionally, you may also include a key `line_numbers` containing a list of `integer` line numbers associated with the snippet.

Let's look at an example of a small valid input - and then process it.


```python
# examine contents of a valid input file
test_file = "../../data/input/1984_very_short.json"
with open(test_file, "r") as file:
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


## Using the default model

Let's process our small input example using the `default` model: .  Because [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) (quantized) is the default model we need not input the optional `modules` argument into `.process`.  Afterwords we will process the same file again, but select our model and quantization explicitly.


```python
# define path to an input file from examples directory
test_file = "../../data/input/1984_very_short.json"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory="../../data/output", # save output repo data output subdir
                                  expire_time=60 * 10,      # set all process data to expire in 10 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  

Because the output of this particular module-model is a `.npy` file embedding vectors of the input, the process output is provided in this object is null.  However these files have been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed file is used as a filename prefix for both output files.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "my-text-embedder-pipeline",
      "request_id": "3517d9da-375e-4824-8212-fc9bebfb7c74",
      "file_id": "525ee760-86ca-4b96-8bd9-46f905b85590",
      "message": "SUCCESS - output fetched for file_id 525ee760-86ca-4b96-8bd9-46f905b85590.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../data/output/525ee760-86ca-4b96-8bd9-46f905b85590.npy"
      ]
    }


## Examining process output locally

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

## Processing with a non-default model

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
test_file = "../../data/input/1984_very_short.json"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory="../../data/output", # save output repo data output subdir
                                  expire_time=60 * 10,      # set all process data to expire in 10 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,            # set verbosity to False
                                  modules={"text-embedder":
                                            {"model": "all-mpnet-base-v2",
                                             "params":{"quantize": False}}})
```

Now we can examine the output as we did above.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "my-text-embedder-pipeline",
      "request_id": "008e70a1-9b55-4fe0-9b02-55dd4b02798e",
      "file_id": "a7e7dd02-fd28-4a8e-8fae-eb495db0bd86",
      "message": "SUCCESS - output fetched for file_id a7e7dd02-fd28-4a8e-8fae-eb495db0bd86.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../data/output/a7e7dd02-fd28-4a8e-8fae-eb495db0bd86.npy"
      ]
    }

