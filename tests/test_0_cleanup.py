import os
import pytest
from utilities import base_dir


def delete_all_files(dir_path: str) -> None:
    files = os.listdir(dir_path)    
    for file_name in files:
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            

def list_files(dir_path: str) -> list:
    file_paths = []    
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            file_paths.append(item_path)
    return file_paths


cleanup_dirs = [
    f"{base_dir}/data/output",
    f"{base_dir}/data/pipeline_configs"
]


@pytest.mark.parametrize("delete_path", cleanup_dirs)
def test_1(delete_path):
    """ remove all files from data/output """
    delete_all_files(delete_path)
    assert len(list_files(delete_path)) == 0, f"some files in {delete_path} could not be deleted"
    