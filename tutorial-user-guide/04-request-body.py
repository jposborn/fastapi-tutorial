from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


# Use pydantic model declared above. Includes validation, any required type conversion, schema generation etc.
@app.post("/items/")
async def create_item(item: Item):
    return item


# Use the model
@app.post("/item_2/")
async def create_item_2(item: Item):
    item_dict = item.model_dump() # convert to dict
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# Model with path parameters
@app.put("/items_1/{item_id}")
async def update_item_1(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}


# Model with path and query parameters
@app.put("/items_2/{item_id}")
async def update_item_2(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result