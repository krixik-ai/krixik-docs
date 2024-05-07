## The `semantic_search` method

krixik's `semantic_search` method is a convenience function for both embedding and querying - and so can only be used with pipelines containing both [`text-embedder`](modules/text-embedder.md) and [`vector-db`](modules/vector-db.md) modules in succession.

A table of contents for the remainder of this document is shown below.

- [basic pipeline setup](#basic-pipeline-setup)
- [basic usage, required input, and output breakdown](#basic-usage,-required-input,-and-output-breakdown)


```python
# import utilities
import sys
import json
import importlib

sys.path.append("../../")
reset = importlib.import_module("utilities.reset")
reset_pipeline = reset.reset_pipeline

# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os

load_dotenv("../../.env")
MY_API_KEY = os.getenv("MY_API_KEY")
MY_API_URL = os.getenv("MY_API_URL")

# import krixik and initialize it with your personal secrets
from krixik import krixik

krixik.init(api_key=MY_API_KEY, api_url=MY_API_URL)
```

## Basic pipeline setup

For this document we will use a pipeline consisting of three modules: a [`parser`](modules/parser.md), [`text-embedder`](modules/text-embedder.md), and [`vector-db`](modules/vector-db.md) index.  We use [`create_pipeline`](system/create_save_load.md) to instantiate the pipeline.


```python
# create a pipeline with multiple modules
pipeline = krixik.create_pipeline(
    name="system-semantic-search",
    module_chain=["parser", "text-embedder", "vector-db"],
)
```

These available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```

## Basic usage, required input, and output breakdown

To illustrate the usage of `semantic_search` we process a short file illustrated in the introduction to the [`parser` method](modules/parser.md).


```python
# define path to an input file from examples directory
test_file = "../../data/input/1984_very_short.txt"

# process for search
process_output = pipeline.process(
    local_file_path=test_file,
    local_save_directory="../../data/output",  # save output repo data output subdir
    expire_time=60 * 10,  # set all process data to expire in 10 minutes
    wait_for_process=True,  # wait for process to complete before regaining ide
    verbose=False,
)  # set verbosity to False

#
print(json.dumps(process_output, indent=2))
```

Let us examine the returned output.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```


    '{\n  "file_id": "3d435c55-05ae-41b6-aee3-76da8c7b0841",\n  "request_id": "5e723bee-4939-21f1-52ef-ca0596dd3f1f",\n  "file_name": "krixik_generated_file_name_vplttsahnp.txt",\n  "symbolic_directory_path": "/etc",\n  "file_tags": null,\n  "file_description": null\n}'


Lets first process a file with our new pipeline.  The [`vector-db`](modules/vector-db.md) module takes in a text file, and returns `faiss` vector database consisting of all non-trivial `(snippet, line_numbers)` tuples from the input.


```python
# define path to an input file from examples directory
test_file = "../../data/input/1984_very_short.txt"

# process for search
process_output = pipeline.process(
    local_file_path=test_file,
    local_save_directory="../../data/output",  # save output repo data output subdir
    expire_time=60 * 10,  # set all process data to expire in 10 minutes
    wait_for_process=True,  # wait for process to complete before regaining ide
    verbose=False,
)  # set verbosity to False

# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "vector-search-pipeline-1",
      "request_id": "1a09068c-872a-4389-a399-7281e2d1764e",
      "file_id": "f69aac3d-e674-45d5-ab33-f16196ce82b2",
      "message": "SUCCESS - output fetched for file_id f69aac3d-e674-45d5-ab33-f16196ce82b2.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "./f69aac3d-e674-45d5-ab33-f16196ce82b2.faiss"
      ]
    }


Note that we did not define a `file_name` or `symbolic_directory_path` ourselves, so defaults will be given as described in the `.process` walkthrough [LINK HERE].

Here the `process_output` key value is `null` since the return object is a database.  We can see this database in the local location provided in the `process_output_files` value.

With `.process` complete we can run `semantic_search` on our input file. 

The `semantic_search` method takes in the exact same arguments as [`list`](system/list.md) - that is `file_ids`, `file_names`, etc., - plus one additional argument: `query`.  The `query` is a string of words to be queried individually.

Let's look at an example.


```python
# perform semantic_search over the input file
semantic_output = pipeline.semantic_search(
    query="it was cold night", file_ids=[process_output["file_id"]]
)

# nicely print the output of this process
print(json.dumps(semantic_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "10503c1c-3959-4897-9315-a69438ecce2b",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "f69aac3d-e674-45d5-ab33-f16196ce82b2",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_awiouirlff.txt",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 2,
            "created_at": "2024-04-26 21:10:50",
            "last_updated": "2024-04-26 21:10:50"
          },
          "search_results": [
            {
              "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
              "line_numbers": [
                1
              ],
              "distance": 0.224
            },
            {
              "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
              "line_numbers": [
                2,
                3,
                4,
                5
              ],
              "distance": 0.417
            }
          ]
        }
      ]
    }


Here we can see one returned search result in `items`.


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
