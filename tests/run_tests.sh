#!/bin/bash

# format notebooks
ruff format docs/*.ipynb
ruff format docs/*/*.ipynb

# run tests on markdown
pytest tests/test_docs.py

# run notebooks
pytest --nbmake docs/