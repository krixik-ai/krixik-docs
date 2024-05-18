## Multi-Module Pipeline: Keyword-Searchable Transcription

This document details a modular pipeline that takes in an audio/video file, [`transcribes`](../modules/ai_model_modules/transcribe_module.md) it, and makes the result [`keyword searchable`](../system/search_methods/keyword_search_method.md).

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)
- [Performing Keyword Search](#performing-keyword-search)

### Pipeline Setup

To achieve what we've described above, let's set up a pipeline sequentially consisting of the following modules:

- A [`transcribe`](../modules/ai_model_modules/transcribe_module.md) module.

- A [`json-to-txt`](../modules/support_function_modules/json-to-txt_module.md) module.

- A [`keyword-db`](../modules/database_modules/keyword-db_module.md) module.

We do this by leveraging the [`.create_pipeline`](../system/pipeline_creation/create_pipeline.md) method, as follows:


```python
# create a pipeline as detailed above

pipeline_1 = krixik.create_pipeline(name="multi_keyword_searchable_transcription",
                                    module_chain=["transcribe",
                                                  "json-to-txt",
                                                  "keyword-db"])
```

### Processing an Input File

Lets take a quick look at a test file before processing.


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

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is an `SQLlite` database file, the `process_output` is "null". However, the output file has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process

print(json.dumps(process_output_1, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "examples-transcribe-keyword-docs",
      "request_id": "52f90a19-b379-445a-8fbf-6cf2426c457c",
      "file_id": "10666b2d-95f6-4551-b991-2de89f641d32",
      "message": "SUCCESS - output fetched for file_id 10666b2d-95f6-4551-b991-2de89f641d32.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/10666b2d-95f6-4551-b991-2de89f641d32.db"
      ]
    }


### Performing Keyword Search

Krixik's [`.keyword_search`](../system/search_methods/keyword_search_method.md) method enables keyword search on documents processed through pipelines that end with the [`keyword-db`](../modules/database_modules/keyword-db_module.md) module.

Since our pipeline satisfies this condition, it has access to the [`.keyword_search`](../system/search_methods/keyword_search_method.md) method. Let's use it to query our text for a few keywords, as below:


```python
# perform keyword search over the file in the pipeline

keyword_output_1 = pipeline_1.keyword_search(query="lets talk about the country of Colombia", 
                                             file_ids=[process_output_1["file_id"]])

# nicely print the output of this process

print(json.dumps(keyword_output_1, indent=2))
```

    {
      "status_code": 200,
      "request_id": "4461da6c-2ad3-4a09-99dd-68e972bcd079",
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
          "file_id": "10666b2d-95f6-4551-b991-2de89f641d32",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_ydfcgrxmkj.mp3",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_lines": 1,
            "created_at": "2024-05-07 17:57:06",
            "last_updated": "2024-05-07 17:57:06"
          },
          "search_results": [
            {
              "keyword": "country",
              "line_number": 1,
              "keyword_number": 8
            },
            {
              "keyword": "talk",
              "line_number": 1,
              "keyword_number": 121
            },
            {
              "keyword": "countries",
              "line_number": 1,
              "keyword_number": 142
            },
            {
              "keyword": "let",
              "line_number": 1,
              "keyword_number": 161
            },
            {
              "keyword": "talk",
              "line_number": 1,
              "keyword_number": 194
            },
            {
              "keyword": "country",
              "line_number": 1,
              "keyword_number": 319
            },
            {
              "keyword": "countries",
              "line_number": 1,
              "keyword_number": 349
            },
            {
              "keyword": "country",
              "line_number": 1,
              "keyword_number": 360
            },
            {
              "keyword": "country",
              "line_number": 1,
              "keyword_number": 472
            }
          ]
        }
      ]
    }

