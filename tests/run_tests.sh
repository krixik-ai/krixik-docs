#!/bin/bash

# format notebooks
ruff check docs/ --fix

# run first tests
python3.10 -m pytest tests/test_0_cleanup.py -x
python3.10 -m pytest tests/test_1_conversion_no_remove.py -x
python3.10 -m pytest tests/test_2_toc_file_check.py -x
python3.10 -m pytest tests/test_3_headers.py -x
python3.10 -m pytest tests/test_4_links.py -x
python3.10 -m pytest tests/test_5_names.py -x
python3.10 -m pytest tests/test_6_data.py -x
python3.10 -m pytest tests/test_7_reset.py -x

# run test 7 - execute notebooks
# python3.10 -m pytest --nbmake docs/ --nbmake-timeout=1000 -n=auto -x

# run test 1 again - convert to markdown for final time
python3.10 -m pytest tests/test_9_conversion_remove.py -x
python3.10 -m pytest tests/test_2_toc_file_check.py -x

