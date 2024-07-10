<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/single_module_pipelines/single_text-embedder.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Single-Module Pipeline: `text-embedder`

This document is a walkthrough of how to assemble and use a single-module pipeline that only includes a [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) module. It's divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Required Input Format](#required-input-format)
- [Using the Default Model](#using-the-default-model)
- [Examining Process Output Locally](#examining-process-output-locally)
- [Using a Non-Default Model](#using-a-non-default-model)

### Pipeline Setup

Let's first instantiate a single-module [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) pipeline.

We use the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method for this, passing only the [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) module name into `module_chain`.


```python
# create a pipeline with a single text-embedder module
pipeline = krixik.create_pipeline(name="single_text-embedder-1", module_chain=["text-embedder"])
```

### Required Input Format

The [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) module accepts JSON file input. The input JSON must respect [this format](../../system/parameters_processing_files_through_pipelines/JSON_input_format.md).

The JSON file may optionally also include, along with each snippet, a key-value pair in which the key is the string `"line numbers"` and the value is an integer list of every line number of the original document that the snippet is on. This will make it easier for you to identify what document line each vector is an embedding of.

Let's take a quick look at a valid input file, and then process it.


```python
# examine contents of a valid input file
with open(data_dir + "input/1984_snippets.json", "r") as file:
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

Let's process our test input file using the [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) module's [default model](../../modules/ai_modules/text-embedder_module.md#available-models-in-the-text-embedder-module): [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).

Given that this is the default model, we need not specify model selection through the optional [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

In a later section of this document we will process the same file again, but select our model and the quantization thereof explicitly.


```python
# process the file with the default model
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_snippets.json",  # the initial local filepath where the input file is stored
    local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # wait for process to complete before returning IDE control to user
    verbose=False,
)  # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Moreover, the output file itself has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_text-embedder-1",
      "request_id": "ce2e57ce-c2be-49ac-8d43-59e6db2bcf25",
      "file_id": "ce4ddfa5-12c6-4dcb-86af-4f6d30ed6188",
      "message": "SUCCESS - output fetched for file_id ce4ddfa5-12c6-4dcb-86af-4f6d30ed6188.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/ce4ddfa5-12c6-4dcb-86af-4f6d30ed6188.npy"
      ]
    }


### Examining Process Output Locally

The outputted NPY file containing embedding vectors of our input data can be examined as follows. For the sake of clarity, in this example we will simply print the shape, and not any of the contents, of the returned array:


```python
# examine vector output
import numpy as np

vectors = np.load(process_output["process_output_files"][0])
print(vectors.shape)
```

    (2, 384)


In other words, the array has 2 rows with 384 values in each row. 

In the context of the input file, the first row is the vectorized form of our first snippet: "It was a bright cold day in April, and the clocks were striking thirteen."

### Using a Non-Default Model

To use a [non-default model](../../modules/ai_modules/text-embedder_module.md#available-models-in-the-text-embedder-module) like [`all-mpnet-base-v2`](https://huggingface.co/sentence-transformers/all-mpnet-base-v2), we must enter it explicitly through the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument when invoking the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method. As [module documentation](../../modules/ai_modules/text-embedder_module.md) indicates, you can also specify whether or not you wish to use the quantized version of the model.


```python
# process the file with a non-default model
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_snippets.json",  # all parameters save 'modules' as above
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,
    wait_for_process=True,
    verbose=False,
    modules={"text-embedder": {"model": "all-mpnet-base-v2", "params": {"quantize": False}}},
)  # specify a non-default model for this process
```

Now we can examine the output as we did above.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_text-embedder-1",
      "request_id": "f53c93da-cf1b-41e0-a578-16dc62736ed4",
      "file_id": "1dcbde04-d4f2-414f-acaf-577c355bbb88",
      "message": "SUCCESS - output fetched for file_id 1dcbde04-d4f2-414f-acaf-577c355bbb88.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/1dcbde04-d4f2-414f-acaf-577c355bbb88.npy"
      ]
    }

