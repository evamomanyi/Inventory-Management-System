from unittest.mock import Mock, patch
import pytest
from external_api import get_product_by_barcode, search_product_by_name, find_product


def fake_response(payload):
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = payload
    return response


@patch("external_api.requests.get")
def test_get_product_by_barcode(mock_get):
    mock_get.return_value = fake_response({
        "status": 1,
        "product": {
            "code": "1234567890123",
            "product_name": "Mock Milk",
            "brands": "Mock Brand",
            "ingredients_text": "Milk",
            "categories": "Milk",
            "image_front_url": "https://example.com/milk.jpg",
            "nutriscore_grade": "a",
        },
    })

    result = get_product_by_barcode("1234567890123")

    assert result["product_name"] == "Mock Milk"
    assert result["brands"] == "Mock Brand"
    mock_get.assert_called_once()


@patch("external_api.requests.get")
def test_barcode_not_found(mock_get):
    mock_get.return_value = fake_response({"status": 0})
    assert get_product_by_barcode("0000000000000") is None


@patch("external_api.requests.get")
def test_search_product_by_name(mock_get):
    mock_get.return_value = fake_response({
        "products": [{
            "code": "1111111111111",
            "product_name": "Mock Cereal",
            "brands": "Mock Brand",
        }]
    })

    result = search_product_by_name("Mock Cereal")

    assert result["product_name"] == "Mock Cereal"


@patch("external_api.get_product_by_barcode")
def test_find_product_uses_barcode_for_numeric_query(mock_barcode):
    mock_barcode.return_value = {"product_name": "Barcode Product"}
    result = find_product("1234567890123")
    assert result["product_name"] == "Barcode Product"
    mock_barcode.assert_called_once_with("1234567890123")


@patch("external_api.search_product_by_name")
def test_find_product_uses_name_for_text_query(mock_search):
    mock_search.return_value = {"product_name": "Name Product"}
    result = find_product("Name Product")
    assert result["product_name"] == "Name Product"
    mock_search.assert_called_once_with("Name Product")


@patch("external_api.requests.get")
def test_external_api_failure(mock_get):
    import requests
    mock_get.side_effect = requests.RequestException("network down")

    with pytest.raises(requests.RequestException):
        get_product_by_barcode("1234567890123")
