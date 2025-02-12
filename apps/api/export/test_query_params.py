from . import DataFormat, DataSubset, DownloadQueryParameterSerializer

Serializer = DownloadQueryParameterSerializer


def test_defaults():
    s = Serializer(data={})
    assert s.is_valid()
    assert s.validated_data == {
        "subset": DataSubset.PUBLIC,
        "format": DataFormat.CSV,
    }, "Defaults to PUBLIC subset and CSV format."


def test_other():
    s = Serializer(data={"other": "da igual"})
    assert s.is_valid(), "Does not make assumptions about unrelated fields."


def test_single_deal():
    s = Serializer(data={"deal_id": None})
    assert not s.is_valid(), "Reject nullish deal ids."

    s = Serializer(data={"deal_id": 345.01})
    assert not s.is_valid(), "Reject floaty deal ids."

    s = Serializer(data={"deal_id": "nan"})
    assert not s.is_valid(), "Reject NaN deal ids."

    s = Serializer(data={"deal_id": "inf"})
    assert not s.is_valid(), "Reject infinit deal ids."

    s = Serializer(data={"deal_id": "123"})
    assert s.is_valid()
    assert s.validated_data["deal_id"] == 123, "Deal id is parsed to int."


def test_subset():
    s = Serializer(data={"subset": "invalid/unknown"})
    assert not s.is_valid()
    assert s.errors["subset"][0].code == "invalid_choice"

    s = Serializer(data={"subset": DataSubset.UNFILTERED})
    assert s.is_valid()
    assert s.validated_data["subset"] == DataSubset.UNFILTERED


def test_format():
    s = Serializer(data={"format": "invalid/unknown"})
    assert not s.is_valid()
    assert s.errors["format"][0].code == "invalid_choice"

    s = Serializer(data={"format": DataFormat.XLSX})
    assert s.is_valid()
    assert s.validated_data["format"] == DataFormat.XLSX
