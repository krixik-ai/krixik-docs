## El Módulo `sentiment` (Análisis de Sentimiento)
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/modules/ai_modules/sentiment_module/)

El módulo `sentiment` (análisis de sentimiento) toma como entrada uno o varios fragmentos de texto y devuelve cada fragmento acompañado de su desglose numérico de sentimiento (entre positivo, negativo y neutral).

Esta introducción al módulo `sentiment` se divide en las siguientes secciones:

- [Entradas y Salidas del Módulo `sentiment`](#entradas-y-salidas-del-modulo-sentiment)
- [Modelos Disponibles en el Módulo `sentiment`](#modelos-disponibles-en-el-modulo-sentiment)
- [Parámetros de los Modelos en el Módulo `sentiment`](#parametros-de-los-modelos-en-el-modulo-sentiment)
- [Un *Pipeline* de Módulo Único para el Módulo `sentiment`](#un-pipeline-de-modulo-unico-para-el-modulo-sentiment)
- [Más Información sobre el Módulo `sentiment`: IO y Conectabilidad](#mas-informacion-sobre-el-modulo-sentiment-io-y-conectabilidad)

### Entradas y Salidas del Modulo `sentiment`

El módulo `sentiment` (análisis de sentimiento) recibe entradas en formato JSON. Las entradas JSON deben respetar [este formato](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/formato_JSON_entrada.md).

El módulo `sentiment` devuelve un archivo JSON. El archivo devuelto incluye todos los fragmentos de entrada, y cada uno es acompañado por su desglose numérico de sentimiento (entre positivo, negativo y neutral). Estos tres valores de sentimiento suman a 1.0.

### Modelos Disponibles en el Modulo `sentiment`

Puedes activar cualquiera de los siguientes modelos al usar el módulo `sentiment`:

- [distilbert-base-uncased-finetuned-sst-2-english](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english) (predeterminado)

- [bert-base-multilingual-uncased-sentiment](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment)

- [distilbert-base-multilingual-cased-sentiments-student](https://huggingface.co/lxyuan/distilbert-base-multilingual-cased-sentiments-student)

- [distilroberta-finetuned-financial-news-sentiment-analysis](https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis)

Usa el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) en el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) para determinar qué modelo quieres activo al procesar archivos a través del módulo `sentiment`.

### Parametros de los Modelos en el Modulo `sentiment`

Ninguno de los modelos en el módulo `sentiment` es parametrizable. Por ende, al elegir qué modelo usarás a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), `params` siempre será un diccionario vacío. Por ejemplo:

```python
# ejemplo de selección de modelo para el módulo sentiment en el método process
modules={'sentiment': {'model':'distilroberta-finetuned-financial-news-sentiment-analysis',
                       'params': {}}}
```

### Un *Pipeline* de Modulo Unico para el Modulo `sentiment`

Haz [clic aquí](../../ejemplos/ejemplos_pipelines_modulo_unico/unico_sentiment_analisis_de_sentimiento.md) para detallar un ejemplo de un *pipeline* de módulo único con un módulo `sentiment`.

### Mas Informacion sobre el Modulo `sentiment`: IO y Conectabilidad

Haz [clic aquí](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md) para visitar documentación Krixik titulada `Métodos de Conveniencia (¡y Más!)`. Allí encontrarás dos herramientas con las que puedes aprender más sobre el módulo `sentiment`: 

- [Ve Ejemplos de Entradas y Salidas de un Módulo](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-ejemplos-de-entradas-y-salidas-de-un-modulo)

- [Ve Data de Conectividad de un Módulo con el Método `click_data`](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-data-de-conectividad-de-un-modulo-con-el-metodo-view_module_click_data)
