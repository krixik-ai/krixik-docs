## The parser module

This document reviews the `parser` module - which takes in input documents, cuts them up into pieces using different model logic, and returns the spliced input as json output. 

This document includes an overview of custom pipeline setup, current model set, parameters, and `.process` usage for this module.

To follow along with this demonstration be sure to initialize your krixik session with your api key and url as shown below. 

We illustrate loading these required secrets in via [python-dotenv](https://pypi.org/project/python-dotenv/), storing those secrets in a `.env` file.  This is always good practice for storing / loading secrets (e.g., doing so will reduce the chance you inadvertantly push secrets to a repo).

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [required input format](#required-input-format)
- [using the default model](#using-the-default-model)
- [using a non-default model](#using-a-non-default-model)

## Pipeline setup

Below we setup a simple one module pipeline using the `parser` module.  This parser takes in an input text file and splits into its constituent snippets.

We do this by passing the module name to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(name="modules-parser-docs", 
                                  module_chain=["parser"])
```

The `parser` module comes with two models that determine how it cuts up an input text:

- `sentence`: (default) splits a text into its individual sentences
- `fixed`: splits a text into potentially overlapping chunks of consecutive words

The `fixed` model takes in two parameters to determine how it operates:

- `chunk_size` (recommended default 10) chunk size length in number of consecutive words
- `overlap_size`: (recommended default 2) length of overlap in words between consecutive chunks

These available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).

## Required input format

The `keyword-db` module accepts `.txt`, `.pdf`, `.docx`, and `.pptx` file formats as input.  The latter three (`.pdf`, `.docx`, and `.pptx`) are first converted to `.txt` prior to processing.

Let's look at an example of a small valid input - and then process it.


```python
# examine contents of a valid test input file
test_file = "../../data/input/1984_very_short.txt"
with open(test_file, "r") as file:
    print(file.read())
```

    It was a bright cold day in April, and the clocks were striking thirteen.
    Winston Smith, his chin nuzzled into his breast in an effort to escape the
    vile wind, slipped quickly through the glass doors of Victory Mansions,
    though not quickly enough to prevent a swirl of gritty dust from entering
    along with him.


## Using the default model

Now let's process the input file above using the default model - `sentence`.  Because `sentence` is the default model we need not input the optional `modules` argument into `.process`.


```python
# define path to an input file from examples directory
test_file = "../../data/input/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path=test_file,
                                  local_save_directory="../../data/output", # save output repo data output subdir
                                  expire_time=60 * 10,    # set all process data to expire in 10 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is json, the process output is provided in the return response.  The output file itself has been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "modules-parser-docs",
      "request_id": "5908efbc-b06d-44f3-93c8-a46c29540637",
      "file_id": "575c69c6-0571-4f56-8e49-6c1e4f4a3f4a",
      "message": "SUCCESS - output fetched for file_id 575c69c6-0571-4f56-8e49-6c1e4f4a3f4a.Output saved to location(s) listed in process_output_files.",
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
        "../../data/output/575c69c6-0571-4f56-8e49-6c1e4f4a3f4a.json"
      ]
    }


Lets break down the output:

- `status_code`: provides the success / failure signal for the api
- `pipeline`: the name of the pipeline we ran `.process` on
- `request_id`: unique id associated with this execution of `.process`
- `file_id`: unique id for the processed file and its associated output
- `message`: message detailing success or failure of call
- `warnings`: message list indicating any warnings related to our call
- `process_output`: returned output (available when module-model output is json only)
- `process_output_files`: list of process output, local file names 

We can see from `process_output` that our two-sentence paragraph input has been separated correctly.  Each sentence also has its corresponding line number(s).

This process output is also stored in the file contained in `process_output_files`.  Lets load it in and confirm we have the same process output we see above.


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


## Using a non-default model

To use a non-default model like `fixed` we pass its name explicitly via the `modules` argument as follows.  This will implicitly pass the default parameter values for the `fixed` model.


```python
# define path to an input file from examples directory
test_file = "../../data/input/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path=test_file,
                                  local_save_directory="../../data/output", # save output repo data output subdir
                                  expire_time=60 * 10,    # set all process data to expire in 10 minutes
                                  wait_for_process=True,  # wait for process to complete before regaining ide
                                  verbose=False,          # set verbosity to False
                                  modules={
                                    "parser": {"model": "fixed", "params": {"chunk_size": 10, "overlap_size": 2}}
                                  })
```

Examining the output below we can see that our input document was not cut into complete sentences, but chunks of text.  Each chunk is 10 words in length, and the consecutive chunks overlap by two words.  


```python
# load in process output from file
with open(process_output["process_output_files"][0]) as f:
  print(json.dumps(json.load(f), indent=2))
```

    [
      {
        "snippet": "It was a bright cold day in April, and the",
        "line_numbers": [
          1
        ]
      },
      {
        "snippet": "and the clocks were striking thirteen. Winston Smith, his chin",
        "line_numbers": [
          1,
          2
        ]
      },
      {
        "snippet": "his chin nuzzled into his breast in an effort to",
        "line_numbers": [
          2
        ]
      },
      {
        "snippet": "effort to escape the vile wind, slipped quickly through the",
        "line_numbers": [
          2,
          3
        ]
      },
      {
        "snippet": "through the glass doors of Victory Mansions, though not quickly",
        "line_numbers": [
          3,
          4
        ]
      },
      {
        "snippet": "not quickly enough to prevent a swirl of gritty dust",
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

