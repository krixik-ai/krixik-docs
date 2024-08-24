<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/pipeline_creation/saving_and_loading_pipelines.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Guardar y Cargar *Pipelines*
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/system/pipeline_creation/saving_and_loading_pipelines/)

Esta introducción a guardar y cargar *pipelines* se divide en las siguientes secciones:

- [El Método `save_pipeline`](#el-metodo-save_pipeline)
- [El Método `load_pipeline`](#el-metodo-load_pipeline)
- [La Función `reset_pipeline`](#la-funcion-reset_pipeline)

### El Metodo `save_pipeline`

En Krixik, guardar tu *pipeline* quiere decir *guardar su [configuración](configuracion_de_pipelines.md)* en disco.

Puedes guardar la [configuración](configuracion_de_pipelines.md) de un *pipeline* con el método `save_pipeline`. Este método toma un argumento (requerido):

- `config_path`: Una ruta de archivo local válida. El archivo no tiene que existir, pero la ruta en directorios sí debe ser posible.

`config_path` debe terminar con una extensión `.yml` o `.yaml`. Este es actualmente el único formato de archivo con el que Krixik guarda *pipelines*.

Para ver cómo funciona, primero tendrás que crear un *pipeline* con el método [`create_pipeline`](creacion_de_pipelines.md):


```python
# primero crea un pipeline
pipeline = krixik.create_pipeline(name="guardar_y_cargar_pipelines_1", module_chain=["summarize", "summarize", "keyword-db"])
```

Ahora que tienes un *pipeline* puedes usar el método `save_pipeline` para guardar ese *pipeline* en disco:


```python
# guardar la configuración de un pipeline en disco (con ejemplo de ruta; la ruta debe obedecer lo que dicte tu sistema operativo)
pipeline.save_pipeline(config_path=data_dir + "configs-de-pipeline/guarda-demo-pipeline.yaml")
```

Para facilitar las cosas, si un archivo con ese nombre de archivo no existe en la ubicación indicada, Krixik creará el archivo localmente y luego guardará tu *pipeline* en él.

### El Metodo `load_pipeline`

Dado que la [configuración](configuracion_de_pipelines.md) de un *pipeline* es su descripción fundamental, cualquier archivo válido de configuración puede cargarse a Krixik, así recreando el *pipeline* asociado.

El método `load_pipeline` toma un argumento (requerido):

- `config_path`: Una ruta de archivo local válida.

Para que el método `load_pipeline` funcione, el archivo indicado por `config_path` debe (a) existir, (b) tener extensión `.yaml` o `.yml` y (c) contener una [configuración](configuracion_de_pipelines.md) de *pipeline* Krixik con formato adecuado. Si uno de estos no es el caso, el método fallará. Si antes [guardaste](#el-metodo-save_pipeline) un *pipeline* Krixik en esa ubicación con ese nombre de archivo, el método funcionará bien.

El método `load_pipeline` se usa de la siguiente manera:


```python
# carga un pipeline a memoria por medio de un archivo válido de configuración
mi_pipeline_2 = krixik.load_pipeline(config_path=data_dir + "configs-de-pipeline/guarda-demo-pipeline.yaml")
```

Verás que no tienes que haber previamente guardado el *pipeline* tú. Por ejemplo, puede que un colega te haya compartido una [configuración](configuracion_de_pipelines.md) de *pipeline*, o que hayas escrito el archivo desde cero. Siempre y cuando el archivo config tenga formato correcto, el método `load_pipeline` funcionará como debe.

### La Funcion `reset_pipeline`

El método `load_pipeline` arriba descrito vuelve a instanciar un *pipeline* previo con el mismo `name` y `module_chain`. Dado que los archivos procesados por un *pipeline* están asociados al `name` de ese *pipeline*, esos archivos están ahora asociados a este nuevo *pipeline*.

Si buscas recrear un *pipeline* pero quieres hacerlo con hoja en blanco, la manera más fácil es con la función `reset_pipeline`, que borra todos datos de proceso asociados a ese *pipeline* (es decir, cualquier cosa relacionada con todo archivo previamente procesado a través de *pipeline(s)* con ese `name`).

La función `reset_pipeline` toma un argumento (requerido):

- `pipeline`: La variable en el que objeto *pipeline* está guardado.

Ten en cuenta que esta variable _no_ es el `name` del *pipeline*. Por ejemplo, si quisieras reiniciar el primer *pipeline* creado en este documento, el argumento `pipeline` para la función `reset_pipeline` tendría el valor `pipeline` (y no el valor `guardar_y_cargar_pipelines_1`), de la siguiente manera:


```python
# elimina todos los datos procesados pertenecientes a este pipeline
reset_pipeline(pipeline)
```

Dicho de otra manera, el argumento `pipeline` de la función `reset_pipeline` es una variable al que se ha asignado un objeto *pipeline*, y `reset_pipeline` eliminará todo dato asociado al `name` de ese objeto *pipeline* en el sistema Krixik.
