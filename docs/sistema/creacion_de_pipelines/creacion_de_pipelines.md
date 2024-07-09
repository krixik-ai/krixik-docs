<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/pipeline_creation/create_pipeline.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>


```python
import os
import sys
import json
import importlib
from pathlib import Path

# preparación de demo - incuye instanciación de secretos, instalación de requerimientos, y definición de rutas
if os.getenv("COLAB_RELEASE_TAG"):
    # si estás usando este notebook en Google Colab, ingresa tus secretos acá
    MY_API_KEY = "TU_API_KEY_VA_AQUI"
    MY_API_URL = "TU_API_URL_VA_AQUI"

    # si estás usando este notebook en Google Colab, instala requerimientos y descarga los subdirectorios requeridos
    # instala el cliente Python de Krixik
    !pip install krixik

    # instala github-clone, que permite clonación fácil de los subdirectorios del repositorio de documentación XXX
    !pip install github-clone

    # clona los conjuntos de datos
    if not Path("data").is_dir():
        !ghclone XXXX #(in english it's https://github.com/krixik-ai/krixik-docs/tree/main/data)
    else:
        print("ya se clonaron los conjuntos de datos de documentación!")

    # define la variable 'data_dir' para tus rutas
    data_dir = "./data/"

    # crea directorio de salidas
    from pathlib import Path

    Path(data_dir + "/salidas").mkdir(parents=True, exist_ok=True)

    # descarga utilidades
    if not Path("utilities").is_dir():
        !ghclone XXXX # (in english it's https://github.com/krixik-ai/krixik-docs/tree/main/utilities)
    else:
        print("ya has clonado las utilidades de documentación!")
else:
    # si estás usando una descarga local de la documentación, define las rutas relativas a la estructura local de la documentación
    # importa utilidades
    sys.path.append("../../../")

    # define la variable 'data_dir' para tus rutas
    data_dir = "../../../data/"

    # si estás usando este notebook localmente desde el repositorio de documentación Krixik, carga tus secretos de un archivo .env ubicado en la base del repositorio de documentación
    from dotenv import load_dotenv

    load_dotenv("../../../.env")

    MY_API_KEY = os.getenv("MY_API_KEY")
    MY_API_URL = os.getenv("MY_API_URL")


# carga 'reset'
reset = importlib.import_module("utilities.reset")
reset_pipeline = reset.reset_pipeline


# importa Krixik e inicializa sesión con tus secretos personales
from krixik import krixik

krixik.init(api_key=MY_API_KEY, api_url=MY_API_URL)
```

## Creación de Pipelines

Esta introducción a cómo crear pipelines se divide en las siguientes secciones:

- [El Método `create_pipeline`](#el-metodo-create_pipeline)
- [Un *Pipeline* de Módulo Único](#un-pipeline-de-modulo-unico)
- [Un *Pipeline* Multimodular](#un-pipeline-multimodular)
- [Validación de Secuencias de Módulos](#validacion-de-secuencias-de-modulos)
- [Repetición de Nombres de Pipelines](#repeticion-de-nombres-de-pipelines)

### El Metodo `create_pipeline`

El método `create_pipeline` instancia nuevos *pipelines*. Es un método muy simple que toma dos argumentos, y ambos son requeridos:

- `name` (str): El nombre de tu nuevo *pipeline*. Piénsalo bien, pues los nombres de los *pipelines* son sus identificadores únicos, así que dos *pipelines* no pueden compartir el mismo nombre.
- `module_chain` (list): La lista secuencial de módulos que forman tu nuevo pipeline.

Haz [clic aquí](../../modulos/introduccion_modulos.md) para ver la lista actual de módulos Krixik disponibles. Recuerda que, siempre y cuando sus entradas y salidas cuadren, cualquier combinación de módulos es válida, incluyendo aquellas en las que se repiten módulos.

### Un *Pipeline* de Modulo Unico

Usa el método `create_pipeline` para crear un *pipeline* de módulo único. Usarás el módulo [`parser`](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md), que fragmenta archivos de texto y los convierte en una serie de frases más cortas.


```python
# crea un pipeline con un solo módulo parser
pipeline = krixik.create_pipeline(name="create_pipeline_1_parser",
                                  module_chain=["parser"])
```

Asegúrate que has [inicializado tu sesión](../inicializacion/inicializacion_y_autenticacion.md  ) antes de ejecutar este código.

Ten en cuenta que el argumento `name` puede ser el *string* que desees. Sin embargo, la lista `module_chain` solo puede estar compuesta de [identificadores de módulo](../metodos_de_conveniencia/metodos_de_conveniencia.md#ve-todos-los-modulos-disponibles-con-la-propiedad-available_modules) establecidos.

### Un *Pipeline* Multimodular

Ahora monta un *pipeline* que consiste de una secuencia de tres módulos: un módulo [`parser` (fragmentación de texto)](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md), un módulo [`text-embedder` (encaje léxico)](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md), y un módulo [`vector-db` (base de datos vectorial)](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md). Este `module_chain` surge a menudo, pues es la fórmula para el [pipeline básico de búsqueda semántica](../../ejemplos/ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_basica.md) (también conocida como búsqueda vectorial).

Como puedes ver, la sintaxis para el montaje del *pipeline* es igual que antes. El orden de los módulos en el argumento `module_chain` es el orden secuencial en el que procesarán entradas al *pipeline*:


```python
# crea un pipeline multimodular básico de búsqueda semántica
pipeline = krixik.create_pipeline(name="create_pipeline_2_parser_embedder_vector",
                                  module_chain=["parser", "text-embedder", "vector-db"])
```

Explora una variedad de ejemplos de *pipelines* multimodulares [aquí](../../ejemplos/introduccion_ejemplos_de_pipelines.md).

### Validacion de Secuencias de Modulos

Al ejecutar `create_pipeline` el cliente Krixik confirma que los módulos indicados funcionarán correctamente en la secuencia solicitada. Si no pueden—lo cual tiende a ser consecuencia de que la salida de un módulo no cuadra con la entrada del siguiente módulo—se lanza una excepción local explicativa.

Por ejemplo, tratar de crear un *pipeline* bimodular que consiste de un módulo [`parser` (fragmentación de texto)](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md) y un módulo [`caption` (leyenda de imagen)](../../modulos/modulos_ia/modulo_caption_leyenda_de_imagen.md), en ese orden, fallará (como debe) y producirá una excepción local. Esto es porque el módulo [`parser`](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md) devuelve un archivo JSON como salida, mientras que el módulo [`caption`](../../modulos/modulos_ia/modulo_caption_leyenda_de_imagen.md) solo toma imágenes como entrada, como indica el mensaje que puedes ver en seguida:


```python
# intenta crear un pipeline compuesto de un módulo parser seguido de un módulo caption
pipeline = krixik.create_pipeline(name="create_pipeline_3_parser_caption",
                                  module_chain=["parser", "caption"])
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    Cell In[4], line 3
          1 # attempt to create a pipeline sequentially comprised of a parser and a caption module
    ----> 3 pipeline_3 = krixik.create_pipeline(name="create_pipeline_3_parser_caption",
          4                                     module_chain=["parser", "caption"])


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\main.py:70, in krixik.create_pipeline(cls, name, module_chain)
         68         raise ValueError(f"module_chain item - {item} - is not a currently one of the currently available modules -{available_modules}")
         69 module_chain_ = [Module(m_name) for m_name in module_chain]
    ---> 70 custom = BuildPipeline(name=name, module_chain=module_chain_)
         71 return cls.load_pipeline(pipeline=custom)


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\pipeline_builder\pipeline.py:63, in BuildPipeline.__init__(self, name, module_chain, config_path)
         61 chain_check(module_chain)
         62 for module in module_chain:
    ---> 63     self._add(module)
         64 self.test_connections()


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\pipeline_builder\pipeline.py:86, in BuildPipeline._add(self, module, insert_index)
         83 self.__module_chain_configs.append(module.config)
         84 self.__module_chain_output_process_keys.append(module.output_process_key)
    ---> 86 self.test_connections()


    File c:\Users\Lucas\Desktop\krixikdocsnoodle\myenv\Lib\site-packages\krixik\pipeline_builder\pipeline.py:160, in BuildPipeline.test_connections(self)
        158 # check format compatibility
        159 if prev_module_output_format != curr_module_input_format:
    --> 160     raise TypeError(
        161         f"format type mismatch between {prev_module.name} - whose output format is {prev_module_output_format} - and {curr_module.name} - whose input format is {curr_module_input_format}"
        162     )
        164 # check process key type compatibility
        165 if prev_module_output_process_key_type != curr_module_input_process_key_type:


    TypeError: format type mismatch between parser - whose output format is json - and caption - whose input format is image


### Repeticion de Nombres de Pipelines

Krixik no te permite crear un *pipeline* con el `name` de otro *pipeline* que ya has creado. La única excepción es si el nuevo *pipeline* tiene una cadena de módulos idéntica a la anterior.

Ten en cuenta que si intentas crear un nuevo *pipeline* con el `name` de un *pipeline* anterior y con un `module_chain` diferente, la creación inicial del *pipeline* no fallará. Podrás ejecutar el método `create_pipeline` sin problema. Sin embargo, cuando dos *pipelines* con el mismo nombre y diferentes `module_chain`s existen y ya has [`procesado`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) al menos un archivo a través de uno de ellos, **no** podrás procesar un archivo a través del otro *pipeline* como consecuencia de esta duplicación de `name`s.


```python
# elimina todos los datos procesados pertenecientes a este pipeline
reset_pipeline(pipeline)
```
