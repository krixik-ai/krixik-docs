## Pipeline `.config`

The `.config` method allows you to view a pipeline's configuration. For each module in the pipeline it displays acceptable input formats, output formats, models available, and any parameters of the available models.  In other words, a pipeline's configuration is its complete "under the hood" description.

Using the `.config` method is very simple. First let's create a pipeline to try it on:


```python
# first create a valid pipeline

pipeline_1 = krixik.create_pipeline(name="pipeline_config_1_parser_translate_sentiment",
                                    module_chain=["translate", "sentiment"])
```

Now let's view this pipeline's configuration with the `.config` method:


```python
# view the pipeline's configuration file

pipeline_1.config
```

As you can see, the `.config` method has provided all relevant details for this pipeline's modules, which are a [`translate module`](../../modules/ai_model_modules/translate_module.md) and a [`sentiment module`](../../modules/ai_model_modules/sentiment_module.md). A blueprint of sorts has been displayed.
