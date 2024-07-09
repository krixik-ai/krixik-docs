## El Módulo `caption` (Leyenda de Imagen)

El módulo `caption` (leyenda de imagen) toma como entrada un archivo de imagen y devuelve una descripción textual de esa imagen.

Esta introducción al módulo `caption` se divide en las siguientes secciones:

- [Entradas y Salidas del Módulo `caption`](#entradas-y-salidas-del-modulo-caption)
- [Modelos Disponibles en el Módulo `caption`](#modelos-disponibles-en-el-modulo-caption)
- [Parámetros de los Modelos en el Módulo `caption`](#parametros-de-los-modelos-en-el-modulo-caption)
- [Un *Pipeline* de Módulo Único para el Módulo `caption`](#un-pipeline-de-modulo-unico-para-el-modulo-caption)
- [Más Información sobre el Módulo `caption`: IO y Conectabilidad](#mas-informacion-sobre-el-modulo-caption-io-y-conectabilidad)

### Entradas y Salidas del Modulo `caption`

El módulo `caption` (leyenda de imagen) recibe entradas de archivos de imagen. Los siguientes formatos de archivo son aceptables:

- JPG

- JPEG

- PNG

El módulo `caption` devuelve un archivo JSON. El elemento principal de este JSON es un diccionario que contiene la leyenda generada de la imagen.

### Modelos Disponibles en el Modulo `caption`

Puedes activar cualquiera de los siguientes modelos al usar el módulo `caption`:

- [vit-gpt2-image-captioning](https://huggingface.co/nlpconnect/vit-gpt2-image-captioning) (predeterminado)

- [git-base](https://huggingface.co/microsoft/git-base)

- [blip-image-captioning-base](https://huggingface.co/Salesforce/blip-image-captioning-base)

- [blip-image-captioning-large](https://huggingface.co/Salesforce/blip-image-captioning-large)

Usa el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) en el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) para determinar qué modelo quieres activo al procesar archivos a través del módulo `caption`.

### Parametros de los Modelos en el Modulo `caption`

Ninguno de los modelos en el módulo `caption` es parametrizable. Por ende, al elegir qué modelo usarás a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), `params` siempre será un diccionario vacío. Por ejemplo:

```python
# ejemplo de selección de modelo para el módulo caption en el método process
modules={'caption': {'model':'blip-image-captioning-base',
                     'params': {}}}
```

### Un *Pipeline* de Modulo Unico para el Modulo `caption`

Haz [clic aquí](../../ejemplos/ejemplos_pipelines_modulo_unico/unico_caption_leyenda_de_imagen.md) para detallar un ejemplo de un *pipeline* de módulo único con un módulo `caption`.

### Mas Informacion sobre el Modulo `caption`: IO y Conectabilidad

Haz [clic aquí](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md) para visitar documentación Krixik titulada `Métodos de Conveniencia (¡y Más!)`. Allí encontrarás dos herramientas con las que puedes aprender más sobre el módulo `caption`: 

- [Ve Ejemplos de Entradas y Salidas de un Módulo](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-ejemplos-de-entradas-y-salidas-de-un-modulo)

- [Ve Data de Conectividad de un Módulo con el Método `click_data`](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-data-de-conectividad-de-un-modulo-con-el-metodo-click_data)
