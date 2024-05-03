## the `.process_status` method

The `.process_status` method lets you check the status of a pipeline usage of `.process` via a `request_id`.  This is especially useful when using the [`.process` method](process.md) with `wait_for_process` set to `False`.

To illustrate its usage, let us first process a file with our pipeline using `wait_for_process` set to `False`.  This will give us back control of our IDE / notebook as soon as the file has completed upload. 


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".",  # save output in current directory
                                  expire_time=60*5,          # set all process data to expire in 5 minutes
                                  wait_for_process=False,    # do not wait for process to complete before regaining ide
                                  verbose=False)             # set verbosity to False
```

Let us quickly examine the returned output.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "file_id": "ce251869-5026-4026-ad40-35e2af5e73eb",
      "request_id": "bcda2f5b-aaf9-5242-98d6-32e5fedbf5ff",
      "file_name": "krixik_generated_file_name_hzufejnxft.txt",
      "symbolic_directory_path": "/etc",
      "file_tags": null,
      "file_description": null
    }


Now we can check the status of our process using returned `request_id` and the `.process_status` as shown below.


```python
# use .process_status
status_output = pipeline.process_status(request_id=process_output["request_id"])

# nicely print the output of this process
json_print(status_output)
```

    {
      "status_code": 200,
      "request_id": "398f4ad1-bb93-4b4b-bfa4-8a26e618a068",
      "file_id": "ce251869-5026-4026-ad40-35e2af5e73eb",
      "message": "SUCCESS: process_status found",
      "pipeline": "parser-pipeline-1",
      "process_status": {
        "parser": true
      },
      "overall_status": "complete"
    }


Here we can see that the status of our single module has not yet completed.

If we wait a few moments and try again, we will see confirmation that the process completed successfully.


```python
# use .process_status
status_output = pipeline.process_status(request_id=process_output["request_id"])

# nicely print the output of this process
json_print(status_output)
```

    {
      "status_code": 200,
      "request_id": "4f91cc57-9df7-4faa-bbfd-57fc3abd9a50",
      "file_id": "ce251869-5026-4026-ad40-35e2af5e73eb",
      "message": "SUCCESS: process_status found",
      "pipeline": "parser-pipeline-1",
      "process_status": {
        "parser": true
      },
      "overall_status": "complete"
    }
