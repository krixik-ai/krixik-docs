## Ejemplos de *Pipelines* Krixik

¿Estás listo para inspirarte con algunos ejemplos de *pipelines* que puedes construir con Krixik? ¡Existen muchísimas posibilidades!

La primera sección a seguir detalla todos los *pipelines* de módulo único que se pueden armar hoy. Usa estos si hay un módulo (o modelo) específico que quieres usar individualmente.

Luego hay detalle sobre algunos ejemplos de pipelines multimodulares, y es allí donde realmente reluce el poder de Krixik. La última sección contiene ejemplos de *pipelines* multimodulares con los que puedes hacer búsqueda (ya sea de palabras clave o semántica); su funcionamiento es un poco diferente al de las demás.

### *Pipelines* de Módulo Único

- [Leyenda de Imagen](ejemplos_pipelines_modulo_unico/unico_caption_leyenda_de_imagen.md)

- [ROC (OCR - Reconocimiendo Óptico de Caracteres)](ejemplos_pipelines_modulo_unico/unico_ocr_roc.md)

- [Análisis de Sentimiento](ejemplos_pipelines_modulo_unico/unico_sentiment_analisis_de_sentimiento.md)

- [Resumen](ejemplos_pipelines_modulo_unico/unico_summarize_resumen.md)

- [Encaje Léxico](ejemplos_pipelines_modulo_unico/unico_text-embedder_encaje_lexico.md)

- [Fragmentación de Texto](ejemplos_pipelines_modulo_unico/unico_parser_fragmentacion.md)

- [Transcripción](ejemplos_pipelines_modulo_unico/unico_transcribe_transcripcion.md)

- [Traducción](ejemplos_pipelines_modulo_unico/unico_translate_traduccion.md)

- [Base de Datos de Palabras Clave](ejemplos_pipelines_modulo_unico/unico_keyword-db_base_de_datos_de_palabras_clave.md)

- [Base de Datos de Vectores](ejemplos_pipelines_modulo_unico/unico_vector-db_base_de_datos_vectorial.md)

- [JSON a TXT](ejemplos_pipelines_modulo_unico/unico_json-to-txt.md)

### Pipelines Multimodulares Sin Búsqueda

- [Resumen Recursivo](ejemplos_pipelines_multi_modulo_sin_busqueda/multi_resumen_recursivo.md): Conecta varios módulos [`summarize`](../modulos/modulos_ia/modulo_summarize_resumen.md) secuencialmente. Mientras más larga la cadena de módulos, más breve y abstracto el resumen generado.

- [Transcripción Traducida](ejemplos_pipelines_multi_modulo_sin_busqueda/multi_transcripcion_traducida.md): Tras [`transcribir`](../modulos/modulos_ia/modulo_transcribe_transcripcion.md) un audio de entrada, [`traduce`](../modulos/modulos_ia/modulo_translate_traduccion.md) la transcripción al idioma seleccionado.

- [Análisis de Sentimiento sobre Transcripción](ejemplos_pipelines_multi_modulo_sin_busqueda/multi_analisis_de_sentimiento_sobre_transcripcion.md): Tras [`transcribir`](../modulos/modulos_ia/modulo_transcribe_transcripcion.md) un audio de entrada, hace [`análisis de sentimiento`](../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md) sobre cada frase de la transcripción.

- [Análisis de Sentimiento sobre Traducción](ejemplos_pipelines_multi_modulo_sin_busqueda/multi_analisis_de_sentimiento_sobre_traduccion.md): [`Traduce`](../modulos/modulos_ia/modulo_translate_traduccion.md) texto de entrada y luego hace [`análisis de sentimiento`](../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md) sobre cada frase de la traducción.

- [Análisis de Sentimiento sobre Transcripción Traducida](ejemplos_pipelines_multi_modulo_sin_busqueda/multi_analisis_de_sentimiento_sobre_transcripcion_traducida.md): Tras primero [`transcribir`](../modulos/modulos_ia/modulo_transcribe_transcripcion.md) un audio de entrada y [`traducir`](../modulos/modulos_ia/modulo_translate_traduccion.md) la transcripción, hace [`análisis de sentimiento`](../modulos/modulos_ia/modulo_sentiment_analisis_de_sentimiento.md) sobre cada frase de la traducción.

### Pipelines Multimodulares de Búsqueda

- [Introducción a Pipelines de Búsqueda](ejemplos_pipelines_de_busqueda/introduccion_pipelines_de_busqueda.md): Los *pipelines* de búsqueda requieren uno de dos métodos adicionales para las búsquedas. Acá aprenderás sobre ellos.

- [Búsqueda Semántica Básica](ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_basica.md): Habilita `búsqueda semántica` sobre un archivo textual de entrada.

- [Búsqueda Semántica Sobre Fragmentos](ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_sobre_fragmentos.md): Habilita `búsqueda semántica` sobre un archivo JSON de entrada.

- [Búsqueda por Palabras Clave](ejemplos_pipelines_de_busqueda/multi_busqueda_por_palabras_clave_basica.md): Habilita `búsqueda por palabras clave` sobre un archivo textual de entrada.

- [Búsqueda Semántica Sobre Transcripción](ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_sobre_transcripcion.md): [`Transcribe`](../modulos/modulos_ia/modulo_transcribe_transcripcion.md) un archivo audio de entrada y habilita `búsqueda semántica` sobre la transcripción.

- [Búsqueda por Palabras Clave sobre Transcripción](ejemplos_pipelines_de_busqueda/multi_busqueda_por_palabras_clave_sobre_transcripcion.md): [`Transcribe`](../modulos/modulos_ia/modulo_transcribe_transcripcion.md) un archivo audio de entrada y habilita `búsqueda por palabras clave` sobre la transcripción.

- [Búsqueda Semántica Sobre Traducción](ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_sobre_traduccion.md): [`Traduce`](../modulos/modulos_ia/modulo_translate_traduccion.md) un archivo textual de entrada y habilita `búsqueda semántica` sobre la traducción.

- [Búsqueda Semántica Sobre Transcripción Traducida](ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_sobre_transcripcion_traducida.md): [`Transcribe`](../modulos/modulos_ia/modulo_transcribe_transcripcion.md) un archivo audio de entrada, lo [`traduce`](../modulos/modulos_ia/modulo_translate_traduccion.md) a otro idioma, y habilita `búsqueda semántica` sobre la traducción.

- [Búsqueda Semántica Sobre ROC (OCR)](ejemplos_pipelines_de_busqueda/multi_busqueda_semantica_sobre_roc.md): [`Extrae texto`](../modulos/modulos_ia/modulo_ocr_roc.md) de una imagen de entrada y habilita `búsqueda semántica` sobre el texto extraído.

- [Búsqueda por Palabras Clave Sobre Leyendas de Imagen](ejemplos_pipelines_de_busqueda/multi_busqueda_por_palabras_clave_sobre_leyendas_de_imagen.md): Recibe una imagen de entrada, le genera una [`leyenda textual`](../modulos/modulos_ia/modulo_caption_leyenda_de_imagen.md), y habilita `búsqueda por palabras clave` sobre la leyenda.
