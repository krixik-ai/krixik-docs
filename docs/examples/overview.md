## multi-module pipeline examples: overview

In this Section we describe an array of multi-module pipelines that can be easily built with krixik.  We roughly categorize these examples into various subsets based on an important module shared by each grouping of examples.


- summarize-centered examples: a collection of pipeline examples roughly centering on the usage of the [summarize module](modules/summarize.md)
    - [recursive summarizer](examples/summarize/recursive_summarize.md): build a pipeline to fine tune a specific level of summarization ability by chaining [summarize](modules/summarize.md) multiple times


- transcribe-centered examples: a collection of examples roughly centering ono the usage of the[transcribe module](modules/transcribe.md)
    - [semantically searchable transcription](examples/transcribe/transcribe-semantic.md): learn how to build a modular pipeline that takes in an audio/video file, transcribes it, and makes the result semantically searchable.

    - [transcription with multilingual translation](examples/transcribe/transcribe-multilingual.md): learn how to build of a modular pipeline that takes in an audio/video file, transcribes it, and makes the result semantically searchable.

    - [semantically searchable multilingual transcription](examples/transcribe/transcribe-multilingual-semantic.md): learn how to build of a modular pipeline that takes in an audio/video file, transcribes it, translates the transcription into a desired language, and makes the result semantically searchable.

    - [transcription to sentiment analysis](examples/transcribe/transcribe-sentiment.md): learn how to build a modular pipeline that takes in an audio/video file, transcribes it, and performs sentiment analysis on each sentence of the output transcription.



