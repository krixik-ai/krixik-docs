### Creating modules

Lets create a few instances of the available modules shown above.


```python
from krixik.pipeline_builder.module import Module

# create a few modules
module_1 = Module(module_type='transcribe')
module_2 = Module(module_type='text-embedder')
module_3 = Module(module_type="vector-db")
module_4 = Module(module_type="parser")
```

Once instantiated we can examine the metadata of these instances or connect them into a pipeline.