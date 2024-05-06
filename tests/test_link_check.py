from krixik.utilities.validators.data.audio import is_valid
from krixik.utilities.validators.data.audio import is_size
from tests.krixik import audio_files_path
import pytest

# first - check is_valid
test_failure_data = [
    audio_files_path + "invalid_1.mp3",
]


toc_files = collect_mkdocks_toc()
for file in toc_files:
    dead_links = check_file_links(file, toc_files)
    if len(dead_links) > 0:
        print(f"file {file} contains the following dead links")
        print(dead_links)
        print("\n")