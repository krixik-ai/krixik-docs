## The `.keyword_search` Method

Krixik's `.keyword_search` method enables keyword search on documents processed through certain pipelines. Keyword search is something internet users are long familiar with: a string of words is submitted as a query, and the search returns any and every instance of any of those words. Contrast this to [semantic search](semantic_search_method.md).

The `.keyword_search` method can only be used with pipelines ending with the [`keyword-db`](../../modules/database_modules/keyword-db_module.md) module.

This overview of the `.keyword_search` method is divided into the following sections:

- [.keyword_search Method Arguments](#.keyword_search-method-arguments)
- [Example Pipeline Setup and File Processing](#example-pipeline-setup-and-file-processing)
- [Example Keyword Searches](#example-keyword-searches)
- [Output Size Cap](#output-size-cap)
- [Stop Words](#stop-words)

### `.keyword_search` Method Arguments

The `.keyword_search` method takes one required argument and at least one of several optional arguments. The required argument is:

- `query` (str) - A string that contains one or more keywords separated by spaces or hyphens that will be individually searched for across the target document.

The optional arguments are the same arguments that the [`.list`](../file_system/list_method.md) method takes—both metadata and timestamp bookends—so please take a moment to [review them here](../file_system/list_method.md). As with the [`.list`](../file_system/list_method.md) method, you can `.keyword_search` across several files at the same time because all metadata arguments are submitted to the `.keyword_search` method in list format. All optional argument elements are the same as for the [`.list`](../file_system/list_method.md) method, including the wildcard operator and the global root.

If none of these optional arguments is present, the `.keyword_search` method will not work because there will be nothing to search through.

Like the [`.list`](../file_system/list_method.md) method, the `.keyword_search` method also accepts the optional `max_files` and `sort_order` arguments, though their function changes a bit:

- `max_files` specifies up to how many files should be searched through.

- `sort_order` here takes two possible values: 'ascending' and descending'. This determines what order searched-through files are returned in (in terms of their creation timestamp), but keyword results within each file are displayed in order of appearance. Default is 'descending'.

### Example Pipeline Setup and File Processing

For this document's examples we will use a pipeline consisting of a single [`keyword-db`](../../modules/database_modules/keyword-db_module.md) module. This is the basic keyword search pipeline. We use the [`.create_pipeline`](../pipeline_creation/create_pipeline.md) method to instantiate the pipeline.


```python
# create the basic keyword search pipeline

pipeline_1 = krixik.create_pipeline(name="keyword_search_method_1_keyword-db",
                                    module_chain=["keyword-db"])
```

The pipeline ready, we'll [`.process`](../parameters_processing_files_through_pipelines/process_method.md) a few text files through it so we have something to search across. Let's use the same files we used in the [`.list` method documentation](../file_system/list_method.md).


```python
# add four files to the pipeline we just created.

output_1 = pipeline_1.process(local_file_path="../../../data/input/Frankenstein partial.txt", # the initial local filepath where the input JSON file is stored
                              expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                              wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                              verbose=False,  # do not display process update printouts upon running code
                              symbolic_directory_path="/novels/gothic",
                              file_name="Frankenstein.txt")

output_2 = pipeline_1.process(local_file_path="../../../data/input/Pride and Prejudice partial.txt", # the initial local filepath where the input JSON file is stored
                              expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                              wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                              verbose=False,  # do not display process update printouts upon running code
                              symbolic_directory_path="/novels/romance",
                              file_name="Pride and Prejudice.txt")

output_3 = pipeline_1.process(local_file_path="../../../data/input/Moby Dick partial.txt", # the initial local filepath where the input JSON file is stored
                              expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                              wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                              verbose=False,  # do not display process update printouts upon running code
                              symbolic_directory_path="/novels/adventure",
                              file_name="Moby Dick.txt")

output_4 = pipeline_1.process(local_file_path="../../../data/input/Little Women partial.txt", # the initial local filepath where the input JSON file is stored
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

    {
      "status_code": 200,
      "pipeline": "keyword_search_method_1_keyword-db",
      "request_id": "3146ca1a-95db-43a3-9378-425939a8cfc6",
      "file_id": "850e00f2-58d6-4d04-a1ae-b8770bfef2a6",
      "message": "SUCCESS - output fetched for file_id 850e00f2-58d6-4d04-a1ae-b8770bfef2a6.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "c:\\Users\\Lucas\\Desktop\\krixikdocsnoodle\\docs\\system\\search_methods/850e00f2-58d6-4d04-a1ae-b8770bfef2a6.db"
      ]
    }


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
      "request_id": "bf66a03f-e9be-4e27-afb3-322fb142972d",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "77a68f9d-d447-4972-9e19-2e2a8045b655",
          "file_metadata": {
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_lines": 5285,
            "created_at": "2024-05-20 18:56:31",
            "last_updated": "2024-05-20 18:56:31"
          },
          "search_results": [
            {
              "keyword": "party",
              "line_number": 281,
              "keyword_number": 4
            },
            {
              "keyword": "enemies",
              "line_number": 1010,
              "keyword_number": 4
            },
            {
              "keyword": "romance",
              "line_number": 1089,
              "keyword_number": 7
            },
            {
              "keyword": "party",
              "line_number": 1271,
              "keyword_number": 7
            },
            {
              "keyword": "party",
              "line_number": 1491,
              "keyword_number": 4
            },
            {
              "keyword": "party",
              "line_number": 1535,
              "keyword_number": 10
            },
            {
              "keyword": "party",
              "line_number": 1553,
              "keyword_number": 11
            },
            {
              "keyword": "party",
              "line_number": 1669,
              "keyword_number": 8
            },
            {
              "keyword": "parties",
              "line_number": 1755,
              "keyword_number": 13
            },
            {
              "keyword": "party",
              "line_number": 2037,
              "keyword_number": 12
            },
            {
              "keyword": "party",
              "line_number": 2041,
              "keyword_number": 5
            },
            {
              "keyword": "party",
              "line_number": 2069,
              "keyword_number": 4
            },
            {
              "keyword": "party",
              "line_number": 2069,
              "keyword_number": 8
            },
            {
              "keyword": "party",
              "line_number": 2076,
              "keyword_number": 3
            },
            {
              "keyword": "party",
              "line_number": 2085,
              "keyword_number": 5
            },
            {
              "keyword": "party",
              "line_number": 2098,
              "keyword_number": 6
            },
            {
              "keyword": "parties",
              "line_number": 2106,
              "keyword_number": 13
            },
            {
              "keyword": "parties",
              "line_number": 2226,
              "keyword_number": 7
            },
            {
              "keyword": "romance",
              "line_number": 2264,
              "keyword_number": 8
            },
            {
              "keyword": "romance",
              "line_number": 2551,
              "keyword_number": 11
            },
            {
              "keyword": "mansion",
              "line_number": 2603,
              "keyword_number": 11
            },
            {
              "keyword": "party",
              "line_number": 2615,
              "keyword_number": 4
            },
            {
              "keyword": "party",
              "line_number": 2623,
              "keyword_number": 5
            },
            {
              "keyword": "party",
              "line_number": 3078,
              "keyword_number": 6
            },
            {
              "keyword": "parties",
              "line_number": 3159,
              "keyword_number": 9
            },
            {
              "keyword": "mansion",
              "line_number": 3167,
              "keyword_number": 6
            },
            {
              "keyword": "party",
              "line_number": 3480,
              "keyword_number": 10
            },
            {
              "keyword": "enemies",
              "line_number": 3600,
              "keyword_number": 1
            },
            {
              "keyword": "party",
              "line_number": 3792,
              "keyword_number": 13
            },
            {
              "keyword": "enemy",
              "line_number": 3814,
              "keyword_number": 5
            },
            {
              "keyword": "enemy",
              "line_number": 4122,
              "keyword_number": 4
            },
            {
              "keyword": "party",
              "line_number": 4243,
              "keyword_number": 10
            },
            {
              "keyword": "party",
              "line_number": 4247,
              "keyword_number": 10
            },
            {
              "keyword": "party",
              "line_number": 4328,
              "keyword_number": 7
            },
            {
              "keyword": "party",
              "line_number": 4557,
              "keyword_number": 3
            },
            {
              "keyword": "party",
              "line_number": 4583,
              "keyword_number": 10
            },
            {
              "keyword": "party",
              "line_number": 4586,
              "keyword_number": 5
            },
            {
              "keyword": "party",
              "line_number": 4720,
              "keyword_number": 5
            },
            {
              "keyword": "party",
              "line_number": 5077,
              "keyword_number": 7
            }
          ]
        }
      ]
    }


The `.keyword_search` method returns each appearance of each searched-for keyword. As you can see, for every searched-through file there is an entry for every keyword appearance. The entry indicates both line number and the word number within that line.

It works just as well when searching through several files by using the [wildcard operator](../file_system/list_method.md#wildcard-operator-arguments):


```python
# perform keyword_search over multiple files

keyword_output_2 = pipeline_1.keyword_search(query="mansion adolescence party enemy romance",
                                             symbolic_directory_paths=["/novels*"])

# nicely print the output of this search

print(json.dumps(keyword_output_2, indent=2))
```

    {
      "status_code": 200,
      "request_id": "d6c04489-81ca-46e2-9b76-092193938d4e",
      "message": "Successfully queried 4 user files.",
      "warnings": [],
      "items": [
        {
          "file_id": "77a68f9d-d447-4972-9e19-2e2a8045b655",
          "file_metadata": {
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_lines": 5285,
            "created_at": "2024-05-20 18:56:31",
            "last_updated": "2024-05-20 18:56:31"
          },
          "search_results": [
            {
              "keyword": "party",
              "line_number": 281,
              "keyword_number": 4
            },
            {
              "keyword": "enemies",
              "line_number": 1010,
              "keyword_number": 4
            },
            {
              "keyword": "romance",
              "line_number": 1089,
              "keyword_number": 7
            },
            {
              "keyword": "party",
              "line_number": 1271,
              "keyword_number": 7
            },
            {
              "keyword": "party",
              "line_number": 1491,
              "keyword_number": 4
            },
            {
              "keyword": "party",
              "line_number": 1535,
              "keyword_number": 10
            },
            {
              "keyword": "party",
              "line_number": 1553,
              "keyword_number": 11
            },
            {
              "keyword": "party",
              "line_number": 1669,
              "keyword_number": 8
            },
            {
              "keyword": "parties",
              "line_number": 1755,
              "keyword_number": 13
            },
            {
              "keyword": "party",
              "line_number": 2037,
              "keyword_number": 12
            },
            {
              "keyword": "party",
              "line_number": 2041,
              "keyword_number": 5
            },
            {
              "keyword": "party",
              "line_number": 2069,
              "keyword_number": 4
            },
            {
              "keyword": "party",
              "line_number": 2069,
              "keyword_number": 8
            },
            {
              "keyword": "party",
              "line_number": 2076,
              "keyword_number": 3
            },
            {
              "keyword": "party",
              "line_number": 2085,
              "keyword_number": 5
            },
            {
              "keyword": "party",
              "line_number": 2098,
              "keyword_number": 6
            },
            {
              "keyword": "parties",
              "line_number": 2106,
              "keyword_number": 13
            },
            {
              "keyword": "parties",
              "line_number": 2226,
              "keyword_number": 7
            },
            {
              "keyword": "romance",
              "line_number": 2264,
              "keyword_number": 8
            },
            {
              "keyword": "romance",
              "line_number": 2551,
              "keyword_number": 11
            },
            {
              "keyword": "mansion",
              "line_number": 2603,
              "keyword_number": 11
            },
            {
              "keyword": "party",
              "line_number": 2615,
              "keyword_number": 4
            },
            {
              "keyword": "party",
              "line_number": 2623,
              "keyword_number": 5
            },
            {
              "keyword": "party",
              "line_number": 3078,
              "keyword_number": 6
            },
            {
              "keyword": "parties",
              "line_number": 3159,
              "keyword_number": 9
            },
            {
              "keyword": "mansion",
              "line_number": 3167,
              "keyword_number": 6
            },
            {
              "keyword": "party",
              "line_number": 3480,
              "keyword_number": 10
            },
            {
              "keyword": "enemies",
              "line_number": 3600,
              "keyword_number": 1
            },
            {
              "keyword": "party",
              "line_number": 3792,
              "keyword_number": 13
            },
            {
              "keyword": "enemy",
              "line_number": 3814,
              "keyword_number": 5
            },
            {
              "keyword": "enemy",
              "line_number": 4122,
              "keyword_number": 4
            },
            {
              "keyword": "party",
              "line_number": 4243,
              "keyword_number": 10
            },
            {
              "keyword": "party",
              "line_number": 4247,
              "keyword_number": 10
            },
            {
              "keyword": "party",
              "line_number": 4328,
              "keyword_number": 7
            },
            {
              "keyword": "party",
              "line_number": 4557,
              "keyword_number": 3
            },
            {
              "keyword": "party",
              "line_number": 4583,
              "keyword_number": 10
            },
            {
              "keyword": "party",
              "line_number": 4586,
              "keyword_number": 5
            },
            {
              "keyword": "party",
              "line_number": 4720,
              "keyword_number": 5
            },
            {
              "keyword": "party",
              "line_number": 5077,
              "keyword_number": 7
            }
          ]
        },
        {
          "file_id": "850e00f2-58d6-4d04-a1ae-b8770bfef2a6",
          "file_metadata": {
            "file_name": "moby dick.txt",
            "symbolic_directory_path": "/novels/adventure",
            "file_tags": [],
            "num_lines": 4412,
            "created_at": "2024-05-20 18:56:20",
            "last_updated": "2024-05-20 18:56:20"
          },
          "search_results": [
            {
              "keyword": "enemies",
              "line_number": 661,
              "keyword_number": 2
            },
            {
              "keyword": "mansion",
              "line_number": 2027,
              "keyword_number": 1
            },
            {
              "keyword": "enemies",
              "line_number": 3290,
              "keyword_number": 4
            },
            {
              "keyword": "party",
              "line_number": 3611,
              "keyword_number": 5
            },
            {
              "keyword": "enemy",
              "line_number": 3980,
              "keyword_number": 5
            }
          ]
        },
        {
          "file_id": "3072ed65-1ec8-44a8-b691-2f1cf2c3a693",
          "file_metadata": {
            "file_name": "pride and prejudice.txt",
            "symbolic_directory_path": "/novels/romance",
            "file_tags": [],
            "num_lines": 2812,
            "created_at": "2024-05-20 18:56:08",
            "last_updated": "2024-05-20 18:56:08"
          },
          "search_results": [
            {
              "keyword": "party",
              "line_number": 23,
              "keyword_number": 8
            },
            {
              "keyword": "party",
              "line_number": 414,
              "keyword_number": 3
            },
            {
              "keyword": "party",
              "line_number": 665,
              "keyword_number": 1
            },
            {
              "keyword": "party",
              "line_number": 874,
              "keyword_number": 4
            },
            {
              "keyword": "party",
              "line_number": 902,
              "keyword_number": 3
            },
            {
              "keyword": "party",
              "line_number": 906,
              "keyword_number": 10
            },
            {
              "keyword": "party",
              "line_number": 911,
              "keyword_number": 10
            },
            {
              "keyword": "party",
              "line_number": 938,
              "keyword_number": 12
            },
            {
              "keyword": "party",
              "line_number": 993,
              "keyword_number": 1
            },
            {
              "keyword": "parties",
              "line_number": 1349,
              "keyword_number": 8
            },
            {
              "keyword": "parties",
              "line_number": 1378,
              "keyword_number": 5
            },
            {
              "keyword": "party",
              "line_number": 1407,
              "keyword_number": 13
            },
            {
              "keyword": "party",
              "line_number": 1855,
              "keyword_number": 10
            },
            {
              "keyword": "party",
              "line_number": 1937,
              "keyword_number": 1
            },
            {
              "keyword": "party",
              "line_number": 2309,
              "keyword_number": 2
            },
            {
              "keyword": "parties",
              "line_number": 2454,
              "keyword_number": 3
            },
            {
              "keyword": "party",
              "line_number": 2572,
              "keyword_number": 9
            },
            {
              "keyword": "party",
              "line_number": 2629,
              "keyword_number": 5
            },
            {
              "keyword": "party",
              "line_number": 2655,
              "keyword_number": 6
            },
            {
              "keyword": "party",
              "line_number": 2687,
              "keyword_number": 6
            }
          ]
        },
        {
          "file_id": "e855e0df-d8ca-40d4-8dd2-e302c9ed494d",
          "file_metadata": {
            "file_name": "frankenstein.txt",
            "symbolic_directory_path": "/novels/gothic",
            "file_tags": [],
            "num_lines": 4245,
            "created_at": "2024-05-20 18:55:44",
            "last_updated": "2024-05-20 18:55:44"
          },
          "search_results": [
            {
              "keyword": "romance",
              "line_number": 850,
              "keyword_number": 13
            },
            {
              "keyword": "party",
              "line_number": 908,
              "keyword_number": 3
            },
            {
              "keyword": "enemy",
              "line_number": 1223,
              "keyword_number": 6
            },
            {
              "keyword": "enemy",
              "line_number": 1671,
              "keyword_number": 13
            },
            {
              "keyword": "enemy",
              "line_number": 1966,
              "keyword_number": 4
            },
            {
              "keyword": "enemies",
              "line_number": 2094,
              "keyword_number": 5
            },
            {
              "keyword": "enemy",
              "line_number": 2480,
              "keyword_number": 1
            },
            {
              "keyword": "enemies",
              "line_number": 2586,
              "keyword_number": 4
            },
            {
              "keyword": "enemies",
              "line_number": 2590,
              "keyword_number": 11
            },
            {
              "keyword": "enemies",
              "line_number": 2618,
              "keyword_number": 4
            },
            {
              "keyword": "enemies",
              "line_number": 3060,
              "keyword_number": 5
            },
            {
              "keyword": "enemies",
              "line_number": 3075,
              "keyword_number": 5
            }
          ]
        }
      ]
    }


### Output Size Cap

The current size limit on output generated by the `.keyword_search` method is 5MB.

### Stop Words

'Stop words' are the words that are ignored by keyword search. There are words in the English language that are so common and so often used (e.g. "the", "and") that we assume that they will not be searched for. Consequently, the `.keyword_search` method skips them if they are in the query, making for more focused results. There is at present no way to keyword search for any word in the stop words list, which you can review here:.


```python
with open("../../../data/other/stop_words.txt", "r") as file:
    print(file.read())
```

    stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

