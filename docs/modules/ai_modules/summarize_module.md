## The `summarize` Module
[🇨🇴 Versión en español de este documento](https://krixik-docs.readthedocs.io/es-main/modulos/modulos_ia/modulo_summarize_resumen/)

The `summarize` module takes a text document and returns a summarized version of it.

This overview of the `summarize` module is divided into the following sections:

- [Inputs and Outputs of the `summarize` Module](#inputs-and-outputs-of-the-summarize-module)
- [Available Models in the `summarize` Module](#available-models-in-the-summarize-module)
- [Model Parameters in the `summarize` Module](#model-parameters-in-the-summarize-module)
- [Input File Size Limit](#input-file-size-limit)
- [A Single-Module Pipeline for the `summarize` Module](#a-single-module-pipeline-for-the-summarize-module)
- [Recursive Summarization](#recursive-summarization)
- [Further Information on `summarize` Module IO and Clickability](#further-information-on-summarize-module-io-and-clickability)

### Inputs and Outputs of the `summarize` Module

The `summarize` module accepts textual document inputs. Acceptable file formats are the following:

- TXT

- PDF (automatically converted to TXT before processing)

- DOCX (automatically converted to TXT before processing)

- PPTX (automatically converted to TXT before processing)

The `summarize` module returns a TXT file containing the requested summary of the input file.

### Available Models in the `summarize` Module

You can activate any of the following models when using the `summarize` module:

- [bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn) (default) [English]

- [text-summarization](https://huggingface.co/Falconsai/text_summarization) [English]

Use the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method to determine what model you'd like active when you process files through the `summarize` module.

### Model Parameters in the `summarize` Module

None of the `summarize` module models are parameterizable. Consequently, when selecting what model you'll use through the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method's [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument, `params` will always be set to an empty dictionary. For example:

```python
# example model selection for summarize module in process
modules={'summarize': {'model':'bart-large-cnn',
                       'params': {}}}
```

### Input File Size Limit

`summarize` module input document files can currently be no larger than 0.25MB.

This size limitation will apply directly to input TXT files. For input PDF, PPTX, and DOCX files, the file size check will take place after conversion to TXT format.

### A Single-Module Pipeline for the `summarize` Module

Please click [here](../../examples/single_module_pipelines/single_summarize.md) to visit the `Pipeline Examples` section of our documentation and review an example of a single-module pipeline for the `summarize` module.

### Recursive Summarization

If the result of summarizing once is not concise enough for your needs, there's a neat trick you can leverage.

One of the most practical ways to achieve a shorter (perhaps more abstract, but still representative) summary is to apply summarization *recursively*. In other words, you feed the summary created above through a summarizer module again, thus producing a briefer summary. Click [here](../../examples/multi_module_non_search_pipeline_examples/multi_recursive_summarization.md) to view detail on a pipeline assembled to achieve exactly this.

### Further Information on `summarize` Module IO and Clickability

Please click [here](../../system/convenience_methods/convenience_methods.md) to visit the `Convenience Methods (and More!)` documentation. There you will find two tools to learn more about the `summarize` module:

- [View Module Input and Output Examples](../../system/convenience_methods/convenience_methods.md#view-module-input-and-output-examples)

- [View Module Click Data with the `click_data` Method](../../system/convenience_methods/convenience_methods.md#view-module-click-data-with-the-click_data-method)
