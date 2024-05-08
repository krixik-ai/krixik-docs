## the `.update` method

You can update the metadata of a file using the `update` method.  This method takes in the `file_id` of the file you would like to update, and the metadata you would like to update.  

You can update any of the following metadata: `expire_time`,  `symbolic_directory_path`, `file_name`, `file_tags`, or `file_description` of the associated file using this method.

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
pipeline = krixik.create_pipeline(name="system-update-docs", module_chain=["parser"])
```


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```

## Basic usage, required input, and output breakdown

To illustrate the usage of `update` we process a short file illustrated in the introduction to the [`parser` method](../modules/parser.md).


```python
# define path to an input file from examples directory
test_file = "../../data/input/1984_very_short.txt"

# process short input file
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


Next we use `update` to change its `file_name`.


```python
# update a process record metadata
update_output = pipeline.update(file_id=process_output["file_id"], file_name="a_new_filename.txt")

# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "parser-pipeline-1",
      "request_id": "4201b289-9088-42e3-a0ec-8053b9190ba3",
      "message": "Successfully updated file metadata",
      "warnings": []
    }


Now if we use [`list`](system/list.md) we can check that our record metadata has been changed.


```python
# list process records
list_output = pipeline.list(file_ids=[process_output["file_id"]])

# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "53c2fc7b-8b84-4128-a34e-1e4de4ceff94",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-04-26 21:06:32",
          "process_id": "461bfe88-0064-13b1-2728-7f5a371092cf",
          "created_at": "2024-04-26 21:05:42",
          "file_metadata": {
            "modules": {
              "parser": {
                "model": "sentence"
              }
            },
            "modules_data": {
              "parser": {
                "data_files_extensions": [
                  ".json"
                ]
              }
            }
          },
          "file_tags": [
            {
              "author": "orwell"
            },
            {
              "category": "fiction"
            }
          ],
          "file_description": "the first paragraph of 1984",
          "symbolic_directory_path": "/my/custom/filepath",
          "pipeline": "parser-pipeline-1",
          "file_id": "ca3ca26c-7b76-4fd2-a1f1-3c86d8eb443a",
          "expire_time": "2024-04-26 21:10:42",
          "file_name": "a_new_filename.txt"
        }
      ]
    }



```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
