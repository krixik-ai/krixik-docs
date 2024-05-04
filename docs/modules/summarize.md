## The `summarize` module

This document reviews the `summarize` module - which takes as input a document and returns a summary of its (text) contents.

This document includes an overview of custom pipeline setup, current model set, parameters, and `.process` usage for this module.

To follow along with this demonstration be sure to initialize your krixik session with your api key and url as shown below. 

We illustrate loading these required secrets in via [python-dotenv](https://pypi.org/project/python-dotenv/), storing those secrets in a `.env` file.  This is always good practice for storing / loading secrets (e.g., doing so will reduce the chance you inadvertantly push secrets to a repo).

A table of contents for the remainder of this document is shown below.

- [pipeline setup](#pipeline-setup)
- [required input format](#required-input-format)
- [using the default model](#using-the-default-model)
- [recursive summarization](#recursive-summarization)
- [using a non-default model](#using-a-non-default-model)

## Pipeline setup

Below we setup a simple one module pipeline using the `summarize` module. 

We do this by passing the module name to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(name="modules-summarize-docs",
                                  module_chain=["summarize"])
```

The `summarize` module comes with a single model:

- [bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn) (default)
- [text-summarization](https://huggingface.co/Falconsai/text_summarization)

These available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).

## Required input format

The `keyword-db` module accepts `.txt`, `.pdf`, `.docx`, and `.pptx` file formats as input.  The latter three (`.pdf`, `.docx`, and `.pptx`) are first converted to `.txt` prior to processing.

Let's look at an example of a small valid input - and then process it.


```python
# examine contents of a valid test input file
test_file = "../../data/input/1984_short.txt"
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


## Using the default model

Now let's process it using our default model - [bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn).  Since we are using the default model we need not input the optional `modules` argument into `.process`.


```python
# define path to an input file from examples directory
test_file = "../../data/input/1984_short.txt"

# process a file through the pipeline
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory="../../data/output", # save output repo data output subdir
                                  expire_time=60 * 10,      # set all process data to expire in 10 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is a json, the process output is provided in this object is as well.  The file itself has been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed file is used as a filename prefix for both output files.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "my-summarize-pipeline",
      "request_id": "ae8cb093-b55f-4f2d-bd45-9048238bb26e",
      "file_id": "d65f3b9e-39d2-4ca5-939b-d317a9a406cf",
      "message": "SUCCESS - output fetched for file_id d65f3b9e-39d2-4ca5-939b-d317a9a406cf.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../data/output/d65f3b9e-39d2-4ca5-939b-d317a9a406cf.txt"
      ]
    }


We load in the text file output from `process_output_files` below. 


```python
# load in process output from file
with open(process_output['process_output_files'][0], "r") as file:
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
    white above the grimy landscape.
    
    The Ministry of Truth --Minitrue, in Newspeak -- was startlingly different from
    any other object in sight. It was an enormous pyramidal structure of
    glittering white concrete, soaring 300 metres into the air. From where Winston
    stood it was just possible to read, picked out on its white
    face, the three slogans of the Party.


We have just summarized a test input of around 5500 characters into a summary of less than half that length.

But what if this is not short enough for our needs?

One of the most practical ways to achieve a shorter - and more absract but still representative - summary is to apply a summarization *recursively*. 

That is, we feed the summary created above through the summarizer again - producing a shorter summary.

We do this next.

## Recursive summarization

To produce a shorter summary of our original text we feed the first summarization made above into our summarizer.

This involves executing `process` on our pipeline in precisely the same manner we saw above.  The only difference is the file we feed into it.  Now we will feed the output summary we just created.


```python
# assign the summary above to a variable for reference
first_summary = process_output['process_output_files'][0]

# process a file through the pipeline
process_output = pipeline.process(local_file_path = first_summary,
                                  local_save_directory="../../data/output", # save output repo data output subdir
                                  expire_time=60 * 10,      # set all process data to expire in 10 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

Once `.process` completes we receive our shorter summary as an output file just as when we performed summarization the first time above.

Let's examine the new shorter summary file.


```python
# load in process output from file
with open(process_output['process_output_files'][0], "r") as file:
    print(file.read())  
```

    Winston Smith walked through the glass doors of Victory Mansions. The hallway
    smelled of boiled cabbage and old rag mats. At one end of
    the hallway an acoloured poster, too large for indoor display, had been
    tacked to the wall. It depicted simply an enormous face, more than
    a metre wide.
    
    Winston kept his back turned to the telescreen. It was safer; though,
    as he well knew, even a back can be revealing. A kilometre
    away the Ministry of Truth, his place of work, towered vast and
    white above the grimy landscape.


This is an even shorter, more abstract, summary of the original input text.

Lets recurse one more time, achieving an even shorter summary of our original text.

Again nothing will change about how we use `.process` - we only point `local_file_path` to the output of our second summarization.


```python
# assign the summary above to a variable for reference
second_summary = process_output['process_output_files'][0]

# process a file through the pipeline
process_output = pipeline.process(local_file_path = second_summary,
                                  local_save_directory="../../data/output", # save output repo data output subdir
                                  expire_time=60 * 10,      # set all process data to expire in 10 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

And we can view the now shorter summary below.


```python
# load in process output from file
with open(process_output['process_output_files'][0], "r") as file:
    print(file.read())  
```

    Winston Smith walked through the glass doors of Victory Mansions. The hallway
    smelled of boiled cabbage and old rag mats. A kilometre away the
    Ministry of Truth, his place of work, towered vast.


And indeed this is very terse but representative summary of our original text.

If we wanted - we could reproduce this result (of summarizing a document recursively three times) by building a new pipeline that contained three `summarize` modules in succession.

We explore just such an example in a [recursive summarization pipeline example](examples/summarize/recursive_summarize.md).

## Using a non-default model

To use a non-default model we simply define it explicitly in the `modules` input to `.process`.

To use the [text-summarization](https://huggingface.co/Falconsai/text_summarization) model we pass it explicitly as 

```
modules = {
    "summarize": {
        "model": "text-summarization
    }
}
```

to `.process`.


```python
# define path to an input file from examples directory
test_file = "../../data/input/1984_short.txt"

# process a file through the pipeline
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory="../../data/output", # save output repo data output subdir
                                  expire_time=60 * 10,      # set all process data to expire in 10 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,            # set verbosity to False
                                  modules = {
                                    "summarize": {
                                        "model": "text-summarization"
                                    }
                                })
```

And we can view the summary by loading in the output file.  The offset punctuation seen in this summary is an artifact of the model, as seen in the [model card](https://huggingface.co/Falconsai/text_summarization) on huggingface.


```python
# load in process output from file
with open(process_output['process_output_files'][0], "r") as file:
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
    Police plugged in on any individual wire was guesswork . But at
    any rate they could plug in your wire whenever they wanted to
    . The Ministry of Truth towered vast and white above the grimy
    landscape .
    
    The Ministry of Truth--Minitrue, in Newspeak, was the official language of Oceania
    . It was an enormous pyramidal structure of glittering white concrete, soaring
    up, terrace after terrace, 300 metres into the air . From where
    Winston stood it was just possible to read, picked out on its
    white face in elegant lettering .

