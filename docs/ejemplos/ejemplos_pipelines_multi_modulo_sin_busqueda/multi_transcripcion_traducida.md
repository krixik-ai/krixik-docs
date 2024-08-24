<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/multi_module_non_search_pipeline_examples/multi_translated_transcription.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## *Pipeline* Multimodular: Transcripción Traducida

Este documento detalla un *pipeline* multimodular que recibe un archivo de audio, lo [`transcribe`](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md) y [`traduce`](../../modulos/modulos_ia/modulo_translate_traduccion.md) la transcripción al idioma indicado.

El documento está dividido en las siguientes secciones:

- [Monta tu *Pipeline*](#monta-tu-pipeline)
- [Procesa un Archivo de Entrada](#procesa-un-archivo-de-entrada)

### Monta tu *Pipeline*

Para lograr lo arriba descrito, monta un *pipeline* que consiste de los siguientes módulos en secuencia:

- Un módulo [`transcribe` (transcripción)](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md).

- Un módulo [`translate` (traducción)](../../modulos/modulos_ia/modulo_translate_traduccion.md).

Para crear el pipeline usarás el método [`create_pipeline`](../../sistema/creacion_de_pipelines/creacion_de_pipelines.md) de la siguiente manera:


```python
# creación del pipeline descrito
pipeline = krixik.create_pipeline(name="multi_transcripcion_traducida",
                                  module_chain=["transcribe", "translate"])
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




Dado que el audio de entrada está en inglés, puedes usar el modelo [predeterminado](../../modulos/modulos_ia/modulo_translate_traduccion.md#modelos-disponibles-en-el-modulo-translate) del módulo [`translate`](../../modulos/modulos_ia/modulo_translate_traduccion.md), [`opus-mt-en-es`](https://huggingface.co/Helsinki-NLP/opus-mt-en-es), para traducir su transcripción a español.

Como usarás el modelo predeterminado para el otro módulo en el *pipeline*, no tendrás que especificarlo en el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).


```python
# procesa el archivo a través del pipeline según lo arriba descrito
process_output = pipeline.process(
    local_file_path=data_dir + "input/video_Colombia.mp3",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False, # no mostrar actualizaciones de proceso al ejecutar el código
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
      "pipeline": "multi_translated_transcription",
      "request_id": "9e1cd6f1-7e3d-4e3f-8493-789b83164de1",
      "file_id": "b3b7d81b-2e81-4f53-806a-87e637e01b59",
      "message": "SUCCESS - output fetched for file_id b3b7d81b-2e81-4f53-806a-87e637e01b59.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "Ese es un episodio mirando el gran pas de Columbia. Miramos algunos hechos realmente bsicos. Es el nombre, un poco de su historia, el tipo de gente que vive all, el tamao de la tierra y todo ese jazz. Pero en este video, vamos a entrar en un poco ms de una mirada detallada. Yo, qu est pasando chicos? Bienvenidos de nuevo a los hechos F2D. El canal donde miro las culturas y lugares de la gente, mi nombre es Dave Wouple. Y hoy vamos a mirar ms a Columbia en nuestro video de la Parte 2 de Columbia. Lo que me recuerda chicos, esto es parte de nuestra lista de Columbia. Lo pondr en el cuadro de descripcin de abajo y hablar ms sobre eso al final del video. Pero si eres nuevo aqu, nete a m todos los lunes para aprender sobre nuevos pases de todo el mundo. Usted puede hacer eso pulsando que suscribirse y ese botn de notificacin de cinturn. Pero eso es lo que pasa."
        }
      ],
      "process_output_files": [
        "../../../data/output/b3b7d81b-2e81-4f53-806a-87e637e01b59.json"
      ]
    }


Para confirmar que todo salió como esperabas, carga el archivo de `process_output_files`:


```python
# carga la salida del proceso del archivo
with open(process_output["process_output_files"][0], "r") as file:
    print(file.read())
```

    [{"snippet": "Ese es un episodio mirando el gran pas de Columbia. Miramos algunos hechos realmente bsicos. Es el nombre, un poco de su historia, el tipo de gente que vive all, el tamao de la tierra y todo ese jazz. Pero en este video, vamos a entrar en un poco ms de una mirada detallada. Yo, qu est pasando chicos? Bienvenidos de nuevo a los hechos F2D. El canal donde miro las culturas y lugares de la gente, mi nombre es Dave Wouple. Y hoy vamos a mirar ms a Columbia en nuestro video de la Parte 2 de Columbia. Lo que me recuerda chicos, esto es parte de nuestra lista de Columbia. Lo pondr en el cuadro de descripcin de abajo y hablar ms sobre eso al final del video. Pero si eres nuevo aqu, nete a m todos los lunes para aprender sobre nuevos pases de todo el mundo. Usted puede hacer eso pulsando que suscribirse y ese botn de notificacin de cinturn. Pero eso es lo que pasa."}]
