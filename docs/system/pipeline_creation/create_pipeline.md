<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/pipeline_creation/create_pipeline.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Creating a Pipeline

This overview on creating pipelines is divided into the following sections:

- [The `create_pipeline` Method](#the-create_pipeline-method)
- [A Single-Module Pipeline](#a-single-module-pipeline)
- [A Multi-Module Pipeline](#a-multi-module-pipeline)

### The `create_pipeline` Method

The `create_pipeline` method instantiates new pipelines. It's a very simple method that takes two arguments, both required:

- `name` (str): The name of your new pipeline. Set it wisely: pipeline names are their key identifiers, and no two pipelines can share the same name.
- `module_chain` (list): The sequential list of modules that your new pipeline is comprised of.

[Click here](../../modules/modules_overview.md) to see the current list of available Krixik modules. Remember that as long as outputs and inputs match any combination of modules is fair game, including those with module repetition.

### A Single-Module Pipeline

Let's use the `create_pipeline` method to create a single-module pipeline. We'll use the [`parser`](../../modules/support_function_modules/parser_module.md) module, which divides input text files into shorter snippets.


```python
# create a pipeline with a single parser module
pipeline = krixik.create_pipeline(name="create_pipeline_1_parser", module_chain=["parser"])
```

Make sure that you have [initialized your session](../initialization/initialize_and_authenticate.md) before executing this code.

Note that the `name` argument can be whatever string you want it to be. However, the `module_chain` list can only be comprised of established [module identifiers](../convenience_methods/convenience_methods.md#view-all-available-modules-with-the-available_modules-property).

### A Multi-Module Pipeline

Now let's set up a pipeline sequentially consisting of three modules: a [`parser module`](../../modules/support_function_modules/parser_module.md), a [`text-embedder module`](../../modules/ai_modules/text-embedder_module.md), and a [`vector-db module`](../../modules/database_modules/vector-db_module.md).  This popular `module_chain` arises often: it's the basic document-based semantic (a.k.a. vector) search [pipeline](../../examples/search_pipeline_examples/multi_basic_semantic_search.md).

As you can see, pipeline setup syntax is the same as above. The order of the modules in `module_chain` is the the order they'll process pipeline input in:


```python
# create a basic semantic search multi-module pipeline
pipeline = krixik.create_pipeline(name="create_pipeline_2_parser_embedder_vector", module_chain=["parser", "text-embedder", "vector-db"])
```

An array of multi-module pipeline examples can be [found here](../../examples/pipeline_examples_overview.md).

### Module Sequence Validation

Upon `create_pipeline` execution the Krixik CLI confirms that the modules indicated will run properly in the provided sequence. If they cannot—which is generally a consequence of one module's output not matching the next module's input—an explanatory local exception is thrown.

For example, attempting to build a two-module pipeline that sequentially consists of a [`parser module`](../../modules/support_function_modules/parser_module.md) and a [`caption module`](../../modules/ai_modules/caption_module.md) modules will rightly fail and produce a local exception.  This is because the [`parser module`](../../modules/support_function_modules/parser_module.md) outputs a JSON file, while the [`caption module`](../../modules/ai_modules/caption_module.md) accepts only image input, as the error message below indicates:


```python
# attempt to create a pipeline sequentially comprised of a parser and a caption module
pipeline = krixik.create_pipeline(name="create_pipeline_3_parser_caption", module_chain=["parser", "caption"])
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    Cell In[4], line 3
          1 # attempt to create a pipeline sequentially comprised of a parser and a caption module
    ----> 3 pipeline_3 = krixik.create_pipeline(name="create_pipeline_3_parser_caption",
          4                                     module_chain=["parser", "caption"])


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\main.py:70, in krixik.create_pipeline(cls, name, module_chain)
         68         raise ValueError(f"module_chain item - {item} - is not a currently one of the currently available modules -{available_modules}")
         69 module_chain_ = [Module(m_name) for m_name in module_chain]
    ---> 70 custom = BuildPipeline(name=name, module_chain=module_chain_)
         71 return cls.load_pipeline(pipeline=custom)


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\pipeline_builder\pipeline.py:63, in BuildPipeline.__init__(self, name, module_chain, config_path)
         61 chain_check(module_chain)
         62 for module in module_chain:
    ---> 63     self._add(module)
         64 self.test_connections()


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\pipeline_builder\pipeline.py:86, in BuildPipeline._add(self, module, insert_index)
         83 self.__module_chain_configs.append(module.config)
         84 self.__module_chain_output_process_keys.append(module.output_process_key)
    ---> 86 self.test_connections()


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\pipeline_builder\pipeline.py:160, in BuildPipeline.test_connections(self)
        158 # check format compatibility
        159 if prev_module_output_format != curr_module_input_format:
    --> 160     raise TypeError(
        161         f"format type mismatch between {prev_module.name} - whose output format is {prev_module_output_format} - and {curr_module.name} - whose input format is {curr_module_input_format}"
        162     )
        164 # check process key type compatibility
        165 if prev_module_output_process_key_type != curr_module_input_process_key_type:


    TypeError: format type mismatch between parser - whose output format is json - and caption - whose input format is image


### Pipeline Name Repetition

Krixik will not allow you to create a pipeline with the `name` of a pipeline you have already created. The only exception is if the new pipeline has a module chain identical to the old one.

If you attempt to create a new pipeline with the `name` of a previous pipeline and with a different `module_chain`, initial pipeline instantiation will not fail; in other words, you will be able to run the `create_pipeline` method without issue. However, when two pipelines with the same name and different `module_chain`s exist and you've already [`processed`](../parameters_processing_files_through_pipelines/process_method.md) one file through one of them, you will **not** be allowed to process a file through the other because of pipeline `name` duplication.
