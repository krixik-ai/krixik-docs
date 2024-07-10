<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/search_methods/semantic_search_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

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
print(json.dumps(output_2, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "semantic_search_method_1_parser_text-embedder_vector-db",
      "request_id": "4197e750-0560-43b9-b7e3-0ea5c8f15151",
      "file_id": "a94765c2-0250-4b3d-98af-20fc167640e8",
      "message": "SUCCESS - output fetched for file_id a94765c2-0250-4b3d-98af-20fc167640e8.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/a94765c2-0250-4b3d-98af-20fc167640e8.faiss"
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
      "request_id": "c1b9116f-0eaa-489d-a8f4-86ca7238e744",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "853f498f-4b1c-439b-bbd4-ccc47c44d254",
          "file_metadata": {
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_vectors": 43,
            "created_at": "2024-06-05 16:19:43",
            "last_updated": "2024-06-05 16:19:43"
          },
          "search_results": [
            {
              "snippet": "The four young faces on which the firelight shone brightened at the\ncheerful words, but darkened again as Jo said sadly,--\n\n\"We haven't got father, and shall not have him for a long time.\"",
              "line_numbers": [
                19,
                20,
                21,
                22,
                23
              ],
              "distance": 0.351
            },
            {
              "snippet": "Nobody spoke for a minute; then Meg said in an altered tone,--\n\n\"You know the reason mother proposed not having any presents this\nChristmas was because it is going to be a hard winter for every one; and\nshe thinks we ought not to spend money for pleasure, when our men are\nsuffering so in the army.",
              "line_numbers": [
                26,
                27,
                28,
                29,
                30,
                31,
                32
              ],
              "distance": 0.363
            },
            {
              "snippet": "said Meg, who could remember better times.",
              "line_numbers": [
                82
              ],
              "distance": 0.402
            },
            {
              "snippet": "\"It's so dreadful to be poor!\"",
              "line_numbers": [
                9,
                10
              ],
              "distance": 0.402
            },
            {
              "snippet": "\"How would you\nlike to be shut up for hours with a nervous, fussy old lady, who keeps\nyou trotting, is never satisfied, and worries you till you're ready to\nfly out of the window or cry?\"",
              "line_numbers": [
                58,
                59,
                60,
                61
              ],
              "distance": 0.403
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
      "request_id": "ba1b7b85-8e36-49e5-8734-68c80d19e433",
      "message": "Successfully queried 4 user files.",
      "warnings": [],
      "items": [
        {
          "snippet": "I am already far north of London, and as I walk in the streets of\nPetersburgh, I feel a cold northern breeze play upon my cheeks, which\nbraces my nerves and fills me with delight.",
          "distance": 0.33,
          "line_numbers": [
            14,
            15,
            16,
            17
          ],
          "file_metadata": {
            "file_id": "f4720361-f94f-4f48-a4bf-0177dd91ba18",
            "file_name": "frankenstein.txt",
            "symbolic_directory_path": "/novels/gothic",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:17:58",
            "last_updated": "2024-06-05 16:17:58"
          }
        },
        {
          "snippet": "This breeze, which has travelled from the regions towards\nwhich I am advancing, gives me a foretaste of those icy climes.",
          "distance": 0.336,
          "line_numbers": [
            18,
            19
          ],
          "file_metadata": {
            "file_id": "f4720361-f94f-4f48-a4bf-0177dd91ba18",
            "file_name": "frankenstein.txt",
            "symbolic_directory_path": "/novels/gothic",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:17:58",
            "last_updated": "2024-06-05 16:17:58"
          }
        },
        {
          "snippet": "The four young faces on which the firelight shone brightened at the\ncheerful words, but darkened again as Jo said sadly,--\n\n\"We haven't got father, and shall not have him for a long time.\"",
          "distance": 0.351,
          "line_numbers": [
            19,
            20,
            21,
            22,
            23
          ],
          "file_metadata": {
            "file_id": "853f498f-4b1c-439b-bbd4-ccc47c44d254",
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:43",
            "last_updated": "2024-06-05 16:19:43"
          }
        },
        {
          "snippet": "There\u2014for with your leave, my sister, I will put\nsome trust in preceding navigators\u2014there snow and frost are banished;\nand, sailing over a calm sea, we may be wafted to a land surpassing in\nwonders and in beauty every region hitherto discovered on the habitable\nglobe.",
          "distance": 0.362,
          "line_numbers": [
            25,
            26,
            27,
            28,
            29
          ],
          "file_metadata": {
            "file_id": "f4720361-f94f-4f48-a4bf-0177dd91ba18",
            "file_name": "frankenstein.txt",
            "symbolic_directory_path": "/novels/gothic",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:17:58",
            "last_updated": "2024-06-05 16:17:58"
          }
        },
        {
          "snippet": "Nobody spoke for a minute; then Meg said in an altered tone,--\n\n\"You know the reason mother proposed not having any presents this\nChristmas was because it is going to be a hard winter for every one; and\nshe thinks we ought not to spend money for pleasure, when our men are\nsuffering so in the army.",
          "distance": 0.363,
          "line_numbers": [
            26,
            27,
            28,
            29,
            30,
            31,
            32
          ],
          "file_metadata": {
            "file_id": "853f498f-4b1c-439b-bbd4-ccc47c44d254",
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:43",
            "last_updated": "2024-06-05 16:19:43"
          }
        },
        {
          "snippet": "There, Margaret, the sun is for ever\nvisible, its broad disk just skirting the horizon and diffusing a\nperpetual splendour.",
          "distance": 0.377,
          "line_numbers": [
            23,
            24,
            25
          ],
          "file_metadata": {
            "file_id": "f4720361-f94f-4f48-a4bf-0177dd91ba18",
            "file_name": "frankenstein.txt",
            "symbolic_directory_path": "/novels/gothic",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:17:58",
            "last_updated": "2024-06-05 16:17:58"
          }
        },
        {
          "snippet": "Far from it.",
          "distance": 0.389,
          "line_numbers": [
            11
          ],
          "file_metadata": {
            "file_id": "d9e477d5-9b2c-4bf3-aa25-b6c739b83b86",
            "file_name": "moby dick.txt",
            "symbolic_directory_path": "/novels/adventure",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:31",
            "last_updated": "2024-06-05 16:19:31"
          }
        },
        {
          "snippet": "said Meg, who could remember better times.",
          "distance": 0.402,
          "line_numbers": [
            82
          ],
          "file_metadata": {
            "file_id": "853f498f-4b1c-439b-bbd4-ccc47c44d254",
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:43",
            "last_updated": "2024-06-05 16:19:43"
          }
        },
        {
          "snippet": "\"It's so dreadful to be poor!\"",
          "distance": 0.402,
          "line_numbers": [
            9,
            10
          ],
          "file_metadata": {
            "file_id": "853f498f-4b1c-439b-bbd4-ccc47c44d254",
            "file_name": "little women.txt",
            "symbolic_directory_path": "/novels/bildungsroman",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:43",
            "last_updated": "2024-06-05 16:19:43"
          }
        },
        {
          "snippet": "But gulp down your tears and hie aloft to the\n  royal-mast with your hearts; for your friends who have gone before\n  are clearing out the seven-storied heavens, and making refugees of\n  long-pampered Gabriel, Michael, and Raphael, against your coming.",
          "distance": 0.41,
          "line_numbers": [
            27,
            28,
            29,
            30
          ],
          "file_metadata": {
            "file_id": "d9e477d5-9b2c-4bf3-aa25-b6c739b83b86",
            "file_name": "moby dick.txt",
            "symbolic_directory_path": "/novels/adventure",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:31",
            "last_updated": "2024-06-05 16:19:31"
          }
        },
        {
          "snippet": "It will be seen that this mere painstaking burrower and grub-worm of\n  a poor devil of a Sub-Sub appears to have gone through the long\n  Vaticans and street-stalls of the earth, picking up whatever random\n  allusions to whales he could anyways find in any book whatsoever,\n  sacred or profane.",
          "distance": 0.433,
          "line_numbers": [
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9
          ],
          "file_metadata": {
            "file_id": "d9e477d5-9b2c-4bf3-aa25-b6c739b83b86",
            "file_name": "moby dick.txt",
            "symbolic_directory_path": "/novels/adventure",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:31",
            "last_updated": "2024-06-05 16:19:31"
          }
        },
        {
          "snippet": "Would that I could clear out Hampton Court and the\n  Tuileries for ye!",
          "distance": 0.438,
          "line_numbers": [
            26,
            27
          ],
          "file_metadata": {
            "file_id": "d9e477d5-9b2c-4bf3-aa25-b6c739b83b86",
            "file_name": "moby dick.txt",
            "symbolic_directory_path": "/novels/adventure",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:31",
            "last_updated": "2024-06-05 16:19:31"
          }
        },
        {
          "snippet": "On the other hand,\nI, for my part, declare for_ Pride and Prejudice _unhesitatingly.",
          "distance": 0.438,
          "line_numbers": [
            35,
            36
          ],
          "file_metadata": {
            "file_id": "a94765c2-0250-4b3d-98af-20fc167640e8",
            "file_name": "pride and prejudice.txt",
            "symbolic_directory_path": "/novels/romance",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:18",
            "last_updated": "2024-06-05 16:19:18"
          }
        },
        {
          "snippet": "The catastrophe of_ Mansfield Park _is admittedly\ntheatrical, the hero and heroine are insipid, and the author has almost\nwickedly destroyed all romantic interest by expressly admitting that\nEdmund only took Fanny because Mary shocked him, and that Fanny might\nvery likely have taken Crawford if he had been a little more assiduous;\nyet the matchless rehearsal-scenes and the characters of Mrs. Norris and\nothers have secured, I believe, a considerable party for it._ Sense and\nSensibility _has perhaps the fewest out-and-out admirers; but it dos\nnot want them._\n\n_I suppose, however, that the majority of at least competent votes\nwould, all things considered, be divided between_ Emma _and the present\nbook; and perhaps the vulgar verdict (if indeed a fondness for Miss\nAusten be not of itself a patent of exemption from any possible charge\nof vulgarity) would go for_ Emma.",
          "distance": 0.465,
          "line_numbers": [
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31
          ],
          "file_metadata": {
            "file_id": "a94765c2-0250-4b3d-98af-20fc167640e8",
            "file_name": "pride and prejudice.txt",
            "symbolic_directory_path": "/novels/romance",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:18",
            "last_updated": "2024-06-05 16:19:18"
          }
        },
        {
          "snippet": "To some the delightful freshness and humour of_ Northanger\nAbbey, _its completeness, finish, and_ entrain, _obscure the undoubted\ncritical facts that its scale is small, and its scheme, after all, that\nof burlesque or parody, a kind in which the first rank is reached with\ndifficulty._ Persuasion, _relatively faint in tone, and not enthralling\nin interest, has devotees who exalt above all the others its exquisite\ndelicacy and keeping.",
          "distance": 0.468,
          "line_numbers": [
            11,
            12,
            13,
            14,
            15,
            16,
            17
          ],
          "file_metadata": {
            "file_id": "a94765c2-0250-4b3d-98af-20fc167640e8",
            "file_name": "pride and prejudice.txt",
            "symbolic_directory_path": "/novels/romance",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:18",
            "last_updated": "2024-06-05 16:19:18"
          }
        },
        {
          "snippet": "And in the sect--fairly large and yet\nunusually choice--of Austenians or Janites, there would probably be\nfound partisans of the claim to primacy of almost every one of the\nnovels.",
          "distance": 0.479,
          "line_numbers": [
            8,
            9,
            10,
            11
          ],
          "file_metadata": {
            "file_id": "a94765c2-0250-4b3d-98af-20fc167640e8",
            "file_name": "pride and prejudice.txt",
            "symbolic_directory_path": "/novels/romance",
            "file_tags": [],
            "num_lines": 0,
            "created_at": "2024-06-05 16:19:18",
            "last_updated": "2024-06-05 16:19:18"
          }
        }
      ]
    }


As you can see, results from all the files have been combined, and the result ranked at the top has the shortest query-result distance of the entire file set.

### Output Size Cap

The current size limit on output generated by the `semantic_search` method is 5MB.
