# Multilingual-to-english translation with sentiment analysis pipeline

This document details a modular pipeline that takes in an a text file in a non-english language, transcribes it, translates the transcription into english, and then performs sentiment analysis on each sentence of the translated transcript.

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

Below we setup a multi module pipeline to serve our intended purpose we use the following modules:

- [`parser`](modules/parser.md): takes in a text file and splits it into snippets
- [`translate`](modules/translate.md): takes in text, slices into (possibly overlapping) strings
- [`json-to-txt`](modules/json-to-txt.md): takes in json of text snippets, merges into text file
- [`parser`](modules/parser.md): takes in text, slices into (possibly overlapping) strings
- [`sentiment`](modules/sentiment.md): takes in text snippets and returns scores for their sentiments

We do this by passing the module names to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a multi-module pipeline
pipeline = krixik.create_pipeline(name="examples-multilingual-sentiment-docs",
                                  module_chain=["parser",
                                                "translate",
                                                "json-to-txt",
                                                "parser",
                                                "sentiment"])
```

With our `custom` pipeline built we now pass it, along with a test file, to our operator to process the file.


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```

## Processing a file

Lets take a quick look at a test file before processing.

This is a short review in spanish.


```python
# examine contents of a valid test input file
test_file = "../../../data/input/spanish_review.txt"
with open(test_file, "r") as file:
    print(file.read())
```

    Para los trabajos que estoy haciendo me resultó muy bueno. En una hora carga la batería y dura más de 3 horas de trabajo continuo. Un golazo contar con una segunda batería. Cómodo y con buen torque. Estoy conforme.


The input video content language content is English.  We will use the `opus-mt-es-en` model of the [`translate`](modules/translate.md) to translate the transcript of this video into Spanish.

For this run we will use the default models for the remainder of the modules.



```python
# test file
test_file = "../../../data/input/spanish_review.txt"

# process test input
process_output = pipeline.process(local_file_path = test_file,
                                  expire_time=60*10,
                                  modules={
                                      "module_2": {"model": "opus-mt-es-en"}
                                      },
                                  verbose=False,
                                  local_save_directory="../../../data/output")
```

The output of this process is printed below.  Because the output of this particular module-model pair is text, the process output is provided in this object is null.  However the file itself has been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "examples-multilingual-sentiment-docs",
      "request_id": "5458c389-7a63-4a4e-85b5-040b0487db92",
      "file_id": "cf26912e-87d9-4d7d-a6c0-a0786d8392eb",
      "message": "SUCCESS - output fetched for file_id cf26912e-87d9-4d7d-a6c0-a0786d8392eb.Output saved to location(s) listed in process_output_files.",
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
        "../../../data/output/cf26912e-87d9-4d7d-a6c0-a0786d8392eb.json"
      ]
    }



```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
