## the `.semantic_search` method

krixik's `vector_search` method is a convenience function for both embedding and querying - and so can be used with pipelines containing both `text-embedder` and `vector-db` modules in succession.

A table of contents for this section is shown below.

- [a simple vector search pipeline](#a-simple-vector-db-pipeline)
- [invoking the `.semantic_search`  method](#invoking-the-vector_search-method)


### a simple vector search pipeline

Below we construct the simplest custom pipeline that satisfies this criteria - a standard vector search pipeline consisting of three modules: a `parser`, `text-embedder`, and `vector-db` index.

```python
# import custom module creation tools
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# instantiate module
module_1 = Module(module_type="parser")
module_2 = Module(module_type="text-embedder")
module_3 = Module(module_type="vector-db")

# create custom pipeline object
custom = CreatePipeline(name='vector-db-pipeline-1', 
                        module_chain=[module_1, module_2, module_3])

# pass the custom object to the krixik operator (note you can also do this by passing its config)
pipeline = krixik.load_pipeline(pipeline=custom)
```

### invoking the `.semantic_search`  method

We can now perform any of the core system methods on our custom pipeline (e.g., `.process`, `.list`, etc.,).  Additionally we can invoke the `vector_search` method.

Lets first process a file with our new pipeline.  The `vector-db` module takes in a text file, and returns `faiss` vector database consisting of all non-trivial `(snippet, line_numbers)` tuples from the input.


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
      "pipeline": "vector-db-pipeline-1",
      "request_id": "1a09068c-872a-4389-a399-7281e2d1764e",
      "file_id": "f69aac3d-e674-45d5-ab33-f16196ce82b2",
      "message": "SUCCESS - output fetched for file_id f69aac3d-e674-45d5-ab33-f16196ce82b2.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "./f69aac3d-e674-45d5-ab33-f16196ce82b2.faiss"
      ]
    }


Note that we did not define a `file_name` or `symbolic_directory_path` ourselves, so defaults will be given as described in the [`.process`](process.md) walkthrough.

Here the `process_output` key value is `null` since the return object is a database.  We can see this database in the local location provided in the `process_output_files` value.

With `.process` complete we can run `vector_search` on our input file. 

The `vector_search` method takes in the exact same arguments as [`.list`](list.md) - that is `file_ids`, `file_names`, etc., - plus one additional argument: `query`.  The `query` is a string of words to be queried individually.

Let's look at an example.


```python
# perform vector_search over the input file
vector_output = pipeline.semantic_search(query="it was cold night",
                                        file_ids=[process_output["file_id"]])

# nicely print the output of this process
json_print(vector_output)
```

Here we can see one returned search result in `items`.
