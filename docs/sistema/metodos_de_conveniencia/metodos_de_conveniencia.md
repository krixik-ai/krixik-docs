<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/convenience_methods/convenience_methods.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Métodos de Conveniencia (¡y Más!)
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/system/convenience_methods/convenience_methods/)

Este documento introduce una variedad de propiedades útiles del objeto principal Krixik y de *pipelines* Krixik que van desde metadata avanzada hasta funciones de conveniencia diseñadas para facilitar pruebas sobre entradas. Todas estas propiedades pueden ser usadas *sin* necesariamente haber antes [inicializado una sesión](../inicializacion/inicializacion_y_autenticacion.md).

El documento se divide en las siguientes secciones:

- [Ve Todos los Módulos Disponibles con la Propiedad `available_modules`](#ve-todos-los-modulos-disponibles-con-la-propiedad-available_modules)
- [Examina la Configuración de un Módulo con el Método `module_details`](#examina-la-configuracion-de-un-modulo-con-el-metodo-module_details)
- [Ve la Cadena de Módulos de un *Pipeline* con la Propiedad `module_chain`](#ve-la-cadena-de-modulos-de-un-pipeline-con-la-propiedad-module_chain)
- [Haz Pruebas Sobre Entradas a un *Pipeline* con el Método `test_input`](#haz-pruebas-sobre-entradas-a-un-pipeline-con-el-metodo-test_input)
- [Ve Ejemplos de Entradas y Salidas de un Módulo](#ve-ejemplos-de-entradas-y-salidas-de-un-modulo)
- [Ve Data de Conectividad de un Módulo con el Método `click_data`](#ve-data-de-conectividad-de-un-modulo-con-el-metodo-click_data)

### Ve Todos los Modulos Disponibles con la Propiedad `available_modules`

Para ver todos los módulos disponbiles usa la propiedad `available_modules`. Esto lo puedes hacer localmente sin antes haber [inicializado una sesión](../inicializacion/inicializacion_y_autenticacion.md) de la siguiente manera:


```python
# ver todos los módulos disponibles
krixik.available_modules
```




    ['caption',
     'json-to-txt',
     'keyword-db',
     'ocr',
     'parser',
     'sentiment',
     'summarize',
     'text-embedder',
     'transcribe',
     'translate',
     'vector-db']



Lo arriba generado es una lista de los nómbres exactos de cada módulo que usarías al montar el `module_chain` de un [nuevo *pipeline*](../creacion_de_pipelines/creacion_de_pipelines.md).

### Examina la Configuracion de un Modulo con el Metodo `module_details`

La [configuración](../creacion_de_pipelines/configuracion_de_pipelines.md) de cualquier módulo puede detallarse con el método `module_details` de Krixik. Esto se puede hacer localmente sin antes haber [inicializado una sesión](../inicializacion/inicializacion_y_autenticacion.md) de la siguiente manera:


```python
# ver la configuración de un módulo Krixik (en este ejemplo, del módulo transcribe)
krixik.module_details(module_name="transcribe")
```




    {'module_config': {'module': {'name': 'transcribe',
       'models': [{'name': 'whisper-tiny'},
        {'name': 'whisper-base'},
        {'name': 'whisper-small'},
        {'name': 'whisper-medium'},
        {'name': 'whisper-large-v3'}],
       'input': {'type': 'audio'},
       'output': {'type': 'json'},
       'defaults': {'model': 'whisper-tiny'}}},
     'input_data_example': None,
     'output_data_example': {'transcript': 'This is the full transcript.',
      'segments': [{'id': 1,
        'seek': 0,
        'start': 0.0,
        'end': 10.0,
        'text': 'This is the',
        'tokens': [20, 34],
        'temperature': 0.0,
        'avg_logprob': 0.0,
        'compression_ratio': 0.0,
        'no_speech_prob': 0.0,
        'confidence': 0.0,
        'words': [{'text': 'This', 'start': 0.0, 'end': 1.0, 'confidence': 0.5},
         {'text': 'is the', 'start': 1.0, 'end': 2.0, 'confidence': 0.6}]},
       {'id': 2,
        'seek': 10,
        'start': 10.0,
        'end': 20.0,
        'text': 'main text',
        'tokens': [44, 101],
        'temperature': 0.0,
        'avg_logprob': 0.0,
        'compression_ratio': 0.0,
        'no_speech_prob': 0.0,
        'confidence': 0.0,
        'words': [{'text': 'main', 'start': 10.0, 'end': 11.0, 'confidence': 0.7},
         {'text': 'text', 'start': 11.0, 'end': 12.0, 'confidence': 0.8}]}],
      'language': 'English'}}



### Ve la Cadena de Modulos de un *Pipeline* con la Propiedad `module_chain`

A veces querrás rápidamente ver el `module_chain` de un *pipeline* sin tener que examinar un archivo [config](../creacion_de_pipelines/configuracion_de_pipelines.md).

Supón que creas un [*pipeline* multimodular](../../ejemplos/introduccion_ejemplos_de_pipelines.md) como el siguiente (puedes verlos en más detalle en ejemplos [como este](../../ejemplos/ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_sobre_traduccion.md)):


```python
# crea un pipeline multimodular
pipeline = krixik.create_pipeline(
    name="sistema-transcripcion-semantica-documentos-multilingües",
    module_chain=["transcribe", "translate", "json-to-txt", "parser", "text-embedder", "vector-db"],
)
```

Para ver la cadena de módulos de este (o cualquier otro) *pipeline*, usa la propiedad `module_chain`. Esto se puede hacer localmente sin antes haber [inicializado una sesión](../inicializacion/inicializacion_y_autenticacion.md) de la siguiente manera:


```python
# ver la cadena de módulos de tu pipeline con la propiedad module_chain
pipeline.module_chain
```




    ['transcribe',
     'translate',
     'json-to-txt',
     'parser',
     'text-embedder',
     'vector-db']



### Haz Pruebas Sobre Entradas a un *Pipeline* con el Metodo `test_input`

Puedes probar si entradas a un *pipeline* fluirán corractamente a través de él con el método `test_input`.

Ilustremos esto con archivos de entrada válidos e inválidos para el [*pipeline* que creamos previamente](#ve-la-cadena-de-modulos-de-un-pipeline-con-la-propiedad-module_chain).

Ten en cuenta que este método de prueba **no** ejecuta nada con tu *pipeline*. Nada se envía al servidor; meramente se confirma que tu archivo de entrada es consumible por el primer módulo de tu *pipeline*. Flujo a través del resto del *pipeline* ya se confirmó al inicialmente [crear el *pipeline*](../creacion_de_pipelines/creacion_de_pipelines.md).

Primero prueba con un archivo que sí es válido para este *pipeline*. Dado que el primer módulo es un módulo [`transcribe`](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md), un archivo MP3 con palabras en inglés claramente habladas funcionará bien. Esto se puede hacer localmente sin antes haber [inicializado una sesión](../inicializacion/inicializacion_y_autenticacion.md) de la siguiente manera:


```python
# usa test_input sobre un archivo de entrada válido para este pipeline
pipeline.test_input(local_file_path=data_dir + "input/video_Colombia.mp3")
```

    SUCCESS: local file '../../../data/input/Interesting Facts About Colombia.mp3' passed pipeline input test passed


Ahora hagamos esta prueba con una entrada que no funcionará con este *pipeline*. El módulo [`transcribe`](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md) con el que empieza el *pipeline* **no** recibirá un archivo TXT, por lo cual el resultado de esta prueba se ve así:


```python
# usa test_input sobre un archivo de entrada que no funcionará con este pipeline
pipeline.test_input(local_file_path=data_dir + "input/1984_muy_corto.txt")
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    File ~/Desktop/krixik/code/krixik-docs/docs_venv/lib/python3.10/site-packages/krixik/utilities/validators/data/utilities/decorators.py:47, in datatype_validator.<locals>.wrapper(*args, **kwargs)
         46             raise ValueError(f"invalid file extension: '{extension}'")
    ---> 47     return func(*args, **kwargs)
         48 except ValueError as e:


    File ~/Desktop/krixik/code/krixik-docs/docs_venv/lib/python3.10/site-packages/krixik/pipeline_builder/pipeline.py:130, in BuildPipeline.test_input(self, local_file_path)
        123 """test input file will flow through pipeline correctly via simulation (currently in beta)
        124 
        125 Parameters
       (...)
        128     path to local file to test for pipeline threadthrough
        129 """
    --> 130 input_check(local_file_path, self.__module_chain)
        131 print(f"SUCCESS: local file '{local_file_path}' passed pipeline input test passed")


    File ~/Desktop/krixik/code/krixik-docs/docs_venv/lib/python3.10/site-packages/krixik/pipeline_builder/utilities/input_checker.py:20, in input_check(local_file_path, module_chain)
         19 if file_ext_format != first_module_input_format:
    ---> 20     raise TypeError(f"file extension '{file_ext}' does not match the expected input format {first_module_input_format}")
         21 is_valid(first_module.name, local_file_path)


    TypeError: file extension '.txt' does not match the expected input format audio

    
    During handling of the above exception, another exception occurred:


    Exception                                 Traceback (most recent call last)

    Cell In[7], line 2
          1 # use test_input on a file that won't work for this pipeline
    ----> 2 pipeline.test_input(local_file_path=data_dir + "input/1984_very_short.txt")


    File ~/Desktop/krixik/code/krixik-docs/docs_venv/lib/python3.10/site-packages/krixik/utilities/validators/data/utilities/decorators.py:51, in datatype_validator.<locals>.wrapper(*args, **kwargs)
         49     raise ValueError(e)
         50 except Exception as e:
    ---> 51     raise Exception(e)


    Exception: file extension '.txt' does not match the expected input format audio


### Ve Ejemplos de Entradas y Salidas de un Modulo

Examina la clase de data aplicable a tu módulo inicial para asegurarte que tus entradas satisfacen todo requerimiento estructural.

Puedes rápidamente hacerte una idea la estructura de entrada/salida de un módulo detallando un ejemplo como aquel reproducido tras el siguiente código. Funciona para cualquier [módulo actualmente disponible](../../modulos/introduccion_modulos.md), en este caso demostrado con el módulo [`parser`](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md). Esto se puede hacer localmente sin antes haber [inicializado una sesión](../inicializacion/inicializacion_y_autenticacion.md) de la siguiente manera:


```python
# examina la estructura de data de entradas y salidas para el módulo parser reproduciendo ejemplos de entrada y salida para el mismo
from krixik.modules.parser import io
import json

print("ejemplo de data - entrada")
print("-----")
print(io.InputStructure().data_example)
print("\n")
print("ejemplo de data - salida")
print("-----")
print(json.dumps(io.OutputStructure().data_example, indent=2))
```

    input data example
    -----
    sample text looks like this.
    
    
    output data example
    -----
    {
      "snippet": "This is the main text.",
      "line_numbers": [
        1,
        2,
        3,
        4
      ],
      "other": null
    }


`"other"` acá indica toda otra clave en tu archivo de entrada. Su valor no importa porque, en lo que concierne a cualquier módulo que conectes al módulo [`parser`](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md), es irrelevante: en el *pipeline*, lo único que pasa al siguiente módulo son los fragmentos de texto.

### Ve Data de Conectividad de un Modulo con el Metodo `click_data`

El método `click_data` muestra toda los datos básicos que necesitas para saber qué modulos se pueden conectar, o hacer "click", con qué otros módulos. Esta es la data que se consulta "tras bambalinas" de Krixik cuando creas un *pipeline* con el método [`create_pipeline`](../creacion_de_pipelines/creacion_de_pipelines.md). Detalla cada componente de su salida:

Primero aparece el formato de datos de entrada y salida del módulo. Un módulo como [`transcribe`](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md) toma entradas audio y devuelve salidas JSON, mientras que el módulo [`text-embedder`](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md) toma entradas JSON y devuelve salidas NPY.

Revisar que el formato de *salida* de un módulo cuadra con el formato de *entrada* de otro módulo es el *primer* paso (de dos) para determinar si dos módulos se pueden conectar secuencialmente. Si el formato de salida del "Módulo A" cuadra con el formato de entrada del "Módulo B", lo más probable es que puedas conectar "Módulo A" → "Módulo B" en un *pipeline*. Sin embargo, aún no es cosa cierta. 

El *segundo* paso para determinar "conectabilidad" de módulos es cerciorarse de que los `process_types` de entrada/salida cuadren. Por ejemplo, el módulo puede recibir formato JSON de entrada, pero solamente *procesar* ciertos pares clave-valor dentro de los JSON. Si hay un descuadre en los pares clave-valor de entrada vs los de salida, es posible que el *pipeline* no funcione.

Revisar la alineación de `process_type` por ende confirma (o refuta) si dos módulos se pueden conectar.

Detalla ahora el `click_data` de dos módulos para determinar qué dice sobre su "conectabilidad". Esto se puede hacer localmente sin antes haber [inicializado una sesión](../inicializacion/inicializacion_y_autenticacion.md) de la siguiente manera:


```python
# examina la "conectabilidad" de un módulo con el método click_data
krixik.view_module_click_data(module_name="text-embedder")
```




    {'module_name': 'text-embedder',
     'input_format': 'json',
     'output_format': 'npy',
     'input_process_key': 'snippet',
     'input_process_type': "<class 'str'>",
     'output_process_key': 'data',
     'output_process_type': "<class 'numpy.ndarray'>"}




```python
# examina la "conectabilidad" de otro módulo con el método click_data
krixik.view_module_click_data(module_name="vector-db")
```




    {'module_name': 'vector-db',
     'input_format': 'npy',
     'output_format': 'faiss',
     'input_process_key': 'data',
     'input_process_type': "<class 'numpy.ndarray'>",
     'output_process_key': None,
     'output_process_type': None}



Esta data nos indica que podemos conectar los módulos así:

`text-embedder` -> `vector-db`

Sin embargo, *no* los podemos conectar así:

 `vector-db` -> `text-embedder`

La primera secuencia de módulos, (`text-embedder` → `vector-db`), funciona porque en el `click_data` de ambos módulos se ve que:

- output_format (formato de salida) de `text-embedder` (`npy`) == input_format (formato de entrada) `vector-db` (`npy`) y 
- output_process_type de `text-embedder` (`<class 'numpy.ndarray'>`) == input_process_type de `vector-db` (`<class 'numpy.ndarray'>`)

La segunda conexión, (`vector-db` → `text-embedder`), no funciona. Se ve que:

- output_format (formato de salida) `vector-db` (`faiss`) != input_format (formato de entrada) `text-embedder` (`json`)
