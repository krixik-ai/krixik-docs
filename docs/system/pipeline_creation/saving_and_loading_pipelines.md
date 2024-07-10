<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/pipeline_creation/saving_and_loading_pipelines.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Saving and Loading Pipelines

This overview of the saving and loading pipelines is divided into the following sections:

- [The `save_pipeline` Method](#the-save_pipeline-method)
- [The `load_pipeline` Method](#the-load_pipeline-method)
- [The `reset_pipeline` Function](#the-reset_pipeline-function)

### The `save_pipeline` Method

Saving your pipeline in Krixik means *saving its [configuration](pipeline_config.md)* to disk.

You can save the [configuration](pipeline_config.md) of a pipeline by using the `save_pipeline` method. This method takes one (required) argument:

- `config_path`: A valid local file path.

`config_path` must end with a `.yml` or `.yaml` extension. This is currently the only file format that Krixik saves pipelines into.

To demonstrate how it works, first you'll need to create a pipeline with the [`create_pipeline`](create_pipeline.md) method:


```python
# first create a pipeline
pipeline = krixik.create_pipeline(
    name="saving_and_loading_pipelines_1_summarize_summarize_keyword-db", module_chain=["summarize", "summarize", "keyword-db"]
)
```

Now that you have a pipeline you can use the `save_pipeline` method to save that pipeline to disk:


```python
# save a pipeline's configuration to disk - example file path provided
pipeline.save_pipeline(config_path=data_dir + "pipeline_configs/save-pipeline-demo.yaml")
```

For your convenience, if a file by the given filename does not exist at the given location, Krixik will locally create the file and then save your pipeline
 into it.

### The `load_pipeline` Method

Given that a pipeline's [configuration](pipeline_config.md) is its fundamental descriptor, any valid config file can be loaded into Krixik, thus reinstantiating its associated pipeline.

The `load_pipeline` method takes a single (required) argument:

- `config_path`: A valid local file path.

For the `load_pipeline` method to work, the file indicated by `config_path` must (a) exist, (b) have a `.yaml` or `.yml` extension, and (c) hold a properly formatted Krixik pipeline [configuration](pipeline_config.md). If one of these is not true, the method will fail. If you've earlier [saved](#the-save_pipeline-method) a Krixik pipeline to that destination with that file name, it should work just fine. 

Using the `load_pipeline` method looks like this:


```python
# load a pipeline into memory via its valid configuration file
pipeline = krixik.load_pipeline(config_path=data_dir + "pipeline_configs/save-pipeline-demo.yaml")
```

Note that you don't need to have previously dealt with the saved pipeline yourself. For instance, a colleague may have shared a pipeline [configuration](pipeline_config.md) file with you, or you may have written the file from scratch. As long as the config is properly formatted, the `load_pipeline` method will work as it should.

### The `reset_pipeline` Function

The `load_pipeline` method discussed above reinstantiates a previously existing pipeline with the same `name` and `module_chain`. Since files processed through a pipeline are attached to the pipeline's `name`, those files would continue to be attached to this newly instantiated pipeline.

If you wish to recreate a pipeline but seek to do so with a blank slate, the easiest way to do it is with the `reset_pipeline` function, which deletes all processed datapoints attached to that pipeline (i.e. anything relating to any files previously processed through it).

The `reset_pipeline` function takes one argument (required):

- `pipeline`: The Python variable that the pipeline object is currently saved to.

Note that this is _not_ the `name` of the pipeline. For instance, if you wished to reset the pipeline in the `.load_pipeline` method example code immediately above, the `pipeline` argument for the `reset_pipeline` function would be set to `my_pipeline_2`, as follows:


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```

In other words, the `pipeline` argument to the `reset_pipeline` function is a Python variable that a pipeline object has been assigned to, and `reset_pipeline` will delete any datapoints associated with that pipeline object's `name` on the Krixik system.
