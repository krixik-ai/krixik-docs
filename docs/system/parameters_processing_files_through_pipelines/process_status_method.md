<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/parameters_processing_files_through_pipelines/process_status_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## The `process_status` Method

The `process_status` method is available on every Krixik pipeline. It is invoked whenever you want to check the status of files being processed through a pipeline.

This method is especially useful when using the [`process`](process_method.md) method with `wait_for_process` set to `False`, for it gives you visibility into processes that have continued server-side after you regain control of your IDE.

This overview of the `process_status` method is divided into the following sections:

- [process_status Method Arguments](#process_status-method-arguments)
- [process_status Example](#process_status-example)
- [process_status Example with Deleted File](#process_status-example-with-deleted-file)

### `process_status` Method Arguments

The `process_status` method takes a single argument:

- `request_id`: (required, str) The unique ID associated with the relevant execution instance of the [`process`](process_method.md) method.

### `process_status` Example

Let's examine how the `process_status` method works when the [`process`](process_method.md) method succeeds. `wait_for_process` will be set to `False`.

First we'll need to create a pipeline. We can use a single-module pipeline with a [`keyword-db`](../../modules/database_modules/keyword-db_module.md) module for this example:


```python
# create a pipeline with a single parser module
pipeline = krixik.create_pipeline(name="process_status_method_1_keyword-db", module_chain=["keyword-db"])
```

Now we'll process a file through your pipeline. Let's use a text file holding Herman Melville's <u>Moby Dick</u>:


```python
# process text file through pipeline with wait_for_process on False
process_output = pipeline.process(
    local_file_path=data_dir + "input/moby_dick_very_short.txt",  # the initial local filepath where the input JSON file is stored
    local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=False,  # do not wait for process to complete before returning IDE control to user
    verbose=False,
)  # do not display process update printouts upon running code
```

What does immediate output for this process look like?


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "file_id": "596bf30e-c13d-41df-8cc8-b7e26709a468",
      "request_id": "f948a6ad-0343-e743-2b3f-0df6bc732a3a",
      "file_name": "krixik_generated_file_name_gewgneptrz.txt",
      "symbolic_directory_path": "/etc",
      "file_tags": null,
      "file_description": null
    }


That's all you see because you retook control of the IDE as soon as the upload to Krixik was completed; the `process_output_1` variable doesn't know how the rest of the process went.

You can check the status of the process by feeding the `request_id` (returned when you called the [`process`](process_method.md) method) to the `process_status` method, as follows:


```python
# invoke process_status
process_1_status = pipeline.process_status(request_id=process_output["request_id"])

# nicely print the output our process_status call
print(json.dumps(process_1_status, indent=2))
```

    {
      "status_code": 200,
      "request_id": "8863f851-fa57-4ffa-98fd-31d9df31fcdc",
      "file_id": "596bf30e-c13d-41df-8cc8-b7e26709a468",
      "message": "SUCCESS: process_status found",
      "pipeline": "process_status_method_1_keyword-db",
      "process_status": {
        "module_1": false
      },
      "overall_status": "ongoing"
    }


Here you can see that your process has not yet finalized; its `overall_status` shows as `"ongoing"`.

If we wait a few moments and try again, you will see confirmation that the process completed successfully.


```python
# invoke process_status again
process_status_output = pipeline.process_status(request_id=process_output["request_id"])

# nicely print the output our process_status call again
print(json.dumps(process_status_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "4cf89f97-b82e-4104-929f-df49d928e345",
      "file_id": "596bf30e-c13d-41df-8cc8-b7e26709a468",
      "message": "SUCCESS: process_status found",
      "pipeline": "process_status_method_1_keyword-db",
      "process_status": {
        "module_1": true
      },
      "overall_status": "complete"
    }


### `process_status` Example with Deleted File

As you have just observed, `process_status` on a failed [`process`](process_method.md) attempt shows us that the process failed.

What happens when the file `process_status` is run on [expires](process_method.md#core-process-method-arguments) or is manually [deleted](../file_system/delete_method.md) from the Krixik system?

We take deletion seriously at Krixik—if a file is [deleted](../file_system/delete_method.md), it's entirely wiped from the system. Consequently, calling the `process_status` method on an [expired](process_method.md#core-process-method-arguments) or manually [deleted](../file_system/delete_method.md) file will tell you that the `request_id` you used as an argument was not found. The file is gone, as is any record of its having been processed in the first place.
