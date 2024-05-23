## The `transcribe` Module

The `transcribe` module takes audio input and returns a text transcript of all words spoken therein.

This overview of the `transcribe` module is divided into the following sections:

- [Inputs and Outputs of the `transcribe` Module](#inputs-and-outputs-of-the-transcribe-module)
- [Available Models in the `transcribe` Module](#available-models-in-the-transcribe-module)
- [Model Parameters in the `transcribe` Module](#model-parameters-in-the-transcribe-module)
- [A Single-Module Pipeline for the `transcribe` Module](#a-single-module-pipeline-for-the-transcribe-module)
- [Further Information on `transcribe` Module IO and Clickability](#further-information-on-transcribe-module-io-and-clickability)

### Inputs and Outputs of the `transcribe` Module

The `transcribe` module accepts audioinputs. Acceptable file formats are the following:

- MP3

The `transcribe` module returns a JSON file. The returned JSON file has all snippets of transcribed text, and along with each includes timestamps and a "confidence" value for the accuracy of each transcription.

### Available Models in the `transcribe` Module

You can activate any of the following models when using the `text-embedder` module:

- [whisper-tiny](https://huggingface.co/openai/whisper-tiny) - (default) Most cost-effective and least accurate of the Whisper models

- [whisper-base](https://huggingface.co/openai/whisper-base)

- [whisper-small](https://huggingface.co/openai/whisper-small)

- [whisper-medium](https://huggingface.co/openai/whisper-medium)

- [whisper-large-v3](https://huggingface.co/openai/whisper-large-v3) - Most accurate but most expensive to run of the Whisper models

Use the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method to determine what model you'd like active when you process files through the `transcribe` module.

### Model Parameters in the `transcribe` Module

None of the `transcribe` module models are parameterizable. Consequently, when selecting what model you'll use through the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method's [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument, `params` will always be set to an empty dictionary. For example:

```python
# example model selection for transcribe module in process
modules={'transcribe': {'model':'whisper-small',
                       'params': {}}}
```

### A Single-Module Pipeline for the `transcribe` Module

Please click [here](../../examples/single_module_pipelines/single_transcribe.md) to visit the `Pipeline Examples` section of our documentation and review an example of a single-module pipeline for the `transcribe` module.

### Further Information on `transcribe` Module IO and Clickability

Please click [here](../../system/convenience_methods/convenience_methods.md) to visit the `Convenience Methods (and More!)` documentation. There you will find two tools to learn more about the `transcribe` module:

- [View Module Input and Output Examples](../../system/convenience_methods/convenience_methods.md#view-module-input-and-output-examples)

- [View Module Click Data with the `.click_data` Method](../../system/convenience_methods/convenience_methods.md#view-module-click-data-with-the-click_data-method)
