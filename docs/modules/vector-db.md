## The `vector-db` module

This document reviews the `vector-db` module - which takes as input a numpy array, indexes its vectors, and returns an indexed [faiss database](https://github.com/facebookresearch/faiss).

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [required input format](#required-input-format)
- [using the default model](#using-the-default-model)
- [using the `semantic_search` method](#using-the-semantic_search-method)
- [querying output databases locally](#querying-output-databases-locally)

## Pipeline setup

Below we setup a simple one module pipeline using the `vector-db` module.

We do this by passing the module name to the `module_chain` argument of [`create_pipeline`](../system/create_save_load.md) along with a name for our pipeline.


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(
    name="modules-vector-db-docs", module_chain=["vector-db"]
)
```

The `vector-db` module comes with a single model:

- `faiss`: (default) indexes a numpy array of input vectors

These available modeling options and parameters are stored in your custom [pipeline's configuration](../system/create_save_load.md).

## Required input format

The `vector-db` module accepts `.npy` consisting of a single numpy array.  Each row is a vector to be indexed for vector search.

Let's look at an example of a small valid input - and then process it.


```python
# examine contents of input file
import numpy as np

test_file = "../../data/input/vectors.npy"
np.load(test_file)
```




    array([[0, 1],
           [1, 0],
           [1, 1]])



## Using the default model

Now let's process it using the default model - `faiss`.  Because `faiss` is the default model we need not input the optional `modules` argument into `.process`.


```python
# define path to an input file from examples directory
test_file = "../../data/input/vectors.npy"

# process for search
process_output = pipeline.process(
    local_file_path=test_file,
    local_save_directory="../../data/output",  # save output repo data output subdir
    expire_time=60 * 10,  # set all process data to expire in 5 minutes
    wait_for_process=True,  # wait for process to complete before regaining ide
    verbose=False,
)  # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is a faiss database, the process output is provided in this object is null.  However the file itself has been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "my-vector-db-pipeline",
      "request_id": "702f3ae8-4d2c-4723-9677-dd42133baba3",
      "file_id": "a98fc86e-204a-428d-9144-d929624e2f5a",
      "message": "SUCCESS - output fetched for file_id a98fc86e-204a-428d-9144-d929624e2f5a.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../data/output/a98fc86e-204a-428d-9144-d929624e2f5a.faiss"
      ]
    }


## Querying output databases locally

We can now perform queries on the pulled vector database whose location is given in `process_output_files`.

Below is a simple function for performing single keyword queries on this database locally.  Note: you will need to install the faiss library to execute this cell.  Install [faiss-cpu](https://pypi.org/project/faiss-cpu/) or [faiss-gpu](https://pypi.org/project/faiss-gpu/) depending on the specs of your local setup.


```python
# make sure you install faiss (faiss-cpu or faiss-gpu)
import faiss
import numpy as np
from typing import Tuple


def query_vector_db(
    query_vector: np.ndarray, k: int, db_file_path: str
) -> Tuple[list, list]:
    # read in vector db
    faiss_index = faiss.read_index(db_file_path)

    # perform query
    similarities, indices = faiss_index.search(query_vector, k)
    distances = 1 - similarities
    return distances, indices
```

Perform a simple query using the test function above.


```python
# perform test query using the above query function
original_vectors = np.load(test_file)
query_vector = np.array([[0, 1]])
distances, indices = query_vector_db(
    query_vector, 2, process_output["process_output_files"][0]
)
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


## Using the `semantic_search` method

krixik's `semantic_search` method is a convenience function for both embedding and querying - and so can only be used with pipelines containing both `text-embedder` and `vector-db` modules in succession.

Below we construct the simplest custom pipeline that satisfies this criteria - a standard vector search pipeline consisting of three modules: a `parser`, `text-embedder`, and `vector-db` index.


```python
# create custom pipeline object
pipeline = krixik.create_pipeline(
    name="vector-search-pipeline-check",
    module_chain=["parser", "text-embedder", "vector-db"],
)
```


```python
reset_pipeline(pipeline)
```

We can now perform any of the core system methods on our custom pipeline (e.g., [`process`](../system/process.md), [`list`](../system/list.md), etc.,).  Additionally we can invoke the [`semantic_search`](../system/semantic_search.md) method.

Lets first process a file with our new pipeline.  The `vector-db` module takes in a text file, and returns `faiss` vector database consisting of all non-trivial `(snippet, line_numbers)` tuples from the input.


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




    '{\n  "status_code": 200,\n  "pipeline": "vector-search-pipeline-check",\n  "request_id": "905f1a09-06c8-4c74-977b-2144a1f4f6a9",\n  "file_id": "04281f52-26db-431f-87c7-7675dd355c99",\n  "message": "SUCCESS - output fetched for file_id 04281f52-26db-431f-87c7-7675dd355c99.Output saved to location(s) listed in process_output_files.",\n  "warnings": [],\n  "process_output": null,\n  "process_output_files": [\n    "../../data/output/04281f52-26db-431f-87c7-7675dd355c99.faiss"\n  ]\n}'



Now we can query our text with natural language as shown below.


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
      "request_id": "dff05e88-1432-4760-9ab1-5ec9210b8f51",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "0ac060c7-c39b-4287-93f2-184335e5cdea",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_zgulrqdfmu.txt",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 2,
            "created_at": "2024-05-03 22:50:11",
            "last_updated": "2024-05-03 22:50:11"
          },
          "search_results": [
            {
              "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
              "line_numbers": [
                1
              ],
              "distance": 0.236
            },
            {
              "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
              "line_numbers": [
                2,
                3,
                4,
                5
              ],
              "distance": 0.429
            }
          ]
        }
      ]
    }

