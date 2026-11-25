from pydantic import BaseModel, Field, field_validator


class ProductSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    price: float = Field(..., gt=0)
    in_stock: bool = True

    @field_validator('name')
    @classmethod
    def name_must_be_alphanumeric(cls, v: str) -> str:
        if v.isdigit():
            raise ValueError('Название продукта должно быть буквенно-цифровым')
        return v


class ProductCreate(ProductSchema):
    pass


class ProductResponse(ProductSchema):
    id: int
