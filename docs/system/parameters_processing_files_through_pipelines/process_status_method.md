## The `.process_status` Method

The `.process_status` method is available on every Krixik pipeline. It is invoked whenever you want to check the status of files being processed through a pipeline.

This method is especially useful when using the [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method with `wait_for_process` set to `False`, for it gives you visibility into processes that have continued server-side after you regain control of your IDE.

This overview of the `.process_status` method is divided into the following sections:

- [.process_status Method Arguments](#.process_status-method-arguments)
- [.process_status Example - Success](#.process_status-example---success)
- [.process_status Example - Failure](#.process_status-example---failure)
- [.process_status Example - Deleted File](#.process_status-example---deleted-file)

### `.process_status` Method Arguments

The `.process_status` method takes a single argument:

- `request_id`: (required, str) The unique ID associated with the relevant execution instance of the [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method.

### `.process_status` Example - Success

Let's examine how the `.process_status` method works when the [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method succeeds. `wait_for_process` will be set to `False`.

First we'll need to create a pipeline. We can use a single-module pipeline with a [`parser`](../../modules/ai_model_modules/parser_module.md) module for this example:


```python
# create a pipeline with a single parser module

pipeline_1 = krixik.create_pipeline(name="process_status_method_1_parser",
                                    module_chain=["parser"])
```

Now we'll process a file through your pipeline. Let's use a text file holding Shirley Jackson's famous short story, <u>The Lottery</u>:


```python
# process text file through pipeline with wait_for_process on False

process_output_1 = pipeline_1.process(local_file_path="../../data/input/XXX.txt", # the initial local filepath where the input JSON file is stored
                                      expire_time=60 * 30, # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=False, # do not wait for process to complete before returning IDE control to user
                                      verbose=False) # do not display process update printouts upon running code
```

What does immediate output for this process look like?


```python
# nicely print the output of this process

print(json.dumps(process_output_1, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "examples-transcribe-multilingual-sentiment-docs",
      "request_id": "1119f07f-e4a1-4021-9668-2f19ea367568",
      "file_id": "efdc2954-9bef-4427-8de1-2bd18a830015",
      "message": "SUCCESS - output fetched for file_id efdc2954-9bef-4427-8de1-2bd18a830015.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "For the starting position, we want to see the feed between the hip and shoulders width, the heels on the floor, a neutral column mediated by abdominal tension, the shoulders are lightly in front of the bar or above, straight arms, symmetrical hands and enough width to not rather the knees and we can have a lightly look forward.",
          "positive": 0.99,
          "negative": 0.01,
          "neutral": 0.0
        },
        {
          "snippet": "To perform the movement, our athlete will push from the heels, he will start to raise the hips and shoulders together, when the bar passes the knees, we extend the hip.",
          "positive": 0.996,
          "negative": 0.004,
          "neutral": 0.0
        },
        {
          "snippet": "For return, we are going to delay the push of the knees and we are going to push the hip back and the chess forward.",
          "positive": 0.006,
          "negative": 0.994,
          "neutral": 0.0
        },
        {
          "snippet": "When the bar passes the knees, we have the correct angle of our trunk and we already blessed the knees to approximately half the hip for starting position and resting.",
          "positive": 0.493,
          "negative": 0.507,
          "neutral": 0.0
        },
        {
          "snippet": "Throughout the movement, we want to see the bar close to the body when going up and down.",
          "positive": 0.972,
          "negative": 0.028,
          "neutral": 0.0
        }
      ],
      "process_output_files": [
        "/Users/jeremywatt/Desktop/krixik/code/krixik-docs/docs/examples/transcribe/efdc2954-9bef-4427-8de1-2bd18a830015.json"
      ]
    }


That's all you see because you retook control of the IDE as soon as the upload to Krixik was completed; the `process_output_1` variable doesn't know how the rest of the process went.

You can check the status of the process by feeding the `request_id` (returned when you called the [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method) to the `.process_status` method, as follows:


```python
# invoke .process_status

process_1_status = pipeline_1.process_status(request_id=XXXX)

# nicely print the output our .process_status call

print(json.dumps(process_1_status, indent=2))
```

    {
      "status_code": 200,
      "request_id": "d248636b-5ea5-4da7-a250-9e00332cd2b8",
      "file_id": "3d435c55-05ae-41b6-aee3-76da8c7b0841",
      "message": "SUCCESS: process_status found",
      "pipeline": "process-status-doc",
      "process_status": {
        "parser": false
      },
      "overall_status": "ongoing"
    }


Here you can see that your process has not yet finalized; its `overall_status` shows as `"ongoing"`.

If we wait a few moments and try again, you will see confirmation that the process completed successfully.


```python
# invoke .process_status again

process_1_status = pipeline_1.process_status(request_id=XXXX)

# nicely print the output our .process_status call again

print(json.dumps(process_1_status, indent=2))
```

    {
      "status_code": 200,
      "request_id": "cf1c55e3-34c8-4c81-a940-b264c7c0448d",
      "file_id": "3d435c55-05ae-41b6-aee3-76da8c7b0841",
      "message": "SUCCESS: process_status found",
      "pipeline": "process-status-doc",
      "process_status": {
        "parser": true
      },
      "overall_status": "complete"
    }


### `.process_status` Example - Failure

Now let's examine how the `.process_status` method works when the [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method fails. `wait_for_process` will be set to `False`.

First we'll need to create a pipeline. We can use a multi-module [vector search pipeline](../../examples/search_pipeline_examples/multi_basic_semantic_search.md) with a [`parser`](../../modules/ai_model_modules/parser_module.md) module, a [`text-embedder`](../modules/ai_model_modules/text-embedder_module.md) module, and a [`vector-db`](../../modules/database_modules/vector-db_module.md) module:


```python
# create a vector search pipeline with a parser, a text embedder, and a vector db module

pipeline_2 = krixik.create_pipeline(name="process_status_method_2_parser_embedder_vector-db",
                                    module_chain=["parser", "text-embedder", "vector-db"])
```

# Now we'll process a file through our new pipeline. We'll use a text file with [XXXXXXX]; our expectation is that this process will fail:


```python
# process text file through pipeline with wait_for_process on False

process_output_2 = pipeline_2.process(local_file_path="../../data/input/XXX.txt", # the initial local filepath where the input JSON file is stored
                                      expire_time=60 * 30, # process data will be deleted from the Krixik system in 30 minutes
                                      wait_for_process=False, # do not wait for process to complete before returning IDE control to user
                                      verbose=False) # do not display process update printouts upon running code
```

What does immediate output for this process look like?


```python
# nicely print the output of this process

print(json.dumps(process_output_2, indent=2))
```

    {
      "status_code": 200,
      "pipeline": "examples-transcribe-multilingual-sentiment-docs",
      "request_id": "1119f07f-e4a1-4021-9668-2f19ea367568",
      "file_id": "efdc2954-9bef-4427-8de1-2bd18a830015",
      "message": "SUCCESS - output fetched for file_id efdc2954-9bef-4427-8de1-2bd18a830015.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "For the starting position, we want to see the feed between the hip and shoulders width, the heels on the floor, a neutral column mediated by abdominal tension, the shoulders are lightly in front of the bar or above, straight arms, symmetrical hands and enough width to not rather the knees and we can have a lightly look forward.",
          "positive": 0.99,
          "negative": 0.01,
          "neutral": 0.0
        },
        {
          "snippet": "To perform the movement, our athlete will push from the heels, he will start to raise the hips and shoulders together, when the bar passes the knees, we extend the hip.",
          "positive": 0.996,
          "negative": 0.004,
          "neutral": 0.0
        },
        {
          "snippet": "For return, we are going to delay the push of the knees and we are going to push the hip back and the chess forward.",
          "positive": 0.006,
          "negative": 0.994,
          "neutral": 0.0
        },
        {
          "snippet": "When the bar passes the knees, we have the correct angle of our trunk and we already blessed the knees to approximately half the hip for starting position and resting.",
          "positive": 0.493,
          "negative": 0.507,
          "neutral": 0.0
        },
        {
          "snippet": "Throughout the movement, we want to see the bar close to the body when going up and down.",
          "positive": 0.972,
          "negative": 0.028,
          "neutral": 0.0
        }
      ],
      "process_output_files": [
        "/Users/jeremywatt/Desktop/krixik/code/krixik-docs/docs/examples/transcribe/efdc2954-9bef-4427-8de1-2bd18a830015.json"
      ]
    }


That's all you see because you retook control of the IDE as soon as the upload to Krixik was completed; the `process_output_2` variable doesn't know how the rest of the process went.

You can check the status of our process by feeding the `request_id` (returned when you called [`.process`](../parameters_processing_files_through_pipelines/process_method.md) method) to the `.process_status` method, as follows:


```python
# invoke .process_status

process_2_status = pipeline_2.process_status(request_id=XXXX)

# nicely print the output our .process_status call

print(json.dumps(process_2_status, indent=2))
```

    {
      "status_code": 200,
      "request_id": "d248636b-5ea5-4da7-a250-9e00332cd2b8",
      "file_id": "3d435c55-05ae-41b6-aee3-76da8c7b0841",
      "message": "SUCCESS: process_status found",
      "pipeline": "process-status-doc",
      "process_status": {
        "parser": false
      },
      "overall_status": "ongoing"
    }


Here you can see that your process has not yet finalized; its `overall_status` shows as `"ongoing"`.

If you wait a bit and try again, you will see confirmation that the process failed.


```python
# invoke .process_status again

process_2_status = pipeline_2.process_status(request_id=XXXX)

# nicely print the output our .process_status call again

print(json.dumps(process_2_status, indent=2))
```

    {
      "status_code": 200,
      "request_id": "cf1c55e3-34c8-4c81-a940-b264c7c0448d",
      "file_id": "3d435c55-05ae-41b6-aee3-76da8c7b0841",
      "message": "SUCCESS: process_status found",
      "pipeline": "process-status-doc",
      "process_status": {
        "parser": true
      },
      "overall_status": "complete"
    }


### `.process_status` Example - Deleted File

As you have just observed, `.process_status` on a failed [`.process`](../parameters_processing_files_through_pipelines/process_method.md) attempt shows us that the process failed.

What happens when the file `.process_status` is run on [expires](../parameters_processing_files_through_pipelines/process_method.md#core-process-method-arguments) or is manually [deleted](../file_system/delete_method.md) from the Krixik system?

We take deletion seriously at Krixik—if a file is [deleted](../file_system/delete_method.md), it's entirely wiped from the system. Consequently, calling the `.process_status` method on an [expired](../parameters_processing_files_through_pipelines/process_method.md#core-process-method-arguments) or manually [deleted](../file_system/delete_method.md) file will tell you that the `request_id` you used as an argument was not found. The file is gone, as is any record of its having been processed in the first place.
