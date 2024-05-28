## Multi-Module Pipeline: Keyword-Searchable Image Captions

This document details a modular pipeline that takes in an image, generates a [`textual caption`](../../modules/ai_modules/caption_module.md) of it, and makes the caption [`keyword searchable`](../../system/search_methods/keyword_search_method.md).

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)
- [Performing Keyword Search](#performing-keyword-search)

### Pipeline Setup

To achieve what we've described above, let's set up a pipeline sequentially consisting of the following modules:

- A [`caption`](../../modules/ai_modules/caption_module.md) module.

- A [`json-to-txt`](../../modules/support_function_modules/json-to-txt_module.md) module.

- A [`keyword-db`](../../modules/database_modules/keyword-db_module.md) module.

We do this by leveraging the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method, as follows:


```python
# create a pipeline as detailed above
pipeline = krixik.create_pipeline(name="multi_keyword_searchable_image_captions", module_chain=["caption", "json-to-txt", "keyword-db"])
```

### Processing an Input File

Lets take a quick look at a test file before processing.


```python
# examine contents of input file
from IPython.display import Image

Image(filename="../../../data/input/restaurant.png")
```




    
![png](multi_keyword_searchable_image_captions_files/multi_keyword_searchable_image_captions_4_0.png)
    



We will use the default models for every module in the pipeline, so the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method doesn't need to be leveraged.


```python
# process the file through the pipeline, as described above
process_output = pipeline.process(
    local_file_path="../../../data/input/restaurant.png",  # the initial local filepath where the input file is stored
    local_save_directory="../../../data/output",  # the local directory that the output file will be saved to
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # wait for process to complete before returning IDE control to user
    verbose=False,
)  # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a `SQLlite` database file, `process_output` is "null". However, the output file has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "multi_keyword_searchable_image_captions",
      "request_id": "b1fce375-9801-4e16-8cbc-98d5f4123bde",
      "file_id": "e9f19151-8b81-4929-803e-846dac0cbc4c",
      "message": "SUCCESS - output fetched for file_id e9f19151-8b81-4929-803e-846dac0cbc4c.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/e9f19151-8b81-4929-803e-846dac0cbc4c.db"
      ]
    }


### Performing Keyword Search

Krixik's [`.keyword_search`](../../system/search_methods/keyword_search_method.md) method enables keyword search on documents processed through pipelines that end with the [`keyword-db`](../../modules/database_modules/keyword-db_module.md) module.

Since our pipeline satisfies this condition, it has access to the [`.keyword_search`](../../system/search_methods/keyword_search_method.md) method. Let's use it to query our text for a few keywords, as below:


```python
# perform keyword search over the file in the pipeline
keyword_output = pipeline.keyword_search(query="people bar sitting tables dinner drinks", file_ids=[process_output["file_id"]])

# nicely print the output of this process
print(json.dumps(keyword_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "c1e7ab7e-f2e3-4cfc-bbc7-484bc7a304c7",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "e9f19151-8b81-4929-803e-846dac0cbc4c",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_zrhxmayoad.png",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_lines": 1,
            "created_at": "2024-05-22 20:17:31",
            "last_updated": "2024-05-22 20:17:31"
          },
          "search_results": [
            {
              "keyword": "people",
              "line_number": 1,
              "keyword_number": 5
            }
          ]
        }
      ]
    }

