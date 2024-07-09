<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/modules/database_modules/vector-db_module.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>


```python
import os
import sys
import json
import importlib
from pathlib import Path

# demo setup - including secrets instantiation, requirements installation, and path setting
if os.getenv("COLAB_RELEASE_TAG"):
    # if running this notebook in collab - make sure to enter your secrets
    MY_API_KEY = "YOUR_API_KEY_HERE"
    MY_API_URL = "YOUR_API_URL_HERE"

    # if running this notebook on collab - install requirements and pull required subdirectories
    # install krixik python client
    !pip install krixik

    # install github clone - allows for easy cloning of subdirectories from docs repo: https://github.com/krixik-ai/krixik-docs
    !pip install github-clone

    # clone datasets
    if not Path("data").is_dir():
        !ghclone https://github.com/krixik-ai/krixik-docs/tree/main/data
    else:
        print("docs datasets already cloned!")

    # define data dir
    data_dir = "./data/"

    # create output dir
    from pathlib import Path

    Path(data_dir + "/output").mkdir(parents=True, exist_ok=True)

    # pull utilities
    if not Path("utilities").is_dir():
        !ghclone https://github.com/krixik-ai/krixik-docs/tree/main/utilities
    else:
        print("docs utilities already cloned!")
else:
    # if running local pull of docs - set paths relative to local docs structure
    # import utilities
    sys.path.append("../../../")

    # define data_dir
    data_dir = "../../../data/"

    # if running this notebook locally from krixik docs repo - load secrets from a .env placed at the base of the docs repo
    from dotenv import load_dotenv

    load_dotenv("../../../.env")

    MY_API_KEY = os.getenv("MY_API_KEY")
    MY_API_URL = os.getenv("MY_API_URL")


# load in reset
reset = importlib.import_module("utilities.reset")
reset_pipeline = reset.reset_pipeline


# import krixik and initialize it with your personal secrets
from krixik import krixik

krixik.init(api_key=MY_API_KEY, api_url=MY_API_URL)
```

    SUCCESS: You are now authenticated.


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
