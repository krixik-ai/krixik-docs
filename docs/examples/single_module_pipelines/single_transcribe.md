## Single-Module Pipeline: `transcribe`

This document is a walkthrough of how to assemble and use a single-module pipeline that only includes a [`transcribe`](../../modules/ai_model_modules/transcribe_module.md) module. It is divided into the following sections:

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

Let's first instantiate a single-module [`transcribe`](../../modules/ai_model_modules/transcribe_module.md)  pipeline.

We use the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method for this, passing only the [`transcribe`](../../modules/ai_model_modules/transcribe_module.md)  module name into `module_chain`.


```python
# create a pipeline with a single transcribe module

pipeline_1 = krixik.create_pipeline(name="single_transcribe_1",
                                    module_chain=["transcribe"])
```

### Required Input Format

The [`transcribe`](../../modules/ai_model_modules/transcribe_module.md)  module accepts audio inputs. Acceptable file formats are only MP3 for the time being.

Let's take a quick look at a valid input file, and then process it.


```python
# examine contents of a valid input file

from IPython.display import Video

Video("../../../data/input/Interesting Facts About Colombia.mp3")
```




<video src="../../../data/input/Interesting Facts About Colombia.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



### Using the Default Model

Let's process our test input file using the [`transcribe`](../../modules/ai_model_modules/transcribe_module.md)  module's [default model](../../modules/ai_model_modules/transcribe_module.md#available-models-in-the-transcribe-module) : [`whisper-tiny`](https://huggingface.co/openai/whisper-tiny).

Given that this is the default model, we need not specify model selection through the optional [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file with the default model

process_output_1 = pipeline_1.process(local_file_path="../../../data/input/Interesting Facts About Colombia.mp3", # the initial local filepath where the input file is stored
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
      "pipeline": "single_transcribe_1",
      "request_id": "7112b2bf-4f00-4a05-8640-fd64523fe53c",
      "file_id": "031af2e4-23ee-4f66-969e-6a02c91c10cd",
      "message": "SUCCESS - output fetched for file_id 031af2e4-23ee-4f66-969e-6a02c91c10cd.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "transcript": " This episode, looking at the great country of Columbia, we looked at some really basic facts. It's name, a bit of its history, the type of people that live there, land size, and all that jazz. But in this video, we're going to go into a little bit more of a detailed look. Yo, what is going on guys? Welcome back to F2D facts. The channel where I look at people cultures and places, my name is Dave Wouple, and today we are going to be looking more at Columbia in our Columbia Part 2 video. Which just reminds me guys, this is part of our Columbia playlist. So put it down in the description box below and I'll talk about that more at the end of the video. But if you're new here, join me every single Monday to learn about new countries from around the world. You can do that by hitting that subscribe and that belt notification button. But let's get started. So we all know, Columbia is famous for its coffee, right? Yes, right. I know. You guys are sitting there going, five bucks says he's going to talk about coffee. Well, I am. That's right, because I got my van, you Columbia coffee. Right here. Boom advertisement. Yeah. Pain me for this. I'm care. So which might not know about coffee is yes, you probably already know that a lot of companies actually buy it up. Starbucks buys all had a coffee from Columbia. It's kind of like their favorite place to buy coffee. And kind of to pay tribute to that Starbucks when they were making their 1,000th store in 2016, they decided, yo, we're going to put it in Columbia. And this was in the town of Medellin, Columbia. Now here's the thing when it comes to coffee in Columbia. They are the third largest producing and exporting coffee country in the world. The amount of coffee that is exported from Columbia equals about 810,000 metric tons. Or approximately 11.5 million bags. However, although it might be beaten by countries like Brazil, it is actually the number one or highest country for producing and growing a specific type of being known as the Arabica being. And I know coffee is really important when it comes to talking about Columbia, but you really don't know how important it is with its culture. Interesting fact that in 2007, major spots, equaling a buffer zone of approximately 207,000 hectares, which are called the coffee cultural landscape, were considered a UNESCO World Heritage Site. And also in 2007, the EU, the European Union, granted Colombian coffee, a protected designation of origin status. Now, interesting enough when it comes to the coffee in Columbia, believe it or not, it is not actually native to the country. It's come from somewhere else, not really an invasive species because it's very much welcomed. Now you may have also seen this guy on many different Colombian coffee brands. Now his name is Juan Valdez. Now some people think that this guy is actually really a real coffee farmer, somebody just",
          "timestamped_transcript": [
            {
              "id": 0,
              "start": 0.0,
              "end": 4.25,
              "text": " This episode, looking at the great country of Columbia, we looked at some really basic facts.",
              "no_speech_prob": 0.5648887157440186,
              "confidence": 0.758,
              "words": [
                {
                  "text": "This",
                  "start": 0.0,
                  "end": 0.1,
                  "confidence": 0.148
                },
                {
                  "text": "episode,",
                  "start": 0.1,
                  "end": 0.44,
                  "confidence": 0.69
                },
                {
                  "text": "looking",
                  "start": 0.54,
                  "end": 0.8,
                  "confidence": 0.835
                },
                {
                  "text": "at",
                  "start": 0.8,
                  "end": 1.0,
                  "confidence": 0.994
                },
                {
                  "text": "the",
                  "start": 1.0,
                  "end": 1.1,
                  "confidence": 0.964
                },
                {
                  "text": "great",
                  "start": 1.1,
                  "end": 1.3,
                  "confidence": 0.97
                },
                {
                  "text": "country",
                  "start": 1.3,
                  "end": 1.66,
                  "confidence": 0.983
                },
                {
                  "text": "of",
                  "start": 1.66,
                  "end": 1.78,
                  "confidence": 0.982
                },
                {
                  "text": "Columbia,",
                  "start": 1.78,
                  "end": 2.12,
                  "confidence": 0.638
                },
                {
                  "text": "we",
                  "start": 2.2,
                  "end": 2.32,
                  "confidence": 0.584
                },
                {
                  "text": "looked",
                  "start": 2.32,
                  "end": 2.6,
                  "confidence": 0.962
                },
                {
                  "text": "at",
                  "start": 2.6,
                  "end": 2.72,
                  "confidence": 0.992
                },
                {
                  "text": "some",
                  "start": 2.72,
                  "end": 3.0,
                  "confidence": 0.982
                },
                {
                  "text": "really",
                  "start": 3.0,
                  "end": 3.28,
                  "confidence": 0.931
                },
                {
                  "text": "basic",
                  "start": 3.28,
                  "end": 3.88,
                  "confidence": 0.603
                },
                {
                  "text": "facts.",
                  "start": 3.88,
                  "end": 4.25,
                  "confidence": 0.796
                }
              ]
            },
            {
              "id": 1,
              "start": 4.25,
              "end": 8.68,
              "text": " It's name, a bit of its history, the type of people that live there, land size, and all",
              "no_speech_prob": 0.5648887157440186,
              "confidence": 0.885,
              "words": [
                {
                  "text": "It's",
                  "start": 4.25,
                  "end": 4.58,
                  "confidence": 0.858
                },
                {
                  "text": "name,",
                  "start": 4.58,
                  "end": 4.94,
                  "confidence": 0.899
                },
                {
                  "text": "a",
                  "start": 4.98,
                  "end": 5.08,
                  "confidence": 0.983
                },
                {
                  "text": "bit",
                  "start": 5.08,
                  "end": 5.2,
                  "confidence": 0.995
                },
                {
                  "text": "of",
                  "start": 5.2,
                  "end": 5.32,
                  "confidence": 0.995
                },
                {
                  "text": "its",
                  "start": 5.32,
                  "end": 5.48,
                  "confidence": 0.853
                },
                {
                  "text": "history,",
                  "start": 5.48,
                  "end": 5.9,
                  "confidence": 0.998
                },
                {
                  "text": "the",
                  "start": 6.04,
                  "end": 6.38,
                  "confidence": 0.9
                },
                {
                  "text": "type",
                  "start": 6.38,
                  "end": 6.52,
                  "confidence": 0.966
                },
                {
                  "text": "of",
                  "start": 6.52,
                  "end": 6.62,
                  "confidence": 0.994
                },
                {
                  "text": "people",
                  "start": 6.62,
                  "end": 6.8,
                  "confidence": 0.998
                },
                {
                  "text": "that",
                  "start": 6.8,
                  "end": 6.96,
                  "confidence": 0.983
                },
                {
                  "text": "live",
                  "start": 6.96,
                  "end": 7.22,
                  "confidence": 0.632
                },
                {
                  "text": "there,",
                  "start": 7.22,
                  "end": 7.46,
                  "confidence": 0.863
                },
                {
                  "text": "land",
                  "start": 7.54,
                  "end": 7.86,
                  "confidence": 0.69
                },
                {
                  "text": "size,",
                  "start": 7.86,
                  "end": 8.28,
                  "confidence": 0.771
                },
                {
                  "text": "and",
                  "start": 8.42,
                  "end": 8.48,
                  "confidence": 0.988
                },
                {
                  "text": "all",
                  "start": 8.48,
                  "end": 8.68,
                  "confidence": 0.728
                }
              ]
            },
            {
              "id": 2,
              "start": 8.68,
              "end": 9.22,
              "text": " that jazz.",
              "no_speech_prob": 0.5648887157440186,
              "confidence": 0.986,
              "words": [
                {
                  "text": "that",
                  "start": 8.68,
                  "end": 8.92,
                  "confidence": 0.984
                },
                {
                  "text": "jazz.",
                  "start": 8.92,
                  "end": 9.22,
                  "confidence": 0.988
                }
              ]
            },
            {
              "id": 3,
              "start": 9.52,
              "end": 12.56,
              "text": " But in this video, we're going to go into a little bit more of a detailed look.",
              "no_speech_prob": 0.5648887157440186,
              "confidence": 0.968,
              "words": [
                {
                  "text": "But",
                  "start": 9.52,
                  "end": 9.64,
                  "confidence": 0.932
                },
                {
                  "text": "in",
                  "start": 9.64,
                  "end": 9.72,
                  "confidence": 0.986
                },
                {
                  "text": "this",
                  "start": 9.72,
                  "end": 9.86,
                  "confidence": 0.998
                },
                {
                  "text": "video,",
                  "start": 9.86,
                  "end": 10.08,
                  "confidence": 0.996
                },
                {
                  "text": "we're",
                  "start": 10.14,
                  "end": 10.22,
                  "confidence": 0.977
                },
                {
                  "text": "going",
                  "start": 10.22,
                  "end": 10.34,
                  "confidence": 0.739
                },
                {
                  "text": "to",
                  "start": 10.34,
                  "end": 10.4,
                  "confidence": 0.988
                },
                {
                  "text": "go",
                  "start": 10.4,
                  "end": 10.48,
                  "confidence": 0.969
                },
                {
                  "text": "into",
                  "start": 10.48,
                  "end": 10.72,
                  "confidence": 0.994
                },
                {
                  "text": "a",
                  "start": 10.72,
                  "end": 10.9,
                  "confidence": 0.992
                },
                {
                  "text": "little",
                  "start": 10.9,
                  "end": 11.12,
                  "confidence": 0.992
                },
                {
                  "text": "bit",
                  "start": 11.12,
                  "end": 11.26,
                  "confidence": 0.944
                },
                {
                  "text": "more",
                  "start": 11.26,
                  "end": 11.56,
                  "confidence": 0.996
                },
                {
                  "text": "of",
                  "start": 11.56,
                  "end": 11.76,
                  "confidence": 0.994
                },
                {
                  "text": "a",
                  "start": 11.76,
                  "end": 11.88,
                  "confidence": 0.996
                },
                {
                  "text": "detailed",
                  "start": 11.88,
                  "end": 12.2,
                  "confidence": 0.997
                },
                {
                  "text": "look.",
                  "start": 12.2,
                  "end": 12.56,
                  "confidence": 0.996
                }
              ]
            },
            {
              "id": 4,
              "start": 12.82,
              "end": 14.26,
              "text": " Yo, what is going on guys?",
              "no_speech_prob": 0.5648887157440186,
              "confidence": 0.887,
              "words": [
                {
                  "text": "Yo,",
                  "start": 12.82,
                  "end": 13.04,
                  "confidence": 0.748
                },
                {
                  "text": "what",
                  "start": 13.1,
                  "end": 13.34,
                  "confidence": 0.992
                },
                {
                  "text": "is",
                  "start": 13.34,
                  "end": 13.48,
                  "confidence": 0.969
                },
                {
                  "text": "going",
                  "start": 13.48,
                  "end": 13.68,
                  "confidence": 0.986
                },
                {
                  "text": "on",
                  "start": 13.68,
                  "end": 13.9,
                  "confidence": 1.0
                },
                {
                  "text": "guys?",
                  "start": 13.9,
                  "end": 14.26,
                  "confidence": 0.689
                }
              ]
            },
            {
              "id": 5,
              "start": 14.32,
              "end": 15.6,
              "text": " Welcome back to F2D facts.",
              "no_speech_prob": 0.5648887157440186,
              "confidence": 0.735,
              "words": [
                {
                  "text": "Welcome",
                  "start": 14.32,
                  "end": 14.58,
                  "confidence": 0.988
                },
                {
                  "text": "back",
                  "start": 14.58,
                  "end": 14.8,
                  "confidence": 0.999
                },
                {
                  "text": "to",
                  "start": 14.8,
                  "end": 14.98,
                  "confidence": 0.986
                },
                {
                  "text": "F2D",
                  "start": 14.98,
                  "end": 15.4,
                  "confidence": 0.641
                },
                {
                  "text": "facts.",
                  "start": 15.4,
                  "end": 15.6,
                  "confidence": 0.453
                }
              ]
            },
            {
              "id": 6,
              "start": 15.6,
              "end": 21.6,
              "text": " The channel where I look at people cultures and places, my name is Dave Wouple, and today we",
              "no_speech_prob": 0.5648887157440186,
              "confidence": 0.772,
              "words": [
                {
                  "text": "The",
                  "start": 15.6,
                  "end": 15.86,
                  "confidence": 0.622
                },
                {
                  "text": "channel",
                  "start": 15.86,
                  "end": 16.0,
                  "confidence": 0.89
                },
                {
                  "text": "where",
                  "start": 16.0,
                  "end": 16.16,
                  "confidence": 0.989
                },
                {
                  "text": "I",
                  "start": 16.16,
                  "end": 16.24,
                  "confidence": 0.989
                },
                {
                  "text": "look",
                  "start": 16.24,
                  "end": 16.36,
                  "confidence": 0.994
                },
                {
                  "text": "at",
                  "start": 16.36,
                  "end": 16.46,
                  "confidence": 0.994
                },
                {
                  "text": "people",
                  "start": 16.46,
                  "end": 16.64,
                  "confidence": 0.932
                },
                {
                  "text": "cultures",
                  "start": 16.64,
                  "end": 16.96,
                  "confidence": 0.513
                },
                {
                  "text": "and",
                  "start": 16.96,
                  "end": 17.14,
                  "confidence": 0.91
                },
                {
                  "text": "places,",
                  "start": 17.14,
                  "end": 17.5,
                  "confidence": 0.995
                },
                {
                  "text": "my",
                  "start": 17.58,
                  "end": 17.84,
                  "confidence": 0.96
                },
                {
                  "text": "name",
                  "start": 17.84,
                  "end": 18.62,
                  "confidence": 0.999
                },
                {
                  "text": "is",
                  "start": 18.62,
                  "end": 18.98,
                  "confidence": 0.957
                },
                {
                  "text": "Dave",
                  "start": 18.98,
                  "end": 19.38,
                  "confidence": 0.98
                },
                {
                  "text": "Wouple,",
                  "start": 19.38,
                  "end": 19.98,
                  "confidence": 0.381
                },
                {
                  "text": "and",
                  "start": 20.18,
                  "end": 20.4,
                  "confidence": 0.991
                },
                {
                  "text": "today",
                  "start": 20.4,
                  "end": 21.06,
                  "confidence": 0.969
                },
                {
                  "text": "we",
                  "start": 21.06,
                  "end": 21.6,
                  "confidence": 0.51
                }
              ]
            },
            {
              "id": 7,
              "start": 21.6,
              "end": 25.24,
              "text": " are going to be looking more at Columbia in our Columbia Part 2 video.",
              "no_speech_prob": 0.5648887157440186,
              "confidence": 0.883,
              "words": [
                {
                  "text": "are",
                  "start": 21.6,
                  "end": 22.08,
                  "confidence": 0.994
                },
                {
                  "text": "going",
                  "start": 22.08,
                  "end": 22.2,
                  "confidence": 0.888
                },
                {
                  "text": "to",
                  "start": 22.2,
                  "end": 22.24,
                  "confidence": 0.991
                },
                {
                  "text": "be",
                  "start": 22.24,
                  "end": 22.38,
                  "confidence": 0.995
                },
                {
                  "text": "looking",
                  "start": 22.38,
                  "end": 22.6,
                  "confidence": 0.997
                },
                {
                  "text": "more",
                  "start": 22.6,
                  "end": 22.96,
                  "confidence": 0.92
                },
                {
                  "text": "at",
                  "start": 22.96,
                  "end": 23.22,
                  "confidence": 0.997
                },
                {
                  "text": "Columbia",
                  "start": 23.22,
                  "end": 23.64,
                  "confidence": 0.981
                },
                {
                  "text": "in",
                  "start": 23.64,
                  "end": 23.86,
                  "confidence": 0.529
                },
                {
                  "text": "our",
                  "start": 23.86,
                  "end": 24.02,
                  "confidence": 0.941
                },
                {
                  "text": "Columbia",
                  "start": 24.02,
                  "end": 24.28,
                  "confidence": 0.975
                },
                {
                  "text": "Part",
                  "start": 24.28,
                  "end": 24.52,
                  "confidence": 0.702
                },
                {
                  "text": "2",
                  "start": 24.52,
                  "end": 24.84,
                  "confidence": 0.691
                },
                {
                  "text": "video.",
                  "start": 24.84,
                  "end": 25.24,
                  "confidence": 0.957
                }
              ]
            },
            {
              "id": 8,
              "start": 25.72,
              "end": 28.8,
              "text": " Which just reminds me guys, this is part of our Columbia playlist.",
              "no_speech_prob": 0.5648887157440186,
              "confidence": 0.935,
              "words": [
                {
                  "text": "Which",
                  "start": 25.72,
                  "end": 26.02,
                  "confidence": 0.892
                },
                {
                  "text": "just",
                  "start": 26.02,
                  "end": 26.24,
                  "confidence": 0.981
                },
                {
                  "text": "reminds",
                  "start": 26.24,
                  "end": 26.66,
                  "confidence": 0.995
                },
                {
                  "text": "me",
                  "start": 26.66,
                  "end": 26.88,
                  "confidence": 0.907
                },
                {
                  "text": "guys,",
                  "start": 26.88,
                  "end": 27.02,
                  "confidence": 0.859
                },
                {
                  "text": "this",
                  "start": 27.12,
                  "end": 27.24,
                  "confidence": 0.984
                },
                {
                  "text": "is",
                  "start": 27.24,
                  "end": 27.32,
                  "confidence": 0.972
                },
                {
                  "text": "part",
                  "start": 27.32,
                  "end": 27.54,
                  "confidence": 0.97
                },
                {
                  "text": "of",
                  "start": 27.54,
                  "end": 27.66,
                  "confidence": 0.999
                },
                {
                  "text": "our",
                  "start": 27.66,
                  "end": 27.84,
                  "confidence": 0.992
                },
                {
                  "text": "Columbia",
                  "start": 27.84,
                  "end": 28.24,
                  "confidence": 0.995
                },
                {
                  "text": "playlist.",
                  "start": 28.24,
                  "end": 28.8,
                  "confidence": 0.716
                }
              ]
            },
            {
              "id": 9,
              "start": 28.92,
              "end": 31.58,
              "text": " So put it down in the description box below and I'll talk about that more at the end",
              "no_speech_prob": 0.3092843294143677,
              "confidence": 0.799,
              "words": [
                {
                  "text": "So",
                  "start": 28.92,
                  "end": 28.98,
                  "confidence": 0.376
                },
                {
                  "text": "put",
                  "start": 28.98,
                  "end": 29.06,
                  "confidence": 0.558
                },
                {
                  "text": "it",
                  "start": 29.06,
                  "end": 29.18,
                  "confidence": 0.988
                },
                {
                  "text": "down",
                  "start": 29.18,
                  "end": 29.38,
                  "confidence": 0.991
                },
                {
                  "text": "in",
                  "start": 29.38,
                  "end": 29.52,
                  "confidence": 0.602
                },
                {
                  "text": "the",
                  "start": 29.52,
                  "end": 29.6,
                  "confidence": 0.889
                },
                {
                  "text": "description",
                  "start": 29.6,
                  "end": 29.84,
                  "confidence": 0.998
                },
                {
                  "text": "box",
                  "start": 29.84,
                  "end": 30.12,
                  "confidence": 0.969
                },
                {
                  "text": "below",
                  "start": 30.12,
                  "end": 30.36,
                  "confidence": 0.99
                },
                {
                  "text": "and",
                  "start": 30.36,
                  "end": 30.52,
                  "confidence": 0.489
                },
                {
                  "text": "I'll",
                  "start": 30.52,
                  "end": 30.64,
                  "confidence": 0.932
                },
                {
                  "text": "talk",
                  "start": 30.64,
                  "end": 30.8,
                  "confidence": 0.976
                },
                {
                  "text": "about",
                  "start": 30.8,
                  "end": 30.96,
                  "confidence": 0.963
                },
                {
                  "text": "that",
                  "start": 30.96,
                  "end": 31.06,
                  "confidence": 0.816
                },
                {
                  "text": "more",
                  "start": 31.06,
                  "end": 31.28,
                  "confidence": 0.946
                },
                {
                  "text": "at",
                  "start": 31.28,
                  "end": 31.52,
                  "confidence": 0.501
                },
                {
                  "text": "the",
                  "start": 31.52,
                  "end": 31.54,
                  "confidence": 0.932
                },
                {
                  "text": "end",
                  "start": 31.54,
                  "end": 31.58,
                  "confidence": 0.939
                }
              ]
            },
            {
              "id": 10,
              "start": 31.58,
              "end": 32.36,
              "text": " of the video.",
              "no_speech_prob": 0.3092843294143677,
              "confidence": 0.984,
              "words": [
                {
                  "text": "of",
                  "start": 31.58,
                  "end": 31.82,
                  "confidence": 0.973
                },
                {
                  "text": "the",
                  "start": 31.82,
                  "end": 31.94,
                  "confidence": 0.983
                },
                {
                  "text": "video.",
                  "start": 31.94,
                  "end": 32.36,
                  "confidence": 0.996
                }
              ]
            },
            {
              "id": 11,
              "start": 32.72,
              "end": 35.95,
              "text": " But if you're new here, join me every single Monday to learn about new countries from",
              "no_speech_prob": 0.3092843294143677,
              "confidence": 0.976,
              "words": [
                {
                  "text": "But",
                  "start": 32.72,
                  "end": 32.84,
                  "confidence": 0.98
                },
                {
                  "text": "if",
                  "start": 32.84,
                  "end": 32.94,
                  "confidence": 0.981
                },
                {
                  "text": "you're",
                  "start": 32.94,
                  "end": 33.1,
                  "confidence": 0.973
                },
                {
                  "text": "new",
                  "start": 33.1,
                  "end": 33.22,
                  "confidence": 0.994
                },
                {
                  "text": "here,",
                  "start": 33.22,
                  "end": 33.46,
                  "confidence": 0.994
                },
                {
                  "text": "join",
                  "start": 33.64,
                  "end": 33.92,
                  "confidence": 0.978
                },
                {
                  "text": "me",
                  "start": 33.92,
                  "end": 34.06,
                  "confidence": 0.999
                },
                {
                  "text": "every",
                  "start": 34.06,
                  "end": 34.24,
                  "confidence": 0.862
                },
                {
                  "text": "single",
                  "start": 34.24,
                  "end": 34.44,
                  "confidence": 0.999
                },
                {
                  "text": "Monday",
                  "start": 34.44,
                  "end": 34.7,
                  "confidence": 0.971
                },
                {
                  "text": "to",
                  "start": 34.7,
                  "end": 34.82,
                  "confidence": 0.979
                },
                {
                  "text": "learn",
                  "start": 34.82,
                  "end": 35.0,
                  "confidence": 0.996
                },
                {
                  "text": "about",
                  "start": 35.0,
                  "end": 35.18,
                  "confidence": 0.997
                },
                {
                  "text": "new",
                  "start": 35.18,
                  "end": 35.38,
                  "confidence": 0.992
                },
                {
                  "text": "countries",
                  "start": 35.38,
                  "end": 35.78,
                  "confidence": 0.984
                },
                {
                  "text": "from",
                  "start": 35.78,
                  "end": 35.95,
                  "confidence": 0.956
                }
              ]
            },
            {
              "id": 12,
              "start": 35.95,
              "end": 36.48,
              "text": " around the world.",
              "no_speech_prob": 0.3092843294143677,
              "confidence": 0.988,
              "words": [
                {
                  "text": "around",
                  "start": 35.95,
                  "end": 36.22,
                  "confidence": 0.991
                },
                {
                  "text": "the",
                  "start": 36.22,
                  "end": 36.34,
                  "confidence": 0.973
                },
                {
                  "text": "world.",
                  "start": 36.34,
                  "end": 36.48,
                  "confidence": 0.998
                }
              ]
            },
            {
              "id": 13,
              "start": 36.48,
              "end": 39.32,
              "text": " You can do that by hitting that subscribe and that belt notification button.",
              "no_speech_prob": 0.3092843294143677,
              "confidence": 0.913,
              "words": [
                {
                  "text": "You",
                  "start": 36.48,
                  "end": 36.58,
                  "confidence": 0.972
                },
                {
                  "text": "can",
                  "start": 36.58,
                  "end": 36.72,
                  "confidence": 0.994
                },
                {
                  "text": "do",
                  "start": 36.72,
                  "end": 36.82,
                  "confidence": 0.996
                },
                {
                  "text": "that",
                  "start": 36.82,
                  "end": 36.98,
                  "confidence": 0.997
                },
                {
                  "text": "by",
                  "start": 36.98,
                  "end": 37.16,
                  "confidence": 0.952
                },
                {
                  "text": "hitting",
                  "start": 37.16,
                  "end": 37.36,
                  "confidence": 0.913
                },
                {
                  "text": "that",
                  "start": 37.36,
                  "end": 37.48,
                  "confidence": 0.993
                },
                {
                  "text": "subscribe",
                  "start": 37.48,
                  "end": 37.92,
                  "confidence": 0.965
                },
                {
                  "text": "and",
                  "start": 37.92,
                  "end": 38.12,
                  "confidence": 0.678
                },
                {
                  "text": "that",
                  "start": 38.12,
                  "end": 38.32,
                  "confidence": 0.967
                },
                {
                  "text": "belt",
                  "start": 38.32,
                  "end": 38.46,
                  "confidence": 0.623
                },
                {
                  "text": "notification",
                  "start": 38.46,
                  "end": 39.04,
                  "confidence": 0.943
                },
                {
                  "text": "button.",
                  "start": 39.04,
                  "end": 39.32,
                  "confidence": 0.998
                }
              ]
            },
            {
              "id": 14,
              "start": 39.32,
              "end": 41.56,
              "text": " But let's get started.",
              "no_speech_prob": 0.3092843294143677,
              "confidence": 0.838,
              "words": [
                {
                  "text": "But",
                  "start": 39.32,
                  "end": 40.38,
                  "confidence": 0.982
                },
                {
                  "text": "let's",
                  "start": 40.38,
                  "end": 41.02,
                  "confidence": 0.654
                },
                {
                  "text": "get",
                  "start": 41.02,
                  "end": 41.18,
                  "confidence": 0.984
                },
                {
                  "text": "started.",
                  "start": 41.18,
                  "end": 41.56,
                  "confidence": 0.998
                }
              ]
            },
            {
              "id": 15,
              "start": 41.56,
              "end": 46.6,
              "text": " So we all know, Columbia is famous for its coffee, right?",
              "no_speech_prob": 0.3092843294143677,
              "confidence": 0.839,
              "words": [
                {
                  "text": "So",
                  "start": 41.56,
                  "end": 42.9,
                  "confidence": 0.234
                },
                {
                  "text": "we",
                  "start": 42.9,
                  "end": 43.52,
                  "confidence": 0.861
                },
                {
                  "text": "all",
                  "start": 43.52,
                  "end": 43.66,
                  "confidence": 0.999
                },
                {
                  "text": "know,",
                  "start": 43.66,
                  "end": 43.92,
                  "confidence": 0.999
                },
                {
                  "text": "Columbia",
                  "start": 44.06,
                  "end": 44.54,
                  "confidence": 0.99
                },
                {
                  "text": "is",
                  "start": 44.54,
                  "end": 44.86,
                  "confidence": 0.988
                },
                {
                  "text": "famous",
                  "start": 44.86,
                  "end": 45.24,
                  "confidence": 0.994
                },
                {
                  "text": "for",
                  "start": 45.24,
                  "end": 45.56,
                  "confidence": 0.999
                },
                {
                  "text": "its",
                  "start": 45.56,
                  "end": 45.8,
                  "confidence": 0.854
                },
                {
                  "text": "coffee,",
                  "start": 45.8,
                  "end": 46.24,
                  "confidence": 0.877
                },
                {
                  "text": "right?",
                  "start": 46.34,
                  "end": 46.6,
                  "confidence": 0.996
                }
              ]
            },
            {
              "id": 16,
              "start": 46.84,
              "end": 47.37,
              "text": " Yes, right.",
              "no_speech_prob": 0.3092843294143677,
              "confidence": 0.971,
              "words": [
                {
                  "text": "Yes,",
                  "start": 46.84,
                  "end": 47.06,
                  "confidence": 0.969
                },
                {
                  "text": "right.",
                  "start": 47.28,
                  "end": 47.37,
                  "confidence": 0.973
                }
              ]
            },
            {
              "id": 17,
              "start": 47.37,
              "end": 47.9,
              "text": " I know.",
              "no_speech_prob": 0.3092843294143677,
              "confidence": 0.911,
              "words": [
                {
                  "text": "I",
                  "start": 47.37,
                  "end": 47.72,
                  "confidence": 0.83
                },
                {
                  "text": "know.",
                  "start": 47.72,
                  "end": 47.9,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 18,
              "start": 48.32,
              "end": 50.8,
              "text": " You guys are sitting there going, five bucks says he's going to talk about coffee.",
              "no_speech_prob": 0.3092843294143677,
              "confidence": 0.847,
              "words": [
                {
                  "text": "You",
                  "start": 48.32,
                  "end": 48.34,
                  "confidence": 0.747
                },
                {
                  "text": "guys",
                  "start": 48.34,
                  "end": 48.36,
                  "confidence": 0.996
                },
                {
                  "text": "are",
                  "start": 48.36,
                  "end": 48.44,
                  "confidence": 0.839
                },
                {
                  "text": "sitting",
                  "start": 48.44,
                  "end": 48.62,
                  "confidence": 0.957
                },
                {
                  "text": "there",
                  "start": 48.62,
                  "end": 48.72,
                  "confidence": 0.976
                },
                {
                  "text": "going,",
                  "start": 48.72,
                  "end": 48.84,
                  "confidence": 0.938
                },
                {
                  "text": "five",
                  "start": 48.92,
                  "end": 49.5,
                  "confidence": 0.367
                },
                {
                  "text": "bucks",
                  "start": 49.5,
                  "end": 49.72,
                  "confidence": 0.977
                },
                {
                  "text": "says",
                  "start": 49.72,
                  "end": 49.92,
                  "confidence": 0.971
                },
                {
                  "text": "he's",
                  "start": 49.92,
                  "end": 50.06,
                  "confidence": 0.676
                },
                {
                  "text": "going",
                  "start": 50.06,
                  "end": 50.14,
                  "confidence": 0.889
                },
                {
                  "text": "to",
                  "start": 50.14,
                  "end": 50.24,
                  "confidence": 0.992
                },
                {
                  "text": "talk",
                  "start": 50.24,
                  "end": 50.38,
                  "confidence": 0.99
                },
                {
                  "text": "about",
                  "start": 50.38,
                  "end": 50.54,
                  "confidence": 0.991
                },
                {
                  "text": "coffee.",
                  "start": 50.54,
                  "end": 50.8,
                  "confidence": 0.923
                }
              ]
            },
            {
              "id": 19,
              "start": 50.8,
              "end": 51.98,
              "text": " Well, I am.",
              "no_speech_prob": 0.3092843294143677,
              "confidence": 0.984,
              "words": [
                {
                  "text": "Well,",
                  "start": 50.8,
                  "end": 51.32,
                  "confidence": 0.992
                },
                {
                  "text": "I",
                  "start": 51.44,
                  "end": 51.58,
                  "confidence": 0.986
                },
                {
                  "text": "am.",
                  "start": 51.58,
                  "end": 51.98,
                  "confidence": 0.974
                }
              ]
            },
            {
              "id": 20,
              "start": 52.16,
              "end": 54.34,
              "text": " That's right, because I got my van, you Columbia coffee.",
              "no_speech_prob": 0.3092843294143677,
              "confidence": 0.864,
              "words": [
                {
                  "text": "That's",
                  "start": 52.16,
                  "end": 52.36,
                  "confidence": 0.996
                },
                {
                  "text": "right,",
                  "start": 52.36,
                  "end": 52.48,
                  "confidence": 0.998
                },
                {
                  "text": "because",
                  "start": 52.52,
                  "end": 52.68,
                  "confidence": 0.997
                },
                {
                  "text": "I",
                  "start": 52.68,
                  "end": 52.74,
                  "confidence": 0.996
                },
                {
                  "text": "got",
                  "start": 52.74,
                  "end": 52.9,
                  "confidence": 0.971
                },
                {
                  "text": "my",
                  "start": 52.9,
                  "end": 53.0,
                  "confidence": 0.998
                },
                {
                  "text": "van,",
                  "start": 53.0,
                  "end": 53.3,
                  "confidence": 0.922
                },
                {
                  "text": "you",
                  "start": 53.62,
                  "end": 53.64,
                  "confidence": 0.375
                },
                {
                  "text": "Columbia",
                  "start": 53.64,
                  "end": 53.96,
                  "confidence": 0.872
                },
                {
                  "text": "coffee.",
                  "start": 53.96,
                  "end": 54.34,
                  "confidence": 0.698
                }
              ]
            },
            {
              "id": 21,
              "start": 54.44,
              "end": 54.94,
              "text": " Right here.",
              "no_speech_prob": 0.3092843294143677,
              "confidence": 0.981,
              "words": [
                {
                  "text": "Right",
                  "start": 54.44,
                  "end": 54.68,
                  "confidence": 0.966
                },
                {
                  "text": "here.",
                  "start": 54.68,
                  "end": 54.94,
                  "confidence": 0.996
                }
              ]
            },
            {
              "id": 22,
              "start": 55.26,
              "end": 56.34,
              "text": " Boom advertisement.",
              "no_speech_prob": 0.3092843294143677,
              "confidence": 0.64,
              "words": [
                {
                  "text": "Boom",
                  "start": 55.26,
                  "end": 55.58,
                  "confidence": 0.962
                },
                {
                  "text": "advertisement.",
                  "start": 55.58,
                  "end": 56.34,
                  "confidence": 0.426
                }
              ]
            },
            {
              "id": 23,
              "start": 56.66,
              "end": 56.86,
              "text": " Yeah.",
              "no_speech_prob": 0.3092843294143677,
              "confidence": 0.904,
              "words": [
                {
                  "text": "Yeah.",
                  "start": 56.66,
                  "end": 56.86,
                  "confidence": 0.904
                }
              ]
            },
            {
              "id": 24,
              "start": 57.54,
              "end": 58.2,
              "text": " Pain me for this.",
              "no_speech_prob": 0.06657163053750992,
              "confidence": 0.614,
              "words": [
                {
                  "text": "Pain",
                  "start": 57.54,
                  "end": 57.76,
                  "confidence": 0.149
                },
                {
                  "text": "me",
                  "start": 57.76,
                  "end": 57.9,
                  "confidence": 0.957
                },
                {
                  "text": "for",
                  "start": 57.9,
                  "end": 58.04,
                  "confidence": 0.995
                },
                {
                  "text": "this.",
                  "start": 58.04,
                  "end": 58.2,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 25,
              "start": 58.2,
              "end": 58.78,
              "text": " I'm care.",
              "no_speech_prob": 0.06657163053750992,
              "confidence": 0.891,
              "words": [
                {
                  "text": "I'm",
                  "start": 58.2,
                  "end": 58.5,
                  "confidence": 0.982
                },
                {
                  "text": "care.",
                  "start": 58.5,
                  "end": 58.78,
                  "confidence": 0.732
                }
              ]
            },
            {
              "id": 26,
              "start": 59.04,
              "end": 62.43,
              "text": " So which might not know about coffee is yes, you probably already know that a lot of",
              "no_speech_prob": 0.06657163053750992,
              "confidence": 0.894,
              "words": [
                {
                  "text": "So",
                  "start": 59.04,
                  "end": 59.2,
                  "confidence": 0.922
                },
                {
                  "text": "which",
                  "start": 59.2,
                  "end": 59.32,
                  "confidence": 0.538
                },
                {
                  "text": "might",
                  "start": 59.32,
                  "end": 59.48,
                  "confidence": 0.7
                },
                {
                  "text": "not",
                  "start": 59.48,
                  "end": 59.64,
                  "confidence": 0.997
                },
                {
                  "text": "know",
                  "start": 59.64,
                  "end": 59.82,
                  "confidence": 0.989
                },
                {
                  "text": "about",
                  "start": 59.82,
                  "end": 60.08,
                  "confidence": 0.994
                },
                {
                  "text": "coffee",
                  "start": 60.08,
                  "end": 60.52,
                  "confidence": 0.98
                },
                {
                  "text": "is",
                  "start": 60.52,
                  "end": 60.76,
                  "confidence": 0.869
                },
                {
                  "text": "yes,",
                  "start": 60.76,
                  "end": 60.92,
                  "confidence": 0.797
                },
                {
                  "text": "you",
                  "start": 61.02,
                  "end": 61.12,
                  "confidence": 0.996
                },
                {
                  "text": "probably",
                  "start": 61.12,
                  "end": 61.36,
                  "confidence": 0.946
                },
                {
                  "text": "already",
                  "start": 61.36,
                  "end": 61.68,
                  "confidence": 0.996
                },
                {
                  "text": "know",
                  "start": 61.68,
                  "end": 61.9,
                  "confidence": 0.993
                },
                {
                  "text": "that",
                  "start": 61.9,
                  "end": 62.12,
                  "confidence": 0.873
                },
                {
                  "text": "a",
                  "start": 62.12,
                  "end": 62.26,
                  "confidence": 0.985
                },
                {
                  "text": "lot",
                  "start": 62.26,
                  "end": 62.4,
                  "confidence": 0.986
                },
                {
                  "text": "of",
                  "start": 62.4,
                  "end": 62.43,
                  "confidence": 0.811
                }
              ]
            },
            {
              "id": 27,
              "start": 62.43,
              "end": 64.02,
              "text": " companies actually buy it up.",
              "no_speech_prob": 0.06657163053750992,
              "confidence": 0.95,
              "words": [
                {
                  "text": "companies",
                  "start": 62.43,
                  "end": 62.96,
                  "confidence": 0.991
                },
                {
                  "text": "actually",
                  "start": 62.96,
                  "end": 63.46,
                  "confidence": 0.969
                },
                {
                  "text": "buy",
                  "start": 63.46,
                  "end": 63.76,
                  "confidence": 0.812
                },
                {
                  "text": "it",
                  "start": 63.76,
                  "end": 63.86,
                  "confidence": 0.992
                },
                {
                  "text": "up.",
                  "start": 63.86,
                  "end": 64.02,
                  "confidence": 0.998
                }
              ]
            },
            {
              "id": 28,
              "start": 64.28,
              "end": 67.18,
              "text": " Starbucks buys all had a coffee from Columbia.",
              "no_speech_prob": 0.06657163053750992,
              "confidence": 0.767,
              "words": [
                {
                  "text": "Starbucks",
                  "start": 64.28,
                  "end": 64.78,
                  "confidence": 0.765
                },
                {
                  "text": "buys",
                  "start": 64.78,
                  "end": 65.16,
                  "confidence": 0.983
                },
                {
                  "text": "all",
                  "start": 65.16,
                  "end": 65.56,
                  "confidence": 0.688
                },
                {
                  "text": "had",
                  "start": 65.56,
                  "end": 65.76,
                  "confidence": 0.244
                },
                {
                  "text": "a",
                  "start": 65.76,
                  "end": 65.92,
                  "confidence": 0.99
                },
                {
                  "text": "coffee",
                  "start": 65.92,
                  "end": 66.3,
                  "confidence": 0.991
                },
                {
                  "text": "from",
                  "start": 66.3,
                  "end": 66.6,
                  "confidence": 0.997
                },
                {
                  "text": "Columbia.",
                  "start": 66.6,
                  "end": 67.18,
                  "confidence": 0.968
                }
              ]
            },
            {
              "id": 29,
              "start": 67.7,
              "end": 69.68,
              "text": " It's kind of like their favorite place to buy coffee.",
              "no_speech_prob": 0.06657163053750992,
              "confidence": 0.961,
              "words": [
                {
                  "text": "It's",
                  "start": 67.7,
                  "end": 67.84,
                  "confidence": 0.977
                },
                {
                  "text": "kind",
                  "start": 67.84,
                  "end": 67.92,
                  "confidence": 0.874
                },
                {
                  "text": "of",
                  "start": 67.92,
                  "end": 68.0,
                  "confidence": 0.99
                },
                {
                  "text": "like",
                  "start": 68.0,
                  "end": 68.1,
                  "confidence": 0.995
                },
                {
                  "text": "their",
                  "start": 68.1,
                  "end": 68.2,
                  "confidence": 0.83
                },
                {
                  "text": "favorite",
                  "start": 68.2,
                  "end": 68.44,
                  "confidence": 0.975
                },
                {
                  "text": "place",
                  "start": 68.44,
                  "end": 68.66,
                  "confidence": 0.997
                },
                {
                  "text": "to",
                  "start": 68.66,
                  "end": 68.84,
                  "confidence": 0.989
                },
                {
                  "text": "buy",
                  "start": 68.84,
                  "end": 69.24,
                  "confidence": 0.996
                },
                {
                  "text": "coffee.",
                  "start": 69.24,
                  "end": 69.68,
                  "confidence": 0.992
                }
              ]
            },
            {
              "id": 30,
              "start": 70.02,
              "end": 74.69,
              "text": " And kind of to pay tribute to that Starbucks when they were making their 1,000th store",
              "no_speech_prob": 0.06657163053750992,
              "confidence": 0.878,
              "words": [
                {
                  "text": "And",
                  "start": 70.02,
                  "end": 70.18,
                  "confidence": 0.99
                },
                {
                  "text": "kind",
                  "start": 70.18,
                  "end": 70.36,
                  "confidence": 0.625
                },
                {
                  "text": "of",
                  "start": 70.36,
                  "end": 70.48,
                  "confidence": 0.996
                },
                {
                  "text": "to",
                  "start": 70.48,
                  "end": 70.62,
                  "confidence": 0.965
                },
                {
                  "text": "pay",
                  "start": 70.62,
                  "end": 70.88,
                  "confidence": 0.996
                },
                {
                  "text": "tribute",
                  "start": 70.88,
                  "end": 71.32,
                  "confidence": 0.999
                },
                {
                  "text": "to",
                  "start": 71.32,
                  "end": 71.58,
                  "confidence": 0.995
                },
                {
                  "text": "that",
                  "start": 71.58,
                  "end": 71.9,
                  "confidence": 0.997
                },
                {
                  "text": "Starbucks",
                  "start": 71.9,
                  "end": 72.72,
                  "confidence": 0.851
                },
                {
                  "text": "when",
                  "start": 72.72,
                  "end": 72.98,
                  "confidence": 0.818
                },
                {
                  "text": "they",
                  "start": 72.98,
                  "end": 73.06,
                  "confidence": 0.988
                },
                {
                  "text": "were",
                  "start": 73.06,
                  "end": 73.2,
                  "confidence": 0.557
                },
                {
                  "text": "making",
                  "start": 73.2,
                  "end": 73.42,
                  "confidence": 0.998
                },
                {
                  "text": "their",
                  "start": 73.42,
                  "end": 73.62,
                  "confidence": 0.986
                },
                {
                  "text": "1,000th",
                  "start": 73.62,
                  "end": 74.58,
                  "confidence": 0.831
                },
                {
                  "text": "store",
                  "start": 74.58,
                  "end": 74.69,
                  "confidence": 0.806
                }
              ]
            },
            {
              "id": 31,
              "start": 74.69,
              "end": 79.36,
              "text": " in 2016, they decided, yo, we're going to put it in Columbia.",
              "no_speech_prob": 0.06657163053750992,
              "confidence": 0.951,
              "words": [
                {
                  "text": "in",
                  "start": 74.69,
                  "end": 75.12,
                  "confidence": 0.995
                },
                {
                  "text": "2016,",
                  "start": 75.12,
                  "end": 76.42,
                  "confidence": 0.995
                },
                {
                  "text": "they",
                  "start": 76.62,
                  "end": 77.06,
                  "confidence": 0.993
                },
                {
                  "text": "decided,",
                  "start": 77.06,
                  "end": 77.56,
                  "confidence": 0.998
                },
                {
                  "text": "yo,",
                  "start": 77.66,
                  "end": 77.96,
                  "confidence": 0.615
                },
                {
                  "text": "we're",
                  "start": 78.02,
                  "end": 78.2,
                  "confidence": 0.979
                },
                {
                  "text": "going",
                  "start": 78.2,
                  "end": 78.36,
                  "confidence": 0.917
                },
                {
                  "text": "to",
                  "start": 78.36,
                  "end": 78.4,
                  "confidence": 0.998
                },
                {
                  "text": "put",
                  "start": 78.4,
                  "end": 78.58,
                  "confidence": 0.998
                },
                {
                  "text": "it",
                  "start": 78.58,
                  "end": 78.7,
                  "confidence": 0.997
                },
                {
                  "text": "in",
                  "start": 78.7,
                  "end": 78.84,
                  "confidence": 0.997
                },
                {
                  "text": "Columbia.",
                  "start": 78.84,
                  "end": 79.36,
                  "confidence": 0.986
                }
              ]
            },
            {
              "id": 32,
              "start": 79.82,
              "end": 82.27,
              "text": " And this was in the town of Medellin, Columbia.",
              "no_speech_prob": 0.06657163053750992,
              "confidence": 0.903,
              "words": [
                {
                  "text": "And",
                  "start": 79.82,
                  "end": 80.0,
                  "confidence": 0.979
                },
                {
                  "text": "this",
                  "start": 80.0,
                  "end": 80.22,
                  "confidence": 0.998
                },
                {
                  "text": "was",
                  "start": 80.22,
                  "end": 80.42,
                  "confidence": 0.991
                },
                {
                  "text": "in",
                  "start": 80.42,
                  "end": 80.58,
                  "confidence": 0.99
                },
                {
                  "text": "the",
                  "start": 80.58,
                  "end": 80.7,
                  "confidence": 0.993
                },
                {
                  "text": "town",
                  "start": 80.7,
                  "end": 80.98,
                  "confidence": 0.993
                },
                {
                  "text": "of",
                  "start": 80.98,
                  "end": 81.22,
                  "confidence": 0.999
                },
                {
                  "text": "Medellin,",
                  "start": 81.22,
                  "end": 81.72,
                  "confidence": 0.706
                },
                {
                  "text": "Columbia.",
                  "start": 81.78,
                  "end": 82.27,
                  "confidence": 0.977
                }
              ]
            },
            {
              "id": 33,
              "start": 82.27,
              "end": 85.4,
              "text": " Now here's the thing when it comes to coffee in Columbia.",
              "no_speech_prob": 0.06657163053750992,
              "confidence": 0.893,
              "words": [
                {
                  "text": "Now",
                  "start": 82.27,
                  "end": 82.74,
                  "confidence": 0.71
                },
                {
                  "text": "here's",
                  "start": 82.74,
                  "end": 83.06,
                  "confidence": 0.949
                },
                {
                  "text": "the",
                  "start": 83.06,
                  "end": 83.22,
                  "confidence": 0.997
                },
                {
                  "text": "thing",
                  "start": 83.22,
                  "end": 83.38,
                  "confidence": 0.999
                },
                {
                  "text": "when",
                  "start": 83.38,
                  "end": 83.54,
                  "confidence": 0.496
                },
                {
                  "text": "it",
                  "start": 83.54,
                  "end": 83.68,
                  "confidence": 0.998
                },
                {
                  "text": "comes",
                  "start": 83.68,
                  "end": 84.06,
                  "confidence": 0.998
                },
                {
                  "text": "to",
                  "start": 84.06,
                  "end": 84.26,
                  "confidence": 0.994
                },
                {
                  "text": "coffee",
                  "start": 84.26,
                  "end": 84.68,
                  "confidence": 0.87
                },
                {
                  "text": "in",
                  "start": 84.68,
                  "end": 84.94,
                  "confidence": 0.99
                },
                {
                  "text": "Columbia.",
                  "start": 84.94,
                  "end": 85.4,
                  "confidence": 0.952
                }
              ]
            },
            {
              "id": 34,
              "start": 85.52,
              "end": 91.9,
              "text": " They are the third largest producing and exporting coffee country in the world.",
              "no_speech_prob": 0.0978880524635315,
              "confidence": 0.962,
              "words": [
                {
                  "text": "They",
                  "start": 85.52,
                  "end": 85.68,
                  "confidence": 0.938
                },
                {
                  "text": "are",
                  "start": 85.68,
                  "end": 85.88,
                  "confidence": 0.991
                },
                {
                  "text": "the",
                  "start": 85.88,
                  "end": 86.06,
                  "confidence": 0.995
                },
                {
                  "text": "third",
                  "start": 86.06,
                  "end": 86.64,
                  "confidence": 0.973
                },
                {
                  "text": "largest",
                  "start": 86.64,
                  "end": 87.5,
                  "confidence": 0.98
                },
                {
                  "text": "producing",
                  "start": 87.5,
                  "end": 88.76,
                  "confidence": 0.832
                },
                {
                  "text": "and",
                  "start": 88.76,
                  "end": 89.34,
                  "confidence": 0.893
                },
                {
                  "text": "exporting",
                  "start": 89.34,
                  "end": 89.92,
                  "confidence": 0.972
                },
                {
                  "text": "coffee",
                  "start": 89.92,
                  "end": 90.5,
                  "confidence": 0.984
                },
                {
                  "text": "country",
                  "start": 90.5,
                  "end": 90.92,
                  "confidence": 0.985
                },
                {
                  "text": "in",
                  "start": 90.92,
                  "end": 91.16,
                  "confidence": 0.988
                },
                {
                  "text": "the",
                  "start": 91.16,
                  "end": 91.32,
                  "confidence": 0.994
                },
                {
                  "text": "world.",
                  "start": 91.32,
                  "end": 91.9,
                  "confidence": 0.993
                }
              ]
            },
            {
              "id": 35,
              "start": 92.22,
              "end": 99.26,
              "text": " The amount of coffee that is exported from Columbia equals about 810,000 metric tons.",
              "no_speech_prob": 0.0978880524635315,
              "confidence": 0.956,
              "words": [
                {
                  "text": "The",
                  "start": 92.22,
                  "end": 92.36,
                  "confidence": 0.998
                },
                {
                  "text": "amount",
                  "start": 92.36,
                  "end": 92.6,
                  "confidence": 1.0
                },
                {
                  "text": "of",
                  "start": 92.6,
                  "end": 92.76,
                  "confidence": 0.999
                },
                {
                  "text": "coffee",
                  "start": 92.76,
                  "end": 93.06,
                  "confidence": 0.997
                },
                {
                  "text": "that",
                  "start": 93.06,
                  "end": 93.2,
                  "confidence": 0.995
                },
                {
                  "text": "is",
                  "start": 93.2,
                  "end": 93.34,
                  "confidence": 0.979
                },
                {
                  "text": "exported",
                  "start": 93.34,
                  "end": 93.84,
                  "confidence": 0.987
                },
                {
                  "text": "from",
                  "start": 93.84,
                  "end": 94.16,
                  "confidence": 0.998
                },
                {
                  "text": "Columbia",
                  "start": 94.16,
                  "end": 94.66,
                  "confidence": 0.977
                },
                {
                  "text": "equals",
                  "start": 94.66,
                  "end": 95.18,
                  "confidence": 0.943
                },
                {
                  "text": "about",
                  "start": 95.18,
                  "end": 95.6,
                  "confidence": 0.986
                },
                {
                  "text": "810,000",
                  "start": 95.6,
                  "end": 98.14,
                  "confidence": 0.873
                },
                {
                  "text": "metric",
                  "start": 98.14,
                  "end": 98.68,
                  "confidence": 0.96
                },
                {
                  "text": "tons.",
                  "start": 98.68,
                  "end": 99.26,
                  "confidence": 0.962
                }
              ]
            },
            {
              "id": 36,
              "start": 99.84,
              "end": 102.93,
              "text": " Or approximately 11.5 million bags.",
              "no_speech_prob": 0.0978880524635315,
              "confidence": 0.981,
              "words": [
                {
                  "text": "Or",
                  "start": 99.84,
                  "end": 100.04,
                  "confidence": 0.984
                },
                {
                  "text": "approximately",
                  "start": 100.04,
                  "end": 100.66,
                  "confidence": 0.991
                },
                {
                  "text": "11.5",
                  "start": 100.66,
                  "end": 102.12,
                  "confidence": 0.98
                },
                {
                  "text": "million",
                  "start": 102.12,
                  "end": 102.52,
                  "confidence": 0.975
                },
                {
                  "text": "bags.",
                  "start": 102.52,
                  "end": 102.93,
                  "confidence": 0.974
                }
              ]
            },
            {
              "id": 37,
              "start": 102.93,
              "end": 108.64,
              "text": " However, although it might be beaten by countries like Brazil, it is actually the",
              "no_speech_prob": 0.0978880524635315,
              "confidence": 0.982,
              "words": [
                {
                  "text": "However,",
                  "start": 102.93,
                  "end": 103.62,
                  "confidence": 0.995
                },
                {
                  "text": "although",
                  "start": 103.82,
                  "end": 104.08,
                  "confidence": 0.984
                },
                {
                  "text": "it",
                  "start": 104.08,
                  "end": 104.38,
                  "confidence": 0.976
                },
                {
                  "text": "might",
                  "start": 104.38,
                  "end": 104.58,
                  "confidence": 0.993
                },
                {
                  "text": "be",
                  "start": 104.58,
                  "end": 104.8,
                  "confidence": 0.996
                },
                {
                  "text": "beaten",
                  "start": 104.8,
                  "end": 105.08,
                  "confidence": 0.944
                },
                {
                  "text": "by",
                  "start": 105.08,
                  "end": 105.36,
                  "confidence": 0.999
                },
                {
                  "text": "countries",
                  "start": 105.36,
                  "end": 105.96,
                  "confidence": 0.985
                },
                {
                  "text": "like",
                  "start": 105.96,
                  "end": 106.46,
                  "confidence": 0.996
                },
                {
                  "text": "Brazil,",
                  "start": 106.46,
                  "end": 107.3,
                  "confidence": 0.976
                },
                {
                  "text": "it",
                  "start": 107.52,
                  "end": 108.02,
                  "confidence": 0.99
                },
                {
                  "text": "is",
                  "start": 108.02,
                  "end": 108.14,
                  "confidence": 0.972
                },
                {
                  "text": "actually",
                  "start": 108.14,
                  "end": 108.44,
                  "confidence": 0.989
                },
                {
                  "text": "the",
                  "start": 108.44,
                  "end": 108.64,
                  "confidence": 0.952
                }
              ]
            },
            {
              "id": 38,
              "start": 108.64,
              "end": 114.36,
              "text": " number one or highest country for producing and growing a specific type of being known",
              "no_speech_prob": 0.0978880524635315,
              "confidence": 0.906,
              "words": [
                {
                  "text": "number",
                  "start": 108.64,
                  "end": 108.92,
                  "confidence": 0.848
                },
                {
                  "text": "one",
                  "start": 108.92,
                  "end": 109.16,
                  "confidence": 0.94
                },
                {
                  "text": "or",
                  "start": 109.16,
                  "end": 109.42,
                  "confidence": 0.843
                },
                {
                  "text": "highest",
                  "start": 109.42,
                  "end": 109.8,
                  "confidence": 0.989
                },
                {
                  "text": "country",
                  "start": 109.8,
                  "end": 110.2,
                  "confidence": 0.987
                },
                {
                  "text": "for",
                  "start": 110.2,
                  "end": 110.5,
                  "confidence": 0.995
                },
                {
                  "text": "producing",
                  "start": 110.5,
                  "end": 111.12,
                  "confidence": 0.996
                },
                {
                  "text": "and",
                  "start": 111.12,
                  "end": 111.36,
                  "confidence": 0.994
                },
                {
                  "text": "growing",
                  "start": 111.36,
                  "end": 111.68,
                  "confidence": 0.996
                },
                {
                  "text": "a",
                  "start": 111.68,
                  "end": 112.22,
                  "confidence": 0.926
                },
                {
                  "text": "specific",
                  "start": 112.22,
                  "end": 112.88,
                  "confidence": 0.997
                },
                {
                  "text": "type",
                  "start": 112.88,
                  "end": 113.24,
                  "confidence": 0.998
                },
                {
                  "text": "of",
                  "start": 113.24,
                  "end": 113.4,
                  "confidence": 0.998
                },
                {
                  "text": "being",
                  "start": 113.4,
                  "end": 114.0,
                  "confidence": 0.447
                },
                {
                  "text": "known",
                  "start": 114.0,
                  "end": 114.36,
                  "confidence": 0.853
                }
              ]
            },
            {
              "id": 39,
              "start": 114.38,
              "end": 116.3,
              "text": " as the Arabica being.",
              "no_speech_prob": 0.0728147029876709,
              "confidence": 0.73,
              "words": [
                {
                  "text": "as",
                  "start": 114.38,
                  "end": 114.68,
                  "confidence": 0.994
                },
                {
                  "text": "the",
                  "start": 114.68,
                  "end": 114.88,
                  "confidence": 0.976
                },
                {
                  "text": "Arabica",
                  "start": 114.88,
                  "end": 115.7,
                  "confidence": 0.542
                },
                {
                  "text": "being.",
                  "start": 115.7,
                  "end": 116.3,
                  "confidence": 0.727
                }
              ]
            },
            {
              "id": 40,
              "start": 116.66,
              "end": 120.26,
              "text": " And I know coffee is really important when it comes to talking about Columbia, but you",
              "no_speech_prob": 0.0728147029876709,
              "confidence": 0.973,
              "words": [
                {
                  "text": "And",
                  "start": 116.66,
                  "end": 116.8,
                  "confidence": 0.986
                },
                {
                  "text": "I",
                  "start": 116.8,
                  "end": 116.9,
                  "confidence": 0.994
                },
                {
                  "text": "know",
                  "start": 116.9,
                  "end": 117.06,
                  "confidence": 1.0
                },
                {
                  "text": "coffee",
                  "start": 117.06,
                  "end": 117.5,
                  "confidence": 0.931
                },
                {
                  "text": "is",
                  "start": 117.5,
                  "end": 117.8,
                  "confidence": 0.995
                },
                {
                  "text": "really",
                  "start": 117.8,
                  "end": 118.12,
                  "confidence": 0.998
                },
                {
                  "text": "important",
                  "start": 118.12,
                  "end": 118.7,
                  "confidence": 0.997
                },
                {
                  "text": "when",
                  "start": 118.7,
                  "end": 118.92,
                  "confidence": 0.987
                },
                {
                  "text": "it",
                  "start": 118.92,
                  "end": 119.0,
                  "confidence": 0.996
                },
                {
                  "text": "comes",
                  "start": 119.0,
                  "end": 119.22,
                  "confidence": 0.997
                },
                {
                  "text": "to",
                  "start": 119.22,
                  "end": 119.4,
                  "confidence": 0.995
                },
                {
                  "text": "talking",
                  "start": 119.4,
                  "end": 119.56,
                  "confidence": 0.903
                },
                {
                  "text": "about",
                  "start": 119.56,
                  "end": 119.7,
                  "confidence": 0.998
                },
                {
                  "text": "Columbia,",
                  "start": 119.7,
                  "end": 119.94,
                  "confidence": 0.973
                },
                {
                  "text": "but",
                  "start": 120.06,
                  "end": 120.16,
                  "confidence": 0.989
                },
                {
                  "text": "you",
                  "start": 120.16,
                  "end": 120.26,
                  "confidence": 0.845
                }
              ]
            },
            {
              "id": 41,
              "start": 120.26,
              "end": 122.64,
              "text": " really don't know how important it is with its culture.",
              "no_speech_prob": 0.0728147029876709,
              "confidence": 0.896,
              "words": [
                {
                  "text": "really",
                  "start": 120.26,
                  "end": 120.58,
                  "confidence": 0.355
                },
                {
                  "text": "don't",
                  "start": 120.58,
                  "end": 120.76,
                  "confidence": 0.998
                },
                {
                  "text": "know",
                  "start": 120.76,
                  "end": 120.94,
                  "confidence": 0.993
                },
                {
                  "text": "how",
                  "start": 120.94,
                  "end": 121.12,
                  "confidence": 0.994
                },
                {
                  "text": "important",
                  "start": 121.12,
                  "end": 121.6,
                  "confidence": 0.999
                },
                {
                  "text": "it",
                  "start": 121.6,
                  "end": 121.78,
                  "confidence": 0.986
                },
                {
                  "text": "is",
                  "start": 121.78,
                  "end": 121.92,
                  "confidence": 0.999
                },
                {
                  "text": "with",
                  "start": 121.92,
                  "end": 122.1,
                  "confidence": 0.985
                },
                {
                  "text": "its",
                  "start": 122.1,
                  "end": 122.26,
                  "confidence": 0.888
                },
                {
                  "text": "culture.",
                  "start": 122.26,
                  "end": 122.64,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 42,
              "start": 123.02,
              "end": 130.51,
              "text": " Interesting fact that in 2007, major spots, equaling a buffer zone of approximately 207,000",
              "no_speech_prob": 0.0728147029876709,
              "confidence": 0.855,
              "words": [
                {
                  "text": "Interesting",
                  "start": 123.02,
                  "end": 123.56,
                  "confidence": 0.832
                },
                {
                  "text": "fact",
                  "start": 123.56,
                  "end": 124.08,
                  "confidence": 0.995
                },
                {
                  "text": "that",
                  "start": 124.08,
                  "end": 124.34,
                  "confidence": 0.929
                },
                {
                  "text": "in",
                  "start": 124.34,
                  "end": 124.6,
                  "confidence": 0.968
                },
                {
                  "text": "2007,",
                  "start": 124.6,
                  "end": 125.58,
                  "confidence": 0.99
                },
                {
                  "text": "major",
                  "start": 125.74,
                  "end": 126.18,
                  "confidence": 0.955
                },
                {
                  "text": "spots,",
                  "start": 126.18,
                  "end": 126.7,
                  "confidence": 0.944
                },
                {
                  "text": "equaling",
                  "start": 126.72,
                  "end": 127.24,
                  "confidence": 0.613
                },
                {
                  "text": "a",
                  "start": 127.24,
                  "end": 127.38,
                  "confidence": 0.597
                },
                {
                  "text": "buffer",
                  "start": 127.38,
                  "end": 127.72,
                  "confidence": 0.737
                },
                {
                  "text": "zone",
                  "start": 127.72,
                  "end": 128.04,
                  "confidence": 0.992
                },
                {
                  "text": "of",
                  "start": 128.04,
                  "end": 128.24,
                  "confidence": 0.853
                },
                {
                  "text": "approximately",
                  "start": 128.24,
                  "end": 128.78,
                  "confidence": 0.995
                },
                {
                  "text": "207,000",
                  "start": 128.78,
                  "end": 130.51,
                  "confidence": 0.897
                }
              ]
            },
            {
              "id": 43,
              "start": 130.51,
              "end": 136.67,
              "text": " hectares, which are called the coffee cultural landscape, were considered a UNESCO World Heritage",
              "no_speech_prob": 0.0728147029876709,
              "confidence": 0.888,
              "words": [
                {
                  "text": "hectares,",
                  "start": 130.51,
                  "end": 131.2,
                  "confidence": 0.894
                },
                {
                  "text": "which",
                  "start": 131.7,
                  "end": 131.84,
                  "confidence": 0.994
                },
                {
                  "text": "are",
                  "start": 131.84,
                  "end": 132.12,
                  "confidence": 0.994
                },
                {
                  "text": "called",
                  "start": 132.12,
                  "end": 132.44,
                  "confidence": 0.998
                },
                {
                  "text": "the",
                  "start": 132.44,
                  "end": 132.68,
                  "confidence": 0.981
                },
                {
                  "text": "coffee",
                  "start": 132.68,
                  "end": 133.12,
                  "confidence": 0.816
                },
                {
                  "text": "cultural",
                  "start": 133.12,
                  "end": 133.58,
                  "confidence": 0.793
                },
                {
                  "text": "landscape,",
                  "start": 133.58,
                  "end": 134.16,
                  "confidence": 0.983
                },
                {
                  "text": "were",
                  "start": 134.28,
                  "end": 134.62,
                  "confidence": 0.894
                },
                {
                  "text": "considered",
                  "start": 134.62,
                  "end": 135.2,
                  "confidence": 0.993
                },
                {
                  "text": "a",
                  "start": 135.2,
                  "end": 135.42,
                  "confidence": 0.987
                },
                {
                  "text": "UNESCO",
                  "start": 135.42,
                  "end": 135.9,
                  "confidence": 0.946
                },
                {
                  "text": "World",
                  "start": 135.9,
                  "end": 136.18,
                  "confidence": 0.656
                },
                {
                  "text": "Heritage",
                  "start": 136.18,
                  "end": 136.67,
                  "confidence": 0.586
                }
              ]
            },
            {
              "id": 44,
              "start": 136.67,
              "end": 137.22,
              "text": " Site.",
              "no_speech_prob": 0.0728147029876709,
              "confidence": 0.696,
              "words": [
                {
                  "text": "Site.",
                  "start": 136.67,
                  "end": 137.22,
                  "confidence": 0.696
                }
              ]
            },
            {
              "id": 45,
              "start": 137.28,
              "end": 144.14,
              "text": " And also in 2007, the EU, the European Union, granted Colombian coffee, a protected designation",
              "no_speech_prob": 0.0728147029876709,
              "confidence": 0.902,
              "words": [
                {
                  "text": "And",
                  "start": 137.28,
                  "end": 137.76,
                  "confidence": 0.758
                },
                {
                  "text": "also",
                  "start": 137.76,
                  "end": 138.06,
                  "confidence": 0.998
                },
                {
                  "text": "in",
                  "start": 138.06,
                  "end": 138.28,
                  "confidence": 0.896
                },
                {
                  "text": "2007,",
                  "start": 138.28,
                  "end": 139.04,
                  "confidence": 0.994
                },
                {
                  "text": "the",
                  "start": 139.2,
                  "end": 139.38,
                  "confidence": 0.993
                },
                {
                  "text": "EU,",
                  "start": 139.38,
                  "end": 139.72,
                  "confidence": 0.923
                },
                {
                  "text": "the",
                  "start": 139.82,
                  "end": 139.96,
                  "confidence": 0.982
                },
                {
                  "text": "European",
                  "start": 139.96,
                  "end": 140.34,
                  "confidence": 0.997
                },
                {
                  "text": "Union,",
                  "start": 140.34,
                  "end": 140.7,
                  "confidence": 0.998
                },
                {
                  "text": "granted",
                  "start": 140.76,
                  "end": 141.24,
                  "confidence": 0.918
                },
                {
                  "text": "Colombian",
                  "start": 141.24,
                  "end": 141.88,
                  "confidence": 0.768
                },
                {
                  "text": "coffee,",
                  "start": 141.88,
                  "end": 142.3,
                  "confidence": 0.921
                },
                {
                  "text": "a",
                  "start": 142.38,
                  "end": 142.8,
                  "confidence": 0.956
                },
                {
                  "text": "protected",
                  "start": 142.8,
                  "end": 143.36,
                  "confidence": 0.978
                },
                {
                  "text": "designation",
                  "start": 143.36,
                  "end": 144.14,
                  "confidence": 0.689
                }
              ]
            },
            {
              "id": 46,
              "start": 144.34,
              "end": 145.62,
              "text": " of origin status.",
              "no_speech_prob": 0.0007917813491076231,
              "confidence": 0.903,
              "words": [
                {
                  "text": "of",
                  "start": 144.34,
                  "end": 144.54,
                  "confidence": 0.984
                },
                {
                  "text": "origin",
                  "start": 144.54,
                  "end": 145.02,
                  "confidence": 0.972
                },
                {
                  "text": "status.",
                  "start": 145.02,
                  "end": 145.62,
                  "confidence": 0.769
                }
              ]
            },
            {
              "id": 47,
              "start": 146.12,
              "end": 149.9,
              "text": " Now, interesting enough when it comes to the coffee in Columbia, believe it or not,",
              "no_speech_prob": 0.0007917813491076231,
              "confidence": 0.854,
              "words": [
                {
                  "text": "Now,",
                  "start": 146.12,
                  "end": 146.22,
                  "confidence": 0.879
                },
                {
                  "text": "interesting",
                  "start": 146.56,
                  "end": 146.62,
                  "confidence": 0.535
                },
                {
                  "text": "enough",
                  "start": 146.62,
                  "end": 146.96,
                  "confidence": 0.955
                },
                {
                  "text": "when",
                  "start": 146.96,
                  "end": 147.14,
                  "confidence": 0.563
                },
                {
                  "text": "it",
                  "start": 147.14,
                  "end": 147.24,
                  "confidence": 0.994
                },
                {
                  "text": "comes",
                  "start": 147.24,
                  "end": 147.46,
                  "confidence": 0.995
                },
                {
                  "text": "to",
                  "start": 147.46,
                  "end": 147.66,
                  "confidence": 0.992
                },
                {
                  "text": "the",
                  "start": 147.66,
                  "end": 147.82,
                  "confidence": 0.982
                },
                {
                  "text": "coffee",
                  "start": 147.82,
                  "end": 148.2,
                  "confidence": 0.966
                },
                {
                  "text": "in",
                  "start": 148.2,
                  "end": 148.5,
                  "confidence": 0.981
                },
                {
                  "text": "Columbia,",
                  "start": 148.5,
                  "end": 149.08,
                  "confidence": 0.576
                },
                {
                  "text": "believe",
                  "start": 149.34,
                  "end": 149.54,
                  "confidence": 0.78
                },
                {
                  "text": "it",
                  "start": 149.54,
                  "end": 149.7,
                  "confidence": 0.978
                },
                {
                  "text": "or",
                  "start": 149.7,
                  "end": 149.8,
                  "confidence": 0.996
                },
                {
                  "text": "not,",
                  "start": 149.8,
                  "end": 149.9,
                  "confidence": 0.932
                }
              ]
            },
            {
              "id": 48,
              "start": 149.9,
              "end": 153.1,
              "text": " it is not actually native to the country.",
              "no_speech_prob": 0.0007917813491076231,
              "confidence": 0.979,
              "words": [
                {
                  "text": "it",
                  "start": 149.9,
                  "end": 150.28,
                  "confidence": 0.991
                },
                {
                  "text": "is",
                  "start": 150.28,
                  "end": 150.42,
                  "confidence": 0.973
                },
                {
                  "text": "not",
                  "start": 150.42,
                  "end": 151.0,
                  "confidence": 0.92
                },
                {
                  "text": "actually",
                  "start": 151.0,
                  "end": 151.78,
                  "confidence": 0.974
                },
                {
                  "text": "native",
                  "start": 151.78,
                  "end": 152.3,
                  "confidence": 0.992
                },
                {
                  "text": "to",
                  "start": 152.3,
                  "end": 152.54,
                  "confidence": 0.995
                },
                {
                  "text": "the",
                  "start": 152.54,
                  "end": 152.74,
                  "confidence": 0.992
                },
                {
                  "text": "country.",
                  "start": 152.74,
                  "end": 153.1,
                  "confidence": 0.998
                }
              ]
            },
            {
              "id": 49,
              "start": 153.54,
              "end": 157.88,
              "text": " It's come from somewhere else, not really an invasive species because it's very much",
              "no_speech_prob": 0.0007917813491076231,
              "confidence": 0.929,
              "words": [
                {
                  "text": "It's",
                  "start": 153.54,
                  "end": 153.78,
                  "confidence": 0.913
                },
                {
                  "text": "come",
                  "start": 153.78,
                  "end": 153.98,
                  "confidence": 0.911
                },
                {
                  "text": "from",
                  "start": 153.98,
                  "end": 154.12,
                  "confidence": 0.997
                },
                {
                  "text": "somewhere",
                  "start": 154.12,
                  "end": 154.52,
                  "confidence": 0.991
                },
                {
                  "text": "else,",
                  "start": 154.52,
                  "end": 155.02,
                  "confidence": 1.0
                },
                {
                  "text": "not",
                  "start": 155.32,
                  "end": 155.44,
                  "confidence": 0.988
                },
                {
                  "text": "really",
                  "start": 155.44,
                  "end": 155.66,
                  "confidence": 0.969
                },
                {
                  "text": "an",
                  "start": 155.66,
                  "end": 155.78,
                  "confidence": 0.845
                },
                {
                  "text": "invasive",
                  "start": 155.78,
                  "end": 156.22,
                  "confidence": 0.994
                },
                {
                  "text": "species",
                  "start": 156.22,
                  "end": 156.74,
                  "confidence": 0.976
                },
                {
                  "text": "because",
                  "start": 156.74,
                  "end": 157.08,
                  "confidence": 0.642
                },
                {
                  "text": "it's",
                  "start": 157.08,
                  "end": 157.38,
                  "confidence": 0.97
                },
                {
                  "text": "very",
                  "start": 157.38,
                  "end": 157.72,
                  "confidence": 0.993
                },
                {
                  "text": "much",
                  "start": 157.72,
                  "end": 157.88,
                  "confidence": 0.869
                }
              ]
            },
            {
              "id": 50,
              "start": 157.88,
              "end": 158.42,
              "text": " welcomed.",
              "no_speech_prob": 0.0007917813491076231,
              "confidence": 0.962,
              "words": [
                {
                  "text": "welcomed.",
                  "start": 157.88,
                  "end": 158.42,
                  "confidence": 0.962
                }
              ]
            },
            {
              "id": 51,
              "start": 158.82,
              "end": 162.81,
              "text": " Now you may have also seen this guy on many different Colombian coffee brands.",
              "no_speech_prob": 0.0007917813491076231,
              "confidence": 0.966,
              "words": [
                {
                  "text": "Now",
                  "start": 158.82,
                  "end": 158.98,
                  "confidence": 0.991
                },
                {
                  "text": "you",
                  "start": 158.98,
                  "end": 159.12,
                  "confidence": 0.924
                },
                {
                  "text": "may",
                  "start": 159.12,
                  "end": 159.28,
                  "confidence": 0.994
                },
                {
                  "text": "have",
                  "start": 159.28,
                  "end": 159.42,
                  "confidence": 0.962
                },
                {
                  "text": "also",
                  "start": 159.42,
                  "end": 159.76,
                  "confidence": 0.985
                },
                {
                  "text": "seen",
                  "start": 159.76,
                  "end": 160.12,
                  "confidence": 0.996
                },
                {
                  "text": "this",
                  "start": 160.12,
                  "end": 160.36,
                  "confidence": 0.988
                },
                {
                  "text": "guy",
                  "start": 160.36,
                  "end": 160.7,
                  "confidence": 0.993
                },
                {
                  "text": "on",
                  "start": 160.7,
                  "end": 160.94,
                  "confidence": 0.974
                },
                {
                  "text": "many",
                  "start": 160.94,
                  "end": 161.12,
                  "confidence": 0.994
                },
                {
                  "text": "different",
                  "start": 161.12,
                  "end": 161.34,
                  "confidence": 0.981
                },
                {
                  "text": "Colombian",
                  "start": 161.34,
                  "end": 162.0,
                  "confidence": 0.908
                },
                {
                  "text": "coffee",
                  "start": 162.0,
                  "end": 162.42,
                  "confidence": 0.911
                },
                {
                  "text": "brands.",
                  "start": 162.42,
                  "end": 162.81,
                  "confidence": 0.987
                }
              ]
            },
            {
              "id": 52,
              "start": 162.81,
              "end": 164.54,
              "text": " Now his name is Juan Valdez.",
              "no_speech_prob": 0.0007917813491076231,
              "confidence": 0.885,
              "words": [
                {
                  "text": "Now",
                  "start": 162.81,
                  "end": 163.04,
                  "confidence": 0.967
                },
                {
                  "text": "his",
                  "start": 163.04,
                  "end": 163.24,
                  "confidence": 0.842
                },
                {
                  "text": "name",
                  "start": 163.24,
                  "end": 163.48,
                  "confidence": 0.999
                },
                {
                  "text": "is",
                  "start": 163.48,
                  "end": 163.72,
                  "confidence": 0.995
                },
                {
                  "text": "Juan",
                  "start": 163.72,
                  "end": 164.0,
                  "confidence": 0.757
                },
                {
                  "text": "Valdez.",
                  "start": 164.0,
                  "end": 164.54,
                  "confidence": 0.852
                }
              ]
            },
            {
              "id": 53,
              "start": 164.54,
              "end": 169.66,
              "text": " Now some people think that this guy is actually really a real coffee farmer, somebody just",
              "no_speech_prob": 0.0007917813491076231,
              "confidence": 0.837,
              "words": [
                {
                  "text": "Now",
                  "start": 164.54,
                  "end": 164.92,
                  "confidence": 0.983
                },
                {
                  "text": "some",
                  "start": 164.92,
                  "end": 165.06,
                  "confidence": 0.964
                },
                {
                  "text": "people",
                  "start": 165.06,
                  "end": 165.24,
                  "confidence": 0.997
                },
                {
                  "text": "think",
                  "start": 165.24,
                  "end": 165.6,
                  "confidence": 0.996
                },
                {
                  "text": "that",
                  "start": 165.6,
                  "end": 165.76,
                  "confidence": 0.876
                },
                {
                  "text": "this",
                  "start": 165.76,
                  "end": 165.98,
                  "confidence": 0.987
                },
                {
                  "text": "guy",
                  "start": 165.98,
                  "end": 166.26,
                  "confidence": 0.996
                },
                {
                  "text": "is",
                  "start": 166.26,
                  "end": 166.4,
                  "confidence": 0.947
                },
                {
                  "text": "actually",
                  "start": 166.4,
                  "end": 166.86,
                  "confidence": 0.92
                },
                {
                  "text": "really",
                  "start": 166.86,
                  "end": 167.4,
                  "confidence": 0.852
                },
                {
                  "text": "a",
                  "start": 167.4,
                  "end": 167.62,
                  "confidence": 0.391
                },
                {
                  "text": "real",
                  "start": 167.62,
                  "end": 167.94,
                  "confidence": 0.971
                },
                {
                  "text": "coffee",
                  "start": 167.94,
                  "end": 168.48,
                  "confidence": 0.978
                },
                {
                  "text": "farmer,",
                  "start": 168.48,
                  "end": 169.02,
                  "confidence": 0.99
                },
                {
                  "text": "somebody",
                  "start": 169.24,
                  "end": 169.46,
                  "confidence": 0.658
                },
                {
                  "text": "just",
                  "start": 169.46,
                  "end": 169.66,
                  "confidence": 0.394
                }
              ]
            }
          ]
        }
      ],
      "process_output_files": [
        "../../../data/output/031af2e4-23ee-4f66-969e-6a02c91c10cd.json"
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
        "transcript": " This episode, looking at the great country of Columbia, we looked at some really basic facts. It's name, a bit of its history, the type of people that live there, land size, and all that jazz. But in this video, we're going to go into a little bit more of a detailed look. Yo, what is going on guys? Welcome back to F2D facts. The channel where I look at people cultures and places, my name is Dave Wouple, and today we are going to be looking more at Columbia in our Columbia Part 2 video. Which just reminds me guys, this is part of our Columbia playlist. So put it down in the description box below and I'll talk about that more at the end of the video. But if you're new here, join me every single Monday to learn about new countries from around the world. You can do that by hitting that subscribe and that belt notification button. But let's get started. So we all know, Columbia is famous for its coffee, right? Yes, right. I know. You guys are sitting there going, five bucks says he's going to talk about coffee. Well, I am. That's right, because I got my van, you Columbia coffee. Right here. Boom advertisement. Yeah. Pain me for this. I'm care. So which might not know about coffee is yes, you probably already know that a lot of companies actually buy it up. Starbucks buys all had a coffee from Columbia. It's kind of like their favorite place to buy coffee. And kind of to pay tribute to that Starbucks when they were making their 1,000th store in 2016, they decided, yo, we're going to put it in Columbia. And this was in the town of Medellin, Columbia. Now here's the thing when it comes to coffee in Columbia. They are the third largest producing and exporting coffee country in the world. The amount of coffee that is exported from Columbia equals about 810,000 metric tons. Or approximately 11.5 million bags. However, although it might be beaten by countries like Brazil, it is actually the number one or highest country for producing and growing a specific type of being known as the Arabica being. And I know coffee is really important when it comes to talking about Columbia, but you really don't know how important it is with its culture. Interesting fact that in 2007, major spots, equaling a buffer zone of approximately 207,000 hectares, which are called the coffee cultural landscape, were considered a UNESCO World Heritage Site. And also in 2007, the EU, the European Union, granted Colombian coffee, a protected designation of origin status. Now, interesting enough when it comes to the coffee in Columbia, believe it or not, it is not actually native to the country. It's come from somewhere else, not really an invasive species because it's very much welcomed. Now you may have also seen this guy on many different Colombian coffee brands. Now his name is Juan Valdez. Now some people think that this guy is actually really a real coffee farmer, somebody just",
        "timestamped_transcript": [
          {
            "id": 0,
            "start": 0.0,
            "end": 4.25,
            "text": " This episode, looking at the great country of Columbia, we looked at some really basic facts.",
            "no_speech_prob": 0.5648887157440186,
            "confidence": 0.758,
            "words": [
              {
                "text": "This",
                "start": 0.0,
                "end": 0.1,
                "confidence": 0.148
              },
              {
                "text": "episode,",
                "start": 0.1,
                "end": 0.44,
                "confidence": 0.69
              },
              {
                "text": "looking",
                "start": 0.54,
                "end": 0.8,
                "confidence": 0.835
              },
              {
                "text": "at",
                "start": 0.8,
                "end": 1.0,
                "confidence": 0.994
              },
              {
                "text": "the",
                "start": 1.0,
                "end": 1.1,
                "confidence": 0.964
              },
              {
                "text": "great",
                "start": 1.1,
                "end": 1.3,
                "confidence": 0.97
              },
              {
                "text": "country",
                "start": 1.3,
                "end": 1.66,
                "confidence": 0.983
              },
              {
                "text": "of",
                "start": 1.66,
                "end": 1.78,
                "confidence": 0.982
              },
              {
                "text": "Columbia,",
                "start": 1.78,
                "end": 2.12,
                "confidence": 0.638
              },
              {
                "text": "we",
                "start": 2.2,
                "end": 2.32,
                "confidence": 0.584
              },
              {
                "text": "looked",
                "start": 2.32,
                "end": 2.6,
                "confidence": 0.962
              },
              {
                "text": "at",
                "start": 2.6,
                "end": 2.72,
                "confidence": 0.992
              },
              {
                "text": "some",
                "start": 2.72,
                "end": 3.0,
                "confidence": 0.982
              },
              {
                "text": "really",
                "start": 3.0,
                "end": 3.28,
                "confidence": 0.931
              },
              {
                "text": "basic",
                "start": 3.28,
                "end": 3.88,
                "confidence": 0.603
              },
              {
                "text": "facts.",
                "start": 3.88,
                "end": 4.25,
                "confidence": 0.796
              }
            ]
          },
          {
            "id": 1,
            "start": 4.25,
            "end": 8.68,
            "text": " It's name, a bit of its history, the type of people that live there, land size, and all",
            "no_speech_prob": 0.5648887157440186,
            "confidence": 0.885,
            "words": [
              {
                "text": "It's",
                "start": 4.25,
                "end": 4.58,
                "confidence": 0.858
              },
              {
                "text": "name,",
                "start": 4.58,
                "end": 4.94,
                "confidence": 0.899
              },
              {
                "text": "a",
                "start": 4.98,
                "end": 5.08,
                "confidence": 0.983
              },
              {
                "text": "bit",
                "start": 5.08,
                "end": 5.2,
                "confidence": 0.995
              },
              {
                "text": "of",
                "start": 5.2,
                "end": 5.32,
                "confidence": 0.995
              },
              {
                "text": "its",
                "start": 5.32,
                "end": 5.48,
                "confidence": 0.853
              },
              {
                "text": "history,",
                "start": 5.48,
                "end": 5.9,
                "confidence": 0.998
              },
              {
                "text": "the",
                "start": 6.04,
                "end": 6.38,
                "confidence": 0.9
              },
              {
                "text": "type",
                "start": 6.38,
                "end": 6.52,
                "confidence": 0.966
              },
              {
                "text": "of",
                "start": 6.52,
                "end": 6.62,
                "confidence": 0.994
              },
              {
                "text": "people",
                "start": 6.62,
                "end": 6.8,
                "confidence": 0.998
              },
              {
                "text": "that",
                "start": 6.8,
                "end": 6.96,
                "confidence": 0.983
              },
              {
                "text": "live",
                "start": 6.96,
                "end": 7.22,
                "confidence": 0.632
              },
              {
                "text": "there,",
                "start": 7.22,
                "end": 7.46,
                "confidence": 0.863
              },
              {
                "text": "land",
                "start": 7.54,
                "end": 7.86,
                "confidence": 0.69
              },
              {
                "text": "size,",
                "start": 7.86,
                "end": 8.28,
                "confidence": 0.771
              },
              {
                "text": "and",
                "start": 8.42,
                "end": 8.48,
                "confidence": 0.988
              },
              {
                "text": "all",
                "start": 8.48,
                "end": 8.68,
                "confidence": 0.728
              }
            ]
          },
          {
            "id": 2,
            "start": 8.68,
            "end": 9.22,
            "text": " that jazz.",
            "no_speech_prob": 0.5648887157440186,
            "confidence": 0.986,
            "words": [
              {
                "text": "that",
                "start": 8.68,
                "end": 8.92,
                "confidence": 0.984
              },
              {
                "text": "jazz.",
                "start": 8.92,
                "end": 9.22,
                "confidence": 0.988
              }
            ]
          },
          {
            "id": 3,
            "start": 9.52,
            "end": 12.56,
            "text": " But in this video, we're going to go into a little bit more of a detailed look.",
            "no_speech_prob": 0.5648887157440186,
            "confidence": 0.968,
            "words": [
              {
                "text": "But",
                "start": 9.52,
                "end": 9.64,
                "confidence": 0.932
              },
              {
                "text": "in",
                "start": 9.64,
                "end": 9.72,
                "confidence": 0.986
              },
              {
                "text": "this",
                "start": 9.72,
                "end": 9.86,
                "confidence": 0.998
              },
              {
                "text": "video,",
                "start": 9.86,
                "end": 10.08,
                "confidence": 0.996
              },
              {
                "text": "we're",
                "start": 10.14,
                "end": 10.22,
                "confidence": 0.977
              },
              {
                "text": "going",
                "start": 10.22,
                "end": 10.34,
                "confidence": 0.739
              },
              {
                "text": "to",
                "start": 10.34,
                "end": 10.4,
                "confidence": 0.988
              },
              {
                "text": "go",
                "start": 10.4,
                "end": 10.48,
                "confidence": 0.969
              },
              {
                "text": "into",
                "start": 10.48,
                "end": 10.72,
                "confidence": 0.994
              },
              {
                "text": "a",
                "start": 10.72,
                "end": 10.9,
                "confidence": 0.992
              },
              {
                "text": "little",
                "start": 10.9,
                "end": 11.12,
                "confidence": 0.992
              },
              {
                "text": "bit",
                "start": 11.12,
                "end": 11.26,
                "confidence": 0.944
              },
              {
                "text": "more",
                "start": 11.26,
                "end": 11.56,
                "confidence": 0.996
              },
              {
                "text": "of",
                "start": 11.56,
                "end": 11.76,
                "confidence": 0.994
              },
              {
                "text": "a",
                "start": 11.76,
                "end": 11.88,
                "confidence": 0.996
              },
              {
                "text": "detailed",
                "start": 11.88,
                "end": 12.2,
                "confidence": 0.997
              },
              {
                "text": "look.",
                "start": 12.2,
                "end": 12.56,
                "confidence": 0.996
              }
            ]
          },
          {
            "id": 4,
            "start": 12.82,
            "end": 14.26,
            "text": " Yo, what is going on guys?",
            "no_speech_prob": 0.5648887157440186,
            "confidence": 0.887,
            "words": [
              {
                "text": "Yo,",
                "start": 12.82,
                "end": 13.04,
                "confidence": 0.748
              },
              {
                "text": "what",
                "start": 13.1,
                "end": 13.34,
                "confidence": 0.992
              },
              {
                "text": "is",
                "start": 13.34,
                "end": 13.48,
                "confidence": 0.969
              },
              {
                "text": "going",
                "start": 13.48,
                "end": 13.68,
                "confidence": 0.986
              },
              {
                "text": "on",
                "start": 13.68,
                "end": 13.9,
                "confidence": 1.0
              },
              {
                "text": "guys?",
                "start": 13.9,
                "end": 14.26,
                "confidence": 0.689
              }
            ]
          },
          {
            "id": 5,
            "start": 14.32,
            "end": 15.6,
            "text": " Welcome back to F2D facts.",
            "no_speech_prob": 0.5648887157440186,
            "confidence": 0.735,
            "words": [
              {
                "text": "Welcome",
                "start": 14.32,
                "end": 14.58,
                "confidence": 0.988
              },
              {
                "text": "back",
                "start": 14.58,
                "end": 14.8,
                "confidence": 0.999
              },
              {
                "text": "to",
                "start": 14.8,
                "end": 14.98,
                "confidence": 0.986
              },
              {
                "text": "F2D",
                "start": 14.98,
                "end": 15.4,
                "confidence": 0.641
              },
              {
                "text": "facts.",
                "start": 15.4,
                "end": 15.6,
                "confidence": 0.453
              }
            ]
          },
          {
            "id": 6,
            "start": 15.6,
            "end": 21.6,
            "text": " The channel where I look at people cultures and places, my name is Dave Wouple, and today we",
            "no_speech_prob": 0.5648887157440186,
            "confidence": 0.772,
            "words": [
              {
                "text": "The",
                "start": 15.6,
                "end": 15.86,
                "confidence": 0.622
              },
              {
                "text": "channel",
                "start": 15.86,
                "end": 16.0,
                "confidence": 0.89
              },
              {
                "text": "where",
                "start": 16.0,
                "end": 16.16,
                "confidence": 0.989
              },
              {
                "text": "I",
                "start": 16.16,
                "end": 16.24,
                "confidence": 0.989
              },
              {
                "text": "look",
                "start": 16.24,
                "end": 16.36,
                "confidence": 0.994
              },
              {
                "text": "at",
                "start": 16.36,
                "end": 16.46,
                "confidence": 0.994
              },
              {
                "text": "people",
                "start": 16.46,
                "end": 16.64,
                "confidence": 0.932
              },
              {
                "text": "cultures",
                "start": 16.64,
                "end": 16.96,
                "confidence": 0.513
              },
              {
                "text": "and",
                "start": 16.96,
                "end": 17.14,
                "confidence": 0.91
              },
              {
                "text": "places,",
                "start": 17.14,
                "end": 17.5,
                "confidence": 0.995
              },
              {
                "text": "my",
                "start": 17.58,
                "end": 17.84,
                "confidence": 0.96
              },
              {
                "text": "name",
                "start": 17.84,
                "end": 18.62,
                "confidence": 0.999
              },
              {
                "text": "is",
                "start": 18.62,
                "end": 18.98,
                "confidence": 0.957
              },
              {
                "text": "Dave",
                "start": 18.98,
                "end": 19.38,
                "confidence": 0.98
              },
              {
                "text": "Wouple,",
                "start": 19.38,
                "end": 19.98,
                "confidence": 0.381
              },
              {
                "text": "and",
                "start": 20.18,
                "end": 20.4,
                "confidence": 0.991
              },
              {
                "text": "today",
                "start": 20.4,
                "end": 21.06,
                "confidence": 0.969
              },
              {
                "text": "we",
                "start": 21.06,
                "end": 21.6,
                "confidence": 0.51
              }
            ]
          },
          {
            "id": 7,
            "start": 21.6,
            "end": 25.24,
            "text": " are going to be looking more at Columbia in our Columbia Part 2 video.",
            "no_speech_prob": 0.5648887157440186,
            "confidence": 0.883,
            "words": [
              {
                "text": "are",
                "start": 21.6,
                "end": 22.08,
                "confidence": 0.994
              },
              {
                "text": "going",
                "start": 22.08,
                "end": 22.2,
                "confidence": 0.888
              },
              {
                "text": "to",
                "start": 22.2,
                "end": 22.24,
                "confidence": 0.991
              },
              {
                "text": "be",
                "start": 22.24,
                "end": 22.38,
                "confidence": 0.995
              },
              {
                "text": "looking",
                "start": 22.38,
                "end": 22.6,
                "confidence": 0.997
              },
              {
                "text": "more",
                "start": 22.6,
                "end": 22.96,
                "confidence": 0.92
              },
              {
                "text": "at",
                "start": 22.96,
                "end": 23.22,
                "confidence": 0.997
              },
              {
                "text": "Columbia",
                "start": 23.22,
                "end": 23.64,
                "confidence": 0.981
              },
              {
                "text": "in",
                "start": 23.64,
                "end": 23.86,
                "confidence": 0.529
              },
              {
                "text": "our",
                "start": 23.86,
                "end": 24.02,
                "confidence": 0.941
              },
              {
                "text": "Columbia",
                "start": 24.02,
                "end": 24.28,
                "confidence": 0.975
              },
              {
                "text": "Part",
                "start": 24.28,
                "end": 24.52,
                "confidence": 0.702
              },
              {
                "text": "2",
                "start": 24.52,
                "end": 24.84,
                "confidence": 0.691
              },
              {
                "text": "video.",
                "start": 24.84,
                "end": 25.24,
                "confidence": 0.957
              }
            ]
          },
          {
            "id": 8,
            "start": 25.72,
            "end": 28.8,
            "text": " Which just reminds me guys, this is part of our Columbia playlist.",
            "no_speech_prob": 0.5648887157440186,
            "confidence": 0.935,
            "words": [
              {
                "text": "Which",
                "start": 25.72,
                "end": 26.02,
                "confidence": 0.892
              },
              {
                "text": "just",
                "start": 26.02,
                "end": 26.24,
                "confidence": 0.981
              },
              {
                "text": "reminds",
                "start": 26.24,
                "end": 26.66,
                "confidence": 0.995
              },
              {
                "text": "me",
                "start": 26.66,
                "end": 26.88,
                "confidence": 0.907
              },
              {
                "text": "guys,",
                "start": 26.88,
                "end": 27.02,
                "confidence": 0.859
              },
              {
                "text": "this",
                "start": 27.12,
                "end": 27.24,
                "confidence": 0.984
              },
              {
                "text": "is",
                "start": 27.24,
                "end": 27.32,
                "confidence": 0.972
              },
              {
                "text": "part",
                "start": 27.32,
                "end": 27.54,
                "confidence": 0.97
              },
              {
                "text": "of",
                "start": 27.54,
                "end": 27.66,
                "confidence": 0.999
              },
              {
                "text": "our",
                "start": 27.66,
                "end": 27.84,
                "confidence": 0.992
              },
              {
                "text": "Columbia",
                "start": 27.84,
                "end": 28.24,
                "confidence": 0.995
              },
              {
                "text": "playlist.",
                "start": 28.24,
                "end": 28.8,
                "confidence": 0.716
              }
            ]
          },
          {
            "id": 9,
            "start": 28.92,
            "end": 31.58,
            "text": " So put it down in the description box below and I'll talk about that more at the end",
            "no_speech_prob": 0.3092843294143677,
            "confidence": 0.799,
            "words": [
              {
                "text": "So",
                "start": 28.92,
                "end": 28.98,
                "confidence": 0.376
              },
              {
                "text": "put",
                "start": 28.98,
                "end": 29.06,
                "confidence": 0.558
              },
              {
                "text": "it",
                "start": 29.06,
                "end": 29.18,
                "confidence": 0.988
              },
              {
                "text": "down",
                "start": 29.18,
                "end": 29.38,
                "confidence": 0.991
              },
              {
                "text": "in",
                "start": 29.38,
                "end": 29.52,
                "confidence": 0.602
              },
              {
                "text": "the",
                "start": 29.52,
                "end": 29.6,
                "confidence": 0.889
              },
              {
                "text": "description",
                "start": 29.6,
                "end": 29.84,
                "confidence": 0.998
              },
              {
                "text": "box",
                "start": 29.84,
                "end": 30.12,
                "confidence": 0.969
              },
              {
                "text": "below",
                "start": 30.12,
                "end": 30.36,
                "confidence": 0.99
              },
              {
                "text": "and",
                "start": 30.36,
                "end": 30.52,
                "confidence": 0.489
              },
              {
                "text": "I'll",
                "start": 30.52,
                "end": 30.64,
                "confidence": 0.932
              },
              {
                "text": "talk",
                "start": 30.64,
                "end": 30.8,
                "confidence": 0.976
              },
              {
                "text": "about",
                "start": 30.8,
                "end": 30.96,
                "confidence": 0.963
              },
              {
                "text": "that",
                "start": 30.96,
                "end": 31.06,
                "confidence": 0.816
              },
              {
                "text": "more",
                "start": 31.06,
                "end": 31.28,
                "confidence": 0.946
              },
              {
                "text": "at",
                "start": 31.28,
                "end": 31.52,
                "confidence": 0.501
              },
              {
                "text": "the",
                "start": 31.52,
                "end": 31.54,
                "confidence": 0.932
              },
              {
                "text": "end",
                "start": 31.54,
                "end": 31.58,
                "confidence": 0.939
              }
            ]
          },
          {
            "id": 10,
            "start": 31.58,
            "end": 32.36,
            "text": " of the video.",
            "no_speech_prob": 0.3092843294143677,
            "confidence": 0.984,
            "words": [
              {
                "text": "of",
                "start": 31.58,
                "end": 31.82,
                "confidence": 0.973
              },
              {
                "text": "the",
                "start": 31.82,
                "end": 31.94,
                "confidence": 0.983
              },
              {
                "text": "video.",
                "start": 31.94,
                "end": 32.36,
                "confidence": 0.996
              }
            ]
          },
          {
            "id": 11,
            "start": 32.72,
            "end": 35.95,
            "text": " But if you're new here, join me every single Monday to learn about new countries from",
            "no_speech_prob": 0.3092843294143677,
            "confidence": 0.976,
            "words": [
              {
                "text": "But",
                "start": 32.72,
                "end": 32.84,
                "confidence": 0.98
              },
              {
                "text": "if",
                "start": 32.84,
                "end": 32.94,
                "confidence": 0.981
              },
              {
                "text": "you're",
                "start": 32.94,
                "end": 33.1,
                "confidence": 0.973
              },
              {
                "text": "new",
                "start": 33.1,
                "end": 33.22,
                "confidence": 0.994
              },
              {
                "text": "here,",
                "start": 33.22,
                "end": 33.46,
                "confidence": 0.994
              },
              {
                "text": "join",
                "start": 33.64,
                "end": 33.92,
                "confidence": 0.978
              },
              {
                "text": "me",
                "start": 33.92,
                "end": 34.06,
                "confidence": 0.999
              },
              {
                "text": "every",
                "start": 34.06,
                "end": 34.24,
                "confidence": 0.862
              },
              {
                "text": "single",
                "start": 34.24,
                "end": 34.44,
                "confidence": 0.999
              },
              {
                "text": "Monday",
                "start": 34.44,
                "end": 34.7,
                "confidence": 0.971
              },
              {
                "text": "to",
                "start": 34.7,
                "end": 34.82,
                "confidence": 0.979
              },
              {
                "text": "learn",
                "start": 34.82,
                "end": 35.0,
                "confidence": 0.996
              },
              {
                "text": "about",
                "start": 35.0,
                "end": 35.18,
                "confidence": 0.997
              },
              {
                "text": "new",
                "start": 35.18,
                "end": 35.38,
                "confidence": 0.992
              },
              {
                "text": "countries",
                "start": 35.38,
                "end": 35.78,
                "confidence": 0.984
              },
              {
                "text": "from",
                "start": 35.78,
                "end": 35.95,
                "confidence": 0.956
              }
            ]
          },
          {
            "id": 12,
            "start": 35.95,
            "end": 36.48,
            "text": " around the world.",
            "no_speech_prob": 0.3092843294143677,
            "confidence": 0.988,
            "words": [
              {
                "text": "around",
                "start": 35.95,
                "end": 36.22,
                "confidence": 0.991
              },
              {
                "text": "the",
                "start": 36.22,
                "end": 36.34,
                "confidence": 0.973
              },
              {
                "text": "world.",
                "start": 36.34,
                "end": 36.48,
                "confidence": 0.998
              }
            ]
          },
          {
            "id": 13,
            "start": 36.48,
            "end": 39.32,
            "text": " You can do that by hitting that subscribe and that belt notification button.",
            "no_speech_prob": 0.3092843294143677,
            "confidence": 0.913,
            "words": [
              {
                "text": "You",
                "start": 36.48,
                "end": 36.58,
                "confidence": 0.972
              },
              {
                "text": "can",
                "start": 36.58,
                "end": 36.72,
                "confidence": 0.994
              },
              {
                "text": "do",
                "start": 36.72,
                "end": 36.82,
                "confidence": 0.996
              },
              {
                "text": "that",
                "start": 36.82,
                "end": 36.98,
                "confidence": 0.997
              },
              {
                "text": "by",
                "start": 36.98,
                "end": 37.16,
                "confidence": 0.952
              },
              {
                "text": "hitting",
                "start": 37.16,
                "end": 37.36,
                "confidence": 0.913
              },
              {
                "text": "that",
                "start": 37.36,
                "end": 37.48,
                "confidence": 0.993
              },
              {
                "text": "subscribe",
                "start": 37.48,
                "end": 37.92,
                "confidence": 0.965
              },
              {
                "text": "and",
                "start": 37.92,
                "end": 38.12,
                "confidence": 0.678
              },
              {
                "text": "that",
                "start": 38.12,
                "end": 38.32,
                "confidence": 0.967
              },
              {
                "text": "belt",
                "start": 38.32,
                "end": 38.46,
                "confidence": 0.623
              },
              {
                "text": "notification",
                "start": 38.46,
                "end": 39.04,
                "confidence": 0.943
              },
              {
                "text": "button.",
                "start": 39.04,
                "end": 39.32,
                "confidence": 0.998
              }
            ]
          },
          {
            "id": 14,
            "start": 39.32,
            "end": 41.56,
            "text": " But let's get started.",
            "no_speech_prob": 0.3092843294143677,
            "confidence": 0.838,
            "words": [
              {
                "text": "But",
                "start": 39.32,
                "end": 40.38,
                "confidence": 0.982
              },
              {
                "text": "let's",
                "start": 40.38,
                "end": 41.02,
                "confidence": 0.654
              },
              {
                "text": "get",
                "start": 41.02,
                "end": 41.18,
                "confidence": 0.984
              },
              {
                "text": "started.",
                "start": 41.18,
                "end": 41.56,
                "confidence": 0.998
              }
            ]
          },
          {
            "id": 15,
            "start": 41.56,
            "end": 46.6,
            "text": " So we all know, Columbia is famous for its coffee, right?",
            "no_speech_prob": 0.3092843294143677,
            "confidence": 0.839,
            "words": [
              {
                "text": "So",
                "start": 41.56,
                "end": 42.9,
                "confidence": 0.234
              },
              {
                "text": "we",
                "start": 42.9,
                "end": 43.52,
                "confidence": 0.861
              },
              {
                "text": "all",
                "start": 43.52,
                "end": 43.66,
                "confidence": 0.999
              },
              {
                "text": "know,",
                "start": 43.66,
                "end": 43.92,
                "confidence": 0.999
              },
              {
                "text": "Columbia",
                "start": 44.06,
                "end": 44.54,
                "confidence": 0.99
              },
              {
                "text": "is",
                "start": 44.54,
                "end": 44.86,
                "confidence": 0.988
              },
              {
                "text": "famous",
                "start": 44.86,
                "end": 45.24,
                "confidence": 0.994
              },
              {
                "text": "for",
                "start": 45.24,
                "end": 45.56,
                "confidence": 0.999
              },
              {
                "text": "its",
                "start": 45.56,
                "end": 45.8,
                "confidence": 0.854
              },
              {
                "text": "coffee,",
                "start": 45.8,
                "end": 46.24,
                "confidence": 0.877
              },
              {
                "text": "right?",
                "start": 46.34,
                "end": 46.6,
                "confidence": 0.996
              }
            ]
          },
          {
            "id": 16,
            "start": 46.84,
            "end": 47.37,
            "text": " Yes, right.",
            "no_speech_prob": 0.3092843294143677,
            "confidence": 0.971,
            "words": [
              {
                "text": "Yes,",
                "start": 46.84,
                "end": 47.06,
                "confidence": 0.969
              },
              {
                "text": "right.",
                "start": 47.28,
                "end": 47.37,
                "confidence": 0.973
              }
            ]
          },
          {
            "id": 17,
            "start": 47.37,
            "end": 47.9,
            "text": " I know.",
            "no_speech_prob": 0.3092843294143677,
            "confidence": 0.911,
            "words": [
              {
                "text": "I",
                "start": 47.37,
                "end": 47.72,
                "confidence": 0.83
              },
              {
                "text": "know.",
                "start": 47.72,
                "end": 47.9,
                "confidence": 0.999
              }
            ]
          },
          {
            "id": 18,
            "start": 48.32,
            "end": 50.8,
            "text": " You guys are sitting there going, five bucks says he's going to talk about coffee.",
            "no_speech_prob": 0.3092843294143677,
            "confidence": 0.847,
            "words": [
              {
                "text": "You",
                "start": 48.32,
                "end": 48.34,
                "confidence": 0.747
              },
              {
                "text": "guys",
                "start": 48.34,
                "end": 48.36,
                "confidence": 0.996
              },
              {
                "text": "are",
                "start": 48.36,
                "end": 48.44,
                "confidence": 0.839
              },
              {
                "text": "sitting",
                "start": 48.44,
                "end": 48.62,
                "confidence": 0.957
              },
              {
                "text": "there",
                "start": 48.62,
                "end": 48.72,
                "confidence": 0.976
              },
              {
                "text": "going,",
                "start": 48.72,
                "end": 48.84,
                "confidence": 0.938
              },
              {
                "text": "five",
                "start": 48.92,
                "end": 49.5,
                "confidence": 0.367
              },
              {
                "text": "bucks",
                "start": 49.5,
                "end": 49.72,
                "confidence": 0.977
              },
              {
                "text": "says",
                "start": 49.72,
                "end": 49.92,
                "confidence": 0.971
              },
              {
                "text": "he's",
                "start": 49.92,
                "end": 50.06,
                "confidence": 0.676
              },
              {
                "text": "going",
                "start": 50.06,
                "end": 50.14,
                "confidence": 0.889
              },
              {
                "text": "to",
                "start": 50.14,
                "end": 50.24,
                "confidence": 0.992
              },
              {
                "text": "talk",
                "start": 50.24,
                "end": 50.38,
                "confidence": 0.99
              },
              {
                "text": "about",
                "start": 50.38,
                "end": 50.54,
                "confidence": 0.991
              },
              {
                "text": "coffee.",
                "start": 50.54,
                "end": 50.8,
                "confidence": 0.923
              }
            ]
          },
          {
            "id": 19,
            "start": 50.8,
            "end": 51.98,
            "text": " Well, I am.",
            "no_speech_prob": 0.3092843294143677,
            "confidence": 0.984,
            "words": [
              {
                "text": "Well,",
                "start": 50.8,
                "end": 51.32,
                "confidence": 0.992
              },
              {
                "text": "I",
                "start": 51.44,
                "end": 51.58,
                "confidence": 0.986
              },
              {
                "text": "am.",
                "start": 51.58,
                "end": 51.98,
                "confidence": 0.974
              }
            ]
          },
          {
            "id": 20,
            "start": 52.16,
            "end": 54.34,
            "text": " That's right, because I got my van, you Columbia coffee.",
            "no_speech_prob": 0.3092843294143677,
            "confidence": 0.864,
            "words": [
              {
                "text": "That's",
                "start": 52.16,
                "end": 52.36,
                "confidence": 0.996
              },
              {
                "text": "right,",
                "start": 52.36,
                "end": 52.48,
                "confidence": 0.998
              },
              {
                "text": "because",
                "start": 52.52,
                "end": 52.68,
                "confidence": 0.997
              },
              {
                "text": "I",
                "start": 52.68,
                "end": 52.74,
                "confidence": 0.996
              },
              {
                "text": "got",
                "start": 52.74,
                "end": 52.9,
                "confidence": 0.971
              },
              {
                "text": "my",
                "start": 52.9,
                "end": 53.0,
                "confidence": 0.998
              },
              {
                "text": "van,",
                "start": 53.0,
                "end": 53.3,
                "confidence": 0.922
              },
              {
                "text": "you",
                "start": 53.62,
                "end": 53.64,
                "confidence": 0.375
              },
              {
                "text": "Columbia",
                "start": 53.64,
                "end": 53.96,
                "confidence": 0.872
              },
              {
                "text": "coffee.",
                "start": 53.96,
                "end": 54.34,
                "confidence": 0.698
              }
            ]
          },
          {
            "id": 21,
            "start": 54.44,
            "end": 54.94,
            "text": " Right here.",
            "no_speech_prob": 0.3092843294143677,
            "confidence": 0.981,
            "words": [
              {
                "text": "Right",
                "start": 54.44,
                "end": 54.68,
                "confidence": 0.966
              },
              {
                "text": "here.",
                "start": 54.68,
                "end": 54.94,
                "confidence": 0.996
              }
            ]
          },
          {
            "id": 22,
            "start": 55.26,
            "end": 56.34,
            "text": " Boom advertisement.",
            "no_speech_prob": 0.3092843294143677,
            "confidence": 0.64,
            "words": [
              {
                "text": "Boom",
                "start": 55.26,
                "end": 55.58,
                "confidence": 0.962
              },
              {
                "text": "advertisement.",
                "start": 55.58,
                "end": 56.34,
                "confidence": 0.426
              }
            ]
          },
          {
            "id": 23,
            "start": 56.66,
            "end": 56.86,
            "text": " Yeah.",
            "no_speech_prob": 0.3092843294143677,
            "confidence": 0.904,
            "words": [
              {
                "text": "Yeah.",
                "start": 56.66,
                "end": 56.86,
                "confidence": 0.904
              }
            ]
          },
          {
            "id": 24,
            "start": 57.54,
            "end": 58.2,
            "text": " Pain me for this.",
            "no_speech_prob": 0.06657163053750992,
            "confidence": 0.614,
            "words": [
              {
                "text": "Pain",
                "start": 57.54,
                "end": 57.76,
                "confidence": 0.149
              },
              {
                "text": "me",
                "start": 57.76,
                "end": 57.9,
                "confidence": 0.957
              },
              {
                "text": "for",
                "start": 57.9,
                "end": 58.04,
                "confidence": 0.995
              },
              {
                "text": "this.",
                "start": 58.04,
                "end": 58.2,
                "confidence": 0.999
              }
            ]
          },
          {
            "id": 25,
            "start": 58.2,
            "end": 58.78,
            "text": " I'm care.",
            "no_speech_prob": 0.06657163053750992,
            "confidence": 0.891,
            "words": [
              {
                "text": "I'm",
                "start": 58.2,
                "end": 58.5,
                "confidence": 0.982
              },
              {
                "text": "care.",
                "start": 58.5,
                "end": 58.78,
                "confidence": 0.732
              }
            ]
          },
          {
            "id": 26,
            "start": 59.04,
            "end": 62.43,
            "text": " So which might not know about coffee is yes, you probably already know that a lot of",
            "no_speech_prob": 0.06657163053750992,
            "confidence": 0.894,
            "words": [
              {
                "text": "So",
                "start": 59.04,
                "end": 59.2,
                "confidence": 0.922
              },
              {
                "text": "which",
                "start": 59.2,
                "end": 59.32,
                "confidence": 0.538
              },
              {
                "text": "might",
                "start": 59.32,
                "end": 59.48,
                "confidence": 0.7
              },
              {
                "text": "not",
                "start": 59.48,
                "end": 59.64,
                "confidence": 0.997
              },
              {
                "text": "know",
                "start": 59.64,
                "end": 59.82,
                "confidence": 0.989
              },
              {
                "text": "about",
                "start": 59.82,
                "end": 60.08,
                "confidence": 0.994
              },
              {
                "text": "coffee",
                "start": 60.08,
                "end": 60.52,
                "confidence": 0.98
              },
              {
                "text": "is",
                "start": 60.52,
                "end": 60.76,
                "confidence": 0.869
              },
              {
                "text": "yes,",
                "start": 60.76,
                "end": 60.92,
                "confidence": 0.797
              },
              {
                "text": "you",
                "start": 61.02,
                "end": 61.12,
                "confidence": 0.996
              },
              {
                "text": "probably",
                "start": 61.12,
                "end": 61.36,
                "confidence": 0.946
              },
              {
                "text": "already",
                "start": 61.36,
                "end": 61.68,
                "confidence": 0.996
              },
              {
                "text": "know",
                "start": 61.68,
                "end": 61.9,
                "confidence": 0.993
              },
              {
                "text": "that",
                "start": 61.9,
                "end": 62.12,
                "confidence": 0.873
              },
              {
                "text": "a",
                "start": 62.12,
                "end": 62.26,
                "confidence": 0.985
              },
              {
                "text": "lot",
                "start": 62.26,
                "end": 62.4,
                "confidence": 0.986
              },
              {
                "text": "of",
                "start": 62.4,
                "end": 62.43,
                "confidence": 0.811
              }
            ]
          },
          {
            "id": 27,
            "start": 62.43,
            "end": 64.02,
            "text": " companies actually buy it up.",
            "no_speech_prob": 0.06657163053750992,
            "confidence": 0.95,
            "words": [
              {
                "text": "companies",
                "start": 62.43,
                "end": 62.96,
                "confidence": 0.991
              },
              {
                "text": "actually",
                "start": 62.96,
                "end": 63.46,
                "confidence": 0.969
              },
              {
                "text": "buy",
                "start": 63.46,
                "end": 63.76,
                "confidence": 0.812
              },
              {
                "text": "it",
                "start": 63.76,
                "end": 63.86,
                "confidence": 0.992
              },
              {
                "text": "up.",
                "start": 63.86,
                "end": 64.02,
                "confidence": 0.998
              }
            ]
          },
          {
            "id": 28,
            "start": 64.28,
            "end": 67.18,
            "text": " Starbucks buys all had a coffee from Columbia.",
            "no_speech_prob": 0.06657163053750992,
            "confidence": 0.767,
            "words": [
              {
                "text": "Starbucks",
                "start": 64.28,
                "end": 64.78,
                "confidence": 0.765
              },
              {
                "text": "buys",
                "start": 64.78,
                "end": 65.16,
                "confidence": 0.983
              },
              {
                "text": "all",
                "start": 65.16,
                "end": 65.56,
                "confidence": 0.688
              },
              {
                "text": "had",
                "start": 65.56,
                "end": 65.76,
                "confidence": 0.244
              },
              {
                "text": "a",
                "start": 65.76,
                "end": 65.92,
                "confidence": 0.99
              },
              {
                "text": "coffee",
                "start": 65.92,
                "end": 66.3,
                "confidence": 0.991
              },
              {
                "text": "from",
                "start": 66.3,
                "end": 66.6,
                "confidence": 0.997
              },
              {
                "text": "Columbia.",
                "start": 66.6,
                "end": 67.18,
                "confidence": 0.968
              }
            ]
          },
          {
            "id": 29,
            "start": 67.7,
            "end": 69.68,
            "text": " It's kind of like their favorite place to buy coffee.",
            "no_speech_prob": 0.06657163053750992,
            "confidence": 0.961,
            "words": [
              {
                "text": "It's",
                "start": 67.7,
                "end": 67.84,
                "confidence": 0.977
              },
              {
                "text": "kind",
                "start": 67.84,
                "end": 67.92,
                "confidence": 0.874
              },
              {
                "text": "of",
                "start": 67.92,
                "end": 68.0,
                "confidence": 0.99
              },
              {
                "text": "like",
                "start": 68.0,
                "end": 68.1,
                "confidence": 0.995
              },
              {
                "text": "their",
                "start": 68.1,
                "end": 68.2,
                "confidence": 0.83
              },
              {
                "text": "favorite",
                "start": 68.2,
                "end": 68.44,
                "confidence": 0.975
              },
              {
                "text": "place",
                "start": 68.44,
                "end": 68.66,
                "confidence": 0.997
              },
              {
                "text": "to",
                "start": 68.66,
                "end": 68.84,
                "confidence": 0.989
              },
              {
                "text": "buy",
                "start": 68.84,
                "end": 69.24,
                "confidence": 0.996
              },
              {
                "text": "coffee.",
                "start": 69.24,
                "end": 69.68,
                "confidence": 0.992
              }
            ]
          },
          {
            "id": 30,
            "start": 70.02,
            "end": 74.69,
            "text": " And kind of to pay tribute to that Starbucks when they were making their 1,000th store",
            "no_speech_prob": 0.06657163053750992,
            "confidence": 0.878,
            "words": [
              {
                "text": "And",
                "start": 70.02,
                "end": 70.18,
                "confidence": 0.99
              },
              {
                "text": "kind",
                "start": 70.18,
                "end": 70.36,
                "confidence": 0.625
              },
              {
                "text": "of",
                "start": 70.36,
                "end": 70.48,
                "confidence": 0.996
              },
              {
                "text": "to",
                "start": 70.48,
                "end": 70.62,
                "confidence": 0.965
              },
              {
                "text": "pay",
                "start": 70.62,
                "end": 70.88,
                "confidence": 0.996
              },
              {
                "text": "tribute",
                "start": 70.88,
                "end": 71.32,
                "confidence": 0.999
              },
              {
                "text": "to",
                "start": 71.32,
                "end": 71.58,
                "confidence": 0.995
              },
              {
                "text": "that",
                "start": 71.58,
                "end": 71.9,
                "confidence": 0.997
              },
              {
                "text": "Starbucks",
                "start": 71.9,
                "end": 72.72,
                "confidence": 0.851
              },
              {
                "text": "when",
                "start": 72.72,
                "end": 72.98,
                "confidence": 0.818
              },
              {
                "text": "they",
                "start": 72.98,
                "end": 73.06,
                "confidence": 0.988
              },
              {
                "text": "were",
                "start": 73.06,
                "end": 73.2,
                "confidence": 0.557
              },
              {
                "text": "making",
                "start": 73.2,
                "end": 73.42,
                "confidence": 0.998
              },
              {
                "text": "their",
                "start": 73.42,
                "end": 73.62,
                "confidence": 0.986
              },
              {
                "text": "1,000th",
                "start": 73.62,
                "end": 74.58,
                "confidence": 0.831
              },
              {
                "text": "store",
                "start": 74.58,
                "end": 74.69,
                "confidence": 0.806
              }
            ]
          },
          {
            "id": 31,
            "start": 74.69,
            "end": 79.36,
            "text": " in 2016, they decided, yo, we're going to put it in Columbia.",
            "no_speech_prob": 0.06657163053750992,
            "confidence": 0.951,
            "words": [
              {
                "text": "in",
                "start": 74.69,
                "end": 75.12,
                "confidence": 0.995
              },
              {
                "text": "2016,",
                "start": 75.12,
                "end": 76.42,
                "confidence": 0.995
              },
              {
                "text": "they",
                "start": 76.62,
                "end": 77.06,
                "confidence": 0.993
              },
              {
                "text": "decided,",
                "start": 77.06,
                "end": 77.56,
                "confidence": 0.998
              },
              {
                "text": "yo,",
                "start": 77.66,
                "end": 77.96,
                "confidence": 0.615
              },
              {
                "text": "we're",
                "start": 78.02,
                "end": 78.2,
                "confidence": 0.979
              },
              {
                "text": "going",
                "start": 78.2,
                "end": 78.36,
                "confidence": 0.917
              },
              {
                "text": "to",
                "start": 78.36,
                "end": 78.4,
                "confidence": 0.998
              },
              {
                "text": "put",
                "start": 78.4,
                "end": 78.58,
                "confidence": 0.998
              },
              {
                "text": "it",
                "start": 78.58,
                "end": 78.7,
                "confidence": 0.997
              },
              {
                "text": "in",
                "start": 78.7,
                "end": 78.84,
                "confidence": 0.997
              },
              {
                "text": "Columbia.",
                "start": 78.84,
                "end": 79.36,
                "confidence": 0.986
              }
            ]
          },
          {
            "id": 32,
            "start": 79.82,
            "end": 82.27,
            "text": " And this was in the town of Medellin, Columbia.",
            "no_speech_prob": 0.06657163053750992,
            "confidence": 0.903,
            "words": [
              {
                "text": "And",
                "start": 79.82,
                "end": 80.0,
                "confidence": 0.979
              },
              {
                "text": "this",
                "start": 80.0,
                "end": 80.22,
                "confidence": 0.998
              },
              {
                "text": "was",
                "start": 80.22,
                "end": 80.42,
                "confidence": 0.991
              },
              {
                "text": "in",
                "start": 80.42,
                "end": 80.58,
                "confidence": 0.99
              },
              {
                "text": "the",
                "start": 80.58,
                "end": 80.7,
                "confidence": 0.993
              },
              {
                "text": "town",
                "start": 80.7,
                "end": 80.98,
                "confidence": 0.993
              },
              {
                "text": "of",
                "start": 80.98,
                "end": 81.22,
                "confidence": 0.999
              },
              {
                "text": "Medellin,",
                "start": 81.22,
                "end": 81.72,
                "confidence": 0.706
              },
              {
                "text": "Columbia.",
                "start": 81.78,
                "end": 82.27,
                "confidence": 0.977
              }
            ]
          },
          {
            "id": 33,
            "start": 82.27,
            "end": 85.4,
            "text": " Now here's the thing when it comes to coffee in Columbia.",
            "no_speech_prob": 0.06657163053750992,
            "confidence": 0.893,
            "words": [
              {
                "text": "Now",
                "start": 82.27,
                "end": 82.74,
                "confidence": 0.71
              },
              {
                "text": "here's",
                "start": 82.74,
                "end": 83.06,
                "confidence": 0.949
              },
              {
                "text": "the",
                "start": 83.06,
                "end": 83.22,
                "confidence": 0.997
              },
              {
                "text": "thing",
                "start": 83.22,
                "end": 83.38,
                "confidence": 0.999
              },
              {
                "text": "when",
                "start": 83.38,
                "end": 83.54,
                "confidence": 0.496
              },
              {
                "text": "it",
                "start": 83.54,
                "end": 83.68,
                "confidence": 0.998
              },
              {
                "text": "comes",
                "start": 83.68,
                "end": 84.06,
                "confidence": 0.998
              },
              {
                "text": "to",
                "start": 84.06,
                "end": 84.26,
                "confidence": 0.994
              },
              {
                "text": "coffee",
                "start": 84.26,
                "end": 84.68,
                "confidence": 0.87
              },
              {
                "text": "in",
                "start": 84.68,
                "end": 84.94,
                "confidence": 0.99
              },
              {
                "text": "Columbia.",
                "start": 84.94,
                "end": 85.4,
                "confidence": 0.952
              }
            ]
          },
          {
            "id": 34,
            "start": 85.52,
            "end": 91.9,
            "text": " They are the third largest producing and exporting coffee country in the world.",
            "no_speech_prob": 0.0978880524635315,
            "confidence": 0.962,
            "words": [
              {
                "text": "They",
                "start": 85.52,
                "end": 85.68,
                "confidence": 0.938
              },
              {
                "text": "are",
                "start": 85.68,
                "end": 85.88,
                "confidence": 0.991
              },
              {
                "text": "the",
                "start": 85.88,
                "end": 86.06,
                "confidence": 0.995
              },
              {
                "text": "third",
                "start": 86.06,
                "end": 86.64,
                "confidence": 0.973
              },
              {
                "text": "largest",
                "start": 86.64,
                "end": 87.5,
                "confidence": 0.98
              },
              {
                "text": "producing",
                "start": 87.5,
                "end": 88.76,
                "confidence": 0.832
              },
              {
                "text": "and",
                "start": 88.76,
                "end": 89.34,
                "confidence": 0.893
              },
              {
                "text": "exporting",
                "start": 89.34,
                "end": 89.92,
                "confidence": 0.972
              },
              {
                "text": "coffee",
                "start": 89.92,
                "end": 90.5,
                "confidence": 0.984
              },
              {
                "text": "country",
                "start": 90.5,
                "end": 90.92,
                "confidence": 0.985
              },
              {
                "text": "in",
                "start": 90.92,
                "end": 91.16,
                "confidence": 0.988
              },
              {
                "text": "the",
                "start": 91.16,
                "end": 91.32,
                "confidence": 0.994
              },
              {
                "text": "world.",
                "start": 91.32,
                "end": 91.9,
                "confidence": 0.993
              }
            ]
          },
          {
            "id": 35,
            "start": 92.22,
            "end": 99.26,
            "text": " The amount of coffee that is exported from Columbia equals about 810,000 metric tons.",
            "no_speech_prob": 0.0978880524635315,
            "confidence": 0.956,
            "words": [
              {
                "text": "The",
                "start": 92.22,
                "end": 92.36,
                "confidence": 0.998
              },
              {
                "text": "amount",
                "start": 92.36,
                "end": 92.6,
                "confidence": 1.0
              },
              {
                "text": "of",
                "start": 92.6,
                "end": 92.76,
                "confidence": 0.999
              },
              {
                "text": "coffee",
                "start": 92.76,
                "end": 93.06,
                "confidence": 0.997
              },
              {
                "text": "that",
                "start": 93.06,
                "end": 93.2,
                "confidence": 0.995
              },
              {
                "text": "is",
                "start": 93.2,
                "end": 93.34,
                "confidence": 0.979
              },
              {
                "text": "exported",
                "start": 93.34,
                "end": 93.84,
                "confidence": 0.987
              },
              {
                "text": "from",
                "start": 93.84,
                "end": 94.16,
                "confidence": 0.998
              },
              {
                "text": "Columbia",
                "start": 94.16,
                "end": 94.66,
                "confidence": 0.977
              },
              {
                "text": "equals",
                "start": 94.66,
                "end": 95.18,
                "confidence": 0.943
              },
              {
                "text": "about",
                "start": 95.18,
                "end": 95.6,
                "confidence": 0.986
              },
              {
                "text": "810,000",
                "start": 95.6,
                "end": 98.14,
                "confidence": 0.873
              },
              {
                "text": "metric",
                "start": 98.14,
                "end": 98.68,
                "confidence": 0.96
              },
              {
                "text": "tons.",
                "start": 98.68,
                "end": 99.26,
                "confidence": 0.962
              }
            ]
          },
          {
            "id": 36,
            "start": 99.84,
            "end": 102.93,
            "text": " Or approximately 11.5 million bags.",
            "no_speech_prob": 0.0978880524635315,
            "confidence": 0.981,
            "words": [
              {
                "text": "Or",
                "start": 99.84,
                "end": 100.04,
                "confidence": 0.984
              },
              {
                "text": "approximately",
                "start": 100.04,
                "end": 100.66,
                "confidence": 0.991
              },
              {
                "text": "11.5",
                "start": 100.66,
                "end": 102.12,
                "confidence": 0.98
              },
              {
                "text": "million",
                "start": 102.12,
                "end": 102.52,
                "confidence": 0.975
              },
              {
                "text": "bags.",
                "start": 102.52,
                "end": 102.93,
                "confidence": 0.974
              }
            ]
          },
          {
            "id": 37,
            "start": 102.93,
            "end": 108.64,
            "text": " However, although it might be beaten by countries like Brazil, it is actually the",
            "no_speech_prob": 0.0978880524635315,
            "confidence": 0.982,
            "words": [
              {
                "text": "However,",
                "start": 102.93,
                "end": 103.62,
                "confidence": 0.995
              },
              {
                "text": "although",
                "start": 103.82,
                "end": 104.08,
                "confidence": 0.984
              },
              {
                "text": "it",
                "start": 104.08,
                "end": 104.38,
                "confidence": 0.976
              },
              {
                "text": "might",
                "start": 104.38,
                "end": 104.58,
                "confidence": 0.993
              },
              {
                "text": "be",
                "start": 104.58,
                "end": 104.8,
                "confidence": 0.996
              },
              {
                "text": "beaten",
                "start": 104.8,
                "end": 105.08,
                "confidence": 0.944
              },
              {
                "text": "by",
                "start": 105.08,
                "end": 105.36,
                "confidence": 0.999
              },
              {
                "text": "countries",
                "start": 105.36,
                "end": 105.96,
                "confidence": 0.985
              },
              {
                "text": "like",
                "start": 105.96,
                "end": 106.46,
                "confidence": 0.996
              },
              {
                "text": "Brazil,",
                "start": 106.46,
                "end": 107.3,
                "confidence": 0.976
              },
              {
                "text": "it",
                "start": 107.52,
                "end": 108.02,
                "confidence": 0.99
              },
              {
                "text": "is",
                "start": 108.02,
                "end": 108.14,
                "confidence": 0.972
              },
              {
                "text": "actually",
                "start": 108.14,
                "end": 108.44,
                "confidence": 0.989
              },
              {
                "text": "the",
                "start": 108.44,
                "end": 108.64,
                "confidence": 0.952
              }
            ]
          },
          {
            "id": 38,
            "start": 108.64,
            "end": 114.36,
            "text": " number one or highest country for producing and growing a specific type of being known",
            "no_speech_prob": 0.0978880524635315,
            "confidence": 0.906,
            "words": [
              {
                "text": "number",
                "start": 108.64,
                "end": 108.92,
                "confidence": 0.848
              },
              {
                "text": "one",
                "start": 108.92,
                "end": 109.16,
                "confidence": 0.94
              },
              {
                "text": "or",
                "start": 109.16,
                "end": 109.42,
                "confidence": 0.843
              },
              {
                "text": "highest",
                "start": 109.42,
                "end": 109.8,
                "confidence": 0.989
              },
              {
                "text": "country",
                "start": 109.8,
                "end": 110.2,
                "confidence": 0.987
              },
              {
                "text": "for",
                "start": 110.2,
                "end": 110.5,
                "confidence": 0.995
              },
              {
                "text": "producing",
                "start": 110.5,
                "end": 111.12,
                "confidence": 0.996
              },
              {
                "text": "and",
                "start": 111.12,
                "end": 111.36,
                "confidence": 0.994
              },
              {
                "text": "growing",
                "start": 111.36,
                "end": 111.68,
                "confidence": 0.996
              },
              {
                "text": "a",
                "start": 111.68,
                "end": 112.22,
                "confidence": 0.926
              },
              {
                "text": "specific",
                "start": 112.22,
                "end": 112.88,
                "confidence": 0.997
              },
              {
                "text": "type",
                "start": 112.88,
                "end": 113.24,
                "confidence": 0.998
              },
              {
                "text": "of",
                "start": 113.24,
                "end": 113.4,
                "confidence": 0.998
              },
              {
                "text": "being",
                "start": 113.4,
                "end": 114.0,
                "confidence": 0.447
              },
              {
                "text": "known",
                "start": 114.0,
                "end": 114.36,
                "confidence": 0.853
              }
            ]
          },
          {
            "id": 39,
            "start": 114.38,
            "end": 116.3,
            "text": " as the Arabica being.",
            "no_speech_prob": 0.0728147029876709,
            "confidence": 0.73,
            "words": [
              {
                "text": "as",
                "start": 114.38,
                "end": 114.68,
                "confidence": 0.994
              },
              {
                "text": "the",
                "start": 114.68,
                "end": 114.88,
                "confidence": 0.976
              },
              {
                "text": "Arabica",
                "start": 114.88,
                "end": 115.7,
                "confidence": 0.542
              },
              {
                "text": "being.",
                "start": 115.7,
                "end": 116.3,
                "confidence": 0.727
              }
            ]
          },
          {
            "id": 40,
            "start": 116.66,
            "end": 120.26,
            "text": " And I know coffee is really important when it comes to talking about Columbia, but you",
            "no_speech_prob": 0.0728147029876709,
            "confidence": 0.973,
            "words": [
              {
                "text": "And",
                "start": 116.66,
                "end": 116.8,
                "confidence": 0.986
              },
              {
                "text": "I",
                "start": 116.8,
                "end": 116.9,
                "confidence": 0.994
              },
              {
                "text": "know",
                "start": 116.9,
                "end": 117.06,
                "confidence": 1.0
              },
              {
                "text": "coffee",
                "start": 117.06,
                "end": 117.5,
                "confidence": 0.931
              },
              {
                "text": "is",
                "start": 117.5,
                "end": 117.8,
                "confidence": 0.995
              },
              {
                "text": "really",
                "start": 117.8,
                "end": 118.12,
                "confidence": 0.998
              },
              {
                "text": "important",
                "start": 118.12,
                "end": 118.7,
                "confidence": 0.997
              },
              {
                "text": "when",
                "start": 118.7,
                "end": 118.92,
                "confidence": 0.987
              },
              {
                "text": "it",
                "start": 118.92,
                "end": 119.0,
                "confidence": 0.996
              },
              {
                "text": "comes",
                "start": 119.0,
                "end": 119.22,
                "confidence": 0.997
              },
              {
                "text": "to",
                "start": 119.22,
                "end": 119.4,
                "confidence": 0.995
              },
              {
                "text": "talking",
                "start": 119.4,
                "end": 119.56,
                "confidence": 0.903
              },
              {
                "text": "about",
                "start": 119.56,
                "end": 119.7,
                "confidence": 0.998
              },
              {
                "text": "Columbia,",
                "start": 119.7,
                "end": 119.94,
                "confidence": 0.973
              },
              {
                "text": "but",
                "start": 120.06,
                "end": 120.16,
                "confidence": 0.989
              },
              {
                "text": "you",
                "start": 120.16,
                "end": 120.26,
                "confidence": 0.845
              }
            ]
          },
          {
            "id": 41,
            "start": 120.26,
            "end": 122.64,
            "text": " really don't know how important it is with its culture.",
            "no_speech_prob": 0.0728147029876709,
            "confidence": 0.896,
            "words": [
              {
                "text": "really",
                "start": 120.26,
                "end": 120.58,
                "confidence": 0.355
              },
              {
                "text": "don't",
                "start": 120.58,
                "end": 120.76,
                "confidence": 0.998
              },
              {
                "text": "know",
                "start": 120.76,
                "end": 120.94,
                "confidence": 0.993
              },
              {
                "text": "how",
                "start": 120.94,
                "end": 121.12,
                "confidence": 0.994
              },
              {
                "text": "important",
                "start": 121.12,
                "end": 121.6,
                "confidence": 0.999
              },
              {
                "text": "it",
                "start": 121.6,
                "end": 121.78,
                "confidence": 0.986
              },
              {
                "text": "is",
                "start": 121.78,
                "end": 121.92,
                "confidence": 0.999
              },
              {
                "text": "with",
                "start": 121.92,
                "end": 122.1,
                "confidence": 0.985
              },
              {
                "text": "its",
                "start": 122.1,
                "end": 122.26,
                "confidence": 0.888
              },
              {
                "text": "culture.",
                "start": 122.26,
                "end": 122.64,
                "confidence": 0.999
              }
            ]
          },
          {
            "id": 42,
            "start": 123.02,
            "end": 130.51,
            "text": " Interesting fact that in 2007, major spots, equaling a buffer zone of approximately 207,000",
            "no_speech_prob": 0.0728147029876709,
            "confidence": 0.855,
            "words": [
              {
                "text": "Interesting",
                "start": 123.02,
                "end": 123.56,
                "confidence": 0.832
              },
              {
                "text": "fact",
                "start": 123.56,
                "end": 124.08,
                "confidence": 0.995
              },
              {
                "text": "that",
                "start": 124.08,
                "end": 124.34,
                "confidence": 0.929
              },
              {
                "text": "in",
                "start": 124.34,
                "end": 124.6,
                "confidence": 0.968
              },
              {
                "text": "2007,",
                "start": 124.6,
                "end": 125.58,
                "confidence": 0.99
              },
              {
                "text": "major",
                "start": 125.74,
                "end": 126.18,
                "confidence": 0.955
              },
              {
                "text": "spots,",
                "start": 126.18,
                "end": 126.7,
                "confidence": 0.944
              },
              {
                "text": "equaling",
                "start": 126.72,
                "end": 127.24,
                "confidence": 0.613
              },
              {
                "text": "a",
                "start": 127.24,
                "end": 127.38,
                "confidence": 0.597
              },
              {
                "text": "buffer",
                "start": 127.38,
                "end": 127.72,
                "confidence": 0.737
              },
              {
                "text": "zone",
                "start": 127.72,
                "end": 128.04,
                "confidence": 0.992
              },
              {
                "text": "of",
                "start": 128.04,
                "end": 128.24,
                "confidence": 0.853
              },
              {
                "text": "approximately",
                "start": 128.24,
                "end": 128.78,
                "confidence": 0.995
              },
              {
                "text": "207,000",
                "start": 128.78,
                "end": 130.51,
                "confidence": 0.897
              }
            ]
          },
          {
            "id": 43,
            "start": 130.51,
            "end": 136.67,
            "text": " hectares, which are called the coffee cultural landscape, were considered a UNESCO World Heritage",
            "no_speech_prob": 0.0728147029876709,
            "confidence": 0.888,
            "words": [
              {
                "text": "hectares,",
                "start": 130.51,
                "end": 131.2,
                "confidence": 0.894
              },
              {
                "text": "which",
                "start": 131.7,
                "end": 131.84,
                "confidence": 0.994
              },
              {
                "text": "are",
                "start": 131.84,
                "end": 132.12,
                "confidence": 0.994
              },
              {
                "text": "called",
                "start": 132.12,
                "end": 132.44,
                "confidence": 0.998
              },
              {
                "text": "the",
                "start": 132.44,
                "end": 132.68,
                "confidence": 0.981
              },
              {
                "text": "coffee",
                "start": 132.68,
                "end": 133.12,
                "confidence": 0.816
              },
              {
                "text": "cultural",
                "start": 133.12,
                "end": 133.58,
                "confidence": 0.793
              },
              {
                "text": "landscape,",
                "start": 133.58,
                "end": 134.16,
                "confidence": 0.983
              },
              {
                "text": "were",
                "start": 134.28,
                "end": 134.62,
                "confidence": 0.894
              },
              {
                "text": "considered",
                "start": 134.62,
                "end": 135.2,
                "confidence": 0.993
              },
              {
                "text": "a",
                "start": 135.2,
                "end": 135.42,
                "confidence": 0.987
              },
              {
                "text": "UNESCO",
                "start": 135.42,
                "end": 135.9,
                "confidence": 0.946
              },
              {
                "text": "World",
                "start": 135.9,
                "end": 136.18,
                "confidence": 0.656
              },
              {
                "text": "Heritage",
                "start": 136.18,
                "end": 136.67,
                "confidence": 0.586
              }
            ]
          },
          {
            "id": 44,
            "start": 136.67,
            "end": 137.22,
            "text": " Site.",
            "no_speech_prob": 0.0728147029876709,
            "confidence": 0.696,
            "words": [
              {
                "text": "Site.",
                "start": 136.67,
                "end": 137.22,
                "confidence": 0.696
              }
            ]
          },
          {
            "id": 45,
            "start": 137.28,
            "end": 144.14,
            "text": " And also in 2007, the EU, the European Union, granted Colombian coffee, a protected designation",
            "no_speech_prob": 0.0728147029876709,
            "confidence": 0.902,
            "words": [
              {
                "text": "And",
                "start": 137.28,
                "end": 137.76,
                "confidence": 0.758
              },
              {
                "text": "also",
                "start": 137.76,
                "end": 138.06,
                "confidence": 0.998
              },
              {
                "text": "in",
                "start": 138.06,
                "end": 138.28,
                "confidence": 0.896
              },
              {
                "text": "2007,",
                "start": 138.28,
                "end": 139.04,
                "confidence": 0.994
              },
              {
                "text": "the",
                "start": 139.2,
                "end": 139.38,
                "confidence": 0.993
              },
              {
                "text": "EU,",
                "start": 139.38,
                "end": 139.72,
                "confidence": 0.923
              },
              {
                "text": "the",
                "start": 139.82,
                "end": 139.96,
                "confidence": 0.982
              },
              {
                "text": "European",
                "start": 139.96,
                "end": 140.34,
                "confidence": 0.997
              },
              {
                "text": "Union,",
                "start": 140.34,
                "end": 140.7,
                "confidence": 0.998
              },
              {
                "text": "granted",
                "start": 140.76,
                "end": 141.24,
                "confidence": 0.918
              },
              {
                "text": "Colombian",
                "start": 141.24,
                "end": 141.88,
                "confidence": 0.768
              },
              {
                "text": "coffee,",
                "start": 141.88,
                "end": 142.3,
                "confidence": 0.921
              },
              {
                "text": "a",
                "start": 142.38,
                "end": 142.8,
                "confidence": 0.956
              },
              {
                "text": "protected",
                "start": 142.8,
                "end": 143.36,
                "confidence": 0.978
              },
              {
                "text": "designation",
                "start": 143.36,
                "end": 144.14,
                "confidence": 0.689
              }
            ]
          },
          {
            "id": 46,
            "start": 144.34,
            "end": 145.62,
            "text": " of origin status.",
            "no_speech_prob": 0.0007917813491076231,
            "confidence": 0.903,
            "words": [
              {
                "text": "of",
                "start": 144.34,
                "end": 144.54,
                "confidence": 0.984
              },
              {
                "text": "origin",
                "start": 144.54,
                "end": 145.02,
                "confidence": 0.972
              },
              {
                "text": "status.",
                "start": 145.02,
                "end": 145.62,
                "confidence": 0.769
              }
            ]
          },
          {
            "id": 47,
            "start": 146.12,
            "end": 149.9,
            "text": " Now, interesting enough when it comes to the coffee in Columbia, believe it or not,",
            "no_speech_prob": 0.0007917813491076231,
            "confidence": 0.854,
            "words": [
              {
                "text": "Now,",
                "start": 146.12,
                "end": 146.22,
                "confidence": 0.879
              },
              {
                "text": "interesting",
                "start": 146.56,
                "end": 146.62,
                "confidence": 0.535
              },
              {
                "text": "enough",
                "start": 146.62,
                "end": 146.96,
                "confidence": 0.955
              },
              {
                "text": "when",
                "start": 146.96,
                "end": 147.14,
                "confidence": 0.563
              },
              {
                "text": "it",
                "start": 147.14,
                "end": 147.24,
                "confidence": 0.994
              },
              {
                "text": "comes",
                "start": 147.24,
                "end": 147.46,
                "confidence": 0.995
              },
              {
                "text": "to",
                "start": 147.46,
                "end": 147.66,
                "confidence": 0.992
              },
              {
                "text": "the",
                "start": 147.66,
                "end": 147.82,
                "confidence": 0.982
              },
              {
                "text": "coffee",
                "start": 147.82,
                "end": 148.2,
                "confidence": 0.966
              },
              {
                "text": "in",
                "start": 148.2,
                "end": 148.5,
                "confidence": 0.981
              },
              {
                "text": "Columbia,",
                "start": 148.5,
                "end": 149.08,
                "confidence": 0.576
              },
              {
                "text": "believe",
                "start": 149.34,
                "end": 149.54,
                "confidence": 0.78
              },
              {
                "text": "it",
                "start": 149.54,
                "end": 149.7,
                "confidence": 0.978
              },
              {
                "text": "or",
                "start": 149.7,
                "end": 149.8,
                "confidence": 0.996
              },
              {
                "text": "not,",
                "start": 149.8,
                "end": 149.9,
                "confidence": 0.932
              }
            ]
          },
          {
            "id": 48,
            "start": 149.9,
            "end": 153.1,
            "text": " it is not actually native to the country.",
            "no_speech_prob": 0.0007917813491076231,
            "confidence": 0.979,
            "words": [
              {
                "text": "it",
                "start": 149.9,
                "end": 150.28,
                "confidence": 0.991
              },
              {
                "text": "is",
                "start": 150.28,
                "end": 150.42,
                "confidence": 0.973
              },
              {
                "text": "not",
                "start": 150.42,
                "end": 151.0,
                "confidence": 0.92
              },
              {
                "text": "actually",
                "start": 151.0,
                "end": 151.78,
                "confidence": 0.974
              },
              {
                "text": "native",
                "start": 151.78,
                "end": 152.3,
                "confidence": 0.992
              },
              {
                "text": "to",
                "start": 152.3,
                "end": 152.54,
                "confidence": 0.995
              },
              {
                "text": "the",
                "start": 152.54,
                "end": 152.74,
                "confidence": 0.992
              },
              {
                "text": "country.",
                "start": 152.74,
                "end": 153.1,
                "confidence": 0.998
              }
            ]
          },
          {
            "id": 49,
            "start": 153.54,
            "end": 157.88,
            "text": " It's come from somewhere else, not really an invasive species because it's very much",
            "no_speech_prob": 0.0007917813491076231,
            "confidence": 0.929,
            "words": [
              {
                "text": "It's",
                "start": 153.54,
                "end": 153.78,
                "confidence": 0.913
              },
              {
                "text": "come",
                "start": 153.78,
                "end": 153.98,
                "confidence": 0.911
              },
              {
                "text": "from",
                "start": 153.98,
                "end": 154.12,
                "confidence": 0.997
              },
              {
                "text": "somewhere",
                "start": 154.12,
                "end": 154.52,
                "confidence": 0.991
              },
              {
                "text": "else,",
                "start": 154.52,
                "end": 155.02,
                "confidence": 1.0
              },
              {
                "text": "not",
                "start": 155.32,
                "end": 155.44,
                "confidence": 0.988
              },
              {
                "text": "really",
                "start": 155.44,
                "end": 155.66,
                "confidence": 0.969
              },
              {
                "text": "an",
                "start": 155.66,
                "end": 155.78,
                "confidence": 0.845
              },
              {
                "text": "invasive",
                "start": 155.78,
                "end": 156.22,
                "confidence": 0.994
              },
              {
                "text": "species",
                "start": 156.22,
                "end": 156.74,
                "confidence": 0.976
              },
              {
                "text": "because",
                "start": 156.74,
                "end": 157.08,
                "confidence": 0.642
              },
              {
                "text": "it's",
                "start": 157.08,
                "end": 157.38,
                "confidence": 0.97
              },
              {
                "text": "very",
                "start": 157.38,
                "end": 157.72,
                "confidence": 0.993
              },
              {
                "text": "much",
                "start": 157.72,
                "end": 157.88,
                "confidence": 0.869
              }
            ]
          },
          {
            "id": 50,
            "start": 157.88,
            "end": 158.42,
            "text": " welcomed.",
            "no_speech_prob": 0.0007917813491076231,
            "confidence": 0.962,
            "words": [
              {
                "text": "welcomed.",
                "start": 157.88,
                "end": 158.42,
                "confidence": 0.962
              }
            ]
          },
          {
            "id": 51,
            "start": 158.82,
            "end": 162.81,
            "text": " Now you may have also seen this guy on many different Colombian coffee brands.",
            "no_speech_prob": 0.0007917813491076231,
            "confidence": 0.966,
            "words": [
              {
                "text": "Now",
                "start": 158.82,
                "end": 158.98,
                "confidence": 0.991
              },
              {
                "text": "you",
                "start": 158.98,
                "end": 159.12,
                "confidence": 0.924
              },
              {
                "text": "may",
                "start": 159.12,
                "end": 159.28,
                "confidence": 0.994
              },
              {
                "text": "have",
                "start": 159.28,
                "end": 159.42,
                "confidence": 0.962
              },
              {
                "text": "also",
                "start": 159.42,
                "end": 159.76,
                "confidence": 0.985
              },
              {
                "text": "seen",
                "start": 159.76,
                "end": 160.12,
                "confidence": 0.996
              },
              {
                "text": "this",
                "start": 160.12,
                "end": 160.36,
                "confidence": 0.988
              },
              {
                "text": "guy",
                "start": 160.36,
                "end": 160.7,
                "confidence": 0.993
              },
              {
                "text": "on",
                "start": 160.7,
                "end": 160.94,
                "confidence": 0.974
              },
              {
                "text": "many",
                "start": 160.94,
                "end": 161.12,
                "confidence": 0.994
              },
              {
                "text": "different",
                "start": 161.12,
                "end": 161.34,
                "confidence": 0.981
              },
              {
                "text": "Colombian",
                "start": 161.34,
                "end": 162.0,
                "confidence": 0.908
              },
              {
                "text": "coffee",
                "start": 162.0,
                "end": 162.42,
                "confidence": 0.911
              },
              {
                "text": "brands.",
                "start": 162.42,
                "end": 162.81,
                "confidence": 0.987
              }
            ]
          },
          {
            "id": 52,
            "start": 162.81,
            "end": 164.54,
            "text": " Now his name is Juan Valdez.",
            "no_speech_prob": 0.0007917813491076231,
            "confidence": 0.885,
            "words": [
              {
                "text": "Now",
                "start": 162.81,
                "end": 163.04,
                "confidence": 0.967
              },
              {
                "text": "his",
                "start": 163.04,
                "end": 163.24,
                "confidence": 0.842
              },
              {
                "text": "name",
                "start": 163.24,
                "end": 163.48,
                "confidence": 0.999
              },
              {
                "text": "is",
                "start": 163.48,
                "end": 163.72,
                "confidence": 0.995
              },
              {
                "text": "Juan",
                "start": 163.72,
                "end": 164.0,
                "confidence": 0.757
              },
              {
                "text": "Valdez.",
                "start": 164.0,
                "end": 164.54,
                "confidence": 0.852
              }
            ]
          },
          {
            "id": 53,
            "start": 164.54,
            "end": 169.66,
            "text": " Now some people think that this guy is actually really a real coffee farmer, somebody just",
            "no_speech_prob": 0.0007917813491076231,
            "confidence": 0.837,
            "words": [
              {
                "text": "Now",
                "start": 164.54,
                "end": 164.92,
                "confidence": 0.983
              },
              {
                "text": "some",
                "start": 164.92,
                "end": 165.06,
                "confidence": 0.964
              },
              {
                "text": "people",
                "start": 165.06,
                "end": 165.24,
                "confidence": 0.997
              },
              {
                "text": "think",
                "start": 165.24,
                "end": 165.6,
                "confidence": 0.996
              },
              {
                "text": "that",
                "start": 165.6,
                "end": 165.76,
                "confidence": 0.876
              },
              {
                "text": "this",
                "start": 165.76,
                "end": 165.98,
                "confidence": 0.987
              },
              {
                "text": "guy",
                "start": 165.98,
                "end": 166.26,
                "confidence": 0.996
              },
              {
                "text": "is",
                "start": 166.26,
                "end": 166.4,
                "confidence": 0.947
              },
              {
                "text": "actually",
                "start": 166.4,
                "end": 166.86,
                "confidence": 0.92
              },
              {
                "text": "really",
                "start": 166.86,
                "end": 167.4,
                "confidence": 0.852
              },
              {
                "text": "a",
                "start": 167.4,
                "end": 167.62,
                "confidence": 0.391
              },
              {
                "text": "real",
                "start": 167.62,
                "end": 167.94,
                "confidence": 0.971
              },
              {
                "text": "coffee",
                "start": 167.94,
                "end": 168.48,
                "confidence": 0.978
              },
              {
                "text": "farmer,",
                "start": 168.48,
                "end": 169.02,
                "confidence": 0.99
              },
              {
                "text": "somebody",
                "start": 169.24,
                "end": 169.46,
                "confidence": 0.658
              },
              {
                "text": "just",
                "start": 169.46,
                "end": 169.66,
                "confidence": 0.394
              }
            ]
          }
        ]
      }
    ]


As anticipated, the returned JSON file has not only the snippets of transcribed text, but along with each includes timestamps and a "confidence" value for the accuracy of each transcription.

### Using a Non-Default Model

To use a [non-default model](../../modules/ai_model_modules/transcribe_module.md#available-models-in-the-transcribe-module) like [`whisper-large-v3`](https://huggingface.co/openai/whisper-large-v3), we must enter it explicitly through the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument when invoking the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

We do so below to process the same input file shown above.


```python
# process the file with a non-default model

process_output_2 = pipeline_1.process(local_file_path="../../../data/input/Interesting Facts About Colombia.mp3", # all parameters save 'modules' as above
                                      local_save_directory="../../../data/output",
                                      expire_time=60 * 30,
                                      wait_for_process=True,
                                      verbose=False,
                                      modules={"transcribe": {"model": "whisper-large-v3"}}) # specify a non-default model for this process as well as its parameters
```

We once again print out and review the output as we did above.


```python
# nicely print the output of this process

print(json.dumps(process_output_2, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_transcribe_1",
      "request_id": "f833fd1e-a23e-43c7-8a99-36ab714c419d",
      "file_id": "f2225a00-7174-4298-a4bc-541e1b360b1b",
      "message": "SUCCESS - output fetched for file_id f2225a00-7174-4298-a4bc-541e1b360b1b.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "transcript": " Episode looking at the great country of Colombia We looked at some really just basic facts its name a bit of its history the type of people that live there Landsize and all that jazz, but in this video, we're gonna go into a little bit more of a detailed look Yo, what is going on guys? Welcome back to have to D facts a channel where I look at people cultures and places My name is Dave Walpole and today We are gonna be looking more at Colombia in our Columbia part 2 video, which just reminds me guys This is part of our Columbia playlist I'll put it down in the description box below and I'll talk about that more at the end of the video But if you're new here join me every single Monday to learn about new countries from around the world You can do that by hitting that subscribe and that belt notification button, but let's get started Columbia so we all know Columbia is famous for its coffee, right? Yes, right I know you guys are sitting there going five bucks says he's gonna talk about coffee Well, I am that's right because I got my van huge Columbia coffee right here. Boom Advertisement. Yeah They're not even paying me for this. I don't care So what you might not know about coffee is yes You probably already know that a lot of companies actually buy it up Starbucks buys all had a coffee from Columbia It's kind of like their favorite place to buy coffee and kind of to pay tribute to that Starbucks when they were making their 1000th store in 2016 they decided yo, we're gonna put it in Colombia and this was in the town of metal in Colombia Now here's the thing when it comes to coffee in Colombia They are the third largest producing and exporting coffee country in the world the amount of coffee that is exported from Colombia equals about 810 thousand metric tons or approximately 11.5 million bags. However, although it might be beaten by countries like Brazil it is actually the number one or highest country for producing and growing a specific type of bean known as the Arabica bean And I know coffee is really important when it comes to talking about Columbia But you guys really don't know how important it is with its culture interesting fact that in 2007 major spots equaling a buffer zone of approximately 207,000 hectares which are called the coffee cultural landscape were considered a UNESCO World Heritage Site and also in 2007 the EU the European Union granted Colombian coffee a protected designation of origin status Now interesting enough when it comes to the coffee in Colombia, believe it or not. It is not actually native to the country It's come from somewhere else not really an invasive species because it's very much welcomed Now you may have also seen this guy on many different Colombian coffee brands Now his name is Juan Valdez. Now some people think that this guy is actually real. He's a real coffee farmer Somebody just drew",
          "timestamped_transcript": [
            {
              "id": 0,
              "start": 0.0,
              "end": 2.12,
              "text": " Episode looking at the great country of Colombia",
              "no_speech_prob": 0.051431022584438324,
              "confidence": 0.923,
              "words": [
                {
                  "text": "Episode",
                  "start": 0.0,
                  "end": 0.46,
                  "confidence": 0.663
                },
                {
                  "text": "looking",
                  "start": 0.46,
                  "end": 0.84,
                  "confidence": 0.996
                },
                {
                  "text": "at",
                  "start": 0.84,
                  "end": 1.0,
                  "confidence": 1.0
                },
                {
                  "text": "the",
                  "start": 1.0,
                  "end": 1.1,
                  "confidence": 0.999
                },
                {
                  "text": "great",
                  "start": 1.1,
                  "end": 1.34,
                  "confidence": 0.983
                },
                {
                  "text": "country",
                  "start": 1.34,
                  "end": 1.66,
                  "confidence": 0.996
                },
                {
                  "text": "of",
                  "start": 1.66,
                  "end": 1.82,
                  "confidence": 0.999
                },
                {
                  "text": "Colombia",
                  "start": 1.82,
                  "end": 2.12,
                  "confidence": 0.815
                }
              ]
            },
            {
              "id": 1,
              "start": 2.18,
              "end": 7.5,
              "text": " We looked at some really just basic facts its name a bit of its history the type of people that live there",
              "no_speech_prob": 0.051431022584438324,
              "confidence": 0.922,
              "words": [
                {
                  "text": "We",
                  "start": 2.18,
                  "end": 2.34,
                  "confidence": 0.88
                },
                {
                  "text": "looked",
                  "start": 2.34,
                  "end": 2.6,
                  "confidence": 0.999
                },
                {
                  "text": "at",
                  "start": 2.6,
                  "end": 2.76,
                  "confidence": 1.0
                },
                {
                  "text": "some",
                  "start": 2.76,
                  "end": 3.04,
                  "confidence": 1.0
                },
                {
                  "text": "really",
                  "start": 3.04,
                  "end": 3.32,
                  "confidence": 0.922
                },
                {
                  "text": "just",
                  "start": 3.32,
                  "end": 3.54,
                  "confidence": 0.996
                },
                {
                  "text": "basic",
                  "start": 3.54,
                  "end": 3.92,
                  "confidence": 0.998
                },
                {
                  "text": "facts",
                  "start": 3.92,
                  "end": 4.38,
                  "confidence": 0.941
                },
                {
                  "text": "its",
                  "start": 4.38,
                  "end": 4.58,
                  "confidence": 0.785
                },
                {
                  "text": "name",
                  "start": 4.58,
                  "end": 4.92,
                  "confidence": 0.999
                },
                {
                  "text": "a",
                  "start": 4.92,
                  "end": 5.06,
                  "confidence": 0.995
                },
                {
                  "text": "bit",
                  "start": 5.06,
                  "end": 5.2,
                  "confidence": 1.0
                },
                {
                  "text": "of",
                  "start": 5.2,
                  "end": 5.32,
                  "confidence": 1.0
                },
                {
                  "text": "its",
                  "start": 5.32,
                  "end": 5.5,
                  "confidence": 0.998
                },
                {
                  "text": "history",
                  "start": 5.5,
                  "end": 5.9,
                  "confidence": 0.999
                },
                {
                  "text": "the",
                  "start": 5.9,
                  "end": 6.36,
                  "confidence": 0.559
                },
                {
                  "text": "type",
                  "start": 6.36,
                  "end": 6.54,
                  "confidence": 0.997
                },
                {
                  "text": "of",
                  "start": 6.54,
                  "end": 6.6,
                  "confidence": 0.999
                },
                {
                  "text": "people",
                  "start": 6.6,
                  "end": 6.82,
                  "confidence": 1.0
                },
                {
                  "text": "that",
                  "start": 6.82,
                  "end": 6.98,
                  "confidence": 0.999
                },
                {
                  "text": "live",
                  "start": 6.98,
                  "end": 7.22,
                  "confidence": 0.685
                },
                {
                  "text": "there",
                  "start": 7.22,
                  "end": 7.5,
                  "confidence": 0.744
                }
              ]
            },
            {
              "id": 2,
              "start": 7.66,
              "end": 12.58,
              "text": " Landsize and all that jazz, but in this video, we're gonna go into a little bit more of a detailed look",
              "no_speech_prob": 0.051431022584438324,
              "confidence": 0.944,
              "words": [
                {
                  "text": "Landsize",
                  "start": 7.66,
                  "end": 8.28,
                  "confidence": 0.772
                },
                {
                  "text": "and",
                  "start": 8.28,
                  "end": 8.44,
                  "confidence": 0.992
                },
                {
                  "text": "all",
                  "start": 8.44,
                  "end": 8.7,
                  "confidence": 1.0
                },
                {
                  "text": "that",
                  "start": 8.7,
                  "end": 8.9,
                  "confidence": 1.0
                },
                {
                  "text": "jazz,",
                  "start": 8.9,
                  "end": 9.32,
                  "confidence": 0.991
                },
                {
                  "text": "but",
                  "start": 9.54,
                  "end": 9.62,
                  "confidence": 1.0
                },
                {
                  "text": "in",
                  "start": 9.62,
                  "end": 9.72,
                  "confidence": 1.0
                },
                {
                  "text": "this",
                  "start": 9.72,
                  "end": 9.88,
                  "confidence": 1.0
                },
                {
                  "text": "video,",
                  "start": 9.88,
                  "end": 10.1,
                  "confidence": 1.0
                },
                {
                  "text": "we're",
                  "start": 10.12,
                  "end": 10.26,
                  "confidence": 1.0
                },
                {
                  "text": "gonna",
                  "start": 10.26,
                  "end": 10.34,
                  "confidence": 0.944
                },
                {
                  "text": "go",
                  "start": 10.34,
                  "end": 10.48,
                  "confidence": 1.0
                },
                {
                  "text": "into",
                  "start": 10.48,
                  "end": 10.7,
                  "confidence": 0.998
                },
                {
                  "text": "a",
                  "start": 10.7,
                  "end": 10.88,
                  "confidence": 1.0
                },
                {
                  "text": "little",
                  "start": 10.88,
                  "end": 11.14,
                  "confidence": 0.999
                },
                {
                  "text": "bit",
                  "start": 11.14,
                  "end": 11.32,
                  "confidence": 1.0
                },
                {
                  "text": "more",
                  "start": 11.32,
                  "end": 11.6,
                  "confidence": 0.998
                },
                {
                  "text": "of",
                  "start": 11.6,
                  "end": 11.76,
                  "confidence": 0.996
                },
                {
                  "text": "a",
                  "start": 11.76,
                  "end": 11.84,
                  "confidence": 1.0
                },
                {
                  "text": "detailed",
                  "start": 11.84,
                  "end": 12.24,
                  "confidence": 0.996
                },
                {
                  "text": "look",
                  "start": 12.24,
                  "end": 12.58,
                  "confidence": 0.489
                }
              ]
            },
            {
              "id": 3,
              "start": 12.76,
              "end": 17.5,
              "text": " Yo, what is going on guys? Welcome back to have to D facts a channel where I look at people cultures and places",
              "no_speech_prob": 0.051431022584438324,
              "confidence": 0.836,
              "words": [
                {
                  "text": "Yo,",
                  "start": 12.76,
                  "end": 13.06,
                  "confidence": 0.778
                },
                {
                  "text": "what",
                  "start": 13.06,
                  "end": 13.34,
                  "confidence": 1.0
                },
                {
                  "text": "is",
                  "start": 13.34,
                  "end": 13.5,
                  "confidence": 1.0
                },
                {
                  "text": "going",
                  "start": 13.5,
                  "end": 13.7,
                  "confidence": 0.999
                },
                {
                  "text": "on",
                  "start": 13.7,
                  "end": 13.94,
                  "confidence": 0.999
                },
                {
                  "text": "guys?",
                  "start": 13.94,
                  "end": 14.3,
                  "confidence": 0.976
                },
                {
                  "text": "Welcome",
                  "start": 14.3,
                  "end": 14.58,
                  "confidence": 0.631
                },
                {
                  "text": "back",
                  "start": 14.58,
                  "end": 14.88,
                  "confidence": 0.993
                },
                {
                  "text": "to",
                  "start": 14.88,
                  "end": 15.04,
                  "confidence": 0.982
                },
                {
                  "text": "have",
                  "start": 15.04,
                  "end": 15.14,
                  "confidence": 0.42
                },
                {
                  "text": "to",
                  "start": 15.14,
                  "end": 15.24,
                  "confidence": 0.682
                },
                {
                  "text": "D",
                  "start": 15.24,
                  "end": 15.38,
                  "confidence": 0.257
                },
                {
                  "text": "facts",
                  "start": 15.38,
                  "end": 15.68,
                  "confidence": 0.878
                },
                {
                  "text": "a",
                  "start": 15.68,
                  "end": 15.84,
                  "confidence": 0.614
                },
                {
                  "text": "channel",
                  "start": 15.84,
                  "end": 16.0,
                  "confidence": 0.996
                },
                {
                  "text": "where",
                  "start": 16.0,
                  "end": 16.16,
                  "confidence": 0.969
                },
                {
                  "text": "I",
                  "start": 16.16,
                  "end": 16.22,
                  "confidence": 0.989
                },
                {
                  "text": "look",
                  "start": 16.22,
                  "end": 16.38,
                  "confidence": 0.995
                },
                {
                  "text": "at",
                  "start": 16.38,
                  "end": 16.48,
                  "confidence": 0.998
                },
                {
                  "text": "people",
                  "start": 16.48,
                  "end": 16.66,
                  "confidence": 0.998
                },
                {
                  "text": "cultures",
                  "start": 16.66,
                  "end": 17.02,
                  "confidence": 0.994
                },
                {
                  "text": "and",
                  "start": 17.02,
                  "end": 17.2,
                  "confidence": 0.925
                },
                {
                  "text": "places",
                  "start": 17.2,
                  "end": 17.5,
                  "confidence": 0.998
                }
              ]
            },
            {
              "id": 4,
              "start": 17.58,
              "end": 20.98,
              "text": " My name is Dave Walpole and today",
              "no_speech_prob": 0.051431022584438324,
              "confidence": 0.862,
              "words": [
                {
                  "text": "My",
                  "start": 17.58,
                  "end": 17.84,
                  "confidence": 0.78
                },
                {
                  "text": "name",
                  "start": 17.84,
                  "end": 18.22,
                  "confidence": 1.0
                },
                {
                  "text": "is",
                  "start": 18.22,
                  "end": 19.04,
                  "confidence": 0.999
                },
                {
                  "text": "Dave",
                  "start": 19.04,
                  "end": 19.46,
                  "confidence": 0.947
                },
                {
                  "text": "Walpole",
                  "start": 19.46,
                  "end": 20.0,
                  "confidence": 0.902
                },
                {
                  "text": "and",
                  "start": 20.0,
                  "end": 20.34,
                  "confidence": 0.53
                },
                {
                  "text": "today",
                  "start": 20.34,
                  "end": 20.98,
                  "confidence": 0.963
                }
              ]
            },
            {
              "id": 5,
              "start": 21.34,
              "end": 27.05,
              "text": " We are gonna be looking more at Colombia in our Columbia part 2 video, which just reminds me guys",
              "no_speech_prob": 0.051431022584438324,
              "confidence": 0.937,
              "words": [
                {
                  "text": "We",
                  "start": 21.34,
                  "end": 21.68,
                  "confidence": 0.967
                },
                {
                  "text": "are",
                  "start": 21.68,
                  "end": 22.06,
                  "confidence": 0.999
                },
                {
                  "text": "gonna",
                  "start": 22.06,
                  "end": 22.24,
                  "confidence": 0.925
                },
                {
                  "text": "be",
                  "start": 22.24,
                  "end": 22.38,
                  "confidence": 1.0
                },
                {
                  "text": "looking",
                  "start": 22.38,
                  "end": 22.62,
                  "confidence": 1.0
                },
                {
                  "text": "more",
                  "start": 22.62,
                  "end": 23.02,
                  "confidence": 0.998
                },
                {
                  "text": "at",
                  "start": 23.02,
                  "end": 23.24,
                  "confidence": 1.0
                },
                {
                  "text": "Colombia",
                  "start": 23.24,
                  "end": 23.66,
                  "confidence": 0.607
                },
                {
                  "text": "in",
                  "start": 23.66,
                  "end": 23.84,
                  "confidence": 0.992
                },
                {
                  "text": "our",
                  "start": 23.84,
                  "end": 24.0,
                  "confidence": 0.998
                },
                {
                  "text": "Columbia",
                  "start": 24.0,
                  "end": 24.28,
                  "confidence": 0.734
                },
                {
                  "text": "part",
                  "start": 24.28,
                  "end": 24.56,
                  "confidence": 0.904
                },
                {
                  "text": "2",
                  "start": 24.56,
                  "end": 24.82,
                  "confidence": 0.815
                },
                {
                  "text": "video,",
                  "start": 24.82,
                  "end": 25.28,
                  "confidence": 0.998
                },
                {
                  "text": "which",
                  "start": 25.3,
                  "end": 25.96,
                  "confidence": 1.0
                },
                {
                  "text": "just",
                  "start": 25.96,
                  "end": 26.26,
                  "confidence": 1.0
                },
                {
                  "text": "reminds",
                  "start": 26.26,
                  "end": 26.7,
                  "confidence": 1.0
                },
                {
                  "text": "me",
                  "start": 26.7,
                  "end": 26.86,
                  "confidence": 0.999
                },
                {
                  "text": "guys",
                  "start": 26.86,
                  "end": 27.05,
                  "confidence": 0.998
                }
              ]
            },
            {
              "id": 6,
              "start": 27.05,
              "end": 28.8,
              "text": " This is part of our Columbia playlist",
              "no_speech_prob": 0.00026602245634421706,
              "confidence": 0.944,
              "words": [
                {
                  "text": "This",
                  "start": 27.05,
                  "end": 27.24,
                  "confidence": 0.956
                },
                {
                  "text": "is",
                  "start": 27.24,
                  "end": 27.36,
                  "confidence": 1.0
                },
                {
                  "text": "part",
                  "start": 27.36,
                  "end": 27.54,
                  "confidence": 0.999
                },
                {
                  "text": "of",
                  "start": 27.54,
                  "end": 27.66,
                  "confidence": 1.0
                },
                {
                  "text": "our",
                  "start": 27.66,
                  "end": 27.82,
                  "confidence": 1.0
                },
                {
                  "text": "Columbia",
                  "start": 27.82,
                  "end": 28.3,
                  "confidence": 0.715
                },
                {
                  "text": "playlist",
                  "start": 28.3,
                  "end": 28.8,
                  "confidence": 0.978
                }
              ]
            },
            {
              "id": 7,
              "start": 28.86,
              "end": 32.36,
              "text": " I'll put it down in the description box below and I'll talk about that more at the end of the video",
              "no_speech_prob": 0.00026602245634421706,
              "confidence": 0.969,
              "words": [
                {
                  "text": "I'll",
                  "start": 28.86,
                  "end": 29.02,
                  "confidence": 0.973
                },
                {
                  "text": "put",
                  "start": 29.02,
                  "end": 29.1,
                  "confidence": 1.0
                },
                {
                  "text": "it",
                  "start": 29.1,
                  "end": 29.18,
                  "confidence": 0.999
                },
                {
                  "text": "down",
                  "start": 29.18,
                  "end": 29.36,
                  "confidence": 1.0
                },
                {
                  "text": "in",
                  "start": 29.36,
                  "end": 29.5,
                  "confidence": 0.553
                },
                {
                  "text": "the",
                  "start": 29.5,
                  "end": 29.6,
                  "confidence": 0.998
                },
                {
                  "text": "description",
                  "start": 29.6,
                  "end": 29.9,
                  "confidence": 0.998
                },
                {
                  "text": "box",
                  "start": 29.9,
                  "end": 30.14,
                  "confidence": 0.996
                },
                {
                  "text": "below",
                  "start": 30.14,
                  "end": 30.38,
                  "confidence": 1.0
                },
                {
                  "text": "and",
                  "start": 30.38,
                  "end": 30.52,
                  "confidence": 0.992
                },
                {
                  "text": "I'll",
                  "start": 30.52,
                  "end": 30.68,
                  "confidence": 0.994
                },
                {
                  "text": "talk",
                  "start": 30.68,
                  "end": 30.82,
                  "confidence": 0.999
                },
                {
                  "text": "about",
                  "start": 30.82,
                  "end": 30.98,
                  "confidence": 0.999
                },
                {
                  "text": "that",
                  "start": 30.98,
                  "end": 31.14,
                  "confidence": 0.999
                },
                {
                  "text": "more",
                  "start": 31.14,
                  "end": 31.28,
                  "confidence": 0.996
                },
                {
                  "text": "at",
                  "start": 31.28,
                  "end": 31.44,
                  "confidence": 0.993
                },
                {
                  "text": "the",
                  "start": 31.44,
                  "end": 31.54,
                  "confidence": 1.0
                },
                {
                  "text": "end",
                  "start": 31.54,
                  "end": 31.72,
                  "confidence": 0.997
                },
                {
                  "text": "of",
                  "start": 31.72,
                  "end": 31.84,
                  "confidence": 0.98
                },
                {
                  "text": "the",
                  "start": 31.84,
                  "end": 31.96,
                  "confidence": 0.998
                },
                {
                  "text": "video",
                  "start": 31.96,
                  "end": 32.36,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 8,
              "start": 32.66,
              "end": 36.4,
              "text": " But if you're new here join me every single Monday to learn about new countries from around the world",
              "no_speech_prob": 0.00026602245634421706,
              "confidence": 0.981,
              "words": [
                {
                  "text": "But",
                  "start": 32.66,
                  "end": 32.84,
                  "confidence": 0.845
                },
                {
                  "text": "if",
                  "start": 32.84,
                  "end": 32.96,
                  "confidence": 1.0
                },
                {
                  "text": "you're",
                  "start": 32.96,
                  "end": 33.12,
                  "confidence": 0.972
                },
                {
                  "text": "new",
                  "start": 33.12,
                  "end": 33.24,
                  "confidence": 1.0
                },
                {
                  "text": "here",
                  "start": 33.24,
                  "end": 33.54,
                  "confidence": 0.999
                },
                {
                  "text": "join",
                  "start": 33.54,
                  "end": 33.9,
                  "confidence": 0.883
                },
                {
                  "text": "me",
                  "start": 33.9,
                  "end": 34.04,
                  "confidence": 0.992
                },
                {
                  "text": "every",
                  "start": 34.04,
                  "end": 34.24,
                  "confidence": 0.992
                },
                {
                  "text": "single",
                  "start": 34.24,
                  "end": 34.48,
                  "confidence": 1.0
                },
                {
                  "text": "Monday",
                  "start": 34.48,
                  "end": 34.72,
                  "confidence": 0.995
                },
                {
                  "text": "to",
                  "start": 34.72,
                  "end": 34.86,
                  "confidence": 1.0
                },
                {
                  "text": "learn",
                  "start": 34.86,
                  "end": 35.02,
                  "confidence": 1.0
                },
                {
                  "text": "about",
                  "start": 35.02,
                  "end": 35.18,
                  "confidence": 1.0
                },
                {
                  "text": "new",
                  "start": 35.18,
                  "end": 35.42,
                  "confidence": 0.998
                },
                {
                  "text": "countries",
                  "start": 35.42,
                  "end": 35.78,
                  "confidence": 0.995
                },
                {
                  "text": "from",
                  "start": 35.78,
                  "end": 36.0,
                  "confidence": 0.996
                },
                {
                  "text": "around",
                  "start": 36.0,
                  "end": 36.22,
                  "confidence": 0.999
                },
                {
                  "text": "the",
                  "start": 36.22,
                  "end": 36.36,
                  "confidence": 0.998
                },
                {
                  "text": "world",
                  "start": 36.36,
                  "end": 36.4,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 9,
              "start": 36.4,
              "end": 41.6,
              "text": " You can do that by hitting that subscribe and that belt notification button, but let's get started",
              "no_speech_prob": 0.00026602245634421706,
              "confidence": 0.93,
              "words": [
                {
                  "text": "You",
                  "start": 36.4,
                  "end": 36.6,
                  "confidence": 0.546
                },
                {
                  "text": "can",
                  "start": 36.6,
                  "end": 36.72,
                  "confidence": 1.0
                },
                {
                  "text": "do",
                  "start": 36.72,
                  "end": 36.84,
                  "confidence": 1.0
                },
                {
                  "text": "that",
                  "start": 36.84,
                  "end": 37.02,
                  "confidence": 1.0
                },
                {
                  "text": "by",
                  "start": 37.02,
                  "end": 37.18,
                  "confidence": 0.999
                },
                {
                  "text": "hitting",
                  "start": 37.18,
                  "end": 37.34,
                  "confidence": 0.986
                },
                {
                  "text": "that",
                  "start": 37.34,
                  "end": 37.54,
                  "confidence": 0.998
                },
                {
                  "text": "subscribe",
                  "start": 37.54,
                  "end": 37.92,
                  "confidence": 0.989
                },
                {
                  "text": "and",
                  "start": 37.92,
                  "end": 38.14,
                  "confidence": 0.763
                },
                {
                  "text": "that",
                  "start": 38.14,
                  "end": 38.32,
                  "confidence": 0.972
                },
                {
                  "text": "belt",
                  "start": 38.32,
                  "end": 38.5,
                  "confidence": 0.819
                },
                {
                  "text": "notification",
                  "start": 38.5,
                  "end": 39.12,
                  "confidence": 0.983
                },
                {
                  "text": "button,",
                  "start": 39.12,
                  "end": 39.46,
                  "confidence": 0.998
                },
                {
                  "text": "but",
                  "start": 39.54,
                  "end": 40.26,
                  "confidence": 1.0
                },
                {
                  "text": "let's",
                  "start": 40.26,
                  "end": 40.86,
                  "confidence": 0.94
                },
                {
                  "text": "get",
                  "start": 40.86,
                  "end": 41.2,
                  "confidence": 0.977
                },
                {
                  "text": "started",
                  "start": 41.2,
                  "end": 41.6,
                  "confidence": 0.998
                }
              ]
            },
            {
              "id": 10,
              "start": 42.18,
              "end": 47.46,
              "text": " Columbia so we all know Columbia is famous for its coffee, right? Yes, right",
              "no_speech_prob": 0.00026602245634421706,
              "confidence": 0.895,
              "words": [
                {
                  "text": "Columbia",
                  "start": 42.18,
                  "end": 42.76,
                  "confidence": 0.681
                },
                {
                  "text": "so",
                  "start": 42.76,
                  "end": 43.34,
                  "confidence": 0.809
                },
                {
                  "text": "we",
                  "start": 43.34,
                  "end": 43.5,
                  "confidence": 0.995
                },
                {
                  "text": "all",
                  "start": 43.5,
                  "end": 43.74,
                  "confidence": 1.0
                },
                {
                  "text": "know",
                  "start": 43.74,
                  "end": 44.08,
                  "confidence": 1.0
                },
                {
                  "text": "Columbia",
                  "start": 44.08,
                  "end": 44.56,
                  "confidence": 0.471
                },
                {
                  "text": "is",
                  "start": 44.56,
                  "end": 44.86,
                  "confidence": 0.999
                },
                {
                  "text": "famous",
                  "start": 44.86,
                  "end": 45.3,
                  "confidence": 1.0
                },
                {
                  "text": "for",
                  "start": 45.3,
                  "end": 45.6,
                  "confidence": 0.999
                },
                {
                  "text": "its",
                  "start": 45.6,
                  "end": 45.84,
                  "confidence": 0.93
                },
                {
                  "text": "coffee,",
                  "start": 45.84,
                  "end": 46.32,
                  "confidence": 0.994
                },
                {
                  "text": "right?",
                  "start": 46.36,
                  "end": 46.7,
                  "confidence": 1.0
                },
                {
                  "text": "Yes,",
                  "start": 46.86,
                  "end": 47.12,
                  "confidence": 0.897
                },
                {
                  "text": "right",
                  "start": 47.18,
                  "end": 47.46,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 11,
              "start": 47.5,
              "end": 50.96,
              "text": " I know you guys are sitting there going five bucks says he's gonna talk about coffee",
              "no_speech_prob": 0.00026602245634421706,
              "confidence": 0.932,
              "words": [
                {
                  "text": "I",
                  "start": 47.5,
                  "end": 47.66,
                  "confidence": 0.999
                },
                {
                  "text": "know",
                  "start": 47.66,
                  "end": 47.94,
                  "confidence": 1.0
                },
                {
                  "text": "you",
                  "start": 47.94,
                  "end": 48.14,
                  "confidence": 0.994
                },
                {
                  "text": "guys",
                  "start": 48.14,
                  "end": 48.32,
                  "confidence": 1.0
                },
                {
                  "text": "are",
                  "start": 48.32,
                  "end": 48.46,
                  "confidence": 0.988
                },
                {
                  "text": "sitting",
                  "start": 48.46,
                  "end": 48.62,
                  "confidence": 0.995
                },
                {
                  "text": "there",
                  "start": 48.62,
                  "end": 48.74,
                  "confidence": 0.984
                },
                {
                  "text": "going",
                  "start": 48.74,
                  "end": 48.98,
                  "confidence": 0.994
                },
                {
                  "text": "five",
                  "start": 48.98,
                  "end": 49.52,
                  "confidence": 0.69
                },
                {
                  "text": "bucks",
                  "start": 49.52,
                  "end": 49.74,
                  "confidence": 0.977
                },
                {
                  "text": "says",
                  "start": 49.74,
                  "end": 49.92,
                  "confidence": 0.745
                },
                {
                  "text": "he's",
                  "start": 49.92,
                  "end": 50.06,
                  "confidence": 0.802
                },
                {
                  "text": "gonna",
                  "start": 50.06,
                  "end": 50.16,
                  "confidence": 0.986
                },
                {
                  "text": "talk",
                  "start": 50.16,
                  "end": 50.38,
                  "confidence": 0.996
                },
                {
                  "text": "about",
                  "start": 50.38,
                  "end": 50.58,
                  "confidence": 0.999
                },
                {
                  "text": "coffee",
                  "start": 50.58,
                  "end": 50.96,
                  "confidence": 0.996
                }
              ]
            },
            {
              "id": 12,
              "start": 51.08,
              "end": 55.58,
              "text": " Well, I am that's right because I got my van huge Columbia coffee right here. Boom",
              "no_speech_prob": 0.00026602245634421706,
              "confidence": 0.882,
              "words": [
                {
                  "text": "Well,",
                  "start": 51.08,
                  "end": 51.28,
                  "confidence": 0.988
                },
                {
                  "text": "I",
                  "start": 51.4,
                  "end": 51.56,
                  "confidence": 1.0
                },
                {
                  "text": "am",
                  "start": 51.56,
                  "end": 51.9,
                  "confidence": 0.999
                },
                {
                  "text": "that's",
                  "start": 51.9,
                  "end": 52.34,
                  "confidence": 0.986
                },
                {
                  "text": "right",
                  "start": 52.34,
                  "end": 52.5,
                  "confidence": 1.0
                },
                {
                  "text": "because",
                  "start": 52.5,
                  "end": 52.66,
                  "confidence": 0.93
                },
                {
                  "text": "I",
                  "start": 52.66,
                  "end": 52.76,
                  "confidence": 1.0
                },
                {
                  "text": "got",
                  "start": 52.76,
                  "end": 52.88,
                  "confidence": 0.999
                },
                {
                  "text": "my",
                  "start": 52.88,
                  "end": 53.02,
                  "confidence": 1.0
                },
                {
                  "text": "van",
                  "start": 53.02,
                  "end": 53.4,
                  "confidence": 0.9
                },
                {
                  "text": "huge",
                  "start": 53.4,
                  "end": 53.66,
                  "confidence": 0.197
                },
                {
                  "text": "Columbia",
                  "start": 53.66,
                  "end": 54.02,
                  "confidence": 0.775
                },
                {
                  "text": "coffee",
                  "start": 54.02,
                  "end": 54.38,
                  "confidence": 0.977
                },
                {
                  "text": "right",
                  "start": 54.38,
                  "end": 54.72,
                  "confidence": 0.99
                },
                {
                  "text": "here.",
                  "start": 54.72,
                  "end": 55.08,
                  "confidence": 0.999
                },
                {
                  "text": "Boom",
                  "start": 55.08,
                  "end": 55.58,
                  "confidence": 0.994
                }
              ]
            },
            {
              "id": 13,
              "start": 55.86,
              "end": 56.82,
              "text": " Advertisement. Yeah",
              "no_speech_prob": 0.00026602245634421706,
              "confidence": 0.938,
              "words": [
                {
                  "text": "Advertisement.",
                  "start": 55.86,
                  "end": 56.54,
                  "confidence": 0.924
                },
                {
                  "text": "Yeah",
                  "start": 56.68,
                  "end": 56.82,
                  "confidence": 0.998
                }
              ]
            },
            {
              "id": 14,
              "start": 57.06,
              "end": 58.88,
              "text": " They're not even paying me for this. I don't care",
              "no_speech_prob": 0.000187394063686952,
              "confidence": 0.912,
              "words": [
                {
                  "text": "They're",
                  "start": 57.06,
                  "end": 57.3,
                  "confidence": 0.638
                },
                {
                  "text": "not",
                  "start": 57.3,
                  "end": 57.36,
                  "confidence": 0.904
                },
                {
                  "text": "even",
                  "start": 57.36,
                  "end": 57.52,
                  "confidence": 0.921
                },
                {
                  "text": "paying",
                  "start": 57.52,
                  "end": 57.72,
                  "confidence": 0.989
                },
                {
                  "text": "me",
                  "start": 57.72,
                  "end": 57.88,
                  "confidence": 1.0
                },
                {
                  "text": "for",
                  "start": 57.88,
                  "end": 58.04,
                  "confidence": 1.0
                },
                {
                  "text": "this.",
                  "start": 58.04,
                  "end": 58.28,
                  "confidence": 1.0
                },
                {
                  "text": "I",
                  "start": 58.3,
                  "end": 58.38,
                  "confidence": 0.999
                },
                {
                  "text": "don't",
                  "start": 58.38,
                  "end": 58.58,
                  "confidence": 0.998
                },
                {
                  "text": "care",
                  "start": 58.58,
                  "end": 58.88,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 15,
              "start": 58.96,
              "end": 60.88,
              "text": " So what you might not know about coffee is yes",
              "no_speech_prob": 0.000187394063686952,
              "confidence": 0.976,
              "words": [
                {
                  "text": "So",
                  "start": 58.96,
                  "end": 59.16,
                  "confidence": 0.919
                },
                {
                  "text": "what",
                  "start": 59.16,
                  "end": 59.28,
                  "confidence": 0.889
                },
                {
                  "text": "you",
                  "start": 59.28,
                  "end": 59.34,
                  "confidence": 0.998
                },
                {
                  "text": "might",
                  "start": 59.34,
                  "end": 59.5,
                  "confidence": 1.0
                },
                {
                  "text": "not",
                  "start": 59.5,
                  "end": 59.66,
                  "confidence": 1.0
                },
                {
                  "text": "know",
                  "start": 59.66,
                  "end": 59.86,
                  "confidence": 1.0
                },
                {
                  "text": "about",
                  "start": 59.86,
                  "end": 60.12,
                  "confidence": 0.999
                },
                {
                  "text": "coffee",
                  "start": 60.12,
                  "end": 60.54,
                  "confidence": 0.98
                },
                {
                  "text": "is",
                  "start": 60.54,
                  "end": 60.74,
                  "confidence": 0.997
                },
                {
                  "text": "yes",
                  "start": 60.74,
                  "end": 60.88,
                  "confidence": 0.985
                }
              ]
            },
            {
              "id": 16,
              "start": 60.88,
              "end": 67.16,
              "text": " You probably already know that a lot of companies actually buy it up Starbucks buys all had a coffee from Columbia",
              "no_speech_prob": 0.000187394063686952,
              "confidence": 0.886,
              "words": [
                {
                  "text": "You",
                  "start": 60.88,
                  "end": 61.1,
                  "confidence": 0.966
                },
                {
                  "text": "probably",
                  "start": 61.1,
                  "end": 61.42,
                  "confidence": 1.0
                },
                {
                  "text": "already",
                  "start": 61.42,
                  "end": 61.7,
                  "confidence": 1.0
                },
                {
                  "text": "know",
                  "start": 61.7,
                  "end": 61.92,
                  "confidence": 0.999
                },
                {
                  "text": "that",
                  "start": 61.92,
                  "end": 62.14,
                  "confidence": 0.999
                },
                {
                  "text": "a",
                  "start": 62.14,
                  "end": 62.26,
                  "confidence": 0.999
                },
                {
                  "text": "lot",
                  "start": 62.26,
                  "end": 62.4,
                  "confidence": 1.0
                },
                {
                  "text": "of",
                  "start": 62.4,
                  "end": 62.52,
                  "confidence": 0.999
                },
                {
                  "text": "companies",
                  "start": 62.52,
                  "end": 63.08,
                  "confidence": 0.998
                },
                {
                  "text": "actually",
                  "start": 63.08,
                  "end": 63.5,
                  "confidence": 0.995
                },
                {
                  "text": "buy",
                  "start": 63.5,
                  "end": 63.74,
                  "confidence": 0.993
                },
                {
                  "text": "it",
                  "start": 63.74,
                  "end": 63.86,
                  "confidence": 0.999
                },
                {
                  "text": "up",
                  "start": 63.86,
                  "end": 64.14,
                  "confidence": 0.999
                },
                {
                  "text": "Starbucks",
                  "start": 64.14,
                  "end": 64.82,
                  "confidence": 0.769
                },
                {
                  "text": "buys",
                  "start": 64.82,
                  "end": 65.18,
                  "confidence": 0.964
                },
                {
                  "text": "all",
                  "start": 65.18,
                  "end": 65.54,
                  "confidence": 0.509
                },
                {
                  "text": "had",
                  "start": 65.54,
                  "end": 65.8,
                  "confidence": 0.462
                },
                {
                  "text": "a",
                  "start": 65.8,
                  "end": 66.0,
                  "confidence": 0.991
                },
                {
                  "text": "coffee",
                  "start": 66.0,
                  "end": 66.34,
                  "confidence": 0.992
                },
                {
                  "text": "from",
                  "start": 66.34,
                  "end": 66.64,
                  "confidence": 0.999
                },
                {
                  "text": "Columbia",
                  "start": 66.64,
                  "end": 67.16,
                  "confidence": 0.48
                }
              ]
            },
            {
              "id": 17,
              "start": 67.66,
              "end": 72.0,
              "text": " It's kind of like their favorite place to buy coffee and kind of to pay tribute to that",
              "no_speech_prob": 0.000187394063686952,
              "confidence": 0.956,
              "words": [
                {
                  "text": "It's",
                  "start": 67.66,
                  "end": 67.8,
                  "confidence": 0.9
                },
                {
                  "text": "kind",
                  "start": 67.8,
                  "end": 67.92,
                  "confidence": 0.946
                },
                {
                  "text": "of",
                  "start": 67.92,
                  "end": 67.98,
                  "confidence": 0.999
                },
                {
                  "text": "like",
                  "start": 67.98,
                  "end": 68.1,
                  "confidence": 1.0
                },
                {
                  "text": "their",
                  "start": 68.1,
                  "end": 68.24,
                  "confidence": 0.999
                },
                {
                  "text": "favorite",
                  "start": 68.24,
                  "end": 68.48,
                  "confidence": 0.986
                },
                {
                  "text": "place",
                  "start": 68.48,
                  "end": 68.7,
                  "confidence": 0.999
                },
                {
                  "text": "to",
                  "start": 68.7,
                  "end": 68.88,
                  "confidence": 0.999
                },
                {
                  "text": "buy",
                  "start": 68.88,
                  "end": 69.26,
                  "confidence": 1.0
                },
                {
                  "text": "coffee",
                  "start": 69.26,
                  "end": 69.72,
                  "confidence": 0.997
                },
                {
                  "text": "and",
                  "start": 69.72,
                  "end": 70.16,
                  "confidence": 0.992
                },
                {
                  "text": "kind",
                  "start": 70.16,
                  "end": 70.36,
                  "confidence": 0.583
                },
                {
                  "text": "of",
                  "start": 70.36,
                  "end": 70.48,
                  "confidence": 0.997
                },
                {
                  "text": "to",
                  "start": 70.48,
                  "end": 70.66,
                  "confidence": 0.987
                },
                {
                  "text": "pay",
                  "start": 70.66,
                  "end": 70.86,
                  "confidence": 0.999
                },
                {
                  "text": "tribute",
                  "start": 70.86,
                  "end": 71.36,
                  "confidence": 0.997
                },
                {
                  "text": "to",
                  "start": 71.36,
                  "end": 71.58,
                  "confidence": 0.998
                },
                {
                  "text": "that",
                  "start": 71.58,
                  "end": 72.0,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 18,
              "start": 72.18,
              "end": 75.12,
              "text": " Starbucks when they were making their 1000th store in",
              "no_speech_prob": 0.000187394063686952,
              "confidence": 0.894,
              "words": [
                {
                  "text": "Starbucks",
                  "start": 72.18,
                  "end": 72.74,
                  "confidence": 0.983
                },
                {
                  "text": "when",
                  "start": 72.74,
                  "end": 72.96,
                  "confidence": 0.999
                },
                {
                  "text": "they",
                  "start": 72.96,
                  "end": 73.06,
                  "confidence": 0.989
                },
                {
                  "text": "were",
                  "start": 73.06,
                  "end": 73.2,
                  "confidence": 0.879
                },
                {
                  "text": "making",
                  "start": 73.2,
                  "end": 73.46,
                  "confidence": 1.0
                },
                {
                  "text": "their",
                  "start": 73.46,
                  "end": 73.72,
                  "confidence": 0.992
                },
                {
                  "text": "1000th",
                  "start": 73.72,
                  "end": 74.64,
                  "confidence": 0.625
                },
                {
                  "text": "store",
                  "start": 74.64,
                  "end": 74.92,
                  "confidence": 0.99
                },
                {
                  "text": "in",
                  "start": 74.92,
                  "end": 75.12,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 19,
              "start": 75.88,
              "end": 82.24,
              "text": " 2016 they decided yo, we're gonna put it in Colombia and this was in the town of metal in Colombia",
              "no_speech_prob": 0.000187394063686952,
              "confidence": 0.854,
              "words": [
                {
                  "text": "2016",
                  "start": 75.88,
                  "end": 76.36,
                  "confidence": 0.998
                },
                {
                  "text": "they",
                  "start": 76.36,
                  "end": 77.06,
                  "confidence": 0.988
                },
                {
                  "text": "decided",
                  "start": 77.06,
                  "end": 77.62,
                  "confidence": 0.998
                },
                {
                  "text": "yo,",
                  "start": 77.62,
                  "end": 77.98,
                  "confidence": 0.942
                },
                {
                  "text": "we're",
                  "start": 77.98,
                  "end": 78.28,
                  "confidence": 0.999
                },
                {
                  "text": "gonna",
                  "start": 78.28,
                  "end": 78.38,
                  "confidence": 0.998
                },
                {
                  "text": "put",
                  "start": 78.38,
                  "end": 78.58,
                  "confidence": 1.0
                },
                {
                  "text": "it",
                  "start": 78.58,
                  "end": 78.74,
                  "confidence": 0.998
                },
                {
                  "text": "in",
                  "start": 78.74,
                  "end": 78.92,
                  "confidence": 1.0
                },
                {
                  "text": "Colombia",
                  "start": 78.92,
                  "end": 79.36,
                  "confidence": 0.518
                },
                {
                  "text": "and",
                  "start": 79.36,
                  "end": 79.96,
                  "confidence": 0.667
                },
                {
                  "text": "this",
                  "start": 79.96,
                  "end": 80.18,
                  "confidence": 0.999
                },
                {
                  "text": "was",
                  "start": 80.18,
                  "end": 80.42,
                  "confidence": 0.999
                },
                {
                  "text": "in",
                  "start": 80.42,
                  "end": 80.58,
                  "confidence": 1.0
                },
                {
                  "text": "the",
                  "start": 80.58,
                  "end": 80.7,
                  "confidence": 1.0
                },
                {
                  "text": "town",
                  "start": 80.7,
                  "end": 81.04,
                  "confidence": 0.997
                },
                {
                  "text": "of",
                  "start": 81.04,
                  "end": 81.26,
                  "confidence": 0.999
                },
                {
                  "text": "metal",
                  "start": 81.26,
                  "end": 81.56,
                  "confidence": 0.237
                },
                {
                  "text": "in",
                  "start": 81.56,
                  "end": 81.8,
                  "confidence": 0.919
                },
                {
                  "text": "Colombia",
                  "start": 81.8,
                  "end": 82.24,
                  "confidence": 0.523
                }
              ]
            },
            {
              "id": 20,
              "start": 82.56,
              "end": 85.37,
              "text": " Now here's the thing when it comes to coffee in Colombia",
              "no_speech_prob": 0.000187394063686952,
              "confidence": 0.97,
              "words": [
                {
                  "text": "Now",
                  "start": 82.56,
                  "end": 82.74,
                  "confidence": 0.959
                },
                {
                  "text": "here's",
                  "start": 82.74,
                  "end": 83.04,
                  "confidence": 0.945
                },
                {
                  "text": "the",
                  "start": 83.04,
                  "end": 83.22,
                  "confidence": 1.0
                },
                {
                  "text": "thing",
                  "start": 83.22,
                  "end": 83.4,
                  "confidence": 1.0
                },
                {
                  "text": "when",
                  "start": 83.4,
                  "end": 83.54,
                  "confidence": 0.994
                },
                {
                  "text": "it",
                  "start": 83.54,
                  "end": 83.66,
                  "confidence": 1.0
                },
                {
                  "text": "comes",
                  "start": 83.66,
                  "end": 84.14,
                  "confidence": 0.999
                },
                {
                  "text": "to",
                  "start": 84.14,
                  "end": 84.32,
                  "confidence": 1.0
                },
                {
                  "text": "coffee",
                  "start": 84.32,
                  "end": 84.76,
                  "confidence": 0.992
                },
                {
                  "text": "in",
                  "start": 84.76,
                  "end": 85.02,
                  "confidence": 0.999
                },
                {
                  "text": "Colombia",
                  "start": 85.02,
                  "end": 85.37,
                  "confidence": 0.824
                }
              ]
            },
            {
              "id": 21,
              "start": 85.37,
              "end": 86.7,
              "text": " They are the third",
              "no_speech_prob": 0.000187394063686952,
              "confidence": 0.939,
              "words": [
                {
                  "text": "They",
                  "start": 85.37,
                  "end": 85.62,
                  "confidence": 0.874
                },
                {
                  "text": "are",
                  "start": 85.62,
                  "end": 85.9,
                  "confidence": 0.971
                },
                {
                  "text": "the",
                  "start": 85.9,
                  "end": 86.12,
                  "confidence": 0.981
                },
                {
                  "text": "third",
                  "start": 86.12,
                  "end": 86.7,
                  "confidence": 0.934
                }
              ]
            },
            {
              "id": 22,
              "start": 86.92,
              "end": 87.62,
              "text": " largest",
              "no_speech_prob": 8.001490641618147e-05,
              "confidence": 0.979,
              "words": [
                {
                  "text": "largest",
                  "start": 86.92,
                  "end": 87.62,
                  "confidence": 0.979
                }
              ]
            },
            {
              "id": 23,
              "start": 87.92,
              "end": 95.64,
              "text": " producing and exporting coffee country in the world the amount of coffee that is exported from Colombia equals about",
              "no_speech_prob": 8.001490641618147e-05,
              "confidence": 0.96,
              "words": [
                {
                  "text": "producing",
                  "start": 87.92,
                  "end": 88.86,
                  "confidence": 0.75
                },
                {
                  "text": "and",
                  "start": 88.86,
                  "end": 89.34,
                  "confidence": 0.926
                },
                {
                  "text": "exporting",
                  "start": 89.34,
                  "end": 89.96,
                  "confidence": 0.91
                },
                {
                  "text": "coffee",
                  "start": 89.96,
                  "end": 90.5,
                  "confidence": 0.959
                },
                {
                  "text": "country",
                  "start": 90.5,
                  "end": 90.88,
                  "confidence": 0.992
                },
                {
                  "text": "in",
                  "start": 90.88,
                  "end": 91.16,
                  "confidence": 0.998
                },
                {
                  "text": "the",
                  "start": 91.16,
                  "end": 91.42,
                  "confidence": 0.999
                },
                {
                  "text": "world",
                  "start": 91.42,
                  "end": 91.96,
                  "confidence": 0.993
                },
                {
                  "text": "the",
                  "start": 91.96,
                  "end": 92.32,
                  "confidence": 0.902
                },
                {
                  "text": "amount",
                  "start": 92.32,
                  "end": 92.56,
                  "confidence": 0.999
                },
                {
                  "text": "of",
                  "start": 92.56,
                  "end": 92.76,
                  "confidence": 0.999
                },
                {
                  "text": "coffee",
                  "start": 92.76,
                  "end": 93.06,
                  "confidence": 0.998
                },
                {
                  "text": "that",
                  "start": 93.06,
                  "end": 93.2,
                  "confidence": 0.999
                },
                {
                  "text": "is",
                  "start": 93.2,
                  "end": 93.36,
                  "confidence": 0.997
                },
                {
                  "text": "exported",
                  "start": 93.36,
                  "end": 93.88,
                  "confidence": 0.99
                },
                {
                  "text": "from",
                  "start": 93.88,
                  "end": 94.18,
                  "confidence": 1.0
                },
                {
                  "text": "Colombia",
                  "start": 94.18,
                  "end": 94.72,
                  "confidence": 0.886
                },
                {
                  "text": "equals",
                  "start": 94.72,
                  "end": 95.2,
                  "confidence": 0.998
                },
                {
                  "text": "about",
                  "start": 95.2,
                  "end": 95.64,
                  "confidence": 0.997
                }
              ]
            },
            {
              "id": 24,
              "start": 95.96,
              "end": 97.04,
              "text": " 810",
              "no_speech_prob": 8.001490641618147e-05,
              "confidence": 0.892,
              "words": [
                {
                  "text": "810",
                  "start": 95.96,
                  "end": 97.04,
                  "confidence": 0.892
                }
              ]
            },
            {
              "id": 25,
              "start": 97.5,
              "end": 99.98,
              "text": " thousand metric tons or",
              "no_speech_prob": 8.001490641618147e-05,
              "confidence": 0.878,
              "words": [
                {
                  "text": "thousand",
                  "start": 97.5,
                  "end": 98.24,
                  "confidence": 0.652
                },
                {
                  "text": "metric",
                  "start": 98.24,
                  "end": 98.74,
                  "confidence": 0.996
                },
                {
                  "text": "tons",
                  "start": 98.74,
                  "end": 99.32,
                  "confidence": 0.95
                },
                {
                  "text": "or",
                  "start": 99.32,
                  "end": 99.98,
                  "confidence": 0.962
                }
              ]
            },
            {
              "id": 26,
              "start": 100.1,
              "end": 100.76,
              "text": " approximately",
              "no_speech_prob": 8.001490641618147e-05,
              "confidence": 0.747,
              "words": [
                {
                  "text": "approximately",
                  "start": 100.1,
                  "end": 100.76,
                  "confidence": 0.747
                }
              ]
            },
            {
              "id": 27,
              "start": 101.02,
              "end": 107.06,
              "text": " 11.5 million bags. However, although it might be beaten by countries like Brazil",
              "no_speech_prob": 8.001490641618147e-05,
              "confidence": 0.992,
              "words": [
                {
                  "text": "11.5",
                  "start": 101.02,
                  "end": 102.12,
                  "confidence": 0.998
                },
                {
                  "text": "million",
                  "start": 102.12,
                  "end": 102.58,
                  "confidence": 0.981
                },
                {
                  "text": "bags.",
                  "start": 102.58,
                  "end": 103.14,
                  "confidence": 0.996
                },
                {
                  "text": "However,",
                  "start": 103.46,
                  "end": 103.6,
                  "confidence": 0.994
                },
                {
                  "text": "although",
                  "start": 103.74,
                  "end": 104.04,
                  "confidence": 0.996
                },
                {
                  "text": "it",
                  "start": 104.04,
                  "end": 104.38,
                  "confidence": 0.999
                },
                {
                  "text": "might",
                  "start": 104.38,
                  "end": 104.6,
                  "confidence": 0.998
                },
                {
                  "text": "be",
                  "start": 104.6,
                  "end": 104.76,
                  "confidence": 1.0
                },
                {
                  "text": "beaten",
                  "start": 104.76,
                  "end": 105.08,
                  "confidence": 0.998
                },
                {
                  "text": "by",
                  "start": 105.08,
                  "end": 105.34,
                  "confidence": 1.0
                },
                {
                  "text": "countries",
                  "start": 105.34,
                  "end": 106.0,
                  "confidence": 0.984
                },
                {
                  "text": "like",
                  "start": 106.0,
                  "end": 106.5,
                  "confidence": 0.99
                },
                {
                  "text": "Brazil",
                  "start": 106.5,
                  "end": 107.06,
                  "confidence": 0.955
                }
              ]
            },
            {
              "id": 28,
              "start": 107.82,
              "end": 112.18,
              "text": " it is actually the number one or highest country for producing and growing a",
              "no_speech_prob": 8.001490641618147e-05,
              "confidence": 0.98,
              "words": [
                {
                  "text": "it",
                  "start": 107.82,
                  "end": 108.02,
                  "confidence": 0.774
                },
                {
                  "text": "is",
                  "start": 108.02,
                  "end": 108.14,
                  "confidence": 0.999
                },
                {
                  "text": "actually",
                  "start": 108.14,
                  "end": 108.44,
                  "confidence": 0.999
                },
                {
                  "text": "the",
                  "start": 108.44,
                  "end": 108.66,
                  "confidence": 1.0
                },
                {
                  "text": "number",
                  "start": 108.66,
                  "end": 108.94,
                  "confidence": 1.0
                },
                {
                  "text": "one",
                  "start": 108.94,
                  "end": 109.16,
                  "confidence": 0.993
                },
                {
                  "text": "or",
                  "start": 109.16,
                  "end": 109.4,
                  "confidence": 1.0
                },
                {
                  "text": "highest",
                  "start": 109.4,
                  "end": 109.84,
                  "confidence": 0.998
                },
                {
                  "text": "country",
                  "start": 109.84,
                  "end": 110.2,
                  "confidence": 0.999
                },
                {
                  "text": "for",
                  "start": 110.2,
                  "end": 110.5,
                  "confidence": 1.0
                },
                {
                  "text": "producing",
                  "start": 110.5,
                  "end": 111.1,
                  "confidence": 0.994
                },
                {
                  "text": "and",
                  "start": 111.1,
                  "end": 111.36,
                  "confidence": 1.0
                },
                {
                  "text": "growing",
                  "start": 111.36,
                  "end": 111.72,
                  "confidence": 0.999
                },
                {
                  "text": "a",
                  "start": 111.72,
                  "end": 112.18,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 29,
              "start": 112.24,
              "end": 116.24,
              "text": " specific type of bean known as the Arabica bean",
              "no_speech_prob": 8.001490641618147e-05,
              "confidence": 0.852,
              "words": [
                {
                  "text": "specific",
                  "start": 112.24,
                  "end": 112.92,
                  "confidence": 0.884
                },
                {
                  "text": "type",
                  "start": 112.92,
                  "end": 113.26,
                  "confidence": 0.999
                },
                {
                  "text": "of",
                  "start": 113.26,
                  "end": 113.48,
                  "confidence": 1.0
                },
                {
                  "text": "bean",
                  "start": 113.48,
                  "end": 113.86,
                  "confidence": 0.891
                },
                {
                  "text": "known",
                  "start": 113.86,
                  "end": 114.38,
                  "confidence": 0.982
                },
                {
                  "text": "as",
                  "start": 114.38,
                  "end": 114.72,
                  "confidence": 1.0
                },
                {
                  "text": "the",
                  "start": 114.72,
                  "end": 114.98,
                  "confidence": 1.0
                },
                {
                  "text": "Arabica",
                  "start": 114.98,
                  "end": 115.76,
                  "confidence": 0.569
                },
                {
                  "text": "bean",
                  "start": 115.76,
                  "end": 116.24,
                  "confidence": 0.802
                }
              ]
            },
            {
              "id": 30,
              "start": 116.24,
              "end": 119.97,
              "text": " And I know coffee is really important when it comes to talking about Columbia",
              "no_speech_prob": 0.00034109604894183576,
              "confidence": 0.944,
              "words": [
                {
                  "text": "And",
                  "start": 116.24,
                  "end": 116.76,
                  "confidence": 0.852
                },
                {
                  "text": "I",
                  "start": 116.76,
                  "end": 116.88,
                  "confidence": 0.997
                },
                {
                  "text": "know",
                  "start": 116.88,
                  "end": 117.06,
                  "confidence": 0.998
                },
                {
                  "text": "coffee",
                  "start": 117.06,
                  "end": 117.54,
                  "confidence": 0.994
                },
                {
                  "text": "is",
                  "start": 117.54,
                  "end": 117.82,
                  "confidence": 0.999
                },
                {
                  "text": "really",
                  "start": 117.82,
                  "end": 118.14,
                  "confidence": 0.997
                },
                {
                  "text": "important",
                  "start": 118.14,
                  "end": 118.74,
                  "confidence": 0.977
                },
                {
                  "text": "when",
                  "start": 118.74,
                  "end": 118.92,
                  "confidence": 0.998
                },
                {
                  "text": "it",
                  "start": 118.92,
                  "end": 119.04,
                  "confidence": 1.0
                },
                {
                  "text": "comes",
                  "start": 119.04,
                  "end": 119.26,
                  "confidence": 0.999
                },
                {
                  "text": "to",
                  "start": 119.26,
                  "end": 119.38,
                  "confidence": 0.999
                },
                {
                  "text": "talking",
                  "start": 119.38,
                  "end": 119.56,
                  "confidence": 0.918
                },
                {
                  "text": "about",
                  "start": 119.56,
                  "end": 119.7,
                  "confidence": 0.999
                },
                {
                  "text": "Columbia",
                  "start": 119.7,
                  "end": 119.97,
                  "confidence": 0.598
                }
              ]
            },
            {
              "id": 31,
              "start": 119.97,
              "end": 122.68,
              "text": " But you guys really don't know how important it is with its culture",
              "no_speech_prob": 0.00034109604894183576,
              "confidence": 0.98,
              "words": [
                {
                  "text": "But",
                  "start": 119.97,
                  "end": 120.16,
                  "confidence": 0.86
                },
                {
                  "text": "you",
                  "start": 120.16,
                  "end": 120.28,
                  "confidence": 0.92
                },
                {
                  "text": "guys",
                  "start": 120.28,
                  "end": 120.42,
                  "confidence": 0.976
                },
                {
                  "text": "really",
                  "start": 120.42,
                  "end": 120.62,
                  "confidence": 0.999
                },
                {
                  "text": "don't",
                  "start": 120.62,
                  "end": 120.8,
                  "confidence": 0.999
                },
                {
                  "text": "know",
                  "start": 120.8,
                  "end": 120.94,
                  "confidence": 0.999
                },
                {
                  "text": "how",
                  "start": 120.94,
                  "end": 121.14,
                  "confidence": 0.999
                },
                {
                  "text": "important",
                  "start": 121.14,
                  "end": 121.62,
                  "confidence": 0.998
                },
                {
                  "text": "it",
                  "start": 121.62,
                  "end": 121.78,
                  "confidence": 0.997
                },
                {
                  "text": "is",
                  "start": 121.78,
                  "end": 121.98,
                  "confidence": 1.0
                },
                {
                  "text": "with",
                  "start": 121.98,
                  "end": 122.12,
                  "confidence": 0.998
                },
                {
                  "text": "its",
                  "start": 122.12,
                  "end": 122.28,
                  "confidence": 0.986
                },
                {
                  "text": "culture",
                  "start": 122.28,
                  "end": 122.68,
                  "confidence": 0.998
                }
              ]
            },
            {
              "id": 32,
              "start": 123.08,
              "end": 128.7,
              "text": " interesting fact that in 2007 major spots equaling a buffer zone of approximately",
              "no_speech_prob": 0.00034109604894183576,
              "confidence": 0.941,
              "words": [
                {
                  "text": "interesting",
                  "start": 123.08,
                  "end": 123.62,
                  "confidence": 0.603
                },
                {
                  "text": "fact",
                  "start": 123.62,
                  "end": 124.12,
                  "confidence": 0.996
                },
                {
                  "text": "that",
                  "start": 124.12,
                  "end": 124.4,
                  "confidence": 0.999
                },
                {
                  "text": "in",
                  "start": 124.4,
                  "end": 124.68,
                  "confidence": 0.999
                },
                {
                  "text": "2007",
                  "start": 124.68,
                  "end": 125.6,
                  "confidence": 0.827
                },
                {
                  "text": "major",
                  "start": 125.6,
                  "end": 126.14,
                  "confidence": 0.982
                },
                {
                  "text": "spots",
                  "start": 126.14,
                  "end": 126.72,
                  "confidence": 0.993
                },
                {
                  "text": "equaling",
                  "start": 126.72,
                  "end": 127.26,
                  "confidence": 0.958
                },
                {
                  "text": "a",
                  "start": 127.26,
                  "end": 127.44,
                  "confidence": 0.994
                },
                {
                  "text": "buffer",
                  "start": 127.44,
                  "end": 127.74,
                  "confidence": 0.999
                },
                {
                  "text": "zone",
                  "start": 127.74,
                  "end": 128.04,
                  "confidence": 0.993
                },
                {
                  "text": "of",
                  "start": 128.04,
                  "end": 128.22,
                  "confidence": 0.992
                },
                {
                  "text": "approximately",
                  "start": 128.22,
                  "end": 128.7,
                  "confidence": 0.985
                }
              ]
            },
            {
              "id": 33,
              "start": 129.74,
              "end": 138.23,
              "text": " 207,000 hectares which are called the coffee cultural landscape were considered a UNESCO World Heritage Site and also in",
              "no_speech_prob": 0.00034109604894183576,
              "confidence": 0.93,
              "words": [
                {
                  "text": "207,000",
                  "start": 129.74,
                  "end": 130.76,
                  "confidence": 0.975
                },
                {
                  "text": "hectares",
                  "start": 130.76,
                  "end": 131.32,
                  "confidence": 0.948
                },
                {
                  "text": "which",
                  "start": 131.32,
                  "end": 131.82,
                  "confidence": 0.866
                },
                {
                  "text": "are",
                  "start": 131.82,
                  "end": 132.08,
                  "confidence": 0.999
                },
                {
                  "text": "called",
                  "start": 132.08,
                  "end": 132.48,
                  "confidence": 0.999
                },
                {
                  "text": "the",
                  "start": 132.48,
                  "end": 132.72,
                  "confidence": 0.994
                },
                {
                  "text": "coffee",
                  "start": 132.72,
                  "end": 133.14,
                  "confidence": 0.976
                },
                {
                  "text": "cultural",
                  "start": 133.14,
                  "end": 133.58,
                  "confidence": 0.981
                },
                {
                  "text": "landscape",
                  "start": 133.58,
                  "end": 134.24,
                  "confidence": 0.957
                },
                {
                  "text": "were",
                  "start": 134.24,
                  "end": 134.62,
                  "confidence": 0.821
                },
                {
                  "text": "considered",
                  "start": 134.62,
                  "end": 135.18,
                  "confidence": 0.99
                },
                {
                  "text": "a",
                  "start": 135.18,
                  "end": 135.44,
                  "confidence": 0.997
                },
                {
                  "text": "UNESCO",
                  "start": 135.44,
                  "end": 135.88,
                  "confidence": 0.887
                },
                {
                  "text": "World",
                  "start": 135.88,
                  "end": 136.2,
                  "confidence": 0.944
                },
                {
                  "text": "Heritage",
                  "start": 136.2,
                  "end": 136.72,
                  "confidence": 0.993
                },
                {
                  "text": "Site",
                  "start": 136.72,
                  "end": 137.22,
                  "confidence": 0.681
                },
                {
                  "text": "and",
                  "start": 137.22,
                  "end": 137.76,
                  "confidence": 0.937
                },
                {
                  "text": "also",
                  "start": 137.76,
                  "end": 138.06,
                  "confidence": 0.725
                },
                {
                  "text": "in",
                  "start": 138.06,
                  "end": 138.23,
                  "confidence": 0.983
                }
              ]
            },
            {
              "id": 34,
              "start": 138.23,
              "end": 145.69,
              "text": " 2007 the EU the European Union granted Colombian coffee a protected designation of origin status",
              "no_speech_prob": 0.00034109604894183576,
              "confidence": 0.951,
              "words": [
                {
                  "text": "2007",
                  "start": 138.23,
                  "end": 139.06,
                  "confidence": 0.995
                },
                {
                  "text": "the",
                  "start": 139.06,
                  "end": 139.36,
                  "confidence": 0.986
                },
                {
                  "text": "EU",
                  "start": 139.36,
                  "end": 139.8,
                  "confidence": 0.97
                },
                {
                  "text": "the",
                  "start": 139.8,
                  "end": 139.96,
                  "confidence": 0.992
                },
                {
                  "text": "European",
                  "start": 139.96,
                  "end": 140.42,
                  "confidence": 0.995
                },
                {
                  "text": "Union",
                  "start": 140.42,
                  "end": 140.74,
                  "confidence": 0.997
                },
                {
                  "text": "granted",
                  "start": 140.74,
                  "end": 141.28,
                  "confidence": 0.993
                },
                {
                  "text": "Colombian",
                  "start": 141.28,
                  "end": 141.92,
                  "confidence": 0.926
                },
                {
                  "text": "coffee",
                  "start": 141.92,
                  "end": 142.32,
                  "confidence": 0.977
                },
                {
                  "text": "a",
                  "start": 142.32,
                  "end": 142.78,
                  "confidence": 0.993
                },
                {
                  "text": "protected",
                  "start": 142.78,
                  "end": 143.34,
                  "confidence": 0.863
                },
                {
                  "text": "designation",
                  "start": 143.34,
                  "end": 144.18,
                  "confidence": 0.771
                },
                {
                  "text": "of",
                  "start": 144.18,
                  "end": 144.56,
                  "confidence": 0.989
                },
                {
                  "text": "origin",
                  "start": 144.56,
                  "end": 145.08,
                  "confidence": 0.912
                },
                {
                  "text": "status",
                  "start": 145.08,
                  "end": 145.69,
                  "confidence": 0.956
                }
              ]
            },
            {
              "id": 35,
              "start": 145.69,
              "end": 153.12,
              "text": " Now interesting enough when it comes to the coffee in Colombia, believe it or not. It is not actually native to the country",
              "no_speech_prob": 3.955722149839858e-06,
              "confidence": 0.948,
              "words": [
                {
                  "text": "Now",
                  "start": 145.69,
                  "end": 146.26,
                  "confidence": 0.433
                },
                {
                  "text": "interesting",
                  "start": 146.26,
                  "end": 146.66,
                  "confidence": 0.905
                },
                {
                  "text": "enough",
                  "start": 146.66,
                  "end": 146.96,
                  "confidence": 0.996
                },
                {
                  "text": "when",
                  "start": 146.96,
                  "end": 147.12,
                  "confidence": 0.989
                },
                {
                  "text": "it",
                  "start": 147.12,
                  "end": 147.26,
                  "confidence": 0.999
                },
                {
                  "text": "comes",
                  "start": 147.26,
                  "end": 147.5,
                  "confidence": 1.0
                },
                {
                  "text": "to",
                  "start": 147.5,
                  "end": 147.64,
                  "confidence": 0.999
                },
                {
                  "text": "the",
                  "start": 147.64,
                  "end": 147.8,
                  "confidence": 0.998
                },
                {
                  "text": "coffee",
                  "start": 147.8,
                  "end": 148.22,
                  "confidence": 0.992
                },
                {
                  "text": "in",
                  "start": 148.22,
                  "end": 148.56,
                  "confidence": 0.997
                },
                {
                  "text": "Colombia,",
                  "start": 148.56,
                  "end": 149.14,
                  "confidence": 0.927
                },
                {
                  "text": "believe",
                  "start": 149.42,
                  "end": 149.52,
                  "confidence": 0.991
                },
                {
                  "text": "it",
                  "start": 149.52,
                  "end": 149.68,
                  "confidence": 0.999
                },
                {
                  "text": "or",
                  "start": 149.68,
                  "end": 149.8,
                  "confidence": 0.999
                },
                {
                  "text": "not.",
                  "start": 149.8,
                  "end": 150.04,
                  "confidence": 1.0
                },
                {
                  "text": "It",
                  "start": 150.14,
                  "end": 150.24,
                  "confidence": 0.996
                },
                {
                  "text": "is",
                  "start": 150.24,
                  "end": 150.5,
                  "confidence": 0.999
                },
                {
                  "text": "not",
                  "start": 150.5,
                  "end": 151.1,
                  "confidence": 0.994
                },
                {
                  "text": "actually",
                  "start": 151.1,
                  "end": 151.8,
                  "confidence": 0.88
                },
                {
                  "text": "native",
                  "start": 151.8,
                  "end": 152.32,
                  "confidence": 0.96
                },
                {
                  "text": "to",
                  "start": 152.32,
                  "end": 152.56,
                  "confidence": 0.999
                },
                {
                  "text": "the",
                  "start": 152.56,
                  "end": 152.72,
                  "confidence": 0.999
                },
                {
                  "text": "country",
                  "start": 152.72,
                  "end": 153.12,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 36,
              "start": 153.54,
              "end": 158.38,
              "text": " It's come from somewhere else not really an invasive species because it's very much welcomed",
              "no_speech_prob": 3.955722149839858e-06,
              "confidence": 0.932,
              "words": [
                {
                  "text": "It's",
                  "start": 153.54,
                  "end": 153.76,
                  "confidence": 0.968
                },
                {
                  "text": "come",
                  "start": 153.76,
                  "end": 153.94,
                  "confidence": 0.998
                },
                {
                  "text": "from",
                  "start": 153.94,
                  "end": 154.16,
                  "confidence": 0.999
                },
                {
                  "text": "somewhere",
                  "start": 154.16,
                  "end": 154.54,
                  "confidence": 0.998
                },
                {
                  "text": "else",
                  "start": 154.54,
                  "end": 155.04,
                  "confidence": 0.996
                },
                {
                  "text": "not",
                  "start": 155.04,
                  "end": 155.46,
                  "confidence": 0.345
                },
                {
                  "text": "really",
                  "start": 155.46,
                  "end": 155.66,
                  "confidence": 0.999
                },
                {
                  "text": "an",
                  "start": 155.66,
                  "end": 155.8,
                  "confidence": 0.997
                },
                {
                  "text": "invasive",
                  "start": 155.8,
                  "end": 156.24,
                  "confidence": 0.999
                },
                {
                  "text": "species",
                  "start": 156.24,
                  "end": 156.76,
                  "confidence": 0.998
                },
                {
                  "text": "because",
                  "start": 156.76,
                  "end": 157.1,
                  "confidence": 0.984
                },
                {
                  "text": "it's",
                  "start": 157.1,
                  "end": 157.4,
                  "confidence": 0.999
                },
                {
                  "text": "very",
                  "start": 157.4,
                  "end": 157.7,
                  "confidence": 0.999
                },
                {
                  "text": "much",
                  "start": 157.7,
                  "end": 157.98,
                  "confidence": 0.999
                },
                {
                  "text": "welcomed",
                  "start": 157.98,
                  "end": 158.38,
                  "confidence": 0.969
                }
              ]
            },
            {
              "id": 37,
              "start": 158.84,
              "end": 162.84,
              "text": " Now you may have also seen this guy on many different Colombian coffee brands",
              "no_speech_prob": 3.955722149839858e-06,
              "confidence": 0.984,
              "words": [
                {
                  "text": "Now",
                  "start": 158.84,
                  "end": 158.96,
                  "confidence": 0.875
                },
                {
                  "text": "you",
                  "start": 158.96,
                  "end": 159.1,
                  "confidence": 0.971
                },
                {
                  "text": "may",
                  "start": 159.1,
                  "end": 159.28,
                  "confidence": 0.998
                },
                {
                  "text": "have",
                  "start": 159.28,
                  "end": 159.42,
                  "confidence": 0.999
                },
                {
                  "text": "also",
                  "start": 159.42,
                  "end": 159.8,
                  "confidence": 0.999
                },
                {
                  "text": "seen",
                  "start": 159.8,
                  "end": 160.14,
                  "confidence": 0.999
                },
                {
                  "text": "this",
                  "start": 160.14,
                  "end": 160.4,
                  "confidence": 0.999
                },
                {
                  "text": "guy",
                  "start": 160.4,
                  "end": 160.7,
                  "confidence": 0.998
                },
                {
                  "text": "on",
                  "start": 160.7,
                  "end": 160.92,
                  "confidence": 0.999
                },
                {
                  "text": "many",
                  "start": 160.92,
                  "end": 161.1,
                  "confidence": 0.998
                },
                {
                  "text": "different",
                  "start": 161.1,
                  "end": 161.4,
                  "confidence": 0.998
                },
                {
                  "text": "Colombian",
                  "start": 161.4,
                  "end": 162.06,
                  "confidence": 0.975
                },
                {
                  "text": "coffee",
                  "start": 162.06,
                  "end": 162.46,
                  "confidence": 0.993
                },
                {
                  "text": "brands",
                  "start": 162.46,
                  "end": 162.84,
                  "confidence": 0.989
                }
              ]
            },
            {
              "id": 38,
              "start": 162.88,
              "end": 169.02,
              "text": " Now his name is Juan Valdez. Now some people think that this guy is actually real. He's a real coffee farmer",
              "no_speech_prob": 3.955722149839858e-06,
              "confidence": 0.929,
              "words": [
                {
                  "text": "Now",
                  "start": 162.88,
                  "end": 163.06,
                  "confidence": 0.955
                },
                {
                  "text": "his",
                  "start": 163.06,
                  "end": 163.24,
                  "confidence": 0.888
                },
                {
                  "text": "name",
                  "start": 163.24,
                  "end": 163.5,
                  "confidence": 1.0
                },
                {
                  "text": "is",
                  "start": 163.5,
                  "end": 163.74,
                  "confidence": 0.999
                },
                {
                  "text": "Juan",
                  "start": 163.74,
                  "end": 164.08,
                  "confidence": 0.872
                },
                {
                  "text": "Valdez.",
                  "start": 164.08,
                  "end": 164.7,
                  "confidence": 0.987
                },
                {
                  "text": "Now",
                  "start": 164.78,
                  "end": 164.88,
                  "confidence": 0.989
                },
                {
                  "text": "some",
                  "start": 164.88,
                  "end": 165.04,
                  "confidence": 0.396
                },
                {
                  "text": "people",
                  "start": 165.04,
                  "end": 165.28,
                  "confidence": 1.0
                },
                {
                  "text": "think",
                  "start": 165.28,
                  "end": 165.6,
                  "confidence": 1.0
                },
                {
                  "text": "that",
                  "start": 165.6,
                  "end": 165.76,
                  "confidence": 0.999
                },
                {
                  "text": "this",
                  "start": 165.76,
                  "end": 166.0,
                  "confidence": 1.0
                },
                {
                  "text": "guy",
                  "start": 166.0,
                  "end": 166.26,
                  "confidence": 0.999
                },
                {
                  "text": "is",
                  "start": 166.26,
                  "end": 166.42,
                  "confidence": 0.999
                },
                {
                  "text": "actually",
                  "start": 166.42,
                  "end": 166.92,
                  "confidence": 0.996
                },
                {
                  "text": "real.",
                  "start": 166.92,
                  "end": 167.4,
                  "confidence": 0.63
                },
                {
                  "text": "He's",
                  "start": 167.48,
                  "end": 167.64,
                  "confidence": 0.999
                },
                {
                  "text": "a",
                  "start": 167.64,
                  "end": 167.76,
                  "confidence": 1.0
                },
                {
                  "text": "real",
                  "start": 167.76,
                  "end": 168.02,
                  "confidence": 0.999
                },
                {
                  "text": "coffee",
                  "start": 168.02,
                  "end": 168.52,
                  "confidence": 0.998
                },
                {
                  "text": "farmer",
                  "start": 168.52,
                  "end": 169.02,
                  "confidence": 0.995
                }
              ]
            },
            {
              "id": 39,
              "start": 169.04,
              "end": 170.02,
              "text": " Somebody just drew",
              "no_speech_prob": 3.955722149839858e-06,
              "confidence": 0.784,
              "words": [
                {
                  "text": "Somebody",
                  "start": 169.04,
                  "end": 169.46,
                  "confidence": 0.604
                },
                {
                  "text": "just",
                  "start": 169.46,
                  "end": 169.74,
                  "confidence": 0.989
                },
                {
                  "text": "drew",
                  "start": 169.74,
                  "end": 170.02,
                  "confidence": 0.806
                }
              ]
            }
          ]
        }
      ],
      "process_output_files": [
        "../../../data/output/f2225a00-7174-4298-a4bc-541e1b360b1b.json"
      ]
    }



```python
# delete all processed datapoints belonging to this pipeline

reset_pipeline(pipeline_1)
```
