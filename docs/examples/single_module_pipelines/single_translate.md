## Single-Module Pipeline: `translate`

This document is a walkthrough of how to assemble and use a single-module pipeline that only includes a [`translate`](../../modules/ai_model_modules/translate_module.md) module. It's divided into the following sections:

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

Let's first instantiate a single-module [`translate`](../../modules/ai_model_modules/translate_module.md) pipeline.

We use the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method for this, passing only the [`translate`](../../modules/ai_model_modules/translate_module.md) module name into `module_chain`.


```python
# create a pipeline with a single translate module
pipeline = krixik.create_pipeline(name="single_translate_1",
                                  module_chain=["translate"])
```

### Required Input Format

The [`translate`](../../modules/ai_model_modules/translate_module.md) module accepts JSON file input. The input JSON must respect [this format](../../system/parameters_processing_files_through_pipelines/JSON_input_format.md).

Let's take a quick look at a valid input file, and then process it.


```python
# examine contents of a valid input file
with open("../../../data/input/valid.json", "r") as file:
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


### Using the Default Model

Let's process our test input file using the [`translate`](../../modules/ai_model_modules/translate_module.md) module's [default model](../../modules/ai_model_modules/translate_module.md#available-models-in-the-translate-module), which translates English into Spanish: [`opus-mt-en-es`](https://huggingface.co/Helsinki-NLP/opus-mt-en-es).

Given that this is the default model, we need not specify model selection through the optional [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file with the default model
process_output = pipeline.process(local_file_path="../../../data/input/valid.json", # the initial local filepath where the input file is stored
                                  local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                  expire_time=60 * 30, # process data will be deleted from the Krixik system in 30 minutes
                                  wait_for_process=True, # wait for process to complete before returning IDE control to user
                                  verbose=False) # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a JSON file, the process output is provided in this object as well (this is only the case for JSON outputs).  Moreover, the output file itself has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_translate_1",
      "request_id": "be3b3fc9-1811-47a5-abfb-29db2019e134",
      "file_id": "54d7b537-5e65-48f7-a8e6-f9c7d44da2f7",
      "message": "SUCCESS - output fetched for file_id 54d7b537-5e65-48f7-a8e6-f9c7d44da2f7.Output saved to location(s) listed in process_output_files.",
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
        "../../../data/output/54d7b537-5e65-48f7-a8e6-f9c7d44da2f7.json"
      ]
    }


To confirm that everything went as it should have, let's load in the text file output from `process_output_files`:


```python
# load in process output from file
with open(process_output["process_output_files"][0]) as f:
    print(json.dumps(json.load(f), indent=2))
```

    [
      {
        "snippet": "Me encanta esta pelcula y la vea una y otra vez!"
      },
      {
        "snippet": "El beneficio de explotacin ascendi a 9,4 millones EUR, frente a 11,7 millones EUR en 2004."
      }
    ]


### Using a Non-Default Model

To use a [non-default model](../../modules/ai_model_modules/translate_module.md#available-models-in-the-translate-module) like Spanish-to-English [`opus-mt-es-en`](https://huggingface.co/Helsinki-NLP/opus-mt-es-en) you must enter it explicitly through the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument when invoking the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

We do so below to process the same input file as above.


```python
# process the file with a non-default model
process_output = pipeline.process(local_file_path="../../../data/input/valid_spanish.json", # all parameters save 'modules' as above
                                  local_save_directory="../../../data/output",
                                  expire_time=60 * 30,
                                  wait_for_process=True,
                                  verbose=False,
                                  modules={"translate": {"model": "opus-mt-es-en"}}) # specify a non-default model for this process
```

We once again print out and review the output as we did above.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_translate_1",
      "request_id": "ec76e171-5191-4b68-8db4-a6389bf474d7",
      "file_id": "126cba83-d7d1-4581-8c7c-25ec7e3a29f5",
      "message": "SUCCESS - output fetched for file_id 126cba83-d7d1-4581-8c7c-25ec7e3a29f5.Output saved to location(s) listed in process_output_files.",
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
        "../../../data/output/126cba83-d7d1-4581-8c7c-25ec7e3a29f5.json"
      ]
    }



```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
