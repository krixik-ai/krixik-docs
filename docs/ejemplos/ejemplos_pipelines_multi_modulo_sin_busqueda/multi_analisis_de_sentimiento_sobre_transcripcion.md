<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/multi_module_non_search_pipeline_examples/multi_sentiment_analysis_on_transcription.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## *Pipeline* Multimodular: Análisis de Sentimiento Sobre Transcripción
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/examples/multi_module_non_search_pipeline_examples/multi_sentiment_analysis_on_transcription/)

Este documento detalla un *pipeline* multimodular que recibe un archivo de audio (por lo pronto en inglés), lo [`transcribe`](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md) y hace [`análisis de sentimiento`](../../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md) sobre cada frase transcrita.

El documento está dividido en las siguientes secciones:

- [Monta tu *Pipeline*](#monta-tu-pipeline)
- [Procesa un Archivo de Entrada](#procesa-un-archivo-de-entrada)

### Monta tu *Pipeline*

Para lograr lo arriba descrito, monta un pipeline que consiste de los siguientes módulos en secuencia:

- Un módulo [`transcribe` (transcripción)](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md).

- Un módulo [`json-to-txt`](../../modulos/modulos_de_funciones_de_apoyo/modulo_json-to-txt.md).

- Un módulo [`parser` (fragmentación de texto)](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md).

- Un módulo [`sentiment` (análisis de sentimiento)](../../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md).

Usas la combinación de módulos [`json-to-txt`](../../modulos/modulos_de_funciones_de_apoyo/modulo_json-to-txt.md) y [`parser`](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md), que combina los fragmentos transcritos en un solo documento que luego vuelve a fragmentar, para asegurarte que cualquier quiebre indeseado generado por el ROC no resulte en fragmentos parciales que confundan el modelo de [`análisis de sentimiento`](../../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md).

Para crear el pipeline usarás el método [`create_pipeline`](../../sistema/creacion_de_pipelines/creacion_de_pipelines.md) de la siguiente manera:


```python
# creación del pipeline descrito
pipeline = krixik.create_pipeline(
    name="multi_analisis_de_sentimiento_sobre_transcripcion", module_chain=["transcribe", "json-to-txt", "parser", "sentiment"]
)
```

### Procesa un Archivo de Entrada

Examina el archivo de prueba antes de continuar:


```python
# examina el archivo de entrada
import IPython

IPython.display.Audio(data_dir + "input/video_Colombia.mp3")
```





<audio  controls="controls" >
    Your browser does not support the audio element.
</audio>




Usarás los modelos predeterminados para todo módulo en este *pipeline*, así que el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) no hará falta.


```python
# procesa el archivo a través del pipeline según lo arriba descrito
process_output = pipeline.process(
    local_file_path=data_dir + "input/video_Colombia.mp3",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False,  # no mostrar actualizaciones de proceso al ejecutar el código
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
      "pipeline": "multi_sentiment_analysis_on_transcription",
      "request_id": "25128c62-4bbc-4929-b5af-cb19e579d809",
      "file_id": "8dacac08-f079-4a83-996f-02eefd748776",
      "message": "SUCCESS - output fetched for file_id 8dacac08-f079-4a83-996f-02eefd748776.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": " That's episode looking at the great country of Columbia.",
          "positive": 0.992,
          "negative": 0.008,
          "neutral": 0.0
        },
        {
          "snippet": "We looked at some really basic facts.",
          "positive": 0.252,
          "negative": 0.748,
          "neutral": 0.0
        },
        {
          "snippet": "It's name, a bit of its history, the type of people that live there, land size and all that jazz.",
          "positive": 0.998,
          "negative": 0.002,
          "neutral": 0.0
        },
        {
          "snippet": "But in this video, we're gonna go into a little bit more of a detailed look.",
          "positive": 0.99,
          "negative": 0.01,
          "neutral": 0.0
        },
        {
          "snippet": "Yo, what is going on guys?",
          "positive": 0.005,
          "negative": 0.995,
          "neutral": 0.0
        },
        {
          "snippet": "Welcome back to F2D facts.",
          "positive": 0.999,
          "negative": 0.001,
          "neutral": 0.0
        },
        {
          "snippet": "The channel where I look at people cultures and places, my name is Dave Wouple.",
          "positive": 0.918,
          "negative": 0.082,
          "neutral": 0.0
        },
        {
          "snippet": "And today we are gonna be looking more at Columbia in our Columbia Part 2 video.",
          "positive": 0.015,
          "negative": 0.985,
          "neutral": 0.0
        },
        {
          "snippet": "Which just reminds me guys, this is part of our Columbia playlist.",
          "positive": 0.997,
          "negative": 0.003,
          "neutral": 0.0
        },
        {
          "snippet": "I'll put it down in the description box below and I'll talk about that more at the end of the video.",
          "positive": 0.004,
          "negative": 0.996,
          "neutral": 0.0
        },
        {
          "snippet": "But if you're new here, join me every single Monday to learn about new countries from around the world.",
          "positive": 0.999,
          "negative": 0.001,
          "neutral": 0.0
        },
        {
          "snippet": "You can do that by hitting that subscribe and that belt notification button.",
          "positive": 0.016,
          "negative": 0.984,
          "neutral": 0.0
        },
        {
          "snippet": "But that skits.",
          "positive": 0.024,
          "negative": 0.976,
          "neutral": 0.0
        }
      ],
      "process_output_files": [
        "../../../data/output/8dacac08-f079-4a83-996f-02eefd748776.json"
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
        "snippet": " That's episode looking at the great country of Columbia.",
        "positive": 0.992,
        "negative": 0.008,
        "neutral": 0.0
      },
      {
        "snippet": "We looked at some really basic facts.",
        "positive": 0.252,
        "negative": 0.748,
        "neutral": 0.0
      },
      {
        "snippet": "It's name, a bit of its history, the type of people that live there, land size and all that jazz.",
        "positive": 0.998,
        "negative": 0.002,
        "neutral": 0.0
      },
      {
        "snippet": "But in this video, we're gonna go into a little bit more of a detailed look.",
        "positive": 0.99,
        "negative": 0.01,
        "neutral": 0.0
      },
      {
        "snippet": "Yo, what is going on guys?",
        "positive": 0.005,
        "negative": 0.995,
        "neutral": 0.0
      },
      {
        "snippet": "Welcome back to F2D facts.",
        "positive": 0.999,
        "negative": 0.001,
        "neutral": 0.0
      },
      {
        "snippet": "The channel where I look at people cultures and places, my name is Dave Wouple.",
        "positive": 0.918,
        "negative": 0.082,
        "neutral": 0.0
      },
      {
        "snippet": "And today we are gonna be looking more at Columbia in our Columbia Part 2 video.",
        "positive": 0.015,
        "negative": 0.985,
        "neutral": 0.0
      },
      {
        "snippet": "Which just reminds me guys, this is part of our Columbia playlist.",
        "positive": 0.997,
        "negative": 0.003,
        "neutral": 0.0
      },
      {
        "snippet": "I'll put it down in the description box below and I'll talk about that more at the end of the video.",
        "positive": 0.004,
        "negative": 0.996,
        "neutral": 0.0
      },
      {
        "snippet": "But if you're new here, join me every single Monday to learn about new countries from around the world.",
        "positive": 0.999,
        "negative": 0.001,
        "neutral": 0.0
      },
      {
        "snippet": "You can do that by hitting that subscribe and that belt notification button.",
        "positive": 0.016,
        "negative": 0.984,
        "neutral": 0.0
      },
      {
        "snippet": "But that skits.",
        "positive": 0.024,
        "negative": 0.976,
        "neutral": 0.0
      }
    ]
