<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/single_module_pipelines/single_parser.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Single-Module Pipeline: `parser`

This document is a walkthrough of how to assemble and use a single-module pipeline that only includes a [`parser`](../../modules/support_function_modules/parser_module.md) module. It's divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Required Input Format](#required-input-format)
- [Using the Default Model](#using-the-default-model)
- [Using a Non-Default Model](#using-a-non-default-model)

### Pipeline Setup

Let's first instantiate a single-module [`parser`](../../modules/support_function_modules/parser_module.md) pipeline.

We use the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method for this, passing only the [`parser`](../../modules/support_function_modules/parser_module.md) module name into `module_chain`.


```python
# create a pipeline with a single parser module
pipeline = krixik.create_pipeline(name="single_parser_1", module_chain=["parser"])
```

### Required Input Format

The [`parser`](../../modules/support_function_modules/parser_module.md) module accepts document inputs. Acceptable file formats are TXT, PDF, DOCX, and PPTX, although the last three formats are automatically converted to TXT before processing.

Let's take a quick look at a valid input file, and then process it:


```python
# examine contents of a valid test input file
with open(data_dir + "input/1984_very_short.txt", "r") as file:
    print(file.read())
```

    It was a bright cold day in April, and the clocks were striking thirteen.
    Winston Smith, his chin nuzzled into his breast in an effort to escape the
    vile wind, slipped quickly through the glass doors of Victory Mansions,
    though not quickly enough to prevent a swirl of gritty dust from entering
    along with him.


### Using the Default Model

Let's process our test input file using the [`parser`](../../modules/support_function_modules/parser_module.md) module's [default model](../../modules/support_function_modules/parser_module.md#available-models-in-the-parser-module): [`sentence`](https://www.nltk.org/api/nltk.tokenize.html).

Given that this is the default model, we need not specify model selection through the optional [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file with the default model
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_very_short.txt",  # the initial local filepath where the input file is stored
    local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # wait for process to complete before returning IDE control to user
    verbose=False,
)  # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a JSON file, the process output is provided in this object as well (this is only the case for JSON outputs).  Moreover, the output file itself has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_parser_1",
      "request_id": "07569a36-93d8-47bb-b487-bba25ccc1348",
      "file_id": "60542629-7470-476f-b94e-40e2c53608bf",
      "message": "SUCCESS - output fetched for file_id 60542629-7470-476f-b94e-40e2c53608bf.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
          "line_numbers": [
            1
          ]
        },
        {
          "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
          "line_numbers": [
            2,
            3,
            4,
            5
          ]
        }
      ],
      "process_output_files": [
        "../../../data/output/60542629-7470-476f-b94e-40e2c53608bf.json"
      ]
    }


We can see from `process_output` that our two-sentence paragraph input has been separated correctly. Each sentence is also accompanied by its corresponding line number(s).

To confirm that everything went as it should have, let's load in the text file output from `process_output_files`:


```python
# load in process output from file
with open(process_output["process_output_files"][0]) as f:
    print(json.dumps(json.load(f), indent=2))
```

    [
      {
        "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
        "line_numbers": [
          1
        ]
      },
      {
        "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
        "line_numbers": [
          2,
          3,
          4,
          5
        ]
      }
    ]


### Using a Non-Default Model

To use a [non-default model](../../modules/support_function_modules/parser_module.md#available-models-in-the-parser-module) like `fixed`, we must enter it explicitly through the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument when invoking the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method. Note that if you don't explicitly define parameters for the `fixed` model (for it is parameterizable) default values will be used instead.


```python
# process the file with a non-default model
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_very_short.txt",  # all parameters save 'modules' as above
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,
    wait_for_process=True,
    verbose=False,
    modules={"parser": {"model": "fixed", "params": {"chunk_size": 9, "overlap_size": 3}}},
)  # specify a non-default model for this process as well as its parameters
```

We can view the newly parsed text by loading in the output file, as below.

Examining the output we can see that our input document was not cut into complete sentences, but instead into chunks of text as specified.  Each chunk is nine words in length, and the consecutive chunks overlap by three words. The parameterized model has worked as instructed.


```python
# load in process output from file
with open(process_output["process_output_files"][0]) as f:
    print(json.dumps(json.load(f), indent=2))
```

    [
      {
        "snippet": "It was a bright cold day in April, and",
        "line_numbers": [
          1
        ]
      },
      {
        "snippet": "in April, and the clocks were striking thirteen. Winston",
        "line_numbers": [
          1,
          2
        ]
      },
      {
        "snippet": "striking thirteen. Winston Smith, his chin nuzzled into his",
        "line_numbers": [
          1,
          2
        ]
      },
      {
        "snippet": "nuzzled into his breast in an effort to escape",
        "line_numbers": [
          2
        ]
      },
      {
        "snippet": "effort to escape the vile wind, slipped quickly through",
        "line_numbers": [
          2,
          3
        ]
      },
      {
        "snippet": "slipped quickly through the glass doors of Victory Mansions,",
        "line_numbers": [
          3
        ]
      },
      {
        "snippet": "of Victory Mansions, though not quickly enough to prevent",
        "line_numbers": [
          3,
          4
        ]
      },
      {
        "snippet": "enough to prevent a swirl of gritty dust from",
        "line_numbers": [
          4
        ]
      },
      {
        "snippet": "gritty dust from entering along with him.",
        "line_numbers": [
          4,
          5
        ]
      }
    ]

