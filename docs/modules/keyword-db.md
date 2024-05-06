## The `keyword-db` module

This document reviews the `keyword-db` module - which takes as input a document, parses the documents for non-trivial keywords and their lemmatized stems, and returns a database with this content.

This document includes an overview of custom pipeline setup, current model set, parameters, and `.process` usage for this module.

To follow along with this demonstration be sure to initialize your krixik session with your api key and url as shown below. 

We illustrate loading these required secrets in via [python-dotenv](https://pypi.org/project/python-dotenv/), storing those secrets in a `.env` file.  This is always good practice for storing / loading secrets (e.g., doing so will reduce the chance you inadvertantly push secrets to a repo).

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [required input format](#required-input-format)
- [using the default model](#using-the-default-model)
- [using the `keyword_search` method](#using-the-keyword_search-method)
- [querying output databases locally](#querying-output-databases-locally)


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

## Pipeline setup

Below we setup a simple one module pipeline using the `keyword-search` module. 

We do this by passing the module name to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(
    name="modules-keyword-db-docs", module_chain=["keyword-db"]
)
```

The `keyword-search` module comes with a single model:

- `base`: (default) parses input document for non-trivial keywords

These available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```

## Required input format

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


## Using the default model

Now let's process it using our default model - `base`.  Because `base` is the default model we need not input the optional `modules` argument into `.process`.


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

The output of this process is printed below.  Because the output of this particular module-model pair is a sqlite database, the process output is provided in this object is null.  However the file itself has been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


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

Any pipeline containing a `keyword-search` module automatically inherits access to the [`keyword_search` method](system/keyword_search.md).  This provides convenient sophisticated query access to the newly created keyword database in krixik.

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


## Querying output databases locally

We can now perform queries on the pulled keyword database whose location is given in `process_output_files`.

Below is a simple function for performing single keyword queries on this database locally.


```python
import sqlite3


def query_db(query_keyword: str, keyword_db_local_file_name: str) -> list:
    # load keyword_db
    keyword_db = sqlite3.connect(keyword_db_local_file_name)
    keyword_cursor = keyword_db.cursor()

    # create query pattern
    query_pattern = f"""
    SELECT
        original_keyword,
        line_number,
        keyword_number
    FROM
        keyword_search
    where original_keyword="{query_keyword}"
    GROUP BY
        original_keyword,
        line_number,
        keyword_number
    ORDER BY
        line_number,
        keyword_number
    """

    # excute query
    keyword_cursor.execute(query_pattern)

    # Fetch and process the results
    rows = keyword_cursor.fetchall()
    return rows
```

Below we query our small database using a single keyword query.


```python
# query database
query = "cold"
query_db(query, process_output["process_output_files"][0])
```




    [('cold', 1, 5)]




```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
