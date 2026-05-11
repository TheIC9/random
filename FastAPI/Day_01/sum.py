from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
app = FastAPI()

@app.get("/sum")
def greet(a: int = 0,b:int = 0):
    result = a+b
    sum = f" a + b = {result} "
    return JSONResponse(content={"sum": sum})


if __name__ == "__main__":
    uvicorn.run("sum:app", host="127.0.0.1", port=8000, reload=True)
