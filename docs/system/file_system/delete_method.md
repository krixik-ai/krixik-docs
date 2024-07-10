<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/file_system/delete_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## The `delete` Method

You can delete all records of a processed file from the Krixik system with the `delete` method. This is the manual version of letting the [`expire_time`](../parameters_processing_files_through_pipelines/process_method.md#core-process-method-arguments) run out on a file.

This overview of the `delete` method is divided into the following sections:

- [`delete` Method Arguments](#delete-method-arguments)
- [`delete` Method Example](#delete-method-example)

### `delete` Method Arguments

The `delete` method takes a single (required) argument:

- `file_id` (str) - The `file_id` of the processed file whose record you wish to entirely delete from Krixik servers.

### `delete` Method Example

For this document's example we will use a pipeline consisting of a single [`parser`](../../modules/support_function_modules/parser_module.md) module.  We use the [`create_pipeline`](../pipeline_creation/create_pipeline.md) method to instantiate the pipeline, and then [`process`](../parameters_processing_files_through_pipelines/process_method.md) a file through it.


```python
# create an example pipeline with a single module
pipeline = krixik.create_pipeline(name="delete_method_1_parser", module_chain=["parser"])

# process short input file
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_very_short.txt",  # the initial local filepath where the input JSON file is stored
    local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
    verbose=False,  # do not display process update printouts upon running code
    symbolic_directory_path="/novels/20th-century",
    file_name="1984_sample.txt",
    file_tags=[{"author": "Orwell"}, {"category": "dystopian"}, {"century": "20"}],
)
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
      "request_id": "46faf749-b758-42d7-8b82-f1f8e8dcb54d",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:31:35",
          "process_id": "0db7cc1d-06c9-13e3-483d-82255c145dd2",
          "created_at": "2024-06-05 15:31:35",
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
          "file_id": "ad927578-a8f1-4ace-acbc-3dee2391075c",
          "expire_time": "2024-06-05 16:01:35",
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
      "request_id": "6e59e916-4233-4088-b85c-2dbe96425383",
      "message": "Successfully deleted file_id: ad927578-a8f1-4ace-acbc-3dee2391075c",
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
      "request_id": "542fe670-ce77-4d33-b1ab-a6024c7360be",
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
