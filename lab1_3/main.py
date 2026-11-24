from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

app = FastAPI()


class Item(BaseModel):
    id: int | None = None
    name: str = Field(
        ..., max_length=50, min_length=3, description='Название товара'
    )
    price: float = Field(..., gt=0, description='Цена товара')
    in_stock: bool

    @field_validator('name')
    @classmethod
    def no_digits(cls, value: str) -> str:
        if any(char.isdigit() for char in value):
            raise ValueError('Имя товара не должно содержать цифры')
        return value


db: list[Item] = []
current_id = 1


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'error': {
                'code': 'internal_server_error',
                'message': 'Упс! Что-то пошло не так. Мы уже чиним это!',
            }
        },
    )


@app.get('/items', response_model=list[Item])
def get_items():
    return db


@app.get('/items/{item_id}', response_model=Item)
def get_item(item_id: int):
    for item in db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail='Item not found')


@app.post('/items', response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    global current_id
    item.id = current_id
    current_id += 1
    db.append(item)
    return item


@app.put('/items/{item_id}', response_model=Item)
def update_item(item_id: int, item: Item):
    for index, item in enumerate(db):  # noqa: PLR1704
        if item.id == item_id:
            db[index] = item
            return item
    raise HTTPException(status_code=404, detail='Item not found')


@app.delete('/items/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    for index, item in enumerate(db):
        if item.id == item_id:
            del db[index]
            return
    raise HTTPException(status_code=404, detail='Item not found')
