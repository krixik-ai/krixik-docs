## The `keyword-db` Module

The `keyword-db` module takes document input, parses the documents for non-trivial keywords, identifies each of their lemmatized stems, and returns an `SQLite` database with this content.

This overview of the `keyword-db` module is divided into the following sections:

- [Inputs and Outputs of the `keyword-db` Module](#inputs-and-outputs-of-the-keyword-db-module)
- [Available Models in the `keyword-db` Module](#available-models-in-the-keyword-db-module)
- [Model Parameters in the `keyword-db` Module](#model-parameters-in-the-keyword-db-module)
- [A Single-Module Pipeline for the `keyword-db` Module and Local Querying](#a-single-module-pipeline-for-the-keyword-db-module-and-local-querying)
- [The `keyword_search` Method](#the-keyword_search-method)
- [Further Information on `keyword-db` Module IO and Clickability](#further-information-on-keyword-db-module-io-and-clickability)

### Inputs and Outputs of the `keyword-db` Module

The `keyword-db` module accepts document inputs. Acceptable file formats are the following:

- TXT

- PDF (automatically converted to TXT before processing)

- DOCX (automatically converted to TXT before processing)

- PPTX (automatically converted to TXT before processing)

The `keyword-db` module returns an `SQLite` database containing every non-trivial keyword in the document and its lemmatized stem.

### Available Models in the `keyword-db` Module

You use the following model when using the `keyword-db` module:

- `base` - (default) Krixik-made

Use the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method to determine what model you'd like active when you process files through the `keyword-db` module, though note that at this time there is only one option.

### Model Parameters in the `keyword-db` Module

The `keyword-db` module model is not parameterizable. Consequently, should you wish to specify what model you'll use through the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method's [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument, `params` will always be set to an empty dictionary. For example:

```python
# example model selection for keyword-db module in process
modules={'keyword-db': {'model':'base',
                        'params': {}}}
```

### A Single-Module Pipeline for the `keyword-db` Module and Local Querying

Please click [here](../../examples/single_module_pipelines/single_keyword-db.md) to visit the `Pipeline Examples` section of our documentation and review an example of a single-module pipeline for the `keyword-db` module.

Keep in mind that the output of this pipeline will be an `SQLite` database file, which is not human-readable.

This example will also include an overview of how to [locally query](../../examples/single_module_pipelines/single_keyword-db.md#querying-output-databases-locally) your output databases.

### The `keyword_search` Method

Any pipeline containing a `keyword-db` module has access to the [`keyword_search`](../../system/search_methods/keyword_search_method.md) method. This provides you with the convenient ability to effect keyword queries on the created keyword database(s).

### Further Information on `keyword-db` Module IO and Clickability

Please click [here](../../system/convenience_methods/convenience_methods.md) to visit the `Convenience Methods (and More!)` documentation. There you will find two tools to learn more about the `keyword-db` module:

- [View Module Input and Output Examples](../../system/convenience_methods/convenience_methods.md#view-module-input-and-output-examples)

- [View Module Click Data with the `.click_data` Method](../../system/convenience_methods/convenience_methods.md#view-module-click-data-with-the-click_data-method)
