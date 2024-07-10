<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/search_methods/keyword_search_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## The `keyword_search` Method

Krixik's `keyword_search` method enables keyword search on documents processed through certain pipelines. Keyword search is something internet users are long familiar with: a string of words is submitted as a query, and the search returns any and every instance of any of those words. Contrast this to [semantic search](semantic_search_method.md).

The `keyword_search` method can only be used with pipelines ending with the [`keyword-db`](../../modules/database_modules/keyword-db_module.md) module.

This overview of the `keyword_search` method is divided into the following sections:

- [keyword_search Method Arguments](#keyword_search-method-arguments)
- [Example Pipeline Setup and File Processing](#example-pipeline-setup-and-file-processing)
- [Example Keyword Searches](#example-keyword-searches)
- [Output Size Cap](#output-size-cap)
- [Stop Words](#stop-words)

### `keyword_search` Method Arguments

The `keyword_search` method takes one required argument and at least one of several optional arguments. The required argument is:

- `query` (str) - A string that contains one or more keywords separated by spaces or hyphens that will be individually searched for across the target document.

The optional arguments are the same arguments that the [`list`](../file_system/list_method.md) method takes—both metadata and timestamp bookends—so please take a moment to [review them here](../file_system/list_method.md). As with the [`list`](../file_system/list_method.md) method, you can `keyword_search` across several files at the same time because all metadata arguments are submitted to the `keyword_search` method in list format. All optional argument elements are the same as for the [`list`](../file_system/list_method.md) method, including the wildcard operator and the global root.

If none of these optional arguments is present, the `keyword_search` method will not work because there will be nothing to search through.

Like the [`list`](../file_system/list_method.md) method, the `keyword_search` method also accepts the optional `max_files` and `sort_order` arguments, though their function changes a bit:

- `max_files` specifies up to how many files should be searched through.

- `sort_order` here takes two possible values: 'ascending' and descending'. This determines what order searched-through files are returned in (in terms of their creation timestamp), but keyword results within each file are displayed in order of appearance. Default is 'descending'.

### Example Pipeline Setup and File Processing

For this document's examples we will use a pipeline consisting of a single [`keyword-db`](../../modules/database_modules/keyword-db_module.md) module. This is the basic keyword search pipeline. We use the [`.create_pipeline`](../pipeline_creation/create_pipeline.md) method to instantiate the pipeline.


```python
# create the basic keyword search pipeline
pipeline = krixik.create_pipeline(name="keyword_search_method_1_keyword-db", module_chain=["keyword-db"])
```

The pipeline ready, we'll [`process`](../parameters_processing_files_through_pipelines/process_method.md) a few text files through it so we have something to search across. Let's use the same files we used in the [`list` method documentation](../file_system/list_method.md).


```python
# add four files to the pipeline we just created.
output_1 = pipeline.process(
    local_file_path=data_dir + "input/frankenstein_very_short.txt",  # the initial local filepath where the input JSON file is stored
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
    verbose=False,  # do not display process update printouts upon running code
    symbolic_directory_path="/novels/gothic",
    file_name="Frankenstein.txt",
)

output_2 = pipeline.process(
    local_file_path=data_dir + "input/pride_and_prejudice_very_short.txt",  # the initial local filepath where the input JSON file is stored
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
    verbose=False,  # do not display process update printouts upon running code
    symbolic_directory_path="/novels/romance",
    file_name="Pride and Prejudice.txt",
)

output_3 = pipeline.process(
    local_file_path=data_dir + "input/moby_dick_very_short.txt",  # the initial local filepath where the input JSON file is stored
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
    verbose=False,  # do not display process update printouts upon running code
    symbolic_directory_path="/novels/adventure",
    file_name="Moby Dick.txt",
)

output_4 = pipeline.process(
    local_file_path=data_dir + "input/little_women_very_short.txt",  # the initial local filepath where the input JSON file is stored
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
    verbose=False,  # do not display process update printouts upon running code
    symbolic_directory_path="/novels/bildungsroman",
    file_name="Little Women.txt",
)
```

Let's take a look at the output for one of these:


```python
# nicely print the output of one of the above processes
print(json.dumps(output_3, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "keyword_search_method_1_keyword-db",
      "request_id": "4763d881-46e0-4d34-857b-bdd4cdf43aab",
      "file_id": "ae071414-7192-4f78-a431-1a13c0f0bc4a",
      "message": "SUCCESS - output fetched for file_id ae071414-7192-4f78-a431-1a13c0f0bc4a.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/ae071414-7192-4f78-a431-1a13c0f0bc4a.db"
      ]
    }


The value of `process_output` is `null` because the return object is an `SQLite` keyword database—one consisting of all non-trivial `(keyword, line_number, word_number)` tuples identified in the input file—so it cannot be printed here. You can review this database in the local location provided in `process_output_files`.

### Example Keyword Searches

With files now processed through the pipeline we can run the `keyword_search` method on it.

Let's try an example in which we search through one file:


```python
# perform keyword_search over one file
keyword_output = pipeline.keyword_search(query="mansion adolescence party enemy romance", file_names=["Little Women.txt"])

# nicely print the output of this search
print(json.dumps(keyword_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "5b252162-6ee5-4a48-ae62-f9954f4107f5",
      "message": "",
      "warnings": [
        {
          "WARNING: the following file_ids returned no results for the given query": [
            "001dd7c5-87f6-4ffa-a647-060291d9679d"
          ]
        }
      ],
      "items": []
    }


The `keyword_search` method returns each appearance of each searched-for keyword. As you can see, for every searched-through file there is an entry for every keyword appearance. The entry indicates both line number and the word number within that line.

It works just as well when searching through several files by using the [wildcard operator](../file_system/list_method.md#wildcard-operator-arguments):


```python
# perform keyword_search over multiple files
keyword_output = pipeline.keyword_search(query="mansion adolescence party enemy romance", symbolic_directory_paths=["/novels*"])

# nicely print the output of this search
print(json.dumps(keyword_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "5e53f349-ed65-4735-a288-d2effbb447a5",
      "message": "Successfully queried the first 1 user file out of 4 defined by input query arguments.",
      "warnings": [
        {
          "WARNING: the following file_ids returned no results for the given query": [
            "ae071414-7192-4f78-a431-1a13c0f0bc4a",
            "f59be5e9-2bd3-4a07-8a7e-1a52064c6ee1",
            "001dd7c5-87f6-4ffa-a647-060291d9679d"
          ]
        }
      ],
      "items": [
        {
          "file_id": "786baed5-66ff-4bf4-941f-0baa562e9666",
          "file_metadata": {
            "file_name": "pride and prejudice.txt",
            "symbolic_directory_path": "/novels/romance",
            "file_tags": [],
            "num_lines": 40,
            "created_at": "2024-06-05 16:18:15",
            "last_updated": "2024-06-05 16:18:15"
          },
          "search_results": [
            {
              "keyword": "party",
              "line_number": 23,
              "keyword_number": 8
            }
          ]
        }
      ]
    }


### Output Size Cap

The current size limit on output generated by the `keyword_search` method is 5MB.

### Stop Words

'Stop words' are the words that are ignored by keyword search. There are words in the English language that are so common and so often used (e.g. "the", "and") that we assume that they will not be searched for. Consequently, the `keyword_search` method skips them if they are in the query, making for more focused results. There is at present no way to keyword search for any word in the stop words list, which you can review here:.


```python
with open(data_dir + "other/stop_words.txt", "r") as file:
    print(file.read())
```

    stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

