## The `json-to-txt` module

This document reviews the `json-to-txt` module - which takes as input a json of string snippets, joins them into a single string separated by double spaces, and returns a text file document.

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [required input format](#required-input-format)
- [using the default model](#using-the-default-model)

## Pipeline setup

Below we setup a simple one module pipeline using the `json-to-txt` module.

We do this by passing the module name to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(
    name="modules-json-to-txt-docs", module_chain=["json-to-txt"]
)
```

The `json-to-txt` module comes with a single model:

- `base`: (default) joins a json of text snippets into a single text separated by double spaces

These available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).

## Required input format

The `json-to-txt` module accepts as input `.json` files consisting of a *list of dictionaries*.  Each dictionary may have as many key-value pairs as desired, but *must* contain the key name *snippet*.  This is the key `json-to-txt` will act on.

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


This input file is a `.json` consisting of a *list of dictionaries*.  Each dictionary contains a key called *snippet* that will be acted on by the module.  All other key-value pairs are ignored.

## Using the default model

Let's process our test input file using the `default` model - `base`.  Because this is the default model we need not input the optional `modules` argument into `.process`.


```python
# define path to an input file from examples directory
test_file = "../../data/input/1984_very_short.json"

# process for search
process_output = pipeline.process(
    local_file_path=test_file,
    local_save_directory="../../data/output",  # save output repo data output subdir
    expire_time=60 * 10,  # set all process data to expire in 10 minutes
    wait_for_process=True,  # wait for process to complete before regaining ide
    verbose=False,
)  # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is text, the process output is provided in this object is null.  However the file itself has been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "my-json-to-txt-pipeline",
      "request_id": "0ea5e2ce-1f60-4673-8616-cbda38487f3c",
      "file_id": "ffa44327-a8ee-41df-bf04-c25c92ff7f8e",
      "message": "SUCCESS - output fetched for file_id ffa44327-a8ee-41df-bf04-c25c92ff7f8e.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../data/output/ffa44327-a8ee-41df-bf04-c25c92ff7f8e.txt"
      ]
    }


We load in the text file output from `process_output_files` below. 


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


Here we see that the module has merged the two *snippet* values from the input dictionaries.
