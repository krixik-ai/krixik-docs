## El Módulo `ocr` (ROC - Reconocimiento Óptico de Caracteres)

El módulo `ocr` (ROC - Reconocimiento Óptico de Caracteres) toma como entrada un archivo de imagen y devuelve todo texto encontrado dentro de esa imagen en un archivo JSON.

Esta introducción al módulo `ocr` se divide en las siguientes secciones:

- [Entradas y Salidas del Módulo `ocr`](#entradas-y-salidas-del-modulo-ocr)
- [Modelos Disponibles en el Módulo `ocr`](#modelos-disponibles-en-el-modulo-ocr)
- [Parámetros de los Modelos en el Módulo `ocr`](#parametros-de-los-modelos-en-el-modulo-ocr)
- [Un *Pipeline* de Módulo Único para el Módulo `ocr`](#un-pipeline-de-modulo-unico-para-el-modulo-ocr)
- [Más Información sobre el Módulo `ocr`: IO y Conectabilidad](#mas-informacion-sobre-el-modulo-ocr-io-y-conectabilidad)

### Entradas y Salidas del Modulo `ocr`

El módulo `ocr` (ROC - Reconocimiento Óptico de Caracteres) recibe entradas de archivos de imagen. Los siguientes formatos de archivo son aceptables:

- JPG

- JPEG

- PNG

El módulo `ocr` devuelve un archivo JSON. El archivo JSON incluye todo el texto identificado en la imagen. También incluye las coordenadas (en pixeles) de cada trozo de texto identificado.

### Modelos Disponibles en el Modulo `ocr`

Puedes activar cualquiera de los siguientes modelos al usar el módulo `ocr`:

- [tesseract-en](https://github.com/tesseract-ocr/tesseract) - (predeterminado) inglés

- [tesseract-es](https://github.com/tesseract-ocr/tesseract) - español

Usa el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) en el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) para determinar qué modelo quieres activo al procesar archivos a través del módulo `ocr`.

### Parametros de los Modelos en el Modulo `ocr`

Ninguno de los modelos en el módulo `ocr` es parametrizable. Por ende, al elegir qué modelo usarás a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), `params` siempre será un diccionario vacío. Por ejemplo:

```python
# ejemplo de selección de modelo para el módulo ocr en el método process
modules={'ocr': {'model':'tesseract-es',
                 'params': {}}}
```

### Un *Pipeline* de Modulo Unico para el Modulo `ocr`

Haz [clic aquí](../../ejemplos/ejemplos_pipelines_modulo_unico/unico_ocr_roc.md) para detallar un ejemplo de un *pipeline* de módulo único con un módulo `ocr`.

### Mas Informacion sobre el Modulo `ocr`: IO y Conectabilidad

Haz [clic aquí](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md) para visitar documentación Krixik titulada `Métodos de Conveniencia (¡y Más!)`. Allí encontrarás dos herramientas con las que puedes aprender más sobre el módulo `ocr`: 

- [Ve Ejemplos de Entradas y Salidas de un Módulo](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-ejemplos-de-entradas-y-salidas-de-un-modulo)

- [Ve Data de Conectividad de un Módulo con el Método `click_data`](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-data-de-conectividad-de-un-modulo-con-el-metodo-click_data)
