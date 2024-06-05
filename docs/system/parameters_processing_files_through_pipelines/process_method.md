<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/parameters_processing_files_through_pipelines/process_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## The Parameterizable `process` Method

The `process` method, available on every Krixik pipeline, is invoked whenever you wish to process files through a pipeline.

This overview of the `process` method is divided into the following sections:

- [Core process Method Arguments](#core-process-method-arguments)
- [Basic Usage and Output Breakdown](#basic-usage-and-output-breakdown)
- [Selecting Models Via the modules Argument](#selecting-models-via-the-modules-argument)
- [Using your own Models](#using-your-own-models)
- [Optional Metadata Arguments](#optional-metadata-arguments)
- [Metadata Argument Defaults](#metadata-argument-defaults)
- [Automatic File Type Conversions](#automatic-file-type-conversions)
- [Output Size Cap](#output-size-cap)

### Core `process` Method Arguments

The `process` method takes five basic arguments (in addition to the `modules` argument and a series of optional metadata arguments, all discussed further below). These five arguments are:

- `local_file_path`: (required, str) The local file path of the file you wish to process through the pipeline.

- `local_save_directory`: (optional, str) The local directory you want process output saved to. Defaults to the current working directory.

- `expire_time`: (optional, int) The amount of time (in seconds) that process output remains on Krixik servers. Defaults to 1800 seconds, which is 30 minutes.

- `wait_for_process`: (optional, bool) Indicates whether or not Krixik should wait for your process to complete before returning control of your IDE or notebook. `True` tells Krixik to wait until the process is complete, so you won't be able to execute anything else in the meantime. `False` tells Krixik that you wish to regain control as soon as file upload to the Krixik system has concluded.  When set to `False`, processing status can be examined via the [`process_status`](process_status_method.md) method. Defaults to `True`.

- `verbose`: (optional, bool) Determines if Krixik should immediately display process update printouts at your terminal/notebook. Defaults to `True`.

### Basic Usage and Output Breakdown

Let's first create a single-module pipeline to demonstrate the `process` method with. We'll use a [`sentiment module`](../../modules/ai_modules/sentiment_module.md).


```python
# create single-module pipeline for process demo
pipeline = krixik.create_pipeline(name="process_method_1_sentiment", module_chain=["sentiment"])
```

We've locally created a JSON file that holds three snippets that simulate online product reviews. The snippets read as follows:

- This recliner is the best damn seat I've ever come across. When I fall asleep on it, which is often, I sleep like a baby.

- This recliner is terrible. It broke on its way out of the box, and no matter what I try, it doesn't recline. Avoid at all costs.

- I've sat on a lot of recliners in my life. I've forgotten about most of them. I'll forget about this one as well.

Keep in mind that input JSON files _must_ follow a very [specific format](JSON_input_format.md). If they don't, they'll be rejected by Krixik.


```python
# process short input file
process_demo_output = pipeline.process(
    local_file_path=data_dir + "input/recliner_reviews.json",  # the initial local filepath where the input JSON file is stored
    local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 10 minutes
    wait_for_process=True,  # wait for process to complete before returning IDE control to user
    verbose=False,
)  # do not display process update printouts upon running code
```

Now let's print the output of the process.  Because the output of this particular module-model pair is in JSON format, we can print it nicely with the following code:


```python
# nicely print the output of the above process
import json

print(json.dumps(process_demo_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "process_method_1_sentiment",
      "request_id": "339ef4dd-5c97-4822-b450-aea700bc6021",
      "file_id": "6a314cdb-6938-4663-aef5-a0258341c120",
      "message": "SUCCESS - output fetched for file_id 6a314cdb-6938-4663-aef5-a0258341c120.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "This recliner is the best damn seat I've ever come across. When I fall asleep on it, which is often, I sleep like a baby.",
          "positive": 0.871,
          "negative": 0.129,
          "neutral": 0.0
        },
        {
          "snippet": "This recliner is terrible. It broke on its way out of the box, and no matter what I try, it doesn't recline. Avoid at all costs.",
          "positive": 0.001,
          "negative": 0.999,
          "neutral": 0.0
        },
        {
          "snippet": "I've sat on a lot of recliners in my life. I've forgotten about most of them. I'll forget about this one as well.",
          "positive": 0.001,
          "negative": 0.999,
          "neutral": 0.0
        }
      ],
      "process_output_files": [
        "../../../data/output/6a314cdb-6938-4663-aef5-a0258341c120.json"
      ]
    }


Let's break down the output:

- `status_code`: The HTTP status code for this process (e.g. "200", "500")

- `pipeline`: The `name` of the pipeline we just ran `process` on.

- `request_id`: The unique ID associated with this execution of `process`.

- `file_id`: The unique server-side ID for the now-processed file (and thus its associated output).

- `message`: This message specifies SUCCESS or FAILURE for the method call and offers detail.

- `warnings`: A message list that includes any warnings related to the method call.

- `process_output`: The output of the process. In this case, since the output is in JSON format, it's easily printable in a code notebook.

- `process_output_files`: A list of file names and file paths generated as process outputs and saved locally.


We can see from `process_output` that our [`sentiment analysis`](../../modules/ai_modules/sentiment_module.md) pipeline has worked correctly. Each of the product reviews has been assigned a sentiment value breakdown between positive, negative, and neutral.

In addition to being printed here, this process output is also stored in the file indicated in `process_output_files`. Let's load it in and confirm that it shows the same process output we received above:


```python
# load in process output from file
import json

with open(process_demo_output["process_output_files"][0], "r") as file:
    print(json.dumps(json.load(file), indent=2))
```

    [
      {
        "snippet": "This recliner is the best damn seat I've ever come across. When I fall asleep on it, which is often, I sleep like a baby.",
        "positive": 0.871,
        "negative": 0.129,
        "neutral": 0.0
      },
      {
        "snippet": "This recliner is terrible. It broke on its way out of the box, and no matter what I try, it doesn't recline. Avoid at all costs.",
        "positive": 0.001,
        "negative": 0.999,
        "neutral": 0.0
      },
      {
        "snippet": "I've sat on a lot of recliners in my life. I've forgotten about most of them. I'll forget about this one as well.",
        "positive": 0.001,
        "negative": 0.999,
        "neutral": 0.0
      }
    ]


### Selecting Models Via the `modules` Argument

The `modules` argument to the `process` method is optional, but through it you can access a wealth of parameterization options. This argument allows you to parameterize how each module operates, **INCLUDING** the determination of (when applicable) what AI model is active within it.

The `modules` argument takes the form of a dictionary with dictionaries within it. On a single-module pipeline it looks like this:

```python
modules={'<model name>': {'model':'<model selection>', 'params': <dictionary of parameters>}}
```

Bear in mind that model names are case sensitive.

An example for a single-module pipeline that holds a [`caption module`](../../modules/ai_modules/caption_module.md) would specifically look like this, `blip-image-captioning-base` being the available model selected:

```python
modules={'caption': {'model':'blip-image-captioning-base', 'params': {}}}
```

In the above example `params` is an empty dictionary because [`caption`](../../modules/ai_modules/caption_module.md) module models don't take any parameters. Other types of models do, such as the [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) module models. This is what the `modules` argument might look like for a single-module [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) pipeline:

modules={'text-embedder': {'model':'multi-qa-MiniLM-L6-cos-v1', 'params': {'quantize': False}}}

`quantize` is a parameter that you can set for [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) module models, and only for [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) module models.

The `modules` argument syntax for multi-module pipelines is similar to the above, but in that case there's one sub-dictionary for every module. For instance, the `modules` argument for a [vector search pipeline](../../examples/search_pipeline_examples/multi_basic_semantic_search.md) that sequentially chains together [`parser`](../../modules/support_function_modules/parser_module.md), [`text-embedder`](../../modules/ai_modules/text-embedder_module.md), and [`vector-db`](../../modules/database_modules/vector-db_module.md) modules might look like this:

```python
modules={'parser': {'model':'fixed', 'params': {"chunk_size": 10, "overlap_size": 5}},
         'text-embedder': {'model':'all-MiniLM-L6-v2', 'params': {}},
         'vector-db': {'model':'faiss', 'params': {}}}
```

Note that any modules not explicitly called out will take their default values. If you need to specify one module's model or its params, that doesn't mean you need to specify all of them in the pipeline. Consequently, given that in the code immediately above the [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) and [`vector-db`](../../modules/database_modules/vector-db_module.md) modules above are being set to their default values, you could achieve the exact same thing by removing them from the code and only leaving the [`parser`](../../modules/support_function_modules/parser_module.md) module, as follows:

```python
modules={'parser': {'model':'fixed', 'params': {"chunk_size": 10, "overlap_size": 5}}}
```

Find detail on each of our current modules, including available models for each, [here](../../modules/modules_overview.md).

### Using your own Models

Do you have a model—either one you've developed or one you've fine-tuned—that you'd like to use on Krixik?

Please [click here](../../modules/adding_your_own_modules_or_models.md) to learn how to do so!

### Optional Metadata Arguments

The `process` method also takes a variety of optional metadata arguments. These do not change how `process` runs or treats data. Instead, they make your processed files easier to retrieve and organize. You can think of it as a file system for files you've processed through your pipelines.

Optional metadata arguments include:

- `symbolic_directory_path` (str) - A UNIX-formatted directory path under your account in the Krixik system. Default is `/etc`.

- `file_name` (str) - A custom file name that must end with the file extension of the original input file. Default is a randomly-generated string (see below).

- `symbolic_file_path` (str) - A combination of `symbolic_directory_path` and `file_name` in a single argument. Default is a concatenation of the default of each.

- `file_tags` (list) - A list of custom file tags (each a key-value pair). Default is an empty list.

- `file_description` (str) - A custom file description. Default is an empty string.

The first four of these—`symbolic_directory_path`, `file_name`, `symbolic_directory_path`, and `file_tags`—can be used as arguments to the [`list`](../file_system/list_method.md) method and to the [`keyword_search`](../search_methods/keyword_search_method.md) and [`semantic_search`](../search_methods/semantic_search_method.md) methods.

Note that a file you process through one pipeline is only accessible to that pipeline. If you upload a file to a certain `symbolic_directory_path` on a certain pipeline, for instance, you will not be able to [`list`](../file_system/list_method.md), [search](../../examples/search_pipeline_examples/search_pipelines_overview.md), or otherwise access it from any other pipeline, even if you target the same `symbolic_directory_path` from there.

Also note that a `symbolic_file_path` cannot be duplicated within a pipeline. In other words, if on a certain pipeline you `process` a file to a specified `symbolic_directory_path` and `file_name`, Krixik will not allow you to `process` any other files with that same combination of `symbolic_file_path` and `file_name`.

Let's call the `process` method once more. We'll use the same product review file as before, but expand our line of code with some of these optional metadata arguments:


```python
# process short input file with optional metadata arguments
process_demo_output = pipeline.process(
    local_file_path=data_dir + "input/recliner_reviews.json",
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,
    wait_for_process=True,
    verbose=False,
    symbolic_directory_path="/my/custom/filepath",
    file_name="product_reviews.json",
    file_tags=[{"category": "furniture"}, {"product code": "recliner-47b-u11"}],
    file_description="Three product reviews for the Orwell Cloq recliner.",
)
```

### Metadata Argument Defaults

- If no `file_name` is provided, a random one is generated. It takes the form `krixik_generated_file_name_{10 random chars}.ext`, where here `.ext` is the extension of your input file provided in `local_file_path`.

- If no `symbolic_directory_path` is provided, the default value it takes is `/etc`.

- Note that you cannot define any children directories under the `symbolic_directory_path` `/etc`; it is the catch-all directory, and is not meant to be built under.

### Automatic File Type Conversions

For certain modules, the `process` method automatically converts the format of some `local_file_path` input files. Conversions currently done by Krixik are:

- `pdf` -> `txt`
- `docx` -> `txt`
- `pptx` -> `txt`

### Output Size Cap

The current size limit on output generated by the `process` method is 5MB.
