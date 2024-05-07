## A simple semantic search pipeline

This document reviews a simple semantic search pipeline that can be used to make any input text semantically-searchable.


- [pipeline setup](#pipeline-setup)
- [processing an input file](#processing-an-input-file)



```python
# import utilities
import sys 
import json
sys.path.append('../../../')
import importlib
reset = importlib.import_module("utilities.reset")
reset_pipeline = reset.reset_pipeline

# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os
load_dotenv("../../.env")
MY_API_KEY = os.getenv('MY_API_KEY')
MY_API_URL = os.getenv('MY_API_URL')

# import krixik and initialize it with your personal secrets
from krixik import krixik
krixik.init(api_key = MY_API_KEY, 
            api_url = MY_API_URL)
```

    SUCCESS: You are now authenticated.


## Pipeline setup

Below we setup a pipeline consisting of a [`parser`](modules/parser.md), [`text-embedder`](modules/text-embedder.md), and [`vector-db`](modules/vector-db.md) modules.  This will allow us to process input files and make them semantically searchable.

We do this by passing the module names to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a pipeline with a multi module pipeline
pipeline = krixik.create_pipeline(name="examples-text-search-semantic-pipeline",
                                  module_chain=["parser", "text-embedder", "vector-db"])
```

This pipeline's available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).


```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```

## Processing an input file

Lets take a quick look at a short test file before processing.


```python
# examine contents of input file
test_file = "../../../data/input/1984_short.txt"
with open(test_file, "r") as file:
    print(file.read())
    
```

    It was a bright cold day in April, and the clocks were striking thirteen.
    Winston Smith, his chin nuzzled into his breast in an effort to escape the
    vile wind, slipped quickly through the glass doors of Victory Mansions,
    though not quickly enough to prevent a swirl of gritty dust from entering
    along with him.
    
    The hallway smelt of boiled cabbage and old rag mats. At one end of it a
    coloured poster, too large for indoor display, had been tacked to the wall.
    It depicted simply an enormous face, more than a metre wide: the face of a
    man of about forty-five, with a heavy black moustache and ruggedly handsome
    features. Winston made for the stairs. It was no use trying the lift. Even
    at the best of times it was seldom working, and at present the electric
    current was cut off during daylight hours. It was part of the economy drive
    in preparation for Hate Week. The flat was seven flights up, and Winston,
    who was thirty-nine and had a varicose ulcer above his right ankle, went
    slowly, resting several times on the way. On each landing, opposite the
    lift-shaft, the poster with the enormous face gazed from the wall. It was
    one of those pictures which are so contrived that the eyes follow you about
    when you move. BIG BROTHER IS WATCHING YOU, the caption beneath it ran.
    
    Inside the flat a fruity voice was reading out a list of figures which had
    something to do with the production of pig-iron. The voice came from an
    oblong metal plaque like a dulled mirror which formed part of the surface
    of the right-hand wall. Winston turned a switch and the voice sank
    somewhat, though the words were still distinguishable. The instrument
    (the telescreen, it was called) could be dimmed, but there was no way of
    shutting it off completely. He moved over to the window: a smallish, frail
    figure, the meagreness of his body merely emphasized by the blue overalls
    which were the uniform of the party. His hair was very fair, his face
    naturally sanguine, his skin roughened by coarse soap and blunt razor
    blades and the cold of the winter that had just ended.
    
    Outside, even through the shut window-pane, the world looked cold. Down in
    the street little eddies of wind were whirling dust and torn paper into
    spirals, and though the sun was shining and the sky a harsh blue, there
    seemed to be no colour in anything, except the posters that were plastered
    everywhere. The black-moustachio'd face gazed down from every commanding
    corner. There was one on the house-front immediately opposite. BIG BROTHER
    IS WATCHING YOU, the caption said, while the dark eyes looked deep into
    Winston's own. Down at street level another poster, torn at one corner,
    flapped fitfully in the wind, alternately covering and uncovering the
    single word INGSOC. In the far distance a helicopter skimmed down between
    the roofs, hovered for an instant like a bluebottle, and darted away again
    with a curving flight. It was the police patrol, snooping into people's
    windows. The patrols did not matter, however. Only the Thought Police
    mattered.
    
    Behind Winston's back the voice from the telescreen was still babbling away
    about pig-iron and the overfulfilment of the Ninth Three-Year Plan. The
    telescreen received and transmitted simultaneously. Any sound that Winston
    made, above the level of a very low whisper, would be picked up by it,
    moreover, so long as he remained within the field of vision which the metal
    plaque commanded, he could be seen as well as heard. There was of course
    no way of knowing whether you were being watched at any given moment. How
    often, or on what system, the Thought Police plugged in on any individual
    wire was guesswork. It was even conceivable that they watched everybody all
    the time. But at any rate they could plug in your wire whenever they wanted
    to. You had to live--did live, from habit that became instinct--in the
    assumption that every sound you made was overheard, and, except in
    darkness, every movement scrutinized.
    
    Winston kept his back turned to the telescreen. It was safer; though, as he
    well knew, even a back can be revealing. A kilometre away the Ministry of
    Truth, his place of work, towered vast and white above the grimy landscape.
    This, he thought with a sort of vague distaste--this was London, chief
    city of Airstrip One, itself the third most populous of the provinces of
    Oceania. He tried to squeeze out some childhood memory that should tell him
    whether London had always been quite like this. Were there always these
    vistas of rotting nineteenth-century houses, their sides shored up with
    baulks of timber, their windows patched with cardboard and their roofs
    with corrugated iron, their crazy garden walls sagging in all directions?
    And the bombed sites where the plaster dust swirled in the air and the
    willow-herb straggled over the heaps of rubble; and the places where the
    bombs had cleared a larger patch and there had sprung up sordid colonies
    of wooden dwellings like chicken-houses? But it was no use, he could not
    remember: nothing remained of his childhood except a series of bright-lit
    tableaux occurring against no background and mostly unintelligible.
    
    The Ministry of Truth--Minitrue, in Newspeak [Newspeak was the official
    language of Oceania. For an account of its structure and etymology see
    Appendix.]--was startlingly different from any other object in sight. It
    was an enormous pyramidal structure of glittering white concrete, soaring
    up, terrace after terrace, 300 metres into the air. From where Winston
    stood it was just possible to read, picked out on its white face in
    elegant lettering, the three slogans of the Party:
    
    
      WAR IS PEACE
      FREEDOM IS SLAVERY
      IGNORANCE IS STRENGTH


Below we [process](system/process.md) the input through our pipeline using the default model for each of our three modules.


```python
# define path to an input file from examples directory
test_file = "../../../data/input/1984_short.txt"

# process a file through the pipeline
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory="../../../data/output",  # save output in current directory
                                  expire_time=60*10,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,     # wait for process to complete before regaining ide
                                  verbose=False)             # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is a faiss database, the process output is provided in this object is null.  However the file itself has been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "examples-text-search-semantic-pipeline",
      "request_id": "262563c3-6841-4aa8-8694-01c056fb4ce8",
      "file_id": "b20fa17b-1df9-4185-94c9-ae17ac187822",
      "message": "SUCCESS - output fetched for file_id b20fa17b-1df9-4185-94c9-ae17ac187822.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/b20fa17b-1df9-4185-94c9-ae17ac187822.faiss"
      ]
    }


## Using the `semantic_search` method

krixik's [`semantic_search` method](system/semantic_search.md) is a convenience function for both embedding and querying - and so can only be used with pipelines containing both `text-embedder` and `vector-db` modules in succession.  Since our pipeline here satisfies this condition, it has access to the `semantic_search` method.

Now we can query our text with natural language as shown below.


```python
# perform semantic_search over the input file
semantic_output = pipeline.semantic_search(
    query="it was cold night", file_ids=[process_output["file_id"]]
)

# nicely print the output of this process
print(json.dumps(semantic_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "57a797f5-bc77-4774-a2b0-b5f13007b356",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "b20fa17b-1df9-4185-94c9-ae17ac187822",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_toyzuamynf.txt",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 50,
            "created_at": "2024-05-07 18:30:32",
            "last_updated": "2024-05-07 18:30:32"
          },
          "search_results": [
            {
              "snippet": "Outside, even through the shut window-pane, the world looked cold.",
              "line_numbers": [
                32,
                33
              ],
              "distance": 0.232
            },
            {
              "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
              "line_numbers": [
                1
              ],
              "distance": 0.236
            },
            {
              "snippet": "His hair was very fair, his face\nnaturally sanguine, his skin roughened by coarse soap and blunt razor\nblades and the cold of the winter that had just ended.",
              "line_numbers": [
                29,
                30,
                31
              ],
              "distance": 0.324
            },
            {
              "snippet": "Down in\nthe street little eddies of wind were whirling dust and torn paper into\nspirals, and though the sun was shining and the sky a harsh blue, there\nseemed to be no colour in anything, except the posters that were plastered\neverywhere.",
              "line_numbers": [
                33,
                34,
                35,
                36,
                37
              ],
              "distance": 0.33
            },
            {
              "snippet": "It was the police patrol, snooping into people's\nwindows.",
              "line_numbers": [
                44,
                45
              ],
              "distance": 0.352
            }
          ]
        }
      ]
    }



```python
# delete all processed datapoints belonging to this pipeline
reset_pipeline(pipeline)
```
