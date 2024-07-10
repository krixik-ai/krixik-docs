<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/convenience_methods/convenience_methods.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Convenience Methods (and More!)

This document introduces several useful properties of the main Krixik object and of Krixik pipelines that range from useful (advanced) metadata to convenience functions designed to facilitate input testing. All of these properties can be leveraged *without* necessarily having [initialized a session](../initialization/initialize_and_authenticate.md).

The document is broken down as follows:

- [View All Available Modules with the `available_modules` Property](#view-all-available-modules-with-the-available_modules-property)
- [Examine Configuration of a Module with the `module_details` method](#examine-configuration-of-a-module-with-the-module_details-method)
- [View Pipeline Module Chain with the `module_chain` Property](#view-pipeline-module-chain-with-the-module_chain-property)
- [Test Pipeline Input with the `test_input` Method](#test-pipeline-input-with-the-test_input-method)
- [View Module Input and Output Examples](#view-module-input-and-output-examples)
- [View Module Click Data with the `click_data` Method](#view-module-click-data-with-the-click_data-method)


### View All Available Modules with the `available_modules` Property

To view all available modules use the `available_modules` property.  This can be done locally and without [first initializing](../initialization/initialize_and_authenticate.md), as follows:


```python
# see all currently available modules
krixik.available_modules
```




    ['caption',
     'json-to-txt',
     'keyword-db',
     'ocr',
     'parser',
     'sentiment',
     'summarize',
     'text-embedder',
     'transcribe',
     'translate',
     'vector-db']



The above is a list of the exact module names you would use when setting up a [new pipeline's](../pipeline_creation/create_pipeline.md) `module_chain`.

### Examine Configuration of a Module with the `module_details` Method

Any module's [configuration](../pipeline_creation/pipeline_config.md) can be viewed using the Krixik `module_details` method. This can be done locally and without [first initializing](../initialization/initialize_and_authenticate.md), as follows:


```python
# view the configuration of a Krixik module - in this example, transcribe
krixik.view_module_config(module_name="transcribe")
```




    {'module_config': {'module': {'name': 'transcribe',
       'models': [{'name': 'whisper-tiny'},
        {'name': 'whisper-base'},
        {'name': 'whisper-small'},
        {'name': 'whisper-medium'},
        {'name': 'whisper-large-v3'}],
       'input': {'type': 'audio'},
       'output': {'type': 'json'},
       'defaults': {'model': 'whisper-tiny'}}},
     'input_data_example': None,
     'output_data_example': {'transcript': 'This is the full transcript.',
      'segments': [{'id': 1,
        'seek': 0,
        'start': 0.0,
        'end': 10.0,
        'text': 'This is the',
        'tokens': [20, 34],
        'temperature': 0.0,
        'avg_logprob': 0.0,
        'compression_ratio': 0.0,
        'no_speech_prob': 0.0,
        'confidence': 0.0,
        'words': [{'text': 'This', 'start': 0.0, 'end': 1.0, 'confidence': 0.5},
         {'text': 'is the', 'start': 1.0, 'end': 2.0, 'confidence': 0.6}]},
       {'id': 2,
        'seek': 10,
        'start': 10.0,
        'end': 20.0,
        'text': 'main text',
        'tokens': [44, 101],
        'temperature': 0.0,
        'avg_logprob': 0.0,
        'compression_ratio': 0.0,
        'no_speech_prob': 0.0,
        'confidence': 0.0,
        'words': [{'text': 'main', 'start': 10.0, 'end': 11.0, 'confidence': 0.7},
         {'text': 'text', 'start': 11.0, 'end': 12.0, 'confidence': 0.8}]}],
      'language': 'English'}}



### View Pipeline Module Chain with the `module_chain` Property

Sometimes you want to quickly view a pipeline's `module_chain` without having to resort to examining a [config](../pipeline_creation/pipeline_config.md) file. This is where the `module_chain` property comes in handy.

Suppose we create a [multi-module pipeline](../../examples/pipeline_examples_overview.md) like the one below (discussed in further detail in examples like [this one](../../examples/search_pipeline_examples/multi_semantically_searchable_translation.md)):


```python
# create a multi-module pipeline
pipeline = krixik.create_pipeline(
    name="system-transcribe-semantic-multilingual-docs",
    module_chain=["transcribe", "translate", "json-to-txt", "parser", "text-embedder", "vector-db"],
)
```

To view the module chain of this (or any pipeline), use the `module_chain` property. This can be done locally and without [first initializing](../initialization/initialize_and_authenticate.md), as follows:


```python
# view the module chain of your pipeline using the module_chain property
pipeline.module_chain
```




    ['transcribe',
     'translate',
     'json-to-txt',
     'parser',
     'text-embedder',
     'vector-db']



### Test Pipeline Input with the `test_input` Method

You can test whether inputs to a pipeline will flow properly through it by using the `test_input` method. 

We illustrate this below for both valid and invalid files using the [pipeline we created above](#view-pipeline-module-chain-with-the-module_chain-property). 

Note that this test method does **not** execute your pipeline.  Nothing is sent server-side; it simply makes sure that your input file is consumable by the first module of your pipeline. Flow-through across the rest of your pipeline was already confirmed upon [pipeline instantiation](../pipeline_creation/create_pipeline.md).

Let's first test with a file that is valid for this pipeline. Since the first module is a [`transcribe`](../../modules/ai_modules/transcribe_module.md) module, an MP3 with clear spoken English in it will do the trick. This can be done locally and without [first initializing](../initialization/initialize_and_authenticate.md), as follows:


```python
# use test_input on a valid file for this pipeline
pipeline.test_input(local_file_path=data_dir + "input/Interesting Facts About Colombia.mp3")
```

    SUCCESS: local file '../../../data/input/Interesting Facts About Colombia.mp3' passed pipeline input test passed


Now let's test with an input that won't work with this pipeline. The [`transcribe`](../../modules/ai_modules/transcribe_module.md) module that the pipeline begins with will **not** accept a TXT file, so the result of this test looks thus:


```python
# use test_input on a file that won't work for this pipeline
pipeline.test_input(local_file_path=data_dir + "input/1984_very_short.txt")
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    File ~/Desktop/krixik/code/krixik-docs/docs_venv/lib/python3.10/site-packages/krixik/utilities/validators/data/utilities/decorators.py:47, in datatype_validator.<locals>.wrapper(*args, **kwargs)
         46             raise ValueError(f"invalid file extension: '{extension}'")
    ---> 47     return func(*args, **kwargs)
         48 except ValueError as e:


    File ~/Desktop/krixik/code/krixik-docs/docs_venv/lib/python3.10/site-packages/krixik/pipeline_builder/pipeline.py:130, in BuildPipeline.test_input(self, local_file_path)
        123 """test input file will flow through pipeline correctly via simulation (currently in beta)
        124 
        125 Parameters
       (...)
        128     path to local file to test for pipeline threadthrough
        129 """
    --> 130 input_check(local_file_path, self.__module_chain)
        131 print(f"SUCCESS: local file '{local_file_path}' passed pipeline input test passed")


    File ~/Desktop/krixik/code/krixik-docs/docs_venv/lib/python3.10/site-packages/krixik/pipeline_builder/utilities/input_checker.py:20, in input_check(local_file_path, module_chain)
         19 if file_ext_format != first_module_input_format:
    ---> 20     raise TypeError(f"file extension '{file_ext}' does not match the expected input format {first_module_input_format}")
         21 is_valid(first_module.name, local_file_path)


    TypeError: file extension '.txt' does not match the expected input format audio

    
    During handling of the above exception, another exception occurred:


    Exception                                 Traceback (most recent call last)

    Cell In[7], line 2
          1 # use test_input on a file that won't work for this pipeline
    ----> 2 pipeline.test_input(local_file_path=data_dir + "input/1984_very_short.txt")


    File ~/Desktop/krixik/code/krixik-docs/docs_venv/lib/python3.10/site-packages/krixik/utilities/validators/data/utilities/decorators.py:51, in datatype_validator.<locals>.wrapper(*args, **kwargs)
         49     raise ValueError(e)
         50 except Exception as e:
    ---> 51     raise Exception(e)


    Exception: file extension '.txt' does not match the expected input format audio


### View Module Input and Output Examples

Examine the applicable data class of your starting module to ensure that your potential input satisfies required input structure requirements.

You can get a quick sense of a module's input/output structure by looking at an example datapoint, like the one printed below the following code. This can be done for any [currently available module](../../modules/modules_overview.md), so we'll illustrate using the [`parser`](../../modules/support_function_modules/parser_module.md) module. This can be done locally and without [first initializing](../initialization/initialize_and_authenticate.md), as follows:


```python
# examine the required input/output data structure for the Parser module by printing an input and output examples for it
from krixik.modules.parser import io
import json

print("input data example")
print("-----")
print(io.InputStructure().data_example)
print("\n")
print("output data example")
print("-----")
print(json.dumps(io.OutputStructure().data_example, indent=2))
```

    input data example
    -----
    sample text looks like this.
    
    
    output data example
    -----
    {
      "snippet": "This is the main text.",
      "line_numbers": [
        1,
        2,
        3,
        4
      ],
      "other": null
    }


Here `"other"` denotes any other key in your input.  Its value is arbitrary because, as far as any model you connect the [`parser`](../../modules/support_function_modules/parser_module.md) module into is concerned, it's irrelevant. Only the snippet is passed through.

### View Module Click Data with the `click_data` Method

The `.click_data` method displays all the basic data required to know which modules can be "clicked" into which other modules.  This is the data referenced "under the hood" of Krixik when you build a pipeline with the [`.create_pipeline`](../pipeline_creation/create_pipeline.md) method. Let's go through this piece by piece.

First there's the module's input/output data format. A module like [`transcribe`](../../modules/ai_modules/transcribe_module.md) takes in `audio/video` and outputs `JSON`, while the [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) module takes in `JSON` and outputs `NPY`.  

Checking that the *output* format of a module matches the *input* format of another module is the *first* of two steps in determining if two modules can sequentially be clicked together. If the output format of "Module A"  matches the input format of "Module B", you'll likely be able to connect "Module A" → "Module B" in a pipeline. It's not a sure thing yet, though.

The *second* step to determine module "clickability" is to make sure that the input/output `process_type`s match. For instance, a module might input a `JSON` format, but only *process* on certain key-value pairs of it. If there's a mismatch in the key-value pairs that are outputted vs inputted, the pipeline may not work after all.

Checking `process_type` aligment thus confirms (or refutes) whether two modules can be connected.

Lets take a look at the `click_data` of two modules and discuss what it says about their "clickability". This can be done locally and without [first initializing](../initialization/initialize_and_authenticate.md), as follows:


```python
# examine a module's "clickability" data by using the .click_data method
krixik.view_module_click_data(module_name="text-embedder")
```




    {'module_name': 'text-embedder',
     'input_format': 'json',
     'output_format': 'npy',
     'input_process_key': 'snippet',
     'input_process_type': "<class 'str'>",
     'output_process_key': 'data',
     'output_process_type': "<class 'numpy.ndarray'>"}




```python
# examine a module's "clickability" data by using the .click_data method
krixik.view_module_click_data(module_name="vector-db")
```




    {'module_name': 'vector-db',
     'input_format': 'npy',
     'output_format': 'faiss',
     'input_process_key': 'data',
     'input_process_type': "<class 'numpy.ndarray'>",
     'output_process_key': None,
     'output_process_type': None}



This data suggests that we can "click" the modules together like this:

`text-embedder` -> `vector-search`

However, we can *not* click them together like this:

 `vector-search` -> `text-embedder`

The former module connection, (`text-embedder` → `vector-search`), will work because in the `click_data` of both modules we can see that 

- `text-embedder` output_format (`npy`) == `vector-search` input_format (`npy`), and 
- `text-embedder` output_process_type (`<class 'numpy.ndarray'>`) == `vector-search` input_process_type (`<class 'numpy.ndarray'>`)


The latter connection, (`vector-search` → `text-embedder`), will instead not work. We can see from the same data that

- `vector-search` output_format (`faiss`) != `text-embedder` input_format (`json`)


