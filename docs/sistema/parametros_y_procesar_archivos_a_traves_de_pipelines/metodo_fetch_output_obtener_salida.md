<a href="https://colab.research.google.com/github/krixik-ai/krixik-docs/blob/main/docs/system/parameters_processing_files_through_pipelines/fetch_output_method.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## El Método `fetch_output` (Obtener Salida)
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/system/parameters_processing_files_through_pipelines/fetch_output_method/)

El método `fetch_output` se usa para descargar la salida de un [`proceso`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) de *pipeline*. Esto es particularmente útil cuando usas el método [`process`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) poniendo `wait_for_process` como `False`, dado que en ese caso la salida del proceso no será inmediatamente reproducida por el método [`process`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md).

### Argumentos del Método `fetch_output`

El método `fetch_output` toma dos argumentos:

- `file_id`: (requerido, str) El `file_id` de un archivo cuya salida del método [`process`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md) quieres buscar.

- `local_save_directory`: (opcional, str) El directorio local donde te gustaría guardar la salida recuperada. Su valor predeterminado es el directorio actual del que estás trabajando.


### Ejemplo de `.fetch_output`

Primero debes crear un *pipeline* sobre el cual puedas ejecutar este ejemplo. Un *pipeline* que consiste de un solo módulo [`parser`](../../modulos/modulos_de_funciones_de_apoyo/modulo_parser_fragmentacion.md) funciona bien:


```python
# crea un pipeline de módulo único con un módulo parser para este ejemplo
pipeline = krixik.create_pipeline(name="metodo_fetch-output_1_parser", module_chain=["parser"])
```

Ahora procesa un archivo a través de este *pipeline*. Usa un breve archivo TXT que contiene el primer párrafo de <u>1984</u>, por George Orwell:


```python
# procesa el archivo TXT por el pipeline de módulo único con un módulo parser
process_output = pipeline.process(
    local_file_path=data_dir + "input/1984_muy_corto.txt",  # la ruta de archivo inicial en la que yace el archivo de entrada
    local_save_directory=data_dir + "output",  # el directorio local en el que se guardará el archivo de salida
    expire_time=60 * 60 * 24 * 7,  # data de este proceso se eliminará del sistema Krixik en 7 días
    wait_for_process=True,  # espera que el proceso termine antes de devolver control del IDE al usuario
    verbose=False,  # no mostrar actualizaciones de proceso al ejecutar el código
)
```

El archivo se ha procesado exitosamente. Ahora asume que han pasado unos días y que necesitas recuperar la salida de este proceso. Necesitarás su `file_id`, así que reproduce el objeto `process_output` anterior para conseguirlo:


```python
# reproduce el objeto para ver su file_id
print(json.dumps(process_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "fetch-output-method_1_parser",
      "request_id": "ff3a5841-f250-49d2-94ca-f142b57129a1",
      "file_id": "83f7bc97-bf47-4b3d-8268-b1a147be8950",
      "message": "SUCCESS - output fetched for file_id 83f7bc97-bf47-4b3d-8268-b1a147be8950.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
          "line_numbers": [
            1
          ]
        },
        {
          "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
          "line_numbers": [
            2,
            3,
            4,
            5
          ]
        }
      ],
      "process_output_files": [
        "../../../data/output/83f7bc97-bf47-4b3d-8268-b1a147be8950.json"
      ]
    }


Ya con el `file_id` puedes usar el método `fetch_output` para recuperar esta salida:


```python
# recupera la salida de este proceso con el método fetch_output y el file_id
fetched_output = pipeline.fetch_output(file_id=process_output["file_id"], local_save_directory="../../../data/output")
```

Reproducir la salida recuperada muestra el JSON que buscabas y alguna información adicional. Esta información adicional es muy similar a la salida del método [`process`](../parametros_y_procesar_archivos_a_traves_de_pipelines/metodo_process_procesar.md):


```python
# nítidamente reproduce la salida de este proceso
print(json.dumps(fetched_output, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "fetch-output-method_1_parser",
      "request_id": "607cfa28-1c7e-4ea7-aba0-9e4de42a0c41",
      "file_id": "83f7bc97-bf47-4b3d-8268-b1a147be8950",
      "message": "SUCCESS - output fetched for file_id 83f7bc97-bf47-4b3d-8268-b1a147be8950.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
          "line_numbers": [
            1
          ]
        },
        {
          "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
          "line_numbers": [
            2,
            3,
            4,
            5
          ]
        }
      ],
      "process_output_files": [
        "../../../data/output/83f7bc97-bf47-4b3d-8268-b1a147be8950.json"
      ]
    }


Al final de esta salida aparece el directorio local al que la salida recuperada se ha descargado.
