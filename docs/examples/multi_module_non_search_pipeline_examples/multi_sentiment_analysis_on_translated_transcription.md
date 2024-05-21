## Multi-Module Pipeline: Sentiment Analysis on Translated Transcription

This document details a modular pipeline that takes in an audio file in a non-English language, [`transcribes`](../../modules/ai_model_modules/transcribe_module.md) it, [`translates`](../../modules/ai_model_modules/translate_module.md) the transcript into English, and then performs [`sentiment analysis`](../../modules/ai_model_modules/sentiment_module.md) on each sentence of the translated transcript.

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

- A [`transcribe`](../../modules/ai_model_modules/transcribe_module.md) module.

- A [`translate`](../../modules/ai_model_modules/translate_module.md) module.

- A [`json-to-txt`](../../modules/support_function_modules/json-to-txt_module.md) module.

- A [`parser`](../../modules/ai_model_modules/parser_module.md) module.

- A [`sentiment`](../../modules/ai_model_modules/sentiment_module.md) module.

We use the [`json-to-txt`](../../modules/support_function_modules/json-to-txt_module.md) and [`parser`](../../modules/ai_model_modules/parser_module.md) combination, which combines the transcribed snippets into one document and then splices it again, to make sure that any pauses in speech don't make for partial snippets that can confuse the [`sentiment`](../../modules/ai_model_modules/sentiment_module.md) model.

Pipeline setup is accomplished through the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method, as follows:


```python
# create a pipeline as detailed above

pipeline_1 = krixik.create_pipeline(name="multi_sentiment_analysis_on_translated_transcription",
                                    module_chain=["transcribe",
                                                  "translate",
                                                  "json-to-txt",
                                                  "parser",
                                                  "sentiment"])
```

### Processing an Input File

Lets take a quick look at a test file before processing. Given that we're [`translating`](../../modules/ai_model_modules/translate_module.md) before performing [`sentiment`](../../modules/ai_model_modules/sentiment_module.md), we'll start with a Spanish-language audio file.


```python
# examine contents of input file

from IPython.display import Video
Video("../../../data/input/deadlift.mp3")
```




<video src="../../../data/input/deadlift.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



Since the input audio is in Spanish, we'll use the (non-default) [`opus-mt-es-en`](https://huggingface.co/Helsinki-NLP/opus-mt-es-en) model of the [`translate`](../../modules/ai_model_modules/translate_module.md) module to translate its transcript into English. We will also leverage a stronger model than the [default](../../modules/ai_model_modules/transcribe_module.md#available-models-in-the-transcribe-module) for our [`transcription`](../../modules/ai_model_modules/transcribe_module.md).

We will use the default models for every other module in the pipeline as well, so they don't have to be specified in the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file through the pipeline, as described above

process_output_1 = pipeline_1.process(local_file_path = "../../../data/input/deadlift.mp3", # the initial local filepath where the input file is stored
                                      local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                      expire_time=60*30, # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True, # wait for process to complete before returning IDE control to user
                                      verbose=False, # do not display process update printouts upon running code
                                      modules={"transcribe": {"model": "whisper-base"}, "translate": {"model": "opus-mt-es-en"}}) # specify a non-default model for use in two modules whose type is only present once each in the pipeline (otherwise, would have to refer to them positionally)
```


    ---------------------------------------------------------------------------

    PermissionError                           Traceback (most recent call last)

    File ~\AppData\Local\Programs\Python\Python312\Lib\shutil.py:634, in _rmtree_unsafe(path, onexc)
        633 try:
    --> 634     os.unlink(fullname)
        635 except OSError as err:


    PermissionError: [WinError 32] The process cannot access the file because it is being used by another process: 'C:\\Users\\Lucas\\AppData\\Local\\Temp\\tmpw7ghvu4q\\krixik_converted_version_deadlift.mp3'

    
    During handling of the above exception, another exception occurred:


    PermissionError                           Traceback (most recent call last)

    File ~\AppData\Local\Programs\Python\Python312\Lib\tempfile.py:891, in TemporaryDirectory._rmtree.<locals>.onexc(func, path, exc)
        890 try:
    --> 891     _os.unlink(path)
        892 # PermissionError is raised on FreeBSD for directories


    PermissionError: [WinError 32] The process cannot access the file because it is being used by another process: 'C:\\Users\\Lucas\\AppData\\Local\\Temp\\tmpw7ghvu4q\\krixik_converted_version_deadlift.mp3'

    
    During handling of the above exception, another exception occurred:


    NotADirectoryError                        Traceback (most recent call last)

    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\utilities\converters\utilities\decorators.py:28, in datatype_converter_wrapper.<locals>.converter_wrapper(*args, **kwargs)
         27 if conversion is not None:
    ---> 28     with tempfile.TemporaryDirectory() as conversion_save_directory:
         29         og_local_file_path = copy.deepcopy(local_file_path)


    File ~\AppData\Local\Programs\Python\Python312\Lib\tempfile.py:919, in TemporaryDirectory.__exit__(self, exc, value, tb)
        918 if self._delete:
    --> 919     self.cleanup()


    File ~\AppData\Local\Programs\Python\Python312\Lib\tempfile.py:923, in TemporaryDirectory.cleanup(self)
        922 if self._finalizer.detach() or _os.path.exists(self.name):
    --> 923     self._rmtree(self.name, ignore_errors=self._ignore_cleanup_errors)


    File ~\AppData\Local\Programs\Python\Python312\Lib\tempfile.py:903, in TemporaryDirectory._rmtree(cls, name, ignore_errors)
        901             raise
    --> 903 _shutil.rmtree(name, onexc=onexc)


    File ~\AppData\Local\Programs\Python\Python312\Lib\shutil.py:796, in rmtree(path, ignore_errors, onerror, onexc, dir_fd)
        795     return
    --> 796 return _rmtree_unsafe(path, onexc)


    File ~\AppData\Local\Programs\Python\Python312\Lib\shutil.py:636, in _rmtree_unsafe(path, onexc)
        635         except OSError as err:
    --> 636             onexc(os.unlink, fullname, err)
        637 try:


    File ~\AppData\Local\Programs\Python\Python312\Lib\tempfile.py:894, in TemporaryDirectory._rmtree.<locals>.onexc(func, path, exc)
        893     except (IsADirectoryError, PermissionError):
    --> 894         cls._rmtree(path, ignore_errors=ignore_errors)
        895 except FileNotFoundError:


    File ~\AppData\Local\Programs\Python\Python312\Lib\tempfile.py:903, in TemporaryDirectory._rmtree(cls, name, ignore_errors)
        901             raise
    --> 903 _shutil.rmtree(name, onexc=onexc)


    File ~\AppData\Local\Programs\Python\Python312\Lib\shutil.py:796, in rmtree(path, ignore_errors, onerror, onexc, dir_fd)
        795     return
    --> 796 return _rmtree_unsafe(path, onexc)


    File ~\AppData\Local\Programs\Python\Python312\Lib\shutil.py:612, in _rmtree_unsafe(path, onexc)
        611 except OSError as err:
    --> 612     onexc(os.scandir, path, err)
        613     entries = []


    File ~\AppData\Local\Programs\Python\Python312\Lib\shutil.py:609, in _rmtree_unsafe(path, onexc)
        608 try:
    --> 609     with os.scandir(path) as scandir_it:
        610         entries = list(scandir_it)


    NotADirectoryError: [WinError 267] The directory name is invalid: 'C:\\Users\\Lucas\\AppData\\Local\\Temp\\tmpw7ghvu4q\\krixik_converted_version_deadlift.mp3'

    
    During handling of the above exception, another exception occurred:


    Exception                                 Traceback (most recent call last)

    Cell In[4], line 3
          1 # process the file through the pipeline, as described above
    ----> 3 process_output_1 = pipeline_1.process(local_file_path = "../../../data/input/deadlift.mp4", # the initial local filepath where the input file is stored
          4                                       local_save_directory="../../../data/output", # the local directory that the output file will be saved to
          5                                       expire_time=60*30, # process data will be deleted from the Krixik system in 30 minutes
          6                                       wait_for_process=True, # wait for process to complete before returning IDE control to user
          7                                       verbose=False, # do not display process update printouts upon running code
          8                                       modules={"transcribe": {"model": "whisper-base"}, "translate": {"model": "opus-mt-es-en"}}) # specify a non-default model for use in two modules whose type is only present once each in the pipeline (otherwise, would have to refer to them positionally)


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\system_builder\utilities\decorators.py:97, in kwargs_checker.<locals>.wrapper(*args, **kwargs)
         95 if unexpected_args:
         96     raise TypeError(f"unexpected keyword argument(s) for '{func_name}': {', '.join(unexpected_args)}")
    ---> 97 return func(*args, **kwargs)


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\system_builder\functions\checkin.py:67, in check_init_decorator.<locals>.wrapper(self, *args, **kwargs)
         64 @functools.wraps(func)
         65 def wrapper(self, *args, **kwargs):
         66     check_init(self)
    ---> 67     return func(self, *args, **kwargs)


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\utilities\converters\utilities\decorators.py:93, in datatype_converter_wrapper.<locals>.converter_wrapper(*args, **kwargs)
         91     raise PermissionError(e)
         92 except Exception as e:
    ---> 93     raise Exception(e)


    Exception: [WinError 267] The directory name is invalid: 'C:\\Users\\Lucas\\AppData\\Local\\Temp\\tmpw7ghvu4q\\krixik_converted_version_deadlift.mp3'


The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a JSON file, the process output is provided in this object as well (this is only the case for JSON outputs).  Moreover, the output file itself has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process

print(json.dumps(process_output_1, indent=2))
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



```python
# delete all processed datapoints belonging to this pipeline

reset_pipeline(pipeline_1)
```
