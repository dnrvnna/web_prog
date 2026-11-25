from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.shemas import ProductCreate, ProductResponse
from app.repos.item_repo import ProductRepository
from app.services.item_service import ProductService

router = APIRouter()


def get_repo(db: Session = Depends(get_db)) -> ProductRepository:  # noqa: B008
    return ProductRepository(db)


def get_service(repo: ProductRepository = Depends(get_repo)) -> ProductService:
    return ProductService(repo)


@router.get('/products', response_model=list[ProductResponse])
def get_all_products(service: ProductService = Depends(get_service)):
    return service.get_all_products()


router.get('/products/{product_id}', response_model=ProductResponse)


def get_product_by_id(
    product_id: int, service: ProductService = Depends(get_service)
):
    try:
        return service.get_product_by_id(product_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
            message='Товар с таким ID не найден',
        )


@router.post(
    '/products',
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_create: ProductCreate,
    service: ProductService = Depends(get_service),
):
    try:
        return service.create_product(product_create)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
            message='Ошибка при создании товара',
        )


@router.put('/products/{product_id}', response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductCreate,
    service: ProductService = Depends(get_service),
):
    product = service.repo.update_product(product_id, product_update)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Товар с таким ID не найден',
        )
    return product


@router.delete(
    '/products/{product_id}', status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id: int, service: ProductService = Depends(get_service)
):
    success = service.repo.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Товар с таким ID не найден',
        )
