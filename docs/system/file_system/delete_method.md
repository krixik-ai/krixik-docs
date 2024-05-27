## The `delete` Method

You can delete all records of a processed file from the Krixik system with the `delete` method. This is the manual version of letting the [`expire_time`](../parameters_processing_files_through_pipelines/process_method.md#core-process-method-arguments) run out on a file.

This overview of the `delete` method is divided into the following sections:

- [`delete` Method Arguments](#delete-method-arguments)
- [`delete` Method Example](#delete-method-example)


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


### `delete` Method Arguments

The `delete` method takes a single (required) argument:

- `file_id` (str) - The `file_id` of the processed file whose record you wish to entirely delete from Krixik servers.

### `delete` Method Example

For this document's example we will use a pipeline consisting of a single [`parser`](../../modules/support_function_modules/parser_module.md) module.  We use the [`create_pipeline`](../pipeline_creation/create_pipeline.md) method to instantiate the pipeline, and then [`process`](../parameters_processing_files_through_pipelines/process_method.md) a file through it.


```python
# create an example pipeline with a single module
pipeline = krixik.create_pipeline(name="delete_method_1_parser",
                                  module_chain=["parser"])

# process short input file
process_output = pipeline.process(local_file_path="../../../data/input/1984_very_short.txt", # the initial local filepath where the input JSON file is stored
                                  local_save_directory="../../../data/output",  # the local directory that the output file will be saved to
                                  expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                  wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                  verbose=False,  # do not display process update printouts upon running code
                                  symbolic_directory_path="/novels/20th-century",
                                  file_name="1984_sample.txt",
                                  file_tags=[{"author": "Orwell"}, {"category": "dystopian"}, {"century": "20"}])
```

Let's see what the files' records look like with the [`list`](list_method.md) method:


```python
# see both files' records with list (they're in the same symbolic_directory_path)
list_output = pipeline.list(symbolic_directory_paths=["/novels/20th-century"])

# nicely print the output of this list
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "258e552d-1cee-4eed-915d-79687f58673c",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-05-22 19:40:11",
          "process_id": "b277c633-06c1-c66b-f450-22387f503375",
          "created_at": "2024-05-22 19:40:11",
          "file_metadata": {
            "modules": {
              "module_1": {
                "parser": {
                  "model": "sentence"
                }
              }
            },
            "modules_data": {
              "module_1": {
                "parser": {
                  "data_files_extensions": [
                    ".json"
                  ],
                  "num_lines": 2
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "orwell"
            },
            {
              "category": "dystopian"
            },
            {
              "century": "20"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/20th-century",
          "pipeline": "delete_method_1_parser",
          "file_id": "c0664f56-41f7-41d8-81a3-e4150f0df100",
          "expire_time": "2024-05-22 20:10:10",
          "file_name": "1984_sample.txt"
        }
      ]
    }


Both files' records are properly showing up.

Now use the `delete` method and one of the files' `file_id`s to delete that file:


```python
# delete processed file's record and output with its file_id
delete_output = pipeline.delete(file_id=process_output["file_id"])

# nicely print the output of this deletion
print(json.dumps(delete_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "delete_method_1_parser",
      "request_id": "8c670f7f-91f0-46f8-9c40-b34b9d917662",
      "message": "Successfully deleted file_id: c0664f56-41f7-41d8-81a3-e4150f0df100",
      "warnings": []
    }


We can check that the file has been deleted by using the [`list`](list_method.md) method on the same `symbolic_directory_path`:


```python
#  to confirm that one file has been deleted
list_output = pipeline.list(symbolic_directory_paths=["/novels/20th-century"])

# nicely print the output of this 
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "97c9a982-3df2-44af-9fd8-bf2b79e7f535",
      "message": "No files were found for the given query arguments",
      "warnings": [
        {
          "WARNING: the following arguments returned zero results": [
            {
              "symbolic_directory_paths": [
                "/novels/20th-century"
              ]
            }
          ]
        }
      ],
      "items": []
    }


As expected, only one of the two previously [processed](../parameters_processing_files_through_pipelines/process_method.md) files shows up; the other has been deleted.


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
