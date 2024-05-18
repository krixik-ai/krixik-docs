## The `.update` Method

You can update any metadata of any processed file by using the `.update` method.

This overview of the `.update` method is divided into the following sections:

- [.update Method Arguments](#.update-method-arguments)
- [.update Method Example](#.update-method-example)
- [Observations on the .update Method](#observations-on-the-.update-Method)

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

process_output_1 = pipeline_1.process(local_file_path="../../data/input/Frankenstein.txt", # the initial local filepath where the input JSON file is stored
                                      expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                      verbose=False,  # do not display process update printouts upon running code
                                      symbolic_directory_path="/novels/gothic",
                                      file_name="The Franken Stein.txt",
                                      file_tags=[{"author": "Shelley"}, {"category": "gothic"}, {"century": 19}])
```

Let's see what the file's record looks like with the [`.list`](../file_system/list_method.md) method:


```python
# see the file's record with .list

list_output_1 = pipeline_1.list(symbolic_directory_paths=['/novels/gothic'])

# nicely print the output of this .list

print(json.dumps(list_output_1, indent=2))
```

We can use the `.update` method to update the file's metadata.

We'll update its `file_name`, since it's erroneous, change the `{"category": "gothic"}` file tag for something different, and add a `file_description`. We'll leave its `symbolic_directory_path` untouched.


```python
# update metadata the metadata for the processed file

update_output_1 = pipeline_1.update(file_id=XXXX,
                                    file_name="Frankenstein.txt",
                                    file_tags=[{"author": "Shelley"}, {"country": "UK"}, {"century": 19}],
                                    file_description='Is the villain the monster or the doctor?')

# nicely print the output of this .update

print(json.dumps(process_output_1, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "parser-pipeline-1",
      "request_id": "4201b289-9088-42e3-a0ec-8053b9190ba3",
      "message": "Successfully updated file metadata",
      "warnings": []
    }


Now we invoke the [`.list`](../file_system/list_method.md) method to confirm that all metadata has indeed been updated as requested:


```python
# call .list to see the file's newly updated record

list_output_2 = pipeline_1.list(symbolic_file_paths=['/novels/gothic/Frankenstein.txt'])

# nicely print the output of this .list

print(json.dumps(list_output_2, indent=2))
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


### Observations on the `.update` Method

We'll close with four observation on the `.update` method:

- Note that in the example above we updated `file_tags` by including the entire set of file tags: `[{"author": "Shelley"}, {"country": "UK"}, {"century": 19}]`. If we'd only used `[{"country": "UK"}]`, the "author" and "century" ones would have been deleted.

- You cannot update a `symbolic_directory_path`/`file_name` combination (a.k.a. a `symbolic_file_path`) so it's identical to that of another file. Krixik will not allow it.

- You can also not update a file's file extension. For instance, a `.txt` file cannot become a `.pdf` file through the `.update` method.

- The `.update` method allows you to extend a file's [`expire_time`](../parameters_processing_files_through_pipelines/process_method.md#core-process-method-arguments) indefinitely. Upon initially uploading a file, its [`expire_time`](../parameters_processing_files_through_pipelines/process_method.md#core-process-method-arguments) cannot be greater than 2,592,000 seconds (30 days). However, if you periodically invoke `.update` on its file and reset its [`expire_time`](../parameters_processing_files_through_pipelines/process_method.md#core-process-method-arguments) to another 2,592,000 seconds (or however many seconds you please), the file will remain on-system for that much more time as of that moment, and so forth.
