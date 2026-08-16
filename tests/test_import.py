from unittest.mock import patch


@patch("app.find_product")
def test_import_external_product(mock_find, client):
    mock_find.return_value = {
        "barcode": "1234567890123",
        "product_name": "Imported Cereal",
        "brands": "Example Brand",
        "ingredients_text": "Oats, sugar",
        "categories": "Cereals",
        "image_url": "https://example.com/cereal.jpg",
        "nutriscore_grade": "b",
    }

    response = client.post(
        "/inventory/import",
        json={"query": "1234567890123", "price": 6.50, "stock": 12},
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Imported Cereal"
    assert data["brand"] == "Example Brand"
    assert data["source"] == "Open Food Facts"


@patch("app.find_product")
def test_import_missing_external_product(mock_find, client):
    mock_find.return_value = None

    response = client.post(
        "/inventory/import",
        json={"query": "Not A Real Product", "price": 5, "stock": 2},
    )

    assert response.status_code == 404
