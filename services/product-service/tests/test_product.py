import json


def test_create_product(client):
    response = client.post("/products/", json={
        "name": "Laptop",
        "price": 999.99,
        "stock": 10
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99
    assert data["stock"] == 10
    assert data["id"] is not None
    assert data["is_active"] is True


def test_read_products_empty(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_products(client):
    client.post("/products/", json={"name": "Laptop", "price": 999.99, "stock": 10})
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Laptop"


def test_read_product_by_id(client):
    create = client.post("/products/", json={"name": "Phone", "price": 499.99, "stock": 5})
    product_id = create.json()["id"]
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Phone"


def test_read_product_not_found(client):
    response = client.get("/products/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_product(client):
    create = client.post("/products/", json={"name": "Tablet", "price": 299.99, "stock": 3})
    product_id = create.json()["id"]
    response = client.put(f"/products/{product_id}", json={"price": 249.99, "stock": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 249.99
    assert data["stock"] == 2
    assert data["name"] == "Tablet"


def test_update_product_not_found(client):
    response = client.put("/products/999", json={"price": 100.00})
    assert response.status_code == 404


def test_delete_product(client):
    create = client.post("/products/", json={"name": "Monitor", "price": 399.99, "stock": 7})
    product_id = create.json()["id"]
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 204
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404


def test_delete_product_not_found(client):
    response = client.delete("/products/999")
    assert response.status_code == 404


def test_create_product_invalid_price(client):
    response = client.post("/products/", json={
        "name": "Laptop",
        "price": -10.00,
        "stock": 5
    })
    assert response.status_code == 422


def test_create_product_missing_name(client):
    response = client.post("/products/", json={
        "price": 99.99,
        "stock": 5
    })
    assert response.status_code == 422


def test_cache_hit(client):
    client.post("/products/", json={"name": "Keyboard", "price": 79.99, "stock": 20})
    first = client.get("/products/")
    second = client.get("/products/")
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()


def test_cache_invalidated_on_create(client):
    client.post("/products/", json={"name": "Mouse", "price": 29.99, "stock": 15})
    first = client.get("/products/")
    assert len(first.json()) == 1
    client.post("/products/", json={"name": "Keyboard", "price": 79.99, "stock": 20})
    second = client.get("/products/")
    assert len(second.json()) == 2