<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/multi_module_non_search_pipeline_examples/multi_sentiment_analysis_on_translated_transcription.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## *Pipeline* Multimodular: Análisis de Sentimiento Sobre Transcripción Traducida

Este documento detalla un *pipeline* multimodular que recibe un archivo de audio, lo [`transcribe`](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md), lo [`traduce`](../../modulos/modulos_ia/modulo_translate_traduccion.md) (por lo pronto al inglés) y hace [`análisis de sentimiento`](../../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md) sobre cada frase transcrita.

El documento está dividido en las siguientes secciones:

- [Monta tu *Pipeline*](#monta-tu-pipeline)
- [Procesa un Archivo de Entrada](#procesa-un-archivo-de-entrada)

### Monta tu *Pipeline*

Para lograr lo arriba descrito, monta un pipeline que consiste de los siguientes módulos en secuencia:

- Un módulo [`transcribe` (transcripción)](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md).

- Un módulo [`translate` (traducción)](../../modulos/modulos_ia/modulo_translate_traduccion.md).

- Un módulo [`json-to-txt`](../../modulos/modulos_de_funciones_de_apoyo/modulo_json-to-txt.md).

- Un módulo [`parser` (fragmentación de texto)](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md).

- Un módulo [`sentiment` (análisis de sentimiento)](../../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md).

Usas la combinación de módulos [`json-to-txt`](../../modulos/modulos_de_funciones_de_apoyo/modulo_json-to-txt.md) y [`parser`](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md), que combina los fragmentos transcritos en un solo documento que luego vuelve a fragmentar, para asegurarte que cualquier quiebre indeseado generado por el ROC no resulte en fragmentos parciales que confundan el modelo de [`análisis de sentimiento`](../../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md).

Para crear el pipeline usarás el método [`create_pipeline`](../../sistema/creacion_de_pipelines/creacion_de_pipelines.md) de la siguiente manera:


```python
# creación del pipeline descrito
pipeline = krixik.create_pipeline(
    name="multi_analisis_de_sentimiento_sobre_transcripcion_traducida",
    module_chain=["transcribe", "translate", "json-to-txt", "parser", "sentiment"]
)
```

### Procesa un Archivo de Entrada

Examina el archivo de prueba antes de continuar. Dado que vas a [`traducir`](../../modulos/modulos_ia/modulo_translate_traduccion.md) antes de hacer [`análisis de sentimiento`](../../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md), arranca con un archivo de audio en español.


```python
# examina el archivo de entrada
import IPython

IPython.display.Audio(data_dir + "input/peso_muerto.mp3")
```





<audio  controls="controls" >
    Your browser does not support the audio element.
</audio>




Dado que el audio de entrada está en español, usarás el modelo no-predeterminado [`opus-mt-es-en`](https://huggingface.co/Helsinki-NLP/opus-mt-es-en) del módulo [`translate`](../../modulos/modulos_ia/modulo_translate_traduccion.md) para traducirlo a inglés. También usarás un modelo más fuerte que el [predeterminado](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md#modelos-disponibles-en-el-modulo-transcribe) para [`transcribir`](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md): usarás [`whisper-base`](https://huggingface.co/openai/whisper-base).

Como usarás los modelos predeterminados para los otros módulos en el *pipeline*, no tendrás que especificarlos en el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).


```python
# procesa el archivo a través del pipeline según lo arriba descrito
process_output = pipeline.process(
    local_file_path=data_dir + "input/peso_muerto.mp3",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False, # no mostrar actualizaciones de proceso al ejecutar el código
    modules={"transcribe": {"model": "whisper-base"}, "translate": {"model": "opus-mt-es-en"}} # especifica modelos no-predeterminados para usar en dos de los módulos del pipeline
)
```

La salida del proceso se reproduce con el siguiente código. Para aprender más sobre cada componente de esta salida, revisa la documentación del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).

Dado que la salida de este modelo/módulo es un archivo JSON, la salida también se incluye en el objeto (esto solo ese el caso para salidas JSON). Además, el archivo de salida se ha guardado en la ubicación indicada bajo `process_output_files`. El `file_id` del archivo procesado es el prefijo del nombre del archivo de salida en esta ubicación.


```python
# nítidamente reproduce la salida de este proceso
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "multi_sentiment_analysis_on_translated_transcription",
      "request_id": "fde9bc3e-5e78-4c72-9f9e-48f2387a7e61",
      "file_id": "6c7c8bf3-8288-40ef-880c-c829f7a39839",
      "message": "SUCCESS - output fetched for file_id 6c7c8bf3-8288-40ef-880c-c829f7a39839.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "The first one is to start with the feet between the width of the hips and the Shoulders, the heels in the ground, a neutral column, medium-potential abdomen, the Shoulders, let's go, looking at them, scholarship the Shoulders are lightly in front of the bar or on the Shoulders, the arms, the right arms, the symmetric hands and an anchored enough to not rather the knees and we can have a lightly front look.",
          "positive": 0.903,
          "negative": 0.097,
          "neutral": 0.0
        },
        {
          "snippet": "To make movement, we will push the heels from the head, we will start to raise the hips and the Shoulders together,",
          "positive": 0.989,
          "negative": 0.011,
          "neutral": 0.0
        }
      ],
      "process_output_files": [
        "../../../data/output/6c7c8bf3-8288-40ef-880c-c829f7a39839.json"
      ]
    }


Para confirmar que todo salió como esperabas, carga el archivo de `process_output_files`:


```python
# carga la salida del proceso del archivo
with open(process_output["process_output_files"][0]) as f:
    print(json.dumps(json.load(f), indent=2))
```

    [
      {
        "snippet": "The first one is to start with the feet between the width of the hips and the Shoulders, the heels in the ground, a neutral column, medium-potential abdomen, the Shoulders, let's go, looking at them, scholarship the Shoulders are lightly in front of the bar or on the Shoulders, the arms, the right arms, the symmetric hands and an anchored enough to not rather the knees and we can have a lightly front look.",
        "positive": 0.903,
        "negative": 0.097,
        "neutral": 0.0
      },
      {
        "snippet": "To make movement, we will push the heels from the head, we will start to raise the hips and the Shoulders together,",
        "positive": 0.989,
        "negative": 0.011,
        "neutral": 0.0
      }
    ]
