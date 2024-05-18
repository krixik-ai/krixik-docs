## Multi-Module Pipeline: Semantically-Searchable Translation

This document details a modular pipeline that takes in text, [`translates`](../modules/ai_model_modules/translate_module.md) it into a desired language, and makes the result [`semantically searchable`](../system/search_methods/semantic_search_method.md).

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)
- [Performing Semantic Search](#performing-semantic-search)

### Pipeline Setup

To achieve what we've described above, let's set up a pipeline sequentially consisting of the following modules:

- A [`parser`](../modules/ai_model_modules/parser_module.md) module.

- A [`translate`](../modules/ai_model_modules/translate_module.md) module.

- A [`text-embedder`](../modules/ai_model_modules/text-embedder_module.md) module.

- A [`vector-db`](../modules/database_modules/vector-db_module.md) module.

We do this by leveraging the [`.create_pipeline`](../system/pipeline_creation/create_pipeline.md) method, as follows:


```python
# create a pipeline as detailed above

pipeline_1 = krixik.create_pipeline(name="multi_keyword_searchable_transcription",
                                    module_chain=["parser",
                                                  "translate",
                                                  "text-embedder",
                                                  "vector-db"])
```

### Processing an Input File

Lets take a quick look at a test file before processing.


```python
# examine contents of input file

with open("../../../data/input/don_esp.txt", "r") as file:
    print(file.read())
```

    PRÓLOGO
    
    Desocupado lector: sin juramento me podrás creer que quisiera que este
    libro, como hijo del entendimiento, fuera el más hermoso, el más gallardo y
    más discreto que pudiera imaginarse. Pero no he podido yo contravenir al
    orden de naturaleza; que en ella cada cosa engendra su semejante. Y así,
    ¿qué podrá engendrar el estéril y mal cultivado ingenio mío, sino la
    historia de un hijo seco, avellanado, antojadizo y lleno de pensamientos
    varios y nunca imaginados de otro alguno, bien como quien se engendró en
    una cárcel, donde toda incomodidad tiene su asiento y donde todo triste
    ruido hace su habitación? El sosiego, el lugar apacible, la amenidad de los
    campos, la serenidad de los cielos, el murmurar de las fuentes, la quietud
    del espíritu son grande parte para que las musas más estériles se muestren
    fecundas y ofrezcan partos al mundo que le colmen de maravilla y de
    contento. Acontece tener un padre un hijo feo y sin gracia alguna, y el
    amor que le tiene le pone una venda en los ojos para que no vea sus faltas,
    antes las juzga por discreciones y lindezas y las cuenta a sus amigos por
    agudezas y donaires. Pero yo, que, aunque parezco padre, soy padrastro de
    Don Quijote, no quiero irme con la corriente del uso, ni suplicarte, casi
    con las lágrimas en los ojos, como otros hacen, lector carísimo, que
    perdones o disimules las faltas que en este mi hijo vieres; y ni eres su
    pariente ni su amigo, y tienes tu alma en tu cuerpo y tu libre albedrío
    como el más pintado, y estás en tu casa, donde eres señor della, como el
    rey de sus alcabalas, y sabes lo que comúnmente se dice: que debajo de mi
    manto, al rey mato. Todo lo cual te esenta y hace libre de todo respecto y
    obligación; y así, puedes decir de la historia todo aquello que te
    pareciere, sin temor que te calunien por el mal ni te premien por el bien
    que dijeres della.


Since the input text is in Spanish, we'll use the (non-default) [`opus-mt-es-en`](https://huggingface.co/Helsinki-NLP/opus-mt-es-en) model of the [`translate`](../modules/ai_model_modules/translate_module.md) module to translate it into English.

We will use the default models for every other module in the pipeline, so they don't have to be specified in the [`modules`](../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file through the pipeline, as described above

process_output_1 = pipeline_1.process(local_file_path = "../../../data/input/don_esp.txt", # the initial local filepath where the input file is stored
                                      local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                      expire_time=60*30, # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True, # wait for process to complete before returning IDE control to user
                                      verbose=False, # do not display process update printouts upon running code
                                      modules={"translate": {"model": "opus-mt-es-en"}}) # specify a non-default model for use in the translate module
```

    INFO: hydrated input modules: {'module_1': {'model': 'sentence', 'params': {}}, 'module_2': {'model': 'opus-mt-es-en', 'params': {}}, 'module_3': {'model': 'base', 'params': {}}}
    INFO: symbolic_directory_path was not set by user - setting to default of /etc
    INFO: file_name was not set by user - setting to random file name: krixik_generated_file_name_bkryhqmkdo.txt
    INFO: wait_for_process is set to True.
    INFO: file will expire and be removed from you account in 600 seconds, at Tue May  7 12:45:30 2024 UTC
    INFO: examples-translate-text-search-pipeline file process and input processing started...
    INFO: metadata can be updated using the .update api.
    INFO: This process's request_id is: 890866e1-3a68-1927-5439-628eac7dca13
    INFO: File process and processing status:
    SUCCESS: module 1 (of 3) - parser processing complete.
    SUCCESS: module 2 (of 3) - translate processing complete.
    SUCCESS: module 3 (of 3) - json-to-txt processing complete.
    SUCCESS: pipeline process complete.
    SUCCESS: process output downloaded


The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a [FAISS](https://github.com/facebookresearch/faiss) database file, `process_output` is "null". However, the output file has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process

print(json.dumps(process_output_1, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "examples-translate-text-search-pipeline",
      "request_id": "d8363ef8-4fe9-4ba1-904a-76a603a8d4d3",
      "file_id": "8b907667-1472-4130-83f5-9b4a82bdb5ee",
      "message": "SUCCESS - output fetched for file_id 8b907667-1472-4130-83f5-9b4a82bdb5ee.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/8b907667-1472-4130-83f5-9b4a82bdb5ee.txt"
      ]
    }


### Performing Semantic Search

Krixik's [`.semantic_search`](../system/search_methods/semantic_search_method.md) method enables semantic search on documents processed through certain pipelines. Given that the [`.semantic_search`](../system/search_methods/semantic_search_method.md) method both [embeds](../modules/ai_model_modules/text-embedder_module.md) the query and performs the search, it can only be used with pipelines containing both a [`text-embedder`](../modules/ai_model_modules/text-embedder_module.md) module and a [`vector-db`](../modules/database_modules/vector-db_module.md) module in immediate succession.

Since our pipeline satisfies this condition, it has access to the [`.semantic_search`](../system/search_methods/semantic_search_method.md) method. Let's use it to query our text with natural language, as shown below:


```python
# perform semantic_search over the file in the pipeline

semantic_output_1 = pipeline_1.semantic_search(query="Sterile ideas bring little to man", 
                                               file_ids=["XXXXX"])

# nicely print the output of this process

print(json.dumps(semantic_output_1, indent=2))
```

    {
      "status_code": 200,
      "request_id": "d88bf437-a742-41c1-8b28-5981d5c44bcc",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "e0024f60-9192-4e05-8bb3-a0a0423305ab",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_tnzlfqdsly.mp3",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 41,
            "created_at": "2024-04-29 22:57:52",
            "last_updated": "2024-04-29 22:57:52"
          },
          "search_results": [
            {
              "snippet": "Learn about Columbia.",
              "line_numbers": [
                1
              ],
              "distance": 0.263
            },
            {
              "snippet": "And I know coffee is really important when it comes to talking about Columbia, but you guys really don't know how important it is with its culture.",
              "line_numbers": [
                1
              ],
              "distance": 0.287
            },
            {
              "snippet": "You Columbia coffee right here.",
              "line_numbers": [
                1
              ],
              "distance": 0.292
            },
            {
              "snippet": "Now interesting enough when it comes to the coffee in Columbia, believe it or not, it is not actually native to the country.",
              "line_numbers": [
                1
              ],
              "distance": 0.298
            },
            {
              "snippet": "So we all know Columbia is famous for its coffee, right?",
              "line_numbers": [
                1
              ],
              "distance": 0.306
            }
          ]
        }
      ]
    }



```python
# delete all processed datapoints belonging to this pipeline

reset_pipeline(pipeline_1)
```
