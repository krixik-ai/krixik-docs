## the `.update` method

You can update the metadata of a file using the `update` method.  This method takes in the `file_id` of the file you would like to update, and the metadata you would like to update.  

You can update any of the following metadata: `expire_time`,  `symbolic_directory_path`, `file_name`, `file_tags`, or `file_description` of the associated file using this method.

We illustrate the use of `.update` by first processing a simple file.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,            # set verbosity to False
                                  symbolic_directory_path = "/my/custom/filepath",
                                  file_name = "some_snippets_3.txt",
                                  file_tags = [{"author": "orwell"}, {"category": "fiction"}],
                                  file_description = "the first paragraph of 1984")
```

Next we use `.update` to change its `file_name`.


```python
# update a process record metadata
update_output = pipeline.update(file_id=process_output["file_id"],
                                file_name="a_new_filename.txt")

# nicely print the output of this process
json_print(update_output)
```

    {
      "status_code": 200,
      "pipeline": "parser-pipeline-1",
      "request_id": "4201b289-9088-42e3-a0ec-8053b9190ba3",
      "message": "Successfully updated file metadata",
      "warnings": []
    }


Now if we use [`.list`](list.md) we can check that our record metadata has been changed.


```python
# list process records
list_output = pipeline.list(file_ids=[process_output["file_id"]])

# nicely print the output of this process
json_print(list_output)
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
