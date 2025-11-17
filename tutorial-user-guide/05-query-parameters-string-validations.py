import random
from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import AfterValidator


app = FastAPI(title="FastAPI Tutorial - User Guide")


# Optional query parameter
@app.get("/items_1/", tags=["Query Parameters & String Validations"], summary="Optional query parameter")
async def read_items_1(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Optional query parameter with additional validation (Modern approach in latest FastAPI)
@app.get("/items_2/", tags=["Query Parameters & String Validations"], summary="Optional query parameter with additional validation (Modern approach in latest FastAPI")
async def read_items_2(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Old syntax for defaults with additional validation (Try not to use this, might see it in legacy code)
@app.get("/items_3/", tags=["Query Parameters & String Validations"], summary="Old syntax for defaults with additional validation (Try not to use this, might see it in legacy code)")
async def read_items_3(q: str | None = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Add more validations, second parameter
@app.get("/items_4/", tags=["Query Parameters & String Validations"], summary="Add more validations, second parameter")
async def read_items_4(
    q: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Add more validations, regex pattern
@app.get("/items_5/", tags=["Query Parameters & String Validations"], summary="Add more validations, regex pattern")
async def read_items_5(
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Non None default values
@app.get("/items_6/", tags=["Query Parameters & String Validations"], summary="Non None default values")
async def read_items_6(q: Annotated[str, Query(min_length=3)] = "fixedquery"):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Required value when using Query
@app.get("/items_7/", tags=["Query Parameters & String Validations"], summary="Required value when using Query")
async def read_items_7(q: Annotated[str, Query(min_length=3)]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Required can be None
@app.get("/items_8/", tags=["Query Parameters & String Validations"], summary="Required can be None")
async def read_items_8(q: Annotated[str | None, Query(min_length=3)]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Query parameter list / multiple values
# To declare a query parameter with a type of list, you need to explicitly use Query, otherwise it would be interpreted as a request body.
@app.get("/items_9/", tags=["Query Parameters & String Validations"], summary="Query parameter list / multiple values")
async def read_items_9(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items


# Query parameter list / multiple values with defaults
@app.get("/items_10/", tags=["Query Parameters & String Validations"], summary="Query parameter list / multiple values with defaults")
async def read_items_10(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items


# Add a title
@app.get("/items_11/", tags=["Query Parameters & String Validations"], summary="Add a title & description")
async def read_items_11(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Alias parameters when wanted parameter name is not a valid python varibale name
@app.get("/items_12/", tags=["Query Parameters & String Validations"], summary="Alias parameters when wanted parameter name is not a valid python variable name")
async def read_items_12(q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Deprecating parameters when they are going to be changed or removed
@app.get("/items_13/", tags=["Query Parameters & String Validations"], summary="Deprecating parameters when they are going to be changed or removed")
async def read_items_13(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Exclude parameters from OpenAPI
@app.get("/items_14/", tags=["Query Parameters & String Validations"], summary="Exclude parameters from OpenAPI")
async def read_items_14(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None,
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}


# Custom Validation
data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


@app.get("/items_15/", tags=["Query Parameters & String Validations"], summary="Custom Validation")
async def read_items_15(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}