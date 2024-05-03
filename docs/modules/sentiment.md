## The `sentiment` module

This document reviews the `sentiment` module - which takes as input a json of string snippets and returns the snippets in a json along with their sentiment scores.

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
- [using a non-default model](#using-a-non-default-model)

## Pipeline setup

Below we setup a simple one module pipeline using the `sentiment` module. 


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(name="my-sentiment-pipeline",
                                  module_chain=["sentiment"])
```

The `sentiment` module comes with a single model:

- `distilbert-base-uncased-finetuned-sst-2-english`: (default)

These available modeling options and parameters are stored in our custom pipeline's configuration (described further in LINK HERE).  We can examine this configuration as shown below.


```python
# nicely print pipeline configuration
json_print(pipeline.config)
```

    {
      "pipeline": {
        "name": "my-sentiment-pipeline",
        "modules": [
          {
            "name": "sentiment",
            "models": [
              {
                "name": "distilbert-base-uncased-finetuned-sst-2-english"
              },
              {
                "name": "bert-base-multilingual-uncased-sentiment"
              },
              {
                "name": "distilbert-base-multilingual-cased-sentiments-student"
              },
              {
                "name": "distilroberta-finetuned-financial-news-sentiment-analysis"
              }
            ],
            "defaults": {
              "model": "distilbert-base-uncased-finetuned-sst-2-english"
            },
            "input": {
              "type": "json",
              "permitted_extensions": [
                ".json"
              ]
            },
            "output": {
              "type": "json"
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

This module accepts as input `.json` files consisting of a *list of dictionaries*.  Each dictionary may have as many key-value pairs as desired, but *must* contain the key name *snippet*.  This is the key `json-to-txt` will act on.

Let's look at an example of a small valid input - and then process it.


```python
# examine contents of a valid input file
test_file = "../input_data/valid.json"
with open(test_file) as f:
    json_print(json.load(f))
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
test_file = "../input_data/valid.json"

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
      "pipeline": "my-sentiment-pipeline",
      "request_id": "b8f3860c-05a2-4a0e-aab2-c3bb4af94f9f",
      "file_id": "5bd5b6e4-86b1-413e-9863-ed96ef34295b",
      "message": "SUCCESS - output fetched for file_id 5bd5b6e4-86b1-413e-9863-ed96ef34295b.Output saved to location(s) listed in process_output_files.",
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
        "./5bd5b6e4-86b1-413e-9863-ed96ef34295b.json"
      ]
    }


We load in the text file output from `process_output_files` below. 


```python
# load in process output from file
import json
with open(process_output['process_output_files'][0], "r") as file:
    json_print(json.load(file))
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
