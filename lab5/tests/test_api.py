from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_create_product(client: TestClient):
    payload = {'name': 'Тест товар', 'price': 150.0, 'in_stock': True}
    response = client.post('/products', json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data['name'] == payload['name']
    assert 'id' in data


def test_get_product_list(client: TestClient):
    payload = {'name': 'Тест товар', 'price': 150.0, 'in_stock': True}
    client.post('/products', json=payload)

    response = client.get('/products')
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_product(client: TestClient):
    payload = {'name': 'Тест товар', 'price': 150.0, 'in_stock': True}
    create_resp = client.post('/products', json=payload)
    product_id = create_resp.json()['id']

    response = client.put(
        f'/products/{product_id}',
        json={'name': 'Новый', 'price': 10.0, 'in_stock': False},
    )
    assert response.status_code == 200
    assert response.json()['name'] == 'Новый'


def test_delele(client):
    payload = {'name': 'Тест товар', 'price': 150.0, 'in_stock': True}
    create_resp = client.post('/products', json=payload)
    product_id = create_resp.json()['id']

    del_response = client.delete(f'/products/{product_id}')
    assert del_response.status_code == 204

    get_resp = client.get(f'/products/{product_id}')
    assert get_resp.status_code == 404


def test_create_product_invalid_price(client: TestClient):
    payload = {'name': '', 'price': -10.0, 'in_stock': True}
    response = client.post('/products', json=payload)

    assert response.status_code == 422  # Unprocessable Entity
    assert 'price' in str(response.json())


def test_create_product_digit_name(client: TestClient):
    payload = {'name': '00000000'.capitalize(), 'price': 100.0}
    response = client.post('/products', json=payload)

    assert response.status_code == 422  # Unprocessable Entity
    assert 'Название продукта должно быть буквенно-цифровым' in str(
        response.json()
    )


def test_get_not_found(client: TestClient):
    response = client.get('/products/999')
    assert response.status_code == 404  # Not Found
    assert response.json() == {'detail': 'Товар с таким ID не найден'}
