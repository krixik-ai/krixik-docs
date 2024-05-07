# Keyword searchable ocr pipeline

This document details a modular pipeline that takes in an image, extract any text it contains, and makes the result keyword searchable.

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [processing a file](#processing-a-file)
- [performing keyword search](#performing-keyword-search)


```python
# import utilities
import sys 
import json
import importlib
sys.path.append('../../../')
reset = importlib.import_module("utilities.reset")
reset_pipeline = reset.reset_pipeline

# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os
load_dotenv("../../.env")
MY_API_KEY = os.getenv('MY_API_KEY')
MY_API_URL = os.getenv('MY_API_URL')

# import krixik and initialize it with your personal secrets
from krixik import krixik
krixik.init(api_key = MY_API_KEY, 
            api_url = MY_API_URL)
```

    SUCCESS: You are now authenticated.


## Pipeline setup

Below we setup a multi module pipeline to serve our intended purpose, which is to build a pipeline that will extract text from an input image and make it keyword searchable.

To do this we will use the following modules:

- [`ocr`](modules/ocr.md): takes in an image as input, outputs json of extracted text
- [`json-to-txt`](modules/json-to-txt.md): takes in json of text snippets, merges into text file
- [`keyword-db`](modules/keyword-db.md): takes in a text file and parses it for non-trivial keywords and their lemmatized stems, returning a searchable database file


We do this by passing the module names to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a multi-module pipeline
pipeline = krixik.create_pipeline(name="examples-ocr-keyword-docs",
                                  module_chain=["ocr",
                                                "json-to-txt",
                                                "keyword-db"])
```

This pipeline's available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).

## Processing a file

We first define a path to a local input file.

Lets take a quick look at this file before processing.


```python
# examine contents of input file
test_file = "../../../data/input/seal.png"
from IPython.display import Image
Image(filename=test_file)
```




    
![png](ocr-keyword_files/ocr-keyword_10_0.png)
    



For this run we will use the default models for the each module of the pipeline.


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```


```python
# test file
test_file = "../../../data/input/seal.png"

# process test input
process_output = pipeline.process(local_file_path = test_file,
                                  expire_time=60*10,
                                  verbose=True,
                                  local_save_directory="../../../data/output")
```

    INFO: hydrated input modules: {'module_1': {'model': 'tesseract-en', 'params': {}}, 'module_2': {'model': 'base', 'params': {}}, 'module_3': {'model': 'sqlite', 'params': {}}}
    INFO: symbolic_directory_path was not set by user - setting to default of /etc
    INFO: file_name was not set by user - setting to random file name: krixik_generated_file_name_xjgncyyndc.png
    INFO: wait_for_process is set to True.
    INFO: file will expire and be removed from you account in 600 seconds, at Tue May  7 11:56:46 2024 UTC
    INFO: examples-ocr-keyword-docs file process and input processing started...
    INFO: metadata can be updated using the .update api.
    INFO: This process's request_id is: efadad08-d4a3-b894-3b78-f0bfddc8b98e
    INFO: File process and processing status:
    SUCCESS: module 1 (of 3) - ocr processing complete.
    SUCCESS: module 2 (of 3) - json-to-txt processing complete.
    SUCCESS: module 3 (of 3) - keyword-db processing complete.
    SUCCESS: pipeline process complete.
    SUCCESS: process output downloaded


The output of this process is printed below.  Because the output of this particular pipeline is a database file, the process output is shown as null in the output.  The local address of the output file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "examples-ocr-keyword-docs",
      "request_id": "535d930b-48d5-4c8a-9809-608624c93210",
      "file_id": "54ddd5f4-0aa7-4f7b-8167-9eb92d37c69e",
      "message": "SUCCESS - output fetched for file_id 54ddd5f4-0aa7-4f7b-8167-9eb92d37c69e.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/54ddd5f4-0aa7-4f7b-8167-9eb92d37c69e.db"
      ]
    }


## Performing keyword search

Because our pipeline has the `keyword-db` module we can use the [keyword_search method](system/keyword_search.md) and search the transcription.


```python
# semantically search translated transcription
search_output = pipeline.keyword_search(query="he has fallen asleep where he collapsed, near the edge of the forest", 
                                         file_ids=[process_output["file_id"]])

print(json.dumps(search_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "707d9ba2-ab9f-4772-b6ba-2549ee3de1a8",
      "message": "Successfully queried 1 user file.",
      "warnings": [
        {
          "WARNING: the following words in the query are in the stop_words list and thus no results will be returned for them": [
            "he",
            "has",
            "where",
            "he",
            "the",
            "of",
            "the"
          ]
        }
      ],
      "items": [
        {
          "file_id": "54ddd5f4-0aa7-4f7b-8167-9eb92d37c69e",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_xjgncyyndc.png",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_lines": 12,
            "created_at": "2024-05-07 18:46:49",
            "last_updated": "2024-05-07 18:46:49"
          },
          "search_results": [
            {
              "keyword": "fallen",
              "line_number": 8,
              "keyword_number": 10
            },
            {
              "keyword": "asleep",
              "line_number": 8,
              "keyword_number": 11
            },
            {
              "keyword": "collapsed",
              "line_number": 9,
              "keyword_number": 1
            },
            {
              "keyword": "edge",
              "line_number": 9,
              "keyword_number": 4
            },
            {
              "keyword": "forest",
              "line_number": 9,
              "keyword_number": 7
            }
          ]
        }
      ]
    }



```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
