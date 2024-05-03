## The `keyword-db` module

This document reviews the `keyword-db` module - which takes as input a document, parses the documents for non-trivial keywords and their lemmatized stems, and returns a database with this content.

This document includes an overview of custom pipeline setup, current model set, parameters, and `.process` usage for this module.

To follow along with this demonstration be sure to initialize your krixik session with your api key and url as shown below. 

We illustrate loading these required secrets in via [python-dotenv](https://pypi.org/project/python-dotenv/), storing those secrets in a `.env` file.  This is always good practice for storing / loading secrets (e.g., doing so will reduce the chance you inadvertantly push secrets to a repo).


```python
# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os
load_dotenv("../.env")
MY_API_KEY = os.getenv('MY_API_KEY')
MY_API_URL = os.getenv('MY_API_URL')

# import krixik and initialize it with your personal secrets
from krixik import krixik
krixik.init(api_key = MY_API_KEY, 
            api_url = MY_API_URL)
```

This small function prints dictionaries very nicely in notebooks / markdown.


```python
# print dictionaries / json nicely in notebooks / markdown
import json
def json_print(data):
    print(json.dumps(data, indent=2))
```

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [required input format](#required-input-format)
- [using the default model](#using-the-default-model)
- [using the `keyword_search` method](#using-the-keyword-search-method)
- [querying output databases locally](#querying-output-databases-locally)

## Pipeline setup

Below we setup a simple one module pipeline using the `keyword-search` module. 


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(name="my-keyword-db-pipeline",
                                  module_chain=["keyword-db"])
```

The `keyword-search` module comes with a single model:

- `base`: (default) parses input document for non-trivial keywords

These available modeling options and parameters are stored in our custom pipeline's configuration (described further in LINK HERE).  We can examine this configuration as shown below.


```python
# nicely print pipeline configuration
json_print(pipeline.config)
```

    {
      "pipeline": {
        "name": "my-keyword-db-pipeline",
        "modules": [
          {
            "name": "keyword-db",
            "models": [
              {
                "name": "sqlite"
              }
            ],
            "defaults": {
              "model": "sqlite"
            },
            "input": {
              "type": "text",
              "permitted_extensions": [
                ".txt",
                ".pdf",
                ".docx",
                ".pptx"
              ]
            },
            "output": {
              "type": "db"
            }
          }
        ]
      }
    }


Here we can see the models and their associated parameters available for use.

You can save this configuration to disk as well by executing


```python
pipeline.save("/valid/path/file.yml")
```

You can instantiate a pipeline directly from its configuration using the [.load_pipeline method](LINK HERE).

## Required input format

The `keyword-db` module accepts `.txt`, `.pdf`, `.docx`, and `.pptx` file formats as input.  The latter three (`.pdf`, `.docx`, and `.pptx`) are first converted to `.txt` prior to processing.

Let's look at an example of a small valid input - and then process it.


```python
# examine contents of a valid test input file
test_file = "../input_data/1984_very_short.txt"
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
test_file = "../input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*10,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is a sqlite database, the process output is provided in this object is null.  However the file itself has been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "my-keyword-db-pipeline",
      "request_id": "74615be1-3d00-415e-9003-d447f8a2ad63",
      "file_id": "44ff5484-2a57-4cd3-8d57-eddf7cec30e2",
      "message": "SUCCESS - output fetched for file_id 44ff5484-2a57-4cd3-8d57-eddf7cec30e2.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "./44ff5484-2a57-4cd3-8d57-eddf7cec30e2.db"
      ]
    }


## Using the `keyword_search` method

Any pipeline containing a `keyword-search` module automatically inherits access to the [`keyword_search` method](keyword_search_method.md).  This provides convenient sophisticated query access to the newly created keyword database in krixik.

The `keyword_search` method takes in an input `query` containing desired keywords separated by spaces, and searches through your database(s) for these keywords as well as their lemmatized stems.

An example use if given below.


```python
# perform keyword_search over the input file
keyword_output = pipeline.keyword_search(query="it was cold night",
                                         file_ids=[process_output["file_id"]])

# nicely print the output of this process
json_print(keyword_output)
```

    {
      "status_code": 200,
      "request_id": "a5912e1b-e7d5-4082-b5c0-fb2bb28f74ed",
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
          "file_id": "44ff5484-2a57-4cd3-8d57-eddf7cec30e2",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_xtbxaaerso.txt",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_lines": 5,
            "created_at": "2024-05-02 22:14:06",
            "last_updated": "2024-05-02 22:14:06"
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

def query_db(query_keyword: str,
             keyword_db_local_file_name: str) -> list:
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
query_db(query,
         process_output['process_output_files'][0])
```




    [('cold', 1, 5)]


