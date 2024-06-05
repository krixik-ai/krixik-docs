<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/search_pipeline_examples/multi_snippet_semantic_search.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Multi-Module Pipeline: Semantic Search on Snippets

This document details a modular pipeline that takes in a series of text snippets in a JSON file and enables [`semantic search`](../../system/search_methods/semantic_search_method.md) on them.

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)
- [Performing Semantic Search](#performing-semantic-search)

### Pipeline Setup

To achieve what we've described above, let's set up a pipeline sequentially consisting of the following modules:

- A [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) module.

- A [`vector-db`](../../modules/database_modules/vector-db_module.md) module.

We do this by leveraging the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method, as follows:


```python
# create a pipeline as detailed above
pipeline = krixik.create_pipeline(name="multi_snippets_semantic_search", module_chain=["text-embedder", "vector-db"])
```

### Processing an Input File

Lets take a quick look at a test file before processing.

The input format to this pipeline is a JSON file (given that it's the input format of its [first module](../../modules/ai_modules/text-embedder_module.md)). JSON input must always be in a [specific format](../../system/parameters_processing_files_through_pipelines/JSON_input_format.md), or the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method will not work.


```python
# examine contents of input file
with open(data_dir + "input/1984_snippets.json", "r") as file:
    print(file.read())
```

    [{"snippet": "It was a bright cold day in April, and the clocks were striking thirteen.", "line_numbers": [1]}, {"snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.", "line_numbers": [2, 3, 4, 5]}]


We will use the default models for every module in the pipeline, so the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method doesn't need to be leveraged.


```python
# process the file through the pipeline, as described above
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_snippets.json",  # the initial local filepath where the input file is stored
    local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # wait for process to complete before returning IDE control to user
    verbose=False,
)  # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a [FAISS](https://github.com/facebookresearch/faiss) database file, the process output is null. However, the output file has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "multi_snippets_semantic_search",
      "request_id": "df80b7bd-d593-4cdd-bc39-4d2bdd18788e",
      "file_id": "f52906bb-eca6-408c-a929-504ea8954e76",
      "message": "SUCCESS - output fetched for file_id f52906bb-eca6-408c-a929-504ea8954e76.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/f52906bb-eca6-408c-a929-504ea8954e76.faiss"
      ]
    }


### Performing Semantic Search

Krixik's [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method enables semantic search on documents processed through certain pipelines. Given that the [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method both [embeds](../../modules/ai_modules/text-embedder_module.md) the query and performs the search, it can only be used with pipelines containing both a [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) module and a [`vector-db`](../../modules/database_modules/vector-db_module.md) module in immediate succession.

Since our pipeline satisfies this condition, it has access to the [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method. Let's use it to query our text with natural language, as shown below:


```python
# perform semantic_search over the file in the pipeline
semantic_output = pipeline.semantic_search(query="it was cold night", file_ids=[process_output["file_id"]])

# nicely print the output of this process
print(json.dumps(semantic_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "4df32bdf-bb82-44d4-8151-ffaf2fc99c18",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "f52906bb-eca6-408c-a929-504ea8954e76",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_xongatwbce.json",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 2,
            "created_at": "2024-06-05 15:31:41",
            "last_updated": "2024-06-05 15:31:41"
          },
          "search_results": [
            {
              "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
              "line_numbers": [
                1
              ],
              "distance": 0.236
            },
            {
              "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
              "line_numbers": [
                2,
                3,
                4,
                5
              ],
              "distance": 0.429
            }
          ]
        }
      ]
    }

