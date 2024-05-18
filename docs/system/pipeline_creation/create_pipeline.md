## Creating a Pipeline

### The `.create_pipeline` Method

The `.create_pipeline` method instantiates new pipelines. It's a very simple method that takes two arguments, both required:

- `name` (str): The name of your new pipeline. Set it wisely: pipeline names are their key identifiers, and no two pipelines can share the same name.
- `module_chain` (list): The sequential list of modules that your new pipeline is comprised of.

[Click here](../../modules/modules_overview.md) to see the current list of available Krixik modules. Remember that as long as outputs and inputs match any combination of modules is fair game, including those with module repetition.

### A Single-Module Pipeline

Let's use the `.create_pipeline` method to create a single-module pipeline. We'll use the [`parser module`](../../modules/ai_model_modules/parser_module.md), which divides input text files into shorter snippets.


```python
# create a pipeline with a single parser module

pipeline_1 = krixik.create_pipeline(name="create_pipeline_1_parser",
                                    module_chain=["parser"])
```

Make sure that you have [initialized your session](../initialization/initialize_and_authenticate.md) before executing this code.

Note that the `name` argument can be whatever string you want it to be. However, the `module_chain` list can only be comprised of established [module identifiers](../17-convenience_methods#view-all-available-modules-with-the-available_modules-property).

### A Multi-Module Pipeline

Now let's set up a pipeline sequentially consisting of three modules: a [`parser module`](../../modules/ai_model_modules/parser_module.md), a [`text-embedder module`](../../modules/modules/ai_model_modules/text-embedder_module.md), and a [`vector-db module`](../modules/database_modules/vector-db_module.md).  This popular `module_chain` arises often: it's the basic document-based semantic (a.k.a. vector) search [pipeline](../../examples/search_pipeline_examples/multi_basic_semantic_search.md).

As you can see, pipeline setup syntax is the same as above. The order of the modules in `module_chain` is the the order they'll process pipeline input in:


```python
# create a basic semantic search multi-module pipeline

pipeline_2 = krixik.create_pipeline(name="create_pipeline_2_parser_embedder_vector",
                                    module_chain=["parser", "text-embedder", "vector-db"])
```

An array of multi-module pipeline examples can be [found here](../../examples/pipeline_examples_overview.md).

### Module Sequence Validation

Upon `.create_pipeline` execution the Krixik CLI confirms that the modules indicated will run properly in the provided sequence. If they cannot—which is generally a consequence of one module's output not matching the next module's input—an explanatory local exception is thrown.

For example, attempting to build a two-module pipeline that sequentially consists of a [`parser module`](../../modules/ai_model_modules/parser_module.md) and a [`caption module`](../../modules/ai_model_modules/caption_module.md) modules will rightly fail and produce a local exception.  This is because the [`parser module`](../../modules/ai_model_modules/parser_module.md) outputs a JSON file, while the [`caption module`](../../modules/ai_model_modules/caption_module.md) accepts only image input, as the error message below indicates:


```python
# attempt to create a pipeline sequentially comprised of a parser and a caption module

pipeline_3 = krixik.create_pipeline(name="create_pipeline_3_parser_caption",
                                    module_chain=["parser", "caption"])
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    Cell In[5], line 3
          1 # attempt to create a pipeline sequentially comprised of a parser and a caption module
    ----> 3 pipeline_3 = krixik.create_pipeline(name="create_pipeline_3_parser_caption",
          4                                     module_chain=["parser", "caption"])


    File c:\Users\Lucas\Desktop\Krixik Documentation 1\Version One\System\krixik\main.py:72, in krixik.create_pipeline(cls, name, module_chain)
         70         raise ValueError(f"module_chain item - {item} - is not a currently one of the currently available modules -{available_modules}")
         71 module_chain_ = [Module(m_name) for m_name in module_chain]
    ---> 72 custom = CreatePipeline(name=name,
         73                         module_chain=module_chain_)
         74 return cls.load_pipeline(pipeline=custom)


    File c:\Users\Lucas\Desktop\Krixik Documentation 1\Version One\System\krixik\pipeline_builder\pipeline.py:58, in CreatePipeline.__init__(self, name, module_chain, config_path)
         56 chain_check(module_chain)
         57 for module in module_chain:
    ---> 58     self.add(module)
         59 self.test_connections()


    File c:\Users\Lucas\Desktop\Krixik Documentation 1\Version One\System\krixik\pipeline_builder\pipeline.py:85, in CreatePipeline.add(self, module, insert_index)
         82 self.__module_chain_configs.append(module.config)
         83 self.__module_chain_output_process_keys.append(module.output_process_key)
    ---> 85 self.test_connections()


    File c:\Users\Lucas\Desktop\Krixik Documentation 1\Version One\System\krixik\pipeline_builder\pipeline.py:154, in CreatePipeline.test_connections(self)
        152 # check format compatibility
        153 if prev_module_output_format != curr_module_input_format:
    --> 154     raise TypeError(
        155         f"format type mismatch between {prev_module.name} - whose output format is {prev_module_output_format} - and {curr_module.name} - whose input format is {curr_module_input_format}"
        156     )
        158 # check process key type compatibility
        159 if (
        160     prev_module_output_process_key_type
        161     != curr_module_input_process_key_type
        162 ):


    TypeError: format type mismatch between parser - whose output format is json - and caption - whose input format is image


### Pipeline Name Repetition

Krixik will not allow you to create a pipeline with the name of a pipeline you have already created. The only exception is if the new pipeline has a module chain identical to the old one.

For instance, with the following code you'll create another pipeline with the name "create_pipeline_1_parser", a name you used to create a pipeline earlier in this document. Since the module chain you're using is the same one as above, no issue will arise:


```python
# valid creation of a pipeline with a pre-existing name

pipeline_4 = krixik.create_pipeline(name="create_pipeline_1_parser",
                                    module_chain=["parser"])
```

Now suppose you want to use the same pipeline name, but this time adding a [`summarize module`](../../modules/ai_model_modules/summarize_module.md) to the [`parser module`](../../modules/ai_model_modules/parser_module.md). Since the `module_chain` has changed, Krixik will not allow you to use the same name as above, and pipeline creation will fail:


```python
# invalid creation of a pipeline with a pre-existing name

pipeline_5 = krixik.create_pipeline(name="create_pipeline_1_parser",
                                    module_chain=["parser", "summarize"])
```

Note that the name itself does not matter; instead of the string "create_pipeline_1_parser", you could have used the string "apples are red" for a name, and the outcome would have been the same.
