# multilingual transcription pipeline

This document details a modular pipeline that takes in an audio/video file, transcribes it, and translates the transcription into a desired language.

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [processing a file](#processing-a-file)


## Pipeline setup

Below we setup a multi module pipeline to serve our intended purpose, which is to build a pipeline that will transcribe any audio/video and make it semantically searchable in any language.

To do this we will use the following modules:

- [`transcribe`](modules/transcribe.md): takes in audio/video input, outputs json of content transcription
- [`translate`](modules/translate.md): takes in json of text snippets, outputs json of translated snippets


We do this by passing the module names to the `module_chain` argument of [`create_pipeline`](system/create_save_load.md) along with a name for our pipeline.


```python
# create a multi-module pipeline
pipeline = krixik.create_pipeline(name="examples-transcribe-translate-docs",
                                  module_chain=["transcribe",
                                                "translate"])
```

This pipeline's available modeling options and parameters are stored in your custom [pipeline's configuration](system/create_save_load.md).

## Processing a file

We first define a path to a local input file.

Lets take a quick look at this file before processing.


```python
# examine contents of input file
test_file = "../../data/input/Interesting Facts About Colombia.mp4"
from IPython.display import Video
Video(test_file)
```




<video src="../input_data/Interesting Facts About Colombia.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



The input video content language content is English.  We will use the `opus-mt-en-es` model of the [`translate`](modules/translate.md) to translate the transcript of this video into Spanish.

For this run we will use the default models for the remainder of the modules.



```python
# test file
test_file = "../../data/input/Interesting Facts About Colombia.mp4"

# process test input
process_output = pipeline.process(local_file_path = test_file,
                                  expire_time=60*10,
                                  modules={"translate": {"model": "opus-mt-en-es"}},
                                  verbose=False)
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


The output of this process is printed below.  Because the output of this particular pipeline is a json file, the process output is shown as well.  The local address of the output file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
print(json.dumps(process_output, indent=2))
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

