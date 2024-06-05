<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/single_module_pipelines/single_vector-db.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Single-Module Pipeline: `vector-db`

This document is a walkthrough of how to assemble and use a single-module pipeline that only includes a [`vector-db`](../../modules/database_modules/vector-db_module.md) module.

Note that this module by itself will not generate a particularly easy-to-use pipeline, since you must already have NPY files ready to process. We suggest also taking a look at this [example pipeline](../../examples/search_pipeline_examples/multi_basic_semantic_search.md) or this [example pipeline](../../examples/search_pipeline_examples/multi_snippet_semantic_search.md), which respectively take TXT files and JSON files and enable vector (a.k.a. semantic) search on them.

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Required Input Format](#required-input-format)
- [Using the Default Model](#using-the-default-model)
- [Using the `semantic_search` Method](#using-the-semantic_search-method)
- [Querying Output Databases Locally](#querying-output-databases-locally)

### Pipeline Setup

Let's first instantiate a single-module [`vector-db`](../../modules/database_modules/vector-db_module.md) pipeline.

We use the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method for this, passing only the [`vector-db`](../../modules/database_modules/vector-db_module.md) module name into `module_chain`.


```python
# create a pipeline with a single vector-db module
pipeline = krixik.create_pipeline(name="modules-vector-db-docs", module_chain=["vector-db"])
```

### Required Input Format

The [`vector-db`](../../modules/database_modules/vector-db_module.md) module accepts NPY file inputs consisting of single NumPy arrays. Each row in the array is a vector that the [`vector-db`](../../modules/database_modules/vector-db_module.md) module then indexes for vector search.

Let's take a quick look at a valid input file, and then process it:


```python
# examine contents of input file
import numpy as np

np.load(data_dir + "input/vectors.npy")
```




    array([[0, 1],
           [1, 0],
           [1, 1]])



### Using the Default Model

Let's process our test input file using the [`vector-db`](../../modules/database_modules/vector-db_module.md) module's default (and currently only) [model](../../modules/database_modules/vector-db_module.md#available-models-in-the-vector-db-module): [`faiss`](https://github.com/facebookresearch/faiss).

Given that this is the default model, we need not specify model selection through the optional [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file with the default model
process_output = pipeline.process(
    local_file_path=data_dir + "input/vectors.npy",  # the initial local filepath where the input file is stored
    local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # wait for process to complete before returning IDE control to user
    verbose=False,
)  # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a [FAISS](https://github.com/facebookresearch/faiss) database file, `process_output` is "null". However, the output file has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "modules-vector-db-docs",
      "request_id": "536c9e0b-41ed-4c41-99dc-11cdabf32ecc",
      "file_id": "63c88fdc-8b62-4f74-af20-c4816ee0bb88",
      "message": "SUCCESS - output fetched for file_id 63c88fdc-8b62-4f74-af20-c4816ee0bb88.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/63c88fdc-8b62-4f74-af20-c4816ee0bb88.faiss"
      ]
    }


### Using the `semantic_search` method

Any pipeline containing a [`vector-db`](../../modules/database_modules/vector-db_module.md) module preceded by a [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) module has access to the [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method. This provides you with the convenient ability to effect semantic queries on the created vector database(s).

As the single-module pipeline created above lacks the [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) module, the [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method will not work on it. Review documentation for this [pipeline example](../../examples/search_pipeline_examples/multi_basic_semantic_search.md) or this [pipeline example](../../examples/search_pipeline_examples/multi_snippet_semantic_search.md), both of which meet the requirements for the method: the former ingests TXT files, and the latter JSON files.

### Querying Output Databases Locally

In addition to what's provided by the [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method, you can **locally** perform queries on the generated vector database whose location is indicated in `process_output_files`.

Below is a simple function for locally performing vector searches on the above-outputted database.

Note: In order to execute this code you will need to install the `FAISS` library. Depending on the specs of your local setup, install [faiss-cpu](https://pypi.org/project/faiss-cpu/) or [faiss-gpu](https://pypi.org/project/faiss-gpu/).


```python
# make sure that you've installed faiss (faiss-cpu or faiss-gpu)
!pip install faiss-cpu
import faiss
import numpy as np
from typing import Tuple


def query_vector_db(query_vector: np.ndarray, k: int, db_file_path: str) -> Tuple[list, list]:
    # read in vector db
    faiss_index = faiss.read_index(db_file_path)

    # perform query
    similarities, indices = faiss_index.search(query_vector, k)
    distances = 1 - similarities
    return distances, indices
```

    Requirement already satisfied: faiss-cpu in /Users/jeremywatt/Desktop/krixik/code/krixik-docs/docs_venv/lib/python3.10/site-packages (1.8.0)
    Requirement already satisfied: numpy in /Users/jeremywatt/Desktop/krixik/code/krixik-docs/docs_venv/lib/python3.10/site-packages (from faiss-cpu) (1.26.4)
    
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip is available: [0m[31;49m23.3.1[0m[39;49m -> [0m[32;49m24.0[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m


Now query your database using a small sample array with the function above. The results are printed below:


```python
# perform test query using the above query function
original_vectors = np.load(data_dir + "input/vectors.npy")
query_vector = np.array([[0, 1]])
distances, indices = query_vector_db(query_vector, 2, process_output["process_output_files"][0])
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

