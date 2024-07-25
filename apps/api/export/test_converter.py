from .converter import __bool_cast


def test_bool_cast():
    data = {
        "true": True,
        "false": False,
        "none": None,
    }
    assert __bool_cast(data, "true") == "Yes"
    assert __bool_cast(data, "false") == "No"
    assert __bool_cast(data, "none") is None
    assert __bool_cast(data, "unknown") is None
