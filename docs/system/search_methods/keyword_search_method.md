## The `.keyword_search` Method

Krixik's `.keyword_search` method enables keyword search on documents processed through certain pipelines. Keyword search is something internet users are long familiar with: a string of words is submitted as a query, and the search returns any and every instance of any of those words. Contrast this to [semantic search](../system/search_methods/semantic_search_method.md).

The `.keyword_search` method can only be used with pipelines ending with the [`keyword-db`](../modules/database_modules/keyword-db_module.md) module.

This overview of the `.keyword_search` method is divided into the following sections:

- [.keyword_search Method Arguments](#.keyword_search-method-arguments)
- [Example Pipeline Setup and File Processing](#example-pipeline-setup-and-file-processing)
- [Example Keyword Searches](#example-keyword-searches)
- [Stop Words](#stop-words)

### `.keyword_search` Method Arguments

The `.keyword_search` method takes one required argument and at least one of several optional arguments. The required argument is:

- `query` (str) - A string that contains one or more keywords separated by spaces that will be individually searched for across the target document.

The optional arguments are the same arguments that the [`.list`](../system/file_system/list_method.md) method takes—both metadata and timestamp bookends—so please take a moment to [review them here](../system/file_system/list_method.md). As with the [`.list`](../system/file_system/list_method.md) method, you can `.keyword_search` across several files at the same time because all metadata arguments are submitted to the `.keyword_search` method in list format. All optional argument elements are the same as for the [`.list`](../system/file_system/list_method.md) method, including the wildcard operator and the global root.

If none of these optional arguments is present, the `.keyword_search` method will not work because there will be nothing to search through.

Like the [`.list`](../system/file_system/list_method.md) method, the `.keyword_search` method also accepts the optional `max_files` and `sort_order` arguments, though their function changes a bit:

- `max_files` specifies up to how many files should be searched through.

- `sort_order` here takes two possible values: 'ascending' and descending'. This determines what order searched-through files are returned in (in terms of their creation timestamp), but keyword results within each file are displayed in order of appearance. Default is 'descending'.

### Example Pipeline Setup and File Processing

For this document's examples we will use a pipeline consisting of a single [`keyword-db`](../modules/database_modules/keyword-db_module.md) module. This is the basic keyword search pipeline. We use the [`.create_pipeline`](../system/pipeline_creation/create_pipeline.md) method to instantiate the pipeline.


```python
# create the basic keyword search pipeline

pipeline_1 = krixik.create_pipeline(name="keyword_search_method_1_keyword-db",
                                    module_chain=["keyword-db"])
```

The pipeline ready, we'll [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) a few text files through it so we have something to search across. Let's use the same files we used in the [`.list` method documentation](../system/file_system/list_method.md).


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

print(json.dumps(output_3, indent=2))
```

The value of `process_output` is `null` because the return object is an `SQLite` keyword database—one consisting of all non-trivial `(keyword, line_number, word_number)` tuples identified in the input file—so it cannot be printed here. You can review this database in the local location provided in `process_output_files`.

### Example Keyword Searches

With files now processed through the pipeline we can run the `.keyword_search` method on it.

Let's try an example in which we search through one file:


```python
# perform keyword_search over one file

keyword_output_1 = pipeline_1.keyword_search(query="mansion adolescence party enemy romance",
                                             file_names=["Little Women.txt"])

# nicely print the output of this search

print(json.dumps(keyword_output_1, indent=2))
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


The `.keyword_search` method returns each appearance of each searched-for keyword. As you can see, for every searched-through file there is an entry for every keyword appearance. The entry indicates both line number and the word number within that line.

It works just as well when searching through several files:


```python
# perform keyword_search over multiple files

keyword_output_2 = pipeline_1.keyword_search(query="mansion adolescence party enemy romance",
                                             symbolic_directory_paths=["/novels*"])

# nicely print the output of this search

print(json.dumps(keyword_output_2, indent=2))
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


### Stop Words

'Stop words' are the words that are ignored by keyword search. There are words in the English language that are so common and so often used (e.g. "the", "and") that we assume that they will not be searched for. Consequently, the `.keyword_search` method skips them if they are in the query, making for more focused results. There is at present no way to keyword search for any word in the stop words list, which you can review [here](../../../data/other_data/stop_words.txt).
