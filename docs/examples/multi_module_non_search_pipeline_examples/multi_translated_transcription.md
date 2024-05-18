## Multi-Module Pipeline: Translated Transcription

This document details a modular pipeline that takes in an audio/video file, [`transcribes`](../modules/ai_model_modules/transcribe_module.md) it, and [`translates`](../modules/ai_model_modules/translate_module.md) the transcription into a desired language.

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)

### Pipeline Setup

To achieve what we've described above, let's set up a pipeline sequentially consisting of the following modules:

- A [`transcribe`](../modules/ai_model_modules/transcribe_module.md) module.

- A [`translate`](../modules/ai_model_modules/translate_module.md) module.

We do this by leveraging the [`.create_pipeline`](../system/pipeline_creation/create_pipeline.md) method, as follows:


```python
# create a pipeline as detailed above

pipeline_1 = krixik.create_pipeline(name="multi_translated_transcription",
                                    module_chain=["transcribe",
                                                  "translate"])
```

### Processing an Input File

Lets take a quick look at a short test file before processing.


```python
# examine contents of input file

from IPython.display import Video
Video("../../../data/input/Interesting Facts About Colombia.mp4")
```




<video src="../../../data/input/Interesting Facts About Colombia.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



Since the input video is in English,  we'll use the default [`opus-mt-en-es`](https://huggingface.co/Helsinki-NLP/opus-mt-en-es) model of the [`translate`](../modules/ai_model_modules/translate_module.md) module to translate the content into Spanish.

We will use the default models for every other module in the pipeline as well, so the [`modules`](../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) method doesn't need to be leveraged.


```python
# process the file through the pipeline, as described above

process_output_1 = pipeline_1.process(local_file_path = "../../../data/input/Interesting Facts About Colombia.mp4", # the initial local filepath where the input file is stored
                                      local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                      expire_time=60*30, # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True, # wait for process to complete before returning IDE control to user
                                      verbose=False) # do not display process update printouts upon running code
```

    INFO: Checking that file size falls within acceptable parameters...
    INFO:...success!
    converted ../input_data/Interesting Facts About Colombia.mp4 to: /var/folders/k9/0vtmhf0s5h56gt15mkf07b1r0000gn/T/tmppaeads7s/krixik_converted_version_Interesting Facts About Colombia.mp3
    INFO: hydrated input modules: {'transcribe': {'model': 'whisper-tiny', 'params': {}}, 'translate': {'model': 'opus-mt-en-es', 'params': {}}}
    INFO: symbolic_directory_path was not set by user - setting to default of /etc
    INFO: file_name was not set by user - setting to random file name: krixik_generated_file_name_xqpbbvidoq.mp3
    INFO: wait_for_process is set to True.
    INFO: file will expire and be removed from you account in 300 seconds, at Mon Apr 29 15:12:17 2024 UTC
    INFO: transcribe-translate-pipeline file process and input processing started...
    INFO: metadata can be updated using the .update api.
    INFO: This process's request_id is: 2cbc5bbb-bc0e-a552-a439-61e25bdfa4cc
    INFO: File process and processing status:
    SUCCESS: module 1 (of 2) - transcribe processing complete.
    SUCCESS: module 2 (of 2) - translate processing complete.
    SUCCESS: pipeline process complete.
    SUCCESS: process output downloaded


The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../system/parameters_processing_files_through_pipelines/process_method.md) method.

Because the output of this particular module-model pair is a JSON file, the process output is provided in this object as well (this is only the case for JSON outputs).  Moreover, the output file itself has been saved to the location noted in the `process_output_files` key.  The `file_id` of the processed input is used as a filename prefix for the output file.


```python
# nicely print the output of this process

print(json.dumps(process_output_1, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "transcribe-translate-pipeline",
      "request_id": "47c08992-bbe6-4d4a-83b6-abb51ed53c8b",
      "file_id": "82713863-4978-4909-b7ae-c61617b33ee8",
      "message": "SUCCESS - output fetched for file_id 82713863-4978-4909-b7ae-c61617b33ee8.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "Ese es el episodio que mira al gran pas de Columbia. Miramos algunos hechos realmente bsicos. Es el nombre, un poco de su historia, el tipo de gente que vive all, el tamao de la tierra, y todo ese jazz. Pero en este video, vamos a entrar en un poco ms de una mirada detallada. Yo, qu est pasando chicos? Bienvenidos de nuevo a los hechos F2D. El canal donde miro las culturas y lugares de la gente. Mi nombre es Dave Wouple, y hoy vamos a ver ms en Columbia y nuestro video de la segunda parte de Columbia. Lo que me recuerda chicos, esto es parte de nuestra lista de Columbia. As que pngalo en el cuadro de descripcin a continuacin, y voy a hablar de eso ms en el vdeo. Pero si eres nuevo aqu, nete a m todos los lunes para aprender sobre nuevos pases de todo el mundo. Usted puede hacer eso pulsando que suscribirse y ese botn de notificacin de cinturn. Pero comencemos. Aprende sobre Columbia. As que todos sabemos que Columbia es famosa por su caf, verdad? S, claro. Lo s. Ustedes estn ah sentados, cinco dlares dicen que va a hablar de caf. Bueno, lo soy. As es, porque tengo mi camioneta. T caf de Columbia justo aqu. Boom anuncio. S. Entonces me estoy pagando por esto. Me importa. As que lo que podra no saber sobre el caf es s, usted probablemente ya sabe que un montn de empresas realmente lo compran. Starbucks compra caf de Columbia. Es como su lugar favorito para comprar caf. Y como para rendir homenaje a ese Starbucks cuando estn haciendo su tienda nmero 1.000 en 2016, decidieron, yo, vamos a ponerlo en Columbia. Y esto fue en la ciudad de Medelln, Columbia. Ahora bien, cuando se trata de caf en Columbia, son el tercer pas productor y exportador de caf ms grande del mundo. La cantidad de caf que se exporta desde Colombia equivale a unas 810.000 toneladas mtricas o aproximadamente 11,5 millones de bolsas. Sin embargo, aunque podra ser vencido por pases como Brasil, en realidad es el pas nmero uno o ms alto para producir y cultivar un tipo especfico de frijol conocido como el beka rabe. Y s que el caf es muy importante cuando se trata de hablar de Columbia, pero ustedes realmente no saben lo importante que es con su cultura. Es interesante el hecho de que en 2007, los principales lugares que equivalan a una zona de amortiguacin de aproximadamente 207.000 hectreas, que se denominan el paisaje cultural del caf, fueron considerados Patrimonio de la Humanidad por la UNESCO. Y tambin en 2007, la UE, la Unin Europea, otorg al caf colombiano una denominacin de origen protegida. Ahora lo suficientemente interesante cuando se trata del caf en Columbia, lo creas o no, en realidad no es nativo del pas. Viene de otro lugar, no es realmente una especie invasiva porque es muy bienvenida. Ahora usted tambin puede haber visto a este tipo en muchas marcas de caf colombianas diferentes. Ahora se llama Juan Valdez. Ahora algunas personas piensan que este tipo es realmente un verdadero granjero de caf, alguien acaba de dibujar."
        }
      ],
      "process_output_files": [
        "/Users/jeremywatt/Desktop/krixik-cli/docs/examples/82713863-4978-4909-b7ae-c61617b33ee8.json"
      ]
    }


To confirm that everything went as it should have, let's load in the text file output from `process_output_files`:


```python
# load in process output from file

with open(process_output_1['process_output_files'][0], "r") as file:
    print(file.read())  
```

    Winston Smith walked through the glass doors of Victory Mansions. The hallway
    smelled of boiled cabbage and old rag mats. A kilometre away the
    Ministry of Truth, his place of work, towered vast.

