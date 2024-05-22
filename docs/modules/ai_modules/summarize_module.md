## The `summarize` Module

The `summarize` module takes a text document and returns a summarized version of it.

This overview of the `summarize` module is divided into the following sections:

- [Inputs and Outputs of the `summarize` Module](#inputs-and-outputs-of-the-summarize-module)
- [Available Models in the `summarize` Module](#available-models-in-the-summarize-module)
- [Model Parameters in the `summarize` Module](#model-parameters-in-the-summarize-module)
- [A Single-Module Pipeline for the `summarize` Module](#a-single-module-pipeline-for-the-summarize-module)
- [Recursive Summarization](#recursive-summarization)
- [Further Information on `summarize` Module IO and Clickability](#further-information-on-summarize-module-io-and-clickability)

### Inputs and Outputs of the `summarize` Module

The `summarize` module accepts document inputs. Acceptable file formats are the following:

- TXT

- PDF (automatically converted to TXT before processing)

- DOCX (automatically converted to TXT before processing)

- PPTX (automatically converted to TXT before processing)

The `summarize` module returns a TXT file containing the requested summary of the input file.

### Available Models in the `summarize` Module

You can activate any of the following models when using the `summarize` module:

- [bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn) (default)

- [text-summarization](https://huggingface.co/Falconsai/text_summarization)

Use the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method to determine what model you'd like active when you process files through the `summarize` module.

### Model Parameters in the `summarize` Module

None of the `summarize` module models are parameterizable. Consequently, when selecting what model you'll use through the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method's [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument, `params` will always be set to an empty dictionary. For example:

```python
# example model selection for summarize module in process
modules={'summarize': {'model':'bart-large-cnn',
                       'params': {}}}
```

### A Single-Module Pipeline for the `summarize` Module

Please click [here](../../examples/single_module_pipelines/single_summarize.md) to visit the `Pipeline Examples` section of our documentation and review an example of a single-module pipeline for the `summarize` module.

### Recursive Summarization

If the result of summarizing once is not concise enough for your needs, there's a neat trick you can leverage.

One of the most practical ways to achieve a shorter (perhaps more abstract, but still representative) summary is to apply summarization *recursively*. In other words, you feed the summary created above through a summarizer module again, thus producing a briefer summary. Click [here](../../examples/multi_module_non_search_pipeline_examples/multi_recursive_summarization.md) to view detail on a pipeline assembled to achieve exactly this.

### Further Information on `summarize` Module IO and Clickability

Please click [here](../../system/convenience_methods/convenience_methods.md) to visit the `Convenience Methods (and More!)` documentation. There you will find two tools to learn more about the `summarize` module:

- [View Module Input and Output Examples](../../system/convenience_methods/convenience_methods.md#view-module-input-and-output-examples)

- [View Module Click Data with the `click_data` Method](../../system/convenience_methods/convenience_methods.md#view-module-click-data-with-the-click_data-method)
