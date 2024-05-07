#!/bin/bash

# format notebooks
ruff format docs/*.ipynb
ruff format docs/*/*.ipynb

# run first 4 tests
pytest tests/test_0_cleanup.py -x
pytest tests/test_1_conversion_no_remove.py -x
pytest tests/test_2_toc_file_check.py -x
pytest tests/test_3_links.py -x
pytest tests/test_4_names.py -x
pytest tests/test_5_reset.py -x

# run test 5 - execute notebooks
pytest --nbmake docs/ --nbmake-timeout=1000 -n=auto

# run test 1 again - convert to markdown for final time
pytest tests/test_7_conversion_remove.py -x
pytest tests/test_2_toc_file_check.py -x
