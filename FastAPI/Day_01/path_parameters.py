from fastapi import FastAPI
app = FastAPI()
@app.get("/items/{name}")
async def read_item(name):
    return {f"Hello {name}"}