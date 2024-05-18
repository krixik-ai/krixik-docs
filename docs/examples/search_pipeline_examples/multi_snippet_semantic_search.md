## Multi-Module Pipeline: Basic Semantic Search

This document details a modular pipeline that takes in a series of text snippets in a JSON file and enables [`semantic search`](../system/search_methods/semantic_search_method.md) on them.

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)
- [Performing Semantic Search](#performing-semantic-search)

### Pipeline Setup

To achieve what we've described above, let's set up a pipeline sequentially consisting of the following modules:

- A [`text-embedder`](../modules/ai_model_modules/text-embedder_module.md) module.

- A [`vector-db`](../modules/database_modules/vector-db_module.md) module.

We do this by leveraging the [`.create_pipeline`](../system/pipeline_creation/create_pipeline.md) method, as follows:


```python
# create a pipeline as detailed above

pipeline_1 = krixik.create_pipeline(name="multi_snippets_semantic_search",
                                    module_chain=["text-embedder",
                                                  "vector-db"])
```

### Processing an Input File

Lets take a quick look at a test file before processing.

The input format to this pipeline is a JSON file (given that it's the input format of its [first module](../modules/ai_model_modules/text-embedder_module.md)). JSON input must always be in a [specific format](../system/parameters_processing_files_through_pipelines/JSON_input_format.md), or the [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) method will not work.


```python
# examine contents of input file

with open("../../../data/input/1984_snippets.json", "r") as file:
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


We will use the default models for every module in the pipeline, so the [`modules`](../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) method doesn't need to be leveraged.


```python
# process the file through the pipeline, as described above

process_output_1 = pipeline_1.process(local_file_path = "../../../data/input/1984_short.txt", # the initial local filepath where the input file is stored
                                      local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                      expire_time=60*30, # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True, # wait for process to complete before returning IDE control to user
                                      verbose=False) # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a [FAISS](https://github.com/facebookresearch/faiss) database file, the process output is null. However, the output file has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process

print(json.dumps(process_output_1, indent=2))
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


### Performing Semantic Search

Krixik's [`.semantic_search`](../system/search_methods/semantic_search_method.md) method enables semantic search on documents processed through certain pipelines. Given that the [`.semantic_search`](../system/search_methods/semantic_search_method.md) method both [embeds](../modules/ai_model_modules/text-embedder_module.md) the query and performs the search, it can only be used with pipelines containing both a [`text-embedder`](../modules/ai_model_modules/text-embedder_module.md) module and a [`vector-db`](../modules/database_modules/vector-db_module.md) module in immediate succession.

Since our pipeline satisfies this condition, it has access to the [`.semantic_search`](../system/search_methods/semantic_search_method.md) method. Let's use it to query our text with natural language, as shown below:


```python
# perform semantic_search over the file in the pipeline

semantic_output_1 = pipeline_1.semantic_search(query="it was cold night",
                                               file_ids=[process_output_1["file_id"]])

# nicely print the output of this process

print(json.dumps(semantic_output_1, indent=2))
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

