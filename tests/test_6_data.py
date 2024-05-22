from utilities.data_check import check_for_dead_data_links


def test_1():
    """check for dead data links - both in pages and in /data/input/"""
    all_page_dead_links, all_data_dead_links = check_for_dead_data_links()
    assert len(all_page_dead_links) == 0, f"dead page data links found in these pages: {all_page_dead_links}"
    assert len(all_data_dead_links) == 0, f"dead /data/input/ links found: {all_data_dead_links}"
