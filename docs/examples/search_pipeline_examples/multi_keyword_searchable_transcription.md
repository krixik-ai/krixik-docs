## Multi-Module Pipeline: Keyword-Searchable Transcription

This document details a modular pipeline that takes in an audio file, [`transcribes`](../../modules/ai_model_modules/transcribe_module.md) it, and makes the result [`keyword searchable`](../../system/search_methods/keyword_search_method.md).

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)
- [Performing Keyword Search](#performing-keyword-search)


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

- A [`transcribe`](../../modules/ai_model_modules/transcribe_module.md) module.

- A [`json-to-txt`](../../modules/support_function_modules/json-to-txt_module.md) module.

- A [`keyword-db`](../../modules/database_modules/keyword-db_module.md) module.

We do this by leveraging the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method, as follows:


```python
# create a pipeline as detailed above
pipeline = krixik.create_pipeline(name="multi_keyword_searchable_transcription",
                                  module_chain=["transcribe",
                                                "json-to-txt",
                                                "keyword-db"])
```

### Processing an Input File

Lets take a quick look at a test file before processing.


```python
# examine contents of input file
import IPython
IPython.display.Audio("../../../data/input/Interesting Facts About Colombia.mp3")
```




<video src="../../../data/input/Interesting Facts About Colombia.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



We will use the default models for every module in the pipeline, so the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method doesn't need to be leveraged.


```python
# process the file through the pipeline, as described above
process_output = pipeline.process(local_file_path = "../../../data/input/Interesting Facts About Colombia.mp3", # the initial local filepath where the input file is stored
                                  local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                  expire_time=60*30, # process data will be deleted from the Krixik system in 30 minutes
                                  wait_for_process=True, # wait for process to complete before returning IDE control to user
                                  verbose=False) # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is an `SQLlite` database file, the `process_output` is "null". However, the output file has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "multi_keyword_searchable_transcription",
      "request_id": "ac2d22e7-2231-4924-a694-445ebe5600b9",
      "file_id": "ff1e268e-d509-4f41-88d2-dada75505134",
      "message": "SUCCESS - output fetched for file_id ff1e268e-d509-4f41-88d2-dada75505134.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/ff1e268e-d509-4f41-88d2-dada75505134.db"
      ]
    }


### Performing Keyword Search

Krixik's [`.keyword_search`](../../system/search_methods/keyword_search_method.md) method enables keyword search on documents processed through pipelines that end with the [`keyword-db`](../../modules/database_modules/keyword-db_module.md) module.

Since our pipeline satisfies this condition, it has access to the [`.keyword_search`](../../system/search_methods/keyword_search_method.md) method. Let's use it to query our text for a few keywords, as below:


```python
# perform keyword search over the file in the pipeline
keyword_output = pipeline.keyword_search(query="lets talk about the country of Colombia", 
                                         file_ids=[process_output["file_id"]])

# nicely print the output of this process
print(json.dumps(keyword_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "19f1b2d9-a154-4bf8-a6a0-14fb37422dd1",
      "message": "Successfully queried 1 user file.",
      "warnings": [
        {
          "WARNING: the following words in the query are in the stop_words list and thus no results will be returned for them": [
            "about",
            "the",
            "of"
          ]
        }
      ],
      "items": [
        {
          "file_id": "ff1e268e-d509-4f41-88d2-dada75505134",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_owutflggbq.mp3",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_lines": 1,
            "created_at": "2024-05-20 06:27:26",
            "last_updated": "2024-05-20 06:27:26"
          },
          "search_results": [
            {
              "keyword": "country",
              "line_number": 1,
              "keyword_number": 7
            },
            {
              "keyword": "talk",
              "line_number": 1,
              "keyword_number": 120
            },
            {
              "keyword": "countries",
              "line_number": 1,
              "keyword_number": 144
            },
            {
              "keyword": "let",
              "line_number": 1,
              "keyword_number": 163
            },
            {
              "keyword": "talk",
              "line_number": 1,
              "keyword_number": 193
            },
            {
              "keyword": "country",
              "line_number": 1,
              "keyword_number": 317
            },
            {
              "keyword": "countries",
              "line_number": 1,
              "keyword_number": 347
            },
            {
              "keyword": "country",
              "line_number": 1,
              "keyword_number": 358
            },
            {
              "keyword": "country",
              "line_number": 1,
              "keyword_number": 468
            }
          ]
        }
      ]
    }



```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
