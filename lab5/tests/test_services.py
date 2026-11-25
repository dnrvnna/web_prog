from unittest.mock import MagicMock

import pytest

from app.models.shemas import ProductCreate
from app.services.item_service import ProductService


def test_create_product_service():
    mock_repo = MagicMock()
    mock_repo.create_product.return_value = {
        'id': 1,
        'name': 'Тестовый продукт',
        'price': 10.0,
    }
    service = ProductService(repo=mock_repo)
    product_create = ProductCreate(name='Тестовый продукт', price=10.0)
    result = service.create_product(product_create)

    assert result['name'] == 'Тестовый продукт'
    mock_repo.create_product.assert_called_once_with(product_create)


def test_get_product_not_found():
    mock_repo = MagicMock()
    mock_repo.get_product_by_id.return_value = None
    service = ProductService(repo=mock_repo)

    with pytest.raises(ValueError, match='Товар с таким ID не найден'):
        service.get_product_by_id(999)
