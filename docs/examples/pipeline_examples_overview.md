## Krixik Pipeline Examples

Ready to see some pipeline examples to draw inspiration from? Let's dive in!

The first section below details every single-module pipeline buildable today. Use these if there is one particular module you'd like to leverage by itself.

Then we delve into a few examples of multi-module pipelines, which is where the power of Krixik really shines through. We close with a look at multi-module search-enabled pipelines, whose functionality is slightly different from the rest.

### Single-Module Pipelines

- [Image Caption](single_module_pipelines/single_caption.md)

- [OCR](single_module_pipelines/single_ocr.md)

- [Sentiment Analysis](single_module_pipelines/single_sentiment.md)

- [Summarizer](single_module_pipelines/single_summarize.md)

- [Text Embedder](single_module_pipelines/single_text-embedder.md)

- [Parser](single_module_pipelines/single_parser.md)

- [Transcriber](single_module_pipelines/single_transcribe.md)

- [Translator](single_module_pipelines/single_translate.md)

- [Keyword Database](single_module_pipelines/single_keyword-db.md)

- [Vector Database](single_module_pipelines/single_vector-db.md)

- [JSON to TXT](single_module_pipelines/single_json-to-txt.md)

### Multi-Module Pipelines (non-search)

- [Recursive Summarization](multi_module_non_search_pipeline_examples/multi_recursive_summarization.md): Chains multiple text [`summarize`](../modules/ai_modules/summarize_module.md) modules together. The longer the module chain, the greater the degree of summarization.

- [Translated Transcription](multi_module_non_search_pipeline_examples/multi_translated_transcription.md): After [`transcribing`](../modules/ai_modules/transcribe_module.md) an input audio file, [`translates`](../modules/ai_modules/translate_module.md) the transcript into the language of your choice.

- [Sentiment Analysis on Transcription](multi_module_non_search_pipeline_examples/multi_sentiment_analysis_on_transcription.md): After [`transcribing`](../modules/ai_modules/transcribe_module.md) an input audio file, performs [`sentiment analysis`](../modules/ai_modules/sentiment_module.md) on each sentence of the transcript.

- [Sentiment Analysis on Translation](multi_module_non_search_pipeline_examples/multi_sentiment_analysis_on_translation.md): [`Translates`](../modules/ai_modules/translate_module.md) input text into English and then perfoms [`sentiment analysis`](../modules/ai_modules/sentiment_module.md) on each sentence of the translation.

- [Sentiment Analysis on Translated Transcription](multi_module_non_search_pipeline_examples/multi_sentiment_analysis_on_translated_transcription.md): After first [`transcribing`](../modules/ai_modules/transcribe_module.md) an input audio file and then [`translating`](../modules/ai_modules/translate_module.md) the transcript into English, performs [`sentiment analysis`](../modules/ai_modules/sentiment_module.md) on each sentence of the translation.

### Multi-Module Search Pipelines

- [Search Pipeline Overview](search_pipeline_examples/search_pipelines_overview.md): Search pipelines call for the use of one of two additional methods. Read about it here.

- [Semantic Search](search_pipeline_examples/multi_basic_semantic_search.md): Enables `semantic search` on an input text file.

- [Semantic Search on Snippets](search_pipeline_examples/multi_snippet_semantic_search.md): Enables `semantic search` on snippets in an input JSON file.

- [Keyword Search](search_pipeline_examples/multi_basic_keyword-search.md): Enables `keyword search` on an input text file.

- [Semantically-Searchable Transcription](search_pipeline_examples/multi_semantically_searchable_transcription.md): [`Transcribes`](../modules/ai_modules/transcribe_module.md) an input audio file and then enables `semantic search` on the transcript.

- [Keyword-Searchable Transcription](search_pipeline_examples/multi_keyword_searchable_transcription.md): [`Transcribes`](../modules/ai_modules/transcribe_module.md) an input audio file and then enables `keyword search` on the transcript.

- [Semantically-Searchable Translation](search_pipeline_examples/multi_semantically_searchable_translation.md): [`Translates`](../modules/ai_modules/translate_module.md) an input text file and then enables `semantic search` on the translation.

- [Semantically-Searchable Translated Transcription](search_pipeline_examples/multi_semantically_searchable_translated_transcription.md): [`Transcribes`](../modules/ai_modules/transcribe_module.md) an input audio file, [`translates`](../modules/ai_modules/translate_module.md) it into English, and then enables `semantic search` on the translation.

- [Semantically-Searchable OCR](search_pipeline_examples/multi_semantically_searchable_ocr.md): [`Extracts text`](../modules/ai_modules/ocr_module.md) from an input image and then enables `semantic search` on the extracted text.

- [Keyword-Searchable Image Captions](search_pipeline_examples/multi_keyword_searchable_image_captions.md): Generates a [`textual caption`](../modules/ai_modules/caption_module.md) for an input image and then enables `keyword search` on the caption.
