<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/single_module_pipelines/single_keyword-db.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Single-Module Pipeline: `keyword-db`

This document is a walkthrough of how to assemble and use a single-module pipeline that only includes a [`keyword-db`](../../modules/database_modules/keyword-db_module.md) module. It's divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Required Input Format](#required-input-format)
- [Using the Default Model](#using-the-default-model)
- [Using the `.keyword_search` Method](#using-the-keyword_search-method)
- [Querying Output Databases Locally](#querying-output-databases-locally)

### Pipeline Setup

Let's first instantiate a single-module [`keyword-db`](../../modules/database_modules/keyword-db_module.md) pipeline.

We use the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method for this, passing only the [`keyword-db`](../../modules/database_modules/keyword-db_module.md) module name into `module_chain`.


```python
# create a pipeline with a single keyword-db module
pipeline = krixik.create_pipeline(name="single_keyword-db_1", module_chain=["keyword-db"])
```

### Required Input Format

The [`keyword-db`](../../modules/database_modules/keyword-db_module.md) module accepts document inputs. Acceptable file formats are TXT, PDF, DOCX, and PPTX, although the last three formats are automatically converted to TXT before processing.

Let's take a quick look at a valid input file, and then process it:


```python
# examine contents of a valid test input file
with open(data_dir + "input/1984_very_short.txt", "r") as file:
    print(file.read())
```

    It was a bright cold day in April, and the clocks were striking thirteen.
    Winston Smith, his chin nuzzled into his breast in an effort to escape the
    vile wind, slipped quickly through the glass doors of Victory Mansions,
    though not quickly enough to prevent a swirl of gritty dust from entering
    along with him.


### Using the Default Model

Let's process our test input file using the [`keyword-db`](../../modules/database_modules/keyword-db_module.md) module's default (and currently only) [model](../../modules/database_modules/keyword-db_module.md#available-models-in-the-keyword-db-module): `base`.

Given that this is the default model, we need not specify model selection through the optional [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file with the default model
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_very_short.txt",  # the initial local filepath where the input file is stored
    local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # wait for process to complete before returning IDE control to user
    verbose=False,
)  # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_keyword-db_1",
      "request_id": "f9055422-6212-454e-bd9e-e863ca37e853",
      "file_id": "530270a9-0430-4c7d-98d0-a858efa7c879",
      "message": "SUCCESS - output fetched for file_id 530270a9-0430-4c7d-98d0-a858efa7c879.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/530270a9-0430-4c7d-98d0-a858efa7c879.db"
      ]
    }


Because the output of this particular module-model pair is an `SQLlite` database file, `process_output` is "null". However, the output file has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.

### Using the `keyword_search` method

Any pipeline containing a [`keyword-db`](../../modules/database_modules/keyword-db_module.md) module has access to the [`.keyword_search`](../../system/search_methods/keyword_search_method.md) method. This provides you with the convenient ability to effect keyword queries on the created keyword database(s).

### Querying Output Databases Locally

In addition to what's provided by the [`.keyword_search`](../../system/search_methods/keyword_search_method.md) method, you can **locally** perform queries on the generated keyword database whose location is indicated in `process_output_files`.

Below is a simple function for locally performing single keyword queries on the above-outputted database:


```python
import sqlite3


def query_db(query_keyword: str, keyword_db_local_file_name: str) -> list:
    # load keyword_db
    keyword_db = sqlite3.connect(keyword_db_local_file_name)
    keyword_cursor = keyword_db.cursor()

    # create query pattern
    query_pattern = f"""
    SELECT
        original_keyword,
        line_number,
        keyword_number
    FROM
        keyword_search
    where original_keyword="{query_keyword}"
    GROUP BY
        original_keyword,
        line_number,
        keyword_number
    ORDER BY
        line_number,
        keyword_number
    """

    # excute query
    keyword_cursor.execute(query_pattern)

    # Fetch and process the results
    rows = keyword_cursor.fetchall()
    return rows
```

We query our small database using a single keyword query with the function above. The results are printed below:


```python
# query database
query = "cold"
query_db(query, process_output["process_output_files"][0])
```




    [('cold', 1, 5)]


