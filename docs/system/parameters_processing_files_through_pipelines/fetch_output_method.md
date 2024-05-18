## The `.fetch_output` Method

The `.fetch_output` method is used to download the output of a pipeline process.  This is particularly useful when using the [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method with `wait_for_process` set to `False`, as your output is in that case not immediately yielded by the [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method.

### `.fetch_output` Method Arguments

The `.fetch_output` method takes two arguments:

- `file_id`: (required, str) The `file_id` of the file whose [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method output you wish to fetch.
- `local_save_directory`: (required, str) The local directory where you would like the fetched output to be saved to. Defaults to current working directory.


### `.fetch_output` Example

You will first need to create a pipeline on which to run this example. A pipeline consisting of a single [`parser`](../../modules/ai_model_modules/parser_module.md) module will do nicely:


```python
# create a single-module pipeline with a parser module for this example

pipeline_1 = krixik.create_pipeline(name="fetch-output-method_1_parser",
                                    module_chain=["parser"])
```


      Cell In[1], line 3
        pipeline_1 = krixik.create_pipeline(name="fetch-output-method_1_parser"
                                                 ^
    SyntaxError: invalid syntax. Perhaps you forgot a comma?



Now we run a file through this pipeline. We'll use a simple TXT file that holds the first paragraph of George Orwell's <u>1984</u>:


```python
# process the TXT file through the single-module parser pipeline

process_output_1 = pipeline_1.process(local_file_path="../../data/input/1984_very_short.txt",
                                      expire_time=60*60*24*7,  # process data will be deleted from the Krixik system in 7 days
                                      wait_for_process=True, # do not wait for process to complete before returning IDE control to user
                                      verbose=False)  # do not display process update printouts upon running code
```

The file has successfully been processed. Let's assume that some days have passed and you need to retrieve this file's output. Armed with its `file_id`, you can use the `.fetch_output` method to suit your purpose:


```python
# fetch the output of this process using .fetch_output and its file_id

fetched_output_1 = pipeline_1.fetch_output(file_id="XXXX",
                                           local_save_directory="../../data/output")
```

Printing the fetched output return displays the sought JSON and some additional information. This additional information is very similar to output from the [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method:


```python
# nicely print the fetched output

print(json.dumps(fetched_output_1, indent=2))
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


At the end of this return the local directory to which the output has been downloaded is displayed.
