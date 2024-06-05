<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/modules/ai_modules/text-embedder_module.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## The `text-embedder` Module

The `text-embedder` module takes one or more text snippets, transforms each into a vector (a mathematical representation of the snippet that retains its meaning), and returns an array containing every generated vector. Vector arrays can then be fed into a vector database to enable semantic (a.k.a. vector) search.

Much has been written about vector embeddings. For instance, if you're curious, take a look at [this Medium article](https://medium.com/@2twitme/an-intuitive-101-guide-to-vector-embeddings-ffde295c3558) or [this YouTube video](https://www.youtube.com/watch?v=NEreO2zlXDk).

This overview of the `text-embedder` module is divided into the following sections:

- [Inputs and Outputs of the `text-embedder` Module](#inputs-and-outputs-of-the-text-embedder-module)
- [Available Models in the `text-embedder` Module](#available-models-in-the-text-embedder-module)
- [Model Parameters in the `text-embedder` Module](#model-parameters-in-the-text-embedder-module)
- [A Single-Module Pipeline for the `text-embedder` Module](#a-single-module-pipeline-for-the-text-embedder-module)
- [Further Information on `text-embedder` Module IO and Clickability](#further-information-on-text-embedder-module-io-and-clickability)

### Inputs and Outputs of the `text-embedder` Module

The `text-embedder` module accepts JSON file input. The input JSON must respect [this format](../../system/parameters_processing_files_through_pipelines/JSON_input_format.md).

The JSON file may optionally also include, along with each snippet, a key-value pair in which the key is the string `"line numbers"` and the value is an integer list of every line number of the original document that the snippet is on. This will make it easier for you to identify what document line each vector is an embedding of.

The `text-embedder` module returns a vector array in an NPY file.

As an example of the `text-embedder` module's input format, take a look at the contents of the following JSON output, printed after the code. This is how an input file must be structured (keep in mind that the `line numbers` key is optional):


```python
# examine the contents of a valid input file
test_file = data_dir + "input/1984_snippets.json"
with open(test_file, "r") as file:
    print(json.dumps(json.load(file), indent=2))
```

    [
      {
        "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
        "line_numbers": [
          1
        ]
      },
      {
        "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
        "line_numbers": [
          2,
          3,
          4,
          5
        ]
      }
    ]


### Available Models in the `text-embedder` Module

You can activate any of the following models when using the `text-embedder` module:

- [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) (default)

- [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2)

- [all-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2)

- [multi-qa-MiniLM-L6-cos-v1](https://huggingface.co/sentence-transformers/multi-qa-MiniLM-L6-cos-v1)

- [msmarco-distilbert-dot-v5](https://huggingface.co/sentence-transformers/msmarco-distilbert-dot-v5)

Use the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method to determine what model you'd like active when you process files through the `text-embedder` module.

### Model Parameters in the `text-embedder` Module

All of the `text-embedder` module models are parameterizable. They all take one parameter:

- `quantize` (boolean) - If `True`, reduces the number of decimal points in vectors for speed and memory while losing a bit of accuracy (this is a very simplified explanation of what vector quantization is). Defaults to `True`.

 Consequently, when selecting what model you'll use through the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method's [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument, `params` can include a value for `quantize`. For example:

```python
# example model selection for text-embedder module in process
modules={'text-embedder': {"model": "all-mpnet-base-v2",
                           "params": {"quantize": False}}}
```

### A Single-Module Pipeline for the `text-embedder` Module

Please click [here](../../examples/single_module_pipelines/single_text-embedder.md) to visit the `Pipeline Examples` section of our documentation and review an example of a single-module pipeline for the `text-embedder` module.

Keep in mind that the output of this pipeline will be an NPY file, which is not human-readable (it's an array of vectors).

### Further Information on `text-embedder` Module IO and Clickability

Please click [here](../../system/convenience_methods/convenience_methods.md) to visit the `Convenience Methods (and More!)` documentation. There you will find two tools to learn more about the `text-embedder` module:

- [View Module Input and Output Examples](../../system/convenience_methods/convenience_methods.md#view-module-input-and-output-examples)

- [View Module Click Data with the `.click_data` Method](../../system/convenience_methods/convenience_methods.md#view-module-click-data-with-the-click_data-method)
