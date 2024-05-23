## The `caption` Module

The `caption` module takes an image as input and returns a text description of that image.

This overview of the `caption` module is divided into the following sections:

- [Inputs and Outputs of the `caption` Module](#inputs-and-outputs-of-the-caption-module)
- [Available Models in the `caption` Module](#available-models-in-the-caption-module)
- [Model Parameters in the `caption` Module](#model-parameters-in-the-caption-module)
- [A Single-Module Pipeline for the `caption` Module](#a-single-module-pipeline-for-the-caption-module)
- [Further Information on `caption` Module IO and Clickability](#further-information-on-caption-module-io-and-clickability)

### Inputs and Outputs of the `caption` Module

The `caption` module accepts image inputs. Acceptable file formats are the following:

- JPG

- JPEG

- PNG

The `caption` module returns a JSON file. At the core of the returned JSON file lies a dictionary that in turn contains the newly generated image caption.

### Available Models in the `caption` Module

You can activate any of the following models when using the `caption` module:

- [vit-gpt2-image-captioning](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning) (default)

- [git-base](https://huggingface.co/microsoft/git-base)

- [blip-image-captioning-base](https://huggingface.co/Salesforce/blip-image-captioning-base)

- [blip-image-captioning-large](https://huggingface.co/Salesforce/blip-image-captioning-large)

Use the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method to determine what model you'd like active when you process files through the `caption` module.

### Model Parameters in the `caption` Module

None of the `caption` module models are parameterizable. Consequently, when selecting what model you'll use through the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method's [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument, `params` will always be set to an empty dictionary. For example:

```python
# example model selection for caption module in .process
modules={'caption': {'model':'blip-image-captioning-base',
                     'params': {}}}
```

### A Single-Module Pipeline for the `caption` Module

Please click [here](../../examples/single_module_pipelines/single_caption.md) to visit the `Pipeline Examples` section of our documentation and review an example of a single-module pipeline for the `caption` module.

### Further Information on `caption` Module IO and Clickability

Please click [here](../../system/convenience_methods/convenience_methods.md) to visit the `Convenience Methods (and More!)` documentation. There you will find two tools to learn more about the `caption` module:

- [View Module Input and Output Examples](../../system/convenience_methods/convenience_methods.md#view-module-input-and-output-examples)

- [View Module Click Data with the `.click_data` Method](../../system/convenience_methods/convenience_methods.md#view-module-click-data-with-the-click_data-method)
