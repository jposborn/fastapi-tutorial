from fastapi import FastAPI

from enum import Enum

app = FastAPI(title="FastAPI Tutorial - User Guide")

# Recieve parameter in path
@app.get("/items/{item_id}", tags=["Path Parameters"], summary="Receive parameter in path")
async def read_item(item_id: int):
    return {"item_id": item_id}


# Order matters for path parameters (/users/me first to avoid /users/{user_id} thinking 'me' is the user_id)
@app.get("/users/me", tags=["Path Parameters"], summary="Order matters for path parameters (/users/me first to avoid /users/{user_id} thinking 'me' is the user_id)")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}", tags=["Path Parameters"], summary="Order matters for path parameters (/users/me first to avoid /users/{user_id} thinking 'me' is the user_id)")
async def read_user(user_id: str):
    return {"user_id": user_id}


# Use enumerator to define fixed parameter values
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}", tags=["Path Parameters"], summary="Use enumerator to define fixed parameter values")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# Passing a file path as a parameter could lead to problems
# Use Starlette option to declare a path parameter
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

