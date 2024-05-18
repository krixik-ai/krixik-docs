## Multi-Module Pipeline: Semantically-Searchable OCR

This document details a modular pipeline that takes in an image, [`extracts all text`](../modules/ai_model_modules/ocr_module.md) found within it, and makes the extracted text [`semantically searchable`](../system/search_methods/semantic_search_method.md).

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)
- [Performing Semantic Search](#performing-semantic-search)

### Pipeline Setup

To achieve what we've described above, let's set up a pipeline sequentially consisting of the following modules:

- An [`ocr`](../modules/ai_model_modules/ocr_module.md) module.

- A [`json-to-txt`](../modules/support_function_modules/json-to-txt_module.md) module.

- A [`parser`](../modules/ai_model_modules/parser_module.md) module.

- A [`text-embedder`](../modules/ai_model_modules/text-embedder_module.md) module.

- A [`vector-db`](../modules/database_modules/vector-db_module.md)

We use the [`json-to-txt`](../modules/support_function_modules/json-to-txt_module.md) and [`parser`](../modules/ai_model_modules/parser_module.md) combination, which combines the transcribed snippets into one document and then splices it again, to make sure that any unsought OCR-generated breaks don't make for partial snippets that can confuse the [`text-embedder`](../modules/ai_model_modules/text-embedder_module.md) model.

Pipeline setup is accomplished through the [`.create_pipeline`](../system/pipeline_creation/create_pipeline.md) method, as follows:


```python
# create a pipeline as detailed above

pipeline_1 = krixik.create_pipeline(name="multi_semantically_searchable_ocr",
                                    module_chain=["ocr",
                                                  "json-to-txt",
                                                  "parser",
                                                  "text-embedder",
                                                  "vector-db"])
```

### Processing an Input File

Lets take a quick look at a test file before processing.


```python
# examine contents of a valid input file

from IPython.display import Image
Image(filename="../../../data/input/seal.png")
```




    
![png](multi_semantically_searchable_ocr_files/multi_semantically_searchable_ocr_4_0.png)
    



We will use the default models for every module in the pipeline, so the [`modules`](../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) method doesn't need to be leveraged.


```python
# process the file through the pipeline, as described above

process_output_1 = pipeline_1.process(local_file_path = "../../../data/input/seal.png", # the initial local filepath where the input file is stored
                                      local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                      expire_time=60*30, # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True, # wait for process to complete before returning IDE control to user
                                      verbose=False) # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a [FAISS](https://github.com/facebookresearch/faiss) database file, `process_output` is "null". However, the output file has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process

print(json.dumps(process_output_1, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "examples-caption-semantic-docs",
      "request_id": "f0bdacfd-c35b-40cb-95b1-7aaac772a5d1",
      "file_id": "793b02d7-2a33-4b6c-93be-c1e8619cfd4f",
      "message": "SUCCESS - output fetched for file_id 793b02d7-2a33-4b6c-93be-c1e8619cfd4f.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/793b02d7-2a33-4b6c-93be-c1e8619cfd4f.faiss"
      ]
    }


### Performing Semantic Search

Krixik's [`.semantic_search`](../system/search_methods/semantic_search_method.md) method enables semantic search on documents processed through certain pipelines. Given that the [`.semantic_search`](../system/search_methods/semantic_search_method.md) method both [embeds](../modules/ai_model_modules/text-embedder_module.md) the query and performs the search, it can only be used with pipelines containing both a [`text-embedder`](../modules/ai_model_modules/text-embedder_module.md) module and a [`vector-db`](../modules/database_modules/vector-db_module.md) module in immediate succession.

Since our pipeline satisfies this condition, it has access to the [`.semantic_search`](../system/search_methods/semantic_search_method.md) method. Let's use it to query our text with natural language, as shown below:


```python
# perform semantic_search over the file in the pipeline

semantic_output_1 = pipeline_1.semantic_search(query="The man sounds like he's dying.", 
                                               file_ids=[process_output_1["file_id"]])

print(json.dumps(semantic_output_1, indent=2))
```

    {
      "status_code": 200,
      "request_id": "a10ce58a-7c7c-4615-9a48-89a63d4fedfd",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "793b02d7-2a33-4b6c-93be-c1e8619cfd4f",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_cqdgdvvznx.png",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 1,
            "created_at": "2024-05-07 18:50:56",
            "last_updated": "2024-05-07 18:50:56"
          },
          "search_results": [
            {
              "snippet": "a large group of people are in a restaurant",
              "line_numbers": [
                1
              ],
              "distance": 0.386
            }
          ]
        }
      ]
    }

