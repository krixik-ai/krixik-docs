## The `fetch_output` method

The `fetch_output` method is used to download the output of a pipeline process.  This is particularly useful when using [`process`](../system/process.md) with `wait_for_process` set to `False`, as your output is not immediately yielded by [`process`](../system/process.md).

A table of contents for the remainder of this document is shown below.

- [basic pipeline setup](#basic-pipeline-setup)
- [basic usage, required input, and output breakdown](#basic-usage,-required-input,-and-output-breakdown)


```python
# import utilities
import sys
import json
import importlib

sys.path.append("../../")
reset = importlib.import_module("utilities.reset")
reset_pipeline = reset.reset_pipeline

# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os

load_dotenv("../../.env")
MY_API_KEY = os.getenv("MY_API_KEY")
MY_API_URL = os.getenv("MY_API_URL")

# import krixik and initialize it with your personal secrets
from krixik import krixik

krixik.init(api_key=MY_API_KEY, api_url=MY_API_URL)
```

## Basic pipeline setup

For this document we will use a pipeline consisting of a single [`parser` module](../modules/parser.md).  We use [`create_pipeline`](../system/create_save_load.md) to instantiate the pipeline.


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(name="fetch-output-docs", module_chain=["parser"])
```

## Basic usage, required input, and output breakdown

To illustrate the usage of `fetch_output` we process a short file illustrated in the introduction to the [`parser` method](../modules/parser.md).


```python
# define path to an input file from examples directory
test_file = "../../data/input/1984_very_short.txt"

# process for search
process_output = pipeline.process(
    local_file_path=test_file,
    local_save_directory="../../data/output",  # save output repo data output subdir
    expire_time=60 * 10,  # set all process data to expire in 10 minutes
    wait_for_process=True,  # wait for process to complete before regaining ide
    verbose=False,
)  # set verbosity to False
```

Let us examine the returned output.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```


    '{\n  "file_id": "3d435c55-05ae-41b6-aee3-76da8c7b0841",\n  "request_id": "5e723bee-4939-21f1-52ef-ca0596dd3f1f",\n  "file_name": "krixik_generated_file_name_vplttsahnp.txt",\n  "symbolic_directory_path": "/etc",\n  "file_tags": null,\n  "file_description": null\n}'


Since the file has completed processing we can now use `fetch_output`.

`fetch_output` takes in a two inputs

 - the `file_id` of the uploaded and processed file
 - a `local_save_directory` (optional) where the completed files will be saved locally (default is current working directory)


```python
# fetch the output of our process using file_id
fetch_output = pipeline.fetch_output(file_id=process_output["file_id"], local_save_directory="../../data/output")
```

Printing the fetched output return we have our json returned in the `fetch_output` key-value.  

The `process_output_files` key-value pair shows the download location(s) of our completed process files pulled by `.fetch_output`.


```python
# nicely print the output of this process
print(json.dumps(fetch_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "parser-pipeline-1",
      "request_id": "66cacfdf-f4a8-4061-9322-50489d5d9670",
      "file_id": "1488dd6d-4bc5-4d61-b7d5-ff5262fce5f1",
      "message": "SUCCESS - output fetched for file_id 1488dd6d-4bc5-4d61-b7d5-ff5262fce5f1.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
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
      ],
      "process_output_files": [
        "./1488dd6d-4bc5-4d61-b7d5-ff5262fce5f1.json"
      ]
    }



```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
