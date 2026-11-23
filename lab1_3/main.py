from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List


app = FastAPI()


class Item(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    in_stock: bool


db: List[Item] = []
current_id = 1


@app.get('/items', response_model=List[Item])
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
    for index, item in enumerate(db):
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
