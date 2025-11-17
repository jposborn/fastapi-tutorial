from fastapi import FastAPI

app = FastAPI(description="First Steps")

@app.get("/", summary="Hello World example")
async def root():
    return {"message": "Hello World"}


