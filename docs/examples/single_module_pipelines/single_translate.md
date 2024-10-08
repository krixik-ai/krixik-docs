<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/single_module_pipelines/single_translate.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> <a href="https://youtu.be/h57nLSAEbho" target="_parent"><img src="https://badges.aleen42.com/src/youtube.svg" alt="Youtube"/></a>

## Single-Module Pipeline: `translate`
[🇨🇴 Versión en español de este documento](https://krixik-docs.readthedocs.io/es-main/ejemplos/ejemplos_pipelines_modulo_unico/unico_translate_traduccion/)

This document is a walkthrough of how to assemble and use a single-module pipeline that only includes a [`translate`](../../modules/ai_modules/translate_module.md) module. 

Machine translation involves using artificial intelligence to translate text from one human language to another. Its applications include facilitating global communication, enabling multilingual customer support, and enhancing access to information across linguistic barriers.

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Required Input Format](#required-input-format)
- [Using the Default Model](#using-the-default-model)
- [Using a Non-Default Model](#using-a-non-default-model)

### Pipeline Setup

Let's first instantiate a single-module [`translate`](../../modules/ai_modules/translate_module.md) pipeline.

We use the [`create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method for this, passing only the [`translate`](../../modules/ai_modules/translate_module.md) module name into `module_chain`.


```python
# create a pipeline with a single translate module
pipeline = krixik.create_pipeline(name="single_translate_1", module_chain=["translate"])
```

### Required Input Format

The [`translate`](../../modules/ai_modules/translate_module.md) module accepts JSON file input. The input JSON must respect [this format](../../system/parameters_processing_files_through_pipelines/JSON_input_format.md).

Let's take a quick look at a valid input file, and then process it.


```python
# examine contents of a valid input file
with open(data_dir + "input/valid.json", "r") as file:
    print(json.dumps(json.load(file), indent=2))
```

    [
      {
        "snippet": "I love this movie and i would watch it again and again!"
      },
      {
        "snippet": "Operating profit totaled EUR 9.4 mn, down from EUR 11.7 mn in 2004."
      }
    ]


### Using the Default Model

Let's process our test input file using the [`translate`](../../modules/ai_modules/translate_module.md) module's [default model](../../modules/ai_modules/translate_module.md#available-models-in-the-translate-module), which translates English into Spanish: [`opus-mt-en-es`](https://huggingface.co/Helsinki-NLP/opus-mt-en-es).

Given that this is the default model, we need not specify model selection through the optional [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file with the default model
process_output = pipeline.process(
    local_file_path=data_dir + "input/valid.json",  # the initial local filepath where the input file is stored
    local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # wait for process to complete before returning IDE control to user
    verbose=False,
)  # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a JSON file, the process output is provided in this object as well (this is only the case for JSON outputs).  Moreover, the output file itself has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_translate_1",
      "request_id": "6e87fa96-3fea-49f9-9ef3-897cc226f94c",
      "file_id": "a2439789-e57d-4cd1-a91e-ab1907edd2a5",
      "message": "SUCCESS - output fetched for file_id a2439789-e57d-4cd1-a91e-ab1907edd2a5.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "Me encanta esta pelcula y la vea una y otra vez!"
        },
        {
          "snippet": "El beneficio de explotacin ascendi a 9,4 millones EUR, frente a 11,7 millones EUR en 2004."
        }
      ],
      "process_output_files": [
        "../../../data/output/a2439789-e57d-4cd1-a91e-ab1907edd2a5.json"
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
        "snippet": "Me encanta esta pelcula y la vea una y otra vez!"
      },
      {
        "snippet": "El beneficio de explotacin ascendi a 9,4 millones EUR, frente a 11,7 millones EUR en 2004."
      }
    ]


As you can see, vowels with accent marks are missing from the translated text. This is a pecularity of the selected translating model; always be sure to familiarize yourself with any model's quirks before using it in production.

### Using a Non-Default Model

To use a [non-default model](../../modules/ai_modules/translate_module.md#available-models-in-the-translate-module) like Spanish-to-English [`opus-mt-es-en`](https://huggingface.co/Helsinki-NLP/opus-mt-es-en) you must enter it explicitly through the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument when invoking the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

We do so below to process the same input file as above.


```python
# process the file with a non-default model
process_output = pipeline.process(
    local_file_path=data_dir + "input/valid_spanish.json",  # all parameters save 'modules' as above
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,
    wait_for_process=True,
    verbose=False,
    modules={"translate": {"model": "opus-mt-es-en"}},
)  # specify a non-default model for this process
```

We once again print out and review the output as we did above.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_translate_1",
      "request_id": "d82d9ebc-b07f-428f-84c5-f3db8fef7975",
      "file_id": "2a070d10-a78a-4f76-b59a-6950d5585662",
      "message": "SUCCESS - output fetched for file_id 2a070d10-a78a-4f76-b59a-6950d5585662.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "I love this book and I've read it over and over again!"
        },
        {
          "snippet": "The production of the factory amounted to 9.4 million units, compared to 11.7 million units in 2004."
        }
      ],
      "process_output_files": [
        "../../../data/output/2a070d10-a78a-4f76-b59a-6950d5585662.json"
      ]
    }

