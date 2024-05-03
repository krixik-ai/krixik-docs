## the `vector-db` module

This document reviews the `vector-db` module - which takes as input a numpy array, indexes its vectors, and returns an indexed [faiss database](https://github.com/facebookresearch/faiss).

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
- [using the `base` model](#using-the-base-model)
- [using the `keyword_search` method](#using-the-keyword-search-method)
- [querying output databases locally](#querying-output-databases-locally)

## Pipeline setup

Below we setup a simple one module pipeline using the `keyword-search` module. 


```python
# import custom module creation tools
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# instantiate module
module_1 = Module(module_type="vector-db")

# create custom pipeline object
custom = CreatePipeline(name='vector-db-pipeline-1', 
                        module_chain=[module_1])

# pass the custom object to the krixik operator (note you can also do this by passing its config)
pipeline = krixik.load_pipeline(pipeline=custom)
```

The `vector-search` module comes with a single model:

- `faiss`: (default) indexes a numpy array of input vectors

These available modeling options and parameters are stored in our custom pipeline's configuration (described further in LINK HERE).  We can examine this configuration as shown below.


```python
# nicely print the configuration of uor custom pipeline
json_print(custom.config)
```

    {
      "pipeline": {
        "name": "vector-db-pipeline-1",
        "modules": [
          {
            "name": "vector-db",
            "models": [
              {
                "name": "faiss"
              }
            ],
            "defaults": {
              "model": "faiss"
            },
            "input": {
              "type": "npy",
              "permitted_extensions": [
                ".npy"
              ]
            },
            "output": {
              "type": "faiss"
            }
          }
        ]
      }
    }


Here we can see the models and their associated parameters available for use.

## using the `faiss` model

We first load in a handful of vectors from disk.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/vectors.npy"
```

Lets take a quick look at this file before processing.


```python
# examine contents of input file
import numpy as np
np.load(test_file)
```




    array([[0, 1],
           [1, 0],
           [1, 1]])



Three simple two dimensional vectors.

Now let's process it using our `faiss` model.  Because `faiss` is the default model we need not input the optional `modules` argument into `.process`.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/vectors.npy"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is a faiss database, the process output is provided in this object is null.  However the file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "vector-search-pipeline-1",
      "request_id": "e0afa9f1-b34c-42bc-b617-dc80f0a6e396",
      "file_id": "8da8fbfd-501d-4933-8559-4a30ed75ef27",
      "message": "SUCCESS - output fetched for file_id 8da8fbfd-501d-4933-8559-4a30ed75ef27.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "./8da8fbfd-501d-4933-8559-4a30ed75ef27.faiss"
      ]
    }


### querying output databases locally

We can now perform queries on the pulled vector database whose location is given in `process_output_files`.

Below is a simple function for performing single keyword queries on this database locally.  Note: you will need to install the faiss library to execute this cell.  Install [faiss-cpu](https://pypi.org/project/faiss-cpu/) or [faiss-gpu](https://pypi.org/project/faiss-gpu/) depending on the specs of your local setup.


```python
import faiss
import numpy as np
from typing import Tuple

def query_vector_db(query_vector: np.ndarray,
                    k: int,
                    db_file_path: str) -> Tuple[list,list]:
    # read in vector db
    faiss_index = faiss.read_index(db_file_path)
    
    # perform query
    similarities, indices = faiss_index.search(query_vector, k)
    distances = 1 - similarities
    return distances, indices
```

Perform a simple query using the test function above.


```python
original_vectors[2]
```




    array([1, 1])




```python
# perform test query using the above query function
original_vectors = np.load(test_file)
query_vector = np.array([[0,1]])
distances, indices = query_vector_db(query_vector, 2, process_output['process_output_files'][0])
print(f"input query vector: {query_vector[0]}")
print(f"closest vector from original: {original_vectors[indices[0][0]]}")
print(f"distance from query to this vector: {distances[0][0]}")
print(f"second closest vector from original: {original_vectors[indices[0][1]]}")
print(f"distance from query to this vector: {distances[0][1]}")
```

    input query vector: [0 1]
    closest vector from original: [0 1]
    distance from query to this vector: 0.0
    second closest vector from original: [1 1]
    distance from query to this vector: 0.2928932309150696


### using the `vector_search` method

krixik's `vector_search` method is a convenience function for both embedding and querying - and so can only be used with pipelines containing both `text-embedder` and `vector-search` modules in succession.

Below we construct the simplest custom pipeline that satisfies this criteria - a standard vector search pipeline consisting of three modules: a `parser`, `text-embedder`, and `vector-search` index.


```python
# import custom module creation tools
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# instantiate module
module_1 = Module(module_type="parser")
module_2 = Module(module_type="text-embedder")
module_3 = Module(module_type="vector-search")

# create custom pipeline object
custom = CreatePipeline(name='vector-search-pipeline-1', 
                        module_chain=[module_1, module_2, module_3])

# pass the custom object to the krixik operator (note you can also do this by passing its config)
pipeline = krixik.load_pipeline(pipeline=custom)
```

We can now perform any of the core system methods on our custom pipeline (e.g., `.process`, `.list`, etc.,).  Additionally we can invoke the `vector_search` method.

Lets first process a file with our new pipeline.  The `vector-search` module takes in a text file, and returns `faiss` vector database consisting of all non-trivial `(snippet, line_numbers)` tuples from the input.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False

# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "vector-search-pipeline-1",
      "request_id": "d6fc4df7-1ae3-4540-ac93-c431008fa063",
      "file_id": "656c6486-8a89-43ea-8658-762dbf8b9c9c",
      "message": "SUCCESS - output fetched for file_id 656c6486-8a89-43ea-8658-762dbf8b9c9c.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "./656c6486-8a89-43ea-8658-762dbf8b9c9c.faiss"
      ]
    }


Now we can query our text with natural language as shown below.


```python
# perform vector_search over the input file
vector_output = pipeline.vector_search(query="it was cold night",
                                       file_ids=[process_output["file_id"]])

# nicely print the output of this process
json_print(vector_output)
```

    {
      "status_code": 200,
      "request_id": "98e6c488-440d-4a1a-978b-bb82affcb1b4",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "656c6486-8a89-43ea-8658-762dbf8b9c9c",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_advielayge.txt",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 2,
            "created_at": "2024-04-28 16:21:06",
            "last_updated": "2024-04-28 16:21:06"
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

