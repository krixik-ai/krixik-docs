## El Módulo `transcribe` (Transcripción)

El módulo `transcribe` (transcripción) toma audio como entrada y devuelve una transcripción textual de todas las palabras pronunciadas en ese audio.

Esta introducción al módulo `transcribe` se divide en las siguientes secciones:

- [Entradas y Salidas del Módulo `transcribe`](#entradas-y-salidas-del-modulo-transcribe)
- [Modelos Disponibles en el Módulo `transcribe`](#modelos-disponibles-en-el-modulo-transcribe)
- [Parámetros de los Modelos en el Módulo `transcribe`](#parametros-de-los-modelos-en-el-modulo-transcribe)
- [Un *Pipeline* de Módulo Único para el Módulo `transcribe`](#un-pipeline-de-modulo-unico-para-el-modulo-transcribe)
- [Más Información sobre el Módulo `transcribe`: IO y Conectabilidad](#mas-informacion-sobre-el-modulo-transcribe-io-y-conectabilidad)

### Entradas y Salidas del Modulo `transcribe`

El módulo `transcribe` recibe entradas audio. Los siguientes formatos de archivo son aceptables:

- MP3

El módulo `translate` devuelve un archivo JSON. El archivo devuelto incluye toda la transcripción dividida en fragmentos, y cada fragmento va acompañado de marcas de tiempo y de un valor que indica el nivel de confianza en la precisión de esa transcripción.

### Modelos Disponibles en el Modulo `transcribe`

Puedes activar cualquiera de los siguientes modelos al usar el módulo `transcribe`:

- [whisper-tiny](https://huggingface.co/openai/whisper-tiny) - (predeterminado) El más económico y menos preciso de los modelos [Whisper](https://huggingface.co/docs/transformers/en/model_doc/whisper)

- [whisper-base](https://huggingface.co/openai/whisper-base)

- [whisper-small](https://huggingface.co/openai/whisper-small)

- [whisper-medium](https://huggingface.co/openai/whisper-medium)

- [whisper-large-v3](https://huggingface.co/openai/whisper-large-v3) - El más preciso y costoso de los modelos Whisper

Usa el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) en el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) para determinar qué modelo quieres activo al procesar archivos a través del módulo `transcribe`.

### Parametros de los Modelos en el Modulo `transcribe`

Ninguno de los modelos en el módulo `transcribe` es parametrizable. Por ende, al elegir qué modelo usarás a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), `params` siempre será un diccionario vacío. Por ejemplo:

```python
# ejemplo de selección de modelo para el módulo transcribe en el método process
modules={'transcribe': {'model':'whisper-small',
                       'params': {}}}
```

### Un *Pipeline* de Modulo Unico para el Modulo `transcribe`

Haz [clic aquí](../../ejemplos/ejemplos_pipelines_modulo_unico/unico_transcribe_transcripcion.md) para detallar un ejemplo de un *pipeline* de módulo único con un módulo `transcribe`.

### Mas Informacion sobre el Modulo `transcribe`: IO y Conectabilidad

Haz [clic aquí](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md) para visitar documentación Krixik titulada `Métodos de Conveniencia (¡y Más!)`. Allí encontrarás dos herramientas con las que puedes aprender más sobre el módulo `transcribe`: 

- [Ve Ejemplos de Entradas y Salidas de un Módulo](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-ejemplos-de-entradas-y-salidas-de-un-modulo)

- [Ve Data de Conectividad de un Módulo con el Método `click_data`](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-data-de-conectividad-de-un-modulo-con-el-metodo-click_data)
