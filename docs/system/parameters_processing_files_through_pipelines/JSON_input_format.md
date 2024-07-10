## JSON Input Format

### JSON Format Details

JSON input files into pipelines that begin with JSON-input modules (e.g. the [`translate module`](../../modules/ai_modules/translate_module.md)) must be in a very specific format for the [`process`](../parameters_processing_files_through_pipelines/process_method.md) method to work. If the file doesn't follow this format, the [`process`](../parameters_processing_files_through_pipelines/process_method.md) attempt will fail.

A description of the format follows:

- The macro container in the JSON file must be a single list.

- The list will hold a series of dictionaries.

- Each text block that is to be processed must be in a separate dictionary. For instance, if you want to process 20 snippets of text, the list should hold 20 dictionaries.

- In each dictionary, the text you wish Krixik to pass on to a following module (assuming you click that module into any other) sits as the value of a key-value pair. The key of this pair must be the string `"snippet"`. If it is anything else, it will fail or be ignored.

- Any key-value pair in a dictionary whose key is not `"snippet"` will be ignored.

- If more than one key-value pair has `"snippet"` for a key, all but one of them will be ignored.

### A JSON Input Example

Here's an example of the above in action. The following list is what the contents of a JSON file should look like if you wanted to separately submit the first two sentences of George Orwell's <u>1984</u> to a Krixik pipeline:


```python
# example JSON content, two separate blocks of text
[
    {"snippet": "It was a bright cold day in April, and the clocks were striking thirteen.", "line_numbers": [1]},
    {
        "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him.",
        "line_numbers": [2, 3, 4, 5],
    },
]
```

### Creating the JSON File

We recommend using JSON functionality to create your JSON files. Directly creating your JSON files may lead to error. The following code is an example of how to do this (note the Python variable we introduced at the top):


```python
# creating and locally saving a JSON file
my_data = [
    {"snippet": "It was a bright cold day in April, and the clocks were striking thirteen.", "line_numbers": [1]},
    {
        "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him.",
        "line_numbers": [2, 3, 4, 5],
    },
]

import json

with open("demo_file_1.json", "w") as f:
    json.dump(my_data, f)
```

The above will locally create a properly formatted JSON file named `demo_file_1.json` (with the contents above) in your current working directory.
