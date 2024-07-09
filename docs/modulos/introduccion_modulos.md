## Introducción a Módulos Krixik (Módulos Hoy Disponibles)

A continuación encontrarás una lista de todos los [módulos](../sistema/creacion_de_pipelines/componentes_de_un_pipeline_de_krixik.md) actualmente disponibles para el [ensamblaje](../sistema/creacion_de_pipelines/creacion_de_pipelines.md) de *pipelines* Krixik. Al estudiar la lista y empezar a tener ideas sobre posibles *pipelines*, ten en cuenta que (siempre y cuando encajen sus entradas y salidas) no hay restricción en cuanto a cómo puedes conectar los módulos. La repetición, incluso la repetición en serie, está permitida. También ten en cuenta que las puertas están abiertas para que incorpores [tus propios módulos y modelos](agrega_tus_propios_modulos_o_modelos.md) a Krixik.

Dado que la lista de módulos Krixik—y de los modelos dentro de ellos—crecerá constantement, sugerimos que marques esta página como una de tus favoritas.

### Módulos IA

- [Leyenda de Imagen](modulos_ia/modulo_caption_leyenda_de_imagen.md): Genera una leyenda textual para una imagen.

- [ROC (OCR - Reconocimiento Óptico de Caracters)](modulos_ia/modulo_ocr_roc.md): Extrae texto de una imagen.

- [Análisis de Sentimiento](modulos_ia/modulo_sentiment_analisis_de_sentimiento.md): Hace análisis de sentimiento sobre fragmentos de texto (¿es este texto positivo/negativo/neutral?). 

- [Resumen](modulos_ia/modulo_summarize_resumen.md): Resume texto. 

- [Encaje Léxico](modulos_ia/modulo_text-embedder_encaje_lexico.md): Convierte texto de entrada en vectores numéricos. Estos luego se pueden guardar en una base de datos vectorial para habilitar [`búsqueda semántica`](../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md).

- [Transcripción](modulos_ia/modulo_transcribe_transcripcion.md): Transcribe el contenido de un archivo audio y devuelve el texto en un archivo JSON.

- [Traducción](modulos_ia/modulo_translate_traduccion.md): Traduce texto a otro idioma.

### Módulos de Bases de Datos

- [Base de Datos Vectorial](modulos_de_bases_de_datos/modulo_vector-db_base_de_datos_vectorial.md): Recibe vectores y crea una base de datos vectorial con ellos. Habilita [`búsqueda semántica`](../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md).

- [Base de Datos de Palabras Clave](modulos_de_bases_de_datos/modulo_keyword-db_base_de_datos_de_palabras_clave.md): Crea una base de datos relacional con las palabras clave identificadas en el texto de entrada. Habilita [`búsqueda por palabras clave`](../sistema/metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md).

### Módulos de Funciones de Apoyo

- [Fragmentación de Texto](modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md): Divide archivos textuales en fragmentos que potencialmente se sobreponen y los devuelve en un archivo JSON.

- [JSON a TXT](modulos_de_funciones_de_apoyo/modulo_json-to-txt.md): Convierte un JSON de entrada en un archivo TXT, concatenando los fragmentos de texto del JSON en un solo *string*.

### Agrega tus Propios Módulos o Modelos

- [Agrega tus Propios Módulos o Modelos](agrega_tus_propios_modulos_o_modelos.md): Cómo incorporar tus propios módulos o modelos a Krixik.
