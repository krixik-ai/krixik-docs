## Multi-Module Pipeline: Sentiment Analysis on Translation

This document details a modular pipeline that takes in an a text file in a non-English language, [`translates`](../../modules/ai_modules/translate_module.md) it into English, and then performs [`sentiment analysis`](../../modules/ai_modules/sentiment_module.md) on each sentence of the translation.

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)


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

To achieve what we've described above, let's set up a pipeline sequentially consisting of the following modules:

- A [`parser`](../../modules/support_function_modules/parser_module.md) module.

- A [`translate`](../../modules/ai_modules/translate_module.md) module.

- A [`sentiment`](../../modules/ai_modules/sentiment_module.md) module.

We do this by leveraging the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method, as follows:


```python
# create a pipeline as detailed above
pipeline = krixik.create_pipeline(name="multi_sentiment_analysis_on_translation",
                                  module_chain=["parser",
                                                "translate",
                                                "sentiment"])
```

### Processing an Input File

Given that we're [`translating`](../../modules/ai_modules/translate_module.md) and then performing [`sentiment analysis`](../../modules/ai_modules/sentiment_module.md), we'll start with a file in Spanish. Since the input text is in Spanish, we'll use the (non-default) [`opus-mt-es-en`](https://huggingface.co/Helsinki-NLP/opus-mt-es-en) model of the [`translate`](../../modules/ai_modules/translate_module.md) module to translate it into English.

We will use the default models for every other module in the pipeline, so they don't have to be specified in the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file through the pipeline, as described above
process_output = pipeline.process(local_file_path = "../../../data/input/spanish_review.txt", # the initial local filepath where the input file is stored
                                  local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                  expire_time=60*30, # process data will be deleted from the Krixik system in 30 minutes
                                  wait_for_process=True, # wait for process to complete before returning IDE control to user
                                  verbose=False, # do not display process update printouts upon running code
                                  modules={"module_2": {"model": "opus-mt-es-en"}}) # specify a non-default model for use in the second module
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a JSON file, the process output is provided in this object as well (this is only the case for JSON outputs).  Moreover, the output file itself has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "multi_sentiment_analysis_on_translation",
      "request_id": "d096b362-d630-41a9-93c8-0c754663bc5f",
      "file_id": "f3ef7479-c4c2-4362-be86-746563889ada",
      "message": "SUCCESS - output fetched for file_id f3ef7479-c4c2-4362-be86-746563889ada.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "For the jobs I'm doing I turned out very good.",
          "positive": 1.0,
          "negative": 0.0,
          "neutral": 0.0
        },
        {
          "snippet": "In one hour load the battery and last more than 3 hours of continuous work.",
          "positive": 0.008,
          "negative": 0.992,
          "neutral": 0.0
        },
        {
          "snippet": "A golasse to have a second batter.",
          "positive": 0.023,
          "negative": 0.977,
          "neutral": 0.0
        },
        {
          "snippet": "Cmodo and with good torque.",
          "positive": 1.0,
          "negative": 0.0,
          "neutral": 0.0
        },
        {
          "snippet": "I agree.",
          "positive": 1.0,
          "negative": 0.0,
          "neutral": 0.0
        }
      ],
      "process_output_files": [
        "../../../data/output/f3ef7479-c4c2-4362-be86-746563889ada.json"
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
        "snippet": "For the jobs I'm doing I turned out very good.",
        "positive": 1.0,
        "negative": 0.0,
        "neutral": 0.0
      },
      {
        "snippet": "In one hour load the battery and last more than 3 hours of continuous work.",
        "positive": 0.008,
        "negative": 0.992,
        "neutral": 0.0
      },
      {
        "snippet": "A golasse to have a second batter.",
        "positive": 0.023,
        "negative": 0.977,
        "neutral": 0.0
      },
      {
        "snippet": "Cmodo and with good torque.",
        "positive": 1.0,
        "negative": 0.0,
        "neutral": 0.0
      },
      {
        "snippet": "I agree.",
        "positive": 1.0,
        "negative": 0.0,
        "neutral": 0.0
      }
    ]


You may note that, in the first returned snippet, the word "sillón" is missing its second vowel and is printed as "silln". This is a model issue: the [`translate`](../../modules/ai_modules/translate_module.md#available-models-in-the-translate-module) model with which we processed the file may have trouble with accented characters and/or outright remove them. It's important that you familiarize yourself with the peculiarities of AI models you intend to leverage often.


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
