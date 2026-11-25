from sqlalchemy.orm import Session

from app.models.database import Product
from app.models.shemas import ProductCreate


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product_create: ProductCreate) -> Product:
        product = Product(
            name=product_create.name,
            price=product_create.price,
            in_stock=product_create.in_stock,
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_product_by_id(self, product_id: int) -> Product:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_all_products(self) -> list[Product]:
        return self.db.query(Product).all()

    def update_product(
        self, product_id: int, product_update: ProductCreate
    ) -> Product:
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        product.name = product_update.name
        product.price = product_update.price
        product.in_stock = product_update.in_stock
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: int) -> bool:
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        self.db.delete(product)
        self.db.commit()
        return True
