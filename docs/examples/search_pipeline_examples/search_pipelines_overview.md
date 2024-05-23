## Krixik Search Pipelines

### Search Pipeline Overview

Search pipelines are those that enable document search  on input text files.

Two types of document search can be enabled: [semantic search](../../system/search_methods/semantic_search_method.md) and [keyword search](../../system/search_methods/keyword_search_method.md). Depending on which of these is sought, the final module of the pipeline must respectively be [`vector-db`](../../modules/database_modules/vector-db_module.md) or [`keyword-db`](../../modules/database_modules/keyword-db_module.md).

Search pipelines are more complex than other pipelines because they require an additional step.

- Files must first be "loaded" into the the pipeline with the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

- The [`.keyword_search`](../../system/search_methods/keyword_search_method.md) or [`.semantic_search`](../../system/search_methods/semantic_search_method.md) methods can be invoked on a search pipeline once at least one file has been [processed](../../system/parameters_processing_files_through_pipelines/process_method.md) through it. Keep in mind that the [`.keyword_search`](../../system/search_methods/keyword_search_method.md) method can only be invoked on a pipeline that ends with [`keyword-db`](../../modules/database_modules/keyword-db_module.md), and the [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method can only be invoked on a pipeline that ends with [`vector-db`](../../modules/database_modules/vector-db_module.md).

### Search Pipeline Examples

- [Semantic Search](multi_basic_semantic_search.md): Enables [`semantic search`](../../system/search_methods/semantic_search_method.md) on an input text file.

- [Semantic Search on Snippets](multi_snippet_semantic_search.md): Enables [`semantic search`](../../system/search_methods/semantic_search_method.md) on snippets in an input JSON file.

- [Keyword Search](multi_basic_keyword-search.md): Enables [`keyword search`](../../system/search_methods/keyword_search_method.md) on an input text file.

- [Semantically-Searchable Transcription](multi_semantically_searchable_transcription.md): [`Transcribes`](../../modules/ai_modules/transcribe_module.md) an input audio file and then enables [`semantic search`](../../system/search_methods/semantic_search_method.md) on the transcript.

- [Keyword-Searchable Transcription](multi_keyword_searchable_transcription.md): [`Transcribes`](../../modules/ai_modules/transcribe_module.md) an input audio file and then enables [`keyword search`](../../system/search_methods/keyword_search_method.md) on the transcript.

- [Semantically-Searchable Translation](multi_semantically_searchable_translation.md): [`Translates`](../../modules/ai_modules/translate_module.md) an input text file and then enables [`semantic search`](../../system/search_methods/semantic_search_method.md) on the translation.

- [Semantically-Searchable Translated Transcription](multi_semantically_searchable_translated_transcription.md): [`Transcribes`](../../modules/ai_modules/transcribe_module.md) an input audio file, [`translates`](../../modules/ai_modules/translate_module.md) it into English, and then enables [`semantic search`](../../system/search_methods/semantic_search_method.md) on the translation.

- [Semantically-Searchable OCR](multi_semantically_searchable_ocr.md): [`Extracts text`](../../modules/ai_modules/ocr_module.md) from an input image and then enables [`semantic search`](../../system/search_methods/semantic_search_method.md) on the extracted text.

- [Keyword-Searchable Image Captions](multi_keyword_searchable_image_captions.md): Generates a [`textual caption`](../../modules/ai_modules/caption_module.md) for an input image and then enables [`keyword search`](../../system/search_methods/keyword_search_method.md) on the caption.
