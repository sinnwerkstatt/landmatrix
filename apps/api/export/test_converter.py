from decimal import Decimal

from .converter import __bool_cast, __decimal_cast


def test_bool_cast():
    data = {
        "true": True,
        "false": False,
        "none": None,
    }
    assert __bool_cast(data, "true") == "Yes"
    assert __bool_cast(data, "false") == "No"
    assert __bool_cast(data, "none") == "Unknown"
    assert __bool_cast(data, "unknown") == "Unknown"


def test_decimal_cast():
    data = {
        "zero": Decimal("0.00"),
        "one": Decimal("01.00"),
        "none": None,
    }
    assert __decimal_cast(data, "zero") == "0.00"
    assert __decimal_cast(data, "one") == "1.00"
    assert __decimal_cast(data, "none") == ""
