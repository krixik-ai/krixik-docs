## El Módulo `parser` (Fragmentación de Texto)
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/modules/support_function_modules/parser_module/)

El módulo `parser` (fragmentación de texto) toma como entrada un documento textual, lo fragmenta en pequeñas frases de palabras consecutivas, y devuelve todos los fragmentos separados en un archivo JSON.

Esta introducción al módulo `parser` se divide en las siguientes secciones:

- [Entradas y Salidas del Módulo `parser`](#entradas-y-salidas-del-modulo-parser)
- [Modelos Disponibles en el Módulo `parser`](#modelos-disponibles-en-el-modulo-parser)
- [Parámetros de los Modelos en el Módulo `parser`](#parametros-de-los-modelos-en-el-modulo-parser)
- [Un *Pipeline* de Módulo Único para el Módulo `parser`](#un-pipeline-de-modulo-unico-para-el-modulo-parser)
- [Más Información sobre el Módulo `parser`: IO y Conectabilidad](#mas-informacion-sobre-el-modulo-parser-io-y-conectabilidad)

### Entradas y Salidas del Modulo `parser`

El módulo `parser` (fragmentación de texto) recibe entradas de documentos textuales. Los siguientes formatos de archivo son aceptables:

- TXT

- PDF (se convierte automáticamente en TXT antes de procesar)

- DOCX (se convierte automáticamente en TXT antes de procesar)

- PPTX (se convierte automáticamente en TXT antes de procesar)

El módulo `parser` devuelve un archivo JSON que contiene todos los fragmentos de texto post-fragmentación. Cada fragmento es acompañado por sus números de linea en el documento original, lo cual te puede ayudar a luego saber de dónde en el documento salió ese fragmento. Por ejemplo, detalla la siguiente salida de un proceso `parser`:

```python
{
  "status_code": 200,
  "pipeline": "modules-parser-docs",
  "request_id": "5908efbc-b06d-44f3-93c8-a46c29540637",
  "file_id": "575c69c6-0571-4f56-8e49-6c1e4f4a3f4a",
  "message": "SUCCESS - output fetched for file_id 575c69c6-0571-4f56-8e49-6c1e4f4a3f4a.Output saved to location(s) listed in process_output_files.",
  "warnings": [],
  "process_output": [
    {
      "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
      "line_numbers": [
        1
      ]
    },
    {
      "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
      "line_numbers": [
        2,
        3,
        4,
        5
      ]
    }
  ],
  "process_output_files": [
    "../../data/output/575c69c6-0571-4f56-8e49-6c1e4f4a3f4a.json"
  ]
}
```

### Modelos Disponibles en el Modulo `parser`

Puedes activar cualquiera de los siguientes modelos al usar el módulo `parser`:

- [sentence](https://www.nltk.org/api/nltk.tokenize.html) - (predeterminado)

- `fixed` - Desarrollado por Krixik. No es un modelo sino una función de apoyo. Divide el texto en fragmentos de texto potencialmente superpuestos—fragmentos de palabras consecutivas que siempre contienen el mismo número de palabras.

Usa el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) en el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) para determinar qué modelo quieres activo al procesar archivos a través del módulo `parser`.

### Parametros de los Modelos en el Modulo `parser`

Diferentes estructuras de parámetros aplican para los diferentes modelos del módulo `parser`.

El modelo predeterminado, [`sentence`](https://www.nltk.org/api/nltk.tokenize.html), no es parametrizable. Por ende, si eliges ese modelo a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), `params` será un diccionario vacío:

```python
# ejemplo de selección del modelo sentence para el módulo parser en el método process
modules={'parser': {'model':'sentence',
                    'params': {}}}
```

El modelo `fixed` <u>sí es</u> parametrizable. Por ende, si eliges ese modelo a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), `params` puede incluir valores para dos parámetros diferentes:

- `chunk_size` (int) - Número de palabras (tokens) consecutivas en cada fragmento. Su valor predeterminado es 10.
- `overlap_size` (int) - Número de palabras de cada fragmento que se superponen/comparten con el fragmento anterior. Si este valor es cero, los fragmentos se alinean punta a punta. Su valor predeterminado es 2.

Por ejemplo:

```python
# ejemplo de selección del modelo fixed para el módulo parser en el método process
modules={'parser': {"model": "fixed",
                    "params": {"chunk_size": 8, "overlap_size": 3}}}
```

### Un *Pipeline* de Modulo Unico para el Modulo `parser`

Haz [clic aquí](../../ejemplos/ejemplos_pipelines_modulo_unico/unico_parser_fragmentacion.md) para detallar un ejemplo de un *pipeline* de módulo único con un módulo `parser`.

### Mas Informacion sobre el Modulo `parser`: IO y Conectabilidad

Haz [clic aquí](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md) para visitar documentación Krixik titulada `Métodos de Conveniencia (¡y Más!)`. Allí encontrarás dos herramientas con las que puedes aprender más sobre el módulo `parser`: 

- [Ve Ejemplos de Entradas y Salidas de un Módulo](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-ejemplos-de-entradas-y-salidas-de-un-modulo)

- [Ve Data de Conectividad de un Módulo con el Método `click_data`](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-data-de-conectividad-de-un-modulo-con-el-metodo-view_module_click_data)
