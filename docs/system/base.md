## Base pipeline setup

Below we setup a simple one module pipeline using the `parser` module, using the default `sentence` parser.  This parser takes in an input text file and splits into its constituent sentences.


```python
# import custom module creation tools
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# instantiate module
module_1 = Module(module_type="parser")

# create custom pipeline object
custom = CreatePipeline(name='parser-pipeline-1', 
                        module_chain=[module_1])

# pass the custom object to the krixik operator (note you can also do this by passing its config)
pipeline = krixik.load_pipeline(pipeline=custom)
```

We will use this `pipeline` object for illustrative purposes for the remainder of this document.