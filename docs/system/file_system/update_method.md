<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/file_system/update_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## The `update` Method

You can update any metadata of any processed file by using the `update` method.

This overview of the `update` method is divided into the following sections:

- [update Method Arguments](#update-method-arguments)
- [update Method Example](#update-method-example)
- [Observations on the update Method](#observations-on-the-update-method)

### `update` Method Arguments

The `update` method takes one required argument and at least one of several optional arguments:

- `file_id` (required, str) - The `file_id` of the file whose metadata you wish to update.

- `expire_time` (optional, int) - The amount of time (in seconds) that file data will remain on Krixik servers, counting as of when the `update` method is run.

- `symbolic_directory_path` (optional, str) - A UNIX-formatted directory path under your account in the Krixik system.

- `file_name` (optional, str) - A custom file name that must end with the file extension of the original input file. **You cannot update the file extension.**

- `symbolic_file_path` (optional, str) - A combination of `symbolic_directory_path` and `file_name` in a single argument.

- `file_tags` (optional, list) - A list of custom file tags (each a key-value pair). Note that you must update the whole set, so if a file has three file tags and you update one of them, entirely excluding the other two from the `update` method `file_tags` argument, both of those will be deleted.

- `file_description` (optional, str) - A custom file description.

If none of the optional arguments are present, the `update` method will not work because there will be nothing to update.

### `update` Method Example

For this document's example we will use a pipeline consisting of a single [`parser`](../../modules/support_function_modules/parser_module.md) module.  We use the [`create_pipeline`](../pipeline_creation/create_pipeline.md) method to instantiate the pipeline, and then process a file through it:


```python
# create an example pipeline with a single parser module
pipeline = krixik.create_pipeline(name="update_method_1_parser", module_chain=["parser"])

# process short input file
process_output = pipeline.process(
    local_file_path=data_dir + "input/frankenstein_very_short.txt",  # the initial local filepath where the input JSON file is stored
    local_save_directory=data_dir + "output",  # save output repo data output subdir
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
    verbose=False,  # do not display process update printouts upon running code
    symbolic_directory_path="/novels/gothic",
    file_name="Frankenstein.txt",
    file_tags=[{"author": "Shelley"}, {"category": "gothic"}, {"century": "19"}],
)
```

Let's see what the file's record looks like with the [`list`](list_method.md) method:


```python
# see the file's record with
list_output = pipeline.list(symbolic_directory_paths=["/novels/gothic"])

# nicely print the output of this
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "6ccb47ec-574d-4d48-9dcb-7d0fe91f23b8",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:20:51",
          "process_id": "d99653b8-d16a-981a-41ab-1a2a86e99e9f",
          "created_at": "2024-06-05 15:20:51",
          "file_metadata": {
            "modules": {
              "module_1": {
                "parser": {
                  "model": "sentence"
                }
              }
            },
            "modules_data": {
              "module_1": {
                "parser": {
                  "data_files_extensions": [
                    ".json"
                  ],
                  "num_lines": 26
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "shelley"
            },
            {
              "category": "gothic"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/gothic",
          "pipeline": "update_method_1_parser",
          "file_id": "e53d3c35-6f4c-466f-ab7c-6971a6312a09",
          "expire_time": "2024-06-05 15:50:50",
          "file_name": "frankenstein.txt"
        }
      ]
    }


We can use the `update` method to update the file's metadata.

We'll update its `file_name`, since it's erroneous, change the `{"category": "gothic"}` file tag for something different, and add a `file_description`. We'll leave its `symbolic_directory_path` untouched.


```python
# update metadata the metadata for the processed file
update_output = pipeline.update(
    file_id=process_output["file_id"],
    file_name="Frankenstein.txt",
    file_tags=[{"author": "Shelley"}, {"country": "UK"}, {"century": "19"}],
    file_description="Is the villain the monster or the doctor?",
)

# nicely print the output of this update
print(json.dumps(process_output, indent=2))
```

    INFO: lower casing file_name Frankenstein.txt to frankenstein.txt
    INFO: lower casing file tag {'author': 'Shelley'} to {'author': 'shelley'}
    INFO: lower casing file tag {'country': 'UK'} to {'country': 'uk'}
    {
      "status_code": 200,
      "pipeline": "update_method_1_parser",
      "request_id": "3c82cde3-dc63-431f-bf68-1a33b998c272",
      "file_id": "e53d3c35-6f4c-466f-ab7c-6971a6312a09",
      "message": "SUCCESS - output fetched for file_id e53d3c35-6f4c-466f-ab7c-6971a6312a09.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "\ufeffLetter 1\n\n_To Mrs. Saville, England._\n\n\nSt. Petersburgh, Dec. 11th, 17\u2014.",
          "line_numbers": [
            1,
            2,
            3,
            4,
            5,
            6
          ]
        },
        {
          "snippet": "You will rejoice to hear that no disaster has accompanied the\ncommencement of an enterprise which you have regarded with such evil\nforebodings.",
          "line_numbers": [
            7,
            8,
            9,
            10,
            11
          ]
        },
        {
          "snippet": "I arrived here yesterday, and my first task is to assure\nmy dear sister of my welfare and increasing confidence in the success\nof my undertaking.",
          "line_numbers": [
            11,
            12,
            13
          ]
        },
        {
          "snippet": "I am already far north of London, and as I walk in the streets of\nPetersburgh, I feel a cold northern breeze play upon my cheeks, which\nbraces my nerves and fills me with delight.",
          "line_numbers": [
            14,
            15,
            16,
            17
          ]
        },
        {
          "snippet": "Do you understand this\nfeeling?",
          "line_numbers": [
            17,
            18
          ]
        },
        {
          "snippet": "This breeze, which has travelled from the regions towards\nwhich I am advancing, gives me a foretaste of those icy climes.",
          "line_numbers": [
            18,
            19
          ]
        },
        {
          "snippet": "Inspirited by this wind of promise, my daydreams become more fervent\nand vivid.",
          "line_numbers": [
            20,
            21
          ]
        },
        {
          "snippet": "I try in vain to be persuaded that the pole is the seat of\nfrost and desolation; it ever presents itself to my imagination as the\nregion of beauty and delight.",
          "line_numbers": [
            21,
            22,
            23
          ]
        },
        {
          "snippet": "There, Margaret, the sun is for ever\nvisible, its broad disk just skirting the horizon and diffusing a\nperpetual splendour.",
          "line_numbers": [
            23,
            24,
            25
          ]
        },
        {
          "snippet": "There\u2014for with your leave, my sister, I will put\nsome trust in preceding navigators\u2014there snow and frost are banished;\nand, sailing over a calm sea, we may be wafted to a land surpassing in\nwonders and in beauty every region hitherto discovered on the habitable\nglobe.",
          "line_numbers": [
            25,
            26,
            27,
            28,
            29
          ]
        },
        {
          "snippet": "Its productions and features may be without example, as the\nphenomena of the heavenly bodies undoubtedly are in those undiscovered\nsolitudes.",
          "line_numbers": [
            29,
            30,
            31
          ]
        },
        {
          "snippet": "What may not be expected in a country of eternal light?",
          "line_numbers": [
            31
          ]
        },
        {
          "snippet": "I\nmay there discover the wondrous power which attracts the needle and may\nregulate a thousand celestial observations that require only this\nvoyage to render their seeming eccentricities consistent for ever.",
          "line_numbers": [
            31,
            32,
            33,
            34
          ]
        },
        {
          "snippet": "I\nshall satiate my ardent curiosity with the sight of a part of the world\nnever before visited, and may tread a land never before imprinted by\nthe foot of man.",
          "line_numbers": [
            34,
            35,
            36,
            37
          ]
        },
        {
          "snippet": "These are my enticements, and they are sufficient to\nconquer all fear of danger or death and to induce me to commence this\nlaborious voyage with the joy a child feels when he embarks in a little\nboat, with his holiday mates, on an expedition of discovery up his\nnative river.",
          "line_numbers": [
            37,
            38,
            39,
            40,
            41
          ]
        },
        {
          "snippet": "But supposing all these conjectures to be false, you\ncannot contest the inestimable benefit which I shall confer on all\nmankind, to the last generation, by discovering a passage near the pole\nto those countries, to reach which at present so many months are\nrequisite; or by ascertaining the secret of the magnet, which, if at\nall possible, can only be effected by an undertaking such as mine.",
          "line_numbers": [
            41,
            42,
            43,
            44,
            45,
            46
          ]
        },
        {
          "snippet": "These reflections have dispelled the agitation with which I began my\nletter, and I feel my heart glow with an enthusiasm which elevates me\nto heaven, for nothing contributes so much to tranquillise the mind as\na steady purpose\u2014a point on which the soul may fix its intellectual\neye.",
          "line_numbers": [
            47,
            48,
            49,
            50,
            51,
            52
          ]
        },
        {
          "snippet": "This expedition has been the favourite dream of my early years.",
          "line_numbers": [
            52
          ]
        },
        {
          "snippet": "I\nhave read with ardour the accounts of the various voyages which have\nbeen made in the prospect of arriving at the North Pacific Ocean\nthrough the seas which surround the pole.",
          "line_numbers": [
            52,
            53,
            54,
            55
          ]
        },
        {
          "snippet": "You may remember that a\nhistory of all the voyages made for purposes of discovery composed the\nwhole of our good Uncle Thomas\u2019 library.",
          "line_numbers": [
            55,
            56,
            57
          ]
        },
        {
          "snippet": "My education was neglected,\nyet I was passionately fond of reading.",
          "line_numbers": [
            57,
            58
          ]
        },
        {
          "snippet": "These volumes were my study\nday and night, and my familiarity with them increased that regret which\nI had felt, as a child, on learning that my father\u2019s dying injunction\nhad forbidden my uncle to allow me to embark in a seafaring life.",
          "line_numbers": [
            58,
            59,
            60,
            61
          ]
        },
        {
          "snippet": "These visions faded when I perused, for the first time, those poets\nwhose effusions entranced my soul and lifted it to heaven.",
          "line_numbers": [
            62,
            63,
            64
          ]
        },
        {
          "snippet": "I also\nbecame a poet and for one year lived in a paradise of my own creation;\nI imagined that I also might obtain a niche in the temple where the\nnames of Homer and Shakespeare are consecrated.",
          "line_numbers": [
            64,
            65,
            66,
            67
          ]
        },
        {
          "snippet": "You are well\nacquainted with my failure and how heavily I bore the disappointment.",
          "line_numbers": [
            67,
            68
          ]
        },
        {
          "snippet": "But just at that time I inherited the fortune of my cousin, and my\nthoughts were turned into the channel of their earlier bent.",
          "line_numbers": [
            69,
            70
          ]
        }
      ],
      "process_output_files": [
        "../../../data/output/e53d3c35-6f4c-466f-ab7c-6971a6312a09.json"
      ]
    }


Now we invoke the [`list`](list_method.md) method to confirm that all metadata has indeed been updated as requested:


```python
# call  to see the file's newly updated record
list_output = pipeline.list(symbolic_file_paths=["/novels/gothic/Frankenstein.txt"])

# nicely print the output of this
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "396b969f-2aeb-4952-bd6a-67e1ccca14f1",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:21:10",
          "process_id": "d99653b8-d16a-981a-41ab-1a2a86e99e9f",
          "created_at": "2024-06-05 15:20:51",
          "file_metadata": {
            "modules": {
              "module_1": {
                "parser": {
                  "model": "sentence"
                }
              }
            },
            "modules_data": {
              "module_1": {
                "parser": {
                  "data_files_extensions": [
                    ".json"
                  ],
                  "num_lines": 26
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "shelley"
            },
            {
              "country": "uk"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "Is the villain the monster or the doctor?",
          "symbolic_directory_path": "/novels/gothic",
          "pipeline": "update_method_1_parser",
          "file_id": "e53d3c35-6f4c-466f-ab7c-6971a6312a09",
          "expire_time": "2024-06-05 15:50:50",
          "file_name": "frankenstein.txt"
        }
      ]
    }


### Observations on the `update` Method

Four closing observation on the `update` method:

- Note that in the example above we updated `file_tags` by including the entire set of file tags: `[{"author": "Shelley"}, {"country": "UK"}, {"century": 19}]`. If we'd only used `[{"country": "UK"}]`, the "author" and "century" ones would have been deleted.

- You cannot update a `symbolic_directory_path`/`file_name` combination (a.k.a. a `symbolic_file_path`) so it's identical to that of another file. Krixik will not allow it.

- You can also not update a file's file extension. For instance, a `.txt` file cannot become a `.pdf` file through the `update` method.

- The `update` method allows you to extend a file's [`expire_time`](../parameters_processing_files_through_pipelines/process_method.md#core-process-method-arguments) indefinitely. Upon initially uploading a file, its [`expire_time`](../parameters_processing_files_through_pipelines/process_method.md#core-process-method-arguments) cannot be greater than 2,592,000 seconds (30 days). However, if you periodically invoke `update` on its file and reset its [`expire_time`](../parameters_processing_files_through_pipelines/process_method.md#core-process-method-arguments) to another 2,592,000 seconds (or however many seconds you please), the file will remain on-system for that much more time as of that moment, and so forth.
