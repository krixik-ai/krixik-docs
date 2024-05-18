## The `.show_tree` Method

The `.show_tree` method allows you to visualize—at your terminal or IDE output—all files currently in your pipeline.  It is designed as a simple analog to the standard UNIX [tree command](https://www.tecmint.com/linux-tree-command-examples/).

This overview of the `.update` method is divided into the following sections:

- [.show_tree Method Arguments](#.show_tree-method-arguments)
- [.show_tree Method Example](#.show_tree-method-example)
- [The Wildcard Operator * and the Global Root](#the-wildcard-operator-*-and-the-global-root)

### `.show_tree` Method Arguments

The `.show_tree` method takes a single (required) argument:

- `symbolic_directory_path` (str) - The `file_id` of the processed file whose record you wish to entirely delete from the Krixik system.

### `.show_tree` Method Example

For this document's example we will use a pipeline consisting of a single [`parser`](../../modules/ai_model_modules/parser_module.md) module.  We use the [`.create_pipeline`](../pipeline_creation/create_pipeline.md) method to instantiate the pipeline, and then [`.process`](../parameters_processing_files_through_pipelines/process_method.md) a few files through it. Note the `symbolic_directory_path` structure we create:


```python
# create an example pipeline with a single module

pipeline_1 = krixik.create_pipeline(name="show_tree_method_1_parser",
                                    module_chain=["parser"])

# now process some files through the pipeline

process_output_1 = pipeline_1.process(local_file_path="../../data/input/Frankenstein.txt", # the initial local filepath where the input JSON file is stored
                                      expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                      verbose=False,  # do not display process update printouts upon running code
                                      symbolic_directory_path="/lit/novels/19th-century",
                                      file_name="Frankenstein.txt")

process_output_2 = pipeline_1.process(local_file_path="../../data/input/Pride and Prejudice.txt", # the initial local filepath where the input JSON file is stored
                                      expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                      verbose=False,  # do not display process update printouts upon running code
                                      symbolic_directory_path="/lit/novels/19th-century",
                                      file_name="Pride and Prejudice.txt")

process_output_3 = pipeline_1.process(local_file_path="../../data/input/Moby Dick.txt", # the initial local filepath where the input JSON file is stored
                                      expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                      verbose=False,  # do not display process update printouts upon running code
                                      symbolic_directory_path="/lit/novels/19th-century/adventure",
                                      file_name="Moby Dick.txt")

process_output_4 = pipeline_1.process(local_file_path="../../data/input/Little Women.txt", # the initial local filepath where the input JSON file is stored
                                      expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True,  # do not wait for process to complete before returning IDE control to user
                                      verbose=False,  # do not display process update printouts upon running code
                                      symbolic_directory_path="/lit/novels/19th-century/bildungsroman",
                                      file_name="Little Women.txt")
```

Now you can visualize your pipeline's symbolic directory structure by using `show_tree`.

This example will leverage the "global root" wildcard `symbolic_directory_path`, which will be explained momentarily.


```python
# show the directory structure of a pipeline

show_tree_output_1 = pipeline_1.show_tree(symbolic_directory_path="/*")
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

### The Wildcard Operator * and the Global Root

As in the [`.list`](../file_system/list_method.md) method, you can use the wildcard operator * in the `symbolic_directory_path` argument for the `.show_tree` method.

The wildcard operator * can be used as a suffix in the `.show_tree` method if you wish to show the tree structure beneath a certain directory. Syntax might look like this:

```python
# symbolic_directory_path use of wildcard operator *
symbolic_directory_path='/home/files/studies'
```

Using this `symbolic_directory_path` in `.show_tree` would generate a visualization of the directory structure under `/home/files/studies`.

The maxium expression of using the wildcard operator in a `symbolic_directory_path` is what we call "the global root". It's simply a forward slash and a wildcard operator *, includes every single file in your pipeline, and looks like this:

```python
# example of the global root
symbolic_directory_path='/*'
```

As seen in the above code output, using the global root with the `.show_tree` method returns a visualization of your entire pipeline's directory structure.
