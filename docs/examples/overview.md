## Multi-module pipeline examples: overview

In this Section we describe an array of multi-module pipelines that can be easily built with krixik.  

We roughly categorize these examples into various subsets based on *either* an key *module* or *concept* shared by each grouping of examples.

- summarize/sentiment centered examples: a collection of pipeline examples roughly centering on the usage of the [summarize](modules/summarize.md) or [sentiment](modules/sentiment.md) modules
    - [recursive summarizer](examples/summarize_sentiment/recursive_summarize.md): build a pipeline to fine tune a specific level of summarization ability by chaining [summarize](modules/summarize.md) multiple times

    - [transcribe to sentiment analysis](examples/summarize_sentiment/transcribe-multilingual-sentiment.md): build a modular pipeline that takes in an audio/video file, transcribes it, and performs sentiment analysis on each sentence of the output transcription

    - [translate to sentiment analysis](examples/summarize_sentiment/translate-sentiment.md): build a modular pipeline that takes in a text file in a non-english language, translates it into english, and performs sentiment analysis on each sentence of the output translation

    - [multilingual transcription to sentiment analysis](examples/summarize_sentiment/translate-sentiment.md): build a modular pipeline that takes in a text file in a non-english language, translates it into english, and performs sentiment analysis on each sentence of the output translation

- transcribe/translate centered examples: a collection of examples roughly centering ono the usage of the[transcribe module](modules/transcribe.md), the [translate](modules/translate.md) module, or both
    - [semantically searchable transcription](examples/transcribe_translate/transcribe-semantic.md): build a modular pipeline that takes in an audio/video file, transcribes it, and makes the result semantically searchable

    - [keyword searchable transcription](examples/transcribe_translate/transcribe-keyword.md): build a modular pipeline that takes in an audio/video file, transcribes it, and makes the result keyword searchable

    - [translate semantic search](examples/transcribe_translate/translate_semantic_search.md): translate any input text file into a different language and make the result semantically searchable

    - [transcription with multilingual translation](examples/transcribe_translate/transcribe-multilingual.md): build a modular pipeline that takes in an audio/video file, transcribes it, and translates the transcription into a target language

    - [semantically searchable multilingual transcription](examples/transcribe_translate/transcribe-multilingual-semantic.md): build a modular pipeline that takes in an audio/video file, transcribes it, translates the transcription into a desired language, and performs semantic search on each sentence of the output

- image-to-text centered examples: pipeline examples centering on the concept of extracting text from images, using [ocr](modules/ocr.md) or [caption](modules/caption.md) modules, and processing it downstream
    - [ocr keyword search](examples/image-to-text/ocr-keyword.md): extract text from input images and make it keyword searchable
    - [caption semantic search](examples/image-to-text/caption-semantic.md): extract text description from an input image and make it semantically searchable

- basic text-search centered examples: pipeline examples centering on the concept of making text searchable
    - [keyword search](examples/text-search/keyword_search.md): make any input text file keyword searchable
    - [semantic search](examples/text-search/semantic_search.md): make any input text file semantically searchable
