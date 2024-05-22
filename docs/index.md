# Welcome to Krixik Documentation!

If you're seeking the Krixik cli repo on GitHub, please [click here](https://github.com/krixik-ai/krixik-cli).

## Table of Contents

-  [What you can do with Krixik](#what-you-can-do-with-krixik)
-  [Core Concepts](#core-concepts)
-  [Documentation Sections](#documentation-sections)

## What you can do with Krixik

With Krixik, you can...

- ...run semantic search on 540 focus group transcripts and then perform sentiment analysis on each result.
  - Pipeline: [Parse → Embed → Vector Database → (Vector Search) → Sentiment Analysis]
- ...transcribe a year's worth of Peruvian political speeches, translate them to English, and then summarize each one.
  - Pipeline: [Transcribe → Translate → JSON-to-TXT → Summarize]
- ...easily and serverlessly consume your open-source OCR model of choice.
  - Pipeline: [OCR]

## Core Concepts

### Components of a Krixik Pipeline

Krixik **pipelines** are comprised of one or more sequentially connected **modules**. These modules are containers for a range of **parameterizable** AI **models** or support functions.

Let's examine each of the above-highlighted terms.

A **pipeline** is a self-contained sequence of one or more modules that is consumed via a serverless API.  

A **module** is a processing step with a unique input/output data footprint. Each model contains a parameterizable AI model or support function.

A **model** is a bespoke processing function contained within a module. Many of these are AI models, but some are simpler "support functions" for inter-pipeline data preparation or transformation.

**Parameters** can be set for each module when a pipeline is run and allow for further customization. Each has a default value, so setting them is optional. For instance, one parameterizable item is which specific AI model you want active within a given module.

## Documentation Sections

Krixik Documentation is divided into the following three sections. Dive in!

- [The Krixik System](system/system_overview.md) (including [installation](system/initialization/install_cli.md), [initialization](system/initialization/initialize_and_authenticate.md), [pipeline creation](system/pipeline_creation/create_pipeline.md), [file processing](system/parameters_processing_files_through_pipelines/process_method.md), and more)
- [The Krixik Module Library](modules/modules_overview.md)
- [Krixik Pipeline Examples](examples/pipeline_examples_overview.md)

And we close with a brief note on the [Future of Krixik](future/future_of_krixik.md).

Happy building—if you have any questions or comments, please feel free to reach out via GitHub Issues!
