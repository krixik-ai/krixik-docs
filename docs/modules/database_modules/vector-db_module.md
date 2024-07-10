<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/modules/database_modules/vector-db_module.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## The `vector-db` Module

The `vector-db` module takes as input a NumPy array, indexes its vectors, and returns an indexed [FAISS database](https://github.com/facebookresearch/faiss).

This overview of the `vector-db` module is divided into the following sections:

- [Inputs and Outputs of the `vector-db` Module](#inputs-and-outputs-of-the-vector-db-module)
- [Available Models in the `vector-db` Module](#available-models-in-the-vector-db-module)
- [Model Parameters in the `vector-db` Module](#model-parameters-in-the-vector-db-module)
- [A Single-Module Pipeline for the `vector-db` Module and Local Querying](#a-single-module-pipeline-for-the-vector-db-module-and-local-querying)
- [The `semantic_search` Method](#the-semantic_search-method)
- [Further Information on `vector-db` Module IO and Clickability](#further-information-on-vector-db-module-io-and-clickability)

### Inputs and Outputs of the `vector-db` Module

The `vector-db` module accepts as input NPY files that consist of a single NumPy array. Each row is a vector to be indexed for vector search.

The `vector-db` module returns an indexed vector [FAISS](https://github.com/facebookresearch/faiss) database file.

For an example of what a small sample input file might look like, see the output of the following code:


```python
# examine contents of a small sample input file
import numpy as np

test_file = data_dir + "input/vectors.npy"
np.load(test_file)
```




    array([[0, 1],
           [1, 0],
           [1, 1]], dtype=int64)



### Available Models in the `vector-db` Module

You use the following model when using the `vector-db` module:

- [faiss](https://github.com/facebookresearch/faiss) (default)

Use the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method to determine what model you'd like active when you process files through the `vector-db` module, though note that at this time there is only one option.

### Model Parameters in the `vector-db` Module

The `vector-db` module model is not parameterizable. Consequently, should you wish to specify what model you'll use through the [`process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method's [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument, `params` will always be set to an empty dictionary. For example:

```python
# example model selection for vector-db module in process
modules={'vector-db': {'model':'base',
                       'params': {}}}
```

### A Single-Module Pipeline for the `vector-db` Module and Local Querying

Please click [here](../../examples/single_module_pipelines/single_vector-db.md) to visit the `Pipeline Examples` section of our documentation and review an example of a single-module pipeline for the `vector-db` module.

Keep in mind that the output of this pipeline will be an [FAISS](https://github.com/facebookresearch/faiss) database file, which is not human-readable. Moreover, for this single-module pipeline to work, you'll need to separately have one or more properly formatted NPY files ready for input.

This example will also include an overview of how to [locally query](../../examples/single_module_pipelines/single_vector-db.md#querying-output-databases-locally) your output databases.

### The `semantic_search` Method

Any pipeline containing a `vector-db` module preceded by a [`text-embedder`](../ai_modules/text-embedder_module.md) module has access to the [`semantic_search`](../../system/search_methods/semantic_search_method.md) method. This provides you with the convenient ability to effect semantic queries on the created vector database(s).

### Further Information on `vector-db` Module IO and Clickability

Please click [here](../../system/convenience_methods/convenience_methods.md) to visit the `Convenience Methods (and More!)` documentation. There you will find two tools to learn more about the `vector-db` module:

- [View Module Input and Output Examples](../../system/convenience_methods/convenience_methods.md#view-module-input-and-output-examples)

- [View Module Click Data with the `click_data` Method](../../system/convenience_methods/convenience_methods.md#view-module-click-data-with-the-click_data-method)
