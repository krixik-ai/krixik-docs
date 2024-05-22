## Multi-Module Pipeline: Semantically-Searchable Translated Transcription

This document details a modular pipeline that takes in an audio file, [`transcribes`](../../modules/ai_model_modules/transcribe_module.md) it, [`translates`](../../modules/ai_model_modules/translate_module.md) the transcription into a desired language, and makes the result [`semantically searchable`](../../system/search_methods/semantic_search_method.md).

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)
- [Performing Semantic Search](#performing-semantic-search)

### Pipeline Setup

To achieve what we've described above, let's set up a pipeline sequentially consisting of the following modules:

- A [`transcribe`](../../modules/ai_model_modules/transcribe_module.md) module.

- A [`translate`](../../modules/ai_model_modules/translate_module.md) module.

- A [`json-to-txt`](../../modules/support_function_modules/json-to-txt_module.md) module.

- A [`parser`](../../modules/ai_model_modules/parser_module.md) module.

- A [`text-embedder`](../../modules/ai_model_modules/text-embedder_module.md) module.

- A [`vector-db`](../../modules/database_modules/vector-db_module.md) module.

We use the [`json-to-txt`](../../modules/support_function_modules/json-to-txt_module.md) and [`parser`](../../modules/ai_model_modules/parser_module.md) combination, which combines the transcribed snippets into one document and then splices it again, to make sure that any pauses in speech don't make for partial snippets that can confuse the [`text-embedder`](../../modules/ai_model_modules/text-embedder_module.md) model.

Pipeline setup is accomplished through the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method, as follows:


```python
# create a pipeline as detailed above

pipeline_1 = krixik.create_pipeline(name="multi_semantically_searchable_translated_transcription",
                                    module_chain=["transcribe",
                                                  "translate",
                                                  "json-to-txt",
                                                  "parser",
                                                  "text-embedder",
                                                  "vector-db"])
```

### Processing an Input File

Lets take a quick look at a test file before processing.


```python
# examine contents of input file

from IPython.display import Video
Video("../../../data/input/deadlift.mp3")
```




<video src="../../../data/input/deadlift.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



Since the input text is in Spanish, we'll use the (non-default) [`opus-mt-es-en`](https://huggingface.co/Helsinki-NLP/opus-mt-es-en) model of the [`translate`](../../modules/ai_model_modules/translate_module.md) module to translate it into English.

We will use the default models for every other module in the pipeline, so they don't have to be specified in the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file through the pipeline, as described above

process_output_1 = pipeline_1.process(local_file_path = "../../../data/input/deadlift.mp3", # the initial local filepath where the input file is stored
                                      local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                      expire_time=60*30, # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True, # wait for process to complete before returning IDE control to user
                                      verbose=False, # do not display process update printouts upon running code
                                      modules={"translate": {"model": "opus-mt-es-en"}}) # specify a non-default model for use in the translate module
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a [FAISS](https://github.com/facebookresearch/faiss) database file, `process_output` is "null". However, the output file has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process

print(json.dumps(process_output_1, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "multi_semantically_searchable_translated_transcription",
      "request_id": "6b26a79b-b322-4c69-a3d4-77358545e045",
      "file_id": "611de878-2c15-4833-bfc3-69073125a3ad",
      "message": "SUCCESS - output fetched for file_id 611de878-2c15-4833-bfc3-69073125a3ad.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/611de878-2c15-4833-bfc3-69073125a3ad.faiss"
      ]
    }


### Performing Semantic Search

Krixik's [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method enables semantic search on documents processed through certain pipelines. Given that the [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method both [embeds](../../modules/ai_model_modules/text-embedder_module.md) the query and performs the search, it can only be used with pipelines containing both a [`text-embedder`](../../modules/ai_model_modules/text-embedder_module.md) module and a [`vector-db`](../../modules/database_modules/vector-db_module.md) module in immediate succession.

Since our pipeline satisfies this condition, it has access to the [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method. Let's use it to query our text with natural language, as shown below:


```python
# perform semantic_search over the file in the pipeline

semantic_output_1 = pipeline_1.semantic_search(query="be sure to hold the weights very firmly", 
                                               file_ids=[process_output_1["file_id"]])

# nicely print the output of this process

print(json.dumps(semantic_output_1, indent=2))
```

    {
      "status_code": 200,
      "request_id": "4927d817-7d3b-4c96-8301-dd75a77ac045",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "611de878-2c15-4833-bfc3-69073125a3ad",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_bnzvpcikcl.mp3",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 8,
            "created_at": "2024-05-20 06:39:38",
            "last_updated": "2024-05-20 06:39:38"
          },
          "search_results": [
            {
              "snippet": "To make movement, we have to put the columns in front of the bar and start to move the Shoulders and the Shoulders together.",
              "line_numbers": [
                1
              ],
              "distance": 0.303
            },
            {
              "snippet": "During all movement, we want to see the bar close to the body, to move and down.",
              "line_numbers": [
                1
              ],
              "distance": 0.355
            },
            {
              "snippet": "When the bar goes to the knees, we have the correct angle of our trunk and we double the knees until the head is properly aligned to position the knee and rest.",
              "line_numbers": [
                1
              ],
              "distance": 0.357
            },
            {
              "snippet": "When the bar goes to the knees, we extend the knee.",
              "line_numbers": [
                1
              ],
              "distance": 0.374
            },
            {
              "snippet": "To begin, we want to see the feet in the anchors of the chair and the men, the columns in the ground, a neutral column, mediated by the abdomen, the men are going to go through there.",
              "line_numbers": [
                1
              ],
              "distance": 0.377
            }
          ]
        }
      ]
    }

