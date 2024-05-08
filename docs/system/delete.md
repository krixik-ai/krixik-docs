## The `delete` method

You can delete the record of your process on demand using the `delete` method.  This will remove all record of the process from our servers.  This is the manual version of letting the `expire_time` run out on a file.

The `delete` method takes in a single argument: the `file_id` of the file you wish to delete.

We will illustrate its usage by processing a simple file, deleting it using the `delete` method, and then checking that it no longer exists using the [`list` method](../system/list.md).

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
pipeline = krixik.create_pipeline(name="system-delete-docs", module_chain=["parser"])
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


Now we delete this process record and its output via its `file_id`.


```python
# delete process record and output by file_id
delete_output = pipeline.delete(file_id=process_output["file_id"])

# nicely print the output of this process
print(json.dumps(delete_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "parser-pipeline-1",
      "request_id": "693d3da8-1e0d-4f24-b85a-2c8287320b51",
      "message": "Successfully deleted file_id: ddb925f3-8cfb-4fdc-bd10-dbb68adecb04",
      "warnings": []
    }


Now we can check that the file has been deleted using `.list`.


```python
# list process records
list_output = pipeline.list(file_ids=[process_output["file_id"]])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "b4f69db4-fece-4b3d-8184-420ebfd912d2",
      "message": "No items found for input query arguments",
      "warnings": [
        {
          "WARNING: the following file_ids were not found": [
            "ddb925f3-8cfb-4fdc-bd10-dbb68adecb04"
          ]
        }
      ],
      "items": []
    }



```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
