# Multilingual-to-english transcription with sentiment analysis pipeline

This document details a modular pipeline that takes in an audio/video file in a non-english language, transcribes it, translates the transcription into english, and then performs sentiment analysis on each sentence of the translated transcript.

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [processing a file](#processing-a-file)



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

Below we setup a multi module pipeline to serve our intended purpose, which is to build a pipeline that will transcribe any audio/video in a non-english language, translate the content of the corresponding transcription into english, and then perform sentiment analysis on the result - sentence-by-sentence.

To do this we will use the following modules:

- [`transcribe`](modules/transcribe.md): takes in audio/video input, outputs json of content transcription
- [`translate`](modules/translate.md): takes in json of text snippets, outputs json of translated snippets
- [`json-to-txt`](modules/json-to-txt.md): takes in json of text snippets, merges into text file
- [`parser`](modules/parser.md): takes in text, slices into (possibly overlapping) strings
- [`sentiment`](modules/sentiment.md): takes in text snippets and returns scores for their sentiments

We do this by passing the module names to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a multi-module pipeline
pipeline = krixik.create_pipeline(name="examples-transcribe-multilingual-sentiment-docs",
                                  module_chain=["transcribe",
                                                "translate",
                                                "json-to-txt",
                                                "parser",
                                                "sentiment"])
```

With our `custom` pipeline built we now pass it, along with a test file, to our operator to process the file.

## Processing a file

Lets take a quick look at a test file before processing.

This is a short video in spanish.  After transcription we will translate it into english.


```python
# examine contents of input file
test_file = "../../../data/input/deadlift.mp4"
from IPython.display import Video
Video(test_file)
```




<video src="../../../data/input/deadlift.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



The input video content language content is English.  We will use the `opus-mt-es-en` model of the [`translate`](modules/translate.md) to translate the transcript of this video into Spanish.

For this run we will use the default models for the remainder of the modules.



```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```


```python

# test file
test_file = "../../../data/input/deadlift.mp4"

# process test input
process_output = pipeline.process(local_file_path = test_file,
                                  expire_time=60*10,
                                  modules={
                                      "transcribe": {"model": "whisper-base"},
                                      "translate": {"model": "opus-mt-es-en"}
                                      },
                                  verbose=True,
                                  local_save_directory="../../../data/output")
```

    INFO: Checking that file size falls within acceptable parameters...
    INFO:...success!
    converted ../../../data/input/deadlift.mp4 to: /var/folders/k9/0vtmhf0s5h56gt15mkf07b1r0000gn/T/tmpbc1_ib05/krixik_converted_version_deadlift.mp3
    INFO: hydrated input modules: {'module_1': {'model': 'whisper-medium', 'params': {}}, 'module_2': {'model': 'opus-mt-es-en', 'params': {}}, 'module_3': {'model': 'base', 'params': {}}, 'module_4': {'model': 'sentence', 'params': {}}, 'module_5': {'model': 'distilbert-base-uncased-finetuned-sst-2-english', 'params': {}}}
    INFO: symbolic_directory_path was not set by user - setting to default of /etc
    INFO: file_name was not set by user - setting to random file name: krixik_generated_file_name_tihuizzppb.mp3
    INFO: wait_for_process is set to True.
    INFO: file will expire and be removed from you account in 600 seconds, at Mon May  6 16:44:53 2024 UTC
    INFO: examples-transcribe-multilingual-sentiment-docs file process and input processing started...
    INFO: metadata can be updated using the .update api.
    INFO: This process's request_id is: df146df8-015c-ed3a-e0d0-d944cea661d9
    INFO: File process and processing status:
    SUCCESS: module 1 (of 5) - transcribe processing complete.
    SUCCESS: module 2 (of 5) - translate processing complete.
    SUCCESS: module 3 (of 5) - json-to-txt processing complete.
    SUCCESS: module 4 (of 5) - parser processing complete.
    SUCCESS: module 5 (of 5) - sentiment processing complete.
    SUCCESS: pipeline process complete.
    SUCCESS: process output downloaded


The output of this process is printed below.  Because the output of this particular pipeline is a database file, the process output is shown as null in the output.  The local address of the output file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "examples-transcribe-multilingual-sentiment-docs",
      "request_id": "1119f07f-e4a1-4021-9668-2f19ea367568",
      "file_id": "efdc2954-9bef-4427-8de1-2bd18a830015",
      "message": "SUCCESS - output fetched for file_id efdc2954-9bef-4427-8de1-2bd18a830015.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "For the starting position, we want to see the feed between the hip and shoulders width, the heels on the floor, a neutral column mediated by abdominal tension, the shoulders are lightly in front of the bar or above, straight arms, symmetrical hands and enough width to not rather the knees and we can have a lightly look forward.",
          "positive": 0.99,
          "negative": 0.01,
          "neutral": 0.0
        },
        {
          "snippet": "To perform the movement, our athlete will push from the heels, he will start to raise the hips and shoulders together, when the bar passes the knees, we extend the hip.",
          "positive": 0.996,
          "negative": 0.004,
          "neutral": 0.0
        },
        {
          "snippet": "For return, we are going to delay the push of the knees and we are going to push the hip back and the chess forward.",
          "positive": 0.006,
          "negative": 0.994,
          "neutral": 0.0
        },
        {
          "snippet": "When the bar passes the knees, we have the correct angle of our trunk and we already blessed the knees to approximately half the hip for starting position and resting.",
          "positive": 0.493,
          "negative": 0.507,
          "neutral": 0.0
        },
        {
          "snippet": "Throughout the movement, we want to see the bar close to the body when going up and down.",
          "positive": 0.972,
          "negative": 0.028,
          "neutral": 0.0
        }
      ],
      "process_output_files": [
        "/Users/jeremywatt/Desktop/krixik/code/krixik-docs/docs/examples/transcribe/efdc2954-9bef-4427-8de1-2bd18a830015.json"
      ]
    }



```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
