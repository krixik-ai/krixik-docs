<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/search_pipeline_examples/multi_keyword_searchable_image_captions.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

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

Image(filename=data_dir + "input/restaurant.png")
```




    
![png](multi_keyword_searchable_image_captions_files/multi_keyword_searchable_image_captions_5_0.png)
    



We will use the default models for every module in the pipeline, so the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method doesn't need to be leveraged.


```python
# process the file through the pipeline, as described above
process_output = pipeline.process(
    local_file_path=data_dir + "input/restaurant.png",  # the initial local filepath where the input file is stored
    local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
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
      "request_id": "a5d38d01-9ff0-492e-abeb-6e1e14ec9ee6",
      "file_id": "913dce6e-2fbe-4d5a-bbd2-84c6a0a73932",
      "message": "SUCCESS - output fetched for file_id 913dce6e-2fbe-4d5a-bbd2-84c6a0a73932.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/913dce6e-2fbe-4d5a-bbd2-84c6a0a73932.db"
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
      "request_id": "1804483a-1551-47f4-b1f1-193afa1e8796",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "913dce6e-2fbe-4d5a-bbd2-84c6a0a73932",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_kbcievmqlb.png",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_lines": 1,
            "created_at": "2024-06-05 14:50:59",
            "last_updated": "2024-06-05 14:50:59"
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

