## Multi-Module Pipeline: Translated Transcription

This document details a modular pipeline that takes in an audio file, [`transcribes`](../../modules/ai_model_modules/transcribe_module.md) it, and [`translates`](../../modules/ai_model_modules/translate_module.md) the transcription into a desired language.

The document is divided into the following sections:

- [Pipeline Setup](#pipeline-setup)
- [Processing an Input File](#processing-an-input-file)

### Pipeline Setup

To achieve what we've described above, let's set up a pipeline sequentially consisting of the following modules:

- A [`transcribe`](../../modules/ai_model_modules/transcribe_module.md) module.

- A [`translate`](../../modules/ai_model_modules/translate_module.md) module.

We do this by leveraging the [`.create_pipeline`](../../system/pipeline_creation/create_pipeline.md) method, as follows:


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
Video("../../../data/input/Interesting Facts About Colombia.mp3")
```




<video src="../../../data/input/Interesting Facts About Colombia.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



Since the input audio is in English,  we'll use the default [`opus-mt-en-es`](https://huggingface.co/Helsinki-NLP/opus-mt-en-es) model of the [`translate`](../../modules/ai_model_modules/translate_module.md) module to translate the content into Spanish.

We will use the default models for every other module in the pipeline as well, so the [`modules`](../../system/parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) argument of the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method doesn't need to be leveraged.


```python
# process the file through the pipeline, as described above

process_output_1 = pipeline_1.process(local_file_path = "../../../data/input/Interesting Facts About Colombia.mp3", # the initial local filepath where the input file is stored
                                      local_save_directory="../../../data/output", # the local directory that the output file will be saved to
                                      expire_time=60*30, # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=True, # wait for process to complete before returning IDE control to user
                                      verbose=False) # do not display process update printouts upon running code
```


    ---------------------------------------------------------------------------

    PermissionError                           Traceback (most recent call last)

    File ~\AppData\Local\Programs\Python\Python312\Lib\shutil.py:634, in _rmtree_unsafe(path, onexc)
        633 try:
    --> 634     os.unlink(fullname)
        635 except OSError as err:


    PermissionError: [WinError 32] The process cannot access the file because it is being used by another process: 'C:\\Users\\Lucas\\AppData\\Local\\Temp\\tmpngu3ckhg\\krixik_converted_version_Interesting Facts About Colombia.mp3'

    
    During handling of the above exception, another exception occurred:


    PermissionError                           Traceback (most recent call last)

    File ~\AppData\Local\Programs\Python\Python312\Lib\tempfile.py:891, in TemporaryDirectory._rmtree.<locals>.onexc(func, path, exc)
        890 try:
    --> 891     _os.unlink(path)
        892 # PermissionError is raised on FreeBSD for directories


    PermissionError: [WinError 32] The process cannot access the file because it is being used by another process: 'C:\\Users\\Lucas\\AppData\\Local\\Temp\\tmpngu3ckhg\\krixik_converted_version_Interesting Facts About Colombia.mp3'

    
    During handling of the above exception, another exception occurred:


    NotADirectoryError                        Traceback (most recent call last)

    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\utilities\converters\utilities\decorators.py:28, in datatype_converter_wrapper.<locals>.converter_wrapper(*args, **kwargs)
         27 if conversion is not None:
    ---> 28     with tempfile.TemporaryDirectory() as conversion_save_directory:
         29         og_local_file_path = copy.deepcopy(local_file_path)


    File ~\AppData\Local\Programs\Python\Python312\Lib\tempfile.py:919, in TemporaryDirectory.__exit__(self, exc, value, tb)
        918 if self._delete:
    --> 919     self.cleanup()


    File ~\AppData\Local\Programs\Python\Python312\Lib\tempfile.py:923, in TemporaryDirectory.cleanup(self)
        922 if self._finalizer.detach() or _os.path.exists(self.name):
    --> 923     self._rmtree(self.name, ignore_errors=self._ignore_cleanup_errors)


    File ~\AppData\Local\Programs\Python\Python312\Lib\tempfile.py:903, in TemporaryDirectory._rmtree(cls, name, ignore_errors)
        901             raise
    --> 903 _shutil.rmtree(name, onexc=onexc)


    File ~\AppData\Local\Programs\Python\Python312\Lib\shutil.py:796, in rmtree(path, ignore_errors, onerror, onexc, dir_fd)
        795     return
    --> 796 return _rmtree_unsafe(path, onexc)


    File ~\AppData\Local\Programs\Python\Python312\Lib\shutil.py:636, in _rmtree_unsafe(path, onexc)
        635         except OSError as err:
    --> 636             onexc(os.unlink, fullname, err)
        637 try:


    File ~\AppData\Local\Programs\Python\Python312\Lib\tempfile.py:894, in TemporaryDirectory._rmtree.<locals>.onexc(func, path, exc)
        893     except (IsADirectoryError, PermissionError):
    --> 894         cls._rmtree(path, ignore_errors=ignore_errors)
        895 except FileNotFoundError:


    File ~\AppData\Local\Programs\Python\Python312\Lib\tempfile.py:903, in TemporaryDirectory._rmtree(cls, name, ignore_errors)
        901             raise
    --> 903 _shutil.rmtree(name, onexc=onexc)


    File ~\AppData\Local\Programs\Python\Python312\Lib\shutil.py:796, in rmtree(path, ignore_errors, onerror, onexc, dir_fd)
        795     return
    --> 796 return _rmtree_unsafe(path, onexc)


    File ~\AppData\Local\Programs\Python\Python312\Lib\shutil.py:612, in _rmtree_unsafe(path, onexc)
        611 except OSError as err:
    --> 612     onexc(os.scandir, path, err)
        613     entries = []


    File ~\AppData\Local\Programs\Python\Python312\Lib\shutil.py:609, in _rmtree_unsafe(path, onexc)
        608 try:
    --> 609     with os.scandir(path) as scandir_it:
        610         entries = list(scandir_it)


    NotADirectoryError: [WinError 267] The directory name is invalid: 'C:\\Users\\Lucas\\AppData\\Local\\Temp\\tmpngu3ckhg\\krixik_converted_version_Interesting Facts About Colombia.mp3'

    
    During handling of the above exception, another exception occurred:


    Exception                                 Traceback (most recent call last)

    Cell In[4], line 3
          1 # process the file through the pipeline, as described above
    ----> 3 process_output_1 = pipeline_1.process(local_file_path = "../../../data/input/Interesting Facts About Colombia.mp4", # the initial local filepath where the input file is stored
          4                                       local_save_directory="../../../data/output", # the local directory that the output file will be saved to
          5                                       expire_time=60*30, # process data will be deleted from the Krixik system in 30 minutes
          6                                       wait_for_process=True, # wait for process to complete before returning IDE control to user
          7                                       verbose=False) # do not display process update printouts upon running code


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\system_builder\utilities\decorators.py:97, in kwargs_checker.<locals>.wrapper(*args, **kwargs)
         95 if unexpected_args:
         96     raise TypeError(f"unexpected keyword argument(s) for '{func_name}': {', '.join(unexpected_args)}")
    ---> 97 return func(*args, **kwargs)


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\system_builder\functions\checkin.py:67, in check_init_decorator.<locals>.wrapper(self, *args, **kwargs)
         64 @functools.wraps(func)
         65 def wrapper(self, *args, **kwargs):
         66     check_init(self)
    ---> 67     return func(self, *args, **kwargs)


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\utilities\converters\utilities\decorators.py:93, in datatype_converter_wrapper.<locals>.converter_wrapper(*args, **kwargs)
         91     raise PermissionError(e)
         92 except Exception as e:
    ---> 93     raise Exception(e)


    Exception: [WinError 267] The directory name is invalid: 'C:\\Users\\Lucas\\AppData\\Local\\Temp\\tmpngu3ckhg\\krixik_converted_version_Interesting Facts About Colombia.mp3'


The output of this process is printed below. To learn more about each component of the output, review documentation for the [`.process`](../../system/parameters_processing_files_through_pipelines/process_method.md) method.

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

