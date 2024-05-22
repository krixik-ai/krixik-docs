## The `translate` Module

The `translate` module takes one or several text snippets and returns their translations in the selected model's output language.

This overview of the `translate` module is divided into the following sections:

- [Inputs and Outputs of the `translate` Module](#inputs-and-outputs-of-the-translate-module)
- [Available Models in the `translate` Module](#available-models-in-the-translate-module)
- [Model Parameters in the `translate` Module](#model-parameters-in-the-translate-module)
- [A Single-Module Pipeline for the `translate` Module](#a-single-module-pipeline-for-the-translate-module)
- [Further Information on `translate` Module IO and Clickability](#further-information-on-translate-module-io-and-clickability)

### Inputs and Outputs of the `translate` Module

The `translate` module accepts JSON file input. The input JSON must respect [this format](../../system/parameters_processing_files_through_pipelines/JSON_input_format.md).

The `translate` module returns a JSON file. The returned JSON file is in the same format as the input file, but each snippet has been translated.

### Available Models in the `translate` Module

You can activate any of the following models when using the `translate` module:

- [opus-mt-en-es](https://huggingface.co/Helsinki-NLP/opus-mt-en-es) - (default) English to Spanish

- [opus-mt-es-en](https://huggingface.co/Helsinki-NLP/opus-mt-es-en) - Spanish to English

- [opus-mt-de-en](https://huggingface.co/Helsinki-NLP/opus-mt-de-en) - German to English

- [opus-mt-en-fr](https://huggingface.co/Helsinki-NLP/opus-mt-en-fr) - English to French

- [opus-mt-fr-en](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en) - French to English

- [opus-mt-it-en](https://huggingface.co/Helsinki-NLP/opus-mt-it-en) - Italian to English

- [opus-mt-zh-en](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en) - Chinese to English

Use the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method to determine what model you'd like active when you process files through the `translate` module.

### Model Parameters in the `translate` Module

None of the `translate` module models are parameterizable. Consequently, when selecting what model you'll use through the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method's [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument, `params` will always be set to an empty dictionary. For example:

```python
# example model selection for translate module in process
modules={'translate': {'model':'opus-mt-zh-en',
                       'params': {}}}
```

### A Single-Module Pipeline for the `translate` Module

Please click [here](../../examples/single_module_pipelines/single_translate.md) to visit the `Pipeline Examples` section of our documentation and review an example of a single-module pipeline for the `translate` module.

### Further Information on `translate` Module IO and Clickability

Please click [here](../../system/convenience_methods/convenience_methods.md) to visit the `Convenience Methods (and More!)` documentation. There you will find two tools to learn more about the `translate` module:

- [View Module Input and Output Examples](../../system/convenience_methods/convenience_methods.md#view-module-input-and-output-examples)

- [View Module Click Data with the `.click_data` Method](../../system/convenience_methods/convenience_methods.md#view-module-click-data-with-the-click_data-method)
