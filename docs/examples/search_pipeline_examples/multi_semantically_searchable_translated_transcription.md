## Multi-Module Pipeline: Semantically-Searchable Translated Transcription

This document details a modular pipeline that takes in an audio/video file, [`transcribes`](../modules/ai_model_modules/transcribe_module.md) it, [`translates`](../modules/ai_model_modules/translate_module.md) the transcription into a desired language, and makes the result [`semantically searchable`](../system/search_methods/semantic_search_method.md).

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)
- [Performing Semantic Search](#performing-semantic-search)

### Pipeline Setup

To achieve what we've described above, let's set up a pipeline sequentially consisting of the following modules:

- A [`transcribe`](../modules/ai_model_modules/transcribe_module.md) module.

- A [`translate`](../modules/ai_model_modules/translate_module.md) module.

- A [`json-to-txt`](../modules/support_function_modules/json-to-txt_module.md) module.

- A [`parser`](../modules/ai_model_modules/parser_module.md) module.

- A [`text-embedder`](../modules/ai_model_modules/text-embedder_module.md) module.

- A [`vector-db`](../modules/database_modules/vector-db_module.md) module.

We use the [`json-to-txt`](../modules/support_function_modules/json-to-txt_module.md) and [`parser`](../modules/ai_model_modules/parser_module.md) combination, which combines the transcribed snippets into one document and then splices it again, to make sure that any pauses in speech don't make for partial snippets that can confuse the [`text-embedder`](../modules/ai_model_modules/text-embedder_module.md) model.

Pipeline setup is accomplished through the [`.create_pipeline`](../system/pipeline_creation/create_pipeline.md) method, as follows:


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
Video("../../../data/input/deadlift.mp4")
```




<video src="../../../data/input/Interesting Facts About Colombia.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



Since the input text is in Spanish, we'll use the (non-default) [`opus-mt-es-en`](https://huggingface.co/Helsinki-NLP/opus-mt-es-en) model of the [`translate`](../modules/ai_model_modules/translate_module.md) module to translate it into English.

We will use the default models for every other module in the pipeline, so they don't have to be specified in the [`modules`](../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file through the pipeline, as described above

process_output_1 = pipeline_1.process(local_file_path = "../../../data/input/deadlift.mp4", # the initial local filepath where the input file is stored
                                      local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                      expire_time=60*30, # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True, # wait for process to complete before returning IDE control to user
                                      verbose=False, # do not display process update printouts upon running code
                                      modules={"translate": {"model": "opus-mt-es-en"}}) # specify a non-default model for use in the translate module
```

    INFO: Checking that file size falls within acceptable parameters...
    INFO:...success!
    converted ../../../data/input/Interesting Facts About Colombia.mp4 to: /var/folders/k9/0vtmhf0s5h56gt15mkf07b1r0000gn/T/tmpvnfz4nvg/krixik_converted_version_Interesting Facts About Colombia.mp3
    INFO: hydrated input modules: {'module_1': {'model': 'whisper-tiny', 'params': {}}, 'module_2': {'model': 'opus-mt-en-es', 'params': {}}, 'module_3': {'model': 'base', 'params': {}}, 'module_4': {'model': 'sentence', 'params': {}}, 'module_5': {'model': 'all-MiniLM-L6-v2', 'params': {'quantize': True}}, 'module_6': {'model': 'faiss', 'params': {}}}
    INFO: symbolic_directory_path was not set by user - setting to default of /etc
    INFO: file_name was not set by user - setting to random file name: krixik_generated_file_name_qfgbnrugsa.mp3
    INFO: wait_for_process is set to True.
    INFO: file will expire and be removed from you account in 600 seconds, at Mon May  6 12:23:47 2024 UTC
    INFO: examples-transcribe-semantic-multilingual-docs file process and input processing started...
    INFO: metadata can be updated using the .update api.
    INFO: This process's request_id is: 8842c45c-bce2-3d52-8426-f26c872ed546
    INFO: File process and processing status:
    SUCCESS: module 1 (of 6) - transcribe processing complete.
    SUCCESS: module 2 (of 6) - translate processing complete.
    SUCCESS: module 3 (of 6) - json-to-txt processing complete.
    SUCCESS: module 4 (of 6) - parser processing complete.
    SUCCESS: module 5 (of 6) - text-embedder processing complete.
    SUCCESS: module 6 (of 6) - vector-db processing complete.
    SUCCESS: pipeline process complete.
    SUCCESS: process output downloaded


The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a [FAISS](https://github.com/facebookresearch/faiss) database file, `process_output` is "null". However, the output file has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process

print(json.dumps(process_output_1, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "examples-transcribe-semantic-multilingual-docs",
      "request_id": "f8ed48c3-b318-48f0-961f-0b9e4cc34b1c",
      "file_id": "600b873e-1bef-471a-a5e9-ae675c0514bc",
      "message": "SUCCESS - output fetched for file_id 600b873e-1bef-471a-a5e9-ae675c0514bc.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "/Users/jeremywatt/Desktop/krixik/code/krixik-docs/docs/examples/transcribe/600b873e-1bef-471a-a5e9-ae675c0514bc.faiss"
      ]
    }


### Performing Semantic Search

Krixik's [`.semantic_search`](../system/search_methods/semantic_search_method.md) method enables semantic search on documents processed through certain pipelines. Given that the [`.semantic_search`](../system/search_methods/semantic_search_method.md) method both [embeds](../modules/ai_model_modules/text-embedder_module.md) the query and performs the search, it can only be used with pipelines containing both a [`text-embedder`](../modules/ai_model_modules/text-embedder_module.md) module and a [`vector-db`](../modules/database_modules/vector-db_module.md) module in immediate succession.

Since our pipeline satisfies this condition, it has access to the [`.semantic_search`](../system/search_methods/semantic_search_method.md) method. Let's use it to query our text with natural language, as shown below:


```python
# perform semantic_search over the file in the pipeline

semantic_output_1 = pipeline_1.semantic_search(query="really basic facts", 
                                               file_ids=[process_output_1["file_id"]])

# nicely print the output of this process

print(json.dumps(semantic_output_1, indent=2))
```

    {
      "status_code": 200,
      "request_id": "b9452617-37da-47c6-aac4-70c82074e94d",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "600b873e-1bef-471a-a5e9-ae675c0514bc",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_qfgbnrugsa.mp3",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 39,
            "created_at": "2024-05-06 19:13:50",
            "last_updated": "2024-05-06 19:13:50"
          },
          "search_results": [
            {
              "snippet": "Miramos algunos hechos realmente bsicos.",
              "line_numbers": [
                1
              ],
              "distance": 0.058
            },
            {
              "snippet": "Bienvenidos de nuevo a los hechos F2D.",
              "line_numbers": [
                1
              ],
              "distance": 0.2
            },
            {
              "snippet": "Pero comencemos.",
              "line_numbers": [
                1
              ],
              "distance": 0.23
            },
            {
              "snippet": "S. Entonces me estoy pagando por esto.",
              "line_numbers": [
                1
              ],
              "distance": 0.242
            },
            {
              "snippet": "Lo que me recuerda chicos, esto es parte de nuestra lista de Columbia.",
              "line_numbers": [
                1
              ],
              "distance": 0.244
            }
          ]
        }
      ]
    }

