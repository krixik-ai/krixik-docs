# Semantically searchable caption pipeline

This document details a modular pipeline that takes in an image, extracts a text-based description of it, and makes the result semantically searchable.

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [processing a file](#processing-a-file)
- [performing semantic search](#performing-semantic-search)



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

Below we setup a multi module pipeline to serve our intended purpose - using the following modules

- [`caption`](modules/transcribe.md): takes in an input image, outputs json of text-based description
- [`json-to-txt`](modules/json-to-txt.md): takes in json of text snippets, merges into text file
- [`parser`](modules/parser.md): takes in text, slices into (possibly overlapping) strings
- [`text-embedder`](modules/text-embedder.md): takes in text snippets, creates vector representation of each outputing an npy file
- [`vector-db`](modules/vector-db.md): takes in npy of vectors, outputs vector db

We do this by passing the module names to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a multi-module pipeline
pipeline = krixik.create_pipeline(name="examples-caption-semantic-docs",
                                  module_chain=["caption",
                                                "json-to-txt",
                                                "parser",
                                                "text-embedder",
                                                "vector-db"])
```

This pipeline's available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).

## Processing a file

We first define a path to a local input file.

Lets take a quick look at this file before processing.


```python
# examine contents of a valid input file
test_file = "../../../data/input/resturant.png"
from IPython.display import Image
Image(filename=test_file)
```




    
![png](caption-semantic_files/caption-semantic_10_0.png)
    



For this run we will use the default models for the each module of the pipeline.


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```


```python
# test file
test_file = "../../../data/input/resturant.png"

# process test input
process_output = pipeline.process(local_file_path = test_file,
                                  expire_time=60*10,
                                  verbose=True,
                                  local_save_directory="../../../data/output")
```

The output of this process is printed below.  Because the output of this particular pipeline is a database file, the process output is shown as null in the output.  The local address of the output file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "examples-caption-semantic-docs",
      "request_id": "f0bdacfd-c35b-40cb-95b1-7aaac772a5d1",
      "file_id": "793b02d7-2a33-4b6c-93be-c1e8619cfd4f",
      "message": "SUCCESS - output fetched for file_id 793b02d7-2a33-4b6c-93be-c1e8619cfd4f.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/793b02d7-2a33-4b6c-93be-c1e8619cfd4f.faiss"
      ]
    }


## Performing semantic search

Because our pipeline has `text-embedder` and `vector-db` modules we can semantically search the translated transcription, here in Spanish (since we processed our file with an English-Spanish model).  


```python
# semantically search translated transcription
search_output = pipeline.semantic_search(query="having a drink at the bar", 
                                         file_ids=[process_output["file_id"]])

print(json.dumps(search_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "a10ce58a-7c7c-4615-9a48-89a63d4fedfd",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "793b02d7-2a33-4b6c-93be-c1e8619cfd4f",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_cqdgdvvznx.png",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 1,
            "created_at": "2024-05-07 18:50:56",
            "last_updated": "2024-05-07 18:50:56"
          },
          "search_results": [
            {
              "snippet": "a large group of people are in a restaurant",
              "line_numbers": [
                1
              ],
              "distance": 0.386
            }
          ]
        }
      ]
    }


Learn more about the [`semantic_search` method here](system/semantic_search.md).


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
