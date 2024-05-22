## The `parser` Module

The `parser` module takes a text document, cuts it up into pieces, and returns the spliced input as snippets in a JSON file.

This overview of the `parser` module is divided into the following sections:

- [Inputs and Outputs of the `parser` Module](#inputs-and-outputs-of-the-parser-module)
- [Available Models in the `parser` Module](#available-models-in-the-parser-module)
- [Model Parameters in the `parser` Module](#model-parameters-in-the-parser-module)
- [A Single-Module Pipeline for the `parser` Module](#a-single-module-pipeline-for-the-parser-module)
- [Further Information on `parser` Module IO and Clickability](#further-information-on-parser-module-io-and-clickability)

### Inputs and Outputs of the `parser` Module

The `parser` module accepts document inputs. Acceptable file formats are the following:

- TXT

- PDF (automatically converted to TXT before processing)

- DOCX (automatically converted to TXT before processing)

- PPTX (automatically converted to TXT before processing)

The `parser` module returns a JSON file that contains all of the post-parsing text snippets. Each snippet is accompanied by its corresponding line numbers (from the original document) to make it easier for you to later know where in the document any single snippet came from. For example, take a look at the following sample output of a `parser` process:

```python
{
  "status_code": 200,
  "pipeline": "modules-parser-docs",
  "request_id": "5908efbc-b06d-44f3-93c8-a46c29540637",
  "file_id": "575c69c6-0571-4f56-8e49-6c1e4f4a3f4a",
  "message": "SUCCESS - output fetched for file_id 575c69c6-0571-4f56-8e49-6c1e4f4a3f4a.Output saved to location(s) listed in process_output_files.",
  "warnings": [],
  "process_output": [
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
  ],
  "process_output_files": [
    "../../data/output/575c69c6-0571-4f56-8e49-6c1e4f4a3f4a.json"
  ]
}
```

### Available Models in the `parser` Module

You can activate any of the following models when using the `parser` module:

- [sentence](https://www.nltk.org/api/nltk.tokenize.html) - (default)

- `fixed` - Krixik-made. Splits a text into potentially overlapping chunks of consecutive words that always have the same length.

Use the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method to determine what model you'd like active when you process files through the `parser` module.

### Model Parameters in the `parser` Module

Different parameter sets apply for the different `parser` models.

The [`sentence`](https://www.nltk.org/api/nltk.tokenize.html) (default) model _is not_ parameterizable. Consequently, if selecting that model through the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method's [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument, `params` will be set to an empty dictionary, as follows:

```python
# example model selection for parser module in process
modules={'parser': {'model':'sentence',
                    'params': {}}}
```

The `fixed` model _is_ parameterizable. Consequently, if selecting that model through the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method's [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument, `params` can include a value for two different parameters:

- `chunk_size` (int) - Number of consecutive words (a.k.a. tokens) in every chunk/snippet. Defaults to 10.
- `overlap_size` (int) - Number of words that a chunk/snippet overlaps/shares with the previous chunk. If 0, chunks are lined up end-to-end. Defaults to 2.

 For example:

```python
# example model selection for parser module in process
modules={'parser': {"model": "fixed",
                    "params": {"chunk_size": 8, "overlap_size": 3}}}
```

### A Single-Module Pipeline for the `parser` Module

Please click [here](../../examples/single_module_pipelines/single_parser.md) to visit the `Pipeline Examples` section of our documentation and review an example of a single-module pipeline for the `parser` module.

### Further Information on `parser` Module IO and Clickability

Please click [here](../../system/convenience_methods/convenience_methods.md) to visit the `Convenience Methods (and More!)` documentation. There you will find two tools to learn more about the `parser` module:

- [View Module Input and Output Examples](../../system/convenience_methods/convenience_methods.md#view-module-input-and-output-examples)

- [View Module Click Data with the `.click_data` Method](../../system/convenience_methods/convenience_methods.md#view-module-click-data-with-the-click_data-method)
