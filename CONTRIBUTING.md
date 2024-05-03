
1.  Tag any cells you want removed / output removed when converted to markdown
    - `remove_output`: tag to remove cell output 
    - `remove_convert`: remove entire cell (input and output)
2.  Clean up your pipelines at the end of each notebook
    - Make sure your notebook ends with a python cell invoking `reset_pipeline` on any pipeline(s) created

2.  make sure all notebooks pass tests