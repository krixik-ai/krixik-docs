## Single-Module Pipeline: `sentiment`

This document is a walkthrough of how to assemble and use a single-module pipeline that only includes a [`sentiment`](../../modules/ai_model_modules/sentiment_module.md) module. It's divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Required Input Format](#required-input-format)
- [Using the Default Model](#using-the-default-model)
- [Using a Non-Default Model](#using-a-non-default-model)


```python
# import utilities
import sys 
import json
import importlib
sys.path.append('../../../')
reset = importlib.import_module("utilities.reset")
reset_pipeline = reset.reset_pipeline

# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os
load_dotenv("../../../.env")
MY_API_KEY = os.getenv('MY_API_KEY')
MY_API_URL = os.getenv('MY_API_URL')

# import krixik and initialize it with your personal secrets
from krixik import krixik
krixik.init(api_key = MY_API_KEY, 
            api_url = MY_API_URL)
```

    SUCCESS: You are now authenticated.


### Pipeline Setup

Let's first instantiate a single-module [`sentiment`](../../modules/ai_model_modules/sentiment_module.md) pipeline.

We use the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method for this, passing only the [`sentiment`](../../modules/ai_model_modules/sentiment_module.md) module name into `module_chain`.


```python
# create a pipeline with a single sentiment module

pipeline_1 = krixik.create_pipeline(name="single_sentiment_1",
                                    module_chain=["sentiment"])
```

### Required Input Format

The [`sentiment`](../../modules/ai_model_modules/sentiment_module.md) module accepts JSON file input. The input JSON must respect [this format](../../system/parameters_processing_files_through_pipelines/JSON_input_format.md).

Let's take a quick look at a valid input file, and then process it.


```python
# examine contents of a valid input file

with open("../../../data/input/valid.json") as f:
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


### Using the Default Model

Let's process our test input file using the [`sentiment`](../../modules/ai_model_modules/sentiment_module.md) module's [default model](../../modules/ai_model_modules/sentiment_module.md#available-models-in-the-sentiment-module): `base`.

Given that this is the default model, we need not specify model selection through the optional [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file with the default model

process_output_1 = pipeline_1.process(local_file_path="../../../data/input/valid.json", # the initial local filepath where the input file is stored
                                      local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                      expire_time=60 * 30, # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True, # wait for process to complete before returning IDE control to user
                                      verbose=False) # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a JSON file, the process output is provided in this object as well (this is only the case for JSON outputs).  Moreover, the output file itself has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process

print(json.dumps(process_output_1, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_sentiment_1",
      "request_id": "3720d5d1-492f-4f0c-97a6-3e9dc3d5f95b",
      "file_id": "27d6d1cb-a64d-4506-bf9e-4b1e31e2d3a3",
      "message": "SUCCESS - output fetched for file_id 27d6d1cb-a64d-4506-bf9e-4b1e31e2d3a3.Output saved to location(s) listed in process_output_files.",
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
        "../../../data/output/27d6d1cb-a64d-4506-bf9e-4b1e31e2d3a3.json"
      ]
    }


To confirm that everything went as it should have, let's load in the text file output from `process_output_files`:


```python
# load in process output from file

with open(process_output_1["process_output_files"][0]) as f:
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


### Using a Non-Default Model

To use a [non-default model](../../modules/ai_model_modules/sentiment_module.md#available-models-in-the-sentiment-module) like [`distilbert-base-multilingual-cased-sentiments-student`](https://huggingface.co/lxyuan/distilbert-base-multilingual-cased-sentiments-student), we must enter it explicitly through the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument when invoking the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file with a non-default model

process_output_2 = pipeline_1.process(local_file_path="../../../data/input/valid.json", # all arguments save for modules are as above
                                      local_save_directory="../../../data/output",
                                      expire_time=60 * 30,
                                      wait_for_process=True,
                                      verbose=False,
                                      modules={"sentiment": {"model": "distilbert-base-multilingual-cased-sentiments-student"}}) # specify a non-default model for this process
```

The output of this process is printed below.

Because the output of this particular module-model pair is a JSON file, the process output is provided in this object as well (this is only the case for JSON outputs).  Moreover, the output file itself has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process

print(json.dumps(process_output_2, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_sentiment_1",
      "request_id": "739e3fe7-a151-4247-a853-d5f4550ab499",
      "file_id": "fbc7e1b6-a97a-4123-8feb-221edd866fda",
      "message": "SUCCESS - output fetched for file_id fbc7e1b6-a97a-4123-8feb-221edd866fda.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "I love this movie and i would watch it again and again!",
          "positive": 0.973,
          "negative": 0.01,
          "neutral": 0.017
        },
        {
          "snippet": "Operating profit totaled EUR 9.4 mn, down from EUR 11.7 mn in 2004.",
          "positive": 0.476,
          "negative": 0.321,
          "neutral": 0.202
        }
      ],
      "process_output_files": [
        "../../../data/output/fbc7e1b6-a97a-4123-8feb-221edd866fda.json"
      ]
    }



```python
# delete all processed datapoints belonging to this pipeline

reset_pipeline(pipeline_1)
```