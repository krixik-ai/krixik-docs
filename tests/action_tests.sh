#!/bin/bash

# format notebooks
ruff check docs/ --fix


PYTHONPATH=. python3.10 -m pytest tests/test_2_toc_file_check.py
PYTHONPATH=. python3.10 -m pytest tests/test_3_headers.py -x
PYTHONPATH=. python3.10 -m pytest tests/test_4_links.py -s -x
PYTHONPATH=. python3.10 -m pytest tests/test_5_names.py -x