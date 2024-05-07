## The `translate` module

This document reviews the `translate` module - which takes as input a json of text snippets and returns their translations.  Translation data is returned as a json.

This document includes an overview of custom pipeline setup, current model set, parameters, and `.process` usage for this module.

To follow along with this demonstration be sure to initialize your krixik session with your api key and url as shown below. 

We illustrate loading these required secrets in via [python-dotenv](https://pypi.org/project/python-dotenv/), storing those secrets in a `.env` file.  This is always good practice for storing / loading secrets (e.g., doing so will reduce the chance you inadvertantly push secrets to a repo).

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [required input format](#required-input-format)
- [using the default model](#using-the-default-model)
- [using-a-non-default-model](#using-a-non-default-model)



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

## Pipeline setup

Below we setup a simple one module pipeline using the `translate` module. 

We do this by passing the module name to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(
    name="modules-translate-docs", module_chain=["translate"]
)
```

The `translate` module comes with a subset of popular translation models created at the [University of Hellsinki](https://huggingface.co/Helsinki-NLP).  These include

- [opus-mt-en-es](https://huggingface.co/Helsinki-NLP/opus-mt-en-es): english to spanish translation model (default)
- [opus-mt-es-en](https://huggingface.co/Helsinki-NLP/opus-mt-es-en): spanish to english translation model
- [opus-mt-de-en](https://huggingface.co/Helsinki-NLP/opus-mt-de-en): german to english translation model
- [opus-mt-en-fr](https://huggingface.co/Helsinki-NLP/opus-mt-en-fr): english to french translation model
- [opus-mt-fr-en](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en): french to english translation model
- [opus-mt-it-en](https://huggingface.co/Helsinki-NLP/opus-mt-it-en): italian to english translation model
- [opus-mt-zh-en](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en): chinese to english translation model

These available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```

## Required input format

The `translate` module accepts as input `.json` files consisting of a *list of dictionaries*.  Each dictionary may have as many key-value pairs as desired, but *must* contain the key name *snippet*.  This is the key `translate` will act on.

Let's look at an example of a small valid input - and then process it.


```python
# examine contents of a valid input file
test_file = "../../data/input/valid.json"
with open(test_file, "r") as file:
    print(json.dumps(json.load(file), indent=2))
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

Now let's process the small example input above using the default model - the english to spanish model `opus-mt-en-es`.  Because this is the default model we need not input the optional `modules` argument into `.process`.


```python
# define path to an input file
test_file = "../../data/input/valid.json"

# process for search
process_output = pipeline.process(
    local_file_path=test_file,
    local_save_directory="../../data/output",  # save output repo data output subdir
    expire_time=60 * 10,  # set all process data to expire in 10 minutes
    wait_for_process=True,  # wait for process to complete before regaining ide
    verbose=False,
)  # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is json, the process output is provided in this object as well.  The output file itself has been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "my-translate-pipeline",
      "request_id": "692d52aa-d081-441c-bd43-871ee9427c27",
      "file_id": "530ae1a1-263e-42ba-b358-5695324605d7",
      "message": "SUCCESS - output fetched for file_id 530ae1a1-263e-42ba-b358-5695324605d7.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "Me encanta esta pelcula y la vea una y otra vez!"
        },
        {
          "snippet": "El beneficio de explotacin ascendi a 9,4 millones EUR, frente a 11,7 millones EUR en 2004."
        }
      ],
      "process_output_files": [
        "../../data/output/530ae1a1-263e-42ba-b358-5695324605d7.json"
      ]
    }


We load in the text file output from `process_output_files` below. 


```python
# load in process output from file
with open(process_output["process_output_files"][0]) as f:
    print(json.dumps(json.load(f), indent=2))
```

    [{"snippet": "Me encanta esta pelcula y la vea una y otra vez!"}, {"snippet": "El beneficio de explotacin ascendi a 9,4 millones EUR, frente a 11,7 millones EUR en 2004."}]


## Using a non-default model

To use a non-default model like the spanish to english model `opus-mt-es-en` we enter it explicitly as a `modules` selection when invoking `.process`.

We use it below to process the following input.


```python
# examine contents of a valid input file
test_file = "../../data/input/valid_spanish.json"
with open(test_file, "r") as file:
    print(json.dumps(json.load(file), indent=2))
```

    [
      {
        "snippet": "Me encanta esta pelcula y la vea una y otra vez!"
      },
      {
        "snippet": "El beneficio de explotacin ascendi a 9,4 millones EUR, frente a 11,7 millones EUR en 2004."
      }
    ]



```python
# define path to an input file
test_file = "../../data/input/valid_spanish.json"

# process for search
process_output = pipeline.process(
    local_file_path=test_file,
    local_save_directory="../../data/output",  # save output repo data output subdir
    expire_time=60 * 10,  # set all process data to expire in 10 minutes
    wait_for_process=True,  # wait for process to complete before regaining ide
    verbose=False,  # set verbosity to False
    modules={"translate": {"model": "opus-mt-es-en"}},
)
```

The output of this process is printed below.  Because the output of this particular module-model pair is json, the process output is provided in this object as well.  The output file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "my-translate-pipeline",
      "request_id": "bb6e01e8-3540-4bea-9ad7-3f2f5fa25c6a",
      "file_id": "61accf67-aec9-44a2-9b6a-685e64027ee0",
      "message": "SUCCESS - output fetched for file_id 61accf67-aec9-44a2-9b6a-685e64027ee0.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "I love this movie and see it over and over again!"
        },
        {
          "snippet": "The operating profit amounted to EUR 9,4 million, compared with EUR 11,7 million in 2004."
        }
      ],
      "process_output_files": [
        "../../data/output/61accf67-aec9-44a2-9b6a-685e64027ee0.json"
      ]
    }



```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
