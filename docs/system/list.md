## The `list` method

After using [`process`](system/process.md) to process a file with your chosen pipeline, you can retrieve the associated record if this file using `list` method using its `file_id` and any other optional metadata you included.  

This document reviews the `list` method available to every krixik pipeline.

A table of contents for the remainder of this document is shown below.


- [basic pipeline setup](#basic-pipeline-setup)
- [basic usage, required input, and output breakdown](#basic-usage,-required-input,-and-output-breakdown)
- [listing by `file_ids`](#listing-by-file_ids)
- [listing by `file_names`](#listing-by-file_names)
- [listing by `symbolic_directory_paths`](#listing-by-symbolic_directory_paths)
- [listing by `file_tags`](#listing-by-file_tags)
- [listing by `created_at` and `updated_at` bookend times](#listing-by-created_at-and-updated_at-bookend-times)
- [wildcard arguments](#wildcard-arguments)
- [using multiple arguments with `list`](#using-multiple-arguments-with-list)


```python
# import utilities
import sys
import json
import importlib

sys.path.append("../../")
reset = importlib.import_module("utilities.reset")
reset_pipeline = reset.reset_pipeline

# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os

load_dotenv("../../.env")
MY_API_KEY = os.getenv("MY_API_KEY")
MY_API_URL = os.getenv("MY_API_URL")

# import krixik and initialize it with your personal secrets
from krixik import krixik

krixik.init(api_key=MY_API_KEY, api_url=MY_API_URL)
```

## Basic pipeline setup

For this document we will use a pipeline consisting of a single [`parser` module](modules/parser.md).  We use [`create_pipeline`](system/create_save_load.md) to instantiate the pipeline.


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(name="system-list-docs", module_chain=["parser"])
```


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```

## Basic usage, required input, and output breakdown

To illustrate the usage of `list` we process a short file illustrated in the introduction to the [`parser` method](modules/parser.md).


```python
# define path to an input file from examples directory
test_file = "../../data/input/1984_very_short.txt"

# process short input file
process_output = pipeline.process(
    local_file_path=test_file,
    local_save_directory="../../data/output",  # save output repo data output subdir
    expire_time=60 * 10,  # set all process data to expire in 10 minutes
    wait_for_process=True,  # wait for process to complete before regaining ide
    verbose=False,  # set verbosity to False
    symbolic_directory_path="/my/custom/filepath",
    file_name="some_snippets.txt",
    file_tags=[{"author": "orwell"}, {"category": "fiction"}],
    file_description="the first paragraph of 1984",
)
```

Let us examine the returned output.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```


    '{\n  "file_id": "3d435c55-05ae-41b6-aee3-76da8c7b0841",\n  "request_id": "5e723bee-4939-21f1-52ef-ca0596dd3f1f",\n  "file_name": "krixik_generated_file_name_vplttsahnp.txt",\n  "symbolic_directory_path": "/etc",\n  "file_tags": null,\n  "file_description": null\n}'


You can list multiple records with a single execution of `list`, hence the inputs into `list` are as follows:

- `file_ids`: (optional) a list of `file_id`'s to return records for
- `file_names`: (optional) a list of `file_id`'s to return records for
- `symbolic_directory_paths`: (optional) a list of `symbolic_directory_paths`'s to return records for
- `symbolic_file_paths`: (optional) a list of `symbolic_directory_path/file_name`'s to return records for
- `file_tags`: (optional) a list of `file_tags`'s to return records for

You may use wildcard operators with `file_names`, `symbolic_directory_paths`,`symbolic_file_paths`, and `file_tags` to retrieve records with fuzzy matching.

You may also list by bookends on the creation and last updated times of your records.  These include:

- `created_at_start`: the earliest `created_at` time for record you wish to retrieve
- `created_at_end`: the latest `created_at` time for record you wish to retrieve
- `last_updated_start`: the earliest `last_updated` time for record you wish to retrieve
- `last_updated_end`: the latest `last_updated` time for record you wish to retrieve

Moreover you may *mix* these arguments to retrieve records for very specific tranches of your process data.

## Listing by `file_ids`

First we list the record of this process using its `file_id`.

Notice we place this in a list, since in practice we can call `.list` on a list of `file_id`'s.


```python
# list process records
list_output = pipeline.list(file_ids=[process_output["file_id"]])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "11dcf756-702c-421c-a85a-49dabc2cca7f",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-04-26 21:05:05",
          "process_id": "578cb0a2-0f19-4d83-4b05-3c543f5e2506",
          "created_at": "2024-04-26 21:05:05",
          "file_metadata": {
            "modules": {
              "parser": {
                "model": "sentence"
              }
            },
            "modules_data": {
              "parser": {
                "data_files_extensions": [
                  ".json"
                ]
              }
            }
          },
          "file_tags": [
            {
              "author": "orwell"
            },
            {
              "category": "fiction"
            }
          ],
          "file_description": "the first paragraph of 1984",
          "symbolic_directory_path": "/my/custom/filepath",
          "pipeline": "parser-pipeline-1",
          "file_id": "fb228e8e-eefd-4c52-b966-a49506d63f34",
          "expire_time": "2024-04-26 21:10:05",
          "file_name": "some_snippets.txt"
        }
      ]
    }


## Listing by `file_names`

We can also list this file via its `file_name`.  Again we place it in a list, since in practice we may provide a list of `file_name`'s to `.list`.


```python
# list process records
list_output = pipeline.list(file_names=["some_snippets.txt"])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "764587e3-7212-429b-baeb-0ba824797fa6",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-04-26 21:05:05",
          "process_id": "578cb0a2-0f19-4d83-4b05-3c543f5e2506",
          "created_at": "2024-04-26 21:05:05",
          "file_metadata": {
            "modules": {
              "parser": {
                "model": "sentence"
              }
            },
            "modules_data": {
              "parser": {
                "data_files_extensions": [
                  ".json"
                ]
              }
            }
          },
          "file_tags": [
            {
              "author": "orwell"
            },
            {
              "category": "fiction"
            }
          ],
          "file_description": "the first paragraph of 1984",
          "symbolic_directory_path": "/my/custom/filepath",
          "pipeline": "parser-pipeline-1",
          "file_id": "fb228e8e-eefd-4c52-b966-a49506d63f34",
          "expire_time": "2024-04-26 21:10:05",
          "file_name": "some_snippets.txt"
        }
      ]
    }


## Listing by `symbolic_directory_paths`

We can also list this file via its `symbolic_directory_path`.  Again we place it in a list, since in practice we may provide a list of `symbolic_directory_path`'s to `.list`.


```python
# list process records
list_output = pipeline.list(symbolic_directory_paths=["/my/custom/filepath"])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "70c71a76-7ce9-43c7-86e7-838b7fa93d8e",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-04-26 21:05:05",
          "process_id": "578cb0a2-0f19-4d83-4b05-3c543f5e2506",
          "created_at": "2024-04-26 21:05:05",
          "file_metadata": {
            "modules": {
              "parser": {
                "model": "sentence"
              }
            },
            "modules_data": {
              "parser": {
                "data_files_extensions": [
                  ".json"
                ]
              }
            }
          },
          "file_tags": [
            {
              "author": "orwell"
            },
            {
              "category": "fiction"
            }
          ],
          "file_description": "the first paragraph of 1984",
          "symbolic_directory_path": "/my/custom/filepath",
          "pipeline": "parser-pipeline-1",
          "file_id": "fb228e8e-eefd-4c52-b966-a49506d63f34",
          "expire_time": "2024-04-26 21:10:05",
          "file_name": "some_snippets.txt"
        }
      ]
    }


## Listing by `file_tags`

We can also list this file via its `file_tags`.  Again we place it in a list, since in practice we may provide a list of `file_tags`'s to `.list`.


```python
# list process records
list_output = pipeline.list(file_tags=[{"author": "orwell"}])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "7915929d-47cc-4fb9-82f6-b737ad823458",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-04-26 21:05:05",
          "process_id": "578cb0a2-0f19-4d83-4b05-3c543f5e2506",
          "created_at": "2024-04-26 21:05:05",
          "file_metadata": {
            "modules": {
              "parser": {
                "model": "sentence"
              }
            },
            "modules_data": {
              "parser": {
                "data_files_extensions": [
                  ".json"
                ]
              }
            }
          },
          "file_tags": [
            {
              "author": "orwell"
            },
            {
              "category": "fiction"
            }
          ],
          "file_description": "the first paragraph of 1984",
          "symbolic_directory_path": "/my/custom/filepath",
          "pipeline": "parser-pipeline-1",
          "file_id": "fb228e8e-eefd-4c52-b966-a49506d63f34",
          "expire_time": "2024-04-26 21:10:05",
          "file_name": "some_snippets.txt"
        }
      ]
    }


## Listing by `created_at` and `updated_at` bookend times

To illustrate how to list by timestamp bookends we first process a file and record the current time (in UTC timezone).


```python
# define path to an input file from examples directory
test_file = "../../data/input/1984_very_short.txt"

# process for search
process_output = pipeline.process(
    local_file_path=test_file,
    local_save_directory="../../data/output",  # save output repo data output subdir
    expire_time=60 * 10,  # set all process data to expire in 10 minutes
    wait_for_process=True,  # wait for process to complete before regaining ide
    verbose=False,
)  # set verbosity to False

# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "parser-pipeline-1",
      "request_id": "d3bca30e-d260-4c62-8aa9-91307b21d8b1",
      "file_id": "3b941b6f-bd05-4fbb-83fd-6fea80c25629",
      "message": "SUCCESS - output fetched for file_id 3b941b6f-bd05-4fbb-83fd-6fea80c25629.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
          "line_numbers": [
            1
          ]
        },
        {
          "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
          "line_numbers": [
            2,
            3,
            4,
            5
          ]
        }
      ],
      "process_output_files": [
        "./3b941b6f-bd05-4fbb-83fd-6fea80c25629.json"
      ]
    }


We can now list by the `created_at` and `last_updated` timestamps - using bookends `_start` and/or `_end`.


```python
# list process records
list_output = pipeline.list(created_at_start=list_output["items"][0]["created_at"])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "aacbb5e9-4701-454b-be2d-16d0f812a201",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-04-26 21:05:21",
          "process_id": "132561f2-336b-c889-ba9e-500df80fdd38",
          "created_at": "2024-04-26 21:05:21",
          "file_metadata": {
            "modules": {
              "parser": {
                "model": "sentence"
              }
            },
            "modules_data": {
              "parser": {
                "data_files_extensions": [
                  ".json"
                ]
              }
            },
            "pipeline_ordered_modules": [
              "parser"
            ],
            "pipeline_output_process_keys": [
              "snippet"
            ]
          },
          "file_tags": [],
          "file_description": "",
          "symbolic_directory_path": "/etc",
          "pipeline": "parser-pipeline-1",
          "file_id": "3b941b6f-bd05-4fbb-83fd-6fea80c25629",
          "expire_time": "2024-04-26 21:10:21",
          "file_name": "krixik_generated_file_name_zqdsvltyrw.txt"
        }
      ]
    }


## Wildcard arguments

You can use wildcard * to use fuzzy matching with your record selection as well.

For `file_names` and `symbolic_directory_paths` a wildcard may be used as both prefix and suffix.

For `file_tags` a wildcard may be used for the value of a tag dictioary to search across all records with a corresopnding key.


```python
# list process records using wildcard(s)
list_output = pipeline.list(file_names=["some*"])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "341c4e07-62a6-47f0-904b-7ff2ee3bbaef",
      "message": "No files were found for the given query arguments",
      "warnings": [
        {
          "WARNING: the following arguments returned zero results": [
            {
              "file_names": [
                "some*"
              ]
            }
          ]
        }
      ],
      "items": []
    }



```python
# list process records using wildcard(s)
list_output = pipeline.list(symbolic_directory_paths=["/my/*"])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "b6d53064-2748-4c3a-ac7a-e0325cf8c58f",
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



```python
# list process records using wildcard(s)
list_output = pipeline.list(file_tags=[{"author": "*"}])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "de17823f-5601-4143-b2ae-c546c173cdc7",
      "message": "No files were found for the given query arguments",
      "warnings": [
        {
          "WARNING: the following arguments returned zero results": [
            {
              "file_tags_keys": [
                "author"
              ]
            }
          ]
        }
      ],
      "items": []
    }


## Using multiple arguments with `list`

You can use multiple input arguments jointly with `list`.  Multiple inputs are combined in a logical AND to retrieve records satisfying all input requirements.


```python
# list process records using a mix of input args
list_output = pipeline.list(file_names=["some*"], symbolic_directory_paths=["/my/*"])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "091a2b5e-4d2f-44cd-9fcf-65a0c80546b7",
      "message": "No files were found for the given query arguments",
      "warnings": [
        {
          "WARNING: the following arguments returned zero results": [
            {
              "symbolic_directory_paths": [
                "/my/*"
              ]
            },
            {
              "file_names": [
                "some*"
              ]
            }
          ]
        }
      ],
      "items": []
    }



```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
