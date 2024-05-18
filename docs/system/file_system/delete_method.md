## The `.delete` Method

You can delete all records of a processed file from the Krixik system with the `.delete` method. This is the manual version of letting the [`expire_time`](../system/parameters_processing_files_through_pipelines/process_method.md#core-process-method-arguments) run out on a file.

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
process_output_1 = pipeline_1.process(local_file_path="../../data/input/Frankenstein.txt", # the initial local filepath where the input JSON file is stored
                                      expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                      verbose=False,  # do not display process update printouts upon running code
                                      symbolic_directory_path="/novels/19th-century",
                                      file_name="Frankenstein.txt",
                                      file_tags=[{"author": "Shelley"}, {"category": "gothic"}, {"century": 19}])

process_output_2 = pipeline_1.process(local_file_path="../../data/input/Moby Dick.txt", # the initial local filepath where the input JSON file is stored
                                      expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                      verbose=False,  # do not display process update printouts upon running code
                                      symbolic_directory_path="/novels/19th-century",
                                      file_name="Moby Dick.txt",
                                      file_tags=[{"author": "Melville"}, {"category": "adventure"}, {"century": 19}])
```

Let's see what the files' records look like with the [`.list`](../file_system/list_method.md) method:


```python
# see both files' records with .list (they're in the same symbolic_directory_path)

list_output_1 = pipeline_1.list(symbolic_directory_paths=["/novels/19th-century"])

# nicely print the output of this .list

print(json.dumps(list_output_1, indent=2))
```

Both files' records are properly showing up.

Now use the `.delete` method and one of the files' `file_id`s to delete that file:


```python
# delete processed file's record and output with its file_id

delete_output_1 = pipeline_1.delete(file_id="XXX")

# nicely print the output of this deletion

print(json.dumps(delete_output_1, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "parser-pipeline-1",
      "request_id": "693d3da8-1e0d-4f24-b85a-2c8287320b51",
      "message": "Successfully deleted file_id: ddb925f3-8cfb-4fdc-bd10-dbb68adecb04",
      "warnings": []
    }


We can check that the file has been deleted by using the [`.list`](../file_system/list_method.md) method on the same `symbolic_directory_path`:


```python
# .list to confirm that one file has been deleted

list_output_2 = pipeline_1.list(symbolic_directory_paths=["/novels/19th-century"])

# nicely print the output of this .list

print(json.dumps(list_output_2, indent=2))
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

