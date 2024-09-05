## El Módulo `translate` (Traducción)
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/modules/ai_modules/translate_module/)

El módulo `translate` (traducción) toma como entrada uno o varios fragmentos de texto y devuelve sus traducciones en el idioma de salida del modelo seleccionado.

Esta introducción al módulo `translate` se divide en las siguientes secciones:

- [Entradas y Salidas del Módulo `translate`](#entradas-y-salidas-del-modulo-translate)
- [Modelos Disponibles en el Módulo `translate`](#modelos-disponibles-en-el-modulo-translate)
- [Parámetros de los Modelos en el Módulo `translate`](#parametros-de-los-modelos-en-el-modulo-translate)
- [Un *Pipeline* de Módulo Único para el Módulo `translate`](#un-pipeline-de-modulo-unico-para-el-modulo-translate)
- [Más Información sobre el Módulo `translate`: IO y Conectabilidad](#mas-informacion-sobre-el-modulo-translate-io-y-conectabilidad)

### Entradas y Salidas del Modulo `translate`

El módulo `translate` (traducción) recibe entradas en formato JSON. Las entradas JSON deben respetar [este formato](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/formato_JSON_entrada.md).

El módulo `translate` devuelve un archivo JSON. El archivo devuelto tiene el mismo formato que el archivo de entrada, pero cada fragmento ha sido traducido.

### Modelos Disponibles en el Modulo `translate`

Puedes activar cualquiera de los siguientes modelos al usar el módulo `translate`:

- [opus-mt-en-es](https://huggingface.co/Helsinki-NLP/opus-mt-en-es) - (predeterminado) inglés a español

- [opus-mt-es-en](https://huggingface.co/Helsinki-NLP/opus-mt-es-en) - español a inglés

- [opus-mt-de-en](https://huggingface.co/Helsinki-NLP/opus-mt-de-en) - alemán a inglés

- [opus-mt-en-fr](https://huggingface.co/Helsinki-NLP/opus-mt-en-fr) - inglés a francés

- [opus-mt-fr-en](https://huggingface.co/Helsinki-NLP/opus-mt-fr-en) - drancés a inglés

- [opus-mt-it-en](https://huggingface.co/Helsinki-NLP/opus-mt-it-en) - italiano a inglés

- [opus-mt-zh-en](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en) - chino a inglés

Usa el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) en el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) para determinar qué modelo quieres activo al procesar archivos a través del módulo `translate`.

### Parametros de los Modelos en el Modulo `translate`

Ninguno de los modelos en el módulo `translate` es parametrizable. Por ende, al elegir qué modelo usarás a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), `params` siempre será un diccionario vacío. Por ejemplo:

```python
# ejemplo de selección de modelo para el módulo translate en el método process
modules={'translate': {'model':'opus-mt-zh-en',
                       'params': {}}}
```

### Un *Pipeline* de Modulo Unico para el Modulo `translate`

Haz [clic aquí](../../ejemplos/ejemplos_pipelines_modulo_unico/unico_translate_traduccion.md) para detallar un ejemplo de un *pipeline* de módulo único con un módulo `translate`.

### Mas Informacion sobre el Modulo `translate`: IO y Conectabilidad

Haz [clic aquí](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md) para visitar documentación Krixik titulada `Métodos de Conveniencia (¡y Más!)`. Allí encontrarás dos herramientas con las que puedes aprender más sobre el módulo `translate`: 

- [Ve Ejemplos de Entradas y Salidas de un Módulo](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-ejemplos-de-entradas-y-salidas-de-un-modulo)

- [Ve Data de Conectividad de un Módulo con el Método `click_data`](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-data-de-conectividad-de-un-modulo-con-el-metodo-view_module_click_data)
