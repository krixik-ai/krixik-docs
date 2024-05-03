## modules: overview

This section describes the following currently available modules that may be used in combination to build pipelines.


- [`parser`](modules/parser.md): a module that takes in input documents, cuts them up into pieces using different model logic, and returns the spliced input as json output. 

- [`json-to-txt`](modules/json-to-txt.md): a module that takes as input a json of string snippets, joins them into a single string separated by double spaces, and returns a text file document.

- [`keyword-db`](modules/keyword-db.md): a module that takes as input a document, parses the documents for non-trivial keywords and their lemmatized stems, and returns a database with this content.

- [`vector-db`](modules/vector-db.md): a module that takes as input a numpy array, indexes its vectors, and returns an indexed database.

- [`transcribe`](modules/transcribe.md): a module that takes as input an audio or video file and returns a transcription of spoken words made in the input.  Transcription data is returned as a json.

- [`translate`](modules/translate.md): a module that takes as input a json of text snippets and returns their translations.  Translation data is returned as a json.

- [`caption`](modules/caption.md): a module that takes as input an image and returns a text description of the input image.  Output data is returned as a json.

- [`ocr`](modules/ocr.md): a module that takes as input an image and returns text detected from the input image.  Output data is returned as a json.
