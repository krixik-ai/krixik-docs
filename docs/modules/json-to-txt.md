## The `json-to-txt` module

This document reviews the `json-to-txt` module - which takes as input a json of string snippets, joins them into a single string separated by double spaces, and returns a text file document.

This document includes an overview of custom pipeline setup, current model set, parameters, and `.process` usage for this module.

To follow along with this demonstration be sure to initialize your krixik session with your api key and url as shown below. 

We illustrate loading these required secrets in via [python-dotenv](https://pypi.org/project/python-dotenv/), storing those secrets in a `.env` file.  This is always good practice for storing / loading secrets (e.g., doing so will reduce the chance you inadvertantly push secrets to a repo).


```python
# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os
load_dotenv("../.env")
MY_API_KEY = os.getenv('MY_API_KEY')
MY_API_URL = os.getenv('MY_API_URL')

# import krixik and initialize it with your personal secrets
from krixik import krixik
krixik.init(api_key = MY_API_KEY, 
            api_url = MY_API_URL)
```

This small function prints dictionaries very nicely in notebooks / markdown.


```python
# print dictionaries / json nicely in notebooks / markdown
import json
def json_print(data):
    print(json.dumps(data, indent=2))
```

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [required input format](#required-input-format)
- [using the default model](#using-the-default-model)

## Pipeline setup

Below we setup a simple one module pipeline using the `json-to-txt` module. 


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(name="my-json-to-txt-pipeline",
                                  module_chain=["json-to-txt"])
```

The `json-to-txt` module comes with a single model:

- `base`: (default) joins a json of text snippets into a single text separated by double spaces

These available modeling options and parameters are stored in our custom pipeline's configuration (described further in LINK HERE).  We can examine this configuration as shown below.


```python
# nicely print pipeline configuration
json_print(pipeline.config)
```

    {
      "pipeline": {
        "name": "my-json-to-txt-pipeline",
        "modules": [
          {
            "name": "json-to-txt",
            "models": [
              {
                "name": "base"
              }
            ],
            "defaults": {
              "model": "base"
            },
            "input": {
              "type": "json",
              "permitted_extensions": [
                ".json"
              ]
            },
            "output": {
              "type": "text"
            }
          }
        ]
      }
    }


Here we can see the models and their associated parameters available for use.

You can save this configuration to disk as well by executing


```python
pipeline.save("/valid/path/file.yml")
```

You can instantiate a pipeline directly from its configuration using the [.load_pipeline method](LINK HERE).

## Required input format

The `json-to-txt` module accepts as input `.json` files consisting of a *list of dictionaries*.  Each dictionary may have as many key-value pairs as desired, but *must* contain the key name *snippet*.  This is the key `json-to-txt` will act on.

Let's look at an example of a small valid input - and then process it.


```python
# examine contents of a valid input file
test_file = "../input_data/1984_very_short.json"
with open(test_file) as f:
    json_print(json.load(f))
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


This input file is a `.json` consisting of a *list of dictionaries*.  Each dictionary contains a key called *snippet* that will be acted on by the module.  All other key-value pairs are ignored.

## Using the default model

Let's process our test input file using the `default` model - `base`.  Because this is the default model we need not input the optional `modules` argument into `.process`.


```python
# define path to an input file from examples directory
test_file = "../input_data/1984_very_short.json"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is text, the process output is provided in this object is null.  However the file itself has been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "my-json-to-txt-pipeline",
      "request_id": "29d88652-6344-44c7-b18d-a24e623e2c5b",
      "file_id": "83f070ac-3efe-4a07-b39a-08859275d84c",
      "message": "SUCCESS - output fetched for file_id 83f070ac-3efe-4a07-b39a-08859275d84c.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "./83f070ac-3efe-4a07-b39a-08859275d84c.txt"
      ]
    }


We load in the text file output from `process_output_files` below. 


```python
# load in process output from file
import json
with open(process_output['process_output_files'][0], "r") as file:
    print(file.read())  
```

    It was a bright cold day in April, and the clocks were striking thirteen.
    Winston Smith, his chin nuzzled into his breast in an effort to escape the
    vile wind, slipped quickly through the glass doors of Victory Mansions,
    though not quickly enough to prevent a swirl of gritty dust from entering
    along with him.


Here we see that the module has merged the two *snippet* values from the input dictionaries.
