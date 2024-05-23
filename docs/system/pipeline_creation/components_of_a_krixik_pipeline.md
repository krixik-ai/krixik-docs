## Components of a Krixik pipeline

Krixik [**pipelines**](create_pipeline.md) are comprised of one or more sequentially connected [**modules**](../../modules/modules_overview.md). These modules are containers for a range of [**parameterizable**](../parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) AI [**models**](../parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) or support functions.

Let's examine each of the key terms in the above sentence.

A [**pipeline**](create_pipeline.md) is a self-contained sequence of one or more modules that is consumed via a serverless API.  

A [**modules**](../../modules/modules_overview.md) is a processing step with a unique input/output data footprint. Each model contains a parameterizable AI model or support function.

A [**model**](../parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) is a bespoke processing function contained within a module. Many of these are AI models, but some are simpler "support functions" for inter-pipeline data preparation or transformation.

[**Parameters**](../parameters_processing_files_through_pipelines/process_method.md#selecting-models-via-the-modules-argument) can be set for each module when a pipeline is run and allow for further customization. Each has a default value, so setting them is optional. For instance, one parameterizable item is which specific AI model you want active within a given module.

--

New modules and models will constantly be added to the Krixik library. To see all available modules at any given time, use the [`.available_modules`](../convenience_methods/convenience_methods.md#view-all-available-modules-with-the-available_modules-property) property:

```python
krixik.available_modules
```

Each [**module**](../../modules/modules_overview.md) has its own documentation that details, among other things, available models for it. For example, here's documentation for the [`transcribe`](../../modules/ai_modules/transcribe_module.md) module.
