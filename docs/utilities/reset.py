# reset pipelines for demo
def reset_pipeline(pipeline):
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] != 500
    for item in current_files["items"]:
        delete_result = pipeline.delete(file_id=item["file_id"])
        assert delete_result["status_code"] != 500
    current_files = pipeline.list(symbolic_directory_paths=["/*"])
    assert current_files["status_code"] != 500
    assert len(current_files["items"]) == 0
