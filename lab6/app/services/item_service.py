from app.models.shemas import ProductCreate
from app.repos.item_repo import ProductRepository


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def get_all_products(self):
        return self.repo.get_all_products()

    def get_product_by_id(self, product_id: int):
        product = self.repo.get_product_by_id(product_id)
        if not product:
            raise ValueError('Товар с таким ID не найден')
        return product

    def create_product(self, product_create: ProductCreate):
        price = product_create.price
        if price <= 0:
            raise ValueError('Цена продукта должна быть больше нуля')
        return self.repo.create_product(product_create)
