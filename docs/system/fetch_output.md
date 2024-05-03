## the `.fetch_output` method

The `.fetch_output` method is used to download the output of a pipeline process.  This is particularly useful when using `.process` with `wait_for_process` set to `False`, as your output is not immediately pulled.

Lets see how this works by processing a file with `wait_for_process` set to `False`.  We will first use [`.process_status`](process_status.md) to make sure the file has completed processing.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  expire_time=60*5,          # set all process data to expire in 5 minutes
                                  wait_for_process=False,    # do not wait for process to complete before regaining ide
                                  verbose=False)             # set verbosity to False
```

Now we check the status of our process via the returned `request_id`.


```python
# use .process_status
status_output = pipeline.process_status(request_id=process_output["request_id"])

# nicely print the output of this process
json_print(status_output)
```

    {
      "status_code": 200,
      "request_id": "9f81bcbc-f523-48a8-a33a-5669547401af",
      "file_id": "1488dd6d-4bc5-4d61-b7d5-ff5262fce5f1",
      "message": "SUCCESS: process_status found",
      "pipeline": "parser-pipeline-1",
      "process_status": {
        "parser": false
      },
      "overall_status": "ongoing"
    }


Since the file has completed processing we can now use `.fetch_output`.

`.fetch_output` takes in a two inputs

 - the `file_id` of the uploaded and processed file
 - a `local_save_directory` (optional) where the completed files will be saved locally (default is current working directory)


```python
# fetch the output of our process using file_id
fetch_output = pipeline.fetch_output(file_id=process_output["file_id"],
                                     local_save_directory=".")
```

Printing the fetched output return we have our json returned in the `fetch_output` key-value.  

The `process_output_files` key-value pair shows the download location(s) of our completed process files pulled by `.fetch_output`.


```python
# nicely print the output of this process
json_print(fetch_output)
```

    {
      "status_code": 200,
      "pipeline": "parser-pipeline-1",
      "request_id": "66cacfdf-f4a8-4061-9322-50489d5d9670",
      "file_id": "1488dd6d-4bc5-4d61-b7d5-ff5262fce5f1",
      "message": "SUCCESS - output fetched for file_id 1488dd6d-4bc5-4d61-b7d5-ff5262fce5f1.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
          "line_numbers": [
            1
          ]
        },
        {
          "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
          "line_numbers": [
            2,
            3,
            4,
            5
          ]
        }
      ],
      "process_output_files": [
        "./1488dd6d-4bc5-4d61-b7d5-ff5262fce5f1.json"
      ]
    }
