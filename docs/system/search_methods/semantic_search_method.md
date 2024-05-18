## The `.semantic_search` Method

Krixik's `.semantic_search` method enables semantic search on documents processed through certain pipelines. Much has been written about semantic search, but in a nutshell, instead of searching a document for specific keywords, it searches for text similar in _meaning_ to the string that's been queried for. Contrast this to [keyword search](../system/search_methods/keyword_search_method.md).

Given that the `.semantic_search` method both [embeds](../modules/ai_model_modules/text-embedder_module.md) the query and performs the search, it can only be used with pipelines containing both a [`text-embedder`](../modules/ai_model_modules/text-embedder_module.md) module and a [`vector-db`](../modules/database_modules/vector-db_module.md) module in immediate succession.

This overview of the `.semantic_search` method is divided into the following sections:

- [.semantic_search Method Arguments](#.semantic_search-method-arguments)
- [Example Pipeline Setup and File Processing](#example-pipeline-setup-and-file-processing)
- [Example Semantic Searches](#example-semantic-searches)

### `.semantic_search` Method Arguments

The `.semantic_search` method takes one required argument and at least one of several optional arguments. The required argument is:

- `query` (str) - A string whose meaning will be searched for across the target document. The closest matches (i.e. snippets of text that most match the query in meaning) will be returned.

The optional arguments are the same arguments that the [`.list`](../system/file_system/list_method.md) method takes—both metadata and timestamp bookends—so please take a moment to [review them here](../system/file_system/list_method.md#.list-method-arguments). As with the [`.list`](../system/file_system/list_method.md) method, you can semantically search across several files at the same time because all metadata arguments are submitted to the `.semantic_search` method in list format. All optional argument elements are the same as for the [`.list`](../system/file_system/list_method.md) method, including the wildcard operator and the global root.

If none of these optional arguments is present, the `.semantic_search` method will not work because there will be nothing to search through.

Like the [`.list`](../system/file_system/list_method.md) method, the `.semantic_search` method also accepts the optional `max_files` and `sort_order` arguments, though their function changes a bit:

- `max_files` - Specifies up to how many files should be searched through. Default is none.

- `sort_order` - Here takes three possible values: 'ascending', descending', and now 'global'. The first two sort results by the file they're in (the files are sorted by the creation timestamp of the file), and 'global' combines all files and returns the very best results across all files. Default is 'descending'.

Finally, the `.semantic_search` method accepts one optional method that is unique to it:

- `k` (int) - Specifies up to how many results will be returned per queried file. Default is 5.

### Example Pipeline Setup and File Processing

For this document's examples we will use a pipeline consisting of three modules: a [`parser module`](../modules/ai_model_modules/parser_module.md), a [`text-embedder module`](../modules/modules/ai_model_modules/text-embedder_module.md), and a [`vector-db module`](../modules/database_modules/vector-db_module.md). This is the basic semantic search [pipeline](../examples/search_pipeline_examples/multi_basic_semantic_search.md). We use the [`create_pipeline`](../system/pipeline_creation/create_pipeline.md) method to instantiate the pipeline.


```python
# create the basic semantic search pipeline

pipeline_1 = krixik.create_pipeline(name="semantic_search_method_1_parser_text-embedder_vector-db",
                                    module_chain=["parser", "text-embedder", "vector-db"])
```

The pipeline ready, we'll [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) a few text files through it so we have something to search through. Let's use the same files we used in the [`.list` method documentation](../system/file_system/list_method.md).


```python
# add four files to the pipeline we just created.

output_1 = pipeline_1.process(local_file_path="../../data/input/Frankenstein.txt", # the initial local filepath where the input JSON file is stored
                              expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                              wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                              verbose=False,  # do not display process update printouts upon running code
                              symbolic_directory_path="/novels/gothic",
                              file_name="Frankenstein.txt")

output_2 = pipeline_1.process(local_file_path="../../data/input/Pride and Prejudice.txt", # the initial local filepath where the input JSON file is stored
                              expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                              wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                              verbose=False,  # do not display process update printouts upon running code
                              symbolic_directory_path="/novels/romance",
                              file_name="Pride and Prejudice.txt")

output_3 = pipeline_1.process(local_file_path="../../data/input/Moby Dick.txt", # the initial local filepath where the input JSON file is stored
                              expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                              wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                              verbose=False,  # do not display process update printouts upon running code
                              symbolic_directory_path="/novels/adventure",
                              file_name="Moby Dick.txt")

output_4 = pipeline_1.process(local_file_path="../../data/input/Little Women.txt", # the initial local filepath where the input JSON file is stored
                              expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                              wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                              verbose=False,  # do not display process update printouts upon running code
                              symbolic_directory_path="/novels/bildungsroman",
                              file_name="Little Women.txt")
```

Let's take a look at the output for one of these:


```python
# nicely print the output of one of the above processes

print(json.dumps(output_2, indent=2))
```

The value of `process_output` is `null` because the return object is a database, so it cannot be printed here. You can review this database in the local location provided in the `process_output_files`.

### Example Semantic Searches

With files now processed through the pipeline we can run the `.semantic_search` method on it.

Let's try an example in which we query one of the files file:


```python
# perform semantic_search over one file

semantic_output_1 = pipeline_1.semantic_search(query="It was cold night.",
                                               file_names=["Little Women.txt"])

# nicely print the output of this search

print(json.dumps(semantic_output_1, indent=2))
```

    {
      "status_code": 200,
      "request_id": "10503c1c-3959-4897-9315-a69438ecce2b",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "f69aac3d-e674-45d5-ab33-f16196ce82b2",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_awiouirlff.txt",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 2,
            "created_at": "2024-04-26 21:10:50",
            "last_updated": "2024-04-26 21:10:50"
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


In addition to returning the snippets that are closest in meaning to our query, we also see the calculated vector distance (in a way, the distance in meaning) between each result and the query. The shorter this distance is, the closer in meaning the result to the query. The `.semantic_search` method returns the snippets with the shortest vector distance to query, ranked in ascending order within each file.

When `sort_order` is set to 'global', results from all files are combined and the method returns the snippets with the shortest distance to query, ranked in ascending order, regardless of what file each result may be in. Let's give this a shot by searching through multiple files:


```python
# perform semantic_search over multiple files

semantic_output_2 = pipeline_1.semantic_search(query="It was cold night.",
                                               symbolic_directory_paths=["/novels*"],
                                               sort_order='global'
                                               k=4)

# nicely print the output of this search

print(json.dumps(semantic_output_2, indent=2))
```

    {
      "status_code": 200,
      "request_id": "10503c1c-3959-4897-9315-a69438ecce2b",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "f69aac3d-e674-45d5-ab33-f16196ce82b2",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_awiouirlff.txt",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 2,
            "created_at": "2024-04-26 21:10:50",
            "last_updated": "2024-04-26 21:10:50"
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


As you can see, results from all the files have been combined, and the result ranked at the top has the shortest query-result distance of the entire file set.
