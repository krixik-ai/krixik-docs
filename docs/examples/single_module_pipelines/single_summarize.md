<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/single_module_pipelines/single_summarize.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Single-Module Pipeline: `summarize`

This document is a walkthrough of how to assemble and use a single-module pipeline that only includes a [`summarize`](../../modules/ai_modules/summarize_module.md) module. It's divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Required Input Format](#required-input-format)
- [Using the Default Model](#using-the-default-model)
- [Using a Non-Default Model](#using-a-non-default-model)
- [Recursive Summarization](#recursive-summarization)

### Pipeline Setup

Let's first instantiate a single-module [`summarize`](../../modules/ai_modules/summarize_module.md) pipeline.

We use the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method for this, passing only the [`summarize`](../../modules/ai_modules/summarize_module.md) module name into `module_chain`.


```python
# create a pipeline with a single sentiment module
pipeline = krixik.create_pipeline(name="single_summarize_1", module_chain=["summarize"])
```

### Required Input Format

The [`summarize`](../../modules/ai_modules/summarize_module.md) module accepts document inputs. Acceptable file formats are TXT, PDF, DOCX, and PPTX, although the last three formats are automatically converted to TXT before processing.

Let's take a quick look at a valid input file, and then process it:


```python
# examine contents of a valid test input file
with open(data_dir + "input/1984_short.txt", "r") as file:
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


### Using the Default Model

Let's process our test input file using the [`summarize`](../../modules/ai_modules/summarize_module.md) module's [default model](../../modules/ai_modules/summarize_module.md#available-models-in-the-summarize-module): [`bart-large-cnn`](https://huggingface.co/facebook/bart-large-cnn).

Given that this is the default model, we need not specify model selection through the optional [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument in the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file with the default model
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_short.txt",  # the initial local filepath where the input file is stored
    local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # wait for process to complete before returning IDE control to user
    verbose=False,
)  # do not display process update printouts upon running code
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

The output file itself has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_summarize_1",
      "request_id": "21af82dc-c558-4d7d-b819-b97b91308994",
      "file_id": "718948f7-685a-4e8e-b610-254b454897ce",
      "message": "SUCCESS - output fetched for file_id 718948f7-685a-4e8e-b610-254b454897ce.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/718948f7-685a-4e8e-b610-254b454897ce.txt"
      ]
    }


To confirm that everything went as it should have, let's load in the text file output from `process_output_files`:


```python
# load in process output from file
with open(process_output["process_output_files"][0], "r") as file:
    print(file.read())
```

    Winston Smith walked through the glass doors of Victory Mansions. The hallway
    smelt of boiled cabbage and old rag mats. At one end of
    it it acoloured poster, too large for indoor display, had been tacked
    to the wall. It depicted simply an enormous face, more than a
    metre wide. Winston made for the stairs.
    
    Inside the flat a fruity voice was reading out a list of
    figures which had something to do with pig-iron. Winston turned a switch
    and the voice sank somewhat, though the words were still distinguishable. He
    moved over to the window: a smallish, frail figure, the meagreness of
    his body merely emphasized by the blue overalls which were the uniform
    of the party.
    
    Winston kept his back turned to the telescreen. It was safer; though,
    as he well knew, even a back can be revealing. A kilometre
    away the Ministry of Truth, his place of work, towered vast and
    white above the grimy landscape. Winston tried to squeeze out some childhood
    memory that should tell him whether London had always been quite like
    this.
    
    The Ministry of Truth--Minitrue, in Newspeak [Newspeak was the officiallanguage of Oceania]--was
    startlingly different from any other object in sight. It was an enormous
    pyramidal structure of glittering white concrete, soaring 300 metres into the air.


### Using a Non-Default Model

To use a [non-default model](../../modules/ai_modules/summarize_module.md#available-models-in-the-summarize-module) like [`text-summarization`](https://huggingface.co/Falconsai/text_summarization), we must enter it explicitly through the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument when invoking the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file with a non-default model
process_output_nd = pipeline.process(
    local_file_path=data_dir + "input/1984_short.txt",  # the initial local filepath where the input file is stored
    local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # wait for process to complete before returning IDE control to user
    verbose=False,  # do not display process update printouts upon running code
    modules={"summarize": {"model": "text-summarization"}},
)  # specify a non-default model for this process
```

We can view the newly generated summary by loading in the output file, as below.

The offset punctuation seen in this summary is an artifact of the model, as seen in the [model card](https://huggingface.co/Falconsai/text_summarization) on Hugging Face.


```python
# load in process output from file
with open(process_output_nd["process_output_files"][0], "r") as file:
    print(file.read())
```

    Winston Smith, his chin nuzzled into his breast in an effort to
    escape the vile wind, slipped quickly through the glass doors of Victory
    Mansions . At one end of it a coloured poster, too large
    for indoor display, had been tacked to the wall . It was
    part of the economy drive in preparation for Hate Week . The
    flat was seven flights up, and Winston went slowly, resting several times
    on the way .
    
    Winston turned a switch and the voice sank somewhat, though the words
    were still distinguishable . The instrument (the telescreen, it was called) could
    be dimmed, but there was no way of shutting it off completely
    . He moved over to the window: a smallish, frail figure, the
    meagreness of his body merely emphasized by the blue overalls which were
    the uniform of the party . Outside, even through the shut window-pane,
    the world looked cold .
    
    There was no way of knowing whether you were being watched at
    any given moment . How often, or on what system, the Thought
    Police plugged in on any individual wire was guesswork . You had
    to live, from habit that became instinct--in the assumption that every sound
    you made was overheard, and, except in darkness, every movement scrutinized .
    
    The Ministry of Truth--Minitrue, in Newspeak, was the official language of Oceania
    . It was an enormous pyramidal structure of glittering white concrete, soaring
    up, terrace after terrace, 300 metres into the air . From where
    Winston stood it was just possible to read, picked out on its
    white face in elegant lettering .


### Recursive Summarization

If the result of summarizing once is not concise enough for your needs, there's a neat trick you can leverage.

One of the most practical ways to achieve a shorter (perhaps more abstract, but still representative) summary is to apply summarization *recursively*. In other words, you feed the new summary through a [`summarize`](../../modules/ai_modules/summarize_module.md) module again, thus producing a briefer summary. Let's do it manually.

To feed the <u>first</u> summarization generated above back into the [`summarize`](../../modules/ai_modules/summarize_module.md) module, we essentially repeat what we did above, but with a slight difference: the file we feed in is the summary output of that first summarization.


```python
# assign the summary generated above to a variable for easy reference
first_summary = process_output["process_output_files"][0]

# process this summary through the pipeline
process_output = pipeline.process(
    local_file_path=first_summary,  # feed back into the pipeline the earlier-generated summary
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,
    wait_for_process=True,
    verbose=False,
)
```

Once this [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) run finishes we receive our even-shorter summary as an output file.

Let's examine the new summary file.


```python
# load in process output from file
with open(process_output["process_output_files"][0], "r") as file:
    print(file.read())
```

    Winston Smith walked through the glass doors of Victory Mansions. The hallway
    smelled of boiled cabbage and old rag mats. At one end of
    the hallway an acoloured poster, too large for indoor display, had been
    tacked to the wall. It depicted simply an enormous face, more than
    a metre wide.
    
    Winston kept his back turned to the telescreen. It was safer; though,
    he well knew, even a back can be revealing. A kilometre away
    the Ministry of Truth, his place of work, towered vast and white.


This is a more concise, if more abstract, summary of the original input text.

Lets recurse one more time, seeking to achieve an even briefer summary of the original.

Once again, almost nothing changes about how we use the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method: we only point `local_file_path` to the output of our second summarization.


```python
# assign the summary of the summary generated above to a variable for easy reference
second_summary = process_output["process_output_files"][0]

# process this summary through the pipeline again
process_output = pipeline.process(
    local_file_path=second_summary,  # feed back into the pipeline the summary of the earlier-generated summary
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,
    wait_for_process=True,
    verbose=False,
)
```

The very short summary result is displayed below:


```python
# load in the recursed summary from file
with open(process_output["process_output_files"][0], "r") as file:
    print(file.read())
```

    Winston Smith walked through the glass doors of Victory Mansions. The hallway
    smelled of boiled cabbage and old rag mats. A kilometre away, his
    place of work, the Ministry of Truth, towered vast and white.


As you can see, this is very terse but representative summary of our original text.

You can reproduce this result (of recursively summarizing a document thrice) by building a new pipeline that contains three [`summarize`](../../modules/ai_modules/summarize_module.md) modules in succession.

We explore just such an example in our recursive summarization pipeline [example](../../examples/multi_module_non_search_pipeline_examples/multi_recursive_summarization.md).
