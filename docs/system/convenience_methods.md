## Convenience methods

In this section we introduce useful properties of the main krixik object and of pipelines.  These range from useful metadata to convenience functions for input testing.  These properties can be viewed *without* [initializing a session](system/initialize.md).

A table of contents for the remainder of this document is shown below.

- [viewing available modules locally](#viewing-available-modules-locally)
- [examine a module configuration](#examine-a-module-configuration)
- [viewing a pipeline module chain](#viewing-a-pipeline-module-chain)
- [testing pipeline input flow](#testing-pipeline-input-flow)
- [viewing example module input](#viewing-example-module-input)
- [viewing module click data](#viewing-module-click-data)

### Viewing available modules locally

To view all available modules locally use the `available_modules` method.  This can be used without first [initializing](system/initialize.md).


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



### Examine a module configuration

A module's configuration can be viewed using the krixik `module_details` method as illustrated below.


```python
# view the configuration of an input module
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



### Viewing a pipeline module chain

Suppose we create a multi-module pipeline like the one below - which is discussed in further detail [in this example](examples/transcribe/transcribe-multilingual-semantic.md).


```python
# create a multi-module pipeline
pipeline = krixik.create_pipeline(name="system-transcribe-semantic-multilingual-docs",
                                  module_chain=["transcribe",
                                                "translate",
                                                "json-to-txt",
                                                "parser",
                                                "text-embedder",
                                                "vector-db"])
```

To view the module chain of this or any pipeline, use the `module_chain` property.


```python
# view the module chain of your pipeline using the .module_chain property
pipeline.module_chain
```




    ['transcribe',
     'translate',
     'json-to-txt',
     'parser',
     'text-embedder',
     'vector-db']



### Testing pipeline input flow

You can test whether inputs to your pipeline will flow properly through it by using your pipeline's `test_input` method. 

We illustrate this below with both a valid and invalid file for the [pipeline above](#viewing-a-pipeline-module-chain). 

This test does not execute your pipeline.  It makes sure your input file is consumable by the first module of your pipeline.


```python
# define path to an input file from examples directory
test_file = "../../data/input/Interesting Facts About Colombia.mp4"

# use .test_input to ensure the pipeline is working as expected on test files
pipeline.test_input(local_file_path=test_file)
```

    SUCCESS: local file ../../data/input/Interesting Facts About Colombia.mp4 passed pipeline input test passed


If you test an input in your pipeline that will not flow correctly you will receive an error like the one below.  Here we test whether or not a text file can be used as input to a pipeline that begins with a [transcribe module](modules/transcribe.md).  It cannot, so we get an error.


```python
# define path to an input file from examples directory
test_file = "../../data/input/1984_very_short.txt"

# use .test_input to ensure the pipeline is working as expected on test files
pipeline.test_input(local_file_path=test_file)
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    File ~/Desktop/krixik/code/krixik-docs/docs/system/../../krixik/utilities/validators/data/utilities/decorators.py:46, in datatype_validator.<locals>.wrapper(*args, **kwargs)
         45             raise ValueError(f"invalid file extension: {extension}")
    ---> 46     return func(*args, **kwargs)
         47 except ValueError as e:


    File ~/Desktop/krixik/code/krixik-docs/docs/system/../../krixik/pipeline_builder/pipeline.py:122, in CreatePipeline.test_input(self, local_file_path)
        120 @datatype_validator
        121 def test_input(self, *, local_file_path: str) -> None:
    --> 122     input_check(local_file_path, self.__module_chain)
        123     print(
        124         f"SUCCESS: local file {local_file_path} passed pipeline input test passed"
        125     )


    File ~/Desktop/krixik/code/krixik-docs/docs/system/../../krixik/pipeline_builder/utilities/input_checker.py:18, in input_check(local_file_path, module_chain)
         17 if file_ext_format != first_module_input_format:
    ---> 18     raise TypeError(
         19         f"file extension {file_ext} does not match the expected input format {first_module_input_format}"
         20     )
         21 is_valid(first_module.name, local_file_path)


    TypeError: file extension .txt does not match the expected input format audio

    
    During handling of the above exception, another exception occurred:


    Exception                                 Traceback (most recent call last)

    Cell In[8], line 5
          2 test_file = "../../data/input/1984_very_short.txt"
          4 # use .test_input to ensure the pipeline is working as expected on test files
    ----> 5 pipeline.test_input(local_file_path=test_file)


    File ~/Desktop/krixik/code/krixik-docs/docs/system/../../krixik/utilities/validators/data/utilities/decorators.py:50, in datatype_validator.<locals>.wrapper(*args, **kwargs)
         48     raise ValueError(e)
         49 except Exception as e:
    ---> 50     raise Exception(e)


    Exception: file extension .txt does not match the expected input format audio


### Viewing example module input

Examine the relevant data class of your starting module to ensure your input satisfies the required input structure requirements.

You can get a quick sense of its required structure by looking at a sample datapoint as shown in the next few cells.  These actions can be performed for any [currently available module](modules/overview.md).  Below we illustrate using the [parser module](modules/parser.md).


```python
# exampine the required input / output data structure for the parser module by printing an example of each
from krixik.modules.parser import io
import json
print('input data example')
print('-----')
print(io.InputStructure().data_example)
print('\n')
print('output data example')
print('-----')
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


Here `other` denotes any other key in your input.  Its value is arbitrary.

### Viewing module click data

The module property `click_data` displays all the basic data required to know which other modules it can be "clicked" into in a pipeline.  This is precisely what data is referenced "under the hood" of krixik when you build a pipeline using the `pipeline` api.

First there's the module's input / output data format.  A module like  `transcribe` takes in `audio` and outputs `json`, while the `text-embedder` takes in `json` and outputs `.npy`.  

Checking that the *output* format of a module matches the *input* format of another module is the *first* of two steps in determining if two modules can be clicked together.  If the output format of "module A"  matches the input format of "module B" you'll likely be able to connect "module A" --> "module B" in a pipeline.

The *second* step to determine module click-ability is to make sure the input/output  `process_type`'s match.  A module might input a `json` format, but only *process* on certain key-value pairs of it.  

Checking this aligment of `process_type` guarantees modules can be connected.

Lets take a look at the `click_data` of two modules and discuss what it says about their "click-ability".


```python
# examine a module's "click-ability" data by using the click_data property
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
# examine a module's "click-ability" data by using the click_data property
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

but *not* like this

 `vector-search` -> `text-embedder`

The first module connection (`text-embedder` -> `vector-search`) will work since - from the `click_data` of both modules - we can see that 

- `text-embedder` output_format (`npy`) == `vector-search` input_format (`npy`), and 
- `text-embedder` output_process_type (`<class 'numpy.ndarray'>`) == `vector-search` input_process_type (`<class 'numpy.ndarray'>`)


The latter connection ( `vector-search` -> `text-embedder`) will not work since we can see from the same data 

- `vector-search` output_format (`faiss`) != `text-embedder` input_format (`json`)


