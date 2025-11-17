from fastapi import FastAPI

app = FastAPI(title="FastAPI Tutorial - User Guide")

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# Query parameters with default values
@app.get("/items_1/", tags=["Query Parameters"], summary="Query parameters with default values")
async def read_item_1(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


# Query parameter with optional values
@app.get("/items_2/{item_id}", tags=["Query Parameters"], summary="Query parameter with optional values")
async def read_item_2(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# Query parameter with str and bool with type conversion. All these (and more) are valid 
# /items/foo?short=1, /items/foo?short=true, /items/foo?short=True, /items/foo?short=on
@app.get("/items_3/{item_id}",  tags=["Query Parameters"], summary="Query parameter with str and bool with type conversion")
async def read_items_3(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# 
@app.get("/users/{user_id}/items/{item_id}", tags=["Query Parameters"], summary="Multiple path and query parameters declared at the same time")
async def read_user_item_1(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Required query parameter (item_id and needy have no defaults)
@app.get("/items_4/{item_id}", tags=["Query Parameters"], summary="Required query parameter (item_id and needy have no defaults")
async def read_user_item_2(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

