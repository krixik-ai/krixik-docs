## the `.show_tree` method

`show_tree` is a convenience function for visualizing - at your terminal or IDE output - your un-expired pipeline files.  It is designed as a simple analog to the standard unix [tree command](https://www.tecmint.com/linux-tree-command-examples/).

To illustrate its usage we first process several files.


```python
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,
                                  symbolic_directory_path="/my/custom/path",
                                  file_name="file_num_one.txt")   

process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,
                                  symbolic_directory_path="/my/custom/path",
                                  file_name="file_num_two.txt")   

process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,
                                  symbolic_directory_path="/my/custom/path/subpath",
                                  file_name="file_num_three.txt")   
```

Now we can visualize our pipeline process file directory structure using `show_tree`.

`show_tree` takes in a single argument - `symbolic_directory_path`.  You can enter a path or stump (path + wildcard) to see all files and directories at or below the input path.


```python
# show the directory structure of a pipeline process file directory
show_tree_output = pipeline.show_tree(symbolic_directory_path='/*')
```

    /
    └── /my
        └── /custom
            └── /path
                ├── file_num_one.txt
                ├── file_num_two.txt
                └── /subpath
                    └── file_num_three.txt
