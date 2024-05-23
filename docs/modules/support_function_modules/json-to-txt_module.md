## The `json-to-txt` Module

The `json-to-txt` module takes several text snippets, joins them into a single string (where the former snippets are now separated by double spaces), and returns the string in a text file.

This overview of the `json-to-txt` module is divided into the following sections:

- [Inputs and Outputs of the `json-to-txt` Module](#inputs-and-outputs-of-the-json-to-txt-module)
- [Available Models in the `json-to-txt` Module](#available-models-in-the-json-to-txt-module)
- [Model Parameters in the `json-to-txt` Module](#model-parameters-in-the-json-to-txt-module)
- [A Single-Module Pipeline for the `json-to-txt` Module](#a-single-module-pipeline-for-the-json-to-txt-module)
- [Further Information on `json-to-txt` Module IO and Clickability](#further-information-on-json-to-txt-module-io-and-clickability)

### Inputs and Outputs of the `json-to-txt` Module

The `json-to-txt` module accepts JSON file input. The input JSON must respect [this format](../../system/parameters_processing_files_through_pipelines/JSON_input_format.md).

The `json-to-txt` module returns a TXT file in which all of the JSON snippets have been concatenated into a single string..

### Available Models in the `json-to-txt` Module

You use the following model when using the `json-to-txt` module:

- `base` - (default) Krixik-made

Use the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method to determine what model you'd like active when you process files through the `json-to-txt` module, though note that at this time there is only one option.

### Model Parameters in the `json-to-txt` Module

The `json-to-txt` module model is not parameterizable. Consequently, should you wish to specify what model you'll use through the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method's [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument, `params` will always be set to an empty dictionary. For example:

```python
# example model selection for json-to-txt module in process
modules={'json-to-txt': {'model':'base',
                         'params': {}}}
```

### A Single-Module Pipeline for the `json-to-txt` Module

Please click [here](../../examples/single_module_pipelines/single_json-to-txt.md) to visit the `Pipeline Examples` section of our documentation and review an example of a single-module pipeline for the `json-to-txt` module.

### Further Information on `json-to-txt` Module IO and Clickability

Please click [here](../../system/convenience_methods/convenience_methods.md) to visit the `Convenience Methods (and More!)` documentation. There you will find two tools to learn more about the `json-to-txt` module:

- [View Module Input and Output Examples](../../system/convenience_methods/convenience_methods.md#view-module-input-and-output-examples)

- [View Module Click Data with the `.click_data` Method](../../system/convenience_methods/convenience_methods.md#view-module-click-data-with-the-click_data-method)
