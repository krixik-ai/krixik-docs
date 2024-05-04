## The `sentiment` module

This document reviews the `sentiment` module - which takes as input a json of string snippets and returns the snippets in a json along with their sentiment scores.

This document includes an overview of custom pipeline setup, current model set, parameters, and `.process` usage for this module.

To follow along with this demonstration be sure to initialize your krixik session with your api key and url as shown below. 

We illustrate loading these required secrets in via [python-dotenv](https://pypi.org/project/python-dotenv/), storing those secrets in a `.env` file.  This is always good practice for storing / loading secrets (e.g., doing so will reduce the chance you inadvertantly push secrets to a repo).

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [required input format](#required-input-format)
- [using the default model](#using-the-default-model)
- [using a non-default model](#using-a-non-default-model)


```python
# import utilities
import sys 
import json
import importlib
sys.path.append('../../')
reset = importlib.import_module("utilities.reset")
reset_pipeline = reset.reset_pipeline

# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os
load_dotenv("../../.env")
MY_API_KEY = os.getenv('MY_API_KEY')
MY_API_URL = os.getenv('MY_API_URL')

# import krixik and initialize it with your personal secrets
from krixik import krixik
krixik.init(api_key = MY_API_KEY, 
            api_url = MY_API_URL)
```

## Pipeline setup

Below we setup a simple one module pipeline using the `sentiment` module.

We do this by passing the module name to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(name="modules-sentiment-docs",
                                  module_chain=["sentiment"])
```

The `sentiment` module comes with a single model:

- `distilbert-base-uncased-finetuned-sst-2-english`: (default)

These available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).

## Required input format

This module accepts as input `.json` files consisting of a *list of dictionaries*.  Each dictionary may have as many key-value pairs as desired, but *must* contain the key name *snippet*.  This is the key `json-to-txt` will act on.

Let's look at an example of a small valid input - and then process it.


```python
# examine contents of a valid input file
test_file = "../../data/input/valid.json"
with open(test_file) as f:
  print(json.dumps(json.load(f), indent=2))
```

    [
      {
        "snippet": "I love this movie and i would watch it again and again!"
      },
      {
        "snippet": "Operating profit totaled EUR 9.4 mn, down from EUR 11.7 mn in 2004."
      }
    ]


## Using the default model

Let's process the small input file above using the default model - `base`.  Because `base` is the default model we need not input the optional `modules` argument into `.process`.


```python
# define path to an input file from examples directory
test_file = "../../data/input/valid.json"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory="../../data/output", # save output repo data output subdir
                                  expire_time=60 * 10,      # set all process data to expire in 10 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is text, the process output is provided in this object is null.  However the file itself has been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "my-sentiment-pipeline",
      "request_id": "e5209619-04c2-4662-9c4f-88fb8b7a0fe5",
      "file_id": "b0d0ab1c-8e86-4580-83bb-1ab0d9340255",
      "message": "SUCCESS - output fetched for file_id b0d0ab1c-8e86-4580-83bb-1ab0d9340255.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "I love this movie and i would watch it again and again!",
          "positive": 1.0,
          "negative": 0.0,
          "neutral": 0.0
        },
        {
          "snippet": "Operating profit totaled EUR 9.4 mn, down from EUR 11.7 mn in 2004.",
          "positive": 0.021,
          "negative": 0.979,
          "neutral": 0.0
        }
      ],
      "process_output_files": [
        "../../data/output/b0d0ab1c-8e86-4580-83bb-1ab0d9340255.json"
      ]
    }


We load in the text file output from `process_output_files` below. 


```python
# load in process output from file
with open(process_output["process_output_files"][0]) as f:
  print(json.dumps(json.load(f), indent=2))
```

    [
      {
        "snippet": "I love this movie and i would watch it again and again!",
        "positive": 1.0,
        "negative": 0.0,
        "neutral": 0.0
      },
      {
        "snippet": "Operating profit totaled EUR 9.4 mn, down from EUR 11.7 mn in 2004.",
        "positive": 0.021,
        "negative": 0.979,
        "neutral": 0.0
      }
    ]


Here we see our two input sentences from the input have been concatenated successfully into a single text.
