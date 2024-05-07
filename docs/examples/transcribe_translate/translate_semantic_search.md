## Semantically searchable translation

This document reviews a semantic search pipeline that can be used to make an input text in a specific language semantically-searchable in another language.


- [pipeline setup](#pipeline-setup)
- [processing an input file](#processing-an-input-file)


## Pipeline setup

Below we setup a two pipelines.

The first is a single module pipeline consisting of [`translate`](modules/translate.md).

The latter consists of a [`translate`](modules/translate.md), [`parser`](modules/parser.md), [`text-embedder`](modules/text-embedder.md), and [`vector-db`](modules/vector-db.md) modules.  This will allow us to translate input files and make them semantically searchable.

We do this by passing the module names to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a multi module pipeline to translate an input text file
translate_pipeline = krixik.create_pipeline(name="examples-translate-text-search-pipeline",
                                            module_chain=["parser", 
                                                          "translate", 
                                                          "json-to-txt"])

# create a pipeline with a multi module
pipeline = krixik.create_pipeline(name="examples-translate-text-search-semantic-pipeline",
                                  module_chain=["parser", 
                                                "translate", 
                                                "json-to-txt", 
                                                "parser",
                                                "text-embedder", 
                                                "vector-db"])
```

This pipeline's available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).

## Processing an input file

Lets take a quick look at a short test file before processing.


```python
# examine contents of input file
test_file = "../../../data/input/don_esp.txt"
with open(test_file, "r") as file:
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


Below we [process](system/process.md) the input through our pipeline using the default model for each of our three modules.


```python
# define path to an input file from examples directory
test_file = "../../../data/input/don_esp.txt"

# process a file through the pipeline
process_output = translate_pipeline.process(local_file_path = test_file,
                                            local_save_directory="../../../data/output",  # save output in current directory
                                            expire_time=60*10,         # set all process data to expire in 5 minutes
                                            wait_for_process=True,     # wait for process to complete before regaining ide
                                            verbose=True,              # set verbosity to False
                                            modules={"translate": {"model": "opus-mt-es-en"}})
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


The output of this process is printed below.  Because the output of this particular pipeline pair is text, the process output is provided in this object is null.  However the file itself has been returned to the address noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
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


We load in the text file output from `process_output_files` below. 


```python
# load in process output from file
import json
with open(process_output["process_output_files"][0], "r") as file:
    print(file.read())
```

    PRLOGO Unoccupied reader: without oath you can believe me that I would want this book, as a son of understanding, to be the most beautiful, the most gallant and discreet that could be imagined.
    But I have not been able to contradict the order of nature; for in it every thing begets its fellowman.
    And so, what can breed the strill and ill-cultivated wit mo, but the story of a dry son, haphazard, craving and full of various thoughts and never imagined of any other, well as who begets in a crcel, where all discomfort has its seat and where all sad noise makes its habitation?
    The quietness, the peaceful place, the abundance of the fields, the serenity of the heavens, the murmuring of the fountains, the stillness of the spirit are a great part for the most strile muses to show themselves fruitful and to give birth to the world that fills it with wonder and contentment.
    It happens to have a father an ugly son with no grace at all, and the love he has puts a blindfold in his eyes so that he does not see his faults, but judges them by discretions and lindezas and tells his friends for acuity and donaires.
    But I, who, though I look like a father, am Don Quixote's stepfather, do not want to go away with the current of use, nor beg you, almost with the tears in your eyes, as others do, hearty reader, to forgive or to dispel the faults that you see in this my son; and you are neither his relative nor his friend, and you have your soul in your body and your free albedro as the most painted, and you are in your house, where you are seor della, as the king of his palaces, and you know what is commonly said: that under my robe, I kill the king.
    All that sitteth upon thee, and maketh thee free from all things, and from all things, and from all things that seem unto thee, thou canst say of history, without fear that they may call thee to evil, nor reward thee for the good which thou sayest of it.


We now process the file with our second pipeline - which will make the outupt searchable in english.

We will specify the models we want for the `translate` and second `parser` module using the `modules` argument of the [`process` method](system/process.md).  This will look like

```python
        modules={
            "module_2": {"model": "opus-mt-es-en"},
            "module_4": {"model": "fixed", 
                        "params": {"chunk_size": 12,
                                    "overlap_size": 6}}
                }
```

When using mutliple instances of the same module - as we do here (the `parser` module is used twice) - we must instantiate the models based on the module order.  So here `module_2` references our `translate` module, and `module_4` the second `parser` in our `module_chain`.


```python
# define path to an input file from examples directory
test_file = "../../../data/input/don_esp.txt"

# process a file through the pipeline
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory="../../../data/output",  # save output in current directory
                                  expire_time=60*10,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,     # wait for process to complete before regaining ide
                                  verbose=True,              # set verbosity to False
                                  modules={
                                      "module_2": {"model": "opus-mt-es-en"},
                                      "module_4": {"model": "fixed", 
                                                   "params": {"chunk_size": 12,
                                                              "overlap_size": 6}}
                                           })
```

    INFO: hydrated input modules: {'module_1': {'model': 'sentence', 'params': {}}, 'module_2': {'model': 'opus-mt-es-en', 'params': {}}, 'module_3': {'model': 'base', 'params': {}}, 'module_4': {'model': 'fixed', 'params': {'chunk_size': 12, 'overlap_size': 6}}, 'module_5': {'model': 'all-MiniLM-L6-v2', 'params': {'quantize': True}}, 'module_6': {'model': 'faiss', 'params': {}}}
    INFO: symbolic_directory_path was not set by user - setting to default of /etc
    INFO: file_name was not set by user - setting to random file name: krixik_generated_file_name_omgbefdcqw.txt
    INFO: wait_for_process is set to True.
    INFO: file will expire and be removed from you account in 600 seconds, at Tue May  7 12:53:00 2024 UTC
    INFO: examples-translate-text-search-semantic-pipeline file process and input processing started...
    INFO: metadata can be updated using the .update api.
    INFO: This process's request_id is: 2a37b4d8-629f-e350-77f3-4ed37b04a7c0
    INFO: File process and processing status:
    SUCCESS: module 2 (of 5) - translate processing complete.
    SUCCESS: module 1 (of 5) - parser processing complete.
    SUCCESS: module 3 (of 5) - json-to-txt processing complete.
    SUCCESS: module 4 (of 5) - text-embedder processing complete.
    SUCCESS: module 5 (of 5) - vector-db processing complete.
    SUCCESS: pipeline process complete.
    SUCCESS: process output downloaded


## Using the `semantic_search` method

krixik's [`semantic_search` method](system/semantic_search.md) is a convenience function for both embedding and querying - and so can only be used with pipelines containing both `text-embedder` and `vector-db` modules in succession.  Since our pipeline here satisfies this condition, it has access to the `semantic_search` method.

Now we can query our text with natural language as shown below.


```python
# perform semantic_search over the input file
semantic_output = pipeline.semantic_search(
    query="an unattractive son", file_ids=[process_output["file_id"]]
)

# nicely print the output of this process
print(json.dumps(semantic_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "4edd8fd4-4c5e-486b-8e95-9b9a1462bcf0",
      "message": "Successfully queried 1 user file.",
      "warnings": [],
      "items": [
        {
          "file_id": "accccba9-5326-4fae-89f9-84e55fd2af4e",
          "file_metadata": {
            "file_name": "krixik_generated_file_name_omgbefdcqw.txt",
            "symbolic_directory_path": "/etc",
            "file_tags": [],
            "num_vectors": 60,
            "created_at": "2024-05-07 19:43:03",
            "last_updated": "2024-05-07 19:43:03"
          },
          "search_results": [
            {
              "snippet": "a father an ugly son with no grace at all, and the",
              "line_numbers": [
                5
              ],
              "distance": 0.195
            },
            {
              "snippet": "that you see in this my son; and you are neither his",
              "line_numbers": [
                6
              ],
              "distance": 0.224
            },
            {
              "snippet": "son; and you are neither his relative nor his friend, and you",
              "line_numbers": [
                6
              ],
              "distance": 0.247
            },
            {
              "snippet": "and contentment. It happens to have a father an ugly son with",
              "line_numbers": [
                4,
                5
              ],
              "distance": 0.257
            },
            {
              "snippet": "I look like a father, am Don Quixote's stepfather, do not want",
              "line_numbers": [
                6
              ],
              "distance": 0.281
            }
          ]
        }
      ]
    }

