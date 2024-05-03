
1.  Tag any cells you want removed / output removed when converted to markdown
    - `remove_output`: tag to remove cell output 
    - `remove_convert`: remove entire cell (input and output)
2.  Clean up your pipelines at the end of each notebook
    - Make sure your notebook ends with a python cell invoking `reset_pipeline` on any pipeline(s) created
3.  Clean up the `data/output` directory - remove everything.  This directory is where all output from demo notebooks is directed so that users can easily see input-output.  If we do not clean it up before each push the data will aggregate.
3.  make sure all notebooks pass tests