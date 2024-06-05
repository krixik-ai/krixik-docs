<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/parameters_processing_files_through_pipelines/fetch_output_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## The `.fetch_output` Method

The `.fetch_output` method is used to download the output of a pipeline process.  This is particularly useful when using the [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method with `wait_for_process` set to `False`, as your output is in that case not immediately yielded by the [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method.

### `.fetch_output` Method Arguments

The `.fetch_output` method takes two arguments:

- `file_id`: (required, str) The `file_id` of the file whose [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method output you wish to fetch.
- `local_save_directory`: (required, str) The local directory where you would like the fetched output to be saved to. Defaults to current working directory.


### `.fetch_output` Example

You will first need to create a pipeline on which to run this example. A pipeline consisting of a single [`parser`](../../modules/support_function_modules/parser_module.md) module will do nicely:


```python
# create a single-module pipeline with a parser module for this example
pipeline = krixik.create_pipeline(name="fetch-output-method_1_parser", module_chain=["parser"])
```

Now we run a file through this pipeline. We'll use a simple TXT file that holds the first paragraph of George Orwell's <u>1984</u>:


```python
# process the TXT file through the single-module parser pipeline
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_very_short.txt",
    local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
    expire_time=60 * 60 * 24 * 7,  # process data will be deleted from the Krixik system in 7 days
    wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
    verbose=False,
)  # do not display process update printouts upon running code
```

The file has successfully been processed. Let's assume that some days have passed and you need to retrieve this file's output. We'll need its `file_id`, so we can print the `process_output_1` object above to get it:


```python
# run o see its file_id
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "fetch-output-method_1_parser",
      "request_id": "ff3a5841-f250-49d2-94ca-f142b57129a1",
      "file_id": "83f7bc97-bf47-4b3d-8268-b1a147be8950",
      "message": "SUCCESS - output fetched for file_id 83f7bc97-bf47-4b3d-8268-b1a147be8950.Output saved to location(s) listed in process_output_files.",
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
        "../../../data/output/83f7bc97-bf47-4b3d-8268-b1a147be8950.json"
      ]
    }


Armed with its `file_id`, you can use the `.fetch_output` method to suit your purpose:


```python
# fetch the output of this process using .fetch_output and its file_id
fetched_output = pipeline.fetch_output(file_id=process_output["file_id"], local_save_directory="../../../data/output")
```

Printing the fetched output return displays the sought JSON and some additional information. This additional information is very similar to output from the [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method:


```python
# nicely print the fetched output
print(json.dumps(fetched_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "fetch-output-method_1_parser",
      "request_id": "607cfa28-1c7e-4ea7-aba0-9e4de42a0c41",
      "file_id": "83f7bc97-bf47-4b3d-8268-b1a147be8950",
      "message": "SUCCESS - output fetched for file_id 83f7bc97-bf47-4b3d-8268-b1a147be8950.Output saved to location(s) listed in process_output_files.",
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
        "../../../data/output/83f7bc97-bf47-4b3d-8268-b1a147be8950.json"
      ]
    }


At the end of this return the local directory to which the output has been downloaded is displayed.
