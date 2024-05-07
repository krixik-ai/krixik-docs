## The `transcribe` module

This document reviews the `transcribe` module - which takes as input an audio or video file and returns a transcription of spoken words made in the input.  Transcription data is returned as a json.

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [required input format](#required-input-format)
- [using the default model](#using-the-default-model)
- [using a non-default model](#using-a-non-default-model)


```python
# import utilities
import sys
import json
import importlib

sys.path.append("../../")
reset = importlib.import_module("utilities.reset")
reset_pipeline = reset.reset_pipeline

# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os

load_dotenv("../../.env")
MY_API_KEY = os.getenv("MY_API_KEY")
MY_API_URL = os.getenv("MY_API_URL")

# import krixik and initialize it with your personal secrets
from krixik import krixik

krixik.init(api_key=MY_API_KEY, api_url=MY_API_URL)
```

    SUCCESS: You are now authenticated.


## Pipeline setup

Below we setup a simple one module pipeline using the `transcribe` module. 

We do this by passing the module name to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(
    name="modules-transcribe-docs", module_chain=["transcribe"]
)
```

The `transcribe` module comes with the current range of [whisper](https://openai.com/research/whisper) transcription models.  These range from tiny to large, and offer a trade-off of transcription accuracy versus computational cost, with smaller models being less accurate but cheaper to run.  

- [`whisper-tiny`](https://huggingface.co/openai/whisper-tiny): the smallest model, cheapest to run, but least accurate (default)
- [`whisper-base`](https://huggingface.co/openai/whisper-base): about 2x model parameters compared to tiny - small, cheap to turn, reasonably accurate 
- [`whisper-small`](https://huggingface.co/openai/whisper-small): about 3x model parameters compared to base - cheap to run, accurate 
- [`whisper-medium`](https://huggingface.co/openai/whisper-medium): about 3x model parameters compared to small - more costly to run, accurate
- [`whisper-large-v3`](https://huggingface.co/openai/whisper-large-v3): about 2x model parameters compared to medium - most costly to run, most accurate

These available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```

## Required input format

The `transcribe` module accepts `.mp3` audio files, and `.mp4` video files. `.mp4` files have their audio extracted and saved as `.mp3` files locally before server-side processing.

Lets take a quick look at a valid input file - and then process it.


```python
# examine contents of a valid input file
test_file = "../../data/input/Interesting Facts About Colombia.mp4"
from IPython.display import Video

Video(test_file)
```




<video src="../../data/input/Interesting Facts About Colombia.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



## Using the default model

Now let's process it using the default model - `whisper-tiny`.  Because `whisper-tiny` is the default model we need not input the optional `modules` argument into `.process`.


```python
# define path to an input file
test_file = "../../data/input/Interesting Facts About Colombia.mp4"

# process for search
process_output = pipeline.process(
    local_file_path=test_file,
    local_save_directory="../../data/output",  # save output repo data output subdir
    expire_time=60 * 10,  # set all process data to expire in 10 minutes
    wait_for_process=True,  # wait for process to complete before regaining ide
    verbose=False,
)  # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is json, the process output is provided in this object as well.  The output file itself has been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "modules-transcribe-docs",
      "request_id": "e9408bc0-a12f-4366-a168-bfed0b22dad4",
      "file_id": "cd5f2dad-f63b-46ed-8076-c0499cae8e5f",
      "message": "SUCCESS - output fetched for file_id cd5f2dad-f63b-46ed-8076-c0499cae8e5f.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "transcript": " That's the episode looking at the great country of Columbia. We looked at some really basic facts. It's name, a bit of its history, the type of people that live there, land size, and all that jazz. But in this video, we're going to go into a little bit more of a detailed look. Yo, what is going on guys? Welcome back to F2D facts. The channel where I look at people cultures and places. My name is Dave Wouple, and today we are going to be looking more at Columbia and our Columbia part two video. Which just reminds me guys, this is part of our Columbia playlist. So put it down in the description box below, and I'll talk about that more in the video. But if you're new here, join me every single Monday to learn about new countries from around the world. You can do that by hitting that subscribe and that belt notification button. But let's get started. Learn about Columbia. So we all know Columbia is famous for its coffee, right? Yes, right. I know. You guys are sitting there going, five bucks says he's going to talk about coffee. Well, I am. That's right, because I got my van. You Columbia coffee right here. Boom advertisement. Yeah. Then I'm paying me for this. I'm care. So which might not know about coffee is yes, you probably already know that a lot of companies actually buy it up. Starbucks buys all had a coffee from Columbia. It's kind of like their favorite place to buy coffee. And kind of to pay tribute to that Starbucks when they're making their 1,000th store in 2016, they decided, yo, we're going to put it in Columbia. And this was in the town of Medellin, Columbia. Now here's the thing, when it comes to coffee in Columbia, they are the third largest producing and exporting coffee country in the world. The amount of coffee that is exported from Columbia equals about 810,000 metric tons or approximately 11.5 million bags. However, although it might be beaten by countries like Brazil, it is actually the number one or highest country for producing and growing a specific type of bean known as the Arab Beka bean. And I know coffee is really important when it comes to talking about Columbia, but you guys really don't know how important it is with its culture. Interesting fact that in 2007, major spots equaling a buffer zone of approximately 207,000 hectares, which are called the coffee cultural landscape, were considered a UNESCO World Heritage Site. And also in 2007, the EU, the European Union, granted Colombian coffee a protected designation of origin status. Now interesting enough when it comes to the coffee in Columbia, believe it or not, it is not actually native to the country. It's come from somewhere else, not really an invasive species because it's very much welcomed. Now you may have also seen this guy on many different Colombian coffee brands. Now his name is Juan Valdez. Now some people think that this guy is actually really a real coffee farmer, somebody just drew.",
          "timestamped_transcript": [
            {
              "id": 0,
              "start": 0.0,
              "end": 2.12,
              "text": " That's the episode looking at the great country of Columbia.",
              "no_speech_prob": 0.5627443194389343,
              "confidence": 0.547,
              "words": [
                {
                  "text": "That's",
                  "start": 0.0,
                  "end": 0.38,
                  "confidence": 0.234
                },
                {
                  "text": "the",
                  "start": 0.38,
                  "end": 0.4,
                  "confidence": 0.461
                },
                {
                  "text": "episode",
                  "start": 0.4,
                  "end": 0.5,
                  "confidence": 0.104
                },
                {
                  "text": "looking",
                  "start": 0.5,
                  "end": 0.8,
                  "confidence": 0.861
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
                  "confidence": 0.98
                },
                {
                  "text": "great",
                  "start": 1.1,
                  "end": 1.32,
                  "confidence": 0.975
                },
                {
                  "text": "country",
                  "start": 1.32,
                  "end": 1.66,
                  "confidence": 0.985
                },
                {
                  "text": "of",
                  "start": 1.66,
                  "end": 1.78,
                  "confidence": 0.982
                },
                {
                  "text": "Columbia.",
                  "start": 1.78,
                  "end": 2.12,
                  "confidence": 0.624
                }
              ]
            },
            {
              "id": 1,
              "start": 2.18,
              "end": 4.34,
              "text": " We looked at some really basic facts.",
              "no_speech_prob": 0.5627443194389343,
              "confidence": 0.906,
              "words": [
                {
                  "text": "We",
                  "start": 2.18,
                  "end": 2.34,
                  "confidence": 0.994
                },
                {
                  "text": "looked",
                  "start": 2.34,
                  "end": 2.6,
                  "confidence": 0.983
                },
                {
                  "text": "at",
                  "start": 2.6,
                  "end": 2.78,
                  "confidence": 0.998
                },
                {
                  "text": "some",
                  "start": 2.78,
                  "end": 3.0,
                  "confidence": 0.996
                },
                {
                  "text": "really",
                  "start": 3.0,
                  "end": 3.28,
                  "confidence": 0.988
                },
                {
                  "text": "basic",
                  "start": 3.28,
                  "end": 3.88,
                  "confidence": 0.527
                },
                {
                  "text": "facts.",
                  "start": 3.88,
                  "end": 4.34,
                  "confidence": 0.992
                }
              ]
            },
            {
              "id": 2,
              "start": 4.34,
              "end": 6.8,
              "text": " It's name, a bit of its history, the type of people",
              "no_speech_prob": 0.5627443194389343,
              "confidence": 0.905,
              "words": [
                {
                  "text": "It's",
                  "start": 4.34,
                  "end": 4.6,
                  "confidence": 0.899
                },
                {
                  "text": "name,",
                  "start": 4.6,
                  "end": 4.94,
                  "confidence": 0.939
                },
                {
                  "text": "a",
                  "start": 4.96,
                  "end": 5.08,
                  "confidence": 0.981
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
                  "confidence": 0.896
                },
                {
                  "text": "history,",
                  "start": 5.48,
                  "end": 5.9,
                  "confidence": 0.999
                },
                {
                  "text": "the",
                  "start": 6.02,
                  "end": 6.38,
                  "confidence": 0.494
                },
                {
                  "text": "type",
                  "start": 6.38,
                  "end": 6.52,
                  "confidence": 0.974
                },
                {
                  "text": "of",
                  "start": 6.52,
                  "end": 6.62,
                  "confidence": 0.963
                },
                {
                  "text": "people",
                  "start": 6.62,
                  "end": 6.8,
                  "confidence": 0.994
                }
              ]
            },
            {
              "id": 3,
              "start": 6.84,
              "end": 9.22,
              "text": " that live there, land size, and all that jazz.",
              "no_speech_prob": 0.5627443194389343,
              "confidence": 0.872,
              "words": [
                {
                  "text": "that",
                  "start": 6.84,
                  "end": 6.98,
                  "confidence": 0.999
                },
                {
                  "text": "live",
                  "start": 6.98,
                  "end": 7.22,
                  "confidence": 0.607
                },
                {
                  "text": "there,",
                  "start": 7.22,
                  "end": 7.46,
                  "confidence": 0.946
                },
                {
                  "text": "land",
                  "start": 7.54,
                  "end": 7.86,
                  "confidence": 0.695
                },
                {
                  "text": "size,",
                  "start": 7.86,
                  "end": 8.28,
                  "confidence": 0.767
                },
                {
                  "text": "and",
                  "start": 8.32,
                  "end": 8.44,
                  "confidence": 0.984
                },
                {
                  "text": "all",
                  "start": 8.44,
                  "end": 8.68,
                  "confidence": 0.998
                },
                {
                  "text": "that",
                  "start": 8.68,
                  "end": 8.86,
                  "confidence": 0.974
                },
                {
                  "text": "jazz.",
                  "start": 8.86,
                  "end": 9.22,
                  "confidence": 0.994
                }
              ]
            },
            {
              "id": 4,
              "start": 9.52,
              "end": 11.61,
              "text": " But in this video, we're going to go into a little bit more",
              "no_speech_prob": 0.5627443194389343,
              "confidence": 0.896,
              "words": [
                {
                  "text": "But",
                  "start": 9.52,
                  "end": 9.64,
                  "confidence": 0.998
                },
                {
                  "text": "in",
                  "start": 9.64,
                  "end": 9.72,
                  "confidence": 0.992
                },
                {
                  "text": "this",
                  "start": 9.72,
                  "end": 9.84,
                  "confidence": 0.999
                },
                {
                  "text": "video,",
                  "start": 9.84,
                  "end": 10.08,
                  "confidence": 0.999
                },
                {
                  "text": "we're",
                  "start": 10.1,
                  "end": 10.24,
                  "confidence": 0.992
                },
                {
                  "text": "going",
                  "start": 10.24,
                  "end": 10.34,
                  "confidence": 0.501
                },
                {
                  "text": "to",
                  "start": 10.34,
                  "end": 10.4,
                  "confidence": 0.952
                },
                {
                  "text": "go",
                  "start": 10.4,
                  "end": 10.48,
                  "confidence": 0.978
                },
                {
                  "text": "into",
                  "start": 10.48,
                  "end": 10.7,
                  "confidence": 0.941
                },
                {
                  "text": "a",
                  "start": 10.7,
                  "end": 10.9,
                  "confidence": 0.647
                },
                {
                  "text": "little",
                  "start": 10.9,
                  "end": 11.14,
                  "confidence": 0.925
                },
                {
                  "text": "bit",
                  "start": 11.14,
                  "end": 11.3,
                  "confidence": 0.968
                },
                {
                  "text": "more",
                  "start": 11.3,
                  "end": 11.61,
                  "confidence": 0.872
                }
              ]
            },
            {
              "id": 5,
              "start": 11.61,
              "end": 12.56,
              "text": " of a detailed look.",
              "no_speech_prob": 0.5627443194389343,
              "confidence": 0.997,
              "words": [
                {
                  "text": "of",
                  "start": 11.61,
                  "end": 11.76,
                  "confidence": 0.999
                },
                {
                  "text": "a",
                  "start": 11.76,
                  "end": 11.88,
                  "confidence": 0.994
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
                  "confidence": 0.997
                }
              ]
            },
            {
              "id": 6,
              "start": 12.82,
              "end": 14.28,
              "text": " Yo, what is going on guys?",
              "no_speech_prob": 0.5627443194389343,
              "confidence": 0.899,
              "words": [
                {
                  "text": "Yo,",
                  "start": 12.82,
                  "end": 13.02,
                  "confidence": 0.843
                },
                {
                  "text": "what",
                  "start": 13.22,
                  "end": 13.34,
                  "confidence": 0.995
                },
                {
                  "text": "is",
                  "start": 13.34,
                  "end": 13.48,
                  "confidence": 0.985
                },
                {
                  "text": "going",
                  "start": 13.48,
                  "end": 13.7,
                  "confidence": 0.979
                },
                {
                  "text": "on",
                  "start": 13.7,
                  "end": 13.9,
                  "confidence": 1.0
                },
                {
                  "text": "guys?",
                  "start": 13.9,
                  "end": 14.28,
                  "confidence": 0.651
                }
              ]
            },
            {
              "id": 7,
              "start": 14.34,
              "end": 15.7,
              "text": " Welcome back to F2D facts.",
              "no_speech_prob": 0.5627443194389343,
              "confidence": 0.703,
              "words": [
                {
                  "text": "Welcome",
                  "start": 14.34,
                  "end": 14.6,
                  "confidence": 0.988
                },
                {
                  "text": "back",
                  "start": 14.6,
                  "end": 14.82,
                  "confidence": 0.999
                },
                {
                  "text": "to",
                  "start": 14.82,
                  "end": 14.98,
                  "confidence": 0.988
                },
                {
                  "text": "F2D",
                  "start": 14.98,
                  "end": 15.4,
                  "confidence": 0.603
                },
                {
                  "text": "facts.",
                  "start": 15.4,
                  "end": 15.7,
                  "confidence": 0.397
                }
              ]
            },
            {
              "id": 8,
              "start": 15.7,
              "end": 17.33,
              "text": " The channel where I look at people cultures and places.",
              "no_speech_prob": 0.5627443194389343,
              "confidence": 0.843,
              "words": [
                {
                  "text": "The",
                  "start": 15.7,
                  "end": 15.86,
                  "confidence": 0.557
                },
                {
                  "text": "channel",
                  "start": 15.86,
                  "end": 16.02,
                  "confidence": 0.887
                },
                {
                  "text": "where",
                  "start": 16.02,
                  "end": 16.16,
                  "confidence": 0.992
                },
                {
                  "text": "I",
                  "start": 16.16,
                  "end": 16.24,
                  "confidence": 0.991
                },
                {
                  "text": "look",
                  "start": 16.24,
                  "end": 16.36,
                  "confidence": 0.995
                },
                {
                  "text": "at",
                  "start": 16.36,
                  "end": 16.46,
                  "confidence": 0.992
                },
                {
                  "text": "people",
                  "start": 16.46,
                  "end": 16.64,
                  "confidence": 0.961
                },
                {
                  "text": "cultures",
                  "start": 16.64,
                  "end": 16.98,
                  "confidence": 0.569
                },
                {
                  "text": "and",
                  "start": 16.98,
                  "end": 17.14,
                  "confidence": 0.692
                },
                {
                  "text": "places.",
                  "start": 17.14,
                  "end": 17.33,
                  "confidence": 0.995
                }
              ]
            },
            {
              "id": 9,
              "start": 17.33,
              "end": 22.38,
              "text": " My name is Dave Wouple, and today we are going to be",
              "no_speech_prob": 0.5627443194389343,
              "confidence": 0.75,
              "words": [
                {
                  "text": "My",
                  "start": 17.33,
                  "end": 17.84,
                  "confidence": 0.994
                },
                {
                  "text": "name",
                  "start": 17.84,
                  "end": 18.62,
                  "confidence": 1.0
                },
                {
                  "text": "is",
                  "start": 18.62,
                  "end": 18.98,
                  "confidence": 0.99
                },
                {
                  "text": "Dave",
                  "start": 18.98,
                  "end": 19.38,
                  "confidence": 0.986
                },
                {
                  "text": "Wouple,",
                  "start": 19.38,
                  "end": 19.98,
                  "confidence": 0.399
                },
                {
                  "text": "and",
                  "start": 20.04,
                  "end": 20.38,
                  "confidence": 0.964
                },
                {
                  "text": "today",
                  "start": 20.38,
                  "end": 21.06,
                  "confidence": 0.996
                },
                {
                  "text": "we",
                  "start": 21.06,
                  "end": 21.64,
                  "confidence": 0.779
                },
                {
                  "text": "are",
                  "start": 21.64,
                  "end": 22.06,
                  "confidence": 0.928
                },
                {
                  "text": "going",
                  "start": 22.06,
                  "end": 22.2,
                  "confidence": 0.656
                },
                {
                  "text": "to",
                  "start": 22.2,
                  "end": 22.24,
                  "confidence": 0.636
                },
                {
                  "text": "be",
                  "start": 22.24,
                  "end": 22.38,
                  "confidence": 0.99
                }
              ]
            },
            {
              "id": 10,
              "start": 22.38,
              "end": 25.22,
              "text": " looking more at Columbia and our Columbia part two video.",
              "no_speech_prob": 0.5627443194389343,
              "confidence": 0.728,
              "words": [
                {
                  "text": "looking",
                  "start": 22.38,
                  "end": 22.62,
                  "confidence": 0.997
                },
                {
                  "text": "more",
                  "start": 22.62,
                  "end": 22.96,
                  "confidence": 0.972
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
                  "confidence": 0.98
                },
                {
                  "text": "and",
                  "start": 23.64,
                  "end": 23.86,
                  "confidence": 0.393
                },
                {
                  "text": "our",
                  "start": 23.86,
                  "end": 24.02,
                  "confidence": 0.584
                },
                {
                  "text": "Columbia",
                  "start": 24.02,
                  "end": 24.24,
                  "confidence": 0.982
                },
                {
                  "text": "part",
                  "start": 24.24,
                  "end": 24.5,
                  "confidence": 0.391
                },
                {
                  "text": "two",
                  "start": 24.5,
                  "end": 24.8,
                  "confidence": 0.525
                },
                {
                  "text": "video.",
                  "start": 24.8,
                  "end": 25.22,
                  "confidence": 0.95
                }
              ]
            },
            {
              "id": 11,
              "start": 25.72,
              "end": 28.8,
              "text": " Which just reminds me guys, this is part of our Columbia playlist.",
              "no_speech_prob": 0.5627443194389343,
              "confidence": 0.909,
              "words": [
                {
                  "text": "Which",
                  "start": 25.72,
                  "end": 25.96,
                  "confidence": 0.988
                },
                {
                  "text": "just",
                  "start": 25.96,
                  "end": 26.24,
                  "confidence": 0.982
                },
                {
                  "text": "reminds",
                  "start": 26.24,
                  "end": 26.66,
                  "confidence": 0.996
                },
                {
                  "text": "me",
                  "start": 26.66,
                  "end": 26.86,
                  "confidence": 0.932
                },
                {
                  "text": "guys,",
                  "start": 26.86,
                  "end": 27.02,
                  "confidence": 0.878
                },
                {
                  "text": "this",
                  "start": 27.14,
                  "end": 27.24,
                  "confidence": 0.946
                },
                {
                  "text": "is",
                  "start": 27.24,
                  "end": 27.32,
                  "confidence": 0.976
                },
                {
                  "text": "part",
                  "start": 27.32,
                  "end": 27.54,
                  "confidence": 0.984
                },
                {
                  "text": "of",
                  "start": 27.54,
                  "end": 27.66,
                  "confidence": 0.886
                },
                {
                  "text": "our",
                  "start": 27.66,
                  "end": 27.82,
                  "confidence": 0.98
                },
                {
                  "text": "Columbia",
                  "start": 27.82,
                  "end": 28.24,
                  "confidence": 0.989
                },
                {
                  "text": "playlist.",
                  "start": 28.24,
                  "end": 28.8,
                  "confidence": 0.516
                }
              ]
            },
            {
              "id": 12,
              "start": 28.92,
              "end": 30.91,
              "text": " So put it down in the description box below, and I'll talk about",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.773,
              "words": [
                {
                  "text": "So",
                  "start": 28.92,
                  "end": 28.98,
                  "confidence": 0.384
                },
                {
                  "text": "put",
                  "start": 28.98,
                  "end": 29.06,
                  "confidence": 0.595
                },
                {
                  "text": "it",
                  "start": 29.06,
                  "end": 29.18,
                  "confidence": 0.992
                },
                {
                  "text": "down",
                  "start": 29.18,
                  "end": 29.38,
                  "confidence": 0.997
                },
                {
                  "text": "in",
                  "start": 29.38,
                  "end": 29.52,
                  "confidence": 0.542
                },
                {
                  "text": "the",
                  "start": 29.52,
                  "end": 29.6,
                  "confidence": 0.876
                },
                {
                  "text": "description",
                  "start": 29.6,
                  "end": 29.84,
                  "confidence": 0.999
                },
                {
                  "text": "box",
                  "start": 29.84,
                  "end": 30.12,
                  "confidence": 0.984
                },
                {
                  "text": "below,",
                  "start": 30.12,
                  "end": 30.34,
                  "confidence": 0.99
                },
                {
                  "text": "and",
                  "start": 30.44,
                  "end": 30.54,
                  "confidence": 0.542
                },
                {
                  "text": "I'll",
                  "start": 30.54,
                  "end": 30.64,
                  "confidence": 0.898
                },
                {
                  "text": "talk",
                  "start": 30.64,
                  "end": 30.8,
                  "confidence": 0.824
                },
                {
                  "text": "about",
                  "start": 30.8,
                  "end": 30.91,
                  "confidence": 0.721
                }
              ]
            },
            {
              "id": 13,
              "start": 30.91,
              "end": 32.3,
              "text": " that more in the video.",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.704,
              "words": [
                {
                  "text": "that",
                  "start": 30.91,
                  "end": 31.08,
                  "confidence": 0.912
                },
                {
                  "text": "more",
                  "start": 31.08,
                  "end": 31.28,
                  "confidence": 0.985
                },
                {
                  "text": "in",
                  "start": 31.28,
                  "end": 31.62,
                  "confidence": 0.422
                },
                {
                  "text": "the",
                  "start": 31.62,
                  "end": 31.84,
                  "confidence": 0.987
                },
                {
                  "text": "video.",
                  "start": 31.84,
                  "end": 32.3,
                  "confidence": 0.463
                }
              ]
            },
            {
              "id": 14,
              "start": 32.72,
              "end": 35.02,
              "text": " But if you're new here, join me every single Monday to learn",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.954,
              "words": [
                {
                  "text": "But",
                  "start": 32.72,
                  "end": 32.84,
                  "confidence": 0.99
                },
                {
                  "text": "if",
                  "start": 32.84,
                  "end": 32.94,
                  "confidence": 0.986
                },
                {
                  "text": "you're",
                  "start": 32.94,
                  "end": 33.1,
                  "confidence": 0.976
                },
                {
                  "text": "new",
                  "start": 33.1,
                  "end": 33.22,
                  "confidence": 0.995
                },
                {
                  "text": "here,",
                  "start": 33.22,
                  "end": 33.56,
                  "confidence": 0.995
                },
                {
                  "text": "join",
                  "start": 33.68,
                  "end": 33.92,
                  "confidence": 0.952
                },
                {
                  "text": "me",
                  "start": 33.92,
                  "end": 34.06,
                  "confidence": 0.998
                },
                {
                  "text": "every",
                  "start": 34.06,
                  "end": 34.24,
                  "confidence": 0.867
                },
                {
                  "text": "single",
                  "start": 34.24,
                  "end": 34.46,
                  "confidence": 0.997
                },
                {
                  "text": "Monday",
                  "start": 34.46,
                  "end": 34.7,
                  "confidence": 0.94
                },
                {
                  "text": "to",
                  "start": 34.7,
                  "end": 34.84,
                  "confidence": 0.857
                },
                {
                  "text": "learn",
                  "start": 34.84,
                  "end": 35.02,
                  "confidence": 0.887
                }
              ]
            },
            {
              "id": 15,
              "start": 35.02,
              "end": 36.38,
              "text": " about new countries from around the world.",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.992,
              "words": [
                {
                  "text": "about",
                  "start": 35.02,
                  "end": 35.18,
                  "confidence": 0.999
                },
                {
                  "text": "new",
                  "start": 35.18,
                  "end": 35.38,
                  "confidence": 0.994
                },
                {
                  "text": "countries",
                  "start": 35.38,
                  "end": 35.78,
                  "confidence": 0.993
                },
                {
                  "text": "from",
                  "start": 35.78,
                  "end": 35.96,
                  "confidence": 0.982
                },
                {
                  "text": "around",
                  "start": 35.96,
                  "end": 36.22,
                  "confidence": 0.996
                },
                {
                  "text": "the",
                  "start": 36.22,
                  "end": 36.34,
                  "confidence": 0.982
                },
                {
                  "text": "world.",
                  "start": 36.34,
                  "end": 36.38,
                  "confidence": 0.998
                }
              ]
            },
            {
              "id": 16,
              "start": 36.38,
              "end": 38.4,
              "text": " You can do that by hitting that subscribe and that belt",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.852,
              "words": [
                {
                  "text": "You",
                  "start": 36.38,
                  "end": 36.62,
                  "confidence": 0.991
                },
                {
                  "text": "can",
                  "start": 36.62,
                  "end": 36.72,
                  "confidence": 0.997
                },
                {
                  "text": "do",
                  "start": 36.72,
                  "end": 36.84,
                  "confidence": 0.999
                },
                {
                  "text": "that",
                  "start": 36.84,
                  "end": 36.96,
                  "confidence": 0.998
                },
                {
                  "text": "by",
                  "start": 36.96,
                  "end": 37.16,
                  "confidence": 0.962
                },
                {
                  "text": "hitting",
                  "start": 37.16,
                  "end": 37.36,
                  "confidence": 0.916
                },
                {
                  "text": "that",
                  "start": 37.36,
                  "end": 37.48,
                  "confidence": 0.994
                },
                {
                  "text": "subscribe",
                  "start": 37.48,
                  "end": 37.92,
                  "confidence": 0.96
                },
                {
                  "text": "and",
                  "start": 37.92,
                  "end": 38.12,
                  "confidence": 0.541
                },
                {
                  "text": "that",
                  "start": 38.12,
                  "end": 38.32,
                  "confidence": 0.886
                },
                {
                  "text": "belt",
                  "start": 38.32,
                  "end": 38.4,
                  "confidence": 0.432
                }
              ]
            },
            {
              "id": 17,
              "start": 38.4,
              "end": 39.23,
              "text": " notification button.",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.953,
              "words": [
                {
                  "text": "notification",
                  "start": 38.4,
                  "end": 39.02,
                  "confidence": 0.909
                },
                {
                  "text": "button.",
                  "start": 39.02,
                  "end": 39.23,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 18,
              "start": 39.23,
              "end": 41.5,
              "text": " But let's get started.",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.845,
              "words": [
                {
                  "text": "But",
                  "start": 39.23,
                  "end": 40.36,
                  "confidence": 0.996
                },
                {
                  "text": "let's",
                  "start": 40.36,
                  "end": 41.02,
                  "confidence": 0.664
                },
                {
                  "text": "get",
                  "start": 41.02,
                  "end": 41.18,
                  "confidence": 0.985
                },
                {
                  "text": "started.",
                  "start": 41.18,
                  "end": 41.5,
                  "confidence": 0.998
                }
              ]
            },
            {
              "id": 19,
              "start": 41.5,
              "end": 42.7,
              "text": " Learn about Columbia.",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.765,
              "words": [
                {
                  "text": "Learn",
                  "start": 41.5,
                  "end": 42.14,
                  "confidence": 0.489
                },
                {
                  "text": "about",
                  "start": 42.14,
                  "end": 42.32,
                  "confidence": 0.93
                },
                {
                  "text": "Columbia.",
                  "start": 42.32,
                  "end": 42.7,
                  "confidence": 0.986
                }
              ]
            },
            {
              "id": 20,
              "start": 43.24,
              "end": 46.6,
              "text": " So we all know Columbia is famous for its coffee, right?",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.903,
              "words": [
                {
                  "text": "So",
                  "start": 43.24,
                  "end": 43.36,
                  "confidence": 0.997
                },
                {
                  "text": "we",
                  "start": 43.36,
                  "end": 43.52,
                  "confidence": 0.968
                },
                {
                  "text": "all",
                  "start": 43.52,
                  "end": 43.68,
                  "confidence": 0.999
                },
                {
                  "text": "know",
                  "start": 43.68,
                  "end": 43.94,
                  "confidence": 0.999
                },
                {
                  "text": "Columbia",
                  "start": 43.94,
                  "end": 44.56,
                  "confidence": 0.453
                },
                {
                  "text": "is",
                  "start": 44.56,
                  "end": 44.86,
                  "confidence": 0.995
                },
                {
                  "text": "famous",
                  "start": 44.86,
                  "end": 45.22,
                  "confidence": 0.996
                },
                {
                  "text": "for",
                  "start": 45.22,
                  "end": 45.62,
                  "confidence": 0.999
                },
                {
                  "text": "its",
                  "start": 45.62,
                  "end": 45.8,
                  "confidence": 0.867
                },
                {
                  "text": "coffee,",
                  "start": 45.8,
                  "end": 46.26,
                  "confidence": 0.88
                },
                {
                  "text": "right?",
                  "start": 46.34,
                  "end": 46.6,
                  "confidence": 0.987
                }
              ]
            },
            {
              "id": 21,
              "start": 46.84,
              "end": 47.42,
              "text": " Yes, right.",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.983,
              "words": [
                {
                  "text": "Yes,",
                  "start": 46.84,
                  "end": 47.08,
                  "confidence": 0.989
                },
                {
                  "text": "right.",
                  "start": 47.28,
                  "end": 47.42,
                  "confidence": 0.978
                }
              ]
            },
            {
              "id": 22,
              "start": 47.54,
              "end": 47.75,
              "text": " I know.",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.975,
              "words": [
                {
                  "text": "I",
                  "start": 47.54,
                  "end": 47.72,
                  "confidence": 0.951
                },
                {
                  "text": "know.",
                  "start": 47.72,
                  "end": 47.75,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 23,
              "start": 47.75,
              "end": 49.87,
              "text": " You guys are sitting there going, five bucks says",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.831,
              "words": [
                {
                  "text": "You",
                  "start": 47.75,
                  "end": 48.14,
                  "confidence": 0.98
                },
                {
                  "text": "guys",
                  "start": 48.14,
                  "end": 48.28,
                  "confidence": 0.998
                },
                {
                  "text": "are",
                  "start": 48.28,
                  "end": 48.44,
                  "confidence": 0.89
                },
                {
                  "text": "sitting",
                  "start": 48.44,
                  "end": 48.62,
                  "confidence": 0.969
                },
                {
                  "text": "there",
                  "start": 48.62,
                  "end": 48.72,
                  "confidence": 0.973
                },
                {
                  "text": "going,",
                  "start": 48.72,
                  "end": 48.84,
                  "confidence": 0.948
                },
                {
                  "text": "five",
                  "start": 48.92,
                  "end": 49.5,
                  "confidence": 0.266
                },
                {
                  "text": "bucks",
                  "start": 49.5,
                  "end": 49.72,
                  "confidence": 0.976
                },
                {
                  "text": "says",
                  "start": 49.72,
                  "end": 49.87,
                  "confidence": 0.932
                }
              ]
            },
            {
              "id": 24,
              "start": 49.87,
              "end": 50.77,
              "text": " he's going to talk about coffee.",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.858,
              "words": [
                {
                  "text": "he's",
                  "start": 49.87,
                  "end": 50.02,
                  "confidence": 0.65
                },
                {
                  "text": "going",
                  "start": 50.02,
                  "end": 50.12,
                  "confidence": 0.847
                },
                {
                  "text": "to",
                  "start": 50.12,
                  "end": 50.22,
                  "confidence": 0.997
                },
                {
                  "text": "talk",
                  "start": 50.22,
                  "end": 50.38,
                  "confidence": 0.992
                },
                {
                  "text": "about",
                  "start": 50.38,
                  "end": 50.52,
                  "confidence": 0.998
                },
                {
                  "text": "coffee.",
                  "start": 50.52,
                  "end": 50.77,
                  "confidence": 0.968
                }
              ]
            },
            {
              "id": 25,
              "start": 50.77,
              "end": 51.8,
              "text": " Well, I am.",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.988,
              "words": [
                {
                  "text": "Well,",
                  "start": 50.77,
                  "end": 51.26,
                  "confidence": 0.996
                },
                {
                  "text": "I",
                  "start": 51.44,
                  "end": 51.58,
                  "confidence": 0.991
                },
                {
                  "text": "am.",
                  "start": 51.58,
                  "end": 51.8,
                  "confidence": 0.975
                }
              ]
            },
            {
              "id": 26,
              "start": 52.18,
              "end": 53.18,
              "text": " That's right, because I got my van.",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.986,
              "words": [
                {
                  "text": "That's",
                  "start": 52.18,
                  "end": 52.36,
                  "confidence": 0.998
                },
                {
                  "text": "right,",
                  "start": 52.36,
                  "end": 52.46,
                  "confidence": 0.999
                },
                {
                  "text": "because",
                  "start": 52.52,
                  "end": 52.68,
                  "confidence": 0.998
                },
                {
                  "text": "I",
                  "start": 52.68,
                  "end": 52.76,
                  "confidence": 0.996
                },
                {
                  "text": "got",
                  "start": 52.76,
                  "end": 52.9,
                  "confidence": 0.968
                },
                {
                  "text": "my",
                  "start": 52.9,
                  "end": 53.0,
                  "confidence": 0.997
                },
                {
                  "text": "van.",
                  "start": 53.0,
                  "end": 53.18,
                  "confidence": 0.934
                }
              ]
            },
            {
              "id": 27,
              "start": 53.18,
              "end": 54.92,
              "text": " You Columbia coffee right here.",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.615,
              "words": [
                {
                  "text": "You",
                  "start": 53.18,
                  "end": 53.62,
                  "confidence": 0.461
                },
                {
                  "text": "Columbia",
                  "start": 53.62,
                  "end": 53.96,
                  "confidence": 0.658
                },
                {
                  "text": "coffee",
                  "start": 53.96,
                  "end": 54.34,
                  "confidence": 0.672
                },
                {
                  "text": "right",
                  "start": 54.34,
                  "end": 54.68,
                  "confidence": 0.435
                },
                {
                  "text": "here.",
                  "start": 54.68,
                  "end": 54.92,
                  "confidence": 0.997
                }
              ]
            },
            {
              "id": 28,
              "start": 55.26,
              "end": 56.34,
              "text": " Boom advertisement.",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.757,
              "words": [
                {
                  "text": "Boom",
                  "start": 55.26,
                  "end": 55.58,
                  "confidence": 0.971
                },
                {
                  "text": "advertisement.",
                  "start": 55.58,
                  "end": 56.34,
                  "confidence": 0.591
                }
              ]
            },
            {
              "id": 29,
              "start": 56.68,
              "end": 56.88,
              "text": " Yeah.",
              "no_speech_prob": 0.13539506494998932,
              "confidence": 0.863,
              "words": [
                {
                  "text": "Yeah.",
                  "start": 56.68,
                  "end": 56.88,
                  "confidence": 0.863
                }
              ]
            },
            {
              "id": 30,
              "start": 57.12,
              "end": 58.24,
              "text": " Then I'm paying me for this.",
              "no_speech_prob": 0.023453781381249428,
              "confidence": 0.68,
              "words": [
                {
                  "text": "Then",
                  "start": 57.12,
                  "end": 57.28,
                  "confidence": 0.118
                },
                {
                  "text": "I'm",
                  "start": 57.28,
                  "end": 57.5,
                  "confidence": 0.921
                },
                {
                  "text": "paying",
                  "start": 57.5,
                  "end": 57.72,
                  "confidence": 0.927
                },
                {
                  "text": "me",
                  "start": 57.72,
                  "end": 57.9,
                  "confidence": 0.728
                },
                {
                  "text": "for",
                  "start": 57.9,
                  "end": 58.02,
                  "confidence": 0.999
                },
                {
                  "text": "this.",
                  "start": 58.02,
                  "end": 58.24,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 31,
              "start": 58.3,
              "end": 58.76,
              "text": " I'm care.",
              "no_speech_prob": 0.023453781381249428,
              "confidence": 0.894,
              "words": [
                {
                  "text": "I'm",
                  "start": 58.3,
                  "end": 58.5,
                  "confidence": 0.975
                },
                {
                  "text": "care.",
                  "start": 58.5,
                  "end": 58.76,
                  "confidence": 0.751
                }
              ]
            },
            {
              "id": 32,
              "start": 59.1,
              "end": 61.4,
              "text": " So which might not know about coffee is yes, you probably",
              "no_speech_prob": 0.023453781381249428,
              "confidence": 0.853,
              "words": [
                {
                  "text": "So",
                  "start": 59.1,
                  "end": 59.18,
                  "confidence": 0.996
                },
                {
                  "text": "which",
                  "start": 59.18,
                  "end": 59.3,
                  "confidence": 0.656
                },
                {
                  "text": "might",
                  "start": 59.3,
                  "end": 59.48,
                  "confidence": 0.665
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
                  "confidence": 0.991
                },
                {
                  "text": "about",
                  "start": 59.82,
                  "end": 60.08,
                  "confidence": 0.997
                },
                {
                  "text": "coffee",
                  "start": 60.08,
                  "end": 60.52,
                  "confidence": 0.984
                },
                {
                  "text": "is",
                  "start": 60.52,
                  "end": 60.76,
                  "confidence": 0.85
                },
                {
                  "text": "yes,",
                  "start": 60.76,
                  "end": 60.96,
                  "confidence": 0.846
                },
                {
                  "text": "you",
                  "start": 61.02,
                  "end": 61.12,
                  "confidence": 0.901
                },
                {
                  "text": "probably",
                  "start": 61.12,
                  "end": 61.4,
                  "confidence": 0.636
                }
              ]
            },
            {
              "id": 33,
              "start": 61.48,
              "end": 63.46,
              "text": " already know that a lot of companies actually",
              "no_speech_prob": 0.023453781381249428,
              "confidence": 0.977,
              "words": [
                {
                  "text": "already",
                  "start": 61.48,
                  "end": 61.7,
                  "confidence": 0.997
                },
                {
                  "text": "know",
                  "start": 61.7,
                  "end": 61.9,
                  "confidence": 0.997
                },
                {
                  "text": "that",
                  "start": 61.9,
                  "end": 62.12,
                  "confidence": 0.886
                },
                {
                  "text": "a",
                  "start": 62.12,
                  "end": 62.24,
                  "confidence": 0.993
                },
                {
                  "text": "lot",
                  "start": 62.24,
                  "end": 62.4,
                  "confidence": 0.996
                },
                {
                  "text": "of",
                  "start": 62.4,
                  "end": 62.48,
                  "confidence": 0.995
                },
                {
                  "text": "companies",
                  "start": 62.48,
                  "end": 62.98,
                  "confidence": 0.984
                },
                {
                  "text": "actually",
                  "start": 62.98,
                  "end": 63.46,
                  "confidence": 0.976
                }
              ]
            },
            {
              "id": 34,
              "start": 63.52,
              "end": 64.02,
              "text": " buy it up.",
              "no_speech_prob": 0.023453781381249428,
              "confidence": 0.877,
              "words": [
                {
                  "text": "buy",
                  "start": 63.52,
                  "end": 63.76,
                  "confidence": 0.679
                },
                {
                  "text": "it",
                  "start": 63.76,
                  "end": 63.86,
                  "confidence": 0.993
                },
                {
                  "text": "up.",
                  "start": 63.86,
                  "end": 64.02,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 35,
              "start": 64.32,
              "end": 67.2,
              "text": " Starbucks buys all had a coffee from Columbia.",
              "no_speech_prob": 0.023453781381249428,
              "confidence": 0.772,
              "words": [
                {
                  "text": "Starbucks",
                  "start": 64.32,
                  "end": 64.76,
                  "confidence": 0.77
                },
                {
                  "text": "buys",
                  "start": 64.76,
                  "end": 65.18,
                  "confidence": 0.982
                },
                {
                  "text": "all",
                  "start": 65.18,
                  "end": 65.58,
                  "confidence": 0.758
                },
                {
                  "text": "had",
                  "start": 65.58,
                  "end": 65.76,
                  "confidence": 0.237
                },
                {
                  "text": "a",
                  "start": 65.76,
                  "end": 65.92,
                  "confidence": 0.989
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
                  "confidence": 0.986
                },
                {
                  "text": "Columbia.",
                  "start": 66.6,
                  "end": 67.2,
                  "confidence": 0.962
                }
              ]
            },
            {
              "id": 36,
              "start": 67.7,
              "end": 69.68,
              "text": " It's kind of like their favorite place to buy coffee.",
              "no_speech_prob": 0.023453781381249428,
              "confidence": 0.95,
              "words": [
                {
                  "text": "It's",
                  "start": 67.7,
                  "end": 67.84,
                  "confidence": 0.971
                },
                {
                  "text": "kind",
                  "start": 67.84,
                  "end": 67.94,
                  "confidence": 0.902
                },
                {
                  "text": "of",
                  "start": 67.94,
                  "end": 68.0,
                  "confidence": 0.992
                },
                {
                  "text": "like",
                  "start": 68.0,
                  "end": 68.14,
                  "confidence": 0.997
                },
                {
                  "text": "their",
                  "start": 68.14,
                  "end": 68.22,
                  "confidence": 0.752
                },
                {
                  "text": "favorite",
                  "start": 68.22,
                  "end": 68.44,
                  "confidence": 0.973
                },
                {
                  "text": "place",
                  "start": 68.44,
                  "end": 68.66,
                  "confidence": 0.991
                },
                {
                  "text": "to",
                  "start": 68.66,
                  "end": 68.84,
                  "confidence": 0.96
                },
                {
                  "text": "buy",
                  "start": 68.84,
                  "end": 69.22,
                  "confidence": 0.994
                },
                {
                  "text": "coffee.",
                  "start": 69.22,
                  "end": 69.68,
                  "confidence": 0.979
                }
              ]
            },
            {
              "id": 37,
              "start": 70.02,
              "end": 73.08,
              "text": " And kind of to pay tribute to that Starbucks when they're",
              "no_speech_prob": 0.023453781381249428,
              "confidence": 0.771,
              "words": [
                {
                  "text": "And",
                  "start": 70.02,
                  "end": 70.18,
                  "confidence": 0.992
                },
                {
                  "text": "kind",
                  "start": 70.18,
                  "end": 70.36,
                  "confidence": 0.61
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
                  "end": 70.62,
                  "confidence": 0.978
                },
                {
                  "text": "pay",
                  "start": 70.62,
                  "end": 70.9,
                  "confidence": 0.997
                },
                {
                  "text": "tribute",
                  "start": 70.9,
                  "end": 71.34,
                  "confidence": 0.999
                },
                {
                  "text": "to",
                  "start": 71.34,
                  "end": 71.6,
                  "confidence": 0.987
                },
                {
                  "text": "that",
                  "start": 71.6,
                  "end": 71.92,
                  "confidence": 0.99
                },
                {
                  "text": "Starbucks",
                  "start": 71.92,
                  "end": 72.72,
                  "confidence": 0.684
                },
                {
                  "text": "when",
                  "start": 72.72,
                  "end": 72.98,
                  "confidence": 0.585
                },
                {
                  "text": "they're",
                  "start": 72.98,
                  "end": 73.08,
                  "confidence": 0.437
                }
              ]
            },
            {
              "id": 38,
              "start": 73.08,
              "end": 77.51,
              "text": " making their 1,000th store in 2016, they decided,",
              "no_speech_prob": 0.023453781381249428,
              "confidence": 0.917,
              "words": [
                {
                  "text": "making",
                  "start": 73.08,
                  "end": 73.42,
                  "confidence": 0.995
                },
                {
                  "text": "their",
                  "start": 73.42,
                  "end": 73.7,
                  "confidence": 0.994
                },
                {
                  "text": "1,000th",
                  "start": 73.7,
                  "end": 74.58,
                  "confidence": 0.843
                },
                {
                  "text": "store",
                  "start": 74.58,
                  "end": 74.9,
                  "confidence": 0.981
                },
                {
                  "text": "in",
                  "start": 74.9,
                  "end": 75.12,
                  "confidence": 0.994
                },
                {
                  "text": "2016,",
                  "start": 75.12,
                  "end": 76.42,
                  "confidence": 0.993
                },
                {
                  "text": "they",
                  "start": 76.62,
                  "end": 77.06,
                  "confidence": 0.817
                },
                {
                  "text": "decided,",
                  "start": 77.06,
                  "end": 77.51,
                  "confidence": 0.981
                }
              ]
            },
            {
              "id": 39,
              "start": 77.51,
              "end": 79.32,
              "text": " yo, we're going to put it in Columbia.",
              "no_speech_prob": 0.023453781381249428,
              "confidence": 0.943,
              "words": [
                {
                  "text": "yo,",
                  "start": 77.51,
                  "end": 77.96,
                  "confidence": 0.639
                },
                {
                  "text": "we're",
                  "start": 77.98,
                  "end": 78.22,
                  "confidence": 0.994
                },
                {
                  "text": "going",
                  "start": 78.22,
                  "end": 78.36,
                  "confidence": 0.954
                },
                {
                  "text": "to",
                  "start": 78.36,
                  "end": 78.46,
                  "confidence": 0.999
                },
                {
                  "text": "put",
                  "start": 78.46,
                  "end": 78.58,
                  "confidence": 0.999
                },
                {
                  "text": "it",
                  "start": 78.58,
                  "end": 78.72,
                  "confidence": 0.995
                },
                {
                  "text": "in",
                  "start": 78.72,
                  "end": 78.88,
                  "confidence": 0.998
                },
                {
                  "text": "Columbia.",
                  "start": 78.88,
                  "end": 79.32,
                  "confidence": 0.986
                }
              ]
            },
            {
              "id": 40,
              "start": 79.32,
              "end": 82.28,
              "text": " And this was in the town of Medellin, Columbia.",
              "no_speech_prob": 0.023453781381249428,
              "confidence": 0.905,
              "words": [
                {
                  "text": "And",
                  "start": 79.32,
                  "end": 79.98,
                  "confidence": 0.997
                },
                {
                  "text": "this",
                  "start": 79.98,
                  "end": 80.2,
                  "confidence": 0.999
                },
                {
                  "text": "was",
                  "start": 80.2,
                  "end": 80.42,
                  "confidence": 0.997
                },
                {
                  "text": "in",
                  "start": 80.42,
                  "end": 80.58,
                  "confidence": 0.997
                },
                {
                  "text": "the",
                  "start": 80.58,
                  "end": 80.72,
                  "confidence": 0.997
                },
                {
                  "text": "town",
                  "start": 80.72,
                  "end": 81.0,
                  "confidence": 0.994
                },
                {
                  "text": "of",
                  "start": 81.0,
                  "end": 81.22,
                  "confidence": 0.999
                },
                {
                  "text": "Medellin,",
                  "start": 81.22,
                  "end": 81.72,
                  "confidence": 0.718
                },
                {
                  "text": "Columbia.",
                  "start": 81.76,
                  "end": 82.28,
                  "confidence": 0.92
                }
              ]
            },
            {
              "id": 41,
              "start": 82.6,
              "end": 85.38,
              "text": " Now here's the thing, when it comes to coffee in Columbia,",
              "no_speech_prob": 0.023453781381249428,
              "confidence": 0.924,
              "words": [
                {
                  "text": "Now",
                  "start": 82.6,
                  "end": 82.76,
                  "confidence": 0.993
                },
                {
                  "text": "here's",
                  "start": 82.76,
                  "end": 83.06,
                  "confidence": 0.758
                },
                {
                  "text": "the",
                  "start": 83.06,
                  "end": 83.22,
                  "confidence": 0.998
                },
                {
                  "text": "thing,",
                  "start": 83.22,
                  "end": 83.38,
                  "confidence": 0.999
                },
                {
                  "text": "when",
                  "start": 83.4,
                  "end": 83.56,
                  "confidence": 0.976
                },
                {
                  "text": "it",
                  "start": 83.56,
                  "end": 83.68,
                  "confidence": 0.996
                },
                {
                  "text": "comes",
                  "start": 83.68,
                  "end": 84.08,
                  "confidence": 0.995
                },
                {
                  "text": "to",
                  "start": 84.08,
                  "end": 84.3,
                  "confidence": 0.973
                },
                {
                  "text": "coffee",
                  "start": 84.3,
                  "end": 84.68,
                  "confidence": 0.862
                },
                {
                  "text": "in",
                  "start": 84.68,
                  "end": 84.94,
                  "confidence": 0.959
                },
                {
                  "text": "Columbia,",
                  "start": 84.94,
                  "end": 85.38,
                  "confidence": 0.876
                }
              ]
            },
            {
              "id": 42,
              "start": 85.44,
              "end": 90.5,
              "text": " they are the third largest producing and exporting coffee",
              "no_speech_prob": 0.0022646081633865833,
              "confidence": 0.826,
              "words": [
                {
                  "text": "they",
                  "start": 85.44,
                  "end": 85.66,
                  "confidence": 0.704
                },
                {
                  "text": "are",
                  "start": 85.66,
                  "end": 85.88,
                  "confidence": 0.991
                },
                {
                  "text": "the",
                  "start": 85.88,
                  "end": 86.08,
                  "confidence": 0.995
                },
                {
                  "text": "third",
                  "start": 86.08,
                  "end": 86.64,
                  "confidence": 0.988
                },
                {
                  "text": "largest",
                  "start": 86.64,
                  "end": 87.5,
                  "confidence": 0.976
                },
                {
                  "text": "producing",
                  "start": 87.5,
                  "end": 88.76,
                  "confidence": 0.672
                },
                {
                  "text": "and",
                  "start": 88.76,
                  "end": 89.36,
                  "confidence": 0.683
                },
                {
                  "text": "exporting",
                  "start": 89.36,
                  "end": 89.92,
                  "confidence": 0.912
                },
                {
                  "text": "coffee",
                  "start": 89.92,
                  "end": 90.5,
                  "confidence": 0.64
                }
              ]
            },
            {
              "id": 43,
              "start": 90.54,
              "end": 91.9,
              "text": " country in the world.",
              "no_speech_prob": 0.0022646081633865833,
              "confidence": 0.996,
              "words": [
                {
                  "text": "country",
                  "start": 90.54,
                  "end": 90.9,
                  "confidence": 0.992
                },
                {
                  "text": "in",
                  "start": 90.9,
                  "end": 91.16,
                  "confidence": 0.994
                },
                {
                  "text": "the",
                  "start": 91.16,
                  "end": 91.32,
                  "confidence": 0.999
                },
                {
                  "text": "world.",
                  "start": 91.32,
                  "end": 91.9,
                  "confidence": 1.0
                }
              ]
            },
            {
              "id": 44,
              "start": 92.22,
              "end": 95.07,
              "text": " The amount of coffee that is exported from Columbia equals",
              "no_speech_prob": 0.0022646081633865833,
              "confidence": 0.907,
              "words": [
                {
                  "text": "The",
                  "start": 92.22,
                  "end": 92.34,
                  "confidence": 0.998
                },
                {
                  "text": "amount",
                  "start": 92.34,
                  "end": 92.6,
                  "confidence": 1.0
                },
                {
                  "text": "of",
                  "start": 92.6,
                  "end": 92.72,
                  "confidence": 1.0
                },
                {
                  "text": "coffee",
                  "start": 92.72,
                  "end": 93.06,
                  "confidence": 0.999
                },
                {
                  "text": "that",
                  "start": 93.06,
                  "end": 93.22,
                  "confidence": 0.997
                },
                {
                  "text": "is",
                  "start": 93.22,
                  "end": 93.34,
                  "confidence": 0.976
                },
                {
                  "text": "exported",
                  "start": 93.34,
                  "end": 93.86,
                  "confidence": 0.99
                },
                {
                  "text": "from",
                  "start": 93.86,
                  "end": 94.18,
                  "confidence": 0.931
                },
                {
                  "text": "Columbia",
                  "start": 94.18,
                  "end": 94.66,
                  "confidence": 0.96
                },
                {
                  "text": "equals",
                  "start": 94.66,
                  "end": 95.07,
                  "confidence": 0.438
                }
              ]
            },
            {
              "id": 45,
              "start": 95.07,
              "end": 102.52,
              "text": " about 810,000 metric tons or approximately 11.5 million",
              "no_speech_prob": 0.0022646081633865833,
              "confidence": 0.819,
              "words": [
                {
                  "text": "about",
                  "start": 95.07,
                  "end": 95.6,
                  "confidence": 0.998
                },
                {
                  "text": "810,000",
                  "start": 95.6,
                  "end": 98.18,
                  "confidence": 0.796
                },
                {
                  "text": "metric",
                  "start": 98.18,
                  "end": 98.68,
                  "confidence": 0.964
                },
                {
                  "text": "tons",
                  "start": 98.68,
                  "end": 99.26,
                  "confidence": 0.972
                },
                {
                  "text": "or",
                  "start": 99.26,
                  "end": 100.0,
                  "confidence": 0.463
                },
                {
                  "text": "approximately",
                  "start": 100.0,
                  "end": 100.66,
                  "confidence": 0.983
                },
                {
                  "text": "11.5",
                  "start": 100.66,
                  "end": 102.1,
                  "confidence": 0.935
                },
                {
                  "text": "million",
                  "start": 102.1,
                  "end": 102.52,
                  "confidence": 0.534
                }
              ]
            },
            {
              "id": 46,
              "start": 102.66,
              "end": 102.94,
              "text": " bags.",
              "no_speech_prob": 0.0022646081633865833,
              "confidence": 0.986,
              "words": [
                {
                  "text": "bags.",
                  "start": 102.66,
                  "end": 102.94,
                  "confidence": 0.986
                }
              ]
            },
            {
              "id": 47,
              "start": 102.94,
              "end": 107.28,
              "text": " However, although it might be beaten by countries like Brazil,",
              "no_speech_prob": 0.0022646081633865833,
              "confidence": 0.975,
              "words": [
                {
                  "text": "However,",
                  "start": 102.94,
                  "end": 103.62,
                  "confidence": 0.997
                },
                {
                  "text": "although",
                  "start": 103.84,
                  "end": 104.08,
                  "confidence": 0.989
                },
                {
                  "text": "it",
                  "start": 104.08,
                  "end": 104.4,
                  "confidence": 0.977
                },
                {
                  "text": "might",
                  "start": 104.4,
                  "end": 104.58,
                  "confidence": 0.993
                },
                {
                  "text": "be",
                  "start": 104.58,
                  "end": 104.82,
                  "confidence": 0.996
                },
                {
                  "text": "beaten",
                  "start": 104.82,
                  "end": 105.08,
                  "confidence": 0.953
                },
                {
                  "text": "by",
                  "start": 105.08,
                  "end": 105.36,
                  "confidence": 0.981
                },
                {
                  "text": "countries",
                  "start": 105.36,
                  "end": 105.96,
                  "confidence": 0.975
                },
                {
                  "text": "like",
                  "start": 105.96,
                  "end": 106.5,
                  "confidence": 0.96
                },
                {
                  "text": "Brazil,",
                  "start": 106.5,
                  "end": 107.28,
                  "confidence": 0.933
                }
              ]
            },
            {
              "id": 48,
              "start": 107.92,
              "end": 111.12,
              "text": " it is actually the number one or highest country for producing",
              "no_speech_prob": 0.0022646081633865833,
              "confidence": 0.906,
              "words": [
                {
                  "text": "it",
                  "start": 107.92,
                  "end": 108.04,
                  "confidence": 0.996
                },
                {
                  "text": "is",
                  "start": 108.04,
                  "end": 108.14,
                  "confidence": 0.994
                },
                {
                  "text": "actually",
                  "start": 108.14,
                  "end": 108.44,
                  "confidence": 0.998
                },
                {
                  "text": "the",
                  "start": 108.44,
                  "end": 108.68,
                  "confidence": 0.986
                },
                {
                  "text": "number",
                  "start": 108.68,
                  "end": 108.92,
                  "confidence": 0.989
                },
                {
                  "text": "one",
                  "start": 108.92,
                  "end": 109.18,
                  "confidence": 0.979
                },
                {
                  "text": "or",
                  "start": 109.18,
                  "end": 109.42,
                  "confidence": 0.909
                },
                {
                  "text": "highest",
                  "start": 109.42,
                  "end": 109.8,
                  "confidence": 0.988
                },
                {
                  "text": "country",
                  "start": 109.8,
                  "end": 110.22,
                  "confidence": 0.872
                },
                {
                  "text": "for",
                  "start": 110.22,
                  "end": 110.52,
                  "confidence": 0.556
                },
                {
                  "text": "producing",
                  "start": 110.52,
                  "end": 111.12,
                  "confidence": 0.826
                }
              ]
            },
            {
              "id": 49,
              "start": 111.18,
              "end": 115.28,
              "text": " and growing a specific type of bean known as the Arab",
              "no_speech_prob": 0.0022646081633865833,
              "confidence": 0.821,
              "words": [
                {
                  "text": "and",
                  "start": 111.18,
                  "end": 111.4,
                  "confidence": 0.818
                },
                {
                  "text": "growing",
                  "start": 111.4,
                  "end": 111.68,
                  "confidence": 0.998
                },
                {
                  "text": "a",
                  "start": 111.68,
                  "end": 112.24,
                  "confidence": 0.949
                },
                {
                  "text": "specific",
                  "start": 112.24,
                  "end": 112.86,
                  "confidence": 0.998
                },
                {
                  "text": "type",
                  "start": 112.86,
                  "end": 113.24,
                  "confidence": 0.999
                },
                {
                  "text": "of",
                  "start": 113.24,
                  "end": 113.42,
                  "confidence": 0.991
                },
                {
                  "text": "bean",
                  "start": 113.42,
                  "end": 114.0,
                  "confidence": 0.598
                },
                {
                  "text": "known",
                  "start": 114.0,
                  "end": 114.36,
                  "confidence": 0.775
                },
                {
                  "text": "as",
                  "start": 114.36,
                  "end": 114.66,
                  "confidence": 0.775
                },
                {
                  "text": "the",
                  "start": 114.66,
                  "end": 114.88,
                  "confidence": 0.878
                },
                {
                  "text": "Arab",
                  "start": 114.88,
                  "end": 115.28,
                  "confidence": 0.473
                }
              ]
            },
            {
              "id": 50,
              "start": 115.32,
              "end": 116.3,
              "text": " Beka bean.",
              "no_speech_prob": 0.008894940838217735,
              "confidence": 0.348,
              "words": [
                {
                  "text": "Beka",
                  "start": 115.32,
                  "end": 115.86,
                  "confidence": 0.278
                },
                {
                  "text": "bean.",
                  "start": 115.86,
                  "end": 116.3,
                  "confidence": 0.546
                }
              ]
            },
            {
              "id": 51,
              "start": 116.68,
              "end": 119.55,
              "text": " And I know coffee is really important when it comes to talking",
              "no_speech_prob": 0.008894940838217735,
              "confidence": 0.917,
              "words": [
                {
                  "text": "And",
                  "start": 116.68,
                  "end": 116.8,
                  "confidence": 0.998
                },
                {
                  "text": "I",
                  "start": 116.8,
                  "end": 116.9,
                  "confidence": 0.997
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
                  "confidence": 0.955
                },
                {
                  "text": "is",
                  "start": 117.5,
                  "end": 117.8,
                  "confidence": 0.998
                },
                {
                  "text": "really",
                  "start": 117.8,
                  "end": 118.14,
                  "confidence": 0.999
                },
                {
                  "text": "important",
                  "start": 118.14,
                  "end": 118.72,
                  "confidence": 0.989
                },
                {
                  "text": "when",
                  "start": 118.72,
                  "end": 118.92,
                  "confidence": 0.926
                },
                {
                  "text": "it",
                  "start": 118.92,
                  "end": 119.02,
                  "confidence": 0.841
                },
                {
                  "text": "comes",
                  "start": 119.02,
                  "end": 119.26,
                  "confidence": 0.923
                },
                {
                  "text": "to",
                  "start": 119.26,
                  "end": 119.4,
                  "confidence": 0.702
                },
                {
                  "text": "talking",
                  "start": 119.4,
                  "end": 119.55,
                  "confidence": 0.748
                }
              ]
            },
            {
              "id": 52,
              "start": 119.55,
              "end": 121.62,
              "text": " about Columbia, but you guys really don't know how important",
              "no_speech_prob": 0.008894940838217735,
              "confidence": 0.882,
              "words": [
                {
                  "text": "about",
                  "start": 119.55,
                  "end": 119.72,
                  "confidence": 0.994
                },
                {
                  "text": "Columbia,",
                  "start": 119.72,
                  "end": 119.94,
                  "confidence": 0.983
                },
                {
                  "text": "but",
                  "start": 120.04,
                  "end": 120.16,
                  "confidence": 0.974
                },
                {
                  "text": "you",
                  "start": 120.16,
                  "end": 120.28,
                  "confidence": 0.927
                },
                {
                  "text": "guys",
                  "start": 120.28,
                  "end": 120.4,
                  "confidence": 0.487
                },
                {
                  "text": "really",
                  "start": 120.4,
                  "end": 120.62,
                  "confidence": 0.983
                },
                {
                  "text": "don't",
                  "start": 120.62,
                  "end": 120.78,
                  "confidence": 0.99
                },
                {
                  "text": "know",
                  "start": 120.78,
                  "end": 120.94,
                  "confidence": 0.825
                },
                {
                  "text": "how",
                  "start": 120.94,
                  "end": 121.12,
                  "confidence": 0.773
                },
                {
                  "text": "important",
                  "start": 121.12,
                  "end": 121.62,
                  "confidence": 0.953
                }
              ]
            },
            {
              "id": 53,
              "start": 121.62,
              "end": 122.64,
              "text": " it is with its culture.",
              "no_speech_prob": 0.008894940838217735,
              "confidence": 0.974,
              "words": [
                {
                  "text": "it",
                  "start": 121.62,
                  "end": 121.8,
                  "confidence": 0.997
                },
                {
                  "text": "is",
                  "start": 121.8,
                  "end": 121.94,
                  "confidence": 1.0
                },
                {
                  "text": "with",
                  "start": 121.94,
                  "end": 122.1,
                  "confidence": 0.995
                },
                {
                  "text": "its",
                  "start": 122.1,
                  "end": 122.28,
                  "confidence": 0.888
                },
                {
                  "text": "culture.",
                  "start": 122.28,
                  "end": 122.64,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 54,
              "start": 123.08,
              "end": 126.61,
              "text": " Interesting fact that in 2007, major spots",
              "no_speech_prob": 0.008894940838217735,
              "confidence": 0.929,
              "words": [
                {
                  "text": "Interesting",
                  "start": 123.08,
                  "end": 123.56,
                  "confidence": 0.82
                },
                {
                  "text": "fact",
                  "start": 123.56,
                  "end": 124.08,
                  "confidence": 0.998
                },
                {
                  "text": "that",
                  "start": 124.08,
                  "end": 124.46,
                  "confidence": 0.908
                },
                {
                  "text": "in",
                  "start": 124.46,
                  "end": 124.6,
                  "confidence": 0.974
                },
                {
                  "text": "2007,",
                  "start": 124.6,
                  "end": 125.56,
                  "confidence": 0.991
                },
                {
                  "text": "major",
                  "start": 125.74,
                  "end": 126.18,
                  "confidence": 0.941
                },
                {
                  "text": "spots",
                  "start": 126.18,
                  "end": 126.61,
                  "confidence": 0.886
                }
              ]
            },
            {
              "id": 55,
              "start": 126.61,
              "end": 131.2,
              "text": " equaling a buffer zone of approximately 207,000 hectares,",
              "no_speech_prob": 0.008894940838217735,
              "confidence": 0.836,
              "words": [
                {
                  "text": "equaling",
                  "start": 126.61,
                  "end": 127.26,
                  "confidence": 0.733
                },
                {
                  "text": "a",
                  "start": 127.26,
                  "end": 127.4,
                  "confidence": 0.647
                },
                {
                  "text": "buffer",
                  "start": 127.4,
                  "end": 127.72,
                  "confidence": 0.681
                },
                {
                  "text": "zone",
                  "start": 127.72,
                  "end": 128.04,
                  "confidence": 0.996
                },
                {
                  "text": "of",
                  "start": 128.04,
                  "end": 128.22,
                  "confidence": 0.925
                },
                {
                  "text": "approximately",
                  "start": 128.22,
                  "end": 128.78,
                  "confidence": 0.998
                },
                {
                  "text": "207,000",
                  "start": 128.78,
                  "end": 130.72,
                  "confidence": 0.913
                },
                {
                  "text": "hectares,",
                  "start": 130.72,
                  "end": 131.2,
                  "confidence": 0.801
                }
              ]
            },
            {
              "id": 56,
              "start": 131.64,
              "end": 134.16,
              "text": " which are called the coffee cultural landscape,",
              "no_speech_prob": 0.008894940838217735,
              "confidence": 0.965,
              "words": [
                {
                  "text": "which",
                  "start": 131.64,
                  "end": 131.84,
                  "confidence": 1.0
                },
                {
                  "text": "are",
                  "start": 131.84,
                  "end": 132.1,
                  "confidence": 0.997
                },
                {
                  "text": "called",
                  "start": 132.1,
                  "end": 132.44,
                  "confidence": 0.999
                },
                {
                  "text": "the",
                  "start": 132.44,
                  "end": 132.72,
                  "confidence": 0.99
                },
                {
                  "text": "coffee",
                  "start": 132.72,
                  "end": 133.12,
                  "confidence": 0.896
                },
                {
                  "text": "cultural",
                  "start": 133.12,
                  "end": 133.58,
                  "confidence": 0.905
                },
                {
                  "text": "landscape,",
                  "start": 133.58,
                  "end": 134.16,
                  "confidence": 0.978
                }
              ]
            },
            {
              "id": 57,
              "start": 134.5,
              "end": 137.22,
              "text": " were considered a UNESCO World Heritage Site.",
              "no_speech_prob": 0.008894940838217735,
              "confidence": 0.881,
              "words": [
                {
                  "text": "were",
                  "start": 134.5,
                  "end": 134.68,
                  "confidence": 0.798
                },
                {
                  "text": "considered",
                  "start": 134.68,
                  "end": 135.2,
                  "confidence": 0.996
                },
                {
                  "text": "a",
                  "start": 135.2,
                  "end": 135.44,
                  "confidence": 0.994
                },
                {
                  "text": "UNESCO",
                  "start": 135.44,
                  "end": 135.9,
                  "confidence": 0.926
                },
                {
                  "text": "World",
                  "start": 135.9,
                  "end": 136.2,
                  "confidence": 0.889
                },
                {
                  "text": "Heritage",
                  "start": 136.2,
                  "end": 136.72,
                  "confidence": 0.994
                },
                {
                  "text": "Site.",
                  "start": 136.72,
                  "end": 137.22,
                  "confidence": 0.604
                }
              ]
            },
            {
              "id": 58,
              "start": 137.62,
              "end": 140.74,
              "text": " And also in 2007, the EU, the European Union,",
              "no_speech_prob": 0.008894940838217735,
              "confidence": 0.965,
              "words": [
                {
                  "text": "And",
                  "start": 137.62,
                  "end": 137.76,
                  "confidence": 0.995
                },
                {
                  "text": "also",
                  "start": 137.76,
                  "end": 138.06,
                  "confidence": 0.999
                },
                {
                  "text": "in",
                  "start": 138.06,
                  "end": 138.28,
                  "confidence": 0.904
                },
                {
                  "text": "2007,",
                  "start": 138.28,
                  "end": 139.04,
                  "confidence": 0.997
                },
                {
                  "text": "the",
                  "start": 139.2,
                  "end": 139.38,
                  "confidence": 0.973
                },
                {
                  "text": "EU,",
                  "start": 139.38,
                  "end": 139.72,
                  "confidence": 0.887
                },
                {
                  "text": "the",
                  "start": 139.84,
                  "end": 139.96,
                  "confidence": 0.958
                },
                {
                  "text": "European",
                  "start": 139.96,
                  "end": 140.36,
                  "confidence": 0.998
                },
                {
                  "text": "Union,",
                  "start": 140.36,
                  "end": 140.74,
                  "confidence": 0.985
                }
              ]
            },
            {
              "id": 59,
              "start": 140.76,
              "end": 145.82,
              "text": " granted Colombian coffee a protected designation of origin status.",
              "no_speech_prob": 0.0017999779665842652,
              "confidence": 0.833,
              "words": [
                {
                  "text": "granted",
                  "start": 140.76,
                  "end": 141.22,
                  "confidence": 0.962
                },
                {
                  "text": "Colombian",
                  "start": 141.22,
                  "end": 141.88,
                  "confidence": 0.807
                },
                {
                  "text": "coffee",
                  "start": 141.88,
                  "end": 142.32,
                  "confidence": 0.947
                },
                {
                  "text": "a",
                  "start": 142.32,
                  "end": 142.78,
                  "confidence": 0.64
                },
                {
                  "text": "protected",
                  "start": 142.78,
                  "end": 143.36,
                  "confidence": 0.995
                },
                {
                  "text": "designation",
                  "start": 143.36,
                  "end": 144.22,
                  "confidence": 0.955
                },
                {
                  "text": "of",
                  "start": 144.22,
                  "end": 144.52,
                  "confidence": 0.537
                },
                {
                  "text": "origin",
                  "start": 144.52,
                  "end": 145.04,
                  "confidence": 0.955
                },
                {
                  "text": "status.",
                  "start": 145.04,
                  "end": 145.82,
                  "confidence": 0.865
                }
              ]
            },
            {
              "id": 60,
              "start": 146.12,
              "end": 149.08,
              "text": " Now interesting enough when it comes to the coffee in Columbia,",
              "no_speech_prob": 0.0017999779665842652,
              "confidence": 0.825,
              "words": [
                {
                  "text": "Now",
                  "start": 146.12,
                  "end": 146.22,
                  "confidence": 0.887
                },
                {
                  "text": "interesting",
                  "start": 146.22,
                  "end": 146.66,
                  "confidence": 0.595
                },
                {
                  "text": "enough",
                  "start": 146.66,
                  "end": 146.96,
                  "confidence": 0.96
                },
                {
                  "text": "when",
                  "start": 146.96,
                  "end": 147.14,
                  "confidence": 0.544
                },
                {
                  "text": "it",
                  "start": 147.14,
                  "end": 147.26,
                  "confidence": 0.994
                },
                {
                  "text": "comes",
                  "start": 147.26,
                  "end": 147.46,
                  "confidence": 0.993
                },
                {
                  "text": "to",
                  "start": 147.46,
                  "end": 147.68,
                  "confidence": 0.899
                },
                {
                  "text": "the",
                  "start": 147.68,
                  "end": 147.82,
                  "confidence": 0.969
                },
                {
                  "text": "coffee",
                  "start": 147.82,
                  "end": 148.2,
                  "confidence": 0.99
                },
                {
                  "text": "in",
                  "start": 148.2,
                  "end": 148.5,
                  "confidence": 0.865
                },
                {
                  "text": "Columbia,",
                  "start": 148.5,
                  "end": 149.08,
                  "confidence": 0.596
                }
              ]
            },
            {
              "id": 61,
              "start": 149.12,
              "end": 153.1,
              "text": " believe it or not, it is not actually native to the country.",
              "no_speech_prob": 0.0017999779665842652,
              "confidence": 0.984,
              "words": [
                {
                  "text": "believe",
                  "start": 149.12,
                  "end": 149.58,
                  "confidence": 0.965
                },
                {
                  "text": "it",
                  "start": 149.58,
                  "end": 149.7,
                  "confidence": 0.99
                },
                {
                  "text": "or",
                  "start": 149.7,
                  "end": 149.82,
                  "confidence": 1.0
                },
                {
                  "text": "not,",
                  "start": 149.82,
                  "end": 150.02,
                  "confidence": 1.0
                },
                {
                  "text": "it",
                  "start": 150.18,
                  "end": 150.28,
                  "confidence": 0.953
                },
                {
                  "text": "is",
                  "start": 150.28,
                  "end": 150.44,
                  "confidence": 0.996
                },
                {
                  "text": "not",
                  "start": 150.44,
                  "end": 151.02,
                  "confidence": 0.996
                },
                {
                  "text": "actually",
                  "start": 151.02,
                  "end": 151.8,
                  "confidence": 0.979
                },
                {
                  "text": "native",
                  "start": 151.8,
                  "end": 152.32,
                  "confidence": 0.984
                },
                {
                  "text": "to",
                  "start": 152.32,
                  "end": 152.56,
                  "confidence": 0.96
                },
                {
                  "text": "the",
                  "start": 152.56,
                  "end": 152.72,
                  "confidence": 0.992
                },
                {
                  "text": "country.",
                  "start": 152.72,
                  "end": 153.1,
                  "confidence": 0.997
                }
              ]
            },
            {
              "id": 62,
              "start": 153.54,
              "end": 156.72,
              "text": " It's come from somewhere else, not really an invasive species",
              "no_speech_prob": 0.0017999779665842652,
              "confidence": 0.924,
              "words": [
                {
                  "text": "It's",
                  "start": 153.54,
                  "end": 153.78,
                  "confidence": 0.988
                },
                {
                  "text": "come",
                  "start": 153.78,
                  "end": 153.96,
                  "confidence": 0.971
                },
                {
                  "text": "from",
                  "start": 153.96,
                  "end": 154.12,
                  "confidence": 0.999
                },
                {
                  "text": "somewhere",
                  "start": 154.12,
                  "end": 154.52,
                  "confidence": 0.992
                },
                {
                  "text": "else,",
                  "start": 154.52,
                  "end": 155.02,
                  "confidence": 1.0
                },
                {
                  "text": "not",
                  "start": 155.1,
                  "end": 155.44,
                  "confidence": 0.789
                },
                {
                  "text": "really",
                  "start": 155.44,
                  "end": 155.68,
                  "confidence": 0.995
                },
                {
                  "text": "an",
                  "start": 155.68,
                  "end": 155.8,
                  "confidence": 0.76
                },
                {
                  "text": "invasive",
                  "start": 155.8,
                  "end": 156.22,
                  "confidence": 0.977
                },
                {
                  "text": "species",
                  "start": 156.22,
                  "end": 156.72,
                  "confidence": 0.77
                }
              ]
            },
            {
              "id": 63,
              "start": 156.72,
              "end": 158.42,
              "text": " because it's very much welcomed.",
              "no_speech_prob": 0.0017999779665842652,
              "confidence": 0.994,
              "words": [
                {
                  "text": "because",
                  "start": 156.72,
                  "end": 157.14,
                  "confidence": 0.999
                },
                {
                  "text": "it's",
                  "start": 157.14,
                  "end": 157.36,
                  "confidence": 0.993
                },
                {
                  "text": "very",
                  "start": 157.36,
                  "end": 157.72,
                  "confidence": 0.999
                },
                {
                  "text": "much",
                  "start": 157.72,
                  "end": 157.96,
                  "confidence": 0.998
                },
                {
                  "text": "welcomed.",
                  "start": 157.96,
                  "end": 158.42,
                  "confidence": 0.979
                }
              ]
            },
            {
              "id": 64,
              "start": 158.84,
              "end": 161.98,
              "text": " Now you may have also seen this guy on many different Colombian",
              "no_speech_prob": 0.0017999779665842652,
              "confidence": 0.897,
              "words": [
                {
                  "text": "Now",
                  "start": 158.84,
                  "end": 159.0,
                  "confidence": 0.999
                },
                {
                  "text": "you",
                  "start": 159.0,
                  "end": 159.14,
                  "confidence": 0.792
                },
                {
                  "text": "may",
                  "start": 159.14,
                  "end": 159.28,
                  "confidence": 0.998
                },
                {
                  "text": "have",
                  "start": 159.28,
                  "end": 159.42,
                  "confidence": 0.987
                },
                {
                  "text": "also",
                  "start": 159.42,
                  "end": 159.76,
                  "confidence": 0.995
                },
                {
                  "text": "seen",
                  "start": 159.76,
                  "end": 160.14,
                  "confidence": 0.998
                },
                {
                  "text": "this",
                  "start": 160.14,
                  "end": 160.36,
                  "confidence": 0.99
                },
                {
                  "text": "guy",
                  "start": 160.36,
                  "end": 160.7,
                  "confidence": 0.991
                },
                {
                  "text": "on",
                  "start": 160.7,
                  "end": 160.9,
                  "confidence": 0.627
                },
                {
                  "text": "many",
                  "start": 160.9,
                  "end": 161.12,
                  "confidence": 0.988
                },
                {
                  "text": "different",
                  "start": 161.12,
                  "end": 161.38,
                  "confidence": 0.965
                },
                {
                  "text": "Colombian",
                  "start": 161.38,
                  "end": 161.98,
                  "confidence": 0.734
                }
              ]
            },
            {
              "id": 65,
              "start": 161.98,
              "end": 162.81,
              "text": " coffee brands.",
              "no_speech_prob": 0.0017999779665842652,
              "confidence": 0.971,
              "words": [
                {
                  "text": "coffee",
                  "start": 161.98,
                  "end": 162.46,
                  "confidence": 0.958
                },
                {
                  "text": "brands.",
                  "start": 162.46,
                  "end": 162.81,
                  "confidence": 0.984
                }
              ]
            },
            {
              "id": 66,
              "start": 162.81,
              "end": 164.68,
              "text": " Now his name is Juan Valdez.",
              "no_speech_prob": 0.0017999779665842652,
              "confidence": 0.892,
              "words": [
                {
                  "text": "Now",
                  "start": 162.81,
                  "end": 163.04,
                  "confidence": 0.994
                },
                {
                  "text": "his",
                  "start": 163.04,
                  "end": 163.24,
                  "confidence": 0.823
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
                  "end": 163.72,
                  "confidence": 0.998
                },
                {
                  "text": "Juan",
                  "start": 163.72,
                  "end": 164.0,
                  "confidence": 0.804
                },
                {
                  "text": "Valdez.",
                  "start": 164.0,
                  "end": 164.68,
                  "confidence": 0.848
                }
              ]
            },
            {
              "id": 67,
              "start": 164.74,
              "end": 167.42,
              "text": " Now some people think that this guy is actually really",
              "no_speech_prob": 0.0017999779665842652,
              "confidence": 0.93,
              "words": [
                {
                  "text": "Now",
                  "start": 164.74,
                  "end": 164.9,
                  "confidence": 0.994
                },
                {
                  "text": "some",
                  "start": 164.9,
                  "end": 165.06,
                  "confidence": 0.944
                },
                {
                  "text": "people",
                  "start": 165.06,
                  "end": 165.24,
                  "confidence": 1.0
                },
                {
                  "text": "think",
                  "start": 165.24,
                  "end": 165.6,
                  "confidence": 0.999
                },
                {
                  "text": "that",
                  "start": 165.6,
                  "end": 165.76,
                  "confidence": 0.958
                },
                {
                  "text": "this",
                  "start": 165.76,
                  "end": 165.98,
                  "confidence": 0.993
                },
                {
                  "text": "guy",
                  "start": 165.98,
                  "end": 166.26,
                  "confidence": 0.999
                },
                {
                  "text": "is",
                  "start": 166.26,
                  "end": 166.42,
                  "confidence": 0.869
                },
                {
                  "text": "actually",
                  "start": 166.42,
                  "end": 166.88,
                  "confidence": 0.982
                },
                {
                  "text": "really",
                  "start": 166.88,
                  "end": 167.42,
                  "confidence": 0.636
                }
              ]
            },
            {
              "id": 68,
              "start": 167.52,
              "end": 170.0,
              "text": " a real coffee farmer, somebody just drew.",
              "no_speech_prob": 0.6980549693107605,
              "confidence": 0.65,
              "words": [
                {
                  "text": "a",
                  "start": 167.52,
                  "end": 167.68,
                  "confidence": 0.498
                },
                {
                  "text": "real",
                  "start": 167.68,
                  "end": 167.94,
                  "confidence": 0.967
                },
                {
                  "text": "coffee",
                  "start": 167.94,
                  "end": 168.48,
                  "confidence": 0.993
                },
                {
                  "text": "farmer,",
                  "start": 168.48,
                  "end": 169.0,
                  "confidence": 0.986
                },
                {
                  "text": "somebody",
                  "start": 169.22,
                  "end": 169.44,
                  "confidence": 0.447
                },
                {
                  "text": "just",
                  "start": 169.44,
                  "end": 169.66,
                  "confidence": 0.56
                },
                {
                  "text": "drew.",
                  "start": 169.66,
                  "end": 170.0,
                  "confidence": 0.416
                }
              ]
            }
          ]
        }
      ],
      "process_output_files": [
        "../../data/output/cd5f2dad-f63b-46ed-8076-c0499cae8e5f.json"
      ]
    }


We load in the text file output from `process_output_files` below. 


```python
# load in process output from file
with open(process_output["process_output_files"][0]) as f:
    print(json.dumps(json.load(f), indent=2))
```

    [
      {
        "transcript": " That's the episode looking at the great country of Columbia. We looked at some really basic facts. It's name, a bit of its history, the type of people that live there, land size, and all that jazz. But in this video, we're going to go into a little bit more of a detailed look. Yo, what is going on guys? Welcome back to F2D facts. The channel where I look at people cultures and places. My name is Dave Wouple, and today we are going to be looking more at Columbia and our Columbia part two video. Which just reminds me guys, this is part of our Columbia playlist. So put it down in the description box below, and I'll talk about that more in the video. But if you're new here, join me every single Monday to learn about new countries from around the world. You can do that by hitting that subscribe and that belt notification button. But let's get started. Learn about Columbia. So we all know Columbia is famous for its coffee, right? Yes, right. I know. You guys are sitting there going, five bucks says he's going to talk about coffee. Well, I am. That's right, because I got my van. You Columbia coffee right here. Boom advertisement. Yeah. Then I'm paying me for this. I'm care. So which might not know about coffee is yes, you probably already know that a lot of companies actually buy it up. Starbucks buys all had a coffee from Columbia. It's kind of like their favorite place to buy coffee. And kind of to pay tribute to that Starbucks when they're making their 1,000th store in 2016, they decided, yo, we're going to put it in Columbia. And this was in the town of Medellin, Columbia. Now here's the thing, when it comes to coffee in Columbia, they are the third largest producing and exporting coffee country in the world. The amount of coffee that is exported from Columbia equals about 810,000 metric tons or approximately 11.5 million bags. However, although it might be beaten by countries like Brazil, it is actually the number one or highest country for producing and growing a specific type of bean known as the Arab Beka bean. And I know coffee is really important when it comes to talking about Columbia, but you guys really don't know how important it is with its culture. Interesting fact that in 2007, major spots equaling a buffer zone of approximately 207,000 hectares, which are called the coffee cultural landscape, were considered a UNESCO World Heritage Site. And also in 2007, the EU, the European Union, granted Colombian coffee a protected designation of origin status. Now interesting enough when it comes to the coffee in Columbia, believe it or not, it is not actually native to the country. It's come from somewhere else, not really an invasive species because it's very much welcomed. Now you may have also seen this guy on many different Colombian coffee brands. Now his name is Juan Valdez. Now some people think that this guy is actually really a real coffee farmer, somebody just drew.",
        "timestamped_transcript": [
          {
            "id": 0,
            "start": 0.0,
            "end": 2.12,
            "text": " That's the episode looking at the great country of Columbia.",
            "no_speech_prob": 0.5627443194389343,
            "confidence": 0.547,
            "words": [
              {
                "text": "That's",
                "start": 0.0,
                "end": 0.38,
                "confidence": 0.234
              },
              {
                "text": "the",
                "start": 0.38,
                "end": 0.4,
                "confidence": 0.461
              },
              {
                "text": "episode",
                "start": 0.4,
                "end": 0.5,
                "confidence": 0.104
              },
              {
                "text": "looking",
                "start": 0.5,
                "end": 0.8,
                "confidence": 0.861
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
                "confidence": 0.98
              },
              {
                "text": "great",
                "start": 1.1,
                "end": 1.32,
                "confidence": 0.975
              },
              {
                "text": "country",
                "start": 1.32,
                "end": 1.66,
                "confidence": 0.985
              },
              {
                "text": "of",
                "start": 1.66,
                "end": 1.78,
                "confidence": 0.982
              },
              {
                "text": "Columbia.",
                "start": 1.78,
                "end": 2.12,
                "confidence": 0.624
              }
            ]
          },
          {
            "id": 1,
            "start": 2.18,
            "end": 4.34,
            "text": " We looked at some really basic facts.",
            "no_speech_prob": 0.5627443194389343,
            "confidence": 0.906,
            "words": [
              {
                "text": "We",
                "start": 2.18,
                "end": 2.34,
                "confidence": 0.994
              },
              {
                "text": "looked",
                "start": 2.34,
                "end": 2.6,
                "confidence": 0.983
              },
              {
                "text": "at",
                "start": 2.6,
                "end": 2.78,
                "confidence": 0.998
              },
              {
                "text": "some",
                "start": 2.78,
                "end": 3.0,
                "confidence": 0.996
              },
              {
                "text": "really",
                "start": 3.0,
                "end": 3.28,
                "confidence": 0.988
              },
              {
                "text": "basic",
                "start": 3.28,
                "end": 3.88,
                "confidence": 0.527
              },
              {
                "text": "facts.",
                "start": 3.88,
                "end": 4.34,
                "confidence": 0.992
              }
            ]
          },
          {
            "id": 2,
            "start": 4.34,
            "end": 6.8,
            "text": " It's name, a bit of its history, the type of people",
            "no_speech_prob": 0.5627443194389343,
            "confidence": 0.905,
            "words": [
              {
                "text": "It's",
                "start": 4.34,
                "end": 4.6,
                "confidence": 0.899
              },
              {
                "text": "name,",
                "start": 4.6,
                "end": 4.94,
                "confidence": 0.939
              },
              {
                "text": "a",
                "start": 4.96,
                "end": 5.08,
                "confidence": 0.981
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
                "confidence": 0.896
              },
              {
                "text": "history,",
                "start": 5.48,
                "end": 5.9,
                "confidence": 0.999
              },
              {
                "text": "the",
                "start": 6.02,
                "end": 6.38,
                "confidence": 0.494
              },
              {
                "text": "type",
                "start": 6.38,
                "end": 6.52,
                "confidence": 0.974
              },
              {
                "text": "of",
                "start": 6.52,
                "end": 6.62,
                "confidence": 0.963
              },
              {
                "text": "people",
                "start": 6.62,
                "end": 6.8,
                "confidence": 0.994
              }
            ]
          },
          {
            "id": 3,
            "start": 6.84,
            "end": 9.22,
            "text": " that live there, land size, and all that jazz.",
            "no_speech_prob": 0.5627443194389343,
            "confidence": 0.872,
            "words": [
              {
                "text": "that",
                "start": 6.84,
                "end": 6.98,
                "confidence": 0.999
              },
              {
                "text": "live",
                "start": 6.98,
                "end": 7.22,
                "confidence": 0.607
              },
              {
                "text": "there,",
                "start": 7.22,
                "end": 7.46,
                "confidence": 0.946
              },
              {
                "text": "land",
                "start": 7.54,
                "end": 7.86,
                "confidence": 0.695
              },
              {
                "text": "size,",
                "start": 7.86,
                "end": 8.28,
                "confidence": 0.767
              },
              {
                "text": "and",
                "start": 8.32,
                "end": 8.44,
                "confidence": 0.984
              },
              {
                "text": "all",
                "start": 8.44,
                "end": 8.68,
                "confidence": 0.998
              },
              {
                "text": "that",
                "start": 8.68,
                "end": 8.86,
                "confidence": 0.974
              },
              {
                "text": "jazz.",
                "start": 8.86,
                "end": 9.22,
                "confidence": 0.994
              }
            ]
          },
          {
            "id": 4,
            "start": 9.52,
            "end": 11.61,
            "text": " But in this video, we're going to go into a little bit more",
            "no_speech_prob": 0.5627443194389343,
            "confidence": 0.896,
            "words": [
              {
                "text": "But",
                "start": 9.52,
                "end": 9.64,
                "confidence": 0.998
              },
              {
                "text": "in",
                "start": 9.64,
                "end": 9.72,
                "confidence": 0.992
              },
              {
                "text": "this",
                "start": 9.72,
                "end": 9.84,
                "confidence": 0.999
              },
              {
                "text": "video,",
                "start": 9.84,
                "end": 10.08,
                "confidence": 0.999
              },
              {
                "text": "we're",
                "start": 10.1,
                "end": 10.24,
                "confidence": 0.992
              },
              {
                "text": "going",
                "start": 10.24,
                "end": 10.34,
                "confidence": 0.501
              },
              {
                "text": "to",
                "start": 10.34,
                "end": 10.4,
                "confidence": 0.952
              },
              {
                "text": "go",
                "start": 10.4,
                "end": 10.48,
                "confidence": 0.978
              },
              {
                "text": "into",
                "start": 10.48,
                "end": 10.7,
                "confidence": 0.941
              },
              {
                "text": "a",
                "start": 10.7,
                "end": 10.9,
                "confidence": 0.647
              },
              {
                "text": "little",
                "start": 10.9,
                "end": 11.14,
                "confidence": 0.925
              },
              {
                "text": "bit",
                "start": 11.14,
                "end": 11.3,
                "confidence": 0.968
              },
              {
                "text": "more",
                "start": 11.3,
                "end": 11.61,
                "confidence": 0.872
              }
            ]
          },
          {
            "id": 5,
            "start": 11.61,
            "end": 12.56,
            "text": " of a detailed look.",
            "no_speech_prob": 0.5627443194389343,
            "confidence": 0.997,
            "words": [
              {
                "text": "of",
                "start": 11.61,
                "end": 11.76,
                "confidence": 0.999
              },
              {
                "text": "a",
                "start": 11.76,
                "end": 11.88,
                "confidence": 0.994
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
                "confidence": 0.997
              }
            ]
          },
          {
            "id": 6,
            "start": 12.82,
            "end": 14.28,
            "text": " Yo, what is going on guys?",
            "no_speech_prob": 0.5627443194389343,
            "confidence": 0.899,
            "words": [
              {
                "text": "Yo,",
                "start": 12.82,
                "end": 13.02,
                "confidence": 0.843
              },
              {
                "text": "what",
                "start": 13.22,
                "end": 13.34,
                "confidence": 0.995
              },
              {
                "text": "is",
                "start": 13.34,
                "end": 13.48,
                "confidence": 0.985
              },
              {
                "text": "going",
                "start": 13.48,
                "end": 13.7,
                "confidence": 0.979
              },
              {
                "text": "on",
                "start": 13.7,
                "end": 13.9,
                "confidence": 1.0
              },
              {
                "text": "guys?",
                "start": 13.9,
                "end": 14.28,
                "confidence": 0.651
              }
            ]
          },
          {
            "id": 7,
            "start": 14.34,
            "end": 15.7,
            "text": " Welcome back to F2D facts.",
            "no_speech_prob": 0.5627443194389343,
            "confidence": 0.703,
            "words": [
              {
                "text": "Welcome",
                "start": 14.34,
                "end": 14.6,
                "confidence": 0.988
              },
              {
                "text": "back",
                "start": 14.6,
                "end": 14.82,
                "confidence": 0.999
              },
              {
                "text": "to",
                "start": 14.82,
                "end": 14.98,
                "confidence": 0.988
              },
              {
                "text": "F2D",
                "start": 14.98,
                "end": 15.4,
                "confidence": 0.603
              },
              {
                "text": "facts.",
                "start": 15.4,
                "end": 15.7,
                "confidence": 0.397
              }
            ]
          },
          {
            "id": 8,
            "start": 15.7,
            "end": 17.33,
            "text": " The channel where I look at people cultures and places.",
            "no_speech_prob": 0.5627443194389343,
            "confidence": 0.843,
            "words": [
              {
                "text": "The",
                "start": 15.7,
                "end": 15.86,
                "confidence": 0.557
              },
              {
                "text": "channel",
                "start": 15.86,
                "end": 16.02,
                "confidence": 0.887
              },
              {
                "text": "where",
                "start": 16.02,
                "end": 16.16,
                "confidence": 0.992
              },
              {
                "text": "I",
                "start": 16.16,
                "end": 16.24,
                "confidence": 0.991
              },
              {
                "text": "look",
                "start": 16.24,
                "end": 16.36,
                "confidence": 0.995
              },
              {
                "text": "at",
                "start": 16.36,
                "end": 16.46,
                "confidence": 0.992
              },
              {
                "text": "people",
                "start": 16.46,
                "end": 16.64,
                "confidence": 0.961
              },
              {
                "text": "cultures",
                "start": 16.64,
                "end": 16.98,
                "confidence": 0.569
              },
              {
                "text": "and",
                "start": 16.98,
                "end": 17.14,
                "confidence": 0.692
              },
              {
                "text": "places.",
                "start": 17.14,
                "end": 17.33,
                "confidence": 0.995
              }
            ]
          },
          {
            "id": 9,
            "start": 17.33,
            "end": 22.38,
            "text": " My name is Dave Wouple, and today we are going to be",
            "no_speech_prob": 0.5627443194389343,
            "confidence": 0.75,
            "words": [
              {
                "text": "My",
                "start": 17.33,
                "end": 17.84,
                "confidence": 0.994
              },
              {
                "text": "name",
                "start": 17.84,
                "end": 18.62,
                "confidence": 1.0
              },
              {
                "text": "is",
                "start": 18.62,
                "end": 18.98,
                "confidence": 0.99
              },
              {
                "text": "Dave",
                "start": 18.98,
                "end": 19.38,
                "confidence": 0.986
              },
              {
                "text": "Wouple,",
                "start": 19.38,
                "end": 19.98,
                "confidence": 0.399
              },
              {
                "text": "and",
                "start": 20.04,
                "end": 20.38,
                "confidence": 0.964
              },
              {
                "text": "today",
                "start": 20.38,
                "end": 21.06,
                "confidence": 0.996
              },
              {
                "text": "we",
                "start": 21.06,
                "end": 21.64,
                "confidence": 0.779
              },
              {
                "text": "are",
                "start": 21.64,
                "end": 22.06,
                "confidence": 0.928
              },
              {
                "text": "going",
                "start": 22.06,
                "end": 22.2,
                "confidence": 0.656
              },
              {
                "text": "to",
                "start": 22.2,
                "end": 22.24,
                "confidence": 0.636
              },
              {
                "text": "be",
                "start": 22.24,
                "end": 22.38,
                "confidence": 0.99
              }
            ]
          },
          {
            "id": 10,
            "start": 22.38,
            "end": 25.22,
            "text": " looking more at Columbia and our Columbia part two video.",
            "no_speech_prob": 0.5627443194389343,
            "confidence": 0.728,
            "words": [
              {
                "text": "looking",
                "start": 22.38,
                "end": 22.62,
                "confidence": 0.997
              },
              {
                "text": "more",
                "start": 22.62,
                "end": 22.96,
                "confidence": 0.972
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
                "confidence": 0.98
              },
              {
                "text": "and",
                "start": 23.64,
                "end": 23.86,
                "confidence": 0.393
              },
              {
                "text": "our",
                "start": 23.86,
                "end": 24.02,
                "confidence": 0.584
              },
              {
                "text": "Columbia",
                "start": 24.02,
                "end": 24.24,
                "confidence": 0.982
              },
              {
                "text": "part",
                "start": 24.24,
                "end": 24.5,
                "confidence": 0.391
              },
              {
                "text": "two",
                "start": 24.5,
                "end": 24.8,
                "confidence": 0.525
              },
              {
                "text": "video.",
                "start": 24.8,
                "end": 25.22,
                "confidence": 0.95
              }
            ]
          },
          {
            "id": 11,
            "start": 25.72,
            "end": 28.8,
            "text": " Which just reminds me guys, this is part of our Columbia playlist.",
            "no_speech_prob": 0.5627443194389343,
            "confidence": 0.909,
            "words": [
              {
                "text": "Which",
                "start": 25.72,
                "end": 25.96,
                "confidence": 0.988
              },
              {
                "text": "just",
                "start": 25.96,
                "end": 26.24,
                "confidence": 0.982
              },
              {
                "text": "reminds",
                "start": 26.24,
                "end": 26.66,
                "confidence": 0.996
              },
              {
                "text": "me",
                "start": 26.66,
                "end": 26.86,
                "confidence": 0.932
              },
              {
                "text": "guys,",
                "start": 26.86,
                "end": 27.02,
                "confidence": 0.878
              },
              {
                "text": "this",
                "start": 27.14,
                "end": 27.24,
                "confidence": 0.946
              },
              {
                "text": "is",
                "start": 27.24,
                "end": 27.32,
                "confidence": 0.976
              },
              {
                "text": "part",
                "start": 27.32,
                "end": 27.54,
                "confidence": 0.984
              },
              {
                "text": "of",
                "start": 27.54,
                "end": 27.66,
                "confidence": 0.886
              },
              {
                "text": "our",
                "start": 27.66,
                "end": 27.82,
                "confidence": 0.98
              },
              {
                "text": "Columbia",
                "start": 27.82,
                "end": 28.24,
                "confidence": 0.989
              },
              {
                "text": "playlist.",
                "start": 28.24,
                "end": 28.8,
                "confidence": 0.516
              }
            ]
          },
          {
            "id": 12,
            "start": 28.92,
            "end": 30.91,
            "text": " So put it down in the description box below, and I'll talk about",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.773,
            "words": [
              {
                "text": "So",
                "start": 28.92,
                "end": 28.98,
                "confidence": 0.384
              },
              {
                "text": "put",
                "start": 28.98,
                "end": 29.06,
                "confidence": 0.595
              },
              {
                "text": "it",
                "start": 29.06,
                "end": 29.18,
                "confidence": 0.992
              },
              {
                "text": "down",
                "start": 29.18,
                "end": 29.38,
                "confidence": 0.997
              },
              {
                "text": "in",
                "start": 29.38,
                "end": 29.52,
                "confidence": 0.542
              },
              {
                "text": "the",
                "start": 29.52,
                "end": 29.6,
                "confidence": 0.876
              },
              {
                "text": "description",
                "start": 29.6,
                "end": 29.84,
                "confidence": 0.999
              },
              {
                "text": "box",
                "start": 29.84,
                "end": 30.12,
                "confidence": 0.984
              },
              {
                "text": "below,",
                "start": 30.12,
                "end": 30.34,
                "confidence": 0.99
              },
              {
                "text": "and",
                "start": 30.44,
                "end": 30.54,
                "confidence": 0.542
              },
              {
                "text": "I'll",
                "start": 30.54,
                "end": 30.64,
                "confidence": 0.898
              },
              {
                "text": "talk",
                "start": 30.64,
                "end": 30.8,
                "confidence": 0.824
              },
              {
                "text": "about",
                "start": 30.8,
                "end": 30.91,
                "confidence": 0.721
              }
            ]
          },
          {
            "id": 13,
            "start": 30.91,
            "end": 32.3,
            "text": " that more in the video.",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.704,
            "words": [
              {
                "text": "that",
                "start": 30.91,
                "end": 31.08,
                "confidence": 0.912
              },
              {
                "text": "more",
                "start": 31.08,
                "end": 31.28,
                "confidence": 0.985
              },
              {
                "text": "in",
                "start": 31.28,
                "end": 31.62,
                "confidence": 0.422
              },
              {
                "text": "the",
                "start": 31.62,
                "end": 31.84,
                "confidence": 0.987
              },
              {
                "text": "video.",
                "start": 31.84,
                "end": 32.3,
                "confidence": 0.463
              }
            ]
          },
          {
            "id": 14,
            "start": 32.72,
            "end": 35.02,
            "text": " But if you're new here, join me every single Monday to learn",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.954,
            "words": [
              {
                "text": "But",
                "start": 32.72,
                "end": 32.84,
                "confidence": 0.99
              },
              {
                "text": "if",
                "start": 32.84,
                "end": 32.94,
                "confidence": 0.986
              },
              {
                "text": "you're",
                "start": 32.94,
                "end": 33.1,
                "confidence": 0.976
              },
              {
                "text": "new",
                "start": 33.1,
                "end": 33.22,
                "confidence": 0.995
              },
              {
                "text": "here,",
                "start": 33.22,
                "end": 33.56,
                "confidence": 0.995
              },
              {
                "text": "join",
                "start": 33.68,
                "end": 33.92,
                "confidence": 0.952
              },
              {
                "text": "me",
                "start": 33.92,
                "end": 34.06,
                "confidence": 0.998
              },
              {
                "text": "every",
                "start": 34.06,
                "end": 34.24,
                "confidence": 0.867
              },
              {
                "text": "single",
                "start": 34.24,
                "end": 34.46,
                "confidence": 0.997
              },
              {
                "text": "Monday",
                "start": 34.46,
                "end": 34.7,
                "confidence": 0.94
              },
              {
                "text": "to",
                "start": 34.7,
                "end": 34.84,
                "confidence": 0.857
              },
              {
                "text": "learn",
                "start": 34.84,
                "end": 35.02,
                "confidence": 0.887
              }
            ]
          },
          {
            "id": 15,
            "start": 35.02,
            "end": 36.38,
            "text": " about new countries from around the world.",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.992,
            "words": [
              {
                "text": "about",
                "start": 35.02,
                "end": 35.18,
                "confidence": 0.999
              },
              {
                "text": "new",
                "start": 35.18,
                "end": 35.38,
                "confidence": 0.994
              },
              {
                "text": "countries",
                "start": 35.38,
                "end": 35.78,
                "confidence": 0.993
              },
              {
                "text": "from",
                "start": 35.78,
                "end": 35.96,
                "confidence": 0.982
              },
              {
                "text": "around",
                "start": 35.96,
                "end": 36.22,
                "confidence": 0.996
              },
              {
                "text": "the",
                "start": 36.22,
                "end": 36.34,
                "confidence": 0.982
              },
              {
                "text": "world.",
                "start": 36.34,
                "end": 36.38,
                "confidence": 0.998
              }
            ]
          },
          {
            "id": 16,
            "start": 36.38,
            "end": 38.4,
            "text": " You can do that by hitting that subscribe and that belt",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.852,
            "words": [
              {
                "text": "You",
                "start": 36.38,
                "end": 36.62,
                "confidence": 0.991
              },
              {
                "text": "can",
                "start": 36.62,
                "end": 36.72,
                "confidence": 0.997
              },
              {
                "text": "do",
                "start": 36.72,
                "end": 36.84,
                "confidence": 0.999
              },
              {
                "text": "that",
                "start": 36.84,
                "end": 36.96,
                "confidence": 0.998
              },
              {
                "text": "by",
                "start": 36.96,
                "end": 37.16,
                "confidence": 0.962
              },
              {
                "text": "hitting",
                "start": 37.16,
                "end": 37.36,
                "confidence": 0.916
              },
              {
                "text": "that",
                "start": 37.36,
                "end": 37.48,
                "confidence": 0.994
              },
              {
                "text": "subscribe",
                "start": 37.48,
                "end": 37.92,
                "confidence": 0.96
              },
              {
                "text": "and",
                "start": 37.92,
                "end": 38.12,
                "confidence": 0.541
              },
              {
                "text": "that",
                "start": 38.12,
                "end": 38.32,
                "confidence": 0.886
              },
              {
                "text": "belt",
                "start": 38.32,
                "end": 38.4,
                "confidence": 0.432
              }
            ]
          },
          {
            "id": 17,
            "start": 38.4,
            "end": 39.23,
            "text": " notification button.",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.953,
            "words": [
              {
                "text": "notification",
                "start": 38.4,
                "end": 39.02,
                "confidence": 0.909
              },
              {
                "text": "button.",
                "start": 39.02,
                "end": 39.23,
                "confidence": 0.999
              }
            ]
          },
          {
            "id": 18,
            "start": 39.23,
            "end": 41.5,
            "text": " But let's get started.",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.845,
            "words": [
              {
                "text": "But",
                "start": 39.23,
                "end": 40.36,
                "confidence": 0.996
              },
              {
                "text": "let's",
                "start": 40.36,
                "end": 41.02,
                "confidence": 0.664
              },
              {
                "text": "get",
                "start": 41.02,
                "end": 41.18,
                "confidence": 0.985
              },
              {
                "text": "started.",
                "start": 41.18,
                "end": 41.5,
                "confidence": 0.998
              }
            ]
          },
          {
            "id": 19,
            "start": 41.5,
            "end": 42.7,
            "text": " Learn about Columbia.",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.765,
            "words": [
              {
                "text": "Learn",
                "start": 41.5,
                "end": 42.14,
                "confidence": 0.489
              },
              {
                "text": "about",
                "start": 42.14,
                "end": 42.32,
                "confidence": 0.93
              },
              {
                "text": "Columbia.",
                "start": 42.32,
                "end": 42.7,
                "confidence": 0.986
              }
            ]
          },
          {
            "id": 20,
            "start": 43.24,
            "end": 46.6,
            "text": " So we all know Columbia is famous for its coffee, right?",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.903,
            "words": [
              {
                "text": "So",
                "start": 43.24,
                "end": 43.36,
                "confidence": 0.997
              },
              {
                "text": "we",
                "start": 43.36,
                "end": 43.52,
                "confidence": 0.968
              },
              {
                "text": "all",
                "start": 43.52,
                "end": 43.68,
                "confidence": 0.999
              },
              {
                "text": "know",
                "start": 43.68,
                "end": 43.94,
                "confidence": 0.999
              },
              {
                "text": "Columbia",
                "start": 43.94,
                "end": 44.56,
                "confidence": 0.453
              },
              {
                "text": "is",
                "start": 44.56,
                "end": 44.86,
                "confidence": 0.995
              },
              {
                "text": "famous",
                "start": 44.86,
                "end": 45.22,
                "confidence": 0.996
              },
              {
                "text": "for",
                "start": 45.22,
                "end": 45.62,
                "confidence": 0.999
              },
              {
                "text": "its",
                "start": 45.62,
                "end": 45.8,
                "confidence": 0.867
              },
              {
                "text": "coffee,",
                "start": 45.8,
                "end": 46.26,
                "confidence": 0.88
              },
              {
                "text": "right?",
                "start": 46.34,
                "end": 46.6,
                "confidence": 0.987
              }
            ]
          },
          {
            "id": 21,
            "start": 46.84,
            "end": 47.42,
            "text": " Yes, right.",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.983,
            "words": [
              {
                "text": "Yes,",
                "start": 46.84,
                "end": 47.08,
                "confidence": 0.989
              },
              {
                "text": "right.",
                "start": 47.28,
                "end": 47.42,
                "confidence": 0.978
              }
            ]
          },
          {
            "id": 22,
            "start": 47.54,
            "end": 47.75,
            "text": " I know.",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.975,
            "words": [
              {
                "text": "I",
                "start": 47.54,
                "end": 47.72,
                "confidence": 0.951
              },
              {
                "text": "know.",
                "start": 47.72,
                "end": 47.75,
                "confidence": 0.999
              }
            ]
          },
          {
            "id": 23,
            "start": 47.75,
            "end": 49.87,
            "text": " You guys are sitting there going, five bucks says",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.831,
            "words": [
              {
                "text": "You",
                "start": 47.75,
                "end": 48.14,
                "confidence": 0.98
              },
              {
                "text": "guys",
                "start": 48.14,
                "end": 48.28,
                "confidence": 0.998
              },
              {
                "text": "are",
                "start": 48.28,
                "end": 48.44,
                "confidence": 0.89
              },
              {
                "text": "sitting",
                "start": 48.44,
                "end": 48.62,
                "confidence": 0.969
              },
              {
                "text": "there",
                "start": 48.62,
                "end": 48.72,
                "confidence": 0.973
              },
              {
                "text": "going,",
                "start": 48.72,
                "end": 48.84,
                "confidence": 0.948
              },
              {
                "text": "five",
                "start": 48.92,
                "end": 49.5,
                "confidence": 0.266
              },
              {
                "text": "bucks",
                "start": 49.5,
                "end": 49.72,
                "confidence": 0.976
              },
              {
                "text": "says",
                "start": 49.72,
                "end": 49.87,
                "confidence": 0.932
              }
            ]
          },
          {
            "id": 24,
            "start": 49.87,
            "end": 50.77,
            "text": " he's going to talk about coffee.",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.858,
            "words": [
              {
                "text": "he's",
                "start": 49.87,
                "end": 50.02,
                "confidence": 0.65
              },
              {
                "text": "going",
                "start": 50.02,
                "end": 50.12,
                "confidence": 0.847
              },
              {
                "text": "to",
                "start": 50.12,
                "end": 50.22,
                "confidence": 0.997
              },
              {
                "text": "talk",
                "start": 50.22,
                "end": 50.38,
                "confidence": 0.992
              },
              {
                "text": "about",
                "start": 50.38,
                "end": 50.52,
                "confidence": 0.998
              },
              {
                "text": "coffee.",
                "start": 50.52,
                "end": 50.77,
                "confidence": 0.968
              }
            ]
          },
          {
            "id": 25,
            "start": 50.77,
            "end": 51.8,
            "text": " Well, I am.",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.988,
            "words": [
              {
                "text": "Well,",
                "start": 50.77,
                "end": 51.26,
                "confidence": 0.996
              },
              {
                "text": "I",
                "start": 51.44,
                "end": 51.58,
                "confidence": 0.991
              },
              {
                "text": "am.",
                "start": 51.58,
                "end": 51.8,
                "confidence": 0.975
              }
            ]
          },
          {
            "id": 26,
            "start": 52.18,
            "end": 53.18,
            "text": " That's right, because I got my van.",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.986,
            "words": [
              {
                "text": "That's",
                "start": 52.18,
                "end": 52.36,
                "confidence": 0.998
              },
              {
                "text": "right,",
                "start": 52.36,
                "end": 52.46,
                "confidence": 0.999
              },
              {
                "text": "because",
                "start": 52.52,
                "end": 52.68,
                "confidence": 0.998
              },
              {
                "text": "I",
                "start": 52.68,
                "end": 52.76,
                "confidence": 0.996
              },
              {
                "text": "got",
                "start": 52.76,
                "end": 52.9,
                "confidence": 0.968
              },
              {
                "text": "my",
                "start": 52.9,
                "end": 53.0,
                "confidence": 0.997
              },
              {
                "text": "van.",
                "start": 53.0,
                "end": 53.18,
                "confidence": 0.934
              }
            ]
          },
          {
            "id": 27,
            "start": 53.18,
            "end": 54.92,
            "text": " You Columbia coffee right here.",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.615,
            "words": [
              {
                "text": "You",
                "start": 53.18,
                "end": 53.62,
                "confidence": 0.461
              },
              {
                "text": "Columbia",
                "start": 53.62,
                "end": 53.96,
                "confidence": 0.658
              },
              {
                "text": "coffee",
                "start": 53.96,
                "end": 54.34,
                "confidence": 0.672
              },
              {
                "text": "right",
                "start": 54.34,
                "end": 54.68,
                "confidence": 0.435
              },
              {
                "text": "here.",
                "start": 54.68,
                "end": 54.92,
                "confidence": 0.997
              }
            ]
          },
          {
            "id": 28,
            "start": 55.26,
            "end": 56.34,
            "text": " Boom advertisement.",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.757,
            "words": [
              {
                "text": "Boom",
                "start": 55.26,
                "end": 55.58,
                "confidence": 0.971
              },
              {
                "text": "advertisement.",
                "start": 55.58,
                "end": 56.34,
                "confidence": 0.591
              }
            ]
          },
          {
            "id": 29,
            "start": 56.68,
            "end": 56.88,
            "text": " Yeah.",
            "no_speech_prob": 0.13539506494998932,
            "confidence": 0.863,
            "words": [
              {
                "text": "Yeah.",
                "start": 56.68,
                "end": 56.88,
                "confidence": 0.863
              }
            ]
          },
          {
            "id": 30,
            "start": 57.12,
            "end": 58.24,
            "text": " Then I'm paying me for this.",
            "no_speech_prob": 0.023453781381249428,
            "confidence": 0.68,
            "words": [
              {
                "text": "Then",
                "start": 57.12,
                "end": 57.28,
                "confidence": 0.118
              },
              {
                "text": "I'm",
                "start": 57.28,
                "end": 57.5,
                "confidence": 0.921
              },
              {
                "text": "paying",
                "start": 57.5,
                "end": 57.72,
                "confidence": 0.927
              },
              {
                "text": "me",
                "start": 57.72,
                "end": 57.9,
                "confidence": 0.728
              },
              {
                "text": "for",
                "start": 57.9,
                "end": 58.02,
                "confidence": 0.999
              },
              {
                "text": "this.",
                "start": 58.02,
                "end": 58.24,
                "confidence": 0.999
              }
            ]
          },
          {
            "id": 31,
            "start": 58.3,
            "end": 58.76,
            "text": " I'm care.",
            "no_speech_prob": 0.023453781381249428,
            "confidence": 0.894,
            "words": [
              {
                "text": "I'm",
                "start": 58.3,
                "end": 58.5,
                "confidence": 0.975
              },
              {
                "text": "care.",
                "start": 58.5,
                "end": 58.76,
                "confidence": 0.751
              }
            ]
          },
          {
            "id": 32,
            "start": 59.1,
            "end": 61.4,
            "text": " So which might not know about coffee is yes, you probably",
            "no_speech_prob": 0.023453781381249428,
            "confidence": 0.853,
            "words": [
              {
                "text": "So",
                "start": 59.1,
                "end": 59.18,
                "confidence": 0.996
              },
              {
                "text": "which",
                "start": 59.18,
                "end": 59.3,
                "confidence": 0.656
              },
              {
                "text": "might",
                "start": 59.3,
                "end": 59.48,
                "confidence": 0.665
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
                "confidence": 0.991
              },
              {
                "text": "about",
                "start": 59.82,
                "end": 60.08,
                "confidence": 0.997
              },
              {
                "text": "coffee",
                "start": 60.08,
                "end": 60.52,
                "confidence": 0.984
              },
              {
                "text": "is",
                "start": 60.52,
                "end": 60.76,
                "confidence": 0.85
              },
              {
                "text": "yes,",
                "start": 60.76,
                "end": 60.96,
                "confidence": 0.846
              },
              {
                "text": "you",
                "start": 61.02,
                "end": 61.12,
                "confidence": 0.901
              },
              {
                "text": "probably",
                "start": 61.12,
                "end": 61.4,
                "confidence": 0.636
              }
            ]
          },
          {
            "id": 33,
            "start": 61.48,
            "end": 63.46,
            "text": " already know that a lot of companies actually",
            "no_speech_prob": 0.023453781381249428,
            "confidence": 0.977,
            "words": [
              {
                "text": "already",
                "start": 61.48,
                "end": 61.7,
                "confidence": 0.997
              },
              {
                "text": "know",
                "start": 61.7,
                "end": 61.9,
                "confidence": 0.997
              },
              {
                "text": "that",
                "start": 61.9,
                "end": 62.12,
                "confidence": 0.886
              },
              {
                "text": "a",
                "start": 62.12,
                "end": 62.24,
                "confidence": 0.993
              },
              {
                "text": "lot",
                "start": 62.24,
                "end": 62.4,
                "confidence": 0.996
              },
              {
                "text": "of",
                "start": 62.4,
                "end": 62.48,
                "confidence": 0.995
              },
              {
                "text": "companies",
                "start": 62.48,
                "end": 62.98,
                "confidence": 0.984
              },
              {
                "text": "actually",
                "start": 62.98,
                "end": 63.46,
                "confidence": 0.976
              }
            ]
          },
          {
            "id": 34,
            "start": 63.52,
            "end": 64.02,
            "text": " buy it up.",
            "no_speech_prob": 0.023453781381249428,
            "confidence": 0.877,
            "words": [
              {
                "text": "buy",
                "start": 63.52,
                "end": 63.76,
                "confidence": 0.679
              },
              {
                "text": "it",
                "start": 63.76,
                "end": 63.86,
                "confidence": 0.993
              },
              {
                "text": "up.",
                "start": 63.86,
                "end": 64.02,
                "confidence": 0.999
              }
            ]
          },
          {
            "id": 35,
            "start": 64.32,
            "end": 67.2,
            "text": " Starbucks buys all had a coffee from Columbia.",
            "no_speech_prob": 0.023453781381249428,
            "confidence": 0.772,
            "words": [
              {
                "text": "Starbucks",
                "start": 64.32,
                "end": 64.76,
                "confidence": 0.77
              },
              {
                "text": "buys",
                "start": 64.76,
                "end": 65.18,
                "confidence": 0.982
              },
              {
                "text": "all",
                "start": 65.18,
                "end": 65.58,
                "confidence": 0.758
              },
              {
                "text": "had",
                "start": 65.58,
                "end": 65.76,
                "confidence": 0.237
              },
              {
                "text": "a",
                "start": 65.76,
                "end": 65.92,
                "confidence": 0.989
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
                "confidence": 0.986
              },
              {
                "text": "Columbia.",
                "start": 66.6,
                "end": 67.2,
                "confidence": 0.962
              }
            ]
          },
          {
            "id": 36,
            "start": 67.7,
            "end": 69.68,
            "text": " It's kind of like their favorite place to buy coffee.",
            "no_speech_prob": 0.023453781381249428,
            "confidence": 0.95,
            "words": [
              {
                "text": "It's",
                "start": 67.7,
                "end": 67.84,
                "confidence": 0.971
              },
              {
                "text": "kind",
                "start": 67.84,
                "end": 67.94,
                "confidence": 0.902
              },
              {
                "text": "of",
                "start": 67.94,
                "end": 68.0,
                "confidence": 0.992
              },
              {
                "text": "like",
                "start": 68.0,
                "end": 68.14,
                "confidence": 0.997
              },
              {
                "text": "their",
                "start": 68.14,
                "end": 68.22,
                "confidence": 0.752
              },
              {
                "text": "favorite",
                "start": 68.22,
                "end": 68.44,
                "confidence": 0.973
              },
              {
                "text": "place",
                "start": 68.44,
                "end": 68.66,
                "confidence": 0.991
              },
              {
                "text": "to",
                "start": 68.66,
                "end": 68.84,
                "confidence": 0.96
              },
              {
                "text": "buy",
                "start": 68.84,
                "end": 69.22,
                "confidence": 0.994
              },
              {
                "text": "coffee.",
                "start": 69.22,
                "end": 69.68,
                "confidence": 0.979
              }
            ]
          },
          {
            "id": 37,
            "start": 70.02,
            "end": 73.08,
            "text": " And kind of to pay tribute to that Starbucks when they're",
            "no_speech_prob": 0.023453781381249428,
            "confidence": 0.771,
            "words": [
              {
                "text": "And",
                "start": 70.02,
                "end": 70.18,
                "confidence": 0.992
              },
              {
                "text": "kind",
                "start": 70.18,
                "end": 70.36,
                "confidence": 0.61
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
                "end": 70.62,
                "confidence": 0.978
              },
              {
                "text": "pay",
                "start": 70.62,
                "end": 70.9,
                "confidence": 0.997
              },
              {
                "text": "tribute",
                "start": 70.9,
                "end": 71.34,
                "confidence": 0.999
              },
              {
                "text": "to",
                "start": 71.34,
                "end": 71.6,
                "confidence": 0.987
              },
              {
                "text": "that",
                "start": 71.6,
                "end": 71.92,
                "confidence": 0.99
              },
              {
                "text": "Starbucks",
                "start": 71.92,
                "end": 72.72,
                "confidence": 0.684
              },
              {
                "text": "when",
                "start": 72.72,
                "end": 72.98,
                "confidence": 0.585
              },
              {
                "text": "they're",
                "start": 72.98,
                "end": 73.08,
                "confidence": 0.437
              }
            ]
          },
          {
            "id": 38,
            "start": 73.08,
            "end": 77.51,
            "text": " making their 1,000th store in 2016, they decided,",
            "no_speech_prob": 0.023453781381249428,
            "confidence": 0.917,
            "words": [
              {
                "text": "making",
                "start": 73.08,
                "end": 73.42,
                "confidence": 0.995
              },
              {
                "text": "their",
                "start": 73.42,
                "end": 73.7,
                "confidence": 0.994
              },
              {
                "text": "1,000th",
                "start": 73.7,
                "end": 74.58,
                "confidence": 0.843
              },
              {
                "text": "store",
                "start": 74.58,
                "end": 74.9,
                "confidence": 0.981
              },
              {
                "text": "in",
                "start": 74.9,
                "end": 75.12,
                "confidence": 0.994
              },
              {
                "text": "2016,",
                "start": 75.12,
                "end": 76.42,
                "confidence": 0.993
              },
              {
                "text": "they",
                "start": 76.62,
                "end": 77.06,
                "confidence": 0.817
              },
              {
                "text": "decided,",
                "start": 77.06,
                "end": 77.51,
                "confidence": 0.981
              }
            ]
          },
          {
            "id": 39,
            "start": 77.51,
            "end": 79.32,
            "text": " yo, we're going to put it in Columbia.",
            "no_speech_prob": 0.023453781381249428,
            "confidence": 0.943,
            "words": [
              {
                "text": "yo,",
                "start": 77.51,
                "end": 77.96,
                "confidence": 0.639
              },
              {
                "text": "we're",
                "start": 77.98,
                "end": 78.22,
                "confidence": 0.994
              },
              {
                "text": "going",
                "start": 78.22,
                "end": 78.36,
                "confidence": 0.954
              },
              {
                "text": "to",
                "start": 78.36,
                "end": 78.46,
                "confidence": 0.999
              },
              {
                "text": "put",
                "start": 78.46,
                "end": 78.58,
                "confidence": 0.999
              },
              {
                "text": "it",
                "start": 78.58,
                "end": 78.72,
                "confidence": 0.995
              },
              {
                "text": "in",
                "start": 78.72,
                "end": 78.88,
                "confidence": 0.998
              },
              {
                "text": "Columbia.",
                "start": 78.88,
                "end": 79.32,
                "confidence": 0.986
              }
            ]
          },
          {
            "id": 40,
            "start": 79.32,
            "end": 82.28,
            "text": " And this was in the town of Medellin, Columbia.",
            "no_speech_prob": 0.023453781381249428,
            "confidence": 0.905,
            "words": [
              {
                "text": "And",
                "start": 79.32,
                "end": 79.98,
                "confidence": 0.997
              },
              {
                "text": "this",
                "start": 79.98,
                "end": 80.2,
                "confidence": 0.999
              },
              {
                "text": "was",
                "start": 80.2,
                "end": 80.42,
                "confidence": 0.997
              },
              {
                "text": "in",
                "start": 80.42,
                "end": 80.58,
                "confidence": 0.997
              },
              {
                "text": "the",
                "start": 80.58,
                "end": 80.72,
                "confidence": 0.997
              },
              {
                "text": "town",
                "start": 80.72,
                "end": 81.0,
                "confidence": 0.994
              },
              {
                "text": "of",
                "start": 81.0,
                "end": 81.22,
                "confidence": 0.999
              },
              {
                "text": "Medellin,",
                "start": 81.22,
                "end": 81.72,
                "confidence": 0.718
              },
              {
                "text": "Columbia.",
                "start": 81.76,
                "end": 82.28,
                "confidence": 0.92
              }
            ]
          },
          {
            "id": 41,
            "start": 82.6,
            "end": 85.38,
            "text": " Now here's the thing, when it comes to coffee in Columbia,",
            "no_speech_prob": 0.023453781381249428,
            "confidence": 0.924,
            "words": [
              {
                "text": "Now",
                "start": 82.6,
                "end": 82.76,
                "confidence": 0.993
              },
              {
                "text": "here's",
                "start": 82.76,
                "end": 83.06,
                "confidence": 0.758
              },
              {
                "text": "the",
                "start": 83.06,
                "end": 83.22,
                "confidence": 0.998
              },
              {
                "text": "thing,",
                "start": 83.22,
                "end": 83.38,
                "confidence": 0.999
              },
              {
                "text": "when",
                "start": 83.4,
                "end": 83.56,
                "confidence": 0.976
              },
              {
                "text": "it",
                "start": 83.56,
                "end": 83.68,
                "confidence": 0.996
              },
              {
                "text": "comes",
                "start": 83.68,
                "end": 84.08,
                "confidence": 0.995
              },
              {
                "text": "to",
                "start": 84.08,
                "end": 84.3,
                "confidence": 0.973
              },
              {
                "text": "coffee",
                "start": 84.3,
                "end": 84.68,
                "confidence": 0.862
              },
              {
                "text": "in",
                "start": 84.68,
                "end": 84.94,
                "confidence": 0.959
              },
              {
                "text": "Columbia,",
                "start": 84.94,
                "end": 85.38,
                "confidence": 0.876
              }
            ]
          },
          {
            "id": 42,
            "start": 85.44,
            "end": 90.5,
            "text": " they are the third largest producing and exporting coffee",
            "no_speech_prob": 0.0022646081633865833,
            "confidence": 0.826,
            "words": [
              {
                "text": "they",
                "start": 85.44,
                "end": 85.66,
                "confidence": 0.704
              },
              {
                "text": "are",
                "start": 85.66,
                "end": 85.88,
                "confidence": 0.991
              },
              {
                "text": "the",
                "start": 85.88,
                "end": 86.08,
                "confidence": 0.995
              },
              {
                "text": "third",
                "start": 86.08,
                "end": 86.64,
                "confidence": 0.988
              },
              {
                "text": "largest",
                "start": 86.64,
                "end": 87.5,
                "confidence": 0.976
              },
              {
                "text": "producing",
                "start": 87.5,
                "end": 88.76,
                "confidence": 0.672
              },
              {
                "text": "and",
                "start": 88.76,
                "end": 89.36,
                "confidence": 0.683
              },
              {
                "text": "exporting",
                "start": 89.36,
                "end": 89.92,
                "confidence": 0.912
              },
              {
                "text": "coffee",
                "start": 89.92,
                "end": 90.5,
                "confidence": 0.64
              }
            ]
          },
          {
            "id": 43,
            "start": 90.54,
            "end": 91.9,
            "text": " country in the world.",
            "no_speech_prob": 0.0022646081633865833,
            "confidence": 0.996,
            "words": [
              {
                "text": "country",
                "start": 90.54,
                "end": 90.9,
                "confidence": 0.992
              },
              {
                "text": "in",
                "start": 90.9,
                "end": 91.16,
                "confidence": 0.994
              },
              {
                "text": "the",
                "start": 91.16,
                "end": 91.32,
                "confidence": 0.999
              },
              {
                "text": "world.",
                "start": 91.32,
                "end": 91.9,
                "confidence": 1.0
              }
            ]
          },
          {
            "id": 44,
            "start": 92.22,
            "end": 95.07,
            "text": " The amount of coffee that is exported from Columbia equals",
            "no_speech_prob": 0.0022646081633865833,
            "confidence": 0.907,
            "words": [
              {
                "text": "The",
                "start": 92.22,
                "end": 92.34,
                "confidence": 0.998
              },
              {
                "text": "amount",
                "start": 92.34,
                "end": 92.6,
                "confidence": 1.0
              },
              {
                "text": "of",
                "start": 92.6,
                "end": 92.72,
                "confidence": 1.0
              },
              {
                "text": "coffee",
                "start": 92.72,
                "end": 93.06,
                "confidence": 0.999
              },
              {
                "text": "that",
                "start": 93.06,
                "end": 93.22,
                "confidence": 0.997
              },
              {
                "text": "is",
                "start": 93.22,
                "end": 93.34,
                "confidence": 0.976
              },
              {
                "text": "exported",
                "start": 93.34,
                "end": 93.86,
                "confidence": 0.99
              },
              {
                "text": "from",
                "start": 93.86,
                "end": 94.18,
                "confidence": 0.931
              },
              {
                "text": "Columbia",
                "start": 94.18,
                "end": 94.66,
                "confidence": 0.96
              },
              {
                "text": "equals",
                "start": 94.66,
                "end": 95.07,
                "confidence": 0.438
              }
            ]
          },
          {
            "id": 45,
            "start": 95.07,
            "end": 102.52,
            "text": " about 810,000 metric tons or approximately 11.5 million",
            "no_speech_prob": 0.0022646081633865833,
            "confidence": 0.819,
            "words": [
              {
                "text": "about",
                "start": 95.07,
                "end": 95.6,
                "confidence": 0.998
              },
              {
                "text": "810,000",
                "start": 95.6,
                "end": 98.18,
                "confidence": 0.796
              },
              {
                "text": "metric",
                "start": 98.18,
                "end": 98.68,
                "confidence": 0.964
              },
              {
                "text": "tons",
                "start": 98.68,
                "end": 99.26,
                "confidence": 0.972
              },
              {
                "text": "or",
                "start": 99.26,
                "end": 100.0,
                "confidence": 0.463
              },
              {
                "text": "approximately",
                "start": 100.0,
                "end": 100.66,
                "confidence": 0.983
              },
              {
                "text": "11.5",
                "start": 100.66,
                "end": 102.1,
                "confidence": 0.935
              },
              {
                "text": "million",
                "start": 102.1,
                "end": 102.52,
                "confidence": 0.534
              }
            ]
          },
          {
            "id": 46,
            "start": 102.66,
            "end": 102.94,
            "text": " bags.",
            "no_speech_prob": 0.0022646081633865833,
            "confidence": 0.986,
            "words": [
              {
                "text": "bags.",
                "start": 102.66,
                "end": 102.94,
                "confidence": 0.986
              }
            ]
          },
          {
            "id": 47,
            "start": 102.94,
            "end": 107.28,
            "text": " However, although it might be beaten by countries like Brazil,",
            "no_speech_prob": 0.0022646081633865833,
            "confidence": 0.975,
            "words": [
              {
                "text": "However,",
                "start": 102.94,
                "end": 103.62,
                "confidence": 0.997
              },
              {
                "text": "although",
                "start": 103.84,
                "end": 104.08,
                "confidence": 0.989
              },
              {
                "text": "it",
                "start": 104.08,
                "end": 104.4,
                "confidence": 0.977
              },
              {
                "text": "might",
                "start": 104.4,
                "end": 104.58,
                "confidence": 0.993
              },
              {
                "text": "be",
                "start": 104.58,
                "end": 104.82,
                "confidence": 0.996
              },
              {
                "text": "beaten",
                "start": 104.82,
                "end": 105.08,
                "confidence": 0.953
              },
              {
                "text": "by",
                "start": 105.08,
                "end": 105.36,
                "confidence": 0.981
              },
              {
                "text": "countries",
                "start": 105.36,
                "end": 105.96,
                "confidence": 0.975
              },
              {
                "text": "like",
                "start": 105.96,
                "end": 106.5,
                "confidence": 0.96
              },
              {
                "text": "Brazil,",
                "start": 106.5,
                "end": 107.28,
                "confidence": 0.933
              }
            ]
          },
          {
            "id": 48,
            "start": 107.92,
            "end": 111.12,
            "text": " it is actually the number one or highest country for producing",
            "no_speech_prob": 0.0022646081633865833,
            "confidence": 0.906,
            "words": [
              {
                "text": "it",
                "start": 107.92,
                "end": 108.04,
                "confidence": 0.996
              },
              {
                "text": "is",
                "start": 108.04,
                "end": 108.14,
                "confidence": 0.994
              },
              {
                "text": "actually",
                "start": 108.14,
                "end": 108.44,
                "confidence": 0.998
              },
              {
                "text": "the",
                "start": 108.44,
                "end": 108.68,
                "confidence": 0.986
              },
              {
                "text": "number",
                "start": 108.68,
                "end": 108.92,
                "confidence": 0.989
              },
              {
                "text": "one",
                "start": 108.92,
                "end": 109.18,
                "confidence": 0.979
              },
              {
                "text": "or",
                "start": 109.18,
                "end": 109.42,
                "confidence": 0.909
              },
              {
                "text": "highest",
                "start": 109.42,
                "end": 109.8,
                "confidence": 0.988
              },
              {
                "text": "country",
                "start": 109.8,
                "end": 110.22,
                "confidence": 0.872
              },
              {
                "text": "for",
                "start": 110.22,
                "end": 110.52,
                "confidence": 0.556
              },
              {
                "text": "producing",
                "start": 110.52,
                "end": 111.12,
                "confidence": 0.826
              }
            ]
          },
          {
            "id": 49,
            "start": 111.18,
            "end": 115.28,
            "text": " and growing a specific type of bean known as the Arab",
            "no_speech_prob": 0.0022646081633865833,
            "confidence": 0.821,
            "words": [
              {
                "text": "and",
                "start": 111.18,
                "end": 111.4,
                "confidence": 0.818
              },
              {
                "text": "growing",
                "start": 111.4,
                "end": 111.68,
                "confidence": 0.998
              },
              {
                "text": "a",
                "start": 111.68,
                "end": 112.24,
                "confidence": 0.949
              },
              {
                "text": "specific",
                "start": 112.24,
                "end": 112.86,
                "confidence": 0.998
              },
              {
                "text": "type",
                "start": 112.86,
                "end": 113.24,
                "confidence": 0.999
              },
              {
                "text": "of",
                "start": 113.24,
                "end": 113.42,
                "confidence": 0.991
              },
              {
                "text": "bean",
                "start": 113.42,
                "end": 114.0,
                "confidence": 0.598
              },
              {
                "text": "known",
                "start": 114.0,
                "end": 114.36,
                "confidence": 0.775
              },
              {
                "text": "as",
                "start": 114.36,
                "end": 114.66,
                "confidence": 0.775
              },
              {
                "text": "the",
                "start": 114.66,
                "end": 114.88,
                "confidence": 0.878
              },
              {
                "text": "Arab",
                "start": 114.88,
                "end": 115.28,
                "confidence": 0.473
              }
            ]
          },
          {
            "id": 50,
            "start": 115.32,
            "end": 116.3,
            "text": " Beka bean.",
            "no_speech_prob": 0.008894940838217735,
            "confidence": 0.348,
            "words": [
              {
                "text": "Beka",
                "start": 115.32,
                "end": 115.86,
                "confidence": 0.278
              },
              {
                "text": "bean.",
                "start": 115.86,
                "end": 116.3,
                "confidence": 0.546
              }
            ]
          },
          {
            "id": 51,
            "start": 116.68,
            "end": 119.55,
            "text": " And I know coffee is really important when it comes to talking",
            "no_speech_prob": 0.008894940838217735,
            "confidence": 0.917,
            "words": [
              {
                "text": "And",
                "start": 116.68,
                "end": 116.8,
                "confidence": 0.998
              },
              {
                "text": "I",
                "start": 116.8,
                "end": 116.9,
                "confidence": 0.997
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
                "confidence": 0.955
              },
              {
                "text": "is",
                "start": 117.5,
                "end": 117.8,
                "confidence": 0.998
              },
              {
                "text": "really",
                "start": 117.8,
                "end": 118.14,
                "confidence": 0.999
              },
              {
                "text": "important",
                "start": 118.14,
                "end": 118.72,
                "confidence": 0.989
              },
              {
                "text": "when",
                "start": 118.72,
                "end": 118.92,
                "confidence": 0.926
              },
              {
                "text": "it",
                "start": 118.92,
                "end": 119.02,
                "confidence": 0.841
              },
              {
                "text": "comes",
                "start": 119.02,
                "end": 119.26,
                "confidence": 0.923
              },
              {
                "text": "to",
                "start": 119.26,
                "end": 119.4,
                "confidence": 0.702
              },
              {
                "text": "talking",
                "start": 119.4,
                "end": 119.55,
                "confidence": 0.748
              }
            ]
          },
          {
            "id": 52,
            "start": 119.55,
            "end": 121.62,
            "text": " about Columbia, but you guys really don't know how important",
            "no_speech_prob": 0.008894940838217735,
            "confidence": 0.882,
            "words": [
              {
                "text": "about",
                "start": 119.55,
                "end": 119.72,
                "confidence": 0.994
              },
              {
                "text": "Columbia,",
                "start": 119.72,
                "end": 119.94,
                "confidence": 0.983
              },
              {
                "text": "but",
                "start": 120.04,
                "end": 120.16,
                "confidence": 0.974
              },
              {
                "text": "you",
                "start": 120.16,
                "end": 120.28,
                "confidence": 0.927
              },
              {
                "text": "guys",
                "start": 120.28,
                "end": 120.4,
                "confidence": 0.487
              },
              {
                "text": "really",
                "start": 120.4,
                "end": 120.62,
                "confidence": 0.983
              },
              {
                "text": "don't",
                "start": 120.62,
                "end": 120.78,
                "confidence": 0.99
              },
              {
                "text": "know",
                "start": 120.78,
                "end": 120.94,
                "confidence": 0.825
              },
              {
                "text": "how",
                "start": 120.94,
                "end": 121.12,
                "confidence": 0.773
              },
              {
                "text": "important",
                "start": 121.12,
                "end": 121.62,
                "confidence": 0.953
              }
            ]
          },
          {
            "id": 53,
            "start": 121.62,
            "end": 122.64,
            "text": " it is with its culture.",
            "no_speech_prob": 0.008894940838217735,
            "confidence": 0.974,
            "words": [
              {
                "text": "it",
                "start": 121.62,
                "end": 121.8,
                "confidence": 0.997
              },
              {
                "text": "is",
                "start": 121.8,
                "end": 121.94,
                "confidence": 1.0
              },
              {
                "text": "with",
                "start": 121.94,
                "end": 122.1,
                "confidence": 0.995
              },
              {
                "text": "its",
                "start": 122.1,
                "end": 122.28,
                "confidence": 0.888
              },
              {
                "text": "culture.",
                "start": 122.28,
                "end": 122.64,
                "confidence": 0.999
              }
            ]
          },
          {
            "id": 54,
            "start": 123.08,
            "end": 126.61,
            "text": " Interesting fact that in 2007, major spots",
            "no_speech_prob": 0.008894940838217735,
            "confidence": 0.929,
            "words": [
              {
                "text": "Interesting",
                "start": 123.08,
                "end": 123.56,
                "confidence": 0.82
              },
              {
                "text": "fact",
                "start": 123.56,
                "end": 124.08,
                "confidence": 0.998
              },
              {
                "text": "that",
                "start": 124.08,
                "end": 124.46,
                "confidence": 0.908
              },
              {
                "text": "in",
                "start": 124.46,
                "end": 124.6,
                "confidence": 0.974
              },
              {
                "text": "2007,",
                "start": 124.6,
                "end": 125.56,
                "confidence": 0.991
              },
              {
                "text": "major",
                "start": 125.74,
                "end": 126.18,
                "confidence": 0.941
              },
              {
                "text": "spots",
                "start": 126.18,
                "end": 126.61,
                "confidence": 0.886
              }
            ]
          },
          {
            "id": 55,
            "start": 126.61,
            "end": 131.2,
            "text": " equaling a buffer zone of approximately 207,000 hectares,",
            "no_speech_prob": 0.008894940838217735,
            "confidence": 0.836,
            "words": [
              {
                "text": "equaling",
                "start": 126.61,
                "end": 127.26,
                "confidence": 0.733
              },
              {
                "text": "a",
                "start": 127.26,
                "end": 127.4,
                "confidence": 0.647
              },
              {
                "text": "buffer",
                "start": 127.4,
                "end": 127.72,
                "confidence": 0.681
              },
              {
                "text": "zone",
                "start": 127.72,
                "end": 128.04,
                "confidence": 0.996
              },
              {
                "text": "of",
                "start": 128.04,
                "end": 128.22,
                "confidence": 0.925
              },
              {
                "text": "approximately",
                "start": 128.22,
                "end": 128.78,
                "confidence": 0.998
              },
              {
                "text": "207,000",
                "start": 128.78,
                "end": 130.72,
                "confidence": 0.913
              },
              {
                "text": "hectares,",
                "start": 130.72,
                "end": 131.2,
                "confidence": 0.801
              }
            ]
          },
          {
            "id": 56,
            "start": 131.64,
            "end": 134.16,
            "text": " which are called the coffee cultural landscape,",
            "no_speech_prob": 0.008894940838217735,
            "confidence": 0.965,
            "words": [
              {
                "text": "which",
                "start": 131.64,
                "end": 131.84,
                "confidence": 1.0
              },
              {
                "text": "are",
                "start": 131.84,
                "end": 132.1,
                "confidence": 0.997
              },
              {
                "text": "called",
                "start": 132.1,
                "end": 132.44,
                "confidence": 0.999
              },
              {
                "text": "the",
                "start": 132.44,
                "end": 132.72,
                "confidence": 0.99
              },
              {
                "text": "coffee",
                "start": 132.72,
                "end": 133.12,
                "confidence": 0.896
              },
              {
                "text": "cultural",
                "start": 133.12,
                "end": 133.58,
                "confidence": 0.905
              },
              {
                "text": "landscape,",
                "start": 133.58,
                "end": 134.16,
                "confidence": 0.978
              }
            ]
          },
          {
            "id": 57,
            "start": 134.5,
            "end": 137.22,
            "text": " were considered a UNESCO World Heritage Site.",
            "no_speech_prob": 0.008894940838217735,
            "confidence": 0.881,
            "words": [
              {
                "text": "were",
                "start": 134.5,
                "end": 134.68,
                "confidence": 0.798
              },
              {
                "text": "considered",
                "start": 134.68,
                "end": 135.2,
                "confidence": 0.996
              },
              {
                "text": "a",
                "start": 135.2,
                "end": 135.44,
                "confidence": 0.994
              },
              {
                "text": "UNESCO",
                "start": 135.44,
                "end": 135.9,
                "confidence": 0.926
              },
              {
                "text": "World",
                "start": 135.9,
                "end": 136.2,
                "confidence": 0.889
              },
              {
                "text": "Heritage",
                "start": 136.2,
                "end": 136.72,
                "confidence": 0.994
              },
              {
                "text": "Site.",
                "start": 136.72,
                "end": 137.22,
                "confidence": 0.604
              }
            ]
          },
          {
            "id": 58,
            "start": 137.62,
            "end": 140.74,
            "text": " And also in 2007, the EU, the European Union,",
            "no_speech_prob": 0.008894940838217735,
            "confidence": 0.965,
            "words": [
              {
                "text": "And",
                "start": 137.62,
                "end": 137.76,
                "confidence": 0.995
              },
              {
                "text": "also",
                "start": 137.76,
                "end": 138.06,
                "confidence": 0.999
              },
              {
                "text": "in",
                "start": 138.06,
                "end": 138.28,
                "confidence": 0.904
              },
              {
                "text": "2007,",
                "start": 138.28,
                "end": 139.04,
                "confidence": 0.997
              },
              {
                "text": "the",
                "start": 139.2,
                "end": 139.38,
                "confidence": 0.973
              },
              {
                "text": "EU,",
                "start": 139.38,
                "end": 139.72,
                "confidence": 0.887
              },
              {
                "text": "the",
                "start": 139.84,
                "end": 139.96,
                "confidence": 0.958
              },
              {
                "text": "European",
                "start": 139.96,
                "end": 140.36,
                "confidence": 0.998
              },
              {
                "text": "Union,",
                "start": 140.36,
                "end": 140.74,
                "confidence": 0.985
              }
            ]
          },
          {
            "id": 59,
            "start": 140.76,
            "end": 145.82,
            "text": " granted Colombian coffee a protected designation of origin status.",
            "no_speech_prob": 0.0017999779665842652,
            "confidence": 0.833,
            "words": [
              {
                "text": "granted",
                "start": 140.76,
                "end": 141.22,
                "confidence": 0.962
              },
              {
                "text": "Colombian",
                "start": 141.22,
                "end": 141.88,
                "confidence": 0.807
              },
              {
                "text": "coffee",
                "start": 141.88,
                "end": 142.32,
                "confidence": 0.947
              },
              {
                "text": "a",
                "start": 142.32,
                "end": 142.78,
                "confidence": 0.64
              },
              {
                "text": "protected",
                "start": 142.78,
                "end": 143.36,
                "confidence": 0.995
              },
              {
                "text": "designation",
                "start": 143.36,
                "end": 144.22,
                "confidence": 0.955
              },
              {
                "text": "of",
                "start": 144.22,
                "end": 144.52,
                "confidence": 0.537
              },
              {
                "text": "origin",
                "start": 144.52,
                "end": 145.04,
                "confidence": 0.955
              },
              {
                "text": "status.",
                "start": 145.04,
                "end": 145.82,
                "confidence": 0.865
              }
            ]
          },
          {
            "id": 60,
            "start": 146.12,
            "end": 149.08,
            "text": " Now interesting enough when it comes to the coffee in Columbia,",
            "no_speech_prob": 0.0017999779665842652,
            "confidence": 0.825,
            "words": [
              {
                "text": "Now",
                "start": 146.12,
                "end": 146.22,
                "confidence": 0.887
              },
              {
                "text": "interesting",
                "start": 146.22,
                "end": 146.66,
                "confidence": 0.595
              },
              {
                "text": "enough",
                "start": 146.66,
                "end": 146.96,
                "confidence": 0.96
              },
              {
                "text": "when",
                "start": 146.96,
                "end": 147.14,
                "confidence": 0.544
              },
              {
                "text": "it",
                "start": 147.14,
                "end": 147.26,
                "confidence": 0.994
              },
              {
                "text": "comes",
                "start": 147.26,
                "end": 147.46,
                "confidence": 0.993
              },
              {
                "text": "to",
                "start": 147.46,
                "end": 147.68,
                "confidence": 0.899
              },
              {
                "text": "the",
                "start": 147.68,
                "end": 147.82,
                "confidence": 0.969
              },
              {
                "text": "coffee",
                "start": 147.82,
                "end": 148.2,
                "confidence": 0.99
              },
              {
                "text": "in",
                "start": 148.2,
                "end": 148.5,
                "confidence": 0.865
              },
              {
                "text": "Columbia,",
                "start": 148.5,
                "end": 149.08,
                "confidence": 0.596
              }
            ]
          },
          {
            "id": 61,
            "start": 149.12,
            "end": 153.1,
            "text": " believe it or not, it is not actually native to the country.",
            "no_speech_prob": 0.0017999779665842652,
            "confidence": 0.984,
            "words": [
              {
                "text": "believe",
                "start": 149.12,
                "end": 149.58,
                "confidence": 0.965
              },
              {
                "text": "it",
                "start": 149.58,
                "end": 149.7,
                "confidence": 0.99
              },
              {
                "text": "or",
                "start": 149.7,
                "end": 149.82,
                "confidence": 1.0
              },
              {
                "text": "not,",
                "start": 149.82,
                "end": 150.02,
                "confidence": 1.0
              },
              {
                "text": "it",
                "start": 150.18,
                "end": 150.28,
                "confidence": 0.953
              },
              {
                "text": "is",
                "start": 150.28,
                "end": 150.44,
                "confidence": 0.996
              },
              {
                "text": "not",
                "start": 150.44,
                "end": 151.02,
                "confidence": 0.996
              },
              {
                "text": "actually",
                "start": 151.02,
                "end": 151.8,
                "confidence": 0.979
              },
              {
                "text": "native",
                "start": 151.8,
                "end": 152.32,
                "confidence": 0.984
              },
              {
                "text": "to",
                "start": 152.32,
                "end": 152.56,
                "confidence": 0.96
              },
              {
                "text": "the",
                "start": 152.56,
                "end": 152.72,
                "confidence": 0.992
              },
              {
                "text": "country.",
                "start": 152.72,
                "end": 153.1,
                "confidence": 0.997
              }
            ]
          },
          {
            "id": 62,
            "start": 153.54,
            "end": 156.72,
            "text": " It's come from somewhere else, not really an invasive species",
            "no_speech_prob": 0.0017999779665842652,
            "confidence": 0.924,
            "words": [
              {
                "text": "It's",
                "start": 153.54,
                "end": 153.78,
                "confidence": 0.988
              },
              {
                "text": "come",
                "start": 153.78,
                "end": 153.96,
                "confidence": 0.971
              },
              {
                "text": "from",
                "start": 153.96,
                "end": 154.12,
                "confidence": 0.999
              },
              {
                "text": "somewhere",
                "start": 154.12,
                "end": 154.52,
                "confidence": 0.992
              },
              {
                "text": "else,",
                "start": 154.52,
                "end": 155.02,
                "confidence": 1.0
              },
              {
                "text": "not",
                "start": 155.1,
                "end": 155.44,
                "confidence": 0.789
              },
              {
                "text": "really",
                "start": 155.44,
                "end": 155.68,
                "confidence": 0.995
              },
              {
                "text": "an",
                "start": 155.68,
                "end": 155.8,
                "confidence": 0.76
              },
              {
                "text": "invasive",
                "start": 155.8,
                "end": 156.22,
                "confidence": 0.977
              },
              {
                "text": "species",
                "start": 156.22,
                "end": 156.72,
                "confidence": 0.77
              }
            ]
          },
          {
            "id": 63,
            "start": 156.72,
            "end": 158.42,
            "text": " because it's very much welcomed.",
            "no_speech_prob": 0.0017999779665842652,
            "confidence": 0.994,
            "words": [
              {
                "text": "because",
                "start": 156.72,
                "end": 157.14,
                "confidence": 0.999
              },
              {
                "text": "it's",
                "start": 157.14,
                "end": 157.36,
                "confidence": 0.993
              },
              {
                "text": "very",
                "start": 157.36,
                "end": 157.72,
                "confidence": 0.999
              },
              {
                "text": "much",
                "start": 157.72,
                "end": 157.96,
                "confidence": 0.998
              },
              {
                "text": "welcomed.",
                "start": 157.96,
                "end": 158.42,
                "confidence": 0.979
              }
            ]
          },
          {
            "id": 64,
            "start": 158.84,
            "end": 161.98,
            "text": " Now you may have also seen this guy on many different Colombian",
            "no_speech_prob": 0.0017999779665842652,
            "confidence": 0.897,
            "words": [
              {
                "text": "Now",
                "start": 158.84,
                "end": 159.0,
                "confidence": 0.999
              },
              {
                "text": "you",
                "start": 159.0,
                "end": 159.14,
                "confidence": 0.792
              },
              {
                "text": "may",
                "start": 159.14,
                "end": 159.28,
                "confidence": 0.998
              },
              {
                "text": "have",
                "start": 159.28,
                "end": 159.42,
                "confidence": 0.987
              },
              {
                "text": "also",
                "start": 159.42,
                "end": 159.76,
                "confidence": 0.995
              },
              {
                "text": "seen",
                "start": 159.76,
                "end": 160.14,
                "confidence": 0.998
              },
              {
                "text": "this",
                "start": 160.14,
                "end": 160.36,
                "confidence": 0.99
              },
              {
                "text": "guy",
                "start": 160.36,
                "end": 160.7,
                "confidence": 0.991
              },
              {
                "text": "on",
                "start": 160.7,
                "end": 160.9,
                "confidence": 0.627
              },
              {
                "text": "many",
                "start": 160.9,
                "end": 161.12,
                "confidence": 0.988
              },
              {
                "text": "different",
                "start": 161.12,
                "end": 161.38,
                "confidence": 0.965
              },
              {
                "text": "Colombian",
                "start": 161.38,
                "end": 161.98,
                "confidence": 0.734
              }
            ]
          },
          {
            "id": 65,
            "start": 161.98,
            "end": 162.81,
            "text": " coffee brands.",
            "no_speech_prob": 0.0017999779665842652,
            "confidence": 0.971,
            "words": [
              {
                "text": "coffee",
                "start": 161.98,
                "end": 162.46,
                "confidence": 0.958
              },
              {
                "text": "brands.",
                "start": 162.46,
                "end": 162.81,
                "confidence": 0.984
              }
            ]
          },
          {
            "id": 66,
            "start": 162.81,
            "end": 164.68,
            "text": " Now his name is Juan Valdez.",
            "no_speech_prob": 0.0017999779665842652,
            "confidence": 0.892,
            "words": [
              {
                "text": "Now",
                "start": 162.81,
                "end": 163.04,
                "confidence": 0.994
              },
              {
                "text": "his",
                "start": 163.04,
                "end": 163.24,
                "confidence": 0.823
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
                "end": 163.72,
                "confidence": 0.998
              },
              {
                "text": "Juan",
                "start": 163.72,
                "end": 164.0,
                "confidence": 0.804
              },
              {
                "text": "Valdez.",
                "start": 164.0,
                "end": 164.68,
                "confidence": 0.848
              }
            ]
          },
          {
            "id": 67,
            "start": 164.74,
            "end": 167.42,
            "text": " Now some people think that this guy is actually really",
            "no_speech_prob": 0.0017999779665842652,
            "confidence": 0.93,
            "words": [
              {
                "text": "Now",
                "start": 164.74,
                "end": 164.9,
                "confidence": 0.994
              },
              {
                "text": "some",
                "start": 164.9,
                "end": 165.06,
                "confidence": 0.944
              },
              {
                "text": "people",
                "start": 165.06,
                "end": 165.24,
                "confidence": 1.0
              },
              {
                "text": "think",
                "start": 165.24,
                "end": 165.6,
                "confidence": 0.999
              },
              {
                "text": "that",
                "start": 165.6,
                "end": 165.76,
                "confidence": 0.958
              },
              {
                "text": "this",
                "start": 165.76,
                "end": 165.98,
                "confidence": 0.993
              },
              {
                "text": "guy",
                "start": 165.98,
                "end": 166.26,
                "confidence": 0.999
              },
              {
                "text": "is",
                "start": 166.26,
                "end": 166.42,
                "confidence": 0.869
              },
              {
                "text": "actually",
                "start": 166.42,
                "end": 166.88,
                "confidence": 0.982
              },
              {
                "text": "really",
                "start": 166.88,
                "end": 167.42,
                "confidence": 0.636
              }
            ]
          },
          {
            "id": 68,
            "start": 167.52,
            "end": 170.0,
            "text": " a real coffee farmer, somebody just drew.",
            "no_speech_prob": 0.6980549693107605,
            "confidence": 0.65,
            "words": [
              {
                "text": "a",
                "start": 167.52,
                "end": 167.68,
                "confidence": 0.498
              },
              {
                "text": "real",
                "start": 167.68,
                "end": 167.94,
                "confidence": 0.967
              },
              {
                "text": "coffee",
                "start": 167.94,
                "end": 168.48,
                "confidence": 0.993
              },
              {
                "text": "farmer,",
                "start": 168.48,
                "end": 169.0,
                "confidence": 0.986
              },
              {
                "text": "somebody",
                "start": 169.22,
                "end": 169.44,
                "confidence": 0.447
              },
              {
                "text": "just",
                "start": 169.44,
                "end": 169.66,
                "confidence": 0.56
              },
              {
                "text": "drew.",
                "start": 169.66,
                "end": 170.0,
                "confidence": 0.416
              }
            ]
          }
        ]
      }
    ]


## Using a non-default model

To use a non-default model like `large-v3` we enter it explicitly as a `modules` selection when invoking `.process`.

We use it below to process the same input file shown above.


```python
# define path to an input file
test_file = "../../data/input/Interesting Facts About Colombia.mp4"

# process for search
process_output = pipeline.process(
    local_file_path=test_file,
    local_save_directory="../../data/output",  # save output repo data output subdir
    expire_time=60 * 10,  # set all process data to expire in 10 minutes
    wait_for_process=True,  # wait for process to complete before regaining ide
    verbose=False,  # set verbosity to False
    modules={"transcribe": {"model": "whisper-large-v3"}},
)
```

The output of this process is printed below.  Because the output of this particular module-model pair is json, the process output is provided in this object as well.  The output file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "modules-transcribe-docs",
      "request_id": "585bf2b7-aa0a-4ffa-9180-2a823086551c",
      "file_id": "09342ea4-cf52-4bb8-9f63-6785af3cb117",
      "message": "SUCCESS - output fetched for file_id 09342ea4-cf52-4bb8-9f63-6785af3cb117.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "transcript": " Episode looking at the great country of Colombia We looked at some really just basic facts its name a bit of its history the type of people that live there Landsize and all that jazz, but in this video, we're gonna go into a little bit more of a detailed look Yo, what is going on guys? Welcome back to have to D facts a channel where I look at people cultures and places My name is Dave Walpole and today We are gonna be looking more at Colombia in our Columbia part 2 video, which just reminds me guys This is part of our Columbia playlist I'll put it down in the description box below and I'll talk about that more at the end of the video But if you're new here join me every single Monday to learn about new countries from around the world You can do that by hitting that subscribe and that belt notification button, but let's get started Columbia so we all know Columbia is famous for its coffee, right? Yes, right I know you guys are sitting there going five bucks says he's gonna talk about coffee Well, I am that's right because I got my van huge Columbia coffee right here. Boom Advertisement. Yeah Yeah Don't I'm paying me for this. I don't care So what you might not know about coffee is yes You probably already know that a lot of companies actually buy it up Starbucks buys all had a coffee from Columbia It's kind of like their favorite place to buy coffee and kind of to pay tribute to that Starbucks when they were making their 1,000th store in 2016 they decided yo we're gonna put it in Columbia and this was in the town of metal in Columbia Now here's the thing when it comes to coffee in Columbia. They are the third largest largest producing and exporting coffee country in the world the amount of coffee that is exported from Columbia equals about 810 thousand metric tons or approximately 11.5 million bags. However, although it might be beaten by countries like Brazil it is actually the number one or highest country for producing and growing a specific type of bean known as the Arabica bean and I know coffee is really important when it comes to talking about Columbia But you guys really don't know how important it is with its culture interesting fact that in 2007 major spots equaling a buffer zone of approximately 207,000 hectares which are called the coffee cultural landscape were considered a UNESCO World Heritage Site and also in 2007 the EU the European Union granted Colombian coffee a protected designation of origin status now Interesting enough when it comes to the coffee in Colombia, believe it or not. It is not actually native to the country It's come from somewhere else not really an invasive species because it's very much welcomed now You may have also seen this guy on many different Colombian coffee brands now His name is Juan Valdez. Now. Some people think that this guy is actually real. He's a real coffee farmer. Somebody just drew",
          "timestamped_transcript": [
            {
              "id": 0,
              "start": 0.0,
              "end": 2.12,
              "text": " Episode looking at the great country of Colombia",
              "no_speech_prob": 0.05201467499136925,
              "confidence": 0.914,
              "words": [
                {
                  "text": "Episode",
                  "start": 0.0,
                  "end": 0.46,
                  "confidence": 0.619
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
                  "confidence": 0.984
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
                  "end": 1.8,
                  "confidence": 0.999
                },
                {
                  "text": "Colombia",
                  "start": 1.8,
                  "end": 2.12,
                  "confidence": 0.808
                }
              ]
            },
            {
              "id": 1,
              "start": 2.18,
              "end": 7.5,
              "text": " We looked at some really just basic facts its name a bit of its history the type of people that live there",
              "no_speech_prob": 0.05201467499136925,
              "confidence": 0.923,
              "words": [
                {
                  "text": "We",
                  "start": 2.18,
                  "end": 2.34,
                  "confidence": 0.871
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
                  "confidence": 0.924
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
                  "confidence": 0.939
                },
                {
                  "text": "its",
                  "start": 4.38,
                  "end": 4.58,
                  "confidence": 0.791
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
                  "confidence": 0.997
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
                  "confidence": 0.564
                },
                {
                  "text": "type",
                  "start": 6.36,
                  "end": 6.54,
                  "confidence": 0.996
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
                  "confidence": 0.675
                },
                {
                  "text": "there",
                  "start": 7.22,
                  "end": 7.5,
                  "confidence": 0.773
                }
              ]
            },
            {
              "id": 2,
              "start": 7.66,
              "end": 12.58,
              "text": " Landsize and all that jazz, but in this video, we're gonna go into a little bit more of a detailed look",
              "no_speech_prob": 0.05201467499136925,
              "confidence": 0.943,
              "words": [
                {
                  "text": "Landsize",
                  "start": 7.66,
                  "end": 8.28,
                  "confidence": 0.761
                },
                {
                  "text": "and",
                  "start": 8.28,
                  "end": 8.44,
                  "confidence": 0.991
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
                  "confidence": 0.99
                },
                {
                  "text": "but",
                  "start": 9.52,
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
                  "confidence": 0.995
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
                  "confidence": 0.491
                }
              ]
            },
            {
              "id": 3,
              "start": 12.74,
              "end": 17.5,
              "text": " Yo, what is going on guys? Welcome back to have to D facts a channel where I look at people cultures and places",
              "no_speech_prob": 0.05201467499136925,
              "confidence": 0.834,
              "words": [
                {
                  "text": "Yo,",
                  "start": 12.74,
                  "end": 13.06,
                  "confidence": 0.78
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
                  "confidence": 0.61
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
                  "confidence": 0.981
                },
                {
                  "text": "have",
                  "start": 15.04,
                  "end": 15.14,
                  "confidence": 0.406
                },
                {
                  "text": "to",
                  "start": 15.14,
                  "end": 15.24,
                  "confidence": 0.674
                },
                {
                  "text": "D",
                  "start": 15.24,
                  "end": 15.38,
                  "confidence": 0.259
                },
                {
                  "text": "facts",
                  "start": 15.38,
                  "end": 15.68,
                  "confidence": 0.876
                },
                {
                  "text": "a",
                  "start": 15.68,
                  "end": 15.82,
                  "confidence": 0.639
                },
                {
                  "text": "channel",
                  "start": 15.82,
                  "end": 16.0,
                  "confidence": 0.996
                },
                {
                  "text": "where",
                  "start": 16.0,
                  "end": 16.16,
                  "confidence": 0.967
                },
                {
                  "text": "I",
                  "start": 16.16,
                  "end": 16.22,
                  "confidence": 0.987
                },
                {
                  "text": "look",
                  "start": 16.22,
                  "end": 16.38,
                  "confidence": 0.996
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
                  "confidence": 0.923
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
              "no_speech_prob": 0.05201467499136925,
              "confidence": 0.86,
              "words": [
                {
                  "text": "My",
                  "start": 17.58,
                  "end": 17.84,
                  "confidence": 0.772
                },
                {
                  "text": "name",
                  "start": 17.84,
                  "end": 18.2,
                  "confidence": 1.0
                },
                {
                  "text": "is",
                  "start": 18.2,
                  "end": 19.04,
                  "confidence": 0.999
                },
                {
                  "text": "Dave",
                  "start": 19.04,
                  "end": 19.46,
                  "confidence": 0.954
                },
                {
                  "text": "Walpole",
                  "start": 19.46,
                  "end": 20.0,
                  "confidence": 0.89
                },
                {
                  "text": "and",
                  "start": 20.0,
                  "end": 20.34,
                  "confidence": 0.536
                },
                {
                  "text": "today",
                  "start": 20.34,
                  "end": 20.98,
                  "confidence": 0.962
                }
              ]
            },
            {
              "id": 5,
              "start": 21.34,
              "end": 27.05,
              "text": " We are gonna be looking more at Colombia in our Columbia part 2 video, which just reminds me guys",
              "no_speech_prob": 0.05201467499136925,
              "confidence": 0.936,
              "words": [
                {
                  "text": "We",
                  "start": 21.34,
                  "end": 21.68,
                  "confidence": 0.966
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
                  "confidence": 0.928
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
                  "end": 23.0,
                  "confidence": 0.998
                },
                {
                  "text": "at",
                  "start": 23.0,
                  "end": 23.24,
                  "confidence": 1.0
                },
                {
                  "text": "Colombia",
                  "start": 23.24,
                  "end": 23.66,
                  "confidence": 0.609
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
                  "confidence": 0.728
                },
                {
                  "text": "part",
                  "start": 24.28,
                  "end": 24.54,
                  "confidence": 0.894
                },
                {
                  "text": "2",
                  "start": 24.54,
                  "end": 24.82,
                  "confidence": 0.811
                },
                {
                  "text": "video,",
                  "start": 24.82,
                  "end": 25.28,
                  "confidence": 0.998
                },
                {
                  "text": "which",
                  "start": 25.7,
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
                  "confidence": 0.999
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
              "no_speech_prob": 0.0002229930687462911,
              "confidence": 0.943,
              "words": [
                {
                  "text": "This",
                  "start": 27.05,
                  "end": 27.24,
                  "confidence": 0.95
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
                  "confidence": 0.716
                },
                {
                  "text": "playlist",
                  "start": 28.3,
                  "end": 28.8,
                  "confidence": 0.979
                }
              ]
            },
            {
              "id": 7,
              "start": 28.86,
              "end": 32.36,
              "text": " I'll put it down in the description box below and I'll talk about that more at the end of the video",
              "no_speech_prob": 0.0002229930687462911,
              "confidence": 0.968,
              "words": [
                {
                  "text": "I'll",
                  "start": 28.86,
                  "end": 29.02,
                  "confidence": 0.979
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
                  "confidence": 0.525
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
                  "confidence": 0.982
                },
                {
                  "text": "the",
                  "start": 31.84,
                  "end": 31.96,
                  "confidence": 0.999
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
              "end": 36.48,
              "text": " But if you're new here join me every single Monday to learn about new countries from around the world",
              "no_speech_prob": 0.0002229930687462911,
              "confidence": 0.98,
              "words": [
                {
                  "text": "But",
                  "start": 32.66,
                  "end": 32.84,
                  "confidence": 0.836
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
                  "confidence": 0.975
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
                  "confidence": 0.879
                },
                {
                  "text": "me",
                  "start": 33.9,
                  "end": 34.04,
                  "confidence": 0.993
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
                  "confidence": 0.996
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
                  "confidence": 0.995
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
                  "end": 36.48,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 9,
              "start": 36.48,
              "end": 41.62,
              "text": " You can do that by hitting that subscribe and that belt notification button, but let's get started",
              "no_speech_prob": 0.0002229930687462911,
              "confidence": 0.927,
              "words": [
                {
                  "text": "You",
                  "start": 36.48,
                  "end": 36.6,
                  "confidence": 0.515
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
                  "confidence": 0.781
                },
                {
                  "text": "that",
                  "start": 38.14,
                  "end": 38.32,
                  "confidence": 0.969
                },
                {
                  "text": "belt",
                  "start": 38.32,
                  "end": 38.5,
                  "confidence": 0.797
                },
                {
                  "text": "notification",
                  "start": 38.5,
                  "end": 39.12,
                  "confidence": 0.984
                },
                {
                  "text": "button,",
                  "start": 39.12,
                  "end": 39.46,
                  "confidence": 0.998
                },
                {
                  "text": "but",
                  "start": 39.56,
                  "end": 40.06,
                  "confidence": 1.0
                },
                {
                  "text": "let's",
                  "start": 40.06,
                  "end": 40.9,
                  "confidence": 0.937
                },
                {
                  "text": "get",
                  "start": 40.9,
                  "end": 41.2,
                  "confidence": 0.974
                },
                {
                  "text": "started",
                  "start": 41.2,
                  "end": 41.62,
                  "confidence": 0.998
                }
              ]
            },
            {
              "id": 10,
              "start": 42.18,
              "end": 47.46,
              "text": " Columbia so we all know Columbia is famous for its coffee, right? Yes, right",
              "no_speech_prob": 0.0002229930687462911,
              "confidence": 0.894,
              "words": [
                {
                  "text": "Columbia",
                  "start": 42.18,
                  "end": 42.76,
                  "confidence": 0.668
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
                  "confidence": 0.994
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
                  "confidence": 0.47
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
                  "confidence": 0.931
                },
                {
                  "text": "coffee,",
                  "start": 45.84,
                  "end": 46.3,
                  "confidence": 0.995
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
              "no_speech_prob": 0.0002229930687462911,
              "confidence": 0.933,
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
                  "confidence": 0.991
                },
                {
                  "text": "sitting",
                  "start": 48.46,
                  "end": 48.62,
                  "confidence": 0.996
                },
                {
                  "text": "there",
                  "start": 48.62,
                  "end": 48.74,
                  "confidence": 0.986
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
                  "confidence": 0.696
                },
                {
                  "text": "bucks",
                  "start": 49.52,
                  "end": 49.74,
                  "confidence": 0.978
                },
                {
                  "text": "says",
                  "start": 49.74,
                  "end": 49.92,
                  "confidence": 0.713
                },
                {
                  "text": "he's",
                  "start": 49.92,
                  "end": 50.06,
                  "confidence": 0.819
                },
                {
                  "text": "gonna",
                  "start": 50.06,
                  "end": 50.16,
                  "confidence": 0.987
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
              "start": 51.04,
              "end": 55.6,
              "text": " Well, I am that's right because I got my van huge Columbia coffee right here. Boom",
              "no_speech_prob": 0.0002229930687462911,
              "confidence": 0.877,
              "words": [
                {
                  "text": "Well,",
                  "start": 51.04,
                  "end": 51.28,
                  "confidence": 0.987
                },
                {
                  "text": "I",
                  "start": 51.38,
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
                  "confidence": 0.928
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
                  "confidence": 0.898
                },
                {
                  "text": "huge",
                  "start": 53.4,
                  "end": 53.66,
                  "confidence": 0.179
                },
                {
                  "text": "Columbia",
                  "start": 53.66,
                  "end": 54.02,
                  "confidence": 0.782
                },
                {
                  "text": "coffee",
                  "start": 54.02,
                  "end": 54.38,
                  "confidence": 0.978
                },
                {
                  "text": "right",
                  "start": 54.38,
                  "end": 54.72,
                  "confidence": 0.991
                },
                {
                  "text": "here.",
                  "start": 54.72,
                  "end": 55.06,
                  "confidence": 0.999
                },
                {
                  "text": "Boom",
                  "start": 55.24,
                  "end": 55.6,
                  "confidence": 0.994
                }
              ]
            },
            {
              "id": 13,
              "start": 55.84,
              "end": 56.74,
              "text": " Advertisement. Yeah",
              "no_speech_prob": 0.0002229930687462911,
              "confidence": 0.936,
              "words": [
                {
                  "text": "Advertisement.",
                  "start": 55.84,
                  "end": 56.54,
                  "confidence": 0.922
                },
                {
                  "text": "Yeah",
                  "start": 56.68,
                  "end": 56.74,
                  "confidence": 0.998
                }
              ]
            },
            {
              "id": 14,
              "start": 56.74,
              "end": 56.88,
              "text": " Yeah",
              "no_speech_prob": 0.0002229930687462911,
              "confidence": 0.439,
              "words": [
                {
                  "text": "Yeah",
                  "start": 56.74,
                  "end": 56.88,
                  "confidence": 0.439
                }
              ]
            },
            {
              "id": 15,
              "start": 57.06,
              "end": 58.88,
              "text": " Don't I'm paying me for this. I don't care",
              "no_speech_prob": 0.00015449173224624246,
              "confidence": 0.827,
              "words": [
                {
                  "text": "Don't",
                  "start": 57.06,
                  "end": 57.3,
                  "confidence": 0.498
                },
                {
                  "text": "I'm",
                  "start": 57.3,
                  "end": 57.48,
                  "confidence": 0.658
                },
                {
                  "text": "paying",
                  "start": 57.48,
                  "end": 57.7,
                  "confidence": 0.962
                },
                {
                  "text": "me",
                  "start": 57.7,
                  "end": 57.88,
                  "confidence": 0.998
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
                  "start": 58.28,
                  "end": 58.38,
                  "confidence": 0.999
                },
                {
                  "text": "don't",
                  "start": 58.38,
                  "end": 58.6,
                  "confidence": 0.998
                },
                {
                  "text": "care",
                  "start": 58.6,
                  "end": 58.88,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 16,
              "start": 59.0,
              "end": 60.88,
              "text": " So what you might not know about coffee is yes",
              "no_speech_prob": 0.00015449173224624246,
              "confidence": 0.977,
              "words": [
                {
                  "text": "So",
                  "start": 59.0,
                  "end": 59.16,
                  "confidence": 0.91
                },
                {
                  "text": "what",
                  "start": 59.16,
                  "end": 59.28,
                  "confidence": 0.915
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
                  "end": 60.14,
                  "confidence": 0.999
                },
                {
                  "text": "coffee",
                  "start": 60.14,
                  "end": 60.54,
                  "confidence": 0.974
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
                  "confidence": 0.98
                }
              ]
            },
            {
              "id": 17,
              "start": 60.88,
              "end": 67.14,
              "text": " You probably already know that a lot of companies actually buy it up Starbucks buys all had a coffee from Columbia",
              "no_speech_prob": 0.00015449173224624246,
              "confidence": 0.896,
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
                  "end": 61.94,
                  "confidence": 0.999
                },
                {
                  "text": "that",
                  "start": 61.94,
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
                  "confidence": 0.994
                },
                {
                  "text": "buy",
                  "start": 63.5,
                  "end": 63.74,
                  "confidence": 0.992
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
                  "end": 64.22,
                  "confidence": 0.999
                },
                {
                  "text": "Starbucks",
                  "start": 64.22,
                  "end": 64.82,
                  "confidence": 0.772
                },
                {
                  "text": "buys",
                  "start": 64.82,
                  "end": 65.18,
                  "confidence": 0.961
                },
                {
                  "text": "all",
                  "start": 65.18,
                  "end": 65.54,
                  "confidence": 0.561
                },
                {
                  "text": "had",
                  "start": 65.54,
                  "end": 65.78,
                  "confidence": 0.503
                },
                {
                  "text": "a",
                  "start": 65.78,
                  "end": 66.0,
                  "confidence": 0.992
                },
                {
                  "text": "coffee",
                  "start": 66.0,
                  "end": 66.34,
                  "confidence": 0.993
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
                  "end": 67.14,
                  "confidence": 0.506
                }
              ]
            },
            {
              "id": 18,
              "start": 67.68,
              "end": 72.0,
              "text": " It's kind of like their favorite place to buy coffee and kind of to pay tribute to that",
              "no_speech_prob": 0.00015449173224624246,
              "confidence": 0.961,
              "words": [
                {
                  "text": "It's",
                  "start": 67.68,
                  "end": 67.8,
                  "confidence": 0.907
                },
                {
                  "text": "kind",
                  "start": 67.8,
                  "end": 67.94,
                  "confidence": 0.944
                },
                {
                  "text": "of",
                  "start": 67.94,
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
                  "confidence": 0.985
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
                  "confidence": 0.999
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
                  "confidence": 0.993
                },
                {
                  "text": "kind",
                  "start": 70.16,
                  "end": 70.36,
                  "confidence": 0.631
                },
                {
                  "text": "of",
                  "start": 70.36,
                  "end": 70.48,
                  "confidence": 0.998
                },
                {
                  "text": "to",
                  "start": 70.48,
                  "end": 70.66,
                  "confidence": 0.989
                },
                {
                  "text": "pay",
                  "start": 70.66,
                  "end": 70.88,
                  "confidence": 0.999
                },
                {
                  "text": "tribute",
                  "start": 70.88,
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
              "id": 19,
              "start": 72.18,
              "end": 75.12,
              "text": " Starbucks when they were making their 1,000th store in",
              "no_speech_prob": 0.00015449173224624246,
              "confidence": 0.897,
              "words": [
                {
                  "text": "Starbucks",
                  "start": 72.18,
                  "end": 72.74,
                  "confidence": 0.981
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
                  "confidence": 0.987
                },
                {
                  "text": "were",
                  "start": 73.06,
                  "end": 73.2,
                  "confidence": 0.883
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
                  "end": 73.7,
                  "confidence": 0.991
                },
                {
                  "text": "1,000th",
                  "start": 73.7,
                  "end": 74.64,
                  "confidence": 0.756
                },
                {
                  "text": "store",
                  "start": 74.64,
                  "end": 74.92,
                  "confidence": 0.989
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
              "id": 20,
              "start": 75.44,
              "end": 82.24,
              "text": " 2016 they decided yo we're gonna put it in Columbia and this was in the town of metal in Columbia",
              "no_speech_prob": 0.00015449173224624246,
              "confidence": 0.836,
              "words": [
                {
                  "text": "2016",
                  "start": 75.44,
                  "end": 76.36,
                  "confidence": 0.998
                },
                {
                  "text": "they",
                  "start": 76.36,
                  "end": 77.06,
                  "confidence": 0.985
                },
                {
                  "text": "decided",
                  "start": 77.06,
                  "end": 77.62,
                  "confidence": 0.998
                },
                {
                  "text": "yo",
                  "start": 77.62,
                  "end": 77.98,
                  "confidence": 0.939
                },
                {
                  "text": "we're",
                  "start": 77.98,
                  "end": 78.26,
                  "confidence": 0.646
                },
                {
                  "text": "gonna",
                  "start": 78.26,
                  "end": 78.38,
                  "confidence": 0.997
                },
                {
                  "text": "put",
                  "start": 78.38,
                  "end": 78.58,
                  "confidence": 0.999
                },
                {
                  "text": "it",
                  "start": 78.58,
                  "end": 78.72,
                  "confidence": 0.997
                },
                {
                  "text": "in",
                  "start": 78.72,
                  "end": 78.92,
                  "confidence": 1.0
                },
                {
                  "text": "Columbia",
                  "start": 78.92,
                  "end": 79.36,
                  "confidence": 0.506
                },
                {
                  "text": "and",
                  "start": 79.36,
                  "end": 79.96,
                  "confidence": 0.843
                },
                {
                  "text": "this",
                  "start": 79.96,
                  "end": 80.18,
                  "confidence": 0.997
                },
                {
                  "text": "was",
                  "start": 80.18,
                  "end": 80.4,
                  "confidence": 0.998
                },
                {
                  "text": "in",
                  "start": 80.4,
                  "end": 80.58,
                  "confidence": 1.0
                },
                {
                  "text": "the",
                  "start": 80.58,
                  "end": 80.7,
                  "confidence": 0.999
                },
                {
                  "text": "town",
                  "start": 80.7,
                  "end": 81.04,
                  "confidence": 0.998
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
                  "confidence": 0.231
                },
                {
                  "text": "in",
                  "start": 81.56,
                  "end": 81.78,
                  "confidence": 0.907
                },
                {
                  "text": "Columbia",
                  "start": 81.78,
                  "end": 82.24,
                  "confidence": 0.692
                }
              ]
            },
            {
              "id": 21,
              "start": 82.54,
              "end": 86.86,
              "text": " Now here's the thing when it comes to coffee in Columbia. They are the third largest",
              "no_speech_prob": 0.00015449173224624246,
              "confidence": 0.858,
              "words": [
                {
                  "text": "Now",
                  "start": 82.54,
                  "end": 82.74,
                  "confidence": 0.954
                },
                {
                  "text": "here's",
                  "start": 82.74,
                  "end": 83.04,
                  "confidence": 0.967
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
                  "end": 83.68,
                  "confidence": 1.0
                },
                {
                  "text": "comes",
                  "start": 83.68,
                  "end": 84.14,
                  "confidence": 0.999
                },
                {
                  "text": "to",
                  "start": 84.14,
                  "end": 84.34,
                  "confidence": 1.0
                },
                {
                  "text": "coffee",
                  "start": 84.34,
                  "end": 84.74,
                  "confidence": 0.992
                },
                {
                  "text": "in",
                  "start": 84.74,
                  "end": 85.06,
                  "confidence": 0.999
                },
                {
                  "text": "Columbia.",
                  "start": 85.06,
                  "end": 85.38,
                  "confidence": 0.557
                },
                {
                  "text": "They",
                  "start": 85.44,
                  "end": 85.64,
                  "confidence": 0.997
                },
                {
                  "text": "are",
                  "start": 85.64,
                  "end": 85.9,
                  "confidence": 0.971
                },
                {
                  "text": "the",
                  "start": 85.9,
                  "end": 86.12,
                  "confidence": 0.988
                },
                {
                  "text": "third",
                  "start": 86.12,
                  "end": 86.72,
                  "confidence": 0.964
                },
                {
                  "text": "largest",
                  "start": 86.72,
                  "end": 86.86,
                  "confidence": 0.165
                }
              ]
            },
            {
              "id": 22,
              "start": 86.96,
              "end": 87.64,
              "text": " largest",
              "no_speech_prob": 9.292483446188271e-05,
              "confidence": 0.609,
              "words": [
                {
                  "text": "largest",
                  "start": 86.96,
                  "end": 87.64,
                  "confidence": 0.609
                }
              ]
            },
            {
              "id": 23,
              "start": 87.98,
              "end": 95.64,
              "text": " producing and exporting coffee country in the world the amount of coffee that is exported from Columbia equals about",
              "no_speech_prob": 9.292483446188271e-05,
              "confidence": 0.965,
              "words": [
                {
                  "text": "producing",
                  "start": 87.98,
                  "end": 88.88,
                  "confidence": 0.805
                },
                {
                  "text": "and",
                  "start": 88.88,
                  "end": 89.34,
                  "confidence": 0.95
                },
                {
                  "text": "exporting",
                  "start": 89.34,
                  "end": 89.98,
                  "confidence": 0.953
                },
                {
                  "text": "coffee",
                  "start": 89.98,
                  "end": 90.5,
                  "confidence": 0.959
                },
                {
                  "text": "country",
                  "start": 90.5,
                  "end": 90.9,
                  "confidence": 0.996
                },
                {
                  "text": "in",
                  "start": 90.9,
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
                  "end": 91.98,
                  "confidence": 0.992
                },
                {
                  "text": "the",
                  "start": 91.98,
                  "end": 92.32,
                  "confidence": 0.91
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
                  "end": 92.74,
                  "confidence": 0.999
                },
                {
                  "text": "coffee",
                  "start": 92.74,
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
                  "confidence": 0.993
                },
                {
                  "text": "from",
                  "start": 93.88,
                  "end": 94.18,
                  "confidence": 0.999
                },
                {
                  "text": "Columbia",
                  "start": 94.18,
                  "end": 94.72,
                  "confidence": 0.834
                },
                {
                  "text": "equals",
                  "start": 94.72,
                  "end": 95.2,
                  "confidence": 0.997
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
              "start": 96.0,
              "end": 97.06,
              "text": " 810",
              "no_speech_prob": 9.292483446188271e-05,
              "confidence": 0.905,
              "words": [
                {
                  "text": "810",
                  "start": 96.0,
                  "end": 97.06,
                  "confidence": 0.905
                }
              ]
            },
            {
              "id": 25,
              "start": 97.52,
              "end": 100.62,
              "text": " thousand metric tons or approximately",
              "no_speech_prob": 9.292483446188271e-05,
              "confidence": 0.812,
              "words": [
                {
                  "text": "thousand",
                  "start": 97.52,
                  "end": 98.24,
                  "confidence": 0.693
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
                  "end": 99.34,
                  "confidence": 0.943
                },
                {
                  "text": "or",
                  "start": 99.34,
                  "end": 100.0,
                  "confidence": 0.96
                },
                {
                  "text": "approximately",
                  "start": 100.0,
                  "end": 100.62,
                  "confidence": 0.565
                }
              ]
            },
            {
              "id": 26,
              "start": 101.02,
              "end": 106.9,
              "text": " 11.5 million bags. However, although it might be beaten by countries like Brazil",
              "no_speech_prob": 9.292483446188271e-05,
              "confidence": 0.991,
              "words": [
                {
                  "text": "11.5",
                  "start": 101.02,
                  "end": 102.12,
                  "confidence": 0.997
                },
                {
                  "text": "million",
                  "start": 102.12,
                  "end": 102.56,
                  "confidence": 0.975
                },
                {
                  "text": "bags.",
                  "start": 102.56,
                  "end": 103.14,
                  "confidence": 0.997
                },
                {
                  "text": "However,",
                  "start": 103.46,
                  "end": 103.6,
                  "confidence": 0.992
                },
                {
                  "text": "although",
                  "start": 103.74,
                  "end": 104.04,
                  "confidence": 0.997
                },
                {
                  "text": "it",
                  "start": 104.04,
                  "end": 104.4,
                  "confidence": 0.999
                },
                {
                  "text": "might",
                  "start": 104.4,
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
                  "confidence": 0.997
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
                  "confidence": 0.985
                },
                {
                  "text": "like",
                  "start": 106.0,
                  "end": 106.5,
                  "confidence": 0.991
                },
                {
                  "text": "Brazil",
                  "start": 106.5,
                  "end": 106.9,
                  "confidence": 0.95
                }
              ]
            },
            {
              "id": 27,
              "start": 106.9,
              "end": 112.18,
              "text": " it is actually the number one or highest country for producing and growing a",
              "no_speech_prob": 9.292483446188271e-05,
              "confidence": 0.981,
              "words": [
                {
                  "text": "it",
                  "start": 106.9,
                  "end": 108.02,
                  "confidence": 0.782
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
                  "confidence": 0.99
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
                  "confidence": 0.999
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
                  "confidence": 0.995
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
                  "confidence": 0.998
                }
              ]
            },
            {
              "id": 28,
              "start": 112.26,
              "end": 116.72,
              "text": " specific type of bean known as the Arabica bean and",
              "no_speech_prob": 9.292483446188271e-05,
              "confidence": 0.877,
              "words": [
                {
                  "text": "specific",
                  "start": 112.26,
                  "end": 112.92,
                  "confidence": 0.912
                },
                {
                  "text": "type",
                  "start": 112.92,
                  "end": 113.26,
                  "confidence": 1.0
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
                  "end": 113.84,
                  "confidence": 0.878
                },
                {
                  "text": "known",
                  "start": 113.84,
                  "end": 114.38,
                  "confidence": 0.99
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
                  "confidence": 0.999
                },
                {
                  "text": "Arabica",
                  "start": 114.98,
                  "end": 115.78,
                  "confidence": 0.684
                },
                {
                  "text": "bean",
                  "start": 115.78,
                  "end": 116.32,
                  "confidence": 0.803
                },
                {
                  "text": "and",
                  "start": 116.32,
                  "end": 116.72,
                  "confidence": 0.796
                }
              ]
            },
            {
              "id": 29,
              "start": 116.74,
              "end": 119.97,
              "text": " I know coffee is really important when it comes to talking about Columbia",
              "no_speech_prob": 0.0003879508003592491,
              "confidence": 0.962,
              "words": [
                {
                  "text": "I",
                  "start": 116.74,
                  "end": 116.86,
                  "confidence": 0.85
                },
                {
                  "text": "know",
                  "start": 116.86,
                  "end": 117.04,
                  "confidence": 0.994
                },
                {
                  "text": "coffee",
                  "start": 117.04,
                  "end": 117.52,
                  "confidence": 0.986
                },
                {
                  "text": "is",
                  "start": 117.52,
                  "end": 117.82,
                  "confidence": 0.998
                },
                {
                  "text": "really",
                  "start": 117.82,
                  "end": 118.16,
                  "confidence": 0.997
                },
                {
                  "text": "important",
                  "start": 118.16,
                  "end": 118.74,
                  "confidence": 0.976
                },
                {
                  "text": "when",
                  "start": 118.74,
                  "end": 118.92,
                  "confidence": 0.997
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
                  "confidence": 0.916
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
                  "confidence": 0.818
                }
              ]
            },
            {
              "id": 30,
              "start": 119.97,
              "end": 122.7,
              "text": " But you guys really don't know how important it is with its culture",
              "no_speech_prob": 0.0003879508003592491,
              "confidence": 0.979,
              "words": [
                {
                  "text": "But",
                  "start": 119.97,
                  "end": 120.16,
                  "confidence": 0.846
                },
                {
                  "text": "you",
                  "start": 120.16,
                  "end": 120.28,
                  "confidence": 0.918
                },
                {
                  "text": "guys",
                  "start": 120.28,
                  "end": 120.42,
                  "confidence": 0.985
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
                  "confidence": 1.0
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
                  "end": 121.6,
                  "confidence": 0.998
                },
                {
                  "text": "it",
                  "start": 121.6,
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
                  "confidence": 0.983
                },
                {
                  "text": "culture",
                  "start": 122.28,
                  "end": 122.7,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 31,
              "start": 123.08,
              "end": 128.74,
              "text": " interesting fact that in 2007 major spots equaling a buffer zone of approximately",
              "no_speech_prob": 0.0003879508003592491,
              "confidence": 0.93,
              "words": [
                {
                  "text": "interesting",
                  "start": 123.08,
                  "end": 123.62,
                  "confidence": 0.57
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
                  "end": 124.7,
                  "confidence": 0.999
                },
                {
                  "text": "2007",
                  "start": 124.7,
                  "end": 125.54,
                  "confidence": 0.763
                },
                {
                  "text": "major",
                  "start": 125.54,
                  "end": 126.14,
                  "confidence": 0.971
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
                  "confidence": 0.948
                },
                {
                  "text": "a",
                  "start": 127.26,
                  "end": 127.44,
                  "confidence": 0.99
                },
                {
                  "text": "buffer",
                  "start": 127.44,
                  "end": 127.74,
                  "confidence": 0.998
                },
                {
                  "text": "zone",
                  "start": 127.74,
                  "end": 128.04,
                  "confidence": 0.991
                },
                {
                  "text": "of",
                  "start": 128.04,
                  "end": 128.22,
                  "confidence": 0.993
                },
                {
                  "text": "approximately",
                  "start": 128.22,
                  "end": 128.74,
                  "confidence": 0.991
                }
              ]
            },
            {
              "id": 32,
              "start": 129.78,
              "end": 138.24,
              "text": " 207,000 hectares which are called the coffee cultural landscape were considered a UNESCO World Heritage Site and also in",
              "no_speech_prob": 0.0003879508003592491,
              "confidence": 0.926,
              "words": [
                {
                  "text": "207,000",
                  "start": 129.78,
                  "end": 130.78,
                  "confidence": 0.982
                },
                {
                  "text": "hectares",
                  "start": 130.78,
                  "end": 131.48,
                  "confidence": 0.952
                },
                {
                  "text": "which",
                  "start": 131.48,
                  "end": 131.82,
                  "confidence": 0.873
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
                  "confidence": 0.982
                },
                {
                  "text": "cultural",
                  "start": 133.14,
                  "end": 133.6,
                  "confidence": 0.984
                },
                {
                  "text": "landscape",
                  "start": 133.6,
                  "end": 134.24,
                  "confidence": 0.967
                },
                {
                  "text": "were",
                  "start": 134.24,
                  "end": 134.64,
                  "confidence": 0.85
                },
                {
                  "text": "considered",
                  "start": 134.64,
                  "end": 135.2,
                  "confidence": 0.982
                },
                {
                  "text": "a",
                  "start": 135.2,
                  "end": 135.44,
                  "confidence": 0.998
                },
                {
                  "text": "UNESCO",
                  "start": 135.44,
                  "end": 135.88,
                  "confidence": 0.85
                },
                {
                  "text": "World",
                  "start": 135.88,
                  "end": 136.2,
                  "confidence": 0.926
                },
                {
                  "text": "Heritage",
                  "start": 136.2,
                  "end": 136.74,
                  "confidence": 0.982
                },
                {
                  "text": "Site",
                  "start": 136.74,
                  "end": 137.2,
                  "confidence": 0.643
                },
                {
                  "text": "and",
                  "start": 137.2,
                  "end": 137.74,
                  "confidence": 0.924
                },
                {
                  "text": "also",
                  "start": 137.74,
                  "end": 138.04,
                  "confidence": 0.732
                },
                {
                  "text": "in",
                  "start": 138.04,
                  "end": 138.24,
                  "confidence": 0.974
                }
              ]
            },
            {
              "id": 33,
              "start": 138.24,
              "end": 146.24,
              "text": " 2007 the EU the European Union granted Colombian coffee a protected designation of origin status now",
              "no_speech_prob": 0.0003879508003592491,
              "confidence": 0.938,
              "words": [
                {
                  "text": "2007",
                  "start": 138.24,
                  "end": 139.1,
                  "confidence": 0.995
                },
                {
                  "text": "the",
                  "start": 139.1,
                  "end": 139.36,
                  "confidence": 0.982
                },
                {
                  "text": "EU",
                  "start": 139.36,
                  "end": 139.78,
                  "confidence": 0.975
                },
                {
                  "text": "the",
                  "start": 139.78,
                  "end": 139.96,
                  "confidence": 0.992
                },
                {
                  "text": "European",
                  "start": 139.96,
                  "end": 140.42,
                  "confidence": 0.996
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
                  "confidence": 0.988
                },
                {
                  "text": "Colombian",
                  "start": 141.28,
                  "end": 141.92,
                  "confidence": 0.915
                },
                {
                  "text": "coffee",
                  "start": 141.92,
                  "end": 142.34,
                  "confidence": 0.981
                },
                {
                  "text": "a",
                  "start": 142.34,
                  "end": 142.78,
                  "confidence": 0.993
                },
                {
                  "text": "protected",
                  "start": 142.78,
                  "end": 143.34,
                  "confidence": 0.819
                },
                {
                  "text": "designation",
                  "start": 143.34,
                  "end": 144.2,
                  "confidence": 0.893
                },
                {
                  "text": "of",
                  "start": 144.2,
                  "end": 144.56,
                  "confidence": 0.993
                },
                {
                  "text": "origin",
                  "start": 144.56,
                  "end": 145.1,
                  "confidence": 0.937
                },
                {
                  "text": "status",
                  "start": 145.1,
                  "end": 145.9,
                  "confidence": 0.965
                },
                {
                  "text": "now",
                  "start": 145.9,
                  "end": 146.24,
                  "confidence": 0.681
                }
              ]
            },
            {
              "id": 34,
              "start": 146.24,
              "end": 153.1,
              "text": " Interesting enough when it comes to the coffee in Colombia, believe it or not. It is not actually native to the country",
              "no_speech_prob": 1.6100901120807976e-05,
              "confidence": 0.959,
              "words": [
                {
                  "text": "Interesting",
                  "start": 146.24,
                  "end": 146.68,
                  "confidence": 0.63
                },
                {
                  "text": "enough",
                  "start": 146.68,
                  "end": 146.98,
                  "confidence": 0.998
                },
                {
                  "text": "when",
                  "start": 146.98,
                  "end": 147.12,
                  "confidence": 0.991
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
                  "end": 147.52,
                  "confidence": 0.999
                },
                {
                  "text": "to",
                  "start": 147.52,
                  "end": 147.64,
                  "confidence": 0.999
                },
                {
                  "text": "the",
                  "start": 147.64,
                  "end": 147.78,
                  "confidence": 0.998
                },
                {
                  "text": "coffee",
                  "start": 147.78,
                  "end": 148.24,
                  "confidence": 0.992
                },
                {
                  "text": "in",
                  "start": 148.24,
                  "end": 148.56,
                  "confidence": 0.998
                },
                {
                  "text": "Colombia,",
                  "start": 148.56,
                  "end": 149.14,
                  "confidence": 0.762
                },
                {
                  "text": "believe",
                  "start": 149.42,
                  "end": 149.52,
                  "confidence": 0.994
                },
                {
                  "text": "it",
                  "start": 149.52,
                  "end": 149.7,
                  "confidence": 0.999
                },
                {
                  "text": "or",
                  "start": 149.7,
                  "end": 149.8,
                  "confidence": 0.999
                },
                {
                  "text": "not.",
                  "start": 149.8,
                  "end": 150.06,
                  "confidence": 1.0
                },
                {
                  "text": "It",
                  "start": 150.14,
                  "end": 150.24,
                  "confidence": 0.998
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
                  "end": 151.12,
                  "confidence": 0.993
                },
                {
                  "text": "actually",
                  "start": 151.12,
                  "end": 151.8,
                  "confidence": 0.91
                },
                {
                  "text": "native",
                  "start": 151.8,
                  "end": 152.32,
                  "confidence": 0.966
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
                  "end": 153.1,
                  "confidence": 0.999
                }
              ]
            },
            {
              "id": 35,
              "start": 153.54,
              "end": 158.91,
              "text": " It's come from somewhere else not really an invasive species because it's very much welcomed now",
              "no_speech_prob": 1.6100901120807976e-05,
              "confidence": 0.921,
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
                  "confidence": 0.999
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
                  "end": 155.44,
                  "confidence": 0.475
                },
                {
                  "text": "really",
                  "start": 155.44,
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
                  "confidence": 0.998
                },
                {
                  "text": "species",
                  "start": 156.24,
                  "end": 156.76,
                  "confidence": 0.997
                },
                {
                  "text": "because",
                  "start": 156.76,
                  "end": 157.1,
                  "confidence": 0.985
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
                  "end": 158.42,
                  "confidence": 0.973
                },
                {
                  "text": "now",
                  "start": 158.42,
                  "end": 158.91,
                  "confidence": 0.549
                }
              ]
            },
            {
              "id": 36,
              "start": 158.91,
              "end": 162.99,
              "text": " You may have also seen this guy on many different Colombian coffee brands now",
              "no_speech_prob": 1.6100901120807976e-05,
              "confidence": 0.924,
              "words": [
                {
                  "text": "You",
                  "start": 158.91,
                  "end": 159.1,
                  "confidence": 0.932
                },
                {
                  "text": "may",
                  "start": 159.1,
                  "end": 159.28,
                  "confidence": 1.0
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
                  "end": 160.72,
                  "confidence": 0.999
                },
                {
                  "text": "on",
                  "start": 160.72,
                  "end": 160.92,
                  "confidence": 0.999
                },
                {
                  "text": "many",
                  "start": 160.92,
                  "end": 161.12,
                  "confidence": 0.998
                },
                {
                  "text": "different",
                  "start": 161.12,
                  "end": 161.4,
                  "confidence": 0.998
                },
                {
                  "text": "Colombian",
                  "start": 161.4,
                  "end": 162.06,
                  "confidence": 0.956
                },
                {
                  "text": "coffee",
                  "start": 162.06,
                  "end": 162.46,
                  "confidence": 0.992
                },
                {
                  "text": "brands",
                  "start": 162.46,
                  "end": 162.84,
                  "confidence": 0.991
                },
                {
                  "text": "now",
                  "start": 162.84,
                  "end": 162.99,
                  "confidence": 0.368
                }
              ]
            },
            {
              "id": 37,
              "start": 162.99,
              "end": 170.02,
              "text": " His name is Juan Valdez. Now. Some people think that this guy is actually real. He's a real coffee farmer. Somebody just drew",
              "no_speech_prob": 1.6100901120807976e-05,
              "confidence": 0.969,
              "words": [
                {
                  "text": "His",
                  "start": 162.99,
                  "end": 163.24,
                  "confidence": 0.984
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
                  "confidence": 0.863
                },
                {
                  "text": "Valdez.",
                  "start": 164.08,
                  "end": 164.7,
                  "confidence": 0.985
                },
                {
                  "text": "Now.",
                  "start": 164.78,
                  "end": 164.88,
                  "confidence": 0.995
                },
                {
                  "text": "Some",
                  "start": 164.94,
                  "end": 165.06,
                  "confidence": 1.0
                },
                {
                  "text": "people",
                  "start": 165.06,
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
                  "end": 165.78,
                  "confidence": 0.999
                },
                {
                  "text": "this",
                  "start": 165.78,
                  "end": 166.02,
                  "confidence": 1.0
                },
                {
                  "text": "guy",
                  "start": 166.02,
                  "end": 166.28,
                  "confidence": 1.0
                },
                {
                  "text": "is",
                  "start": 166.28,
                  "end": 166.42,
                  "confidence": 0.999
                },
                {
                  "text": "actually",
                  "start": 166.42,
                  "end": 166.92,
                  "confidence": 0.998
                },
                {
                  "text": "real.",
                  "start": 166.92,
                  "end": 167.4,
                  "confidence": 0.593
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
                  "end": 168.04,
                  "confidence": 0.999
                },
                {
                  "text": "coffee",
                  "start": 168.04,
                  "end": 168.52,
                  "confidence": 0.998
                },
                {
                  "text": "farmer.",
                  "start": 168.52,
                  "end": 169.02,
                  "confidence": 0.995
                },
                {
                  "text": "Somebody",
                  "start": 169.12,
                  "end": 169.46,
                  "confidence": 0.99
                },
                {
                  "text": "just",
                  "start": 169.46,
                  "end": 169.72,
                  "confidence": 0.989
                },
                {
                  "text": "drew",
                  "start": 169.72,
                  "end": 170.02,
                  "confidence": 0.952
                }
              ]
            }
          ]
        }
      ],
      "process_output_files": [
        "../../data/output/09342ea4-cf52-4bb8-9f63-6785af3cb117.json"
      ]
    }



```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
