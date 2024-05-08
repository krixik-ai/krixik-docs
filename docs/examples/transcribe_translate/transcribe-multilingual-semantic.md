# Semantically searchable multilingual transcription pipeline

This document details a modular pipeline that takes in an audio/video file, transcribes it, translates the transcription into a desired language, and makes the result semantically searchable.

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [processing a file](#processing-a-file)
- [performing semantic search](#performing-semantic-search)


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
load_dotenv("../../.env")
MY_API_KEY = os.getenv('MY_API_KEY')
MY_API_URL = os.getenv('MY_API_URL')

# import krixik and initialize it with your personal secrets
from krixik import krixik
krixik.init(api_key = MY_API_KEY, 
            api_url = MY_API_URL)
```

    SUCCESS: You are now authenticated.


## Pipeline setup

Below we setup a multi module pipeline to serve our intended purpose, which is to build a pipeline that will transcribe any audio/video and make it semantically searchable in any language.

To do this we will use the following modules:

- [`transcribe`](../../modules/transcribe.md): takes in audio/video input, outputs json of content transcription
- [`translate`](../../modules/translate.md): takes in json of text snippets, outputs json of translated snippets
- [`json-to-txt`](../../modules/json-to-txt.md): takes in json of text snippets, merges into text file
- [`parser`](../../modules/parser.md): takes in text, slices into (possibly overlapping) strings
- [`text-embedder`](../../modules/text-embedder.md): takes in text snippets, creates vector representation of each outputing an npy file
- [`vector-db`](../../modules/vector-db.md): takes in npy of vectors, outputs vector db

We do this by passing the module names to the `module_chain` argument of [`create_pipeline`](../../system/create_save_load.md) along with a name for our pipeline.


```python
# create a multi-module pipeline
pipeline = krixik.create_pipeline(name="examples-transcribe-semantic-multilingual-docs",
                                  module_chain=["transcribe",
                                                "translate",
                                                "json-to-txt",
                                                "parser",
                                                "text-embedder",
                                                "vector-db"])
```

This pipeline's available modeling options and parameters are stored in your custom [pipeline's configuration](../../system/create_save_load.md).


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```

## Processing a file

We first define a path to a local input file.

Lets take a quick look at this file before processing.


```python
# examine contents of input file
test_file = "../../../data/input/Interesting Facts About Colombia.mp4"
from IPython.display import Video
Video(test_file)
```




<video src="../../../data/input/Interesting Facts About Colombia.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



The input video content language content is English.  We will use the `opus-mt-en-es` model of the [`translate`](../../modules/translate.md) to translate the transcript of this video into Spanish.

For this run we will use the default models for the remainder of the modules.



```python
dictionary = {"transcript": "hi"}
for key, value in dictionary.items():
    print(len(key))
```

    10



```python
# test file
test_file = "../../../data/input/Interesting Facts About Colombia.mp4"

# process test input
process_output = pipeline.process(local_file_path = test_file,
                                  expire_time=60*10,
                                  modules={"translate": {"model": "opus-mt-en-es"}},
                                  verbose=True,
                                  local_save_directory="../../../data/output")
```

    INFO: Checking that file size falls within acceptable parameters...
    INFO:...success!
    converted ../../../data/input/Interesting Facts About Colombia.mp4 to: /var/folders/k9/0vtmhf0s5h56gt15mkf07b1r0000gn/T/tmpvnfz4nvg/krixik_converted_version_Interesting Facts About Colombia.mp3
    INFO: hydrated input modules: {'module_1': {'model': 'whisper-tiny', 'params': {}}, 'module_2': {'model': 'opus-mt-en-es', 'params': {}}, 'module_3': {'model': 'base', 'params': {}}, 'module_4': {'model': 'sentence', 'params': {}}, 'module_5': {'model': 'all-MiniLM-L6-v2', 'params': {'quantize': True}}, 'module_6': {'model': 'faiss', 'params': {}}}
    INFO: symbolic_directory_path was not set by user - setting to default of /etc
    INFO: file_name was not set by user - setting to random file name: krixik_generated_file_name_qfgbnrugsa.mp3
    INFO: wait_for_process is set to True.
    INFO: file will expire and be removed from you account in 600 seconds, at Mon May  6 12:23:47 2024 UTC
    INFO: examples-transcribe-semantic-multilingual-docs file process and input processing started...
    INFO: metadata can be updated using the .update api.
    INFO: This process's request_id is: 8842c45c-bce2-3d52-8426-f26c872ed546
    INFO: File process and processing status:
    SUCCESS: module 1 (of 6) - transcribe processing complete.
    SUCCESS: module 2 (of 6) - translate processing complete.
    SUCCESS: module 3 (of 6) - json-to-txt processing complete.
    SUCCESS: module 4 (of 6) - parser processing complete.
    SUCCESS: module 5 (of 6) - text-embedder processing complete.
    SUCCESS: module 6 (of 6) - vector-db processing complete.
    SUCCESS: pipeline process complete.
    SUCCESS: process output downloaded


The output of this process is printed below.  Because the output of this particular pipeline is a database file, the process output is shown as null in the output.  The local address of the output file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "examples-transcribe-semantic-multilingual-docs",
      "request_id": "f8ed48c3-b318-48f0-961f-0b9e4cc34b1c",
      "file_id": "600b873e-1bef-471a-a5e9-ae675c0514bc",
      "message": "SUCCESS - output fetched for file_id 600b873e-1bef-471a-a5e9-ae675c0514bc.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "/Users/jeremywatt/Desktop/krixik/code/krixik-docs/docs/examples/transcribe/600b873e-1bef-471a-a5e9-ae675c0514bc.faiss"
      ]
    }


## Performing semantic search

Because our pipeline has `text-embedder` and `vector-db` modules we can semantically search the translated transcription, here in Spanish (since we processed our file with an English-Spanish model).  


```python
# semantically search translated transcription
search_output = pipeline.semantic_search(query="hechos realmente bsicos", 
                                         file_ids=[process_output["file_id"]])

print(json.dumps(search_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "b9452617-37da-47c6-aac4-70c82074e94d",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "600b873e-1bef-471a-a5e9-ae675c0514bc",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_qfgbnrugsa.mp3",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 39,
            "created_at": "2024-05-06 19:13:50",
            "last_updated": "2024-05-06 19:13:50"
          },
          "search_results": [
            {
              "snippet": "Miramos algunos hechos realmente bsicos.",
              "line_numbers": [
                1
              ],
              "distance": 0.058
            },
            {
              "snippet": "Bienvenidos de nuevo a los hechos F2D.",
              "line_numbers": [
                1
              ],
              "distance": 0.2
            },
            {
              "snippet": "Pero comencemos.",
              "line_numbers": [
                1
              ],
              "distance": 0.23
            },
            {
              "snippet": "S. Entonces me estoy pagando por esto.",
              "line_numbers": [
                1
              ],
              "distance": 0.242
            },
            {
              "snippet": "Lo que me recuerda chicos, esto es parte de nuestra lista de Columbia.",
              "line_numbers": [
                1
              ],
              "distance": 0.244
            }
          ]
        }
      ]
    }


Learn more about the [`semantic_search` method here](../../system/semantic_search.md).


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
