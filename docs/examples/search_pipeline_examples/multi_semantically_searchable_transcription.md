## Multi-Module Pipeline: Semantically-Searchable Transcription

This document details a modular pipeline that takes in an audio/video file, [`transcribes`](../modules/ai_model_modules/transcribe_module.md) it, and makes the result [`semantically searchable`](../system/search_methods/semantic_search_method.md).

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)
- [Performing Semantic Search](#performing-semantic-search)

### Pipeline Setup

To achieve what we've described above, let's set up a pipeline sequentially consisting of the following modules:

- A [`transcribe`](../modules/ai_model_modules/transcribe_module.md) module.

- A [`json-to-txt`](../modules/support_function_modules/json-to-txt_module.md) module.

- A [`parser`](../modules/ai_model_modules/parser_module.md) module.

- A [`text-embedder`](../modules/ai_model_modules/text-embedder_module.md) module.

- A [`vector-db`](../modules/database_modules/vector-db_module.md) module.

We use the [`json-to-txt`](../modules/support_function_modules/json-to-txt_module.md) and [`parser`](../modules/ai_model_modules/parser_module.md) combination, which combines the transcribed snippets into one document and then splices it again, to make sure that any pauses in speech don't make for partial snippets that can confuse the [`text-embedder`](../modules/ai_model_modules/text-embedder_module.md) model.

Pipeline setup is accomplished through the [`.create_pipeline`](../system/pipeline_creation/create_pipeline.md) method, as follows:


```python
# create a pipeline as detailed above

pipeline_1 = krixik.create_pipeline(name="multi_semantically_searchable_transcription",
                                    module_chain=["transcribe",
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
    converted ../../input_data/Interesting Facts About Colombia.mp4 to: /var/folders/k9/0vtmhf0s5h56gt15mkf07b1r0000gn/T/tmpb5m88eea/krixik_converted_version_Interesting Facts About Colombia.mp3
    INFO: hydrated input modules: {'transcribe': {'model': 'whisper-tiny', 'params': {}}, 'json-to-txt': {'model': 'base', 'params': {}}, 'parser': {'model': 'sentence', 'params': {}}, 'text-embedder': {'model': 'multi-qa-MiniLM-L6-cos-v1', 'params': {'quantize': True}}, 'vector-db': {'model': 'faiss', 'params': {}}}
    INFO: symbolic_directory_path was not set by user - setting to default of /etc
    INFO: file_name was not set by user - setting to random file name: krixik_generated_file_name_tnzlfqdsly.mp3
    INFO: wait_for_process is set to True.
    INFO: file will expire and be removed from you account in 300 seconds, at Mon Apr 29 16:02:50 2024 UTC
    INFO: transcribe-semantic-pipeline file process and input processing started...
    INFO: metadata can be updated using the .update api.
    INFO: This process's request_id is: e04aa020-3d5c-5391-531e-23c222c820cd
    INFO: File process and processing status:
    SUCCESS: module 1 (of 5) - transcribe processing complete.
    SUCCESS: module 2 (of 5) - json-to-txt processing complete.
    SUCCESS: module 3 (of 5) - parser processing complete.
    SUCCESS: module 4 (of 5) - text-embedder processing complete.
    SUCCESS: module 5 (of 5) - vector-db processing complete.
    SUCCESS: pipeline process complete.
    SUCCESS: process output downloaded


The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a [`FAISS`](https://github.com/facebookresearch/faiss) database file, the process output is null. However, the output file has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process

print(json.dumps(process_output_1, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "transcribe-semantic-pipeline",
      "request_id": "37608ba0-db6e-44ef-b93e-7196616b3331",
      "file_id": "e0024f60-9192-4e05-8bb3-a0a0423305ab",
      "message": "SUCCESS - output fetched for file_id e0024f60-9192-4e05-8bb3-a0a0423305ab.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "/Users/jeremywatt/Desktop/krixik-cli/docs/examples/transcribe/e0024f60-9192-4e05-8bb3-a0a0423305ab.faiss"
      ]
    }


### Performing Semantic Search

Krixik's [`.semantic_search`](../system/search_methods/semantic_search_method.md) method enables semantic search on documents [processed](../system/parameters_processing_files_through_pipelines/process_method.md) through certain pipelines. Given that the [`.semantic_search`](../system/search_methods/semantic_search_method.md) method both [embeds](../modules/ai_model_modules/text-embedder_module.md) the query and performs the search, it can only be used with pipelines containing both a [`text-embedder`](../modules/ai_model_modules/text-embedder_module.md) module and a [`vector-db`](../modules/database_modules/vector-db_module.md) module in immediate succession.

Since our pipeline satisfies this condition, it has access to the [`.semantic_search`](../system/search_methods/semantic_search_method.md) method. Let's use it to query our text with natural language, as shown below:


```python
# perform semantic_search over the file in the pipeline

semantic_output_1 = pipeline_1.semantic_search(query="Let's talk about the country of Colombia", 
                                               file_ids=["XXXXX"])

# nicely print the output of this process

print(json.dumps(semantic_output_1, indent=2))
```

    {
      "status_code": 200,
      "request_id": "d88bf437-a742-41c1-8b28-5981d5c44bcc",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "e0024f60-9192-4e05-8bb3-a0a0423305ab",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_tnzlfqdsly.mp3",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 41,
            "created_at": "2024-04-29 22:57:52",
            "last_updated": "2024-04-29 22:57:52"
          },
          "search_results": [
            {
              "snippet": "Learn about Columbia.",
              "line_numbers": [
                1
              ],
              "distance": 0.263
            },
            {
              "snippet": "And I know coffee is really important when it comes to talking about Columbia, but you guys really don't know how important it is with its culture.",
              "line_numbers": [
                1
              ],
              "distance": 0.287
            },
            {
              "snippet": "You Columbia coffee right here.",
              "line_numbers": [
                1
              ],
              "distance": 0.292
            },
            {
              "snippet": "Now interesting enough when it comes to the coffee in Columbia, believe it or not, it is not actually native to the country.",
              "line_numbers": [
                1
              ],
              "distance": 0.298
            },
            {
              "snippet": "So we all know Columbia is famous for its coffee, right?",
              "line_numbers": [
                1
              ],
              "distance": 0.306
            }
          ]
        }
      ]
    }

