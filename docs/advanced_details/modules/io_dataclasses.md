### Examining input/output dataclasses

To get a deeper understanding of each module's input/output data structure you can examine its associated dataclasses.

As an example the first module in our `text_search_pipeline` pipeline is `parser`.  The io dataclasss for this module is shown below.  Your input must match this class requirement in order for your input test to pass, and in order for your pipeline to function propertly.


```python
# load in io.py from krixik.modules.parser
from krixik.modules.parser import io
import inspect
print(inspect.getsource(io.InputStructure))
```

    @dataclass
    class InputStructure:
        format: Literal["text"] = "text"
        filename: str = "input_text.txt"
        process_key: None = None
    
        @property
        def data_example(self):
            return "sample text looks like this."
    
        @property
        def process_type(self):
            return (
                str(self.__annotations__[self.process_key])
                if self.process_key is not None
                else None
            )
    