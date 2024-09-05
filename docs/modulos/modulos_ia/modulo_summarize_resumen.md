## El Módulo `summarize` (Resumen)
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/modules/ai_modules/summarize_module/)

El módulo `summarize` (resumen) toma un documento textual como entrada y devuelve una versión resumida del mismo.

Esta introducción al módulo `summarize` se divide en las siguientes secciones:

- [Entradas y Salidas del Módulo `summarize`](#entradas-y-salidas-del-modulo-summarize)
- [Modelos Disponibles en el Módulo `summarize`](#modelos-disponibles-en-el-modulo-summarize)
- [Parámetros de los Modelos en el Módulo `summarize`](#parametros-de-los-modelos-en-el-modulo-summarize)
- [Un *Pipeline* de Módulo Único para el Módulo `summarize`](#un-pipeline-de-modulo-unico-para-el-modulo-summarize)
- [Resumen Recursivo](#resumen-recursivo)
- [Más Información sobre el Módulo `summarize`: IO y Conectabilidad](#mas-informacion-sobre-el-modulo-summarize-io-y-conectabilidad)

### Entradas y Salidas del Modulo `summarize`

El módulo `summarize` (resumen) recibe entradas de documentos textuales. Los siguientes formatos de archivo son aceptables:

- TXT

- PDF (se convierte automáticamente en TXT antes de procesar)

- DOCX (se convierte automáticamente en TXT antes de procesar)

- PPTX (se convierte automáticamente en TXT antes de procesar)

El módulo `summarize` devuelve un archivo TXT que contiene un resumen del archivo de entrada.

### Modelos Disponibles en el Modulo `summarize`

Puedes activar cualquiera de los siguientes modelos al usar el módulo `summarize`:

- [bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn) (predeterminado)

- [text-summarization](https://huggingface.co/Falconsai/text_summarization)

Usa el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) en el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) para determinar qué modelo quieres activo al procesar archivos a través del módulo `summarize`.

### Parametros de los Modelos en el Modulo `summarize`

Ninguno de los modelos en el módulo `summarize` es parametrizable. Por ende, al elegir qué modelo usarás a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), `params` siempre será un diccionario vacío. Por ejemplo:

```python
# ejemplo de selección de modelo para el módulo summarize en el método process
modules={'summarize': {'model':'bart-large-cnn',
                       'params': {}}}
```

### Un *Pipeline* de Modulo Unico para el Modulo `summarize`

Haz [clic aquí](../../ejemplos/ejemplos_pipelines_modulo_unico/unico_summarize_resumen.md) para detallar un ejemplo de un *pipeline* de módulo único con un módulo `summarize`.

### Resumen Recursivo

Si el resultado de resumir una vez no es lo suficientemente conciso, hay un elegante truco que puedes usar.

Una de las formas más prácticas para lograr resúmenes más cortos (tal vez más abstractos, pero igual representativos) es resumir recursivamente. En otras palabras, le alimentas un resumen antes creado al módulo `summarize` una vez más, así produciendo un resumen más breve. Haz [clic aquí](../../ejemplos/ejemplos_pipelines_multi_modulo_sin_busqueda/multi_resumen_recursivo.md) para detallar un *pipeline* que hace justamente eso.

### Mas Informacion sobre el Modulo `summarize`: IO y Conectabilidad

Haz [clic aquí](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md) para visitar documentación Krixik titulada `Métodos de Conveniencia (¡y Más!)`. Allí encontrarás dos herramientas con las que puedes aprender más sobre el módulo `summarize`: 

- [Ve Ejemplos de Entradas y Salidas de un Módulo](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-ejemplos-de-entradas-y-salidas-de-un-modulo)

- [Ve Data de Conectividad de un Módulo con el Método `click_data`](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-data-de-conectividad-de-un-modulo-con-el-metodo-view_module_click_data)
