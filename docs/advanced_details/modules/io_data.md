### Viewing a module's i/o details

You can use the `._example` property to see an example a module's input/output. 


```python
# examine a module's "click-ability" data by using the click_data property
# print a dictionary nicely in an ide or notebook
json_print(module_1.output_example)
```

    {
      "transcript": "This is the full transcript.",
      "segments": [
        {
          "id": 1,
          "seek": 0,
          "start": 0.0,
          "end": 10.0,
          "text": "This is the",
          "tokens": [
            20,
            34
          ],
          "temperature": 0.0,
          "avg_logprob": 0.0,
          "compression_ratio": 0.0,
          "no_speech_prob": 0.0,
          "confidence": 0.0,
          "words": [
            {
              "text": "This",
              "start": 0.0,
              "end": 1.0,
              "confidence": 0.5
            },
            {
              "text": "is the",
              "start": 1.0,
              "end": 2.0,
              "confidence": 0.6
            }
          ]
        },
        {
          "id": 2,
          "seek": 10,
          "start": 10.0,
          "end": 20.0,
          "text": "main text",
          "tokens": [
            44,
            101
          ],
          "temperature": 0.0,
          "avg_logprob": 0.0,
          "compression_ratio": 0.0,
          "no_speech_prob": 0.0,
          "confidence": 0.0,
          "words": [
            {
              "text": "main",
              "start": 10.0,
              "end": 11.0,
              "confidence": 0.7
            },
            {
              "text": "text",
              "start": 11.0,
              "end": 12.0,
              "confidence": 0.8
            }
          ]
        }
      ],
      "language": "English"
    }
