[![Python application](https://github.com/krixik-ai/krixik-docs/actions/workflows/python-app.yml/badge.svg)](https://github.com/krixik-ai/krixik-docs/actions/workflows/python-app.yml/python-app.yml)
[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)



# Welcome to Krixik!

Sequentially assembling multiple AI models into a single pipeline can be painful and expensive. Consuming even a single model can often be draining.

That's why we're here. **Welcome to Krixik**, where you can easily assemble and serverlessly consume modular AI pipelines through secure APIs.

### Table of Contents

- [Quickstart Guide](#quickstart-guide)
- [What can you build with Krixik?](#what-can-you-build-with-krixik)
- [Further Detail - Documentation](#further-detail---documentation)

## Quickstart Guide

### Account Registration

Krixik is currently in beta, so access to the Krixik Python client is by request only.

If you'd like to participate as a beta tester, please complete [this brief Google form](https://forms.gle/RyBAvjN1HEWPScb67).

### Install Krixik

Run the following command to install the Krixik Python client:

```pip
pip install krixik
```

Note: Python version 3.8 or higher is required.


### Initialize your Session

To [initialize](https://krixik-docs.readthedocs.io/latest/system/initialization/initialize_and_authenticate/) your Krixik client session you will need your unique `api_key` and `api_url` secrets.  Beta testers will receive their secrets from Krixik admin.

Instead of handling your secrets directly, we strongly recommend storing them in an `.env` file and loading them via [python-dotenv](https://pypi.org/project/python-dotenv/).

Once you have your secrets, [initialize](https://krixik-docs.readthedocs.io/latest/system/initialization/initialize_and_authenticate/) your session as follows:


```python
from krixik import krixik
krixik.init(api_key=MY_API_KEY, 
            api_url=MY_API_URL)
```

...where  `MY_API_KEY` and `MY_API_URL` are your account secrets.

If you've misplaced your secrets, please reach out to us directly.

### Building your First Pipeline

[Let's build a simple transcription pipeline consisting of a single `transcribe` module.](https://krixik-docs.readthedocs.io/latest/examples/single_module_pipelines/single_transcribe/) We can [create](https://krixik-docs.readthedocs.io/latest/system/pipeline_creation/create_pipeline/) the pipeline with a single line of code:

```python
# create a simple transcription pipeline
pipeline = krixik.create_pipeline(name='my_transcribe-pipeline-1', 
                                  module_chain=["transcribe"])
```

The pipeline is ready! Now you can [process](https://krixik-docs.readthedocs.io/latest/system/parameters_processing_files_through_pipelines/process_method/) audio and video files through it to generate transcripts of them.

```python
pipeline.process(local_file_path='./path/to/my/mp3/or/mp4')
```

The outputs of [this pipeline](https://krixik-docs.readthedocs.io/latest/examples/single_module_pipelines/single_transcribe/) will be a timestamped transcript of your input audio/video file, a `file_id` for the processed file, and a `request_id` for the process itself.


### Extending your Pipeline

[Suppose you wanted to immediately perform vector search on `transcribe` module output.](https://krixik-docs.readthedocs.io/latest/examples/search_pipeline_examples/multi_semantically_searchable_transcription/)

You would need to do the following after transcription:

1.  *Transform* the transcript into a text file
2.  *Parse* the text using a sliding window, chunking it into (possibly overlapping) snippets
3.  *Embed* each snippet using an appropriate text embedder
4.  *Store* the resulting vectors in a vector database
5.  *Index* said database
6.  *Enable* vector search on the database

Locally creating and testing this sequence of steps would be time consuming—orchestrating them in a secure production service even more so. And that's without trying to make the entire process serverless.

With **Krixik**, however, you can rapidly incorporate this functionality to your earlier pipeline by just adding a few modules. Syntax remains as above, so [making](https://krixik-docs.readthedocs.io/latest/system/pipeline_creation/create_pipeline/) the new pipeline still takes one line:

```python
# create pipeline with the above-alluded-to modules
pipeline = krixik.create_pipeline(name='transcribe_vsearch', 
                                  module_chain=["transcribe",
                                                "json-to-txt",
                                                "parser", 
                                                "text-embedder", 
                                                "vector-db"])
```

Let's [process](https://krixik-docs.readthedocs.io/latest/system/parameters_processing_files_through_pipelines/process_method/) a file through your new pipeline.

```python
pipeline.process(local_file_path='./path/to/my/mp3/or/mp4')
```

Now that there is at least one file in [the pipeline](https://krixik-docs.readthedocs.io/latest/examples/search_pipeline_examples/multi_semantically_searchable_transcription/), you can use the file's `file_id`—which was returned at the end of the above process—to perform semantic search on the associated transcript with [`.semantic_search`](https://krixik-docs.readthedocs.io/latest/system/search_methods/semantic_search_method/):

```python
pipeline.semantic_search(query="The text you wish to semantically search for goes here",
                         file_ids=['the_file_id_from_above'])
```

That's it! You have now transcribed a file, processed the transcript, performed vector search on it, and can reuse [the pipeline](https://krixik-docs.readthedocs.io/latest/examples/search_pipeline_examples/multi_semantically_searchable_transcription/) for as many files and queries as you like... all of it in a couple of minutes and with a few lines of code.

### Optional: Pull the [Krixik Docs Repo](https://github.com/krixik-ai/krixik-docs)

If you wish to follow along with the above example, or with any other of the score of examples we lay out in the documentation, then simply pull the entire [Krixik Docs repo](https://github.com/krixik-ai/krixik-docs).

Doing so will provide you with every file you need, and code will already be configured to run in that directory structure.

## What can you build with Krixik?

The [range of examples](https://krixik-docs.readthedocs.io/latest/examples/pipeline_examples_overview/) we've documented for you include pipelines to:

- ...generate an image caption for a set of images and then perform keyword search on the caption set.
  - [Pipeline: [Caption → JSON-to-TXT → Keyword Database]](https://krixik-docs.readthedocs.io/latest/examples/search_pipeline_examples/multi_keyword_searchable_image_captions/)
- ...transcribe a trove of documents, translate them to English, and then run sentiment analysis on each one.
  - [Pipeline: [Transcribe → Translate → JSON-to-TXT → Parser → Sentiment Analysis]](https://krixik-docs.readthedocs.io/latest/examples/multi_module_non_search_pipeline_examples/multi_sentiment_analysis_on_translated_transcription/)
- ...easily and serverlessly consume your open-source OCR model of choice.
  - [Pipeline: [OCR]](https://krixik-docs.readthedocs.io/latest/examples/single_module_pipelines/single_ocr/)

This is only the tip of the iceberg. Many more pipelines are currently possible ([see here for more examples](https://krixik-docs.readthedocs.io/latest/examples/pipeline_examples_overview/)), and the Krixik module/model library will constantly be expanding—perhaps even to include modules/models [of your own submission](https://krixik-docs.readthedocs.io/latest/modules/adding_your_own_modules_or_models/).

## Further Detail - Documentation

The above is just a peek at the power of Krixik. In addition to all possible parameterization (which we didn't even touch on), the Krixik toolbox is an ever-growing collection of modules and models for you to build with.

If you'd like to learn more, please visit [Krixik Documentation](https://krixik-docs.readthedocs.io/latest/), where we go into detail on:

- [Getting Started and Beyond: The Krixik System](https://krixik-docs.readthedocs.io/latest/system/system_overview/)
- [The Krixik Module Library](https://krixik-docs.readthedocs.io/latest/modules/modules_overview/)
- [Krixik Pipeline Examples](https://krixik-docs.readthedocs.io/latest/examples/pipeline_examples_overview/)

## Krixik Launch Date and Newsletter

Excited about Krixik graduating from beta? So are we! We're confident that this product is going to kick a monumental amount of ass, and we'd love to have you on board when it does.

If you wish to be in the loop about launch and other matters (we promise not to spam), please subscribe to occasional correspondence from us [HERE](https://forms.gle/Lp38U1UDpkppqoCD9).

Thanks for reading, and welcome to Krixik!