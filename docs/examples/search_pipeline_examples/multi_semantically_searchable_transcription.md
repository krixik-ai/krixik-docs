## Multi-Module Pipeline: Semantically-Searchable Transcription

This document details a modular pipeline that takes in an audio file, [`transcribes`](../../modules/ai_model_modules/transcribe_module.md) it, and makes the result [`semantically searchable`](../../system/search_methods/semantic_search_method.md).

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)
- [Performing Semantic Search](#performing-semantic-search)


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

- A [`parser`](../../modules/ai_model_modules/parser_module.md) module.

- A [`text-embedder`](../../modules/ai_model_modules/text-embedder_module.md) module.

- A [`vector-db`](../../modules/database_modules/vector-db_module.md) module.

We use the [`json-to-txt`](../../modules/support_function_modules/json-to-txt_module.md) and [`parser`](../../modules/ai_model_modules/parser_module.md) combination, which combines the transcribed snippets into one document and then splices it again, to make sure that any pauses in speech don't make for partial snippets that can confuse the [`text-embedder`](../../modules/ai_model_modules/text-embedder_module.md) model.

Pipeline setup is accomplished through the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method, as follows:


```python
# create a pipeline as detailed above

pipeline_1 = krixik.create_pipeline(name="multi_semantically_searchable_transcription",
                                    module_chain=["transcribe",
                                                  "json-to-txt",
                                                  "parser",
                                                  "text-embedder",
                                                  "vector-db"])
```

### Processing an Input File

Lets take a quick look at a test file before processing.


```python
# examine contents of input file

from IPython.display import Video
Video("../../../data/input/Interesting Facts About Colombia.mp3")
```




<video src="../../../data/input/Interesting Facts About Colombia.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



We will use the default models for every module in the pipeline, so the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method doesn't need to be leveraged.


```python
# process the file through the pipeline, as described above

process_output_1 = pipeline_1.process(local_file_path = "../../../data/input/Interesting Facts About Colombia.mp3", # the initial local filepath where the input file is stored
                                      local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                      expire_time=60*30, # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True, # wait for process to complete before returning IDE control to user
                                      verbose=False) # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a [`FAISS`](https://github.com/facebookresearch/faiss) database file, the process output is null. However, the output file has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process

print(json.dumps(process_output_1, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "multi_semantically_searchable_transcription",
      "request_id": "51c5df18-64f0-44d7-bb48-611d30a4664a",
      "file_id": "8475ae1c-6618-4798-a51a-fcab70b94923",
      "message": "SUCCESS - output fetched for file_id 8475ae1c-6618-4798-a51a-fcab70b94923.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/8475ae1c-6618-4798-a51a-fcab70b94923.faiss"
      ]
    }


### Performing Semantic Search

Krixik's [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method enables semantic search on documents [processed](../../system/parameters_processing_files_through_pipelines/process_method.md) through certain pipelines. Given that the [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method both [embeds](../../modules/ai_model_modules/text-embedder_module.md) the query and performs the search, it can only be used with pipelines containing both a [`text-embedder`](../../modules/ai_model_modules/text-embedder_module.md) module and a [`vector-db`](../../modules/database_modules/vector-db_module.md) module in immediate succession.

Since our pipeline satisfies this condition, it has access to the [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method. Let's use it to query our text with natural language, as shown below:


```python
# perform semantic_search over the file in the pipeline

semantic_output_1 = pipeline_1.semantic_search(query="Let's talk about the country of Colombia", 
                                               file_ids=["8475ae1c-6618-4798-a51a-fcab70b94923"])

# nicely print the output of this process

print(json.dumps(semantic_output_1, indent=2))
```

    {
      "status_code": 200,
      "request_id": "79dc66c3-a7fd-4702-b5bc-99904bcae644",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "8475ae1c-6618-4798-a51a-fcab70b94923",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_eopdghinjh.mp3",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 40,
            "created_at": "2024-05-20 06:31:45",
            "last_updated": "2024-05-20 06:31:45"
          },
          "search_results": [
            {
              "snippet": "Now, interesting enough when it comes to the coffee in Columbia, believe it or not, it is not actually native to the country.",
              "line_numbers": [
                1
              ],
              "distance": 0.242
            },
            {
              "snippet": "And I know coffee is really important when it comes to talking about Columbia, but you really don't know how important it is with its culture.",
              "line_numbers": [
                1
              ],
              "distance": 0.247
            },
            {
              "snippet": "So we all know, Columbia is famous for its coffee, right?",
              "line_numbers": [
                1
              ],
              "distance": 0.25
            },
            {
              "snippet": " This episode, looking at the great country of Columbia, we looked at some really basic facts.",
              "line_numbers": [
                1
              ],
              "distance": 0.257
            },
            {
              "snippet": "Now here's the thing when it comes to coffee in Columbia.",
              "line_numbers": [
                1
              ],
              "distance": 0.257
            }
          ]
        }
      ]
    }



```python
# delete all processed datapoints belonging to this pipeline

reset_pipeline(pipeline_1)
```
