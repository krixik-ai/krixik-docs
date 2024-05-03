## Building your first custom krixik pipeline

With krixik *modules* are the building blocks of *pipelines*.  *Moduels* - consisting of both AI models and supporting functions.  

We start off this Section by describing the necessary steps to get started building pipelines with modules.  Advanced details on modules may be found in Section 2.

Note: throughout we will use the following small function to print dictionaries and json files more prettily to cell output.


```python
# print dictionaries / json nicely in notebooks / markdown
import json
def json_print(data):
    print(json.dumps(data, indent=2))
```