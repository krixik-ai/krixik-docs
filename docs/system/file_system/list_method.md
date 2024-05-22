## The `.list` Method

After using the [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method to process one or several files through your chosen pipeline, you can retrieve the record of any file(s) with the `.list` method. You can `.list` by `file_id` or by any other metadata you included when initially processing the file.  

This overview of the `.list` method is divided into the following sections:

- [.list Method Arguments](#.list-method-arguments)
- [Example Pipeline Setup and File Processing](#example-pipeline-setup-and-file-processing)
- [Listing by `file_ids`](#listing-by-file_ids)
- [Listing by `file_names`](#listing-by-file_names)
- [Listing by `symbolic_directory_paths`](#listing-by-symbolic_directory_paths)
- [Listing by `file_tags`](#listing-by-file_tags)
- [Listing by `created_at` and `updated_at` Bookend Times](#listing-by-created_at-and-updated_at-bookend-times)
- [Wildcard Operator Arguments](#wildcard-operator-arguments)
- [The Global Root](#the-global-root)
- [Using Multiple Arguments with the `.list` Method](#using-multiple-arguments-with-the-.list-method)
- [Output Size Cap](#output-size-cap)


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


### `.list` Method Arguments

The `.list` method is very versatile. It allows you to list by several different metadata items and by a combination of different metadata items.

All of the following arguments are optional. However, you must use at least one argument for the `.list` method to function.

For a refresher on file system metadata arguments please visit the [`.process` method overview](../parameters_processing_files_through_pipelines/process_method.md). The metadata arguments you can use for `.list` are:

- `file_ids`: A list of one or several `file_id`s to return records for.

- `file_names`: A list of  one or several `file_name`s to return records for.

- `symbolic_directory_paths`: A list of one or several `symbolic_directory_path`s to return records for.

- `symbolic_file_paths`: A list of one or several `symbolic_file_path`s to return records for.

- `file_tags`: A list of one or several `file_tag`s to return records for. Note that individual file_tags suffice; if a file has several file tags and you include at least one of them as a `.list` argument, that file's record will be returned.

You may use wildcard operators with `file_names`, `symbolic_directory_paths`,`symbolic_file_paths`, and `file_tags` to retrieve records whose exact metadata you don't remember—or if you wish to retrieve records for a group of files that share similar metadata. More on wildcards operators [later](#wildcard-operator-arguments) in this document.

You may also list by timestamp bookends. The `.list` method accepts timestamps based on both the creation and latest-update times of your records. These are strings in the `"YYYY-MM-DD HH:MM:SS"` format, or alternatively just in the `"YYYY-MM-DD"` format.

- `created_at_start`: Filters out all files whose `created_at` time is earlier than what you've specified.

- `created_at_end`: Filters out all files whose `created_at` time is after what you've specified.

- `last_updated_start`: Filters out all files whose `last_updated` time is earlier than what you've specified.

- `last_updated_end`: Filters out all files whose `last_updated` time is after what you've specified.

Examples on how to use metadata and timestamps in the `.list` method are included below.

Note that file system metadata arguments operate on **OR** logic: for instance, if you `.list` by `file_names`, `file_ids`, and `file_tags`, any file that is a match for any of these will be returned. However, timestamp arguments operate on **AND** logic; all files returned must respect the given timestamp bookends. If two timestamp bookends are given and there is no overlap between them, the `.list` method will return nothing.

Finally, the `.list` method takes two additional optional arguments to help you organize your output:

- `max_files` (int): Determines the maximum number of file records `.list` should return. Defaults to none.

- `sort_order` (str): Specifies how results should be sorted. The two valid values for this argument are 'ascending' and 'descending' (in reference to creation timestamp). Defaults to 'descending'.

### Example Pipeline Setup and File Processing

We will need to create a pipeline and [`.process`](../parameters_processing_files_through_pipelines/process_method.md) a couple of files through it to illustrate usage of `.list`. We'll create a single-module pipeline with a [`summarize`](../../modules/ai_model_modules/summarize_module.md) module and [`.process`](../parameters_processing_files_through_pipelines/process_method.md) some TXT files that hold the text of some English-language classics.


```python
# create single-module summarize pipeline
pipeline = krixik.create_pipeline(name='list_method_1_summarize',
                                  module_chain=['summarize'])
```


```python
# process four files through the pipeline we just created.
process_output_1 = pipeline.process(local_file_path="../../../data/input/Frankenstein partial.txt", # the initial local filepath where the input file is stored
                                      expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                      verbose=False,  # do not display process update printouts upon running code
                                      symbolic_directory_path="/novels/gothic",
                                      file_name="Frankenstein.txt",
                                      file_tags=[{"author": "Shelley"}, {"category": "gothic"}, {"century": "19"}])

process_output_2 = pipeline.process(local_file_path="../../../data/input/Pride and Prejudice partial.txt", # the initial local filepath where the input file is stored
                                      expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                      verbose=False,  # do not display process update printouts upon running code
                                      symbolic_directory_path="/novels/romance",
                                      file_name="Pride and Prejudice.txt",
                                      file_tags=[{"author": "Austen"}, {"category": "romance"}, {"century": "19"}])

process_output_3 = pipeline.process(local_file_path="../../../data/input/Moby Dick partial.txt", # the initial local filepath where the input file is stored
                                      expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                      verbose=False,  # do not display process update printouts upon running code
                                      symbolic_directory_path="/novels/adventure",
                                      file_name="Moby Dick.txt",
                                      file_tags=[{"author": "Melville"}, {"category": "adventure"}, {"century": "19"}])

process_output_4 = pipeline.process(local_file_path="../../../data/input/Little Women partial.txt", # the initial local filepath where the input file is stored
                                      expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                      verbose=False,  # do not display process update printouts upon running code
                                      symbolic_directory_path="/novels/bildungsroman",
                                      file_name="Little Women.txt",
                                      file_tags=[{"author": "Alcott"}, {"category": "bildungsroman"}, {"century": "19"}])
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\utilities\validators\data\utilities\decorators.py:47, in datatype_validator.<locals>.wrapper(*args, **kwargs)
         46             raise ValueError(f"invalid file extension: '{extension}'")
    ---> 47     return func(*args, **kwargs)
         48 except ValueError as e:


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\utilities\validators\system\base\lower_case.py:163, in lower_case_decorator.<locals>.wrapper(*args, **kwargs)
        161     raise Exception(e)
    --> 163 return func(*args, **kwargs)


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\system_builder\base.py:548, in KrixikBasePipeline.process(self, file_name, symbolic_directory_path, symbolic_file_path, local_file_path, file_tags, file_description, modules, expire_time, verbose, wait_for_process, local_save_directory, download_output, og_local_file_path)
        547 # process s3 file via presigned url
    --> 548 self.__upload_file_to_s3_via_presignedurl(verbose=verbose)
        550 # reset class variables


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\system_builder\base.py:391, in KrixikBasePipeline.__upload_file_to_s3_via_presignedurl(self, verbose)
        390 except ValueError as err:
    --> 391     raise err


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\system_builder\base.py:367, in KrixikBasePipeline.__upload_file_to_s3_via_presignedurl(self, verbose)
        366 if "failure_module" in list(failure_status.keys()):
    --> 367     raise ValueError(
        368         f"processes associated with request_id '{failure_status['process_id']}' failed at module '{failure_status['failure_module']}'"
        369     )
        370 else:


    ValueError: processes associated with request_id '8594789e-42d3-b069-d0f2-2d5f0d33c3be' failed at module 'summarize'

    
    During handling of the above exception, another exception occurred:


    ValueError                                Traceback (most recent call last)

    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\utilities\validators\utilities\decorators.py:16, in type_check_inputs.<locals>.wrapper(self, *args, **kwargs)
         15 try:
    ---> 16     result = system_base_type_check_inputs(system_data_type_check_inputs(datatype_validator(lower_case_decorator(func))))(
         17         self, *args, **kwargs
         18     )
         20     return result


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\utilities\validators\system\base\utilities\decorators.py:143, in type_check_inputs.<locals>.wrapper(*args, **kwargs)
        141     raise Exception(e)
    --> 143 return func(*args, **kwargs)


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\utilities\validators\system\data\utilities\decorators.py:137, in type_check_inputs.<locals>.wrapper(*args, **kwargs)
        135     raise Exception(e)
    --> 137 return func(self_arg, *args[1:], **kwargs)


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\utilities\validators\data\utilities\decorators.py:49, in datatype_validator.<locals>.wrapper(*args, **kwargs)
         48 except ValueError as e:
    ---> 49     raise ValueError(e)
         50 except Exception as e:


    ValueError: processes associated with request_id '8594789e-42d3-b069-d0f2-2d5f0d33c3be' failed at module 'summarize'

    
    During handling of the above exception, another exception occurred:


    ValueError                                Traceback (most recent call last)

    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\utilities\converters\utilities\decorators.py:83, in datatype_converter_wrapper.<locals>.converter_wrapper(*args, **kwargs)
         82                 return func(*args, **kwargs)
    ---> 83     return func(*args, **kwargs)
         84 except ValueError as e:


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\modules\utilities\decorators.py:54, in type_check_inputs.<locals>.wrapper(*args, **kwargs)
         52     raise e
    ---> 54 return func(self_arg, *args[1:], **kwargs)


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\utilities\validators\utilities\decorators.py:23, in type_check_inputs.<locals>.wrapper(self, *args, **kwargs)
         22 except ValueError as e:
    ---> 23     raise ValueError(e)
         24 except TypeError as e:


    ValueError: processes associated with request_id '8594789e-42d3-b069-d0f2-2d5f0d33c3be' failed at module 'summarize'

    
    During handling of the above exception, another exception occurred:


    ValueError                                Traceback (most recent call last)

    Cell In[4], line 3
          1 # process four files through the pipeline we just created.
    ----> 3 process_output_1 = pipeline_1.process(local_file_path="../../../data/input/Frankenstein partial.txt", # the initial local filepath where the input file is stored
          4                                       expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
          5                                       wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
          6                                       verbose=False,  # do not display process update printouts upon running code
          7                                       symbolic_directory_path="/novels/gothic",
          8                                       file_name="Frankenstein.txt",
          9                                       file_tags=[{"author": "Shelley"}, {"category": "gothic"}, {"century": "19"}])
         11 process_output_2 = pipeline_1.process(local_file_path="../../../data/input/Pride and Prejudice partial.txt", # the initial local filepath where the input file is stored
         12                                       expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
         13                                       wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
       (...)
         16                                       file_name="Pride and Prejudice.txt",
         17                                       file_tags=[{"author": "Austen"}, {"category": "romance"}, {"century": "19"}])
         19 process_output_3 = pipeline_1.process(local_file_path="../../../data/input/Moby Dick partial.txt", # the initial local filepath where the input file is stored
         20                                       expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
         21                                       wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
       (...)
         24                                       file_name="Moby Dick.txt",
         25                                       file_tags=[{"author": "Melville"}, {"category": "adventure"}, {"century": "19"}])


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\system_builder\utilities\decorators.py:97, in kwargs_checker.<locals>.wrapper(*args, **kwargs)
         95 if unexpected_args:
         96     raise TypeError(f"unexpected keyword argument(s) for '{func_name}': {', '.join(unexpected_args)}")
    ---> 97 return func(*args, **kwargs)


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\system_builder\functions\checkin.py:67, in check_init_decorator.<locals>.wrapper(self, *args, **kwargs)
         64 @functools.wraps(func)
         65 def wrapper(self, *args, **kwargs):
         66     check_init(self)
    ---> 67     return func(self, *args, **kwargs)


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\utilities\converters\utilities\decorators.py:85, in datatype_converter_wrapper.<locals>.converter_wrapper(*args, **kwargs)
         83     return func(*args, **kwargs)
         84 except ValueError as e:
    ---> 85     raise ValueError(e)
         86 except TypeError as e:
         87     raise TypeError(e)


    ValueError: processes associated with request_id '8594789e-42d3-b069-d0f2-2d5f0d33c3be' failed at module 'summarize'


Let's quickly look at what the output for the four of these looks like. The first one:


```python
# nicely print the output of the first process
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


The second one:


```python
# nicely print the output of the second process
print(json.dumps(process_output_2, indent=2))
```

The third one:


```python
# nicely print the output of the third process
print(json.dumps(process_output_3, indent=2))
```

And the fourth one:


```python
# nicely print the output of the fourth process
print(json.dumps(process_output_4, indent=2))
```

### Listing by `file_ids`

Let's try listing by `file_ids`.

You have the `file_id` of each of the four files you processed; each was returned after processing finalized. Remember that you can list by multiple `file_id`s if you so choose, and it's easy to do so because `file_ids` is submitted in list format.

Listing for the <u>Frankenstein</u> and <u>Moby Dick</u> files is done as follows:


```python
# .list records for two of the uploaded files via file_ids
list_output = pipeline.list(file_ids=["XXXXX", "YYYY"])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "11dcf756-702c-421c-a85a-49dabc2cca7f",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-04-26 21:05:05",
          "process_id": "578cb0a2-0f19-4d83-4b05-3c543f5e2506",
          "created_at": "2024-04-26 21:05:05",
          "file_metadata": {
            "modules": {
              "parser": {
                "model": "sentence"
              }
            },
            "modules_data": {
              "parser": {
                "data_files_extensions": [
                  ".json"
                ]
              }
            }
          },
          "file_tags": [
            {
              "author": "orwell"
            },
            {
              "category": "fiction"
            }
          ],
          "file_description": "the first paragraph of 1984",
          "symbolic_directory_path": "/my/custom/filepath",
          "pipeline": "parser-pipeline-1",
          "file_id": "fb228e8e-eefd-4c52-b966-a49506d63f34",
          "expire_time": "2024-04-26 21:10:05",
          "file_name": "some_snippets.txt"
        }
      ]
    }


As you can see, a full record for each file was returned. To learn more about each metadata item, visit the documentation for the [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method, where they are gone into detail on.

### Listing by `file_names`

You can also list via `file_name`s. It works just like listing with `file_id`s above, but with `file_name` instead of `file_id`. We'll list <u>Pride and Prejudice</u> via `file_names`, as follows:


```python
# .list records for one of the uploaded files via file_names
list_output = pipeline.list(file_names=["Pride and Prejudice.txt"])

# nicely print the output of this .list
print(json.dumps(list_output, indent=2))
```

As you can see, a full record for each file was returned. To learn more about each metadata item, visit the documentation for the [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method, where they are gone into detail on.

### Listing by `symbolic_directory_paths`

You can also list via `symbolic_directory_paths`. It works just like listing with `file_id`s and `file_name`s above, but with `symbolic_directory_path` instead. We'll list <u>Little Women</u> and <u>Moby Dick</u> via `symbolic_directory_paths`, as follows:


```python
# .list records for two of the uploaded files via symbolic_directory_paths
list_output = pipeline.list(file_names=["/novels/bildungsroman", "/novels/adventure"])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "70c71a76-7ce9-43c7-86e7-838b7fa93d8e",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-04-26 21:05:05",
          "process_id": "578cb0a2-0f19-4d83-4b05-3c543f5e2506",
          "created_at": "2024-04-26 21:05:05",
          "file_metadata": {
            "modules": {
              "parser": {
                "model": "sentence"
              }
            },
            "modules_data": {
              "parser": {
                "data_files_extensions": [
                  ".json"
                ]
              }
            }
          },
          "file_tags": [
            {
              "author": "orwell"
            },
            {
              "category": "fiction"
            }
          ],
          "file_description": "the first paragraph of 1984",
          "symbolic_directory_path": "/my/custom/filepath",
          "pipeline": "parser-pipeline-1",
          "file_id": "fb228e8e-eefd-4c52-b966-a49506d63f34",
          "expire_time": "2024-04-26 21:10:05",
          "file_name": "some_snippets.txt"
        }
      ]
    }


As you can see, a full record for each file was returned. To learn more about each metadata item, visit the documentation for the [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method, where they are gone into detail on.

## Listing by `file_tags`

We can also list through `file_tags`.  We'll list for 19th century novels and any novels by 'Alcott', as follows:


```python
# .list records for two of the uploaded files via symbolic_directory_paths
list_output = pipeline.list(file_tags=[{"author": "alcott"}, {"century": 19}])

# nicely print the output of this process
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "7915929d-47cc-4fb9-82f6-b737ad823458",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-04-26 21:05:05",
          "process_id": "578cb0a2-0f19-4d83-4b05-3c543f5e2506",
          "created_at": "2024-04-26 21:05:05",
          "file_metadata": {
            "modules": {
              "parser": {
                "model": "sentence"
              }
            },
            "modules_data": {
              "parser": {
                "data_files_extensions": [
                  ".json"
                ]
              }
            }
          },
          "file_tags": [
            {
              "author": "orwell"
            },
            {
              "category": "fiction"
            }
          ],
          "file_description": "the first paragraph of 1984",
          "symbolic_directory_path": "/my/custom/filepath",
          "pipeline": "parser-pipeline-1",
          "file_id": "fb228e8e-eefd-4c52-b966-a49506d63f34",
          "expire_time": "2024-04-26 21:10:05",
          "file_name": "some_snippets.txt"
        }
      ]
    }


Given that every file included the file tag `{"century": 19}` when initially processed, all four files were listed. <u>Little Women</u> also included the file tag `{"author": "alcott"}`, but there's no duplication of results, so that file's record is only listed once.

### Listing by `created_at` and `updated_at` Bookend Times

To illustrate how to `.list` by timestamp bookends, let's first [`.process`](../parameters_processing_files_through_pipelines/process_method.md) one additional file through our pipeline:


```python
# process an additional file into earlier pipeline
process_output = pipeline.process(local_file_path="../../../data/input/A Tale of Two Cities.txt", # the initial local filepath where the input JSON file is stored
                                  expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                  wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                  verbose=False,  # do not display process update printouts upon running code
                                  symbolic_directory_path="/novels/historical",
                                  file_name="A Tale of Two Cities.txt",
                                  file_tags=[{"author": "Dickens"}, {"category": "hisorical"}, {"century": 19}])
```

    {
      "status_code": 200,
      "pipeline": "parser-pipeline-1",
      "request_id": "d3bca30e-d260-4c62-8aa9-91307b21d8b1",
      "file_id": "3b941b6f-bd05-4fbb-83fd-6fea80c25629",
      "message": "SUCCESS - output fetched for file_id 3b941b6f-bd05-4fbb-83fd-6fea80c25629.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
          "line_numbers": [
            1
          ]
        },
        {
          "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
          "line_numbers": [
            2,
            3,
            4,
            5
          ]
        }
      ],
      "process_output_files": [
        "./3b941b6f-bd05-4fbb-83fd-6fea80c25629.json"
      ]
    }


Listing by timestamp bookends is as straightforward as doing it by file system metadata. The following example only uses one type of bookend—`last_updated_start`—but all of them work the same way.

Based on the output from the file we just processed and the output from the four earlier files, we'll choose a time/date that falls in the middle of all five `last_updated` timestamps:


```python
# .list process records by last_updated timestamp bookend
list_output = pipeline.list(created_at_start="XXXX")

# nicely print the output of this .list
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "aacbb5e9-4701-454b-be2d-16d0f812a201",
      "message": "Successfully returned 1 item.  Note: all timestamps in UTC.",
      "warnings": [],
      "items": [
        {
          "last_updated": "2024-04-26 21:05:21",
          "process_id": "132561f2-336b-c889-ba9e-500df80fdd38",
          "created_at": "2024-04-26 21:05:21",
          "file_metadata": {
            "modules": {
              "parser": {
                "model": "sentence"
              }
            },
            "modules_data": {
              "parser": {
                "data_files_extensions": [
                  ".json"
                ]
              }
            },
            "pipeline_ordered_modules": [
              "parser"
            ],
            "pipeline_output_process_keys": [
              "snippet"
            ]
          },
          "file_tags": [],
          "file_description": "",
          "symbolic_directory_path": "/etc",
          "pipeline": "parser-pipeline-1",
          "file_id": "3b941b6f-bd05-4fbb-83fd-6fea80c25629",
          "expire_time": "2024-04-26 21:10:21",
          "file_name": "krixik_generated_file_name_zqdsvltyrw.txt"
        }
      ]
    }


Keep in mind that timestamp bookend arguments operate with **AND** logic: to be listed, a file _must_ fall within the specified timestamp window. This also means that if two timestamp arguments are provided and there is no overlap between them, the `.list` method will return nothing.

### Wildcard Operator Arguments

The wildcard operator is the asterisk: *

You can use the wildcard operator * to `.list` records whose exact metadata you don't remember—or if you wish to `.list` records for a group of files that share similar metadata.

For `file_names` and `symbolic_directory_paths` a wildcard may be used as either prefix or suffix:

- Example * as a prefix: `*report.txt`
- Example * as a suffix: `/home/files/studies*`

Note that you don't necessarily have to attach full words to the wildcard operator *. The two above examples could thus instead be:

- Example * as a prefix: `*ort.txt`
- Example * as a suffix: `/home/files/studi*`

For `file_tags` a wildcard may be used for as the value in a key-value pair dictionary. This will return all records with the corresponding key.

- Example * in file_tags: `{"invoice_type": "*"}`

Let's dig into `.list` method examples for each of these. First a prefix wildcard in `file_names`:


```python
# list process records using a wildcard prefix in file_names
list_output = pipeline.list(file_names=["*e.txt"])

# nicely print the output of this .list
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "341c4e07-62a6-47f0-904b-7ff2ee3bbaef",
      "message": "No files were found for the given query arguments",
      "warnings": [
        {
          "WARNING: the following arguments returned zero results": [
            {
              "file_names": [
                "some*"
              ]
            }
          ]
        }
      ],
      "items": []
    }


The above will return records for every file whose `file_name` ends with "e.txt".

Now a suffix wildcard in `symbolic_directory_paths`:


```python
# list process records using wildcard suffix in symbolic_directory_paths
list_output = pipeline.list(symbolic_directory_paths=["/my/*"])

# nicely print the output of this .list
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "b6d53064-2748-4c3a-ac7a-e0325cf8c58f",
      "message": "No files were found for the given query arguments",
      "warnings": [
        {
          "WARNING: the following arguments returned zero results": [
            {
              "symbolic_directory_paths": [
                "/my/*"
              ]
            }
          ]
        }
      ],
      "items": []
    }


The above will return records for every file whose `symbolic_directory_path` begins with "/my/".

Now a wildcard operator in `file_tags`:


```python
# list process records using the wildcard operator in file_tags
list_output = pipeline.list(file_tags=[{"author": "*"}])

# nicely print the output of this .list
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "de17823f-5601-4143-b2ae-c546c173cdc7",
      "message": "No files were found for the given query arguments",
      "warnings": [
        {
          "WARNING: the following arguments returned zero results": [
            {
              "file_tags_keys": [
                "author"
              ]
            }
          ]
        }
      ],
      "items": []
    }


The above will return records for every file that has a file_tag whose key is "author", regardless of the value.

You can also use the wildcard operator with the [`.show_tree`](show_tree_method.md) method, the [`.semantic_search`](../search_methods/semantic_search_method.md) method, and the [`.keyword_search`](../search_methods/keyword_search_method.md) method.

### The Global Root

As you might have surmised, there is one very special use of the wildcard operator on `symbolic_directory_path`s: we call it "the global root". It's leveraged by placing a wildcard operator * right after the root slash, and having nothing else, as follows:

```python
# example line of code with the global root
symbolic_directory_paths=['/*']
```

Listing the global root returns records for every single file in your pipeline.

### Using Multiple Arguments with the `.list` method

As earlier mentioned, you can jointly use multiple input arguments with the `.list` method. Multiple inputs are combined in a logical **OR** (if they are metadata arguments) or **AND** (if they are timestamp bookends) to retrieve records satisfying what's been requested.

As an example, let's combine a timestamp bookend, a `symbolic_file_path`, and `file_tags` in one `.list` method invocation:


```python
# list process records using a combination of input args
list_output = pipeline.list(created_at_end=XXXX,
                                symbolic_file_path="/novels/gothic/Pride and Prejudice.txt",
                                file_tags=[({"author":"Alcott"})])

# nicely print the output of this .list
print(json.dumps(list_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "091a2b5e-4d2f-44cd-9fcf-65a0c80546b7",
      "message": "No files were found for the given query arguments",
      "warnings": [
        {
          "WARNING: the following arguments returned zero results": [
            {
              "symbolic_directory_paths": [
                "/my/*"
              ]
            },
            {
              "file_names": [
                "some*"
              ]
            }
          ]
        }
      ],
      "items": []
    }


Although <u>Pride and Prejudice</u> and <u>Little Women</u> are respectively covered by the `symbolic_file_paths` and `file_tags` arguments, neither of them falls within the indicated timestamp window. Consequently, they are both excluded from the above result.

### Output Size Cap

The current size limit on output generated by the `.list` method is 5MB.


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
