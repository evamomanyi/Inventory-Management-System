def test_get_all_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.get_json()
    assert "inventory" in data
    assert data["count"] >= 2


def test_get_single_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_get_missing_item(client):
    response = client.get("/inventory/99999")
    assert response.status_code == 404


def test_create_item(client):
    response = client.post(
        "/inventory",
        json={"name": "Test Juice", "price": 3.25, "stock": 10},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test Juice"
    assert data["price"] == 3.25
    assert data["stock"] == 10
    assert "id" in data


def test_create_item_validation(client):
    response = client.post("/inventory", json={"name": "Incomplete"})
    assert response.status_code == 400


def test_patch_item(client):
    response = client.patch("/inventory/1", json={"price": 5.75, "stock": 8})
    assert response.status_code == 200
    data = response.get_json()
    assert data["price"] == 5.75
    assert data["stock"] == 8


def test_delete_item(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200

    response = client.get("/inventory/1")
    assert response.status_code == 404


def test_lookup_requires_query(client):
    response = client.get("/api/lookup")
    assert response.status_code == 400
