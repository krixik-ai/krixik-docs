## Componentes de un Pipeline Krixik
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/system/pipeline_creation/components_of_a_krixik_pipeline/)

Los [**pipelines**](creacion_de_pipelines.md) Krixik están compuestos de uno o más [**módulos**](../../modulos/introduccion_modulos.md) secuencialmente conectados. Estos módulos son contenedores para una variedad de [**modelos**](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) IA (o funciones de apoyo) [**parametrizables**](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules).

Entremos en detalle sobre cada palabra clave en la anterior descripción:

Un [**pipeline**](creacion_de_pipelines.md) es una secuencia autónoma de uno o más módulos que se consume por medio de un API sin servidor.

Un [**módulo**](../../modulos/introduccion_modulos.md) es un paso de procesamiento con una huella única de datos de entrada/salida. Cada módulo contiene uno o más modelos IA (o funciones de apoyo) parametrizables.

Un [**modelo**](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) es una función de procesamiento personalizada contenida en un módulo. Muchos de estos son modelos de IA, pero algunos son "funciones de apoyo" más simples para la preparación o transformación de datos dentro de los *pipelines*.

[**Parámetros**](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md#seleccion-de-modelo-por-medio-del-argumento-modules) pueden ser definidos para cada módulo cuando se ejecuta un *pipeline* y permiten personalización más precisa. Cada uno tiene un valor predeterminado, así que especificarlos es opcional. Por ejemplo, un elemento parametrizable es la selección de modelo IA que está activo en un módulo al procesar un *pipeline*.

--

Nuevos módulos y modelos serán añadidos con frecuencia a la librería Krixik. Para ver todos los módulos disponibles, usa la propiedad [`available_modules`](../metodos_de_conveniencia/metodos_de_conveniencia.md#ve-todos-los-modulos-disponibles-con-la-propiedad-available_modules):

```python
krixik.available_modules
```

Cada [**módulo**](../../modulos/introduccion_modulos.md) tiene su propia documentación. Esta detalla, entre otras cosas, todos los modelos disponibles para ese módulo. Por ejemplo, he aquí documentación para el módulo [`transcribe`](../../modulos/modulos_ia/modulo_transcribe_transcripcion.md).
