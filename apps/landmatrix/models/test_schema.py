from datetime import datetime

import pytest
from pydantic import ValidationError

from .schema import QuotationItem


def test_valid_quotation():
    quotation = QuotationItem(nid="abc123", pages="15-20")
    assert quotation.nid == "abc123"
    assert quotation.pages == "15-20"
    assert isinstance(quotation.timestamp, datetime)


def test_valid_empty_pages():
    quotation = QuotationItem(nid="abc123")
    assert quotation.pages == ""


def test_valid_page_formats():
    valid_pages = ["15", "15-20", "15, 18, 22-25", "xviii, 3-7"]
    for pages in valid_pages:
        quotation = QuotationItem(nid="abc123", pages=pages)
        assert quotation.pages == pages


def test_invalid_page_format():
    with pytest.raises(ValidationError):
        QuotationItem(nid="abc123", pages=123)  # noqa


def test_missing_nid():
    with pytest.raises(ValidationError):
        QuotationItem(pages="10-15")  # noqa


def test_extra_fields_forbidden():
    with pytest.raises(ValidationError):
        QuotationItem(
            nid="abc123",
            pages="15-20",
            extra_field="invalid",  # noqa
        )
