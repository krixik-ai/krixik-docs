## Formato JSON para Entradas
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/system/parameters_processing_files_through_pipelines/JSON_input_format/)

### Detalles del Formato JSON

Los archivos de entrada JSON a *pipelines* que empiezan con módulos de entrada JSON (p.ej. el módulo [`translate`](../../modulos/modulos_ia/modulo_translate_traduccion.md)) deben estar en un formato muy específico para que el método [`process`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) funcione. Si el archivo no sigue este formato, el intento de ejecutar [`process`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) fallará.

Las reglas de este formato son las siguientes:

- El contenedor macro dentro del archivo JSON debe ser una sola lista.

- La lista contiene múltiples diccionarios.

- Cada bloque de texto que se va a procesar debe estar en un diccionario separado. Por ejemplo, si quieres procesar 20 fragmentos de texto, la lista debe contener 20 diccionarios.

- En cada diccionario, el texto que quieres que Krixik pase al siguiente módulo (asumiendo que conectes ese módulo a uno que lo sigue) es el valor de un par clave-valor. La clave de este par debe ser el *string* `"snippet"`. Si la clave cualquier otra cosa, será ignorado o fallará.

- Cualquier par clave-valor en un diccionario cuya clave no es `"snippet"` será ignorado.

- Si más de un par clave-valor en un diccionario tiene la clave `"snippet"`, todos menos uno de ellos será ignorado.

### Ejemplo de Entrada JSON

Detalla el siguiente ejemplo de lo arriba explicado. Esta lista indica cómo se debe estructurar el contenido de un archivo JSON si quieres enviar las primeras dos oraciones de <u>1984</u> (por George Orwell) a un *pipeline* Krixik por separado.


```python
# ejemplo de contenido de JSON; dos bloques de texto separados
[
    {"snippet": "It was a bright cold day in April, and the clocks were striking thirteen.", "line_numbers": [1]},
    {
        "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him.",
        "line_numbers": [2, 3, 4, 5],
    },
]
```

### Creación de Archivos JSON

Recomendamos usar funcionalidad JSON para crear tus archivos JSON. Crearlos directamente puede generar errores. El siguiente código es un ejemplo de cómo hacerlo en Python (ten en cuenta la variable Python 'my_data' que introducimos al principio):


```python
# crear y localmente guardar un archivo JSON
my_data = [
    {"snippet": "It was a bright cold day in April, and the clocks were striking thirteen.", "line_numbers": [1]},
    {
        "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him.",
        "line_numbers": [2, 3, 4, 5],
    },
]

import json

with open("demo_file_1.json", "w") as f:
    json.dump(my_data, f)
```

Este código localmente creará un archivo JSON con formato correcto llamado `demo_file_1.json`, archivo que contiene el contenido que ves, en tu directorio de trabajo actual.
