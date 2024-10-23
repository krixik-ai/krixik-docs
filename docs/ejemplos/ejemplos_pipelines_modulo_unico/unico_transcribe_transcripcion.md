<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/single_module_pipelines/single_transcribe.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## *Pipeline* de Módulo Único: `transcribe` (Transcripción)
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/examples/single_module_pipelines/single_transcribe/)

Este documento presenta una guía de cómo ensamblar y consumir un *pipeline* de módulo único que solo incluye un módulo [`transcribe` (transcripción)](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md). Se divide en las siguientes secciones:

- [Monta tu *Pipeline*](#monta-tu-pipeline)
- [Formato de Entrada Requerido](#formato-de-entrada-requerido)
- [Cómo Usar el Modelo Predeterminado](#como-usar-el-modelo-predeterminado)
- [Cómo Usar un Modelo No-Predeterminado](#como-usar-un-modelo-no-predeterminado)

### Monta tu *Pipeline*

Primero crea un *pipeline* de módulo único con un módulo [`transcribe` (transcripción)](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md).

Usa el método [`create_pipeline`](../../sistema/creacion_de_pipelines/creacion_de_pipelines.md) para esto, incluyendo solamente una referencia de módulo [`transcribe`](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md) en el argumento `module_chain`.


```python
# crea un pipeline con un solo módulo transcribe
pipeline = krixik.create_pipeline(name="unico_transcribe_1", module_chain=["transcribe"])
```

### Formato de Entrada Requerido

El módulo [`transcribe` (transcripción)](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md) recibe archivos audio como entradas. Por ahora el único formato aceptable es MP3.

Antes de procesar un archivo de entrada—uno válido para este *pipeline*—examínalo con el siguiente código:


```python
# examina el contenido de un archivo de entrada válido
import IPython

IPython.display.Audio(data_dir + "input/video_Colombia.mp3")
```





<audio  controls="controls" >
    Your browser does not support the audio element.
</audio>




### Como Usar el Modelo Predeterminado

Ahora procesa el archivo usando el modelo [predeterminado](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md#modelos-disponibles-en-el-modulo-transcribe) del módulo [`transcribe` (transcripción)](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md): [`whisper-tiny`](https://huggingface.co/openai/whisper-tiny).

Dado que este es el modelo predeterminado, no hace falta que especifiques qué modelo quieres usar a través del argumento opcional [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).


```python
# procesa el archivo con el modelo predeterminado
process_output = pipeline.process(
    local_file_path=data_dir + "input/video_Colombia.mp3",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False,  # no mostrar actualizaciones de proceso al ejecutar el código
)
```

Con el siguiente código cargas la salida indicada en `process_output_files`.

Dado que la salida de este modelo/módulo es un archivo JSON, la salida también se incluye en el objeto (esto solo ese el caso para salidas JSON)—pero dado que la salida es bastante larga, para este documento solamente cargarás la transcripción. Además, el archivo de salida se ha guardado en la ubicación indicada bajo `process_output_files`. El `file_id` del archivo procesado es el prefijo del nombre del archivo de salida en esta ubicación.


```python
# carga el la salida del proceso del archivo de salida—aquí solo reproducimos la transcripción, dado que toda la salida es bastante larga
with open(process_output["process_output_files"][0]) as f:
    print(json.dumps(json.load(f)[0]["transcript"].strip(), indent=2))
```

    "That's episode looking at the great country of Columbia. We looked at some really basic facts. It's name, a bit of its history, the type of people that live there, land size and all that jazz. But in this video, we're gonna go into a little bit more of a detailed look. Yo, what is going on guys? Welcome back to F2D facts. The channel where I look at people cultures and places, my name is Dave Wouple. And today we are gonna be looking more at Columbia in our Columbia Part 2 video. Which just reminds me guys, this is part of our Columbia playlist. I'll put it down in the description box below and I'll talk about that more at the end of the video. But if you're new here, join me every single Monday to learn about new countries from around the world. You can do that by hitting that subscribe and that belt notification button. But that skits."


El archivo JSON devuelto contiene, además de los fragmentos de texto transcrito, marcas de tiempo para cada uno y un valor que indica el nivel de confianza en la precisión de cada transcripción fragmentaria.

### Como Usar un Modelo No-Predeterminado

Para usar un modelo [no-predeterminado](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md#modelos-disponibles-en-el-modulo-transcribe) como [`whisper-large-v3`](https://huggingface.co/openai/whisper-large-v3), debes especificarlo a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) al usar el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md):


```python
# procesa el archivo con un modelo no-predeterminado
process_output = pipeline.process(
    local_file_path=data_dir + "input/video_Colombia.mp3",  # todos los argumentos (salvo modules) son iguales que antes
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,
    wait_for_process=True,
    verbose=False,
    modules={"transcribe": {"model": "whisper-large-v3"}},  # especifica un modelo no-predeterminado (y sus parámetros) para este proceso
)
```


```python
# carga la salida del proceso de un archivo—acá solo se imprime la transcripción, y no la versión completa con marcas de tiempo, dado que la salida entera es bastante larga
with open(process_output["process_output_files"][0]) as f:
    print(json.dumps(json.load(f)[0]["transcript"].strip(), indent=2))
```