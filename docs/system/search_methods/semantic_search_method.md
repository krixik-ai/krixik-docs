## The `semantic_search` Method

Krixik's `semantic_search` method enables semantic search on documents processed through certain pipelines. Much has been written about semantic search, but in a nutshell, instead of searching a document for specific keywords, it searches for text similar in _meaning_ to the string that's been queried for. Contrast this to [keyword search](keyword_search_method.md).

Given that the `semantic_search` method both [embeds](../../modules/ai_modules/text-embedder_module.md) the query and performs the search, it can only be used with pipelines containing both a [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) module and a [`vector-db`](../../modules/database_modules/vector-db_module.md) module in immediate succession.

This overview of the `semantic_search` method is divided into the following sections:

- [semantic_search Method Arguments](#semantic_search-method-arguments)
- [Example Pipeline Setup and File Processing](#example-pipeline-setup-and-file-processing)
- [Example Semantic Searches](#example-semantic-searches)
- [Output Size Cap](#output-size-cap)

### `semantic_search` Method Arguments

The `semantic_search` method takes one required argument and at least one of several optional arguments. The required argument is:

- `query` (str) - A string whose meaning will be searched for across the target document. The closest matches (i.e. snippets of text that most match the query in meaning) will be returned.

The optional arguments are the same arguments that the [`list`](../file_system/list_method.md) method takes—both metadata and timestamp bookends—so please take a moment to [review them here](../file_system/list_method.md#list-method-arguments). As with the [`list`](../file_system/list_method.md) method, you can semantically search across several files at the same time because all metadata arguments are submitted to the `semantic_search` method in list format. All optional argument elements are the same as for the [`list`](../file_system/list_method.md) method, including the wildcard operator and the global root.

If none of these optional arguments is present, the `semantic_search` method will not work because there will be nothing to search through.

Like the [`list`](../file_system/list_method.md) method, the `semantic_search` method also accepts the optional `max_files` and `sort_order` arguments, though their function changes a bit:

- `max_files` - Specifies up to how many files should be searched through. Default is none.

- `sort_order` - Here takes three possible values: 'ascending', descending', and now 'global'. The first two sort results by the file they're in (the files are sorted by the creation timestamp of the file), and 'global' combines all files and returns the very best results across all files. Default is 'descending'.

Finally, the `semantic_search` method accepts one optional method that is unique to it:

- `k` (int) - Specifies up to how many results will be returned per queried file. Default is 5.

### Example Pipeline Setup and File Processing

For this document's examples we will use a pipeline consisting of three modules: a [`parser module`](../../modules/support_function_modules/parser_module.md), a [`text-embedder module`](../../modules/ai_modules/text-embedder_module.md), and a [`vector-db module`](../../modules/database_modules/vector-db_module.md). This is the basic semantic search [pipeline](../../examples/search_pipeline_examples/multi_basic_semantic_search.md). We use the [`create_pipeline`](../pipeline_creation/create_pipeline.md) method to instantiate the pipeline.


```python
# create the basic semantic search pipeline
pipeline = krixik.create_pipeline(
    name="semantic_search_method_1_parser_text-embedder_vector-db", module_chain=["parser", "text-embedder", "vector-db"]
)
```

The pipeline ready, we'll [`process`](../parameters_processing_files_through_pipelines/process_method.md) a few text files through it so we have something to search through. Let's use the same files we used in the [`list` method documentation](../file_system/list_method.md).


```python
# add four files to the pipeline we just created.
output_1 = pipeline.process(
    local_file_path="../../../data/input/frankenstein_very_short.txt",  # the initial local filepath where the input JSON file is stored
    local_save_directory="../../../data/output",
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
    verbose=False,  # do not display process update printouts upon running code
    symbolic_directory_path="/novels/gothic",
    file_name="Frankenstein.txt",
)

output_2 = pipeline.process(
    local_file_path="../../../data/input/pride_and_prejudice_very_short.txt",  # the initial local filepath where the input JSON file is stored
    local_save_directory="../../../data/output",
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
    verbose=False,  # do not display process update printouts upon running code
    symbolic_directory_path="/novels/romance",
    file_name="Pride and Prejudice.txt",
)

output_3 = pipeline.process(
    local_file_path="../../../data/input/moby_dick_very_short.txt",  # the initial local filepath where the input JSON file is stored
    local_save_directory="../../../data/output",
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
    verbose=False,  # do not display process update printouts upon running code
    symbolic_directory_path="/novels/adventure",
    file_name="Moby Dick.txt",
)

output_4 = pipeline.process(
    local_file_path="../../../data/input/little_women_very_short.txt",  # the initial local filepath where the input JSON file is stored
    local_save_directory="../../../data/output",
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
print(json.dumps(output_2, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "semantic_search_method_1_parser_text-embedder_vector-db",
      "request_id": "2615ca13-adf7-4951-9ab9-bf3465ea47ce",
      "file_id": "c9ac7eae-81ac-451f-b15e-ead72ee234c9",
      "message": "SUCCESS - output fetched for file_id c9ac7eae-81ac-451f-b15e-ead72ee234c9.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "c:\\Users\\Lucas\\Desktop\\krixikdocsnoodle\\docs\\system\\search_methods/c9ac7eae-81ac-451f-b15e-ead72ee234c9.faiss"
      ]
    }


The value of `process_output` is `null` because the return object is a database, so it cannot be printed here. You can review this database in the local location provided in the `process_output_files`.

### Example Semantic Searches

With files now processed through the pipeline we can run the `semantic_search` method on it.

Let's try an example in which we query one of the files file:


```python
# perform semantic_search over one file
semantic_output = pipeline.semantic_search(query="It was cold night.", file_names=["Little Women.txt"])

# nicely print the output of this search
print(json.dumps(semantic_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "85192b31-b872-4d40-b4bb-2cbcf926fead",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "7c352bfe-3487-4ccd-acc6-144f8b7cdfbf",
          "file_metadata": {
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_vectors": 2068,
            "created_at": "2024-05-20 19:11:26",
            "last_updated": "2024-05-20 19:11:26"
          },
          "search_results": [
            {
              "snippet": "How is your cold, Meg?",
              "line_numbers": [
                940
              ],
              "distance": 0.27
            },
            {
              "snippet": "Shivering, dripping, and crying, they got Amy home; and, after an\nexciting time of it, she fell asleep, rolled in blankets, before a hot\nfire.",
              "line_numbers": [
                4016,
                4017,
                4018,
                4019
              ],
              "distance": 0.274
            },
            {
              "snippet": "Jo saw her coming, and turned her back; Laurie did not see, for he\nwas carefully skating along the shore, sounding the ice, for a warm\nspell had preceded the cold snap.",
              "line_numbers": [
                3966,
                3967,
                3968
              ],
              "distance": 0.274
            },
            {
              "snippet": "Jo was the first to wake in the gray dawn of Christmas morning.",
              "line_numbers": [
                1134,
                1135,
                1136
              ],
              "distance": 0.287
            },
            {
              "snippet": "Everybody dawdled\nthat morning, and it was noon before the girls found energy enough even\nto take up their worsted work.",
              "line_numbers": [
                4432,
                4433,
                4434
              ],
              "distance": 0.288
            }
          ]
        }
      ]
    }


In addition to returning the snippets that are closest in meaning to our query, we also see the calculated vector distance (in a way, the distance in meaning) between each result and the query. The shorter this distance is, the closer in meaning the result to the query. The `semantic_search` method returns the snippets with the shortest vector distance to query, ranked in ascending order within each file.

When `sort_order` is set to 'global', results from all files are combined and the method returns the snippets with the shortest distance to query, ranked in ascending order, regardless of what file each result may be in. Let's give this a shot by searching through multiple files with the [wildcard operator](../file_system/list_method.md#wildcard-operator-arguments):


```python
# perform semantic_search over multiple files
semantic_output = pipeline.semantic_search(query="It was cold night.", symbolic_directory_paths=["/novels*"], sort_order="global", k=4)

# nicely print the output of this search
print(json.dumps(semantic_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "76b5d209-8bb4-467d-b454-4e784bf32ad4",
      "message": "Successfully queried 4 user files.",
      "warnings": [],
      "items": [
        {
          "snippet": "It was a Saturday night\nin December.",
          "distance": 0.189,
          "line_numbers": [
            1048,
            1049
          ],
          "file_metadata": {
            "file_id": "23f62ad0-daf6-448d-a44b-47a447b2f6d7",
            "file_name": "moby dick.txt",
            "symbolic_directory_path": "/novels/adventure",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:10:46",
            "last_updated": "2024-05-20 19:10:46"
          }
        },
        {
          "snippet": "It was a\nvery dubious-looking, nay, a very dark and dismal night, bitingly cold\nand cheerless.",
          "distance": 0.203,
          "line_numbers": [
            1072,
            1073,
            1074
          ],
          "file_metadata": {
            "file_id": "23f62ad0-daf6-448d-a44b-47a447b2f6d7",
            "file_name": "moby dick.txt",
            "symbolic_directory_path": "/novels/adventure",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:10:46",
            "last_updated": "2024-05-20 19:10:46"
          }
        },
        {
          "snippet": "A great fall of snow had taken\nplace the night before, and the fields were of one uniform white; the\nappearance was disconsolate, and I found my feet chilled by the cold\ndamp substance that covered the ground.",
          "distance": 0.242,
          "line_numbers": [
            3236,
            3237,
            3238,
            3239
          ],
          "file_metadata": {
            "file_id": "4830bdad-7b1b-46ad-9e70-2a60c077849f",
            "file_name": "frankenstein.txt",
            "symbolic_directory_path": "/novels/gothic",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:09:33",
            "last_updated": "2024-05-20 19:09:33"
          }
        },
        {
          "snippet": "By degrees, after the morning\u2019s dawn,\nsleep came.",
          "distance": 0.247,
          "line_numbers": [
            1233,
            1234
          ],
          "file_metadata": {
            "file_id": "4830bdad-7b1b-46ad-9e70-2a60c077849f",
            "file_name": "frankenstein.txt",
            "symbolic_directory_path": "/novels/gothic",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:09:33",
            "last_updated": "2024-05-20 19:09:33"
          }
        },
        {
          "snippet": "I was still cold when under one of the trees I found a huge cloak, with\nwhich I covered myself, and sat down upon the ground.",
          "distance": 0.25,
          "line_numbers": [
            3165,
            3166
          ],
          "file_metadata": {
            "file_id": "4830bdad-7b1b-46ad-9e70-2a60c077849f",
            "file_name": "frankenstein.txt",
            "symbolic_directory_path": "/novels/gothic",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:09:33",
            "last_updated": "2024-05-20 19:09:33"
          }
        },
        {
          "snippet": "I then paused, and a\ncold shivering came over me.",
          "distance": 0.252,
          "line_numbers": [
            1665,
            1666
          ],
          "file_metadata": {
            "file_id": "4830bdad-7b1b-46ad-9e70-2a60c077849f",
            "file_name": "frankenstein.txt",
            "symbolic_directory_path": "/novels/gothic",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:09:33",
            "last_updated": "2024-05-20 19:09:33"
          }
        },
        {
          "snippet": "The sky had changed from clear, sunny cold, to driving\nsleet and mist.",
          "distance": 0.26,
          "line_numbers": [
            2062,
            2063
          ],
          "file_metadata": {
            "file_id": "23f62ad0-daf6-448d-a44b-47a447b2f6d7",
            "file_name": "moby dick.txt",
            "symbolic_directory_path": "/novels/adventure",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:10:46",
            "last_updated": "2024-05-20 19:10:46"
          }
        },
        {
          "snippet": "We felt\nvery nice and snug, the more so since it was so chilly out of doors;\nindeed out of bed-clothes too, seeing that there was no fire in the\nroom.",
          "distance": 0.264,
          "line_numbers": [
            2727,
            2728,
            2729,
            2730
          ],
          "file_metadata": {
            "file_id": "23f62ad0-daf6-448d-a44b-47a447b2f6d7",
            "file_name": "moby dick.txt",
            "symbolic_directory_path": "/novels/adventure",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:10:46",
            "last_updated": "2024-05-20 19:10:46"
          }
        },
        {
          "snippet": "How is your cold, Meg?",
          "distance": 0.27,
          "line_numbers": [
            940
          ],
          "file_metadata": {
            "file_id": "7c352bfe-3487-4ccd-acc6-144f8b7cdfbf",
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:11:26",
            "last_updated": "2024-05-20 19:11:26"
          }
        },
        {
          "snippet": "Shivering, dripping, and crying, they got Amy home; and, after an\nexciting time of it, she fell asleep, rolled in blankets, before a hot\nfire.",
          "distance": 0.274,
          "line_numbers": [
            4016,
            4017,
            4018,
            4019
          ],
          "file_metadata": {
            "file_id": "7c352bfe-3487-4ccd-acc6-144f8b7cdfbf",
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:11:26",
            "last_updated": "2024-05-20 19:11:26"
          }
        },
        {
          "snippet": "Jo saw her coming, and turned her back; Laurie did not see, for he\nwas carefully skating along the shore, sounding the ice, for a warm\nspell had preceded the cold snap.",
          "distance": 0.274,
          "line_numbers": [
            3966,
            3967,
            3968
          ],
          "file_metadata": {
            "file_id": "7c352bfe-3487-4ccd-acc6-144f8b7cdfbf",
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:11:26",
            "last_updated": "2024-05-20 19:11:26"
          }
        },
        {
          "snippet": "Jo was the first to wake in the gray dawn of Christmas morning.",
          "distance": 0.287,
          "line_numbers": [
            1134,
            1135,
            1136
          ],
          "file_metadata": {
            "file_id": "7c352bfe-3487-4ccd-acc6-144f8b7cdfbf",
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:11:26",
            "last_updated": "2024-05-20 19:11:26"
          }
        },
        {
          "snippet": "Miss\nBennet had slept ill, and though up, was very feverish, and not well\nenough to leave her room.",
          "distance": 0.29,
          "line_numbers": [
            1792,
            1793,
            1794
          ],
          "file_metadata": {
            "file_id": "c9ac7eae-81ac-451f-b15e-ead72ee234c9",
            "file_name": "pride and prejudice.txt",
            "symbolic_directory_path": "/novels/romance",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:10:16",
            "last_updated": "2024-05-20 19:10:16"
          }
        },
        {
          "snippet": "The apothecary came; and having\nexamined his patient, said, as might be supposed, that she had caught a\nviolent cold, and that they must endeavour to get the better of it;\nadvised her to return to bed, and promised her some draughts.",
          "distance": 0.304,
          "line_numbers": [
            1805,
            1806,
            1807,
            1808
          ],
          "file_metadata": {
            "file_id": "c9ac7eae-81ac-451f-b15e-ead72ee234c9",
            "file_name": "pride and prejudice.txt",
            "symbolic_directory_path": "/novels/romance",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:10:16",
            "last_updated": "2024-05-20 19:10:16"
          }
        },
        {
          "snippet": "Why must _she_ be scampering about the\ncountry, because her sister had a cold?",
          "distance": 0.309,
          "line_numbers": [
            1876,
            1877
          ],
          "file_metadata": {
            "file_id": "c9ac7eae-81ac-451f-b15e-ead72ee234c9",
            "file_name": "pride and prejudice.txt",
            "symbolic_directory_path": "/novels/romance",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:10:16",
            "last_updated": "2024-05-20 19:10:16"
          }
        },
        {
          "snippet": "People do not die of little\ntrifling colds.",
          "distance": 0.321,
          "line_numbers": [
            1740,
            1741
          ],
          "file_metadata": {
            "file_id": "c9ac7eae-81ac-451f-b15e-ead72ee234c9",
            "file_name": "pride and prejudice.txt",
            "symbolic_directory_path": "/novels/romance",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-05-20 19:10:16",
            "last_updated": "2024-05-20 19:10:16"
          }
        }
      ]
    }


As you can see, results from all the files have been combined, and the result ranked at the top has the shortest query-result distance of the entire file set.

### Output Size Cap

The current size limit on output generated by the `semantic_search` method is 5MB.
