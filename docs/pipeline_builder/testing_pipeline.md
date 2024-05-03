### Testing input in your pipeline

You can test whether inputs to your pipeline will flow properly through it by using your pipeline's `.test_input` api. 

We illustrate this below with both a valid and invalid file for our `text_search_pipeline` above.

Make sure to examine your modules' configs or your pipeline config (detailed in the next subsection) - and in particular the first module's config - to understand allowable input data types and file extensions for your pipeline.  

This test does not execute your pipeline.  It makes sure your input file is consumable by the first module of your pipeline.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# use .test_input to ensure the pipeline is working as expected on test files
text_search_pipeline.test_input(local_file_path=test_file)
```

    SUCCESS: local file ../../examples/input_data/1984_very_short.txt passed pipeline input test passed



```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/seal.png"

# use .test_input to ensure the pipeline is working as expected on test files
text_search_pipeline.test_input(local_file_path=test_file)
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    File ~/Desktop/krixik/krixik_cli/docs/system/../../krixik/utilities/validators/data/utilities/decorators.py:46, in datatype_validator.<locals>.wrapper(*args, **kwargs)
         45             raise ValueError(f"invalid file extension: {extension}")
    ---> 46     return func(*args, **kwargs)
         47 except ValueError as e:


    File ~/Desktop/krixik/krixik_cli/docs/system/../../krixik/pipeline_builder/pipeline.py:125, in CreatePipeline.test_input(self, local_file_path)
        124 if file_ext_format != first_module_input_format:
    --> 125     raise TypeError(
        126         f"file extension {file_ext} does not match the expected input format {first_module_input_format}"
        127     )
        128 is_valid(first_module.name, local_file_path)


    TypeError: file extension .png does not match the expected input format text

    
    During handling of the above exception, another exception occurred:


    Exception                                 Traceback (most recent call last)

    Cell In[10], line 5
          2 test_file = "../../examples/input_data/seal.png"
          4 # use .test_input to ensure the pipeline is working as expected on test files
    ----> 5 text_search_pipeline.test_input(local_file_path=test_file)


    File ~/Desktop/krixik/krixik_cli/docs/system/../../krixik/utilities/validators/data/utilities/decorators.py:50, in datatype_validator.<locals>.wrapper(*args, **kwargs)
         48     raise ValueError(e)
         49 except Exception as e:
    ---> 50     raise Exception(e)


    Exception: file extension .png does not match the expected input format text


Examine the relevant data class of your starting module to ensure your input satisfies the required input structure requirements.

You can get a quick sense of its required structure by looking at a sample datapoint as shown in the next few cells.


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

For a deeper understanding of module io you can examine its `dataclass` as detailed in Section 2.