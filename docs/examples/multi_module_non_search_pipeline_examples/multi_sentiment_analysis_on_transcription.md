## Multi-Module Pipeline: Sentiment Analysis on Transcription

This document details a modular pipeline that takes in an audio/video file in English, [`transcribes`](../modules/ai_model_modules/transcribe_module.md) it, and then performs [`sentiment analysis`](../modules/ai_model_modules/sentiment_module.md) on each sentence of the transcript.

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)

### Pipeline Setup

To achieve what we've described above, let's set up a pipeline sequentially consisting of the following modules:

- A [`transcribe`](../modules/ai_model_modules/transcribe_module.md) module.

- A [`json-to-txt`](../modules/support_function_modules/json-to-txt_module.md) module.

- A [`parser`](../modules/ai_model_modules/parser_module.md) module.

- A [`sentiment`](../modules/ai_model_modules/sentiment_module.md) module.

We use the [`json-to-txt`](../modules/support_function_modules/json-to-txt_module.md) and [`parser`](../modules/ai_model_modules/parser_module.md) combination, which combines the transcribed snippets into one document and then splices it again, to make sure that any pauses in speech don't make for partial snippets that can confuse the [`sentiment`](../modules/ai_model_modules/sentiment_module.md) model.

Pipeline setup is accomplished through the [`.create_pipeline`](../system/pipeline_creation/create_pipeline.md) method, as follows:


```python
# create a pipeline as detailed above

pipeline_1 = krixik.create_pipeline(name="multi_sentiment_analysis_on_transcription",
                                    module_chain=["transcribe",
                                                  "json-to-txt",
                                                  "parser",
                                                  "sentiment"])
```

### Processing an Input File

Lets take a quick look at a short test file before processing.


```python
# examine contents of input file

from IPython.display import Video
Video("../../../data/input/Interesting Facts About Colombia.mp4")
```




<video src="../../../data/input/Interesting Facts About Colombia.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



We will use the default models for every module in the pipeline, so the [`modules`](../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) method doesn't need to be leveraged.


```python
# process the file through the pipeline, as described above

process_output_1 = pipeline_1.process(local_file_path = "../../../data/input/Interesting Facts About Colombia.mp4", # the initial local filepath where the input file is stored
                                      local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                      expire_time=60*30, # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True, # wait for process to complete before returning IDE control to user
                                      verbose=False) # do not display process update printouts upon running code
```

    INFO: Checking that file size falls within acceptable parameters...
    INFO:...success!
    converted ../../input_data/Interesting Facts About Colombia.mp4 to: /var/folders/k9/0vtmhf0s5h56gt15mkf07b1r0000gn/T/tmpas8o2_np/krixik_converted_version_Interesting Facts About Colombia.mp3
    INFO: hydrated input modules: {'transcribe': {'model': 'whisper-tiny', 'params': {}}, 'json-to-txt': {'model': 'base', 'params': {}}, 'parser': {'model': 'sentence', 'params': {}}, 'sentiment': {'model': 'distilbert-base-uncased-finetuned-sst-2-english', 'params': {}}}
    INFO: symbolic_directory_path was not set by user - setting to default of /etc
    INFO: file_name was not set by user - setting to random file name: krixik_generated_file_name_gndqwwmyqb.mp3
    INFO: wait_for_process is set to True.
    INFO: file will expire and be removed from you account in 300 seconds, at Mon Apr 29 15:42:13 2024 UTC
    INFO: transcribe-sentiment-pipeline file process and input processing started...
    INFO: metadata can be updated using the .update api.
    INFO: This process's request_id is: e3bdba39-9c7f-ea8d-05c8-2e83a524bbbe
    INFO: File process and processing status:
    SUCCESS: module 1 (of 4) - transcribe processing complete.
    SUCCESS: module 2 (of 4) - json-to-txt processing complete.
    SUCCESS: module 3 (of 4) - parser processing complete.
    SUCCESS: module 4 (of 4) - sentiment processing complete.
    SUCCESS: pipeline process complete.
    SUCCESS: process output downloaded


The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a JSON file, the process output is provided in this object as well (this is only the case for JSON outputs).  Moreover, the output file itself has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process

print(json.dumps(process_output_1, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "transcribe-sentiment-pipeline",
      "request_id": "bca798e6-85de-4f8a-9974-744108545dae",
      "file_id": "dfaced90-11ed-41c8-9bf0-8751656be563",
      "message": "SUCCESS - output fetched for file_id dfaced90-11ed-41c8-9bf0-8751656be563.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": " That's the episode looking at the great country of Columbia.",
          "positive": 0.993,
          "negative": 0.007,
          "neutral": 0.0
        },
        {
          "snippet": "We looked at some really basic facts.",
          "positive": 0.252,
          "negative": 0.748,
          "neutral": 0.0
        },
        {
          "snippet": "It's name, a bit of its history, the type of people that live there, land size, and all that jazz.",
          "positive": 0.998,
          "negative": 0.002,
          "neutral": 0.0
        },
        {
          "snippet": "But in this video, we're going to go into a little bit more of a detailed look.",
          "positive": 0.992,
          "negative": 0.008,
          "neutral": 0.0
        },
        {
          "snippet": "Yo, what is going on guys?",
          "positive": 0.005,
          "negative": 0.995,
          "neutral": 0.0
        },
        {
          "snippet": "Welcome back to F2D facts.",
          "positive": 0.999,
          "negative": 0.001,
          "neutral": 0.0
        },
        {
          "snippet": "The channel where I look at people cultures and places.",
          "positive": 0.999,
          "negative": 0.001,
          "neutral": 0.0
        },
        {
          "snippet": "My name is Dave Wouple, and today we are going to be looking more at Columbia and our Columbia part two video.",
          "positive": 0.027,
          "negative": 0.973,
          "neutral": 0.0
        },
        {
          "snippet": "Which just reminds me guys, this is part of our Columbia playlist.",
          "positive": 0.997,
          "negative": 0.003,
          "neutral": 0.0
        },
        {
          "snippet": "So put it down in the description box below, and I'll talk about that more in the video.",
          "positive": 0.005,
          "negative": 0.995,
          "neutral": 0.0
        },
        {
          "snippet": "But if you're new here, join me every single Monday to learn about new countries from around the world.",
          "positive": 0.999,
          "negative": 0.001,
          "neutral": 0.0
        },
        {
          "snippet": "You can do that by hitting that subscribe and that belt notification button.",
          "positive": 0.016,
          "negative": 0.984,
          "neutral": 0.0
        },
        {
          "snippet": "But let's get started.",
          "positive": 0.03,
          "negative": 0.97,
          "neutral": 0.0
        },
        {
          "snippet": "Learn about Columbia.",
          "positive": 0.999,
          "negative": 0.001,
          "neutral": 0.0
        },
        {
          "snippet": "So we all know Columbia is famous for its coffee, right?",
          "positive": 0.977,
          "negative": 0.023,
          "neutral": 0.0
        },
        {
          "snippet": "Yes, right.",
          "positive": 1.0,
          "negative": 0.0,
          "neutral": 0.0
        },
        {
          "snippet": "I know.",
          "positive": 0.997,
          "negative": 0.003,
          "neutral": 0.0
        },
        {
          "snippet": "You guys are sitting there going, five bucks says he's going to talk about coffee.",
          "positive": 0.974,
          "negative": 0.026,
          "neutral": 0.0
        },
        {
          "snippet": "Well, I am.",
          "positive": 1.0,
          "negative": 0.0,
          "neutral": 0.0
        },
        {
          "snippet": "That's right, because I got my van.",
          "positive": 0.999,
          "negative": 0.001,
          "neutral": 0.0
        },
        {
          "snippet": "You Columbia coffee right here.",
          "positive": 0.407,
          "negative": 0.593,
          "neutral": 0.0
        },
        {
          "snippet": "Boom advertisement.",
          "positive": 0.944,
          "negative": 0.056,
          "neutral": 0.0
        },
        {
          "snippet": "Yeah.",
          "positive": 1.0,
          "negative": 0.0,
          "neutral": 0.0
        },
        {
          "snippet": "Then I'm paying me for this.",
          "positive": 0.217,
          "negative": 0.783,
          "neutral": 0.0
        },
        {
          "snippet": "I'm care.",
          "positive": 1.0,
          "negative": 0.0,
          "neutral": 0.0
        },
        {
          "snippet": "So which might not know about coffee is yes, you probably already know that a lot of companies actually buy it up.",
          "positive": 0.039,
          "negative": 0.961,
          "neutral": 0.0
        },
        {
          "snippet": "Starbucks buys all had a coffee from Columbia.",
          "positive": 0.048,
          "negative": 0.952,
          "neutral": 0.0
        },
        {
          "snippet": "It's kind of like their favorite place to buy coffee.",
          "positive": 0.995,
          "negative": 0.005,
          "neutral": 0.0
        },
        {
          "snippet": "And kind of to pay tribute to that Starbucks when they're making their 1,000th store in 2016, they decided, yo, we're going to put it in Columbia.",
          "positive": 0.968,
          "negative": 0.032,
          "neutral": 0.0
        },
        {
          "snippet": "And this was in the town of Medellin, Columbia.",
          "positive": 0.13,
          "negative": 0.87,
          "neutral": 0.0
        },
        {
          "snippet": "Now here's the thing, when it comes to coffee in Columbia, they are the third largest producing and exporting coffee country in the world.",
          "positive": 0.997,
          "negative": 0.003,
          "neutral": 0.0
        },
        {
          "snippet": "The amount of coffee that is exported from Columbia equals about 810,000 metric tons or approximately 11.5 million bags.",
          "positive": 0.043,
          "negative": 0.957,
          "neutral": 0.0
        },
        {
          "snippet": "However, although it might be beaten by countries like Brazil, it is actually the number one or highest country for producing and growing a specific type of bean known as the Arab Beka bean.",
          "positive": 0.999,
          "negative": 0.001,
          "neutral": 0.0
        },
        {
          "snippet": "And I know coffee is really important when it comes to talking about Columbia, but you guys really don't know how important it is with its culture.",
          "positive": 0.005,
          "negative": 0.995,
          "neutral": 0.0
        },
        {
          "snippet": "Interesting fact that in 2007, major spots equaling a buffer zone of approximately 207,000 hectares, which are called the coffee cultural landscape, were considered a UNESCO World Heritage Site.",
          "positive": 0.996,
          "negative": 0.004,
          "neutral": 0.0
        },
        {
          "snippet": "And also in 2007, the EU, the European Union, granted Colombian coffee a protected designation of origin status.",
          "positive": 0.995,
          "negative": 0.005,
          "neutral": 0.0
        },
        {
          "snippet": "Now interesting enough when it comes to the coffee in Columbia, believe it or not, it is not actually native to the country.",
          "positive": 0.979,
          "negative": 0.021,
          "neutral": 0.0
        },
        {
          "snippet": "It's come from somewhere else, not really an invasive species because it's very much welcomed.",
          "positive": 0.997,
          "negative": 0.003,
          "neutral": 0.0
        },
        {
          "snippet": "Now you may have also seen this guy on many different Colombian coffee brands.",
          "positive": 0.978,
          "negative": 0.022,
          "neutral": 0.0
        },
        {
          "snippet": "Now his name is Juan Valdez.",
          "positive": 0.989,
          "negative": 0.011,
          "neutral": 0.0
        },
        {
          "snippet": "Now some people think that this guy is actually really a real coffee farmer, somebody just drew.",
          "positive": 0.011,
          "negative": 0.989,
          "neutral": 0.0
        }
      ],
      "process_output_files": [
        "/Users/jeremywatt/Desktop/krixik-cli/docs/examples/transcribe/dfaced90-11ed-41c8-9bf0-8751656be563.json"
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
        "snippet": " That's the episode looking at the great country of Columbia.",
        "positive": 0.993,
        "negative": 0.007,
        "neutral": 0.0
      },
      {
        "snippet": "We looked at some really basic facts.",
        "positive": 0.252,
        "negative": 0.748,
        "neutral": 0.0
      },
      {
        "snippet": "It's name, a bit of its history, the type of people that live there, land size, and all that jazz.",
        "positive": 0.998,
        "negative": 0.002,
        "neutral": 0.0
      },
      {
        "snippet": "But in this video, we're going to go into a little bit more of a detailed look.",
        "positive": 0.992,
        "negative": 0.008,
        "neutral": 0.0
      },
      {
        "snippet": "Yo, what is going on guys?",
        "positive": 0.005,
        "negative": 0.995,
        "neutral": 0.0
      },
      {
        "snippet": "Welcome back to F2D facts.",
        "positive": 0.999,
        "negative": 0.001,
        "neutral": 0.0
      },
      {
        "snippet": "The channel where I look at people cultures and places.",
        "positive": 0.999,
        "negative": 0.001,
        "neutral": 0.0
      },
      {
        "snippet": "My name is Dave Wouple, and today we are going to be looking more at Columbia and our Columbia part two video.",
        "positive": 0.027,
        "negative": 0.973,
        "neutral": 0.0
      },
      {
        "snippet": "Which just reminds me guys, this is part of our Columbia playlist.",
        "positive": 0.997,
        "negative": 0.003,
        "neutral": 0.0
      },
      {
        "snippet": "So put it down in the description box below, and I'll talk about that more in the video.",
        "positive": 0.005,
        "negative": 0.995,
        "neutral": 0.0
      },
      {
        "snippet": "But if you're new here, join me every single Monday to learn about new countries from around the world.",
        "positive": 0.999,
        "negative": 0.001,
        "neutral": 0.0
      },
      {
        "snippet": "You can do that by hitting that subscribe and that belt notification button.",
        "positive": 0.016,
        "negative": 0.984,
        "neutral": 0.0
      },
      {
        "snippet": "But let's get started.",
        "positive": 0.03,
        "negative": 0.97,
        "neutral": 0.0
      },
      {
        "snippet": "Learn about Columbia.",
        "positive": 0.999,
        "negative": 0.001,
        "neutral": 0.0
      },
      {
        "snippet": "So we all know Columbia is famous for its coffee, right?",
        "positive": 0.977,
        "negative": 0.023,
        "neutral": 0.0
      },
      {
        "snippet": "Yes, right.",
        "positive": 1.0,
        "negative": 0.0,
        "neutral": 0.0
      },
      {
        "snippet": "I know.",
        "positive": 0.997,
        "negative": 0.003,
        "neutral": 0.0
      },
      {
        "snippet": "You guys are sitting there going, five bucks says he's going to talk about coffee.",
        "positive": 0.974,
        "negative": 0.026,
        "neutral": 0.0
      },
      {
        "snippet": "Well, I am.",
        "positive": 1.0,
        "negative": 0.0,
        "neutral": 0.0
      },
      {
        "snippet": "That's right, because I got my van.",
        "positive": 0.999,
        "negative": 0.001,
        "neutral": 0.0
      },
      {
        "snippet": "You Columbia coffee right here.",
        "positive": 0.407,
        "negative": 0.593,
        "neutral": 0.0
      },
      {
        "snippet": "Boom advertisement.",
        "positive": 0.944,
        "negative": 0.056,
        "neutral": 0.0
      },
      {
        "snippet": "Yeah.",
        "positive": 1.0,
        "negative": 0.0,
        "neutral": 0.0
      },
      {
        "snippet": "Then I'm paying me for this.",
        "positive": 0.217,
        "negative": 0.783,
        "neutral": 0.0
      },
      {
        "snippet": "I'm care.",
        "positive": 1.0,
        "negative": 0.0,
        "neutral": 0.0
      },
      {
        "snippet": "So which might not know about coffee is yes, you probably already know that a lot of companies actually buy it up.",
        "positive": 0.039,
        "negative": 0.961,
        "neutral": 0.0
      },
      {
        "snippet": "Starbucks buys all had a coffee from Columbia.",
        "positive": 0.048,
        "negative": 0.952,
        "neutral": 0.0
      },
      {
        "snippet": "It's kind of like their favorite place to buy coffee.",
        "positive": 0.995,
        "negative": 0.005,
        "neutral": 0.0
      },
      {
        "snippet": "And kind of to pay tribute to that Starbucks when they're making their 1,000th store in 2016, they decided, yo, we're going to put it in Columbia.",
        "positive": 0.968,
        "negative": 0.032,
        "neutral": 0.0
      },
      {
        "snippet": "And this was in the town of Medellin, Columbia.",
        "positive": 0.13,
        "negative": 0.87,
        "neutral": 0.0
      },
      {
        "snippet": "Now here's the thing, when it comes to coffee in Columbia, they are the third largest producing and exporting coffee country in the world.",
        "positive": 0.997,
        "negative": 0.003,
        "neutral": 0.0
      },
      {
        "snippet": "The amount of coffee that is exported from Columbia equals about 810,000 metric tons or approximately 11.5 million bags.",
        "positive": 0.043,
        "negative": 0.957,
        "neutral": 0.0
      },
      {
        "snippet": "However, although it might be beaten by countries like Brazil, it is actually the number one or highest country for producing and growing a specific type of bean known as the Arab Beka bean.",
        "positive": 0.999,
        "negative": 0.001,
        "neutral": 0.0
      },
      {
        "snippet": "And I know coffee is really important when it comes to talking about Columbia, but you guys really don't know how important it is with its culture.",
        "positive": 0.005,
        "negative": 0.995,
        "neutral": 0.0
      },
      {
        "snippet": "Interesting fact that in 2007, major spots equaling a buffer zone of approximately 207,000 hectares, which are called the coffee cultural landscape, were considered a UNESCO World Heritage Site.",
        "positive": 0.996,
        "negative": 0.004,
        "neutral": 0.0
      },
      {
        "snippet": "And also in 2007, the EU, the European Union, granted Colombian coffee a protected designation of origin status.",
        "positive": 0.995,
        "negative": 0.005,
        "neutral": 0.0
      },
      {
        "snippet": "Now interesting enough when it comes to the coffee in Columbia, believe it or not, it is not actually native to the country.",
        "positive": 0.979,
        "negative": 0.021,
        "neutral": 0.0
      },
      {
        "snippet": "It's come from somewhere else, not really an invasive species because it's very much welcomed.",
        "positive": 0.997,
        "negative": 0.003,
        "neutral": 0.0
      },
      {
        "snippet": "Now you may have also seen this guy on many different Colombian coffee brands.",
        "positive": 0.978,
        "negative": 0.022,
        "neutral": 0.0
      },
      {
        "snippet": "Now his name is Juan Valdez.",
        "positive": 0.989,
        "negative": 0.011,
        "neutral": 0.0
      },
      {
        "snippet": "Now some people think that this guy is actually really a real coffee farmer, somebody just drew.",
        "positive": 0.011,
        "negative": 0.989,
        "neutral": 0.0
      }
    ]

