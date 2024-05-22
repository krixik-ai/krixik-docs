## The `sentiment` Module

The `sentiment` module takes one or several text snippets and returns a numerical sentiment breakdown analysis (between positive, negative, and neutral) of each snippet along with each snippet.

This overview of the `sentiment` module is divided into the following sections:

- [Inputs and Outputs of the `sentiment` Module](#inputs-and-outputs-of-the-sentiment-module)
- [Available Models in the `sentiment` Module](#available-models-in-the-sentiment-module)
- [Model Parameters in the `sentiment` Module](#model-parameters-in-the-sentiment-module)
- [A Single-Module Pipeline for the `sentiment` Module](#a-single-module-pipeline-for-the-sentiment-module)
- [Further Information on `sentiment` Module IO and Clickability](#further-information-on-sentiment-module-io-and-clickability)

### Inputs and Outputs of the `sentiment` Module

The `sentiment` module accepts JSON file input. The input JSON must respect [this format](../../system/parameters_processing_files_through_pipelines/JSON_input_format.md).

The `sentiment` module returns a JSON file. The returned JSON file has all input snippets, and along with each has a numerical sentiment breakdown analysis (between positive, negative, and neutral sentiment). The three sentiment scores add up to 1.0.

### Available Models in the `sentiment` Module

You can activate any of the following models when using the `sentiment` module:

- [distilbert-base-uncased-finetuned-sst-2-english](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english) (default)

- [bert-base-multilingual-uncased-sentiment](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment)

- [distilbert-base-multilingual-cased-sentiments-student](https://huggingface.co/lxyuan/distilbert-base-multilingual-cased-sentiments-student)

- [distilroberta-finetuned-financial-news-sentiment-analysis](https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis)

Use the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method to determine what model you'd like active when you process files through the `sentiment` module.

### Model Parameters in the `sentiment` Module

None of the `sentiment` module models are parameterizable. Consequently, when selecting what model you'll use through the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method's [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument, `params` will always be set to an empty dictionary. For example:

```python
# example model selection for sentiment module in process
modules={'sentiment': {'model':'distilroberta-finetuned-financial-news-sentiment-analysis',
                       'params': {}}}
```

### A Single-Module Pipeline for the `sentiment` Module

Please click [here](../../examples/single_module_pipelines/single_sentiment.md) to visit the `Pipeline Examples` section of our documentation and review an example of a single-module pipeline for the `sentiment` module.

### Further Information on `sentiment` Module IO and Clickability

Please click [here](../../system/convenience_methods/convenience_methods.md) to visit the `Convenience Methods (and More!)` documentation. There you will find two tools to learn more about the `sentiment` module:

- [View Module Input and Output Examples](../../system/convenience_methods/convenience_methods.md#view-module-input-and-output-examples)

- [View Module Click Data with the `.click_data` Method](../../system/convenience_methods/convenience_methods.md#view-module-click-data-with-the-click_data-method)
