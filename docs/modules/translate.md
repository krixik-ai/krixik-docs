## the `translate` module

This document reviews the `translate` module - which takes as input a json of text snippets and returns their translations.  Translation data is returned as a json.

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
- [using the english to spanish translation model](#using-the-english-to-spanish-translation-model)
- [using the spanish to english translation model](#using-spanish-to-english-translation-model)


## Pipeline setup

Below we setup a simple one module pipeline using the `translate` module. 


```python
# import custom module creation tools
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# instantiate module
module_1 = Module(module_type="translate")

# create custom pipeline object
custom = CreatePipeline(name='translate-pipeline-1', 
                        module_chain=[module_1])

# pass the custom object to the krixik operator (note you can also do this by passing its config)
pipeline = krixik.load_pipeline(pipeline=custom)
```

The `translate` module comes with a subset of popular translation models created at the [University of Hellsinki](https://huggingface.co/Helsinki-NLP).  These include

- [opus-mt-en-es](https://huggingface.co/Helsinki-NLP/opus-mt-en-es): english to spanish translation model (default)
- [opus-mt-es-en](https://huggingface.co/Helsinki-NLP/opus-mt-es-en): spanish to english translation model
- [opus-mt-de-en](https://huggingface.co/Helsinki-NLP/opus-mt-de-en): german to english translation model
- [opus-mt-en-fr](https://huggingface.co/Helsinki-NLP/opus-mt-en-fr): english to french translation model
- [opus-mt-fr-en](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en): french to english translation model
- [opus-mt-it-en](https://huggingface.co/Helsinki-NLP/opus-mt-it-en): italian to english translation model
- [opus-mt-zh-en](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en): chinese to english translation model

These available modeling options and parameters are stored in our custom pipeline's configuration (described further in LINK HERE).  We can examine this configuration as shown below.


```python
# nicely print the configuration of uor custom pipeline
json_print(custom.config)
```

    {
      "pipeline": {
        "name": "translate-pipeline-1",
        "modules": [
          {
            "name": "translate",
            "models": [
              {
                "name": "opus-mt-de-en"
              },
              {
                "name": "opus-mt-en-es"
              },
              {
                "name": "opus-mt-es-en"
              },
              {
                "name": "opus-mt-en-fr"
              },
              {
                "name": "opus-mt-fr-en"
              },
              {
                "name": "opus-mt-it-en"
              },
              {
                "name": "opus-mt-zh-en"
              }
            ],
            "defaults": {
              "model": "opus-mt-en-es"
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

## using the english to spanish translation model

We first define a path to a local input file.


```python
# define path to an input file
test_file = "../input_data/valid.json"
```

Lets take a quick look at this file before processing.


```python
# examine contents of input file
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


Now let's process it using the english to spanish model - `opus-mt-en-es`.  Because this is the default model we need not input the optional `modules` argument into `.process`.


```python
# define path to an input file
test_file = "../input_data/valid.json"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is json, the process output is provided in this object as well.  The output file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "translate-pipeline-1",
      "request_id": "d8abf348-0780-4786-b9d7-4325b7402847",
      "file_id": "00ce8caf-9604-4b06-b498-21ccb70f153e",
      "message": "SUCCESS - output fetched for file_id 00ce8caf-9604-4b06-b498-21ccb70f153e.Output saved to location(s) listed in process_output_files.",
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
        "./00ce8caf-9604-4b06-b498-21ccb70f153e.json"
      ]
    }


We load in the text file output from `process_output_files` below. 


```python
# load in process output from file
import json
with open(process_output['process_output_files'][0], "r") as file:
    print(file.read())  
```

    [{"snippet": "Me encanta esta pelcula y la vea una y otra vez!"}, {"snippet": "El beneficio de explotacin ascendi a 9,4 millones EUR, frente a 11,7 millones EUR en 2004."}]


### using the spanish to english translation model

To use a non-default model like the spanish to english model `opus-mt-es-en` we enter it explicitly as a `modules` selection when invoking `.process`.

We use it below to process the following input.


```python
# define path to an input file
test_file = "../input_data/valid_spanish.json"

# examine contents of input file
with open(test_file) as f:
    json_print(json.load(f))
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
test_file = "../input_data/valid_spanish.json"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,            # set verbosity to False
                                  modules={"translate":{"model":"opus-mt-es-en"}})
```

The output of this process is printed below.  Because the output of this particular module-model pair is json, the process output is provided in this object as well.  The output file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "translate-pipeline-1",
      "request_id": "9a78b0d7-d699-4886-ac67-3622ba73fe37",
      "file_id": "be556616-4ddd-4228-b504-81d61c605c54",
      "message": "SUCCESS - output fetched for file_id be556616-4ddd-4228-b504-81d61c605c54.Output saved to location(s) listed in process_output_files.",
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
        "./be556616-4ddd-4228-b504-81d61c605c54.json"
      ]
    }

