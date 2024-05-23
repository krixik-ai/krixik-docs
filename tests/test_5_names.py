from utilities.name_check import duplicate_name_check


def test_1():
    """success test that pipeline names are unique per page"""
    assert duplicate_name_check()
