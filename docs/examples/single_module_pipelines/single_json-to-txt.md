<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/single_module_pipelines/single_json-to-txt.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Single-Module Pipeline: `json-to-txt`

This document is a walkthrough of how to assemble and use a single-module pipeline that only includes a [`json-to-txt`](../../modules/support_function_modules/json-to-txt_module.md) module. It's divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Required Input Format](#required-input-format)
- [Using the Default Model](#using-the-default-model)

### Pipeline Setup

Let's first instantiate a single-module [`json-to-txt`](../../modules/support_function_modules/json-to-txt_module.md) pipeline.

We use the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method for this, passing only the [`json-to-txt`](../../modules/support_function_modules/json-to-txt_module.md) module name into `module_chain`.


```python
# create a pipeline with a single json-to-txtmodule
pipeline = krixik.create_pipeline(name="single_json-to-txt_1", module_chain=["json-to-txt"])
```

### Required Input Format

The [`json-to-txt`](../../modules/support_function_modules/json-to-txt_module.md) module accepts JSON file input. The input JSON must respect [this format](../../system/parameters_processing_files_through_pipelines/JSON_input_format.md).

Let's take a quick look at a valid input file, and then process it.


```python
# examine the contents of a valid input file
test_file = data_dir + "input/1984_snippets.json"
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


### Using the Default Model

Let's process our test input file using the [`json-to-txt`](../../modules/support_function_modules/json-to-txt_module.md) module's default (and currently only) [model](../../modules/support_function_modules/json-to-txt_module.md#available-models-in-the-json-to-txt-module), `base`.

Given that this is the default model, we need not specify model selection through the optional [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


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

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

The output file itself has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_json-to-txt_1",
      "request_id": "1a1bec21-0b49-40fc-b548-87c354d8c478",
      "file_id": "67b7c6cf-829b-4afa-99ff-3c1387b3db02",
      "message": "SUCCESS - output fetched for file_id 67b7c6cf-829b-4afa-99ff-3c1387b3db02.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data//output/67b7c6cf-829b-4afa-99ff-3c1387b3db02.txt"
      ]
    }


To confirm that everything went as it should have, let's load in the text file output from `process_output_files`:


```python
# load in process output from file
import json

with open(process_output["process_output_files"][0], "r") as file:
    print(file.read())
```

    It was a bright cold day in April, and the clocks were striking thirteen.
    Winston Smith, his chin nuzzled into his breast in an effort to escape the
    vile wind, slipped quickly through the glass doors of Victory Mansions,
    though not quickly enough to prevent a swirl of gritty dust from entering
    along with him.


You can confirm that the module has merged the two snippet values from the input dictionaries into a single string.
