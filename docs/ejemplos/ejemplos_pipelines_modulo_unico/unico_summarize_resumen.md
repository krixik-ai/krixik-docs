<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/examples/single_module_pipelines/single_summarize.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## *Pipeline* de Módulo Único: `summarize` (Resumen)
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/examples/single_module_pipelines/single_summarize/)

Este documento presenta una guía de cómo ensamblar y consumir un *pipeline* de módulo único que solo incluye un módulo [`summarize` (resumen)](../../modulos/modulos_ia/modulo_summarize_resumen.md). Se divide en las siguientes secciones:

- [Monta tu *Pipeline*](#monta-tu-pipeline)
- [Formato de Entrada Requerido](#formato-de-entrada-requerido)
- [Cómo Usar el Modelo Predeterminado](#como-usar-el-modelo-predeterminado)
- [Cómo Usar un Modelo No-Predeterminado](#como-usar-un-modelo-no-predeterminado)
- [Resumen Recursivo](#resumen-recursivo)

### Monta tu *Pipeline*

Primero crea un *pipeline* de módulo único con un módulo [`summarize` (resumen)](../../modulos/modulos_ia/modulo_summarize_resumen.md).

Usa el método [`create_pipeline`](../../sistema/creacion_de_pipelines/creacion_de_pipelines.md) para esto, incluyendo solamente una referencia de módulo [`summarize`](../../modulos/modulos_ia/modulo_summarize_resumen.md) en el argumento `module_chain`.


```python
# crea un pipeline con un solo módulo summarize
pipeline = krixik.create_pipeline(name="unico_summarize_1", module_chain=["summarize"])
```

### Formato de Entrada Requerido

El módulo [`summarize` (resumen)](../../modulos/modulos_ia/modulo_summarize_resumen.md) recibe como entradas documentos textuales con formato TXT, PDF, DOCX y PPTX, aunque estos últimos tres formatos son automáticamente convertidos a TXT al iniciar proceso.

Antes de procesar un archivo de entrada—uno válido para este *pipeline*—examínalo con el siguiente código:


```python
# examina el contenido de un archivo de entrada válido
with open(data_dir + "input/1984_corto.txt", "r") as file:
    print(file.read())
```

    It was a bright cold day in April, and the clocks were striking thirteen.
    Winston Smith, his chin nuzzled into his breast in an effort to escape the
    vile wind, slipped quickly through the glass doors of Victory Mansions,
    though not quickly enough to prevent a swirl of gritty dust from entering
    along with him.
    
    The hallway smelt of boiled cabbage and old rag mats. At one end of it a
    coloured poster, too large for indoor display, had been tacked to the wall.
    It depicted simply an enormous face, more than a metre wide: the face of a
    man of about forty-five, with a heavy black moustache and ruggedly handsome
    features. Winston made for the stairs. It was no use trying the lift. Even
    at the best of times it was seldom working, and at present the electric
    current was cut off during daylight hours. It was part of the economy drive
    in preparation for Hate Week. The flat was seven flights up, and Winston,
    who was thirty-nine and had a varicose ulcer above his right ankle, went
    slowly, resting several times on the way. On each landing, opposite the
    lift-shaft, the poster with the enormous face gazed from the wall. It was
    one of those pictures which are so contrived that the eyes follow you about
    when you move. BIG BROTHER IS WATCHING YOU, the caption beneath it ran.
    
    Inside the flat a fruity voice was reading out a list of figures which had
    something to do with the production of pig-iron. The voice came from an
    oblong metal plaque like a dulled mirror which formed part of the surface
    of the right-hand wall. Winston turned a switch and the voice sank
    somewhat, though the words were still distinguishable. The instrument
    (the telescreen, it was called) could be dimmed, but there was no way of
    shutting it off completely. He moved over to the window: a smallish, frail
    figure, the meagreness of his body merely emphasized by the blue overalls
    which were the uniform of the party. His hair was very fair, his face
    naturally sanguine, his skin roughened by coarse soap and blunt razor
    blades and the cold of the winter that had just ended.
    
    Outside, even through the shut window-pane, the world looked cold. Down in
    the street little eddies of wind were whirling dust and torn paper into
    spirals, and though the sun was shining and the sky a harsh blue, there
    seemed to be no colour in anything, except the posters that were plastered
    everywhere. The black-moustachio'd face gazed down from every commanding
    corner. There was one on the house-front immediately opposite. BIG BROTHER
    IS WATCHING YOU, the caption said, while the dark eyes looked deep into
    Winston's own. Down at street level another poster, torn at one corner,
    flapped fitfully in the wind, alternately covering and uncovering the
    single word INGSOC. In the far distance a helicopter skimmed down between
    the roofs, hovered for an instant like a bluebottle, and darted away again
    with a curving flight. It was the police patrol, snooping into people's
    windows. The patrols did not matter, however. Only the Thought Police
    mattered.
    
    Behind Winston's back the voice from the telescreen was still babbling away
    about pig-iron and the overfulfilment of the Ninth Three-Year Plan. The
    telescreen received and transmitted simultaneously. Any sound that Winston
    made, above the level of a very low whisper, would be picked up by it,
    moreover, so long as he remained within the field of vision which the metal
    plaque commanded, he could be seen as well as heard. There was of course
    no way of knowing whether you were being watched at any given moment. How
    often, or on what system, the Thought Police plugged in on any individual
    wire was guesswork. It was even conceivable that they watched everybody all
    the time. But at any rate they could plug in your wire whenever they wanted
    to. You had to live--did live, from habit that became instinct--in the
    assumption that every sound you made was overheard, and, except in
    darkness, every movement scrutinized.
    
    Winston kept his back turned to the telescreen. It was safer; though, as he
    well knew, even a back can be revealing. A kilometre away the Ministry of
    Truth, his place of work, towered vast and white above the grimy landscape.
    This, he thought with a sort of vague distaste--this was London, chief
    city of Airstrip One, itself the third most populous of the provinces of
    Oceania. He tried to squeeze out some childhood memory that should tell him
    whether London had always been quite like this. Were there always these
    vistas of rotting nineteenth-century houses, their sides shored up with
    baulks of timber, their windows patched with cardboard and their roofs
    with corrugated iron, their crazy garden walls sagging in all directions?
    And the bombed sites where the plaster dust swirled in the air and the
    willow-herb straggled over the heaps of rubble; and the places where the
    bombs had cleared a larger patch and there had sprung up sordid colonies
    of wooden dwellings like chicken-houses? But it was no use, he could not
    remember: nothing remained of his childhood except a series of bright-lit
    tableaux occurring against no background and mostly unintelligible.
    
    The Ministry of Truth--Minitrue, in Newspeak [Newspeak was the official
    language of Oceania. For an account of its structure and etymology see
    Appendix.]--was startlingly different from any other object in sight. It
    was an enormous pyramidal structure of glittering white concrete, soaring
    up, terrace after terrace, 300 metres into the air. From where Winston
    stood it was just possible to read, picked out on its white face in
    elegant lettering, the three slogans of the Party:
    
    
      WAR IS PEACE
      FREEDOM IS SLAVERY
      IGNORANCE IS STRENGTH


### Como Usar el Modelo Predeterminado

Ahora procesa el archivo usando el modelo [predeterminado](../../modulos/modulos_ia/modulo_summarize_resumen.md#modelos-disponibles-en-el-modulo-summarize) del módulo [`summarize` (resumen)](../../modulos/modulos_ia/modulo_summarize_resumen.md): [`bart-large-cnn`](https://huggingface.co/facebook/bart-large-cnn).

Dado que este es el modelo predeterminado, no hace falta que especifiques qué modelo quieres usar a través del argumento opcional [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).


```python
# procesa el archivo con el modelo predeterminado
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_corto.txt",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False,  # no mostrar actualizaciones de proceso al ejecutar el código
)
```

La salida del proceso se reproduce con el siguiente código. Para aprender más sobre cada componente de esta salida, revisa la documentación del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).

El archivo de salida se ha guardado en la ubicación indicada bajo `process_output_files`. El `file_id` del archivo procesado es el prefijo del nombre del archivo de salida en esta ubicación.


```python
# nítidamente reproduce la salida de este proceso
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "single_summarize_1",
      "request_id": "21af82dc-c558-4d7d-b819-b97b91308994",
      "file_id": "718948f7-685a-4e8e-b610-254b454897ce",
      "message": "SUCCESS - output fetched for file_id 718948f7-685a-4e8e-b610-254b454897ce.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": null,
      "process_output_files": [
        "../../../data/output/718948f7-685a-4e8e-b610-254b454897ce.txt"
      ]
    }


Para confirmar que todo salió como esperabas, carga el archivo de texto de `process_output_files`:


```python
# carga la salida del proceso del archivo
with open(process_output["process_output_files"][0], "r") as file:
    print(file.read())
```

    Winston Smith walked through the glass doors of Victory Mansions. The hallway
    smelt of boiled cabbage and old rag mats. At one end of
    it it acoloured poster, too large for indoor display, had been tacked
    to the wall. It depicted simply an enormous face, more than a
    metre wide. Winston made for the stairs.
    
    Inside the flat a fruity voice was reading out a list of
    figures which had something to do with pig-iron. Winston turned a switch
    and the voice sank somewhat, though the words were still distinguishable. He
    moved over to the window: a smallish, frail figure, the meagreness of
    his body merely emphasized by the blue overalls which were the uniform
    of the party.
    
    Winston kept his back turned to the telescreen. It was safer; though,
    as he well knew, even a back can be revealing. A kilometre
    away the Ministry of Truth, his place of work, towered vast and
    white above the grimy landscape. Winston tried to squeeze out some childhood
    memory that should tell him whether London had always been quite like
    this.
    
    The Ministry of Truth--Minitrue, in Newspeak [Newspeak was the officiallanguage of Oceania]--was
    startlingly different from any other object in sight. It was an enormous
    pyramidal structure of glittering white concrete, soaring 300 metres into the air.


### Como Usar un Modelo No-Predeterminado

Para usar un modelo [no-predeterminado](../../modulos/modulos_ia/modulo_summarize_resumen.md#modelos-disponibles-en-el-modulo-summarize) como [`text-summarization`](https://huggingface.co/Falconsai/text_summarization), debes especificarlo a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) al usar el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md):


```python
# procesa el archivo con un modelo no-predeterminado
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_corto.txt",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # data de este proceso se eliminará del sistema Krixik en 30 minutos
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False,  # no mostrar actualizaciones de proceso al ejecutar el código
    modules={"summarize": {"model": "text-summarization"}},  # especifica un modelo no-predeterminado para este proceso
)
```

Puedes ver el nuevo resumen si cargas el archivo de salida con el siguiente código.

Los descuadres en puntuación son un artefacto del modelo, como indica la [tarjeta del modelo](https://huggingface.co/Falconsai/text_summarization) en [HuggingFace](https://huggingface.co/).


```python
# carga la salida del proceso del archivo
with open(process_output_nd["process_output_files"][0], "r") as file:
    print(file.read())
```

    Winston Smith, his chin nuzzled into his breast in an effort to
    escape the vile wind, slipped quickly through the glass doors of Victory
    Mansions . At one end of it a coloured poster, too large
    for indoor display, had been tacked to the wall . It was
    part of the economy drive in preparation for Hate Week . The
    flat was seven flights up, and Winston went slowly, resting several times
    on the way .
    
    Winston turned a switch and the voice sank somewhat, though the words
    were still distinguishable . The instrument (the telescreen, it was called) could
    be dimmed, but there was no way of shutting it off completely
    . He moved over to the window: a smallish, frail figure, the
    meagreness of his body merely emphasized by the blue overalls which were
    the uniform of the party . Outside, even through the shut window-pane,
    the world looked cold .
    
    There was no way of knowing whether you were being watched at
    any given moment . How often, or on what system, the Thought
    Police plugged in on any individual wire was guesswork . You had
    to live, from habit that became instinct--in the assumption that every sound
    you made was overheard, and, except in darkness, every movement scrutinized .
    
    The Ministry of Truth--Minitrue, in Newspeak, was the official language of Oceania
    . It was an enormous pyramidal structure of glittering white concrete, soaring
    up, terrace after terrace, 300 metres into the air . From where
    Winston stood it was just possible to read, picked out on its
    white face in elegant lettering .


### Resumen Recursivo

Si el resultado de resumir una vez no es lo suficientemente conciso, hay un elegante truco que puedes usar.

Una de las formas más prácticas para lograr resúmenes más cortos (tal vez más abstractos, pero igual representativos) es resumir recursivamente. En otras palabras, le alimentas el resumen antes creado al módulo `summarize` una vez más, así produciendo un resumen más breve. En esta sección aprenderás a hacer este proceso manualmente.

Para ingresar el <u>primer</u> resumen arriba generado en el módulo [`summarize`](../../modulos/modulos_ia/modulo_summarize_resumen.md) debes repetir lo que hiciste anteriormente, pero con una diferencia: el archivo que alimentas como entrada es la salida resumida de ese primer proceso de resumen, y no el archivo original.


```python
# asigna el resumen generado a una variable para encontrarlo facilmente
first_summary = process_output["process_output_files"][0]

# procesa este resumen a través del pipeline
process_output = pipeline.process(
    local_file_path=first_summary,  # alimenta al pipeline el resumen antes generado
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,
    wait_for_process=True,
    verbose=False,
)
```

Una vez termina este proceso recibes un resumen aún más breve como archivo de salida.

Con el siguiente código puedes examinar este nuevo resumen:


```python
# carga la salida del proceso del archivo
with open(process_output["process_output_files"][0], "r") as file:
    print(file.read())
```

    Winston Smith walked through the glass doors of Victory Mansions. The hallway
    smelled of boiled cabbage and old rag mats. At one end of
    the hallway an acoloured poster, too large for indoor display, had been
    tacked to the wall. It depicted simply an enormous face, more than
    a metre wide.
    
    Winston kept his back turned to the telescreen. It was safer; though,
    he well knew, even a back can be revealing. A kilometre away
    the Ministry of Truth, his place of work, towered vast and white.


Este es un resumen más conciso, y por ende un poco más abstracto, del texto original.

Ahora haz este proceso recursivo una vez más, buscando un resumen aún más breve del texto original.

El uso del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) es casi igual. La única diferencia es que `local_file_path`, que le dice a Krixik qué archivo usar como entrada, indica la salida del segundo resumen que generaste.


```python
# asigna el segundo resumen generado a una variable para encontrarlo facilmente
second_summary = process_output["process_output_files"][0]

# procesa este resumen a través del pipeline una vez más
process_output = pipeline.process(
    local_file_path=second_summary,  # alimenta al pipeline el segundo resumen antes generado
    local_save_directory=data_dir + "output",
    expire_time=60 * 30,
    wait_for_process=True,
    verbose=False,
)
```

Ahora puedes ver el nuevo y muy corto resumen:


```python
# load in the recursed summary from file
with open(process_output["process_output_files"][0], "r") as file:
    print(file.read())
```

    Winston Smith walked through the glass doors of Victory Mansions. The hallway
    smelled of boiled cabbage and old rag mats. A kilometre away, his
    place of work, the Ministry of Truth, towered vast and white.


Puedes ver que este es un resumen muy reducido del texto original—reducido pero aún representativo.

Puedes obtener el mismo resultado (de resumir recursivamente tres veces) con un pipeline que contiene tres módulos [`summarize`](../../modulos/modulos_ia/modulo_summarize_resumen.md) consecutivos. Haz [clic aquí](../../ejemplos/ejemplos_pipelines_multi_modulo_sin_busqueda/multi_resumen_recursivo.md) para detallar un ejemplo de un *pipeline* de resumen recursivo en el que hacemos justamente esto.
