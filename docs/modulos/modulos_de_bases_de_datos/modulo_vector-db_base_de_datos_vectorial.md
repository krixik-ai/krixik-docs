<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/modules/database_modules/vector-db_module.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## El Módulo `vector-db` (Base de Datos Vectorial)

El módulo `vector-db` (base de datos vectorial) toma como entrada un arreglo NumPy, indexa sus vectores, y devuelve una base de datos [FAISS](https://github.com/facebookresearch/faiss) indexada.

Esta introducción al módulo `vector-db` se divide en las siguientes secciones:

- [Entradas y Salidas del Módulo `vector-db`](#entradas-y-salidas-del-modulo-vector-db)
- [Modelos Disponibles en el Módulo `vector-db`](#modelos-disponibles-en-el-modulo-vector-db)
- [Parámetros de Modelo en el Módulo `vector-db`](#parametros-de-modelo-en-el-modulo-vector-db)
- [Un *Pipeline* de Módulo Único para el Módulo `vector-db` y Consultas Locales](#un-pipeline-de-modulo-unico-para-el-modulo-vector-db-y-consultas-locales)
- [El Método `semantic_search`](#el-metodo-semantic_search)
- [Más Información sobre el Módulo `vector-db`: IO y Conectabilidad](#mas-informacion-sobre-el-modulo-vector-db-io-y-conectabilidad)

### Entradas y Salidas del Modulo `vector-db`

El módulo `vector-db` recibe como entrada un archivo NPY que consiste de un solo arreglo NumPy. Cada fila en el arreglo es un vector a indexar para búsqueda semántica (también conocida como búsqueda vectorial).

El módulo `vector-db` devuelve un archivo de base de datos [FAISS](https://github.com/facebookresearch/faiss) indexada.

Para ver un ejemplo de un pequeño archivo de entrada para este módulo, detalla la salida del siguiente código:


```python
# detallar el contenido de un pequeño archivo de entrada
import numpy as np

test_file = data_dir + "input/vectores.npy"
np.load(test_file)
```




    array([[0, 1],
           [1, 0],
           [1, 1]], dtype=int64)



### Modelos Disponibles en el Modulo `vector-db`

Puedes utilizar el siguiente modelo al usar el módulo `vector-db`:

- [faiss](https://github.com/facebookresearch/faiss) (predeterminado)

Usa el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) en el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) para determinar qué modelo quieres activo al procesar archivos a través del módulo `vector-db`, pero ten en cuenta que por lo pronto solo existe una opción.

### Parametros de Modelo en el Modulo `vector-db`

El modelo [`faiss`](https://github.com/facebookresearch/faiss) del módulo `vector-db` no es parametrizable. Por ende, si especificas qué modelo usarás a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), `params` siempre será un diccionario vacío. Por ejemplo:

```python
# ejemplo de especificación de modelo para el módulo vector-db en el método process
modules={'vector-db': {'model':'faiss',
                       'params': {}}}
```

### Un *Pipeline* de Modulo Unico para el Modulo `vector-db` y Consultas Locales

Haz [clic aquí](../../ejemplos/ejemplos_pipelines_modulo_unico/unico_vector-db_base_de_datos_vectorial.md) para detallar un ejemplo de un *pipeline* de módulo único con un módulo `vector-db`.

Ten en cuenta que las salidas de este *pipeline* son en formato archivo de base de datos [FAISS](https://github.com/facebookresearch/faiss), un formato no legible por humanos. Además, para que este *pipeline* de módulo único funcione, necesitarás tener por separado uno o más archivos NPY en formato correcto que te sirvan de entradas.

El ejemplo también incluye una introducción a cómo hacer [consultas locales](../../ejemplos/ejemplos_pipelines_modulo_unico/unico_vector-db_base_de_datos_vectorial.md#consulta-bases-de-datos-de-salida-localmente) a tus salidas en formato base de dato [FAISS](https://github.com/facebookresearch/faiss).

### El Metodo `semantic_search`

Cualquier pipeline que contiene un módulo `vector-db` precedido de un módulo [`text-embedder`](../modulos_ia/modulo_text-embedder_encaje_lexico.md) tiene acceso al método [`semantic_search`](../../sistema/metodos_de_busqueda/metodo_semantic_search_busqueda_semantica.md). Este te permite hacer búsqueda semántica sobre las bases de datos vectoriales que se han creado.

### Mas Informacion sobre el Modulo `vector-db`: IO y Conectabilidad

Haz [clic aquí](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md) para visitar documentación Krixik titulada `Métodos de Conveniencia (¡y Más!)`. Allí encontrarás dos herramientas con las que puedes aprender más sobre el módulo `vector-db`: 

- [Ve Ejemplos de Entradas y Salidas de un Módulo](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-ejemplos-de-entradas-y-salidas-de-un-modulo)

- [Ve Data de Conectividad de un Módulo con el Método `click_data`](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-data-de-conectividad-de-un-modulo-con-el-metodo-click_data)
