<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/parameters_processing_files_through_pipelines/process_status_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## El Método `process_status` (Estado de Proceso)
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/system/parameters_processing_files_through_pipelines/process_status_method/)

El método `process_status` (estado de proceso) está disponible para todo *pipeline* Krixik. Se usa cuando quieres revisar el estado de archivos que se están procesando por un *pipeline*.

Este método es particularmente útil cuando usas el método [`process`](metodo_process_procesar.md) con `wait_for_process` en `False`, pues te da visibilidad en cuanto a procesos que han continuado del lado del servidor después de que recuperas control de tu IDE.

Esta introducción del método `process_status` se divide en las siguientes secciones:

- [Argumentos del Método process_status](#argumentos-del-metodo-process_status)
- [Ejemplo de process_status](#ejemplo-de-process_status)
- [Ejemplo de process_status con Archivo Eliminado](#ejemplo-de-process_status-con-archivo-eliminado)

### Argumentos del Metodo process_status

El método `process_status` toma un solo argumento (requerido):

- `request_id`: (str) El identificador único asociado a la ejecución específica del método [`process`](metodo_process_procesar.md).

### Ejemplo de process_status

Ahora detalla cómo funciona el método `process_status` cuando el método [`process`](metodo_process_procesar.md) ha sido exitoso. El argumento `wait_for_process` se pondrá en `False`.

Primero debes crear un *pipeline* sobre el cual puedas ejecutar este ejemplo. Un *pipeline* que consiste de un solo módulo [`keyword-db`](../../modulos/modulos_de_bases_de_datos/modulo_keyword-db_base_de_datos_de_palabras_clave.md) funciona bien:


```python
# crea un pipeline de módulo único con un módulo keyword-db para este ejemplo
pipeline = krixik.create_pipeline(name="metodo_process_status_1_keyword-db", module_chain=["keyword-db"])
```

Ahora procesa un archivo a través de este *pipeline*. Usa un breve archivo TXT que contiene una porción de <u>Moby Dick</u>, de Herman Melville:


```python
# procesa el archivo TXT por el pipeline de módulo único con un módulo keyword-db con wait_for_process en False
process_output = pipeline.process(
    local_file_path=data_dir + "input/moby_dick_muy_corto.txt",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 30,  # process data will be deleted from the Krixik system in 30 minutes
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False,  # no mostrar actualizaciones de proceso al ejecutar el código
)
```

¿Cómo se ve la salida inmediata de este proceso?


```python
# nítidamente reproduce la salida de este proceso
print(json.dumps(process_output, indent=2))
```

    {
      "file_id": "596bf30e-c13d-41df-8cc8-b7e26709a468",
      "request_id": "f948a6ad-0343-e743-2b3f-0df6bc732a3a",
      "file_name": "krixik_generated_file_name_gewgneptrz.txt",
      "symbolic_directory_path": "/etc",
      "file_tags": null,
      "file_description": null
    }


Eso es lo único que ves porque retomaste control del IDE apenas que terminaste de subir el archivo a Krixik; la variable `process_output` no sabe cómo continuó o concluyó el proceso.

Puedes revisar el estado del proceso pasando el `request_id` (devuelto cuando usaste el método [`process`](metodo_process_procesar.md)) al método `process_status`, así:


```python
# usar process_status
process_1_status = pipeline.process_status(request_id=process_output["request_id"])

# nítidamente reproduce la salida de este uso de process_status
print(json.dumps(process_1_status, indent=2))
```

    {
      "status_code": 200,
      "request_id": "8863f851-fa57-4ffa-98fd-31d9df31fcdc",
      "file_id": "596bf30e-c13d-41df-8cc8-b7e26709a468",
      "message": "SUCCESS: process_status found",
      "pipeline": "process_status_method_1_keyword-db",
      "process_status": {
        "module_1": false
      },
      "overall_status": "ongoing"
    }


Acá puedes ver que el proceso no ha terminado, pues su `overall_status` (estado general) es `"ongoing"` (en curso).

Si esperas un poco y vuelves a intentar, obtendrás confirmación de que el proceso concluyó exitosamente:


```python
# usar process_status nuevamente
process_status_output = pipeline.process_status(request_id=process_output["request_id"])

# nítidamente reproduce la salida de este nuevo uso de process_status
print(json.dumps(process_status_output, indent=2))
```

    {
      "status_code": 200,
      "request_id": "4cf89f97-b82e-4104-929f-df49d928e345",
      "file_id": "596bf30e-c13d-41df-8cc8-b7e26709a468",
      "message": "SUCCESS: process_status found",
      "pipeline": "process_status_method_1_keyword-db",
      "process_status": {
        "module_1": true
      },
      "overall_status": "complete"
    }


### Ejemplo de process_status con Archivo Eliminado

Como has visto, usar `process_status` sobre una instancia fallida de [`process`](metodo_process_procesar.md) evidencia que el proceso falló.

Pero ¿qué ocurre cuando el archivo sobre el que usas `process_status` se [vence](metodo_process_procesar.md#argumentos-principales-del-metodo-process) o se [elimina](../sistema_de_archivos/metodo_delete_eliminar.md) manualmente del sistema Krixik?

En Krixik nos tomamos la eliminación de archivos muy en serio: si un archivo es [eliminado](../sistema_de_archivos/metodo_delete_eliminar.md) se borra totalmente del sistema. Por ende, si usas el método `process_status` sobre un archivo [vencido](metodo_process_procesar.md#argumentos-principales-del-metodo-process) o manualmente [eliminado](../sistema_de_archivos/metodo_delete_eliminar.md) el sistema te indicará que el `request_id` que usaste como argumento no fue hallado. El archivo ya no está, y tampoco está ningún registro de su haber sido procesado inicialmente.
