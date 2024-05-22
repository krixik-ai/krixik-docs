## The `.delete` Method

You can delete all records of a processed file from the Krixik system with the `.delete` method. This is the manual version of letting the [`expire_time`](../parameters_processing_files_through_pipelines/process_method.md#core-.process-method-arguments) run out on a file.

This overview of the `.delete` method is divided into the following sections:

- [`.delete` Method Arguments](#.delete-method-arguments)
- [`.delete` Method Example](#.delete-method-example)


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


### `.delete` Method Arguments

The `.delete` method takes a single (required) argument:

- `file_id` (str) - The `file_id` of the processed file whose record you wish to entirely delete from Krixik servers.

### `.delete` Method Example

For this document's example we will use a pipeline consisting of a single [`parser`](../../modules/ai_model_modules/parser_module.md) module.  We use the [`.create_pipeline`](../pipeline_creation/create_pipeline.md) method to instantiate the pipeline, and then [`.process`](../parameters_processing_files_through_pipelines/process_method.md) two files through it into the same `symbolic_directory_path` (to make the demonstration clearer):


```python
# create an example pipeline with a single module

pipeline_1 = krixik.create_pipeline(name="delete_method_1_parser",
                                    module_chain=["parser"])

# process short input file
process_output_1 = pipeline_1.process(local_file_path="../../../data/input/Frankenstein.txt", # the initial local filepath where the input JSON file is stored
                                      expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                      verbose=False,  # do not display process update printouts upon running code
                                      symbolic_directory_path="/novels/19th-century",
                                      file_name="Frankenstein.txt",
                                      file_tags=[{"author": "Shelley"}, {"category": "gothic"}, {"century": "19"}])

process_output_2 = pipeline_1.process(local_file_path="../../../data/input/Moby Dick.txt", # the initial local filepath where the input JSON file is stored
                                      expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                      verbose=False,  # do not display process update printouts upon running code
                                      symbolic_directory_path="/novels/19th-century",
                                      file_name="Moby Dick.txt",
                                      file_tags=[{"author": "Melville"}, {"category": "adventure"}, {"century": "19"}])
```

    INFO: output json downloaded but larger than 0.5MB and will not be returned with .process output
    INFO: output json downloaded but larger than 0.5MB and will not be returned with .process output


Let's see what the files' records look like with the [`.list`](list_method.md) method:


```python
# see both files' records with .list (they're in the same symbolic_directory_path)

list_output_1 = pipeline_1.list(symbolic_directory_paths=["/novels/19th-century"])

# nicely print the output of this .list

print(json.dumps(list_output_1, indent=2))
```

    {
      "status_code": 200,
      "request_id": "1496a1a2-1bd6-4ae0-a54d-743fcefc846d",
      "message": "Successfully returned 2 items.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-05-20 02:56:41",
          "process_id": "602f1b2a-2267-0af0-e278-3d5ae10e571d",
          "created_at": "2024-05-20 02:56:41",
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
                  "num_lines": 9184
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "melville"
            },
            {
              "category": "adventure"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/19th-century",
          "pipeline": "delete_method_1_parser",
          "file_id": "adf1d212-eb1c-460c-b526-4eeb09450962",
          "expire_time": "2024-05-20 03:26:40",
          "file_name": "moby dick.txt"
        },
        {
          "last_updated": "2024-05-20 02:56:26",
          "process_id": "aa4a086a-0839-63d9-dc9b-75e4f30fe911",
          "created_at": "2024-05-20 02:56:26",
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
                  "num_lines": 3199
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "shelley"
            },
            {
              "category": "gothic"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/19th-century",
          "pipeline": "delete_method_1_parser",
          "file_id": "e1c9b5c4-132d-4922-a05e-3eeaeda87e47",
          "expire_time": "2024-05-20 03:26:25",
          "file_name": "frankenstein.txt"
        }
      ]
    }


Both files' records are properly showing up.

Now use the `.delete` method and one of the files' `file_id`s to delete that file:


```python
# delete processed file's record and output with its file_id

delete_output_1 = pipeline_1.delete(file_id="e1c9b5c4-132d-4922-a05e-3eeaeda87e47")

# nicely print the output of this deletion

print(json.dumps(delete_output_1, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "delete_method_1_parser",
      "request_id": "341c883f-6433-4674-ab22-c0361cf7eb63",
      "message": "Successfully deleted file_id: e1c9b5c4-132d-4922-a05e-3eeaeda87e47",
      "warnings": []
    }


We can check that the file has been deleted by using the [`.list`](list_method.md) method on the same `symbolic_directory_path`:


```python
# .list to confirm that one file has been deleted

list_output_2 = pipeline_1.list(symbolic_directory_paths=["/novels/19th-century"])

# nicely print the output of this .list

print(json.dumps(list_output_2, indent=2))
```

    {
      "status_code": 200,
      "request_id": "3216abaa-5262-450b-920b-7d23624eddcb",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-05-20 02:56:41",
          "process_id": "602f1b2a-2267-0af0-e278-3d5ae10e571d",
          "created_at": "2024-05-20 02:56:41",
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
                  "num_lines": 9184
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "melville"
            },
            {
              "category": "adventure"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/19th-century",
          "pipeline": "delete_method_1_parser",
          "file_id": "adf1d212-eb1c-460c-b526-4eeb09450962",
          "expire_time": "2024-05-20 03:26:40",
          "file_name": "moby dick.txt"
        }
      ]
    }


As expected, only one of the two previously [processed](../parameters_processing_files_through_pipelines/process_method.md) files shows up; the other has been deleted.


```python
# delete all processed datapoints belonging to this pipeline

reset_pipeline(pipeline_1)
```
