## overview of krixik system apis

In this document we use a small example to illustrate the usage of krixik system apis.  These are apis avaiilable with all pipelines built with krixik.

To follow along with this demonstration be sure to initialize your krixik session with your api key and url as shown below. 

We illustrate loading these required secrets in via [python-dotenv](https://pypi.org/project/python-dotenv/), storing those secrets in a `.env` file.  This is always good practice for storing / loading secrets (e.g., doing so will reduce the chance you inadvertantly push secrets to a repo).


```python
# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os
load_dotenv()
MY_API_KEY = os.getenv('MY_API_KEY')
MY_API_URL = os.getenv('MY_API_URL')

# import krixik and initialize it with your personal secrets
from krixik import krixik
krixik.init(api_key = MY_API_KEY, 
            api_url = MY_API_URL)
```

    SUCCESS: You are now authenticated.


This small function prints dictionaries very nicely in notebooks / markdown.


```python
# print dictionaries / json nicely in notebooks / markdown
import json
def json_print(data):
    print(json.dumps(data, indent=2))
```

A table of contents for the remainder of this document is shown below.

- [base pipeline setup](#base-pipeline-setup)
- [the `.process` method](#the-.process-method)
    - [core inputs to the `.process` method](#core-inputs-to-the-process-method)
    - [basic usage and output breakdown](#basic-usage-and-output-breakdown)
    - [optional input arguments](#optional-input-arguments)
    - [defaults when using `.process`](#defaults-when-using-process)
    - [automatic data type transformations](#automatic-data-type-transformations)
- [the `.process_status` method](#the-process_status-method)
- [the `.fetch_output` method](#the-fetch_output-method)
- [the `.list` method](#the-list-method)
    - [listing by `file_ids`](#listing-by-file_ids)
    - [listing by `file_names`](#listing-by-file_names)
    - [listing by `symbolic_directory_paths`](#listing-by-symbolic_directory_paths)
    - [listing by `file_tags`](#listing-by-file_tags)
    - [listing by `created_at` and `updated_at` bookend times](#listing-by-created_at-and-updated_at-bookend-times)
    - [wildcard arguments](#wildcard-arguments)
    - [using multiple arguments with `.list`](#using-multiple-arguments-with-list)
- [the `.update` method](#the-update-method)
- [the `.delete` method](#the-delete-method)
- [the `.show_tree` method](#the-show_tree-method)
- [the `.keyword_search` method](#the-keyword_search-method)
    [a simple keyword search pipeline](#a-simple-keyword-db-pipeline)
    [invoking the `keyword_search`  method](#invoking-the-keyword-db-method)
- [the `.semantic_search` method](#the-vector_search-method)
    [a simple vector search pipeline](#a-simple-vector-db-pipeline)
    [invoking the `vector_search`  method](#invoking-the-vector-db-method)

## Base pipeline setup

Below we setup a simple one module pipeline using the `parser` module, using the default `sentence` parser.  This parser takes in an input text file and splits into its constituent sentences.


```python
# import custom module creation tools
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# instantiate module
module_1 = Module(module_type="parser")

# create custom pipeline object
custom = CreatePipeline(name='parser-pipeline-1', 
                        module_chain=[module_1])

# pass the custom object to the krixik operator (note you can also do this by passing its config)
pipeline = krixik.load_pipeline(pipeline=custom)
```

We will use this `pipeline` object for illustrative purposes for the remainder of this document.

## the `.process` method

The `.process` api is available to every krixik pipeline.  This api is invoked whenever you want to process files through your defined pipeline.

### core inputs to the `.process` method

The api has five basic inputs, as well as a range of optional metdata.  These inputs are

- `local_file_path`:  (required) the path to the local file you wish to process
- `local_save_directory`: (optional) local location for saving process output (defaults to current working directory)
 - `expire_time`: (optional) length of time process output remains on krixik servers (default is 30 minutes / 1800 seconds)
- `wait_for_process`: (optional) whether or not to wait for your process to complete before regaining control of your IDE or notebook - `True` means wait until the process is complete, `False` means regain control immediately after your file has uploaded for processing (default `True`)  When set to `False` the status of processing can be retrieved via the `.process_status` api [LINK HERE]
- `verbose`: (optional) whether to show process update printouts at your terminal / notebook (default `True`)

Lets process a simple file using these core inputs.

### basic usage and output breakdown

We first define a path to a local input file.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"
```

Lets take a quick look at this file before processing.


```python
# examine contents of input file
with open(test_file, "r") as file:
    print(file.read())
```

    It was a bright cold day in April, and the clocks were striking thirteen.
    Winston Smith, his chin nuzzled into his breast in an effort to escape the
    vile wind, slipped quickly through the glass doors of Victory Mansions,
    though not quickly enough to prevent a swirl of gritty dust from entering
    along with him.


A paragraph of text consisting of two sentences.

Now let's process it using our sentence parser and explore `.process` inputs.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is json, the process output is provided in the return response.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "parser-pipeline-1",
      "request_id": "e957e17f-ca3c-40bf-afd1-ebca1f27ba51",
      "file_id": "9d94d011-b445-41fa-ae9e-92322726be96",
      "message": "SUCCESS - output fetched for file_id 9d94d011-b445-41fa-ae9e-92322726be96.Output saved to location(s) listed in process_output_files.",
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
        "./9d94d011-b445-41fa-ae9e-92322726be96.json"
      ]
    }


Lets break down the output:

- `status_code`: provides the success / failure signal for the api
- `pipeline`: the name of the pipeline we ran `.process` on
- `request_id`: unique id associated with this execution of `.process`
- `file_id`: unique id for the processed file and its associated output
- `message`: message detailing success or failure of call
- `warnings`: message list indicating any warnings related to our call
- `process_output`: returned output (available when module-model output is json only)
- `process_output_files`: list of process output, local file names 

We can see from `process_output` that our two-sentence paragraph input has been separated correctly.  Each sentence also has its corresponding line number(s).

This process output is also stored in the file contained in `process_output_files`.  Lets load it in and confirm we have the same process output we see above.


```python
# load in process output from file
import json
with open(process_output['process_output_files'][0], "r") as file:
    process_output = json.load(file)
    json_print(process_output)
```

    [
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
    ]


### optional input arguments

 When using the api you may optionally include a variety of process metadata.  
 
These optional do not change how `.process` runs or treats input / output data - they make your process output easier to retrieve and organize.   

Optional inputs include

- `modules`: model and parameter selections for pipeline modules
- `symbolic_directory_path` - a unix formatted directory path (default is `/etc`)
- `file_name` - a custom file name (randomly assigned name by default)
- `file_tags` - a list of custom file tags (none by default)
- `file_description` - a custom file description (none by default)

These three arguments  - `symbolic_directory_path`, `file_name`, and `file_tags` - can be used to retrieve the record of your process at a later time using the [`.list` method](list.md).  They can also be used as filters for search if your pipeline ends with a `keyword-db` [LINK HERE] or `vector-db` [LINK HERE] module.

The `file_description` can be used to provide a description of the file.

Lets use the `.process` method with and without these arguments.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for parser
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,            # set verbosity to False
                                  symbolic_directory_path = "/my/custom/filepath",
                                  file_name = "some_snippets.txt",
                                  file_tags = [{"author": "orwell"}, {"category": "fiction"}],
                                  file_description = "the first paragraph of 1984")
```

The `modules` argument is optional since when not set default model options are made for each module in a pipeline.

To use any non-default model you must define the `modules` input argument when using `.process`.  

For example, the `parser` module has a secondary model called `fixed` which takes in two parameters.  You can employ it in an invocation of `.process` like this (see the [`parser` example](LINK HERE) for further information).

```python
# process using parser
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,            # set verbosity to False
                                  symbolic_directory_path = "/my/custom/filepath",
                                  file_name = "some_snippets.txt",
                                  file_tags = [{"author": "orwell"}, {"category": "fiction"}],
                                  file_description = "the first paragraph of 1984",
                                  modules={"parser":{"model":"fixed",
                                                     "params":{
                                                         "chunk_size": 10,
                                                         "overlap_size": 2
                                                     }}})
```



### defaults when using `.process`

- if no `file_name` is provided a random name is provided for the process input file of the form `krixik_generated_file_name_{10 random chars}.ext`
where here `ext` is the extension of your input provided by `local_file_path`

- if no value for `symbolic_directory_path` is provided it is set to the default value of `/etc`

- you cannot define `symbolic_directory_path`s that are children of `/etc` - e.g., `/etc/mypath` is not allowed

### automatic data type transformations

The `.process` method automatically transforms the following input data types from `local_file_path`

- `pdf` -> `txt`
- `docx` -> `txt`
- `pptx` -> `txt`
- `mp4` -> `mp3`


## the `.process_status` method

The `.process_status` method lets you check the status of a pipeline usage of `.process` via a `request_id`.  This is epically useful when using `.process` with `wait_for_process` set to `False` [LINK HERE].

To illustrate its usage, let us first process a file with our pipeline using `wait_for_process` set to `False`.  This will give us back control of our IDE / notebook as soon as the file has completed upload. 


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".",  # save output in current directory
                                  expire_time=60*5,          # set all process data to expire in 5 minutes
                                  wait_for_process=False,    # do not wait for process to complete before regaining ide
                                  verbose=False)             # set verbosity to False
```

Let us quickly examine the returned output.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "file_id": "ce251869-5026-4026-ad40-35e2af5e73eb",
      "request_id": "bcda2f5b-aaf9-5242-98d6-32e5fedbf5ff",
      "file_name": "krixik_generated_file_name_hzufejnxft.txt",
      "symbolic_directory_path": "/etc",
      "file_tags": null,
      "file_description": null
    }


Now we can check the status of our process using returned `request_id` and the `.process_status` as shown below.


```python
# use .process_status
status_output = pipeline.process_status(request_id=process_output["request_id"])

# nicely print the output of this process
json_print(status_output)
```

    {
      "status_code": 200,
      "request_id": "398f4ad1-bb93-4b4b-bfa4-8a26e618a068",
      "file_id": "ce251869-5026-4026-ad40-35e2af5e73eb",
      "message": "SUCCESS: process_status found",
      "pipeline": "parser-pipeline-1",
      "process_status": {
        "parser": true
      },
      "overall_status": "complete"
    }


Here we can see that the status of our single module has not yet completed.

If we wait a few moments and try again, we will see confirmation that the process completed successfully.


```python
# use .process_status
status_output = pipeline.process_status(request_id=process_output["request_id"])

# nicely print the output of this process
json_print(status_output)
```

    {
      "status_code": 200,
      "request_id": "4f91cc57-9df7-4faa-bbfd-57fc3abd9a50",
      "file_id": "ce251869-5026-4026-ad40-35e2af5e73eb",
      "message": "SUCCESS: process_status found",
      "pipeline": "parser-pipeline-1",
      "process_status": {
        "parser": true
      },
      "overall_status": "complete"
    }


## the `.fetch_output` method

The `.fetch_output` method is used to download the output of a pipeline process.  This is particularly useful when using `.process` with `wait_for_process` set to `False`, as your output is not immediately pulled.

Lets see how this works by processing a file with `wait_for_process` set to `False`.  We will first use `.process_status` [LINK HERE] to make sure the file has completed processing.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  expire_time=60*5,          # set all process data to expire in 5 minutes
                                  wait_for_process=False,    # do not wait for process to complete before regaining ide
                                  verbose=False)             # set verbosity to False
```

Now we check the status of our process via the returned `request_id`.


```python
# use .process_status
status_output = pipeline.process_status(request_id=process_output["request_id"])

# nicely print the output of this process
json_print(status_output)
```

    {
      "status_code": 200,
      "request_id": "9f81bcbc-f523-48a8-a33a-5669547401af",
      "file_id": "1488dd6d-4bc5-4d61-b7d5-ff5262fce5f1",
      "message": "SUCCESS: process_status found",
      "pipeline": "parser-pipeline-1",
      "process_status": {
        "parser": false
      },
      "overall_status": "ongoing"
    }


Since the file has completed processing we can now use `.fetch_output`.

`.fetch_output` takes in a two inputs

 - the `file_id` of the uploaded and processed file
 - a `local_save_directory` (optional) where the completed files will be saved locally (default is current working directory)


```python
# fetch the output of our process using file_id
fetch_output = pipeline.fetch_output(file_id=process_output["file_id"],
                                     local_save_directory=".")
```

Printing the fetched output return we have our json returned in the `fetch_output` key-value.  

The `process_output_files` key-value pair shows the download location(s) of our completed process files pulled by `.fetch_output`.


```python
# nicely print the output of this process
json_print(fetch_output)
```

    {
      "status_code": 200,
      "pipeline": "parser-pipeline-1",
      "request_id": "66cacfdf-f4a8-4061-9322-50489d5d9670",
      "file_id": "1488dd6d-4bc5-4d61-b7d5-ff5262fce5f1",
      "message": "SUCCESS - output fetched for file_id 1488dd6d-4bc5-4d61-b7d5-ff5262fce5f1.Output saved to location(s) listed in process_output_files.",
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
        "./1488dd6d-4bc5-4d61-b7d5-ff5262fce5f1.json"
      ]
    }


## the `.list` method

After using `.process` [LINK HERE] to process a file with your chosen pipeline, you can retrieve the associated record if this file using `list` method using its `file_id` and any other optional metadata you included.

You can list multiple records with a single execution of `.list`, hence the inputs into `.list` are as follows:

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

Let start by processing a file, including optinoal metadata so that we can retrieve it via several core inputs.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,            # set verbosity to False
                                  symbolic_directory_path = "/my/custom/filepath",
                                  file_name = "some_snippets.txt",
                                  file_tags = [{"author": "orwell"}, {"category": "fiction"}],
                                  file_description = "the first paragraph of 1984")
```

### listing by `file_ids`

First we list the record of this process using its `file_id`.

Notice we place this in a list, since in practice we can call `.list` on a list of `file_id`'s.


```python
# list process records
list_output = pipeline.list(file_ids=[process_output["file_id"]])

# nicely print the output of this process
json_print(list_output)
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


### listing by `file_names`

We can also list this file via its `file_name`.  Again we place it in a list, since in practice we may provide a list of `file_name`'s to `.list`.


```python
# list process records
list_output = pipeline.list(file_names=["some_snippets.txt"])

# nicely print the output of this process
json_print(list_output)
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


### listing by `symbolic_directory_paths`

We can also list this file via its `symbolic_directory_path`.  Again we place it in a list, since in practice we may provide a list of `symbolic_directory_path`'s to `.list`.


```python
# list process records
list_output = pipeline.list(symbolic_directory_paths=["/my/custom/filepath"])

# nicely print the output of this process
json_print(list_output)
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


### listing by `file_tags`

We can also list this file via its `file_tags`.  Again we place it in a list, since in practice we may provide a list of `file_tags`'s to `.list`.


```python
# list process records
list_output = pipeline.list(file_tags=[{"author": "orwell"}])

# nicely print the output of this process
json_print(list_output)
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


### listing by `created_at` and `updated_at` bookend times

To illustrate how to list by timestamp bookends we first process a file and record the current time (in UTC timezone).


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
json_print(list_output)
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


### wildcard arguments

You can use wildcard * to use fuzzy matching with your record selection as well.

For `file_names` and `symbolic_directory_paths` a wildcard may be used as both prefix and suffix.

For `file_tags` a wildcard may be used for the value of a tag dictioary to search across all records with a corresopnding key.


```python
# list process records using wildcard(s)
list_output = pipeline.list(file_names=["some*"])

# nicely print the output of this process
json_print(list_output)
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
json_print(list_output)
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
json_print(list_output)
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


### using multiple arguments with `.list`

You can use multiple input arguments jointly with `.list`.  Multiple inputs are combined in a logical AND to retrieve records satisfying all input requirements.


```python
# list process records using a mix of input args
list_output = pipeline.list(file_names = ["some*"],
                            symbolic_directory_paths=["/my/*"])

# nicely print the output of this process
json_print(list_output)
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


## the `.update` method

You can update the metadata of a file using the `update` method.  This method takes in the `file_id` of the file you would like to update, and the metadata you would like to update.  

You can update any of the following metadata: `expire_time`,  `symbolic_directory_path`, `file_name`, `file_tags`, or `file_description` of the associated file using this method.

We illustrate the use of `.update` by first processing a simple file.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,            # set verbosity to False
                                  symbolic_directory_path = "/my/custom/filepath",
                                  file_name = "some_snippets_3.txt",
                                  file_tags = [{"author": "orwell"}, {"category": "fiction"}],
                                  file_description = "the first paragraph of 1984")
```

Next we use `.update` to change its `file_name`.


```python
# update a process record metadata
update_output = pipeline.update(file_id=process_output["file_id"],
                                file_name="a_new_filename.txt")

# nicely print the output of this process
json_print(update_output)
```

    {
      "status_code": 200,
      "pipeline": "parser-pipeline-1",
      "request_id": "4201b289-9088-42e3-a0ec-8053b9190ba3",
      "message": "Successfully updated file metadata",
      "warnings": []
    }


Now if we use `.list` [LINK HERE] we can check that our record metadata has been changed.


```python
# list process records
list_output = pipeline.list(file_ids=[process_output["file_id"]])

# nicely print the output of this process
json_print(list_output)
```

    {
      "status_code": 200,
      "request_id": "53c2fc7b-8b84-4128-a34e-1e4de4ceff94",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-04-26 21:06:32",
          "process_id": "461bfe88-0064-13b1-2728-7f5a371092cf",
          "created_at": "2024-04-26 21:05:42",
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
          "file_id": "ca3ca26c-7b76-4fd2-a1f1-3c86d8eb443a",
          "expire_time": "2024-04-26 21:10:42",
          "file_name": "a_new_filename.txt"
        }
      ]
    }


## the `.delete` method

You can delete the record of your process on demand using the `delete` method.  This will remove all record of the process from our servers.  This is the manual version of letting the `expire_time` run out on a file.

The `.delete` method takes in a single argument: the `file_id` of the file you wish to delete.

We will illustrate its usage by processing a simple file, deleting it using the `.delete` method, and then checking that it no longer exists using the `.list` method [LINK HERE].


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False)
```

Now we delete this process record and its output via its `file_id`.


```python
# delete process record and output by file_id
delete_output = pipeline.delete(file_id=process_output["file_id"])

# nicely print the output of this process
json_print(delete_output)
```

    {
      "status_code": 200,
      "pipeline": "parser-pipeline-1",
      "request_id": "693d3da8-1e0d-4f24-b85a-2c8287320b51",
      "message": "Successfully deleted file_id: ddb925f3-8cfb-4fdc-bd10-dbb68adecb04",
      "warnings": []
    }


Now we can check that the file has been deleted using `.list`.


```python
# list process records
list_output = pipeline.list(file_ids=[process_output["file_id"]])

# nicely print the output of this process
json_print(list_output)
```

    {
      "status_code": 200,
      "request_id": "b4f69db4-fece-4b3d-8184-420ebfd912d2",
      "message": "No items found for input query arguments",
      "warnings": [
        {
          "WARNING: the following file_ids were not found": [
            "ddb925f3-8cfb-4fdc-bd10-dbb68adecb04"
          ]
        }
      ],
      "items": []
    }


## the `.show_tree` method

`show_tree` is a convenience function for visualizing - at your terminal or IDE output - your un-expired pipeline files.  It is designed as a simple analog to the standard unix [tree command](https://www.tecmint.com/linux-tree-command-examples/).

To illustrate its usage we first process several files.


```python
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,
                                  symbolic_directory_path="/my/custom/path",
                                  file_name="file_num_one.txt")   

process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,
                                  symbolic_directory_path="/my/custom/path",
                                  file_name="file_num_two.txt")   

process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,
                                  symbolic_directory_path="/my/custom/path/subpath",
                                  file_name="file_num_three.txt")   
```

Now we can visualize our pipeline process file directory structure using `show_tree`.

`show_tree` takes in a single argument - `symbolic_directory_path`.  You can enter a path or stump (path + wildcard) to see all files and directories at or below the input path.


```python
# show the directory structure of a pipeline process file directory
show_tree_output = pipeline.show_tree(symbolic_directory_path='/*')
```

    /
    └── /my
        └── /custom
            └── /path
                ├── file_num_one.txt
                ├── file_num_two.txt
                └── /subpath
                    └── file_num_three.txt


## the `.keyword_search` method

The `.keyword_search` method can be used with any pipeline that ends with `keyword-db` module.

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

### invoking the `keyword_search`  method 

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


Note that we did not define a `file_name` or `symbolic_directory_path` ourselves, so defaults will be given as described in the `.process` walkthrough [LINK HERE].

Here the `process_output` key value is `null` since the return object is a database.  We can see this database in the local location provided in the `process_output_files` value.

With `.process` complete we can run `keyword_search` on our input file. 

The `keyword_search` method takes in the exact same arguments as `.list` [LINK HERE] - that is `file_ids`, `file_names`, etc., - plus one additional argument: `query`.  The `query` is a string of words to be queried individually.

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

## the `.semantic_search` method

krixik's `.semantic_search` method is a convenience function for both embedding and querying - and can be used with any pipeline containing a consecutive pair of []`text-embedder`](LINK HERE) and [`vector-db`](LINK HERE) modules.

### a simple vector search pipeline

Below we construct the simplest custom pipeline that satisfies this criteria - a standard vector search pipeline consisting of three modules: a `parser`, `text-embedder`, and `vector-db` index.


```python
# import custom module creation tools
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# instantiate module
module_1 = Module(module_type="parser")
module_2 = Module(module_type="text-embedder")
module_3 = Module(module_type="vector-db")

# create custom pipeline object
custom = CreatePipeline(name='vector-db-pipeline-1', 
                        module_chain=[module_1, module_2, module_3])

# pass the custom object to the krixik operator (note you can also do this by passing its config)
pipeline = krixik.load_pipeline(pipeline=custom)
```

### invoking the `vector_search`  method 

We can now perform any of the core system methods on our custom pipeline (e.g., `.process`, `.list`, etc.,).  Additionally we can invoke the `vector_search` method.

Lets first process a file with our new pipeline.  The `vector-db` module takes in a text file, and returns `faiss` vector database consisting of all non-trivial `(snippet, line_numbers)` tuples from the input.


```python
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
      "pipeline": "vector-db-pipeline-1",
      "request_id": "1a09068c-872a-4389-a399-7281e2d1764e",
      "file_id": "f69aac3d-e674-45d5-ab33-f16196ce82b2",
      "message": "SUCCESS - output fetched for file_id f69aac3d-e674-45d5-ab33-f16196ce82b2.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "./f69aac3d-e674-45d5-ab33-f16196ce82b2.faiss"
      ]
    }


Note that we did not define a `file_name` or `symbolic_directory_path` ourselves, so defaults will be given as described in the `.process` walkthrough [LINK HERE].

Here the `process_output` key value is `null` since the return object is a database.  We can see this database in the local location provided in the `process_output_files` value.

With `.process` complete we can run `vector_search` on our input file. 

The `vector_search` method takes in the exact same arguments as `.list` [LINK HERE] - that is `file_ids`, `file_names`, etc., - plus one additional argument: `query`.  The `query` is a string of words to be queried individually.

Let's look at an example.


```python
# perform vector_search over the input file
vector_output = pipeline.semantic_search(query="it was cold night",
                                        file_ids=[process_output["file_id"]])

# nicely print the output of this process
json_print(vector_output)
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


Here we can see one returned search result in `items`.
