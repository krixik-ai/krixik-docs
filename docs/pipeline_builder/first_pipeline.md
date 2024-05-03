### Build your first pipeline

Let's build a standard text search pipeline using modules.
 
First we instantiate our modules - here we need the `parser`, `text-embedder`, and `vector-db` modules.  The `parser` currently takes care of setting up `keyword-db`.


```python
from krixik.pipeline_builder.module import Module

# define a text search pipeline using modules
parser = Module(module_type='parser')
text_embedder = Module(module_type='text-embedder')
vector_search = Module(module_type='vector-db')
```

We want to make a pipeline from these four modules that looks like this

`parser` --> `text-embedder` --> `vector-db`

That is, a sequence of discrete processing steps:

- the `parser` module takes a *json* file as *input* and outputs a *json* file of text snippets
- the `text-embedder` processes as *input* the *json* output from the `parser`'s and produces numpy *output*
- the `vector-db` module takes as *input* the numpy *output* from `text-embedder` and produces a vector index as *output*

With our modules instantiated they can be added one a time using pipeline's `.add` api, or all together at instantiation of the pipeline.  

When taking the latter approach the modules are simply placed in order into a list called `module_chain` as shown below


```python
from krixik.pipeline_builder.pipeline import CreatePipeline

text_search_pipeline = CreatePipeline(name='my-text-search-pipeline', 
                                      module_chain=[parser, text_embedder, vector_search])
```

Connection or "click-ability" tests are performed on the instantiation of this object.  These guarantee proper flow of input/output information through the defined module chain of the pipeline.

These tests catch incompatible module connections.  For example if we try the pipeline

`vector-db` --> `text-embedder`

our instantiation will fail with a message about *why* the connection won't work. 

 Lets try (and fail) to build this pipeline.


```python
from krixik.pipeline_builder.pipeline import CreatePipeline

fail_pipeline = CreatePipeline(name='my-failed-pipeline', 
                               module_chain=[vector_search, text_embedder])
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    Cell In[8], line 3
          1 from krixik.pipeline_builder.pipeline import CreatePipeline
    ----> 3 fail_pipeline = CreatePipeline(name='my-failed-pipeline', 
          4                                module_chain=[vector_search, text_embedder])


    File ~/Desktop/krixik/krixik_cli/docs/system/../../krixik/pipeline_builder/pipeline.py:58, in CreatePipeline.__init__(self, name, module_chain, config_path)
         54     raise ValueError(
         55         f"pipelines cannot currently have more than {MAX_MODULES} modules"
         56     )
         57 for module in module_chain:
    ---> 58     self.add(module)
         59 self.test_connections()


    File ~/Desktop/krixik/krixik_cli/docs/system/../../krixik/pipeline_builder/pipeline.py:83, in CreatePipeline.add(self, module, insert_index)
         80 self.__module_chain_configs.append(module.config)
         81 self.__module_chain_output_process_keys.append(module.output_process_key)
    ---> 83 self.test_connections()


    File ~/Desktop/krixik/krixik_cli/docs/system/../../krixik/pipeline_builder/pipeline.py:160, in CreatePipeline.test_connections(self)
        158 # check format compatibility
        159 if prev_module_output_format != curr_module_input_format:
    --> 160     raise TypeError(
        161         f"format type mismatch between {prev_module.name} - whose output format is {prev_module_output_format} - and {curr_module.name} - whose input format is {curr_module_input_format}"
        162     )
        164 # check process key type compatibility
        165 if (
        166     prev_module_output_process_key_type
        167     != curr_module_input_process_key_type
        168 ):


    TypeError: format type mismatch between vector-db - whose output format is faiss - and text-embedder - whose input format is json


For more details on what's happening with these tests see Section 2 of this document.  For now the details are not critical.