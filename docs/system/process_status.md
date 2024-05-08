## The `process_status` method

The `process_status` method is available on every krixik pipeline, and is invoked whenever you want to check the status of files being processed through your defined pipeline.

This method is especially useful when using [`process`](../system/process.md) with `wait_for_process` set to `False`.

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

    SUCCESS: You are now authenticated.


## Basic pipeline setup

For this document we will use a pipeline consisting of a single [`parser` module](../modules/parser.md).  We use [`create_pipeline`](../system/create_save_load.md) to instantiate the pipeline.


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(name="system-process-status-docs", module_chain=["parser"])
```


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```

## Basic usage, required input, and output breakdown

To illustrate the usage of `process_status` we process a short file illustrated in the introduction to the [`parser` method](../modules/parser.md).


```python
# define path to an input file from examples directory
test_file = "../../data/input/1984_very_short.txt"

# process short input file
process_output = pipeline.process(
    local_file_path=test_file,
    local_save_directory="../../data/output",  # save output repo data output subdir
    expire_time=60 * 10,  # set all process data to expire in 10 minutes
    wait_for_process=False,  # wait for process to complete before regaining ide
    verbose=False,
)  # set verbosity to False
```

Let us examine the returned output.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```




    '{\n  "file_id": "3d435c55-05ae-41b6-aee3-76da8c7b0841",\n  "request_id": "5e723bee-4939-21f1-52ef-ca0596dd3f1f",\n  "file_name": "krixik_generated_file_name_vplttsahnp.txt",\n  "symbolic_directory_path": "/etc",\n  "file_tags": null,\n  "file_description": null\n}'



We can check the status of our process using returned `request_id` and the `process_status` as shown below.  `process_status` takes in a single required input: `request_id`.


```python
# use .process_status
status_output = pipeline.process_status(request_id=process_output["request_id"])

# nicely print the output of this process
print(json.dumps(status_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "d248636b-5ea5-4da7-a250-9e00332cd2b8",
      "file_id": "3d435c55-05ae-41b6-aee3-76da8c7b0841",
      "message": "SUCCESS: process_status found",
      "pipeline": "process-status-doc",
      "process_status": {
        "parser": false
      },
      "overall_status": "ongoing"
    }


Here we can see that the status of our single module has not yet completed.

If we wait a few moments and try again, we will see confirmation that the process completed successfully.


```python
# use .process_status
status_output = pipeline.process_status(request_id=process_output["request_id"])

# nicely print the output of this process
print(json.dumps(status_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "cf1c55e3-34c8-4c81-a940-b264c7c0448d",
      "file_id": "3d435c55-05ae-41b6-aee3-76da8c7b0841",
      "message": "SUCCESS: process_status found",
      "pipeline": "process-status-doc",
      "process_status": {
        "parser": true
      },
      "overall_status": "complete"
    }



```python
# delete all processed datapoints belonging to this pipeline
import time

time.sleep(10)
reset_pipeline(pipeline)
```
