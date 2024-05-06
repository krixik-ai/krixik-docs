## The `ocr` module

This document reviews the `ocr` module - which takes as input an image and returns text detected from the input image.  Output data is returned as a json.

This document includes an overview of custom pipeline setup, current model set, parameters, and `.process` usage for this module.

To follow along with this demonstration be sure to initialize your krixik session with your api key and url as shown below. 

We illustrate loading these required secrets in via [python-dotenv](https://pypi.org/project/python-dotenv/), storing those secrets in a `.env` file.  This is always good practice for storing / loading secrets (e.g., doing so will reduce the chance you inadvertantly push secrets to a repo).

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [required input format](#required-input-format)
- [using the default model](#using-the-default-model)

## Pipeline setup

Below we setup a simple one module pipeline using the `ocr` module. 

We do this by passing the module name to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a pipeline with a single module
pipeline = krixik.create_pipeline(name="my-ocr-pipeline",
                                  module_chain=["ocr"])
```

The `ocr` module comes with a subset of popular caption models including the following:

- [tesseract-en](https://github.com/tesseract-ocr/tesseract): Tesseract OCR is an open-source software tool that performs optical character recognition, converting images containing printed or handwritten text into machine-encoded text data.
- [tesseract-es](https://github.com/tesseract-ocr/tesseract): Tesseract OCR with spanish language detection.

These available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).

## Required input format

The `caption` module accepts `.png`, `.jpg`, and `.jpeg` images as input.

Lets take a quick look at a valid input file - and then process it.


```python
# examine contents of a valid input file
test_file = "../../data/input/seal.png"
from IPython.display import Image
Image(filename=test_file) 
```




    
![png](ocr_files/ocr_7_0.png)
    



## Using the default model

Let's process the input file above using the default model - `tesseract-en`.  Because this is the default model we need not input the optional `modules` argument into `.process`.


```python
# define path to an input file
test_file = "../../data/input/seal.png"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory="../../data/output", # save output repo data output subdir
                                  expire_time=60 * 10,    # set all process data to expire in 10 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is json, the process output is provided in this object as well.  The output file itself has been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "my-ocr-pipeline",
      "request_id": "06c3b2ba-c7e6-43ef-a549-f0781067c3fa",
      "file_id": "daffe207-3924-446d-91bb-d51e193ce179",
      "message": "SUCCESS - output fetched for file_id daffe207-3924-446d-91bb-d51e193ce179.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "text": "The Seventh Seal\n\nThe night had brought little relief from the heat, and at dawn a hot gust of\nwind blows across the colorless sea. The KNIGHT, Antonius Block, lies\nprostrate on some spruce branches spread over the fine sand. His eyes are\nwide-open and bloodshot from lack of sleep.\n\nNearby his squire JONS is snoring loudly. He has fallen asleep where he\ncollapsed, at the edge of the forest among the wind-gnarled fir trees. His\nopen mouth gapes towards the dawn, and unearthly sounds come from his throat.\nAt the sudden gust of wind, the horses stir, stretching their parched muzzles\ntowards the sea. They are as thin and worn as their masters.\n",
          "detections": [
            {
              "left": 10,
              "top": 54,
              "width": 51,
              "height": 22,
              "text": "The",
              "conf": 90.48
            },
            {
              "left": 81,
              "top": 54,
              "width": 117,
              "height": 22,
              "text": "Seventh",
              "conf": 90.48
            },
            {
              "left": 220,
              "top": 54,
              "width": 66,
              "height": 22,
              "text": "Seal",
              "conf": 92.21
            },
            {
              "left": 10,
              "top": 122,
              "width": 51,
              "height": 22,
              "text": "The",
              "conf": 92.12
            },
            {
              "left": 82,
              "top": 122,
              "width": 81,
              "height": 28,
              "text": "night",
              "conf": 91.98
            },
            {
              "left": 186,
              "top": 122,
              "width": 47,
              "height": 22,
              "text": "had",
              "conf": 92.23
            },
            {
              "left": 255,
              "top": 122,
              "width": 116,
              "height": 28,
              "text": "brought",
              "conf": 92.23
            },
            {
              "left": 395,
              "top": 122,
              "width": 99,
              "height": 22,
              "text": "little",
              "conf": 90.88
            },
            {
              "left": 518,
              "top": 122,
              "width": 97,
              "height": 22,
              "text": "relief",
              "conf": 91.56
            },
            {
              "left": 637,
              "top": 122,
              "width": 65,
              "height": 22,
              "text": "from",
              "conf": 92.14
            },
            {
              "left": 723,
              "top": 122,
              "width": 48,
              "height": 22,
              "text": "the",
              "conf": 92.14
            },
            {
              "left": 793,
              "top": 122,
              "width": 77,
              "height": 27,
              "text": "heat,",
              "conf": 90.93
            },
            {
              "left": 896,
              "top": 122,
              "width": 48,
              "height": 22,
              "text": "and",
              "conf": 91.68
            },
            {
              "left": 965,
              "top": 123,
              "width": 31,
              "height": 21,
              "text": "at",
              "conf": 92.24
            },
            {
              "left": 1017,
              "top": 122,
              "width": 66,
              "height": 22,
              "text": "dawn",
              "conf": 92.24
            },
            {
              "left": 1104,
              "top": 128,
              "width": 13,
              "height": 16,
              "text": "a",
              "conf": 91.17
            },
            {
              "left": 1140,
              "top": 122,
              "width": 46,
              "height": 22,
              "text": "hot",
              "conf": 91.81
            },
            {
              "left": 1208,
              "top": 123,
              "width": 65,
              "height": 27,
              "text": "gust",
              "conf": 91.59
            },
            {
              "left": 1295,
              "top": 122,
              "width": 31,
              "height": 22,
              "text": "of",
              "conf": 91.59
            },
            {
              "left": 10,
              "top": 156,
              "width": 67,
              "height": 22,
              "text": "wind",
              "conf": 90.08
            },
            {
              "left": 99,
              "top": 156,
              "width": 82,
              "height": 22,
              "text": "blows",
              "conf": 91.73
            },
            {
              "left": 202,
              "top": 162,
              "width": 100,
              "height": 16,
              "text": "across",
              "conf": 90.8
            },
            {
              "left": 324,
              "top": 156,
              "width": 49,
              "height": 22,
              "text": "the",
              "conf": 91.33
            },
            {
              "left": 394,
              "top": 156,
              "width": 151,
              "height": 22,
              "text": "colorless",
              "conf": 90.55
            },
            {
              "left": 568,
              "top": 162,
              "width": 59,
              "height": 16,
              "text": "sea.",
              "conf": 93.01
            },
            {
              "left": 652,
              "top": 156,
              "width": 50,
              "height": 22,
              "text": "The",
              "conf": 91.62
            },
            {
              "left": 723,
              "top": 156,
              "width": 113,
              "height": 27,
              "text": "KNIGHT,",
              "conf": 92.28
            },
            {
              "left": 860,
              "top": 156,
              "width": 136,
              "height": 22,
              "text": "Antonius",
              "conf": 91.4
            },
            {
              "left": 1018,
              "top": 156,
              "width": 95,
              "height": 27,
              "text": "Block,",
              "conf": 91.85
            },
            {
              "left": 1140,
              "top": 156,
              "width": 64,
              "height": 22,
              "text": "lies",
              "conf": 82.9
            },
            {
              "left": 13,
              "top": 191,
              "width": 152,
              "height": 27,
              "text": "prostrate",
              "conf": 91.37
            },
            {
              "left": 185,
              "top": 196,
              "width": 31,
              "height": 16,
              "text": "on",
              "conf": 92.02
            },
            {
              "left": 238,
              "top": 196,
              "width": 65,
              "height": 16,
              "text": "some",
              "conf": 91.64
            },
            {
              "left": 325,
              "top": 196,
              "width": 100,
              "height": 22,
              "text": "spruce",
              "conf": 91.83
            },
            {
              "left": 446,
              "top": 190,
              "width": 133,
              "height": 22,
              "text": "branches",
              "conf": 91.98
            },
            {
              "left": 602,
              "top": 190,
              "width": 99,
              "height": 28,
              "text": "spread",
              "conf": 92.01
            },
            {
              "left": 723,
              "top": 196,
              "width": 66,
              "height": 16,
              "text": "over",
              "conf": 92.6
            },
            {
              "left": 809,
              "top": 190,
              "width": 49,
              "height": 22,
              "text": "the",
              "conf": 93.04
            },
            {
              "left": 880,
              "top": 190,
              "width": 65,
              "height": 22,
              "text": "fine",
              "conf": 91.36
            },
            {
              "left": 967,
              "top": 190,
              "width": 77,
              "height": 22,
              "text": "sand.",
              "conf": 92.68
            },
            {
              "left": 1070,
              "top": 190,
              "width": 47,
              "height": 22,
              "text": "His",
              "conf": 92.28
            },
            {
              "left": 1139,
              "top": 196,
              "width": 65,
              "height": 22,
              "text": "eyes",
              "conf": 91.88
            },
            {
              "left": 1225,
              "top": 196,
              "width": 49,
              "height": 16,
              "text": "are",
              "conf": 90.57
            },
            {
              "left": 10,
              "top": 224,
              "width": 154,
              "height": 28,
              "text": "wide-open",
              "conf": 73.54
            },
            {
              "left": 185,
              "top": 224,
              "width": 48,
              "height": 22,
              "text": "and",
              "conf": 91.18
            },
            {
              "left": 255,
              "top": 224,
              "width": 151,
              "height": 22,
              "text": "bloodshot",
              "conf": 91.84
            },
            {
              "left": 429,
              "top": 224,
              "width": 65,
              "height": 22,
              "text": "from",
              "conf": 91.61
            },
            {
              "left": 516,
              "top": 224,
              "width": 66,
              "height": 22,
              "text": "lack",
              "conf": 92.2
            },
            {
              "left": 601,
              "top": 224,
              "width": 31,
              "height": 22,
              "text": "of",
              "conf": 92.89
            },
            {
              "left": 654,
              "top": 224,
              "width": 95,
              "height": 28,
              "text": "sleep.",
              "conf": 90.45
            },
            {
              "left": 10,
              "top": 292,
              "width": 103,
              "height": 28,
              "text": "Nearby",
              "conf": 92.22
            },
            {
              "left": 134,
              "top": 292,
              "width": 47,
              "height": 22,
              "text": "his",
              "conf": 91.96
            },
            {
              "left": 204,
              "top": 292,
              "width": 99,
              "height": 28,
              "text": "squire",
              "conf": 91.78
            },
            {
              "left": 323,
              "top": 292,
              "width": 67,
              "height": 22,
              "text": "JONS",
              "conf": 85.69
            },
            {
              "left": 412,
              "top": 292,
              "width": 29,
              "height": 22,
              "text": "is",
              "conf": 87.03
            },
            {
              "left": 464,
              "top": 292,
              "width": 116,
              "height": 28,
              "text": "snoring",
              "conf": 91.88
            },
            {
              "left": 603,
              "top": 292,
              "width": 111,
              "height": 28,
              "text": "loudly.",
              "conf": 91.29
            },
            {
              "left": 740,
              "top": 293,
              "width": 31,
              "height": 21,
              "text": "He",
              "conf": 92.41
            },
            {
              "left": 793,
              "top": 292,
              "width": 47,
              "height": 22,
              "text": "has",
              "conf": 90.81
            },
            {
              "left": 862,
              "top": 292,
              "width": 99,
              "height": 22,
              "text": "fallen",
              "conf": 90.81
            },
            {
              "left": 983,
              "top": 292,
              "width": 100,
              "height": 28,
              "text": "asleep",
              "conf": 92.57
            },
            {
              "left": 1102,
              "top": 292,
              "width": 86,
              "height": 22,
              "text": "where",
              "conf": 92.41
            },
            {
              "left": 1209,
              "top": 292,
              "width": 31,
              "height": 22,
              "text": "he",
              "conf": 90.62
            },
            {
              "left": 13,
              "top": 326,
              "width": 164,
              "height": 28,
              "text": "collapsed,",
              "conf": 90.44
            },
            {
              "left": 202,
              "top": 327,
              "width": 31,
              "height": 21,
              "text": "at",
              "conf": 92.59
            },
            {
              "left": 254,
              "top": 326,
              "width": 49,
              "height": 22,
              "text": "the",
              "conf": 92.17
            },
            {
              "left": 324,
              "top": 326,
              "width": 66,
              "height": 28,
              "text": "edge",
              "conf": 91.37
            },
            {
              "left": 411,
              "top": 326,
              "width": 30,
              "height": 22,
              "text": "of",
              "conf": 92.52
            },
            {
              "left": 462,
              "top": 326,
              "width": 49,
              "height": 22,
              "text": "the",
              "conf": 92.7
            },
            {
              "left": 533,
              "top": 326,
              "width": 98,
              "height": 22,
              "text": "forest",
              "conf": 92.7
            },
            {
              "left": 653,
              "top": 332,
              "width": 83,
              "height": 22,
              "text": "among",
              "conf": 92.0
            },
            {
              "left": 757,
              "top": 326,
              "width": 49,
              "height": 22,
              "text": "the",
              "conf": 92.68
            },
            {
              "left": 825,
              "top": 326,
              "width": 206,
              "height": 28,
              "text": "wind-gnarled",
              "conf": 77.4
            },
            {
              "left": 1053,
              "top": 326,
              "width": 48,
              "height": 22,
              "text": "fir",
              "conf": 92.84
            },
            {
              "left": 1121,
              "top": 327,
              "width": 96,
              "height": 21,
              "text": "trees.",
              "conf": 91.35
            },
            {
              "left": 1243,
              "top": 326,
              "width": 47,
              "height": 22,
              "text": "His",
              "conf": 91.08
            },
            {
              "left": 12,
              "top": 366,
              "width": 65,
              "height": 22,
              "text": "open",
              "conf": 92.05
            },
            {
              "left": 98,
              "top": 360,
              "width": 83,
              "height": 22,
              "text": "mouth",
              "conf": 92.26
            },
            {
              "left": 202,
              "top": 366,
              "width": 83,
              "height": 22,
              "text": "gapes",
              "conf": 92.6
            },
            {
              "left": 306,
              "top": 360,
              "width": 117,
              "height": 22,
              "text": "towards",
              "conf": 90.24
            },
            {
              "left": 445,
              "top": 360,
              "width": 49,
              "height": 22,
              "text": "the",
              "conf": 90.24
            },
            {
              "left": 514,
              "top": 360,
              "width": 79,
              "height": 27,
              "text": "dawn,",
              "conf": 91.95
            },
            {
              "left": 618,
              "top": 360,
              "width": 48,
              "height": 22,
              "text": "and",
              "conf": 92.56
            },
            {
              "left": 689,
              "top": 360,
              "width": 152,
              "height": 28,
              "text": "unearthly",
              "conf": 91.36
            },
            {
              "left": 862,
              "top": 360,
              "width": 99,
              "height": 22,
              "text": "sounds",
              "conf": 92.15
            },
            {
              "left": 984,
              "top": 366,
              "width": 65,
              "height": 16,
              "text": "come",
              "conf": 92.9
            },
            {
              "left": 1070,
              "top": 360,
              "width": 66,
              "height": 22,
              "text": "from",
              "conf": 91.26
            },
            {
              "left": 1157,
              "top": 360,
              "width": 47,
              "height": 22,
              "text": "his",
              "conf": 91.26
            },
            {
              "left": 1225,
              "top": 360,
              "width": 113,
              "height": 22,
              "text": "throat.",
              "conf": 92.48
            },
            {
              "left": 10,
              "top": 395,
              "width": 32,
              "height": 21,
              "text": "At",
              "conf": 92.4
            },
            {
              "left": 64,
              "top": 394,
              "width": 49,
              "height": 22,
              "text": "the",
              "conf": 92.4
            },
            {
              "left": 134,
              "top": 394,
              "width": 99,
              "height": 22,
              "text": "sudden",
              "conf": 90.06
            },
            {
              "left": 254,
              "top": 395,
              "width": 65,
              "height": 27,
              "text": "gust",
              "conf": 90.46
            },
            {
              "left": 341,
              "top": 394,
              "width": 31,
              "height": 22,
              "text": "of",
              "conf": 92.95
            },
            {
              "left": 391,
              "top": 394,
              "width": 81,
              "height": 27,
              "text": "wind,",
              "conf": 91.2
            },
            {
              "left": 497,
              "top": 394,
              "width": 49,
              "height": 22,
              "text": "the",
              "conf": 91.21
            },
            {
              "left": 567,
              "top": 394,
              "width": 99,
              "height": 22,
              "text": "horses",
              "conf": 90.56
            },
            {
              "left": 689,
              "top": 394,
              "width": 77,
              "height": 27,
              "text": "stir,",
              "conf": 89.29
            },
            {
              "left": 793,
              "top": 394,
              "width": 168,
              "height": 28,
              "text": "stretching",
              "conf": 92.05
            },
            {
              "left": 983,
              "top": 394,
              "width": 84,
              "height": 22,
              "text": "their",
              "conf": 90.23
            },
            {
              "left": 1088,
              "top": 394,
              "width": 116,
              "height": 28,
              "text": "parched",
              "conf": 90.23
            },
            {
              "left": 1225,
              "top": 394,
              "width": 117,
              "height": 22,
              "text": "muzzles",
              "conf": 91.35
            },
            {
              "left": 12,
              "top": 428,
              "width": 117,
              "height": 22,
              "text": "towards",
              "conf": 92.03
            },
            {
              "left": 150,
              "top": 428,
              "width": 49,
              "height": 22,
              "text": "the",
              "conf": 92.49
            },
            {
              "left": 221,
              "top": 434,
              "width": 60,
              "height": 16,
              "text": "sea.",
              "conf": 91.67
            },
            {
              "left": 305,
              "top": 428,
              "width": 68,
              "height": 28,
              "text": "They",
              "conf": 91.42
            },
            {
              "left": 393,
              "top": 434,
              "width": 49,
              "height": 16,
              "text": "are",
              "conf": 91.27
            },
            {
              "left": 462,
              "top": 434,
              "width": 31,
              "height": 16,
              "text": "as",
              "conf": 89.91
            },
            {
              "left": 514,
              "top": 428,
              "width": 66,
              "height": 22,
              "text": "thin",
              "conf": 89.91
            },
            {
              "left": 601,
              "top": 428,
              "width": 48,
              "height": 22,
              "text": "and",
              "conf": 91.09
            },
            {
              "left": 669,
              "top": 434,
              "width": 67,
              "height": 16,
              "text": "worn",
              "conf": 91.22
            },
            {
              "left": 757,
              "top": 434,
              "width": 31,
              "height": 16,
              "text": "as",
              "conf": 90.83
            },
            {
              "left": 809,
              "top": 428,
              "width": 84,
              "height": 22,
              "text": "their",
              "conf": 90.83
            },
            {
              "left": 913,
              "top": 429,
              "width": 131,
              "height": 21,
              "text": "masters.",
              "conf": 92.17
            }
          ]
        }
      ],
      "process_output_files": [
        "../../data/output/daffe207-3924-446d-91bb-d51e193ce179.json"
      ]
    }


We load in the text file output from `process_output_files` below. 


```python
# load in process output from file
with open(process_output["process_output_files"][0]) as f:
  print(json.dumps(json.load(f), indent=2))
```

    [{"text": "The Seventh Seal\n\nThe night had brought little relief from the heat, and at dawn a hot gust of\nwind blows across the colorless sea. The KNIGHT, Antonius Block, lies\nprostrate on some spruce branches spread over the fine sand. His eyes are\nwide-open and bloodshot from lack of sleep.\n\nNearby his squire JONS is snoring loudly. He has fallen asleep where he\ncollapsed, at the edge of the forest among the wind-gnarled fir trees. His\nopen mouth gapes towards the dawn, and unearthly sounds come from his throat.\nAt the sudden gust of wind, the horses stir, stretching their parched muzzles\ntowards the sea. They are as thin and worn as their masters.\n", "detections": [{"left": 10, "top": 54, "width": 51, "height": 22, "text": "The", "conf": 90.48}, {"left": 81, "top": 54, "width": 117, "height": 22, "text": "Seventh", "conf": 90.48}, {"left": 220, "top": 54, "width": 66, "height": 22, "text": "Seal", "conf": 92.21}, {"left": 10, "top": 122, "width": 51, "height": 22, "text": "The", "conf": 92.12}, {"left": 82, "top": 122, "width": 81, "height": 28, "text": "night", "conf": 91.98}, {"left": 186, "top": 122, "width": 47, "height": 22, "text": "had", "conf": 92.23}, {"left": 255, "top": 122, "width": 116, "height": 28, "text": "brought", "conf": 92.23}, {"left": 395, "top": 122, "width": 99, "height": 22, "text": "little", "conf": 90.88}, {"left": 518, "top": 122, "width": 97, "height": 22, "text": "relief", "conf": 91.56}, {"left": 637, "top": 122, "width": 65, "height": 22, "text": "from", "conf": 92.14}, {"left": 723, "top": 122, "width": 48, "height": 22, "text": "the", "conf": 92.14}, {"left": 793, "top": 122, "width": 77, "height": 27, "text": "heat,", "conf": 90.93}, {"left": 896, "top": 122, "width": 48, "height": 22, "text": "and", "conf": 91.68}, {"left": 965, "top": 123, "width": 31, "height": 21, "text": "at", "conf": 92.24}, {"left": 1017, "top": 122, "width": 66, "height": 22, "text": "dawn", "conf": 92.24}, {"left": 1104, "top": 128, "width": 13, "height": 16, "text": "a", "conf": 91.17}, {"left": 1140, "top": 122, "width": 46, "height": 22, "text": "hot", "conf": 91.81}, {"left": 1208, "top": 123, "width": 65, "height": 27, "text": "gust", "conf": 91.59}, {"left": 1295, "top": 122, "width": 31, "height": 22, "text": "of", "conf": 91.59}, {"left": 10, "top": 156, "width": 67, "height": 22, "text": "wind", "conf": 90.08}, {"left": 99, "top": 156, "width": 82, "height": 22, "text": "blows", "conf": 91.73}, {"left": 202, "top": 162, "width": 100, "height": 16, "text": "across", "conf": 90.8}, {"left": 324, "top": 156, "width": 49, "height": 22, "text": "the", "conf": 91.33}, {"left": 394, "top": 156, "width": 151, "height": 22, "text": "colorless", "conf": 90.55}, {"left": 568, "top": 162, "width": 59, "height": 16, "text": "sea.", "conf": 93.01}, {"left": 652, "top": 156, "width": 50, "height": 22, "text": "The", "conf": 91.62}, {"left": 723, "top": 156, "width": 113, "height": 27, "text": "KNIGHT,", "conf": 92.28}, {"left": 860, "top": 156, "width": 136, "height": 22, "text": "Antonius", "conf": 91.4}, {"left": 1018, "top": 156, "width": 95, "height": 27, "text": "Block,", "conf": 91.85}, {"left": 1140, "top": 156, "width": 64, "height": 22, "text": "lies", "conf": 82.9}, {"left": 13, "top": 191, "width": 152, "height": 27, "text": "prostrate", "conf": 91.37}, {"left": 185, "top": 196, "width": 31, "height": 16, "text": "on", "conf": 92.02}, {"left": 238, "top": 196, "width": 65, "height": 16, "text": "some", "conf": 91.64}, {"left": 325, "top": 196, "width": 100, "height": 22, "text": "spruce", "conf": 91.83}, {"left": 446, "top": 190, "width": 133, "height": 22, "text": "branches", "conf": 91.98}, {"left": 602, "top": 190, "width": 99, "height": 28, "text": "spread", "conf": 92.01}, {"left": 723, "top": 196, "width": 66, "height": 16, "text": "over", "conf": 92.6}, {"left": 809, "top": 190, "width": 49, "height": 22, "text": "the", "conf": 93.04}, {"left": 880, "top": 190, "width": 65, "height": 22, "text": "fine", "conf": 91.36}, {"left": 967, "top": 190, "width": 77, "height": 22, "text": "sand.", "conf": 92.68}, {"left": 1070, "top": 190, "width": 47, "height": 22, "text": "His", "conf": 92.28}, {"left": 1139, "top": 196, "width": 65, "height": 22, "text": "eyes", "conf": 91.88}, {"left": 1225, "top": 196, "width": 49, "height": 16, "text": "are", "conf": 90.57}, {"left": 10, "top": 224, "width": 154, "height": 28, "text": "wide-open", "conf": 73.54}, {"left": 185, "top": 224, "width": 48, "height": 22, "text": "and", "conf": 91.18}, {"left": 255, "top": 224, "width": 151, "height": 22, "text": "bloodshot", "conf": 91.84}, {"left": 429, "top": 224, "width": 65, "height": 22, "text": "from", "conf": 91.61}, {"left": 516, "top": 224, "width": 66, "height": 22, "text": "lack", "conf": 92.2}, {"left": 601, "top": 224, "width": 31, "height": 22, "text": "of", "conf": 92.89}, {"left": 654, "top": 224, "width": 95, "height": 28, "text": "sleep.", "conf": 90.45}, {"left": 10, "top": 292, "width": 103, "height": 28, "text": "Nearby", "conf": 92.22}, {"left": 134, "top": 292, "width": 47, "height": 22, "text": "his", "conf": 91.96}, {"left": 204, "top": 292, "width": 99, "height": 28, "text": "squire", "conf": 91.78}, {"left": 323, "top": 292, "width": 67, "height": 22, "text": "JONS", "conf": 85.69}, {"left": 412, "top": 292, "width": 29, "height": 22, "text": "is", "conf": 87.03}, {"left": 464, "top": 292, "width": 116, "height": 28, "text": "snoring", "conf": 91.88}, {"left": 603, "top": 292, "width": 111, "height": 28, "text": "loudly.", "conf": 91.29}, {"left": 740, "top": 293, "width": 31, "height": 21, "text": "He", "conf": 92.41}, {"left": 793, "top": 292, "width": 47, "height": 22, "text": "has", "conf": 90.81}, {"left": 862, "top": 292, "width": 99, "height": 22, "text": "fallen", "conf": 90.81}, {"left": 983, "top": 292, "width": 100, "height": 28, "text": "asleep", "conf": 92.57}, {"left": 1102, "top": 292, "width": 86, "height": 22, "text": "where", "conf": 92.41}, {"left": 1209, "top": 292, "width": 31, "height": 22, "text": "he", "conf": 90.62}, {"left": 13, "top": 326, "width": 164, "height": 28, "text": "collapsed,", "conf": 90.44}, {"left": 202, "top": 327, "width": 31, "height": 21, "text": "at", "conf": 92.59}, {"left": 254, "top": 326, "width": 49, "height": 22, "text": "the", "conf": 92.17}, {"left": 324, "top": 326, "width": 66, "height": 28, "text": "edge", "conf": 91.37}, {"left": 411, "top": 326, "width": 30, "height": 22, "text": "of", "conf": 92.52}, {"left": 462, "top": 326, "width": 49, "height": 22, "text": "the", "conf": 92.7}, {"left": 533, "top": 326, "width": 98, "height": 22, "text": "forest", "conf": 92.7}, {"left": 653, "top": 332, "width": 83, "height": 22, "text": "among", "conf": 92.0}, {"left": 757, "top": 326, "width": 49, "height": 22, "text": "the", "conf": 92.68}, {"left": 825, "top": 326, "width": 206, "height": 28, "text": "wind-gnarled", "conf": 77.4}, {"left": 1053, "top": 326, "width": 48, "height": 22, "text": "fir", "conf": 92.84}, {"left": 1121, "top": 327, "width": 96, "height": 21, "text": "trees.", "conf": 91.35}, {"left": 1243, "top": 326, "width": 47, "height": 22, "text": "His", "conf": 91.08}, {"left": 12, "top": 366, "width": 65, "height": 22, "text": "open", "conf": 92.05}, {"left": 98, "top": 360, "width": 83, "height": 22, "text": "mouth", "conf": 92.26}, {"left": 202, "top": 366, "width": 83, "height": 22, "text": "gapes", "conf": 92.6}, {"left": 306, "top": 360, "width": 117, "height": 22, "text": "towards", "conf": 90.24}, {"left": 445, "top": 360, "width": 49, "height": 22, "text": "the", "conf": 90.24}, {"left": 514, "top": 360, "width": 79, "height": 27, "text": "dawn,", "conf": 91.95}, {"left": 618, "top": 360, "width": 48, "height": 22, "text": "and", "conf": 92.56}, {"left": 689, "top": 360, "width": 152, "height": 28, "text": "unearthly", "conf": 91.36}, {"left": 862, "top": 360, "width": 99, "height": 22, "text": "sounds", "conf": 92.15}, {"left": 984, "top": 366, "width": 65, "height": 16, "text": "come", "conf": 92.9}, {"left": 1070, "top": 360, "width": 66, "height": 22, "text": "from", "conf": 91.26}, {"left": 1157, "top": 360, "width": 47, "height": 22, "text": "his", "conf": 91.26}, {"left": 1225, "top": 360, "width": 113, "height": 22, "text": "throat.", "conf": 92.48}, {"left": 10, "top": 395, "width": 32, "height": 21, "text": "At", "conf": 92.4}, {"left": 64, "top": 394, "width": 49, "height": 22, "text": "the", "conf": 92.4}, {"left": 134, "top": 394, "width": 99, "height": 22, "text": "sudden", "conf": 90.06}, {"left": 254, "top": 395, "width": 65, "height": 27, "text": "gust", "conf": 90.46}, {"left": 341, "top": 394, "width": 31, "height": 22, "text": "of", "conf": 92.95}, {"left": 391, "top": 394, "width": 81, "height": 27, "text": "wind,", "conf": 91.2}, {"left": 497, "top": 394, "width": 49, "height": 22, "text": "the", "conf": 91.21}, {"left": 567, "top": 394, "width": 99, "height": 22, "text": "horses", "conf": 90.56}, {"left": 689, "top": 394, "width": 77, "height": 27, "text": "stir,", "conf": 89.29}, {"left": 793, "top": 394, "width": 168, "height": 28, "text": "stretching", "conf": 92.05}, {"left": 983, "top": 394, "width": 84, "height": 22, "text": "their", "conf": 90.23}, {"left": 1088, "top": 394, "width": 116, "height": 28, "text": "parched", "conf": 90.23}, {"left": 1225, "top": 394, "width": 117, "height": 22, "text": "muzzles", "conf": 91.35}, {"left": 12, "top": 428, "width": 117, "height": 22, "text": "towards", "conf": 92.03}, {"left": 150, "top": 428, "width": 49, "height": 22, "text": "the", "conf": 92.49}, {"left": 221, "top": 434, "width": 60, "height": 16, "text": "sea.", "conf": 91.67}, {"left": 305, "top": 428, "width": 68, "height": 28, "text": "They", "conf": 91.42}, {"left": 393, "top": 434, "width": 49, "height": 16, "text": "are", "conf": 91.27}, {"left": 462, "top": 434, "width": 31, "height": 16, "text": "as", "conf": 89.91}, {"left": 514, "top": 428, "width": 66, "height": 22, "text": "thin", "conf": 89.91}, {"left": 601, "top": 428, "width": 48, "height": 22, "text": "and", "conf": 91.09}, {"left": 669, "top": 434, "width": 67, "height": 16, "text": "worn", "conf": 91.22}, {"left": 757, "top": 434, "width": 31, "height": 16, "text": "as", "conf": 90.83}, {"left": 809, "top": 428, "width": 84, "height": 22, "text": "their", "conf": 90.83}, {"left": 913, "top": 429, "width": 131, "height": 21, "text": "masters.", "conf": 92.17}]}]
