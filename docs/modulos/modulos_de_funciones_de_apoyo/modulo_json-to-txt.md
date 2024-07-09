## El Módulo `json-to-txt`

El módulo `json-to-txt` toma como entrada una serie de fragmentos de texto, los concatena en un solo *string* en el que los antiguos fragmentos ahora son separados por un espacio doble ("  ") y devuelve este nuevo *string* en un archivo de texto.

Esta introducción al módulo `json-to-txt` se divide en las siguientes secciones:

- [Entradas y Salidas del Módulo `json-to-txt`](#entradas-y-salidas-del-modulo-json-to-txt)
- [Modelos Disponibles en el Módulo `json-to-txt`](#modelos-disponibles-en-el-modulo-json-to-txt)
- [Parametros de Modelo en el Módulo `json-to-txt`](#parametros-de-modelo-en-el-modulo-json-to-txt)
- [Un *Pipeline* de Módulo Único para el Módulo `json-to-txt`](#un-pipeline-de-modulo-unico-para-el-modulo-json-to-txt)
- [Más Información sobre el Módulo `json-to-txt`: IO y Conectabilidad](#mas-informacion-sobre-el-modulo-json-to-txt-io-y-conectabilidad)

### Entradas y Salidas del Modulo `json-to-txt`

El módulo `json-to-txt` recibe entradas en formato JSON. Las entradas JSON deben respetar [esta estructura](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/formato_JSON_entrada.md).

El módulo `json-to-txt` devuelve un archivo TXT en el que todos los fragmentos del JSON se han concatenado en un solo *string*.

### Modelos Disponibles en el Modulo `json-to-txt`

Puedes utilizar el siguiente modelo al usar el módulo `json-to-txt`:

- `base` - (predeterminado) Desarrollado por Krixik. No es un modelo sino una función de apoyo.

Usa el argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) en el método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) para determinar qué modelo quieres activo al procesar archivos a través del módulo `json-to-txt`, pero ten en cuenta que por lo pronto solo existe una opción.

### Parametros de Modelo en el Modulo `json-to-txt`

El modelo `base` del módulo `json-to-txt` no es parametrizable. Por ende, si especificas qué modelo usarás a través del argumento [`modules`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) del método [`process`](../../sistema/parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md), `params` siempre será un diccionario vacío. Por ejemplo:

```python
# ejemplo de especificación de modelo para el módulo json-to-txt en el método process
modules={'json-to-txt': {'model':'base',
                         'params': {}}}
```

### Un *Pipeline* de Modulo Unico para el Modulo `json-to-txt`

Haz [clic aquí](../../ejemplos/ejemplos_pipelines_modulo_unico/unico_json-to-txt.md) para detallar un ejemplo de un *pipeline* de módulo único con un módulo `json-to-txt`.

### Mas Informacion sobre el Modulo `json-to-txt`: IO y Conectabilidad

Haz [clic aquí](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md) para visitar documentación Krixik titulada `Métodos de Conveniencia (¡y Más!)`. Allí encontrarás dos herramientas con las que puedes aprender más sobre el módulo `json-to-txt`: 

- [Ve Ejemplos de Entradas y Salidas de un Módulo](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-ejemplos-de-entradas-y-salidas-de-un-modulo)

- [Ve Data de Conectividad de un Módulo con el Método `click_data`](../../sistema/metodos_de_conveniencia/metodos_de_conveniencia.md#ve-data-de-conectividad-de-un-modulo-con-el-metodo-click_data)
