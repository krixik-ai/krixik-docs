<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/search_pipeline_examples/multi_semantically_searchable_translation.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Multi-Module Pipeline: Semantically-Searchable Translation

This document details a modular pipeline that takes in text, [`translates`](../../modules/ai_modules/translate_module.md) it into a desired language, and makes the result [`semantically searchable`](../../system/search_methods/semantic_search_method.md).

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)
- [Performing Semantic Search](#performing-semantic-search)

### Pipeline Setup

To achieve what we've described above, let's set up a pipeline sequentially consisting of the following modules:

- A [`parser`](../../modules/support_function_modules/parser_module.md) module.

- A [`translate`](../../modules/ai_modules/translate_module.md) module.

- A [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) module.

- A [`vector-db`](../../modules/database_modules/vector-db_module.md) module.

We do this by leveraging the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method, as follows:


```python
# create a pipeline as detailed above
pipeline = krixik.create_pipeline(
    name="multi_semantically_searchable_translation", module_chain=["parser", "translate", "text-embedder", "vector-db"]
)
```

### Processing an Input File

Lets take a quick look at a test file before processing.


```python
# examine contents of input file
with open(data_dir + "input/don_esp.txt", "r") as file:
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


Since the input text is in Spanish, we'll use the (non-default) [`opus-mt-es-en`](https://huggingface.co/Helsinki-NLP/opus-mt-es-en) model of the [`translate`](../../modules/ai_modules/translate_module.md) module to translate it into English.

We will use the default models for every other module in the pipeline, so they don't have to be specified in the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.


```python
# process the file through the pipeline, as described above
process_output = pipeline.process(
    local_file_path=data_dir + "input/don_esp.txt",  # the initial local filepath where the input file is stored
    local_save_directory=data_dir + "output",  # the local directory that the output file will be saved to
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # wait for process to complete before returning IDE control to user
    verbose=False,  # do not display process update printouts upon running code
    modules={"translate": {"model": "opus-mt-es-en"}},
)  # specify a non-default model for use in the translate module
```

The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a [FAISS](https://github.com/facebookresearch/faiss) database file, `process_output` is "null". However, the output file has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "multi_semantically_searchable_translation",
      "request_id": "68b21796-7c9a-4834-8848-d4aeb95b8a57",
      "file_id": "d51f32f5-09d1-4656-a0d5-5da9bdb0a69c",
      "message": "SUCCESS - output fetched for file_id d51f32f5-09d1-4656-a0d5-5da9bdb0a69c.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/d51f32f5-09d1-4656-a0d5-5da9bdb0a69c.faiss"
      ]
    }


### Performing Semantic Search

Krixik's [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method enables semantic search on documents processed through certain pipelines. Given that the [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method both [embeds](../../modules/ai_modules/text-embedder_module.md) the query and performs the search, it can only be used with pipelines containing both a [`text-embedder`](../../modules/ai_modules/text-embedder_module.md) module and a [`vector-db`](../../modules/database_modules/vector-db_module.md) module in immediate succession.

Since our pipeline satisfies this condition, it has access to the [`.semantic_search`](../../system/search_methods/semantic_search_method.md) method. Let's use it to query our text with natural language, as shown below:


```python
# perform semantic_search over the file in the pipeline
semantic_output = pipeline.semantic_search(query="Sterile ideas bring little to man", file_ids=[process_output["file_id"]])

# nicely print the output of this process
print(json.dumps(semantic_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "0442dfa7-1069-407a-9e44-0357f48fdf32",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "d51f32f5-09d1-4656-a0d5-5da9bdb0a69c",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_zvwkdkrayg.txt",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 7,
            "created_at": "2024-06-05 14:57:07",
            "last_updated": "2024-06-05 14:57:07"
          },
          "search_results": [
            {
              "snippet": "And so, what can breed the strill and ill-cultivated wit mo, but the story of a dry son, haphazard, craving and full of various thoughts and never imagined of any other, well as who begets in a crcel, where all discomfort has its seat and where all sad noise makes its habitation?",
              "line_numbers": [
                3
              ],
              "distance": 0.361
            },
            {
              "snippet": "The quietness, the peaceful place, the abundance of the fields, the serenity of the heavens, the murmuring of the fountains, the stillness of the spirit are a great part for the most strile muses to show themselves fruitful and to give birth to the world that fills it with wonder and contentment.",
              "line_numbers": [
                4
              ],
              "distance": 0.404
            },
            {
              "snippet": "It happens to have a father an ugly son with no grace at all, and the love he has puts a blindfold in his eyes so that he does not see his faults, but judges them by discretions and lindezas and tells his friends for acuity and donaires.",
              "line_numbers": [
                5
              ],
              "distance": 0.413
            },
            {
              "snippet": "But I, who, though I look like a father, am Don Quixote's stepfather, do not want to go away with the current of use, nor beg you, almost with the tears in your eyes, as others do, hearty reader, to forgive or to dispel the faults that you see in this my son; and you are neither his relative nor his friend, and you have your soul in your body and your free albedro as the most painted, and you are in your house, where you are seor della, as the king of his palaces, and you know what is commonly said: that under my robe, I kill the king.",
              "line_numbers": [
                6
              ],
              "distance": 0.422
            },
            {
              "snippet": "But I have not been able to contradict the order of nature; for in it every thing begets its fellowman.",
              "line_numbers": [
                2
              ],
              "distance": 0.426
            }
          ]
        }
      ]
    }

