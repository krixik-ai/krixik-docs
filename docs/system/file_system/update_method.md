## The `.update` Method

You can update any metadata of any processed file by using the `.update` method.

This overview of the `.update` method is divided into the following sections:

- [.update Method Arguments](#update-method-arguments)
- [.update Method Example](#update-method-example)
- [Observations on the .update Method](#observations-on-the-update-method)


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


### `.update` Method Arguments

The `.update` method takes one required argument and at least one of several optional arguments:

- `file_id` (required, str) - The `file_id` of the file whose metadata you wish to update.

- `expire_time` (optional, int) - The amount of time (in seconds) that file data will remain on Krixik servers, counting as of when the `.update` method is run.

- `symbolic_directory_path` (optional, str) - A UNIX-formatted directory path under your account in the Krixik system.

- `file_name` (optional, str) - A custom file name that must end with the file extension of the original input file. **You cannot update the file extension.**

- `symbolic_file_path` (optional, str) - A combination of `symbolic_directory_path` and `file_name` in a single argument.

- `file_tags` (optional, list) - A list of custom file tags (each a key-value pair). Note that you must update the whole set, so if a file has three file tags and you update one of them, entirely excluding the other two from the `.update` method `file_tags` argument, both of those will be deleted.

- `file_description` (optional, str) - A custom file description.

If none of the optional arguments are present, the `.update` method will not work because there will be nothing to update.

### `.update` Method Example

For this document's example we will use a pipeline consisting of a single [`parser`](../../modules/ai_model_modules/parser_module.md) module.  We use the [`.create_pipeline`](../pipeline_creation/create_pipeline.md) method to instantiate the pipeline, and then process a file through it:


```python
# create an example pipeline with a single parser module

pipeline_1 = krixik.create_pipeline(name="update_method_1_parser",
                                    module_chain=["parser"])

# process short input file

process_output_1 = pipeline_1.process(local_file_path="../../../data/input/Frankenstein.txt", # the initial local filepath where the input JSON file is stored
                                      expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                      verbose=False,  # do not display process update printouts upon running code
                                      symbolic_directory_path="/novels/gothic",
                                      file_name="The Franken Stein.txt",
                                      file_tags=[{"author": "Shelley"}, {"category": "gothic"}, {"century": "19"}])
```

    INFO: output json downloaded but larger than 0.5MB and will not be returned with .process output


Let's see what the file's record looks like with the [`.list`](list_method.md) method:


```python
# see the file's record with .list

list_output_1 = pipeline_1.list(symbolic_directory_paths=['/novels/gothic'])

# nicely print the output of this .list

print(json.dumps(list_output_1, indent=2))
```

    {
      "status_code": 200,
      "request_id": "abaa977d-e56b-41b9-9c49-f2809f987a2d",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-05-20 17:49:30",
          "process_id": "b107e0e0-74da-a983-d1d2-56cd9bbe33d7",
          "created_at": "2024-05-20 17:49:30",
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
          "symbolic_directory_path": "/novels/gothic",
          "pipeline": "update_method_1_parser",
          "file_id": "463a697d-a8b5-4674-ace8-79fe53b862a1",
          "expire_time": "2024-05-20 18:19:30",
          "file_name": "the franken stein.txt"
        }
      ]
    }


We can use the `.update` method to update the file's metadata.

We'll update its `file_name`, since it's erroneous, change the `{"category": "gothic"}` file tag for something different, and add a `file_description`. We'll leave its `symbolic_directory_path` untouched.


```python
# update metadata the metadata for the processed file

update_output_1 = pipeline_1.update(file_id="463a697d-a8b5-4674-ace8-79fe53b862a1",
                                    file_name="Frankenstein.txt",
                                    file_tags=[{"author": "Shelley"}, {"country": "UK"}, {"century": "19"}],
                                    file_description='Is the villain the monster or the doctor?')

# nicely print the output of this .update

print(json.dumps(process_output_1, indent=2))
```

    INFO: lower casing file_name Frankenstein.txt to frankenstein.txt
    INFO: lower casing file tag {'author': 'Shelley'} to {'author': 'shelley'}
    INFO: lower casing file tag {'country': 'UK'} to {'country': 'uk'}
    {
      "status_code": 200,
      "pipeline": "update_method_1_parser",
      "request_id": "090cb419-2e92-4dff-b82f-d14d562f45d5",
      "file_id": "463a697d-a8b5-4674-ace8-79fe53b862a1",
      "message": "SUCCESS - output fetched for file_id 463a697d-a8b5-4674-ace8-79fe53b862a1.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "c:\\Users\\Lucas\\Desktop\\krixikdocsnoodle\\docs\\system\\file_system/463a697d-a8b5-4674-ace8-79fe53b862a1.json"
      ]
    }


Now we invoke the [`.list`](list_method.md) method to confirm that all metadata has indeed been updated as requested:


```python
# call .list to see the file's newly updated record

list_output_2 = pipeline_1.list(symbolic_file_paths=['/novels/gothic/Frankenstein.txt'])

# nicely print the output of this .list

print(json.dumps(list_output_2, indent=2))
```

    {
      "status_code": 200,
      "request_id": "8bbcc518-4204-439e-9173-7f659f1b96e5",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-05-20 17:51:00",
          "process_id": "b107e0e0-74da-a983-d1d2-56cd9bbe33d7",
          "created_at": "2024-05-20 17:49:30",
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
              "country": "uk"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "Is the villain the monster or the doctor?",
          "symbolic_directory_path": "/novels/gothic",
          "pipeline": "update_method_1_parser",
          "file_id": "463a697d-a8b5-4674-ace8-79fe53b862a1",
          "expire_time": "2024-05-20 18:19:30",
          "file_name": "frankenstein.txt"
        }
      ]
    }


### Observations on the `.update` Method

Four closing observation on the `.update` method:

- Note that in the example above we updated `file_tags` by including the entire set of file tags: `[{"author": "Shelley"}, {"country": "UK"}, {"century": 19}]`. If we'd only used `[{"country": "UK"}]`, the "author" and "century" ones would have been deleted.

- You cannot update a `symbolic_directory_path`/`file_name` combination (a.k.a. a `symbolic_file_path`) so it's identical to that of another file. Krixik will not allow it.

- You can also not update a file's file extension. For instance, a `.txt` file cannot become a `.pdf` file through the `.update` method.

- The `.update` method allows you to extend a file's [`expire_time`](../parameters_processing_files_through_pipelines/process_method.md#core-process-method-arguments) indefinitely. Upon initially uploading a file, its [`expire_time`](../parameters_processing_files_through_pipelines/process_method.md#core-process-method-arguments) cannot be greater than 2,592,000 seconds (30 days). However, if you periodically invoke `.update` on its file and reset its [`expire_time`](../parameters_processing_files_through_pipelines/process_method.md#core-process-method-arguments) to another 2,592,000 seconds (or however many seconds you please), the file will remain on-system for that much more time as of that moment, and so forth.


```python
# delete all processed datapoints belonging to this pipeline

reset_pipeline(pipeline_1)
```
