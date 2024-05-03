### Viewing a module's `click_data`

The module property `click_data` displays all the basic data required to know which other modules it can be "clicked" into in a pipeline.  This is precisely what data is referenced "under the hood" of krixik when you build a pipeline using the `pipeline` api.

First there's the module's input / output data format.  A module like  `transcribe` takes in `audio` and outputs `json`, while the `text-embedder` takes in `json` and outputs `.npy`.  

Checking that the *output* format of a module matches the *input* format of another module is the *first* of two steps in determining if two modules can be clicked together.  If the output format of "module A"  matches the input format of "module B" you'll likely be able to connect "module A" --> "module B" in a pipeline.

The *second* step to determine module click-ability is to make sure the input/output  `process_type`'s match.  A module might input a `json` format, but only *process* on certain key-value pairs of it.  

Checking this aligment of `process_type` guarantees modules can be connected.

Lets take a look at the `click_data` of two modules and discuss what it says about their "click-ability".


```python
# examine a module's "click-ability" data by using the click_data property
# print a dictionary nicely in an ide or notebook
json_print(module_2.click_data)
json_print(module_3.click_data)
```

    {
      "module_name": "text-embedder",
      "input_format": "json",
      "output_format": "npy",
      "input_process_key": "snippet",
      "input_process_type": "<class 'str'>",
      "output_process_key": "data",
      "output_process_type": "<class 'numpy.ndarray'>"
    }
    {
      "module_name": "vector-db",
      "input_format": "npy",
      "output_format": "faiss",
      "input_process_key": "data",
      "input_process_type": "<class 'numpy.ndarray'>",
      "output_process_key": null,
      "output_process_type": null
    }


This data suggests that we can "click" the modules together like this:

`text-embedder` -> `vector-db`

but *not* like this

 `vector-db` -> `text-embedder`

The first module connection (`text-embedder` -> `vector-db`) will work since - from the `click_data` of both modules - we can see that 

- `text-embedder` output_format (`npy`) == `vector-db` input_format (`npy`), and 
- `text-embedder` output_process_type (`<class 'numpy.ndarray'>`) == `vector-db` input_process_type (`<class 'numpy.ndarray'>`)


The latter connection ( `vector-db` -> `text-embedder`) will not work since we can see from the same data 

- `vector-db` output_format (`faiss`) != `text-embedder` input_format (`json`)

