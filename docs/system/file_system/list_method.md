<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/file_system/list_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## The `list` Method

After using the [`process`](../parameters_processing_files_through_pipelines/process_method.md) method to process one or several files through your chosen pipeline, you can retrieve the record of any file(s) with the `list` method. You can `list` by `file_id` or by any other metadata you included when initially processing the file.  

This overview of the `list` method is divided into the following sections:

- [list Method Arguments](#list-method-arguments)
- [Example Pipeline Setup and File Processing](#example-pipeline-setup-and-file-processing)
- [Listing by `file_ids`](#listing-by-file_ids)
- [Listing by `file_names`](#listing-by-file_names)
- [Listing by `symbolic_directory_paths`](#listing-by-symbolic_directory_paths)
- [Listing by `file_tags`](#listing-by-file_tags)
- [Listing by `created_at` and `updated_at` Bookend Times](#listing-by-created_at-and-updated_at-bookend-times)
- [Wildcard Operator Arguments](#wildcard-operator-arguments)
- [The Global Root](#the-global-root)
- [Using Multiple Arguments with the `list` Method](#using-multiple-arguments-with-the-list-method)
- [Output Size Cap](#output-size-cap)

### `list` Method Arguments

The `list` method is very versatile. It allows you to list by several different metadata items and by a combination of different metadata items.

All of the following arguments are optional. However, you must use at least one argument for the `list` method to function.

For a refresher on file system metadata arguments please visit the [`process` method overview](../parameters_processing_files_through_pipelines/process_method.md). The metadata arguments you can use for `list` are:

- `file_ids`: A list of one or several `file_id`s to return records for.

- `file_names`: A list of  one or several `file_name`s to return records for.

- `symbolic_directory_paths`: A list of one or several `symbolic_directory_path`s to return records for.

- `symbolic_file_paths`: A list of one or several `symbolic_file_path`s to return records for.

- `file_tags`: A list of one or several `file_tag`s to return records for. Note that individual file_tags suffice; if a file has several file tags and you include at least one of them as a `list` argument, that file's record will be returned.

You may use wildcard operators with `file_names`, `symbolic_directory_paths`,`symbolic_file_paths`, and `file_tags` to retrieve records whose exact metadata you don't remember—or if you wish to retrieve records for a group of files that share similar metadata. More on wildcards operators [later](#wildcard-operator-arguments) in this document.

You may also list by timestamp bookends. The `list` method accepts timestamps based on both the creation and latest-update times of your records. These are strings in the `"YYYY-MM-DD HH:MM:SS"` format, or alternatively just in the `"YYYY-MM-DD"` format.

- `created_at_start`: Filters out all files whose `created_at` time is earlier than what you've specified.

- `created_at_end`: Filters out all files whose `created_at` time is after what you've specified.

- `last_updated_start`: Filters out all files whose `last_updated` time is earlier than what you've specified.

- `last_updated_end`: Filters out all files whose `last_updated` time is after what you've specified.

Examples on how to use metadata and timestamps in the `list` method are included below.

Note that file system metadata arguments operate on **OR** logic: for instance, if you `list` by `file_names`, `file_ids`, and `file_tags`, any file that is a match for any of these will be returned. However, timestamp arguments operate on **AND** logic; all files returned must respect the given timestamp bookends. If two timestamp bookends are given and there is no overlap between them, the `list` method will return nothing.

Finally, the `list` method takes two additional optional arguments to help you organize your output:

- `max_files` (int): Determines the maximum number of file records `list` should return. Defaults to none.

- `sort_order` (str): Specifies how results should be sorted. The two valid values for this argument are 'ascending' and 'descending' (in reference to creation timestamp). Defaults to 'descending'.

### Example Pipeline Setup and File Processing

We will need to create a pipeline and [`process`](../parameters_processing_files_through_pipelines/process_method.md) a couple of files through it to illustrate usage of `list`. We'll create a single-module pipeline with a [`parser`](../../modules/support_function_modules/parser_module.md) module and [`process`](../parameters_processing_files_through_pipelines/process_method.md) some TXT files that hold the text of some English-language classics.  We define optional metadata like file_name, file_tags, and symbolic_directory_path for each process to illustrate how each can be used with `list` below.


```python
# create single-module parser pipeline
pipeline = krixik.create_pipeline(name="list_method_1_parser", module_chain=["parser"])
```


```python
# process files through the pipeline we just created.
# we define optional metadata like file_name, file_tags, and symbolic_directory_path for each
# to illustrate the ability to list by each.
entries = [
    {
        "local_file_path": data_dir + "input/frankenstein_very_short.txt",
        "file_name": "Frankenstein.txt",
        "file_tags": [{"author": "Shelley"}, {"category": "gothic"}, {"century": "19"}],
        "symbolic_directory_path": "/novels/gothic",
    },
    {
        "local_file_path": data_dir + "input/pride_and_prejudice_very_short.txt",
        "file_name": "Pride and Prejudice.txt",
        "symbolic_directory_path": "/novels/romance",
        "file_tags": [{"author": "Austen"}, {"category": "romance"}, {"century": "19"}],
    },
    {
        "local_file_path": data_dir + "input/moby_dick_very_short.txt",
        "file_name": "Moby Dick.txt",
        "symbolic_directory_path": "/novels/adventure",
        "file_tags": [{"author": "Melville"}, {"category": "adventure"}, {"century": "19"}],
    },
]

# process each file
all_process_output = []
for entry in entries:
    process_output = pipeline.process(
        local_file_path=entry["local_file_path"],  # the initial local filepath where the input file is stored
        local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
        expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
        wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
        verbose=False,  # do not display process update printouts upon running code
        file_name=entry["file_name"],
        symbolic_directory_path=entry["symbolic_directory_path"],
        file_tags=entry["file_tags"],
    )
    all_process_output.append(process_output)
```

Let's quickly look at what the output for the last of these processed files.


```python
# nicely print the output of the last process
print(json.dumps(all_process_output[-1], indent=2))
```

    {
      "status_code": 200,
      "pipeline": "list_method_1_parser",
      "request_id": "96c60151-9e74-40c1-a904-af10e03b2f3c",
      "file_id": "60d6e243-91bd-4561-a17d-291539cd651a",
      "message": "SUCCESS - output fetched for file_id 60d6e243-91bd-4561-a17d-291539cd651a.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "\ufeff  EXTRACTS.",
          "line_numbers": [
            1
          ]
        },
        {
          "snippet": "(Supplied by a Sub-Sub-Librarian).",
          "line_numbers": [
            1
          ]
        },
        {
          "snippet": "It will be seen that this mere painstaking burrower and grub-worm of\n  a poor devil of a Sub-Sub appears to have gone through the long\n  Vaticans and street-stalls of the earth, picking up whatever random\n  allusions to whales he could anyways find in any book whatsoever,\n  sacred or profane.",
          "line_numbers": [
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9
          ]
        },
        {
          "snippet": "Therefore you must not, in every case at least,\n  take the higgledy-piggledy whale statements, however authentic, in\n  these extracts, for veritable gospel cetology.",
          "line_numbers": [
            9,
            10,
            11
          ]
        },
        {
          "snippet": "Far from it.",
          "line_numbers": [
            11
          ]
        },
        {
          "snippet": "As\n  touching the ancient authors generally, as well as the poets here\n  appearing, these extracts are solely valuable or entertaining, as\n  affording a glancing bird\u2019s eye view of what has been promiscuously\n  said, thought, fancied, and sung of Leviathan, by many nations and\n  generations, including our own.",
          "line_numbers": [
            11,
            12,
            13,
            14,
            15,
            16
          ]
        },
        {
          "snippet": "So fare thee well, poor devil of a Sub-Sub, whose commentator I am.",
          "line_numbers": [
            17,
            18
          ]
        },
        {
          "snippet": "Thou belongest to that hopeless, sallow tribe which no wine of this\n  world will ever warm; and for whom even Pale Sherry would be too\n  rosy-strong; but with whom one sometimes loves to sit, and feel\n  poor-devilish, too; and grow convivial upon tears; and say to them\n  bluntly, with full eyes and empty glasses, and in not altogether\n  unpleasant sadness\u2014Give it up, Sub-Subs!",
          "line_numbers": [
            19,
            20,
            21,
            22,
            23,
            24
          ]
        },
        {
          "snippet": "For by how much the more\n  pains ye take to please the world, by so much the more shall ye for\n  ever go thankless!",
          "line_numbers": [
            24,
            25,
            26
          ]
        },
        {
          "snippet": "Would that I could clear out Hampton Court and the\n  Tuileries for ye!",
          "line_numbers": [
            26,
            27
          ]
        },
        {
          "snippet": "But gulp down your tears and hie aloft to the\n  royal-mast with your hearts; for your friends who have gone before\n  are clearing out the seven-storied heavens, and making refugees of\n  long-pampered Gabriel, Michael, and Raphael, against your coming.",
          "line_numbers": [
            27,
            28,
            29,
            30
          ]
        },
        {
          "snippet": "Here ye strike but splintered hearts together\u2014there, ye shall strike\n  unsplinterable glasses!",
          "line_numbers": [
            31,
            32
          ]
        }
      ],
      "process_output_files": [
        "../../../data/output/60d6e243-91bd-4561-a17d-291539cd651a.json"
      ]
    }


### Listing by `file_ids`

Let's try listing by `file_ids`.

You have the `file_id` of each of the four files you processed; each was returned after processing finalized.  

You can list by multiple `file_id`s if you so choose by providing a list of desired `file_ids`.

For example, to see metadata associated with each file processed above simply pluck out the `file_id` from each processed return.


```python
# list records for two of the uploaded files via file_ids
list_output = pipeline.list(file_ids=[v["file_id"] for v in all_process_output])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "06a926de-267a-48df-90fe-3e0b8e6f3e29",
      "message": "Successfully returned 3 items.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:28:06",
          "process_id": "0131ae96-424f-350e-eede-b9b9f6e60a7c",
          "created_at": "2024-06-05 15:28:06",
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
                  "num_lines": 12
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "melville"
            },
            {
              "category": "adventure"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/adventure",
          "pipeline": "list_method_1_parser",
          "file_id": "60d6e243-91bd-4561-a17d-291539cd651a",
          "expire_time": "2024-06-05 15:58:05",
          "file_name": "moby dick.txt"
        },
        {
          "last_updated": "2024-06-05 15:27:58",
          "process_id": "f6ae9e98-bec4-2314-3d20-9116ec2a4baf",
          "created_at": "2024-06-05 15:27:58",
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
                  "num_lines": 9
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "austen"
            },
            {
              "category": "romance"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/romance",
          "pipeline": "list_method_1_parser",
          "file_id": "5b90a7c0-ccf8-4abf-b8ff-9eb7b755c2d2",
          "expire_time": "2024-06-05 15:57:58",
          "file_name": "pride and prejudice.txt"
        },
        {
          "last_updated": "2024-06-05 15:27:43",
          "process_id": "06cd2d57-22df-5d94-36e4-3133c4d757f7",
          "created_at": "2024-06-05 15:27:43",
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
          "pipeline": "list_method_1_parser",
          "file_id": "8abc402e-57ed-459d-af9c-918ae9dad038",
          "expire_time": "2024-06-05 15:57:41",
          "file_name": "frankenstein.txt"
        }
      ]
    }


As you can see, a full record for each file was returned. To learn more about each metadata item, visit the documentation for the [`process`](../parameters_processing_files_through_pipelines/process_method.md) method, where they are gone into detail on.

### Listing by `file_names`

You can also list via `file_name`s. It works just like listing with `file_id`s above, but with `file_name` instead of `file_id`.  We'll list <u>Pride and Prejudice</u> via `file_names`, as follows:


```python
# list records for one of the uploaded files via file_names
list_output = pipeline.list(file_names=["Pride and Prejudice.txt"])

# nicely print the output of this list
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "a5b399fe-a0e9-4a78-a4eb-2bbc3a7311b7",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:27:58",
          "process_id": "f6ae9e98-bec4-2314-3d20-9116ec2a4baf",
          "created_at": "2024-06-05 15:27:58",
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
                  "num_lines": 9
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "austen"
            },
            {
              "category": "romance"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/romance",
          "pipeline": "list_method_1_parser",
          "file_id": "5b90a7c0-ccf8-4abf-b8ff-9eb7b755c2d2",
          "expire_time": "2024-06-05 15:57:58",
          "file_name": "pride and prejudice.txt"
        }
      ]
    }


As you can see, a full record for each file was returned. To learn more about each metadata item, visit the documentation for the [`process`](../parameters_processing_files_through_pipelines/process_method.md) method, where they are gone into detail on.

### Listing by `symbolic_directory_paths`

You can also list via `symbolic_directory_paths`. It works just like listing with `file_id`s and `file_name`s above, but with `symbolic_directory_path` instead. We'll list <u>Little Women</u> and <u>Moby Dick</u> via `symbolic_directory_paths`, as follows:


```python
# list records for two of the uploaded files via symbolic_directory_paths
list_output = pipeline.list(symbolic_directory_paths=["/novels/gothic", "/novels/adventure"])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "300cf157-a441-47e7-b36e-a3f63856533d",
      "message": "Successfully returned 2 items.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:28:06",
          "process_id": "0131ae96-424f-350e-eede-b9b9f6e60a7c",
          "created_at": "2024-06-05 15:28:06",
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
                  "num_lines": 12
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "melville"
            },
            {
              "category": "adventure"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/adventure",
          "pipeline": "list_method_1_parser",
          "file_id": "60d6e243-91bd-4561-a17d-291539cd651a",
          "expire_time": "2024-06-05 15:58:05",
          "file_name": "moby dick.txt"
        },
        {
          "last_updated": "2024-06-05 15:27:43",
          "process_id": "06cd2d57-22df-5d94-36e4-3133c4d757f7",
          "created_at": "2024-06-05 15:27:43",
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
          "pipeline": "list_method_1_parser",
          "file_id": "8abc402e-57ed-459d-af9c-918ae9dad038",
          "expire_time": "2024-06-05 15:57:41",
          "file_name": "frankenstein.txt"
        }
      ]
    }


As you can see, a full record for each file was returned. To learn more about each metadata item, visit the documentation for the [`process`](../parameters_processing_files_through_pipelines/process_method.md) method, where they are gone into detail on.

## Listing by `file_tags`

We can also list through `file_tags`.  We'll list for 19th century novels and any novels by 'Melville', as follows:


```python
# list records for two of the uploaded files via symbolic_directory_paths
list_output = pipeline.list(file_tags=[{"author": "Melville"}, {"century": "19"}])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "11bcf2d1-6c09-403d-8138-9c642fb3f4c2",
      "message": "Successfully returned 3 items.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:28:06",
          "process_id": "0131ae96-424f-350e-eede-b9b9f6e60a7c",
          "created_at": "2024-06-05 15:28:06",
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
                  "num_lines": 12
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "melville"
            },
            {
              "category": "adventure"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/adventure",
          "pipeline": "list_method_1_parser",
          "file_id": "60d6e243-91bd-4561-a17d-291539cd651a",
          "expire_time": "2024-06-05 15:58:05",
          "file_name": "moby dick.txt"
        },
        {
          "last_updated": "2024-06-05 15:27:58",
          "process_id": "f6ae9e98-bec4-2314-3d20-9116ec2a4baf",
          "created_at": "2024-06-05 15:27:58",
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
                  "num_lines": 9
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "austen"
            },
            {
              "category": "romance"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/romance",
          "pipeline": "list_method_1_parser",
          "file_id": "5b90a7c0-ccf8-4abf-b8ff-9eb7b755c2d2",
          "expire_time": "2024-06-05 15:57:58",
          "file_name": "pride and prejudice.txt"
        },
        {
          "last_updated": "2024-06-05 15:27:43",
          "process_id": "06cd2d57-22df-5d94-36e4-3133c4d757f7",
          "created_at": "2024-06-05 15:27:43",
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
          "pipeline": "list_method_1_parser",
          "file_id": "8abc402e-57ed-459d-af9c-918ae9dad038",
          "expire_time": "2024-06-05 15:57:41",
          "file_name": "frankenstein.txt"
        }
      ]
    }


Given that every file included the file tag `{"century": 19}` when initially processed, all four files were listed. <u>Little Women</u> also included the file tag `{"author": "Melville"}`, but there's no duplication of results, so that file's record is only listed once.

### Listing by `created_at` and `updated_at` Bookend Times

To illustrate how to `list` by timestamp bookends, let's first [`process`](../parameters_processing_files_through_pipelines/process_method.md) one additional file through our pipeline:


```python
# get current time
from datetime import datetime, timezone

time_now = datetime.now(tz=timezone.utc).strftime(format="%Y-%m-%d %H:%M:%S")

# process an additional file into earlier pipeline
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_very_short.txt",  # the initial local filepath where the input JSON file is stored
    local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
    verbose=False,  # do not display process update printouts upon running code
    symbolic_directory_path="/novels/dystopian",
    file_name="1984.txt",
    file_tags=[{"author": "Orwell"}, {"category": "dystopian"}, {"century": "20"}],
)
```

Listing by timestamp bookends is as straightforward as doing it by file system metadata. The following example only uses one type of bookend—`last_updated_start`—but all of them work the same way.

Based on the output from the file we just processed and the output from the four earlier files, we'll choose a time/date that falls in the middle of all five `last_updated` timestamps:


```python
# list process records by last_updated timestamp bookend
list_output = pipeline.list(created_at_start=time_now)

# nicely print the output of this list
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "f090a0e5-cfe6-42fb-b8ed-3272cda048c6",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:28:19",
          "process_id": "c3968a8c-c9de-f5dd-ea16-d81e80b3ef3f",
          "created_at": "2024-06-05 15:28:19",
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
                  "num_lines": 2
                }
              }
            },
            "pipeline_ordered_modules": [
              "parser"
            ],
            "pipeline_output_process_keys": [
              "snippet"
            ]
          },
          "file_tags": [
            {
              "author": "orwell"
            },
            {
              "category": "dystopian"
            },
            {
              "century": "20"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/dystopian",
          "pipeline": "list_method_1_parser",
          "file_id": "c3b610f7-1c22-4a7d-b2a1-4cb4ee7d5a6e",
          "expire_time": "2024-06-05 15:58:19",
          "file_name": "1984.txt"
        }
      ]
    }


Keep in mind that timestamp bookend arguments operate with **AND** logic: to be listed, a file _must_ fall within the specified timestamp window. This also means that if two timestamp arguments are provided and there is no overlap between them, the `list` method will return nothing.

### Wildcard Operator Arguments

The wildcard operator is the asterisk: *

You can use the wildcard operator * to `list` records whose exact metadata you don't remember—or if you wish to `list` records for a group of files that share similar metadata.

For `file_names` and `symbolic_directory_paths` a wildcard may be used as either prefix or suffix:

- Example * as a prefix: `*report.txt`
- Example * as a suffix: `/home/files/studies*`

Note that you don't necessarily have to attach full words to the wildcard operator *. The two above examples could thus instead be:

- Example * as a prefix: `*ort.txt`
- Example * as a suffix: `/home/files/studi*`

For `file_tags` a wildcard may be used for as the value in a key-value pair dictionary. This will return all records with the corresponding key.

- Example * in file_tags: `{"invoice_type": "*"}`

Let's dig into `list` method examples for each of these. First a prefix wildcard in `file_names`:


```python
# list process records using a wildcard prefix in file_names
list_output = pipeline.list(file_names=["*e.txt"])

# nicely print the output of this list
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "0d5eff98-3c4a-4419-b306-c57638549f4a",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:27:58",
          "process_id": "f6ae9e98-bec4-2314-3d20-9116ec2a4baf",
          "created_at": "2024-06-05 15:27:58",
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
                  "num_lines": 9
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "austen"
            },
            {
              "category": "romance"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/romance",
          "pipeline": "list_method_1_parser",
          "file_id": "5b90a7c0-ccf8-4abf-b8ff-9eb7b755c2d2",
          "expire_time": "2024-06-05 15:57:58",
          "file_name": "pride and prejudice.txt"
        }
      ]
    }


The above will return records for every file whose `file_name` ends with "e.txt".

Now a suffix wildcard in `symbolic_directory_paths`:


```python
# list process records using wildcard suffix in symbolic_directory_paths
list_output = pipeline.list(symbolic_directory_paths=["/my/*"])

# nicely print the output of this list
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "b6485d2e-5c54-4843-a454-8b2e363a96cc",
      "message": "No files were found for the given query arguments",
      "warnings": [
        {
          "WARNING: the following arguments returned zero results": [
            {
              "symbolic_directory_paths": [
                "/my/*"
              ]
            }
          ]
        }
      ],
      "items": []
    }


The above will return records for every file whose `symbolic_directory_path` begins with "/my/".

Now a wildcard operator in `file_tags`:


```python
# list process records using the wildcard operator in file_tags
list_output = pipeline.list(file_tags=[{"author": "*"}])

# nicely print the output of this list
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "820bedaa-dba3-44d4-9677-433dfa902395",
      "message": "Successfully returned 4 items.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-06-05 15:28:19",
          "process_id": "c3968a8c-c9de-f5dd-ea16-d81e80b3ef3f",
          "created_at": "2024-06-05 15:28:19",
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
                  "num_lines": 2
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "orwell"
            },
            {
              "category": "dystopian"
            },
            {
              "century": "20"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/dystopian",
          "pipeline": "list_method_1_parser",
          "file_id": "c3b610f7-1c22-4a7d-b2a1-4cb4ee7d5a6e",
          "expire_time": "2024-06-05 15:58:19",
          "file_name": "1984.txt"
        },
        {
          "last_updated": "2024-06-05 15:28:06",
          "process_id": "0131ae96-424f-350e-eede-b9b9f6e60a7c",
          "created_at": "2024-06-05 15:28:06",
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
                  "num_lines": 12
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "melville"
            },
            {
              "category": "adventure"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/adventure",
          "pipeline": "list_method_1_parser",
          "file_id": "60d6e243-91bd-4561-a17d-291539cd651a",
          "expire_time": "2024-06-05 15:58:05",
          "file_name": "moby dick.txt"
        },
        {
          "last_updated": "2024-06-05 15:27:58",
          "process_id": "f6ae9e98-bec4-2314-3d20-9116ec2a4baf",
          "created_at": "2024-06-05 15:27:58",
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
                  "num_lines": 9
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "austen"
            },
            {
              "category": "romance"
            },
            {
              "century": "19"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/romance",
          "pipeline": "list_method_1_parser",
          "file_id": "5b90a7c0-ccf8-4abf-b8ff-9eb7b755c2d2",
          "expire_time": "2024-06-05 15:57:58",
          "file_name": "pride and prejudice.txt"
        },
        {
          "last_updated": "2024-06-05 15:27:43",
          "process_id": "06cd2d57-22df-5d94-36e4-3133c4d757f7",
          "created_at": "2024-06-05 15:27:43",
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
          "pipeline": "list_method_1_parser",
          "file_id": "8abc402e-57ed-459d-af9c-918ae9dad038",
          "expire_time": "2024-06-05 15:57:41",
          "file_name": "frankenstein.txt"
        }
      ]
    }


The above will return records for every file that has a file_tag whose key is "author", regardless of the value.

You can also use the wildcard operator with the [`.show_tree`](show_tree_method.md) method, the [`.semantic_search`](../search_methods/semantic_search_method.md) method, and the [`.keyword_search`](../search_methods/keyword_search_method.md) method.

### The Global Root

As you might have surmised, there is one very special use of the wildcard operator on `symbolic_directory_path`s: we call it "the global root". It's leveraged by placing a wildcard operator * right after the root slash, and having nothing else, as follows:

```python
# example line of code with the global root
symbolic_directory_paths=['/*']
```

Listing the global root returns records for every single file in your pipeline.

### Using Multiple Arguments with the `list` method

As earlier mentioned, you can jointly use multiple input arguments with the `list` method. Multiple inputs are combined in a logical **OR** (if they are metadata arguments) or **AND** (if they are timestamp bookends) to retrieve records satisfying what's been requested.

As an example, let's combine a timestamp bookend, a `symbolic_file_path`, and `file_tags` in one `list` method invocation:


```python
# get current time
from datetime import datetime, timezone

time_now = datetime.now(tz=timezone.utc).strftime(format="%Y-%m-%d %H:%M:%S")

# list process records using a combination of input args
list_output = pipeline.list(
    created_at_end=time_now, symbolic_file_paths=["/novels/gothic/Pride and Prejudice.txt"], file_tags=[({"author": "Orwell"})]
)

# nicely print the output of this list
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "cf82edeb-51a1-4c77-8f1e-53a647660b9f",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [
        {
          "WARNING: the following arguments returned zero results": [
            {
              "symbolic_file_paths": [
                "/novels/gothic/pride and prejudice.txt"
              ]
            }
          ]
        }
      ],
      "items": [
        {
          "last_updated": "2024-06-05 15:28:19",
          "process_id": "c3968a8c-c9de-f5dd-ea16-d81e80b3ef3f",
          "created_at": "2024-06-05 15:28:19",
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
                  "num_lines": 2
                }
              }
            }
          },
          "file_tags": [
            {
              "author": "orwell"
            },
            {
              "category": "dystopian"
            },
            {
              "century": "20"
            }
          ],
          "file_description": "",
          "symbolic_directory_path": "/novels/dystopian",
          "pipeline": "list_method_1_parser",
          "file_id": "c3b610f7-1c22-4a7d-b2a1-4cb4ee7d5a6e",
          "expire_time": "2024-06-05 15:58:19",
          "file_name": "1984.txt"
        }
      ]
    }


Although <u>Pride and Prejudice</u> and <u>Little Women</u> are respectively covered by the `symbolic_file_paths` and `file_tags` arguments, neither of them falls within the indicated timestamp window. Consequently, they are both excluded from the above result.

### Output Size Cap

The current size limit on output generated by the `list` method is 5MB.
