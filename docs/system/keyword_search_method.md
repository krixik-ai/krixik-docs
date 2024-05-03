## the `.keyword_search` method

The `.keyword_search` method can be used with any pipeline that ends with `keyword-db` module.

A table of contents for this section is shown below.

- [a simple keyword search pipeline](#a-simple-keyword-db-pipeline)
- [invoking the `.keyword_search`  method](#invoking-the-keyword_search-method)

### a simple keyword search pipeline

Below we construct the simplest custom pipeline that satisfies this criteria - a pipeline consisting of the `keyword-db` module alone.


```python
# import custom module creation tools
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# instantiate module
module_1 = Module(module_type="keyword-db")

# create custom pipeline object
custom = CreatePipeline(name='keyword-db-pipeline-1', 
                        module_chain=[module_1])

# pass the custom object to the krixik operator (note you can also do this by passing its config)
pipeline = krixik.load_pipeline(pipeline=custom)
```

### invoking the `.keyword_search`  method 

We can now perform any of the core system methods on our custom pipeline (e.g., `.process`, `.list`, etc.,).  Additionally we can invoke the `keyword_search` method.

Lets first process a file with our new pipeline.  The `keyword-db` module takes in a text file, and returns `sqlite` keyword database consisting of all non-trivial `(keyword, line_number, token_number)` tuples from the input.


```python
import time

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
      "pipeline": "keyword-db-pipeline-1",
      "request_id": "d1a2cfe0-2d28-41ff-93bb-c262cc2bcab4",
      "file_id": "83279d22-2f50-48fd-8650-f8a58e7ce103",
      "message": "SUCCESS - output fetched for file_id 83279d22-2f50-48fd-8650-f8a58e7ce103.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "./83279d22-2f50-48fd-8650-f8a58e7ce103.db"
      ]
    }


Note that we did not define a `file_name` or `symbolic_directory_path` ourselves, so defaults will be given as described in the [`.process` walkthrough](process.md).

Here the `process_output` key value is `null` since the return object is a database.  We can see this database in the local location provided in the `process_output_files` value.

With `.process` complete we can run `keyword_search` on our input file. 

The `keyword_search` method takes in the exact same arguments as [the `.list` method](list.md) - that is `file_ids`, `file_names`, etc., - plus one additional argument: `query`.  

`keyword_search` takes in a input argument `query` containing desired keywords separated by spaces, and searches through your database(s) for these keywords as well as their lemmatized stems.

Let's look at an example.


```python
# perform keyword_search over the input file
keyword_output = pipeline.keyword_search(query="it was cold night",
                                         file_ids=[process_output["file_id"]])

# nicely print the output of this process
json_print(keyword_output)
```

    {
      "status_code": 200,
      "request_id": "98034dfa-eb3c-4950-b8b6-e205f5355531",
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
          "file_id": "83279d22-2f50-48fd-8650-f8a58e7ce103",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_pcirbljkok.txt",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_lines": 5,
            "created_at": "2024-04-26 21:10:22",
            "last_updated": "2024-04-26 21:10:22"
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


Here we can see one returned search result in `items`, as well as stop words removed from the input query shown in the return `warnings`.