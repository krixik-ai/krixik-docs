## A simple keyword search pipeline

This document reviews a simple keyword search pipeline that can be used to make any input text keyword-searchable.

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [processing a file](#processing-a-file)
- [using the `keyword_search` method](#using-the-keyword_search-method)

## Pipeline setup

Below we setup a simple one module pipeline using the [keyword-db module](../../modules/keyword-db.md). 

We do this by passing the module names to the `module_chain` argument of [`create_pipeline`](../../system/create_save_load.md) along with a name for our pipeline.


```python
# create a pipeline with a multi module pipeline
pipeline = krixik.create_pipeline(
    name="examples-text-search-keyword-docs", module_chain=["keyword-db"]
)
```

This pipeline's available modeling options and parameters are stored in your custom [pipeline's configuration](../../system/create_save_load.md).

## Processing a file

The `keyword-db` module accepts `.txt`, `.pdf`, `.docx`, and `.pptx` file formats as input.  The latter three (`.pdf`, `.docx`, and `.pptx`) are first converted to `.txt` prior to processing.

Let's look at an example of a small valid input - and then process it.


```python
# examine contents of a valid test input file
test_file = "../../data/input/1984_very_short.txt"
with open(test_file, "r") as file:
    print(file.read())
```

    It was a bright cold day in April, and the clocks were striking thirteen.
    Winston Smith, his chin nuzzled into his breast in an effort to escape the
    vile wind, slipped quickly through the glass doors of Victory Mansions,
    though not quickly enough to prevent a swirl of gritty dust from entering
    along with him.


Now let's process this file using our default model.


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
```

The output of this process is printed below.  Because the output of this particular pipeline is a sqlite database, the process output is provided in this object is null.  However the file itself has been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "my-keyword-db-pipeline",
      "request_id": "5951c05e-5cb0-4c17-8d4d-d87c887c9cd1",
      "file_id": "36c032ab-ac57-4c3f-a67a-0810fee184bd",
      "message": "SUCCESS - output fetched for file_id 36c032ab-ac57-4c3f-a67a-0810fee184bd.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../data/output/36c032ab-ac57-4c3f-a67a-0810fee184bd.db"
      ]
    }


## Using the `keyword_search` method

Any pipeline containing a `keyword-search` module automatically inherits access to the [`keyword_search` method](../../system/keyword_search.md).  This provides convenient sophisticated query access to the newly created keyword database in krixik.

The `keyword_search` method takes in an input `query` containing desired keywords separated by spaces, and searches through your database(s) for these keywords as well as their lemmatized stems.

An example use if given below.


```python
# perform keyword_search over the input file
keyword_output = pipeline.keyword_search(
    query="it was cold night", file_ids=[process_output["file_id"]]
)

# nicely print the output of this process
print(json.dumps(keyword_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "03d35d92-edf9-4969-8b5a-481606535b09",
      "message": "Successfully queried 1 user file.",
      "warnings": [
        {
          "WARNING: the following words in the query are in the stop_words list and thus no results will be returned for them": [
            "it",
            "was"
          ]
        }
      ],
      "items": [
        {
          "file_id": "36c032ab-ac57-4c3f-a67a-0810fee184bd",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_sblojcvlzc.txt",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_lines": 5,
            "created_at": "2024-05-03 21:59:13",
            "last_updated": "2024-05-03 21:59:13"
          },
          "search_results": [
            {
              "keyword": "cold",
              "line_number": 1,
              "keyword_number": 5
            }
          ]
        }
      ]
    }

