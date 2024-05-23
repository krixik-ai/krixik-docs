## Single-Module Pipeline: `caption`

This document is a walkthrough of how to assemble and use a single-module pipeline that only includes a [`caption`](../../modules/ai_modules/caption_module.md) module. It's divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Required Input Format](#required-input-format)
- [Using the Default Model](#using-the-default-model)
- [Using a Non-Default Model](#using-a-non-default-model)

### Pipeline Setup

Let's first instantiate a single-module [`caption`](../../modules/ai_modules/caption_module.md) pipeline.

We use the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method for this, passing only the [`caption`](../../modules/ai_modules/caption_module.md) module name into `module_chain`.


```python
# create a pipeline with a single caption module
pipeline = krixik.create_pipeline(name="single_caption_1",
                                  module_chain=["caption"])
```

### Required Input Format

The [`caption`](../../modules/ai_modules/caption_module.md) module accepts `.png`, `.jpg`, and `.jpeg` images as [input](../../modules/ai_modules/caption_module.md#inputs-and-outputs-of-the-caption-module).

Let's take a quick look at a valid input file, and then process it.


```python
# examine the contents of a valid input file
from IPython.display import Image
Image(filename="../../../data/input/restaurant.png")
```




    
![png](single_caption_files/single_caption_5_0.png)
    



### Using the Default Model

Let's process our test input file using the [`caption`](../../modules/ai_modules/caption_module.md) module's [default model](../../modules/ai_modules/caption_module.md#available-models-in-the-caption-module): [`vit-gpt2-image-captioning`](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning).

Given that this is the default model, we need not specify model selection through the optional [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file with the default model
process_output = pipeline.process(local_file_path="../../../data/input/restaurant.png", # the initial local filepath where the input file is stored
                                  local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                  expire_time=60 * 30, # process data will be deleted from the Krixik system in 30 minutes
                                  wait_for_process=True, # wait for process to complete before returning IDE control to user
                                  verbose=False) # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a JSON file, the process output is provided in this object as well (this is only the case for JSON outputs).  Moreover, the output file itself has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_caption_1",
      "request_id": "68dc3d6f-0761-46db-923c-92c5fff12170",
      "file_id": "843d9ded-89de-4b25-b275-f463cf966fdd",
      "message": "SUCCESS - output fetched for file_id 843d9ded-89de-4b25-b275-f463cf966fdd.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "caption": "a large group of people are in a restaurant"
        }
      ],
      "process_output_files": [
        "../../../data/output/843d9ded-89de-4b25-b275-f463cf966fdd.json"
      ]
    }


To confirm that everything went as it should have, let's load in the text file output from `process_output_files`:


```python
# load in process output from file
with open(process_output["process_output_files"][0]) as f:
    print(json.dumps(json.load(f), indent=2))
```

    [
      {
        "caption": "a large group of people are in a restaurant"
      }
    ]


### Using a Non-Default Model

To use a [non-default model](../../modules/ai_modules/caption_module.md#available-models-in-the-caption-module) like [`blip-image-captioning-base`](https://huggingface.co/Salesforce/blip-image-captioning-base), we must enter it explicitly through the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument when invoking the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file with a non-default model
process_output = pipeline.process(local_file_path="../../../data/input/restaurant.png", # the initial local filepath where the input file is stored
                                  local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                  expire_time=60 * 30, # process data will be deleted from the Krixik system in 30 minutes
                                  wait_for_process=True, # wait for process to complete before returning IDE control to user
                                  verbose=False, # do not display process update printouts upon running code
                                  modules={"caption": {"model": "blip-image-captioning-base"}}) # specify a non-default model for this process
```

The output of this process is printed below.

Because the output of this particular module-model pair is a JSON file, the process output is provided in this object as well (this is only the case for JSON outputs).  Moreover, the output file itself has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_caption_1",
      "request_id": "2c1ce8fd-77b4-4b83-91f9-0b2794b28272",
      "file_id": "aeecf5c5-54fd-425c-ab52-5e80dc584cff",
      "message": "SUCCESS - output fetched for file_id aeecf5c5-54fd-425c-ab52-5e80dc584cff.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "caption": "a group of people sitting around a bar"
        }
      ],
      "process_output_files": [
        "../../../data/output/aeecf5c5-54fd-425c-ab52-5e80dc584cff.json"
      ]
    }

