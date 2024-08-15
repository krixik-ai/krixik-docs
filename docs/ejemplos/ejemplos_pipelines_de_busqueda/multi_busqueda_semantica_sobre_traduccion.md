<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/search_pipeline_examples/multi_semantically_searchable_translation.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## *Pipeline* Multimodular: Búsqueda Semántica Sobre Traducción
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/examples/search_pipeline_examples/multi_semantically_searchable_translation/)

Este documento detalla un *pipeline* multimodular que recibe un archivo de texto como entrada, [traduce el texto](../../modulos/modulos_ia/modulo_translate_traduccion.md) a otro idioma, y habilita [búsqueda semántica](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) sobre la traducción.

El documento se divide en las siguientes secciones:

- [Monta tu *Pipeline*](#monta-tu-pipeline)
- [Procesa un Archivo de Entrada](#procesa-un-archivo-de-entrada)
- [Búsqueda Semántica](#busqueda-semantica)

### Monta tu *Pipeline*

Para lograr lo arriba descrito, monta un pipeline que consiste de los siguientes módulos en secuencia:

- Un módulo [`parser` (fragmentación de texto)](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md).

- Un módulo [`translate` (traducción)](../../modulos/modulos_ia/modulo_translate_traduccion.md)

- Un módulo [`text-embedder` (encaje léxico)](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md).

- Un módulo [`vector-db` (base de datos vectorial)](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md).

Para esto usarás el método [`create_pipeline`](../../sistema/creacion_de_pipelines/creacion_de_pipelines.md) de la siguiente manera:


```python
# creación del pipeline descrito
pipeline = krixik.create_pipeline(
    name="multi_busqueda_semantica_sobre_traduccion", module_chain=["parser", "translate", "text-embedder", "vector-db"]
)
```

### Procesa un Archivo de Entrada

Examina el archivo de prueba antes de continuar:


```python
# examina el archivo de entrada
with open(data_dir + "input/don_quijote_esp.txt", "r") as file:
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


Dado que el texto de entrada está en español, usarás uno de los modelos no-predeterminados del módulo [`translate` (traducción)](../../modulos/modulos_ia/modulo_translate_traduccion.md) para traducirlo a inglés: [`opus-mt-es-en`](https://huggingface.co/Helsinki-NLP/opus-mt-es-en).

<u>Sí</u> usarás los modelos predeterminados para el resto de los módulos de este *pipeline*, así que no hace falta especificarlos en el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).


```python
# procesa el archivo a través del pipeline según lo arriba descrito
process_output = pipeline.process(
    local_file_path=data_dir + "input/don_quijote_esp.txt",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False,  # no mostrar actualizaciones de proceso al ejecutar el código
    modules={"translate": {"model": "opus-mt-es-en"}},  # especificar un modelo no-predeterminado para el módulo de traducción
)
```

Reproduce la salida de este proceso con el siguiente código. Para aprender más sobre cada componente de la salida, estudia la documentación del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).

Dado que la salida de este modelo/módulo es un archivo de base de datos [FAISS](https://github.com/facebookresearch/faiss), `process_output` se muestra como "null". Sin embargo, el archivo de salida se ha guardado en la ubicación indicada bajo `process_output_files`. El `file_id` del archivo procesado es el prefijo del nombre del archivo de salida en esta ubicación.


```python
# nítidamente reproduce la salida de este proceso
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


### Busqueda Semantica

El método [`semantic_search`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) de Krixik habilita búsqueda semántica sobre documentos procesados a través de ciertos *pipelines*. Dado que el método [`semantic_search`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) hace [`embedding` (encaje léxico)](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md) con la consulta y luego lleva a cabo la búsqueda, solo se puede usar con *pipelines* que de manera consecutiva contienen los módulos [`text-embedder` (encaje léxico)](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md) y [`vector-db` (base de datos vectorial)](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md).

Ya que tu *pipeline* satisface esta condición tiene acceso al método [`semantic_search`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md). Úsalo de la siguiente manera para consultar el texto con lengua natural:


```python
# haz búsqueda semántica sobre la traducción generada por el pipeline
semantic_output = pipeline.semantic_search(query="Sterile ideas bring little to man", file_ids=[process_output["file_id"]])

# nítidamente reproduce la salida de esta búsqueda
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

