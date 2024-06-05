<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/file_system/show_tree_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## The `show_tree` Method

The `show_tree` method allows you to visualize—at your terminal or IDE output—all files currently in your pipeline.  It is designed as a simple analog to the standard UNIX [tree command](https://www.tecmint.com/linux-tree-command-examples/).

This overview of the `show_tree` method is divided into the following sections:

- [show_tree Method Arguments](#show_tree-method-arguments)
- [show_tree Method Example](#show_tree-method-example)
- [The Wildcard Operator and the Global Root](#the-wildcard-operator-and-the-global-root)

### `show_tree` Method Arguments

The `show_tree` method takes a single (required) argument:

- `symbolic_directory_path` (str) - The `file_id` of the processed file whose record you wish to entirely delete from the Krixik system.

### `show_tree` Method Example

For this document's example we will use a pipeline consisting of a single [`parser`](../../modules/support_function_modules/parser_module.md) module.  We use the [`.create_pipeline`](../pipeline_creation/create_pipeline.md) method to instantiate the pipeline, and then [`process`](../parameters_processing_files_through_pipelines/process_method.md) a few files through it. Note the `symbolic_directory_path` structure we create:


```python
# create an example pipeline with a single module
pipeline = krixik.create_pipeline(name="show_tree_method_1_parser", module_chain=["parser"])

# define path to an input file from examples directory
test_file = data_dir + "input/1984_very_short.txt"

# process short input file with various metdata
process_output = pipeline.process(
    local_file_path=test_file,
    local_save_directory=data_dir + "output",  # save output repo data output subdir
    expire_time=60 * 30,  # set all process data to expire in 30 minutes
    wait_for_process=True,  # wait for process to complete before regaining ide
    verbose=False,
    symbolic_directory_path="/my/custom/path",
    file_name="file_num_one.txt",
)

process_output = pipeline.process(
    local_file_path=test_file,
    local_save_directory=data_dir + "output",  # save output repo data output subdir
    expire_time=60 * 30,  # set all process data to expire in 30 minutes
    wait_for_process=True,  # wait for process to complete before regaining ide
    verbose=False,
    symbolic_directory_path="/my/custom/path",
    file_name="file_num_two.txt",
)

process_output = pipeline.process(
    local_file_path=test_file,
    local_save_directory=data_dir + "output",  # save output repo data output subdir
    expire_time=60 * 30,  # set all process data to expire in 30 minutes
    wait_for_process=True,  # wait for process to complete before regaining ide
    verbose=False,
    symbolic_directory_path="/my/custom/path/subpath",
    file_name="file_num_three.txt",
)
```

Now you can visualize your pipeline's symbolic directory structure by using `show_tree`.

This example will leverage the "global root" wildcard `symbolic_directory_path`, which will be explained momentarily.


```python
# show the directory structure of a pipeline
show_tree_output = pipeline.show_tree(symbolic_directory_path="/*")
```

    /
    └── /my
        └── /custom
            └── /path
                ├── file_num_one.txt
                ├── file_num_two.txt
                └── /subpath
                    └── file_num_three.txt


Note that directory names are preceded by a forward slash (`/`) character and file names are not. This allows you to easily differentiate between them.

### The Wildcard Operator and the Global Root

The wildcard operator is the asterisk: *

As in the [`list`](list_method.md) method, the [`semantic_search`](../search_methods/semantic_search_method.md) method and the [`keyword_search`](../search_methods/keyword_search_method.md) method you can use the wildcard operator * in the `symbolic_directory_path` argument for the `show_tree` method.

The wildcard operator * can be used as a suffix in the `show_tree` method if you wish to show the tree structure beneath a certain directory. Syntax might look like this:

```python
# symbolic_directory_path use of wildcard operator *
symbolic_directory_path='/home/files/studies'
```

Using this `symbolic_directory_path` in `show_tree` would generate a visualization of the directory structure under `/home/files/studies`.

The maxium expression of using the wildcard operator in a `symbolic_directory_path` is what we call "the global root". It's simply a forward slash and a wildcard operator *, includes every single file in your pipeline, and looks like this:

```python
# example of the global root
symbolic_directory_path='/*'
```

As seen in the above code output, using the global root with the `show_tree` method returns a visualization of your entire pipeline's directory structure.
