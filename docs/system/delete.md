## the `.delete` method

You can delete the record of your process on demand using the `delete` method.  This will remove all record of the process from our servers.  This is the manual version of letting the `expire_time` run out on a file.

The `.delete` method takes in a single argument: the `file_id` of the file you wish to delete.

We will illustrate its usage by processing a simple file, deleting it using the `.delete` method, and then checking that it no longer exists using the [`.list` method](list.md).


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False)
```

Now we delete this process record and its output via its `file_id`.


```python
# delete process record and output by file_id
delete_output = pipeline.delete(file_id=process_output["file_id"])

# nicely print the output of this process
json_print(delete_output)
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
json_print(list_output)
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