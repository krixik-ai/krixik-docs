# Keyword searchable transcription pipeline

This document details a modular pipeline that takes in an audio/video file, transcribes it, and makes the result keyword searchable.

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [processing a file](#processing-a-file)
- [performing keyword search](#performing-keyword-search)

## Pipeline setup

Below we setup a multi module pipeline to serve our intended purpose, which is to build a pipeline that will transcribe any audio/video and make it semantically searchable in any language.

To do this we will use the following modules:

- [`transcribe`](modules/transcribe.md): takes in audio/video input, outputs json of content transcription
- [`json-to-txt`](modules/json-to-txt.md): takes in json of text snippets, merges into text file
- [`keyword-db`](modules/keyword-db.md): takes in a text file and parses it for non-trivial keywords and their lemmatized stems, returning a searchable database file


We do this by passing the module names to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a multi-module pipeline
pipeline = krixik.create_pipeline(name="examples-transcribe-keyword-docs",
                                  module_chain=["transcribe",
                                                "json-to-txt",
                                                "keyword-db"])
```

This pipeline's available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).

## Processing a file

We first define a path to a local input file.

Lets take a quick look at this file before processing.


```python
# examine contents of input file
test_file = "../../../data/input/Interesting Facts About Colombia.mp4"
from IPython.display import Video
Video(test_file)
```




<video src="../../../data/input/Interesting Facts About Colombia.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



For this run we will use the default models for the each module of the pipeline.


```python
# test file
test_file = "../../../data/input/Interesting Facts About Colombia.mp4"

# process test input
process_output = pipeline.process(local_file_path = test_file,
                                  expire_time=60*10,
                                  verbose=False,
                                  local_save_directory="../../../data/output")
```

The output of this process is printed below.  Because the output of this particular pipeline is a database file, the process output is shown as null in the output.  The local address of the output file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
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


## Performing keyword search

Because our pipeline has the `keyword-db` module we can use the [keyword_search method](system/keyword_search.md) and search the transcription.


```python
# semantically search translated transcription
search_output = pipeline.keyword_search(query="lets talk about the country of Colombia", 
                                         file_ids=[process_output["file_id"]])

print(json.dumps(search_output, indent=2))
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

