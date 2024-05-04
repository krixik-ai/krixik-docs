## Create, save, and load a pipeline

In this document we introduce how to create, save, and load a pipeline from disk.

A table of contents for the remainder of this document is shown below.

- [using the `create_pipeline` method](#using-the-create-pipeline-method)
- [using the `config` method](#using-the-config-method)
- [using the `save_pipeline` method](#using-the-save-pipeline-method)
- [using the `load_pipeline` method](#using-the-load-pipeline-method)

## Using the `create_pipeline` method

`create_pipeline` is used to instantiate a modular pipeline with krixik.  Required input to this method include the following:

- `name`: your custom pipeline name (required)
- `module_chain`: a list of [module names](modules/overview.md) constituting your desired processing steps

Below we setup a simple one module pipeline using the [`parser` module](modules/parser.md).  This is an example of a single module pipeline.


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(name="system-create-save-load-1",
                                  module_chain=["parser"])
```

Make sure you have [initialized your session](system/initialize.md) before executing this code.

Now we setup a pipeline consisting of three modules: a [`parser`](modules/parser.md), [`text-embedder`](modules/text-embedder.md), and [`vector-db`](modules/vector-db.md).  This `module_chain` constitutes a basic document-based semantic (or vector) search pipeline.


```python
# create a pipeline basic document based semantic search pipeline
pipeline = krixik.create_pipeline(name="system-create-save-load-2",
                                  module_chain=["parser", 
                                                "text-embedder", 
                                                "vector-db"])
```

An array of multi-module pipeline examples can be found in the [examples section](examples/overview.md) of this documentation.

Upon execution, the krixik cli performs checks to ensure that these three modules will run properly in the provided sequence.  If they do not, a local exception is thrown with a message about why a module pair cannot be placed in a particular order.

For example, attempting to build the following two module pipeline consisting of [`parser`](modules/parser.md) and [`caption`](modules/caption.md) modules in sequence will rightly produce failure with local exception.  This is because the `parser` outputs a json file, while `caption` takes in images.


```python
# create a pipeline basic document based semantic search pipeline
pipeline = krixik.create_pipeline(name="system-create-save-load-3",
                                  module_chain=["parser", 
                                                "caption"])
```

## Using the `config` method

View the configuration of a pipeline by using the `.config` method on a pipeline object.  This displays required input for each module, the models available for each module of a pipeline and any parameters of these models.  A pipeline's configuration is its complete "under the hood" description.


```python
# create a valid pipeline - here a basic document based semantic search pipeline
pipeline = krixik.create_pipeline(name="system-create-save-load-4",
                                  module_chain=["parser", 
                                                "text-embedder", 
                                                "vector-db"])

# view the pipeline's configuration file
pipeline.config
```

## Using the `save_pipeline` method

Saving your pipeline in krixik means *saving its configuration*.

You can save the configuration of pipeline at any time by using the `save_pipeline` method.  Required input to this method:

- `config_path`: a valid local file path

Your `config_path` must end with a `.yml` or `.yaml` extension.


```python
# save a pipeline's configuration to disk - to the data/pipeline_configs directory of the docs repository
pipeline.save_pipeline(config_path="../../data/pipeline_configs/save-pipeline-demo.yaml")
```

## Using the `load_pipeline` method

A pipeline's configuration is its fundamental descriptor in krixik.  

Any valid config file can be loaded into krixik, re-instantiating its associated pipeline.


```python
# load a pipeline into memory via its valid configuration file - stored in the data/pipeline_configs directory of the krixik docs repository
pipeline = krixik.load_pipeline(config_path="../../data/pipeline_configs/save-pipeline-demo.yaml")
```
