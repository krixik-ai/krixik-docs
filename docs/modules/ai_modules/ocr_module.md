## The `ocr` Module

The `ocr` module takes an image as input and returns any text found within that image in a JSON file.

This overview of the `ocr` module is divided into the following sections:

- [Inputs and Outputs of the `ocr` Module](#inputs-and-outputs-of-the-ocr-module)
- [Available Models in the `ocr` Module](#available-models-in-the-ocr-module)
- [Model Parameters in the `ocr` Module](#model-parameters-in-the-ocr-module)
- [A Single-Module Pipeline for the `ocr` Module](#a-single-module-pipeline-for-the-ocr-module)
- [Further Information on `ocr` Module IO and Clickability](#further-information-on-ocr-module-io-and-clickability)

### Inputs and Outputs of the `ocr` Module

The `ocr` module accepts image inputs. Acceptable file formats are the following:

- JPG

- JPEG

- PNG

The `ocr` module returns a JSON file. The JSON file holds all identified text and the pixel coordinates on the image for each chunk of identified text.

### Available Models in the `ocr` Module

You can activate any of the following models when using the `ocr` module:

- [tesseract-en](https://github.com/tesseract-ocr/tesseract) - (default) English

- [tesseract-es](https://github.com/tesseract-ocr/tesseract) - Spanish

Use the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method to determine what model you'd like active when you process files through the `ocr` module.

### Model Parameters in the `ocr` Module

None of the `ocr` module models are parameterizable. Consequently, when selecting what model you'll use through the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method's [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument, `params` will always be set to an empty dictionary. For example:

```python
# example model selection for ocr module in .process
modules={'ocr': {'model':'tesseract-es',
                 'params': {}}}
```

### A Single-Module Pipeline for the `ocr` Module

Please click [here](../../examples/single_module_pipelines/single_ocr.md) to visit the `Pipeline Examples` section of our documentation and review an example of a single-module pipeline for the `ocr` module.

### Further Information on `ocr` Module IO and Clickability

Please click [here](../../system/convenience_methods/convenience_methods.md) to visit the `Convenience Methods (and More!)` documentation. There you will find two tools to learn more about the `ocr` module:

- [View Module Input and Output Examples](../../system/convenience_methods/convenience_methods.md#view-module-input-and-output-examples)

- [View Module Click Data with the `.click_data` Method](../../system/convenience_methods/convenience_methods.md#view-module-click-data-with-the-click_data-method)
