## Create, save, and load a pipeline

In this document we introduce how to create, save, and load a pipeline from disk.

A table of contents for the remainder of this document is shown below.

- [using the `create_pipeline` method](#using-the-create_pipeline-method)
- [using the `config` method](#using-the-config-method)
- [using the `save_pipeline` method](#using-the-save_pipeline-method)
- [using the `load_pipeline` method](#using-the-load_pipeline-method)

## Using the `create_pipeline` method

`create_pipeline` is used to instantiate a modular pipeline with krixik.  Required input to this method include the following:

- `name`: your custom pipeline name (required)
- `module_chain`: a list of [module names](../modules/overview.md) constituting your desired processing steps

Below we setup a simple one module pipeline using the [`parser` module](../modules/parser.md).  This is an example of a single module pipeline.


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(
    name="system-create-save-load-1", module_chain=["parser"]
)
```

Make sure you have [initialized your session](../system/initialize.md) before executing this code.

Now we setup a pipeline consisting of three modules: a [`parser`](../modules/parser.md), [`text-embedder`](../modules/text-embedder.md), and [`vector-db`](../modules/vector-db.md).  This `module_chain` constitutes a basic document-based semantic (or vector) search pipeline.


```python
# create a pipeline basic document based semantic search pipeline
pipeline = krixik.create_pipeline(
    name="system-create-save-load-2",
    module_chain=["parser", "text-embedder", "vector-db"],
)
```

An array of multi-module pipeline examples can be found in the of this documentation.

Upon execution, the krixik cli performs checks to ensure that these three modules will run properly in the provided sequence.  If they do not, a local exception is thrown with a message about why a module pair cannot be placed in a particular order.

For example, attempting to build the following two module pipeline consisting of [`parser`](../modules/parser.md) and [`caption`](../modules/caption.md) modules in sequence will rightly produce failure with local exception.  This is because the `parser` outputs a json file, while `caption` takes in images.


```python
# create a pipeline basic document based semantic search pipeline
pipeline = krixik.create_pipeline(
    name="system-create-save-load-3", module_chain=["parser", "caption"]
)
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    Cell In[4], line 2
          1 # create a pipeline basic document based semantic search pipeline
    ----> 2 pipeline = krixik.create_pipeline(
          3     name="system-create-save-load-3", module_chain=["parser", "caption"]
          4 )


    File ~/Desktop/krixik/code/krixik-docs/docs/system/../../krixik/main.py:73, in krixik.create_pipeline(cls, name, module_chain)
         71         raise ValueError(f"module_chain item - {item} - is not a currently one of the currently available modules -{available_modules}")
         72 module_chain_ = [Module(m_name) for m_name in module_chain]
    ---> 73 custom = CreatePipeline(name=name,
         74                         module_chain=module_chain_)
         75 return cls.load_pipeline(pipeline=custom)


    File ~/Desktop/krixik/code/krixik-docs/docs/system/../../krixik/pipeline_builder/pipeline.py:58, in CreatePipeline.__init__(self, name, module_chain, config_path)
         56 chain_check(module_chain)
         57 for module in module_chain:
    ---> 58     self._add(module)
         59 self.test_connections()


    File ~/Desktop/krixik/code/krixik-docs/docs/system/../../krixik/pipeline_builder/pipeline.py:85, in CreatePipeline._add(self, module, insert_index)
         82 self.__module_chain_configs.append(module.config)
         83 self.__module_chain_output_process_keys.append(module.output_process_key)
    ---> 85 self.test_connections()


    File ~/Desktop/krixik/code/krixik-docs/docs/system/../../krixik/pipeline_builder/pipeline.py:154, in CreatePipeline.test_connections(self)
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


## Using the `config` method

View the configuration of a pipeline by using the `.config` method on a pipeline object.  This displays required input for each module, the models available for each module of a pipeline and any parameters of these models.  A pipeline's configuration is its complete "under the hood" description.


```python
# create a valid pipeline - here a basic document based semantic search pipeline
pipeline = krixik.create_pipeline(
    name="system-create-save-load-4",
    module_chain=["parser", "text-embedder", "vector-db"],
)

# view the pipeline's configuration file
pipeline.config
```




    {'pipeline': {'name': 'system-create-save-load-4',
      'modules': [{'name': 'parser',
        'models': [{'name': 'sentence'},
         {'name': 'fixed',
          'params': {'chunk_size': {'type': 'int', 'default': 10},
           'overlap_size': {'type': 'int', 'default': 4}}}],
        'defaults': {'model': 'sentence'},
        'input': {'type': 'text',
         'permitted_extensions': ['.txt', '.pdf', '.docx', '.pptx']},
        'output': {'type': 'json'}},
       {'name': 'text-embedder',
        'models': [{'name': 'all-MiniLM-L6-v2',
          'params': {'quantize': {'type': 'bool', 'default': True}}},
         {'name': 'all-mpnet-base-v2',
          'params': {'quantize': {'type': 'bool', 'default': True}}},
         {'name': 'all-MiniLM-L12-v2',
          'params': {'quantize': {'type': 'bool', 'default': True}}},
         {'name': 'multi-qa-MiniLM-L6-cos-v1',
          'params': {'quantize': {'type': 'bool', 'default': True}}},
         {'name': 'msmarco-distilbert-dot-v5',
          'params': {'quantize': {'type': 'bool', 'default': True}}}],
        'defaults': {'model': 'all-MiniLM-L6-v2', 'params': {'quantize': True}},
        'input': {'type': 'json', 'permitted_extensions': ['.json']},
        'output': {'type': 'npy'}},
       {'name': 'vector-db',
        'models': [{'name': 'faiss'}],
        'defaults': {'model': 'faiss'},
        'input': {'type': 'npy', 'permitted_extensions': ['.npy']},
        'output': {'type': 'faiss'}}]}}



## Using the `save_pipeline` method

Saving your pipeline in krixik means *saving its configuration*.

You can save the configuration of pipeline at any time by using the `save_pipeline` method.  Required input to this method:

- `config_path`: a valid local file path

Your `config_path` must end with a `.yml` or `.yaml` extension.


```python
# save a pipeline's configuration to disk - to the data/pipeline_configs directory of the docs repository
pipeline.save_pipeline(
    config_path="../../data/pipeline_configs/save-pipeline-demo.yaml"
)
```

## Using the `load_pipeline` method

A pipeline's configuration is its fundamental descriptor in krixik.  

Any valid config file can be loaded into krixik, re-instantiating its associated pipeline.


```python
# load a pipeline into memory via its valid configuration file - stored in the data/pipeline_configs directory of the krixik docs repository
pipeline = krixik.load_pipeline(
    config_path="../../data/pipeline_configs/save-pipeline-demo.yaml"
)
```
