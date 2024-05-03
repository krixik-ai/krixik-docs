## Modules - advanced details

This section contains advanced topics on module usage.  This includes the discussion of additional module data properties - `click_data` and `_example`.


```python
from krixik.pipeline_builder.module import Module

# create a few modules
module_1 = Module(module_type='transcribe')
module_2 = Module(module_type='text-embedder')
module_3 = Module(module_type="vector-db")
module_4 = Module(module_type="parser")
```