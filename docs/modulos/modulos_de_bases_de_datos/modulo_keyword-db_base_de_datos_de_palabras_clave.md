## El Módulo `keyword-db` (Base de Datos de Palabras Clave)
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/modules/database_modules/keyword-db_module/)

El módulo `keyword-db` (base de datos de palabras clave) toma como un entrada un documento textual, extrae todas sus palabras clave, identifica el truncamiento lematizado de cada una, y devuelve una base de datos `SQLite` con ese contenido.

Esta introducción al módulo `keyword-db` se divide en las siguientes secciones:

- [Entradas y Salidas del Módulo `keyword-db`](#entradas-y-salidas-del-modulo-keyword-db)
- [Modelos Disponibles en el Módulo `keyword-db`](#modelos-disponibles-en-el-modulo-keyword-db)
- [Parámetros de Modelo en el Módulo `keyword-db`](#parametros-de-modelo-en-el-modulo-keyword-db)
- [Un *Pipeline* de Módulo Único para el Módulo `keyword-db` y Consultas Locales](#un-pipeline-de-modulo-unico-para-el-modulo-keyword-db-y-consultas-locales)
- [El Método `keyword_search`](#el-metodo-keyword_search)
- [Más Información sobre el Módulo `keyword-db`: IO y Conectabilidad](#mas-informacion-sobre-el-modulo-keyword-db-io-y-conectabilidad)

### Entradas y Salidas del Modulo `keyword-db`

El módulo `keyword-db` (base de datos de palabras clave) recibe entradas de documentos textuales. Los siguientes formatos de archivo son aceptables:

- TXT

- PDF (se convierte automáticamente en TXT antes de procesar)

- DOCX (se convierte automáticamente en TXT antes de procesar)

- PPTX (se convierte automáticamente en TXT antes de procesar)

El módulo `keyword-db` devuelve un archivo de base de datos `SQLite` que contiene todas las palabras clave (es decir, excluyendo "[stop words](../../sistema/metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md#stop-words-palabras-ignoradas)") del documento y el truncamiento lematizado de cada una.

### Modelos Disponibles en el Modulo `keyword-db`

Puedes utilizar el siguiente modelo al usar el módulo `keyword-db`:

- `base` - (predeterminado) Desarrollado por Krixik

Usa el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) en el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) para determinar qué modelo quieres activo al procesar archivos a través del módulo `keyword-db`, pero ten en cuenta que por lo pronto solo existe una opción.

### Parametros de Modelo en el Modulo `keyword-db`

El modelo `base` del módulo `keyword-db` no es parametrizable. Por ende, si especificas qué modelo usarás a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), `params` siempre será un diccionario vacío. Por ejemplo:

```python
# ejemplo de especificación de modelo para el módulo keyword-db en el método process
modules={'keyword-db': {'model':'base',
                        'params': {}}}
```

### Un *Pipeline* de Modulo Unico para el Modulo `keyword-db` y Consultas Locales

Haz [clic aquí](../../ejemplos/ejemplos_pipelines_modulo_unico/unico_keyword-db_base_de_datos_de_palabras_clave.md) para detallar un ejemplo de un *pipeline* de módulo único con un módulo `keyword-db`.

Ten en cuenta que las salidas de este *pipeline* son en formato archivo de base de datos `SQLITE`, un formato no legible por humanos.

Este ejemplo también incluye una introducción a cómo hacer [consultas locales](../../ejemplos/ejemplos_pipelines_modulo_unico/unico_keyword-db_base_de_datos_de_palabras_clave.md#consulta-bases-de-datos-de-salida-localmente) a tus salidas `SQLite`.

### El Metodo `keyword_search`

Cualquier *pipeline* que contiene un módulo `keyword-db` tiene acceso al método [`keyword_search`](../../sistema/metodos_de_busqueda/metodo_keyword_search_busqueda_por_palabras_clave.md). Este te permite hacer búsqueda de palabras clave sobre las bases de datos `SQLite` que has creado.

### Mas Informacion sobre el Modulo `keyword-db`: IO y Conectabilidad

Haz [clic aquí](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md) para visitar documentación Krixik titulada `Métodos de Conveniencia (¡y Más!)`. Allí encontrarás dos herramientas con las que puedes aprender más sobre el módulo `keyword-db`: 

- [Ve Ejemplos de Entradas y Salidas de un Módulo](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-ejemplos-de-entradas-y-salidas-de-un-modulo)

- [Ve Data de Conectividad de un Módulo con el Método `click_data`](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-data-de-conectividad-de-un-modulo-con-el-metodo-view_module_click_data)
