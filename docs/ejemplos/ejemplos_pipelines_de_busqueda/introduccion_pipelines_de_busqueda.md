## *Pipelines* de Búsqueda Krixik
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/examples/search_pipeline_examples/search_pipelines_overview/)

### Introducción a *Pipelines* de Búsqueda

Los *pipelines* de búsqueda son aquellos que habilitan funciones de búsqueda sobre documentos textuales.

Dos tipos de búsqueda pueden actualmente ser habilitados en Krixik: [búsqueda semántica](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) y [búsqueda por palabras clave](../../sistema/metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md). Dependiendo de cuál de estos quieras usar, el último módulo del *pipeline* debe respectivamente ser [`vector-db` (base de datos vectorial)](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md) o [`keyword-db` (base de datos de palabras clave)](../../modulos/modulos_de_bases_de_datos/modulo_keyword-db_base_de_datos_de_palabras_clave.md).

Los *pipelines* de búsqueda son más complejos que otros *pipelines* porque usarlos requiere un paso adicional.

- Primero se deben "cargar" archivos en el *pipeline* con el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).

- Los métodos [`keyword_search` (búsqueda por palabras clave)](../../sistema/metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md) y [`semantic_search` (búsqueda semántica)](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) pueden ser invocados sobre un *pipeline* de búsqueda una vez uno o más archivos se han [procesado](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) a través de él. Ten en cuenta que el método [`keyword_search`](../../sistema/metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md) solamente se puede invocar sobre un *pipeline* que termina con el módulo [`keyword-db`](../../modulos/modulos_de_bases_de_datos/modulo_keyword-db_base_de_datos_de_palabras_clave.md) y el método [`semantic_search`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) solo puede ser invocado sobre un *pipeline* que termina con el módulo [`text-embedder`](../../modulos/modulos_ia/modulo_text-embedder_encaje_lexico.md) seguido del módulo [`vector-db`](../../modulos/modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md).

### Ejemplos de Pipelines de Búsqueda

- [Búsqueda Semántica Básica](multi_busqueda_semantica_basica.md): Habilita [`búsqueda semántica`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) sobre entradas que son archivos de texto.

- [Búsqueda Semántica Sobre Fragmentos](multi_busqueda_semantica_sobre_fragmentos.md): Habilita [`búsqueda semántica`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) sobre fragmentos de texto en entradas JSON.

- [Búsqueda por Palabras Clave Básica](multi_busqueda_por_palabras_clave_basica.md): Habilita [`búsqueda por palabras clave`](../../sistema/metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md) sobre entradas que son archivos de texto.

- [Búsqueda Semántica Sobre Transcripción](multi_busqueda_semantica_sobre_transcripcion.md): [`Transcribe`](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md) entradas que son archivos audio y luego habilita [`búsqueda semántica`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) sobre la transcripción.

- [Búsqueda por Palabras Clave Sobre Transcripción](multi_busqueda_por_palabras_clave_sobre_transcripcion.md): [`Transcribe`](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md) entradas que son archivos audio y luego habilita [`búsqueda por palabras clave`](../../sistema/metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md) sobre la transcripción.

- [Búsqueda Semántica Sobre Traducción](multi_busqueda_semantica_sobre_traduccion.md): [`Traduce`](../../modulos/modulos_ia/modulo_translate_traduccion.md) entradas que son archivos de texto y luego habilita [`búsqueda semántica`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) sobre la traducción.

- [Búsqueda Semántica Sobre Transcripción Traducida](multi_busqueda_semantica_sobre_transcripcion_traducida.md): [`Transcribe`](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md) entradas que son archivos audio, [`traduce`](../../modulos/modulos_ia/modulo_translate_traduccion.md) la transcripción a otro idioma y luego habilita [`búsqueda semántica`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) sobre la traducción.

- [Búsqueda Semántica Sobre ROC (OCR)](multi_busqueda_semantica_sobre_roc.md): [`Extrae texto`](../../modulos/modulos_ia/modulo_ocr_roc.md) de entradas que son imágenes y luego habilita [`búsqueda semántica`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md) sobre el texto extraído.

- [Búsqueda por Palabras Clave Sobre Leyendas de Imagen](multi_busqueda_por_palabras_clave_sobre_leyendas_de_imagen.md): Genera [`leyendas`](../../modulos/modulos_ia/modulo_caption_leyenda_de_imagen.md) de entradas que son imágenes y luego habilita [`búsqueda por palabras clave`](../../sistema/metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md) sobre las leyendas.
