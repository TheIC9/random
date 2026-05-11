from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
app = FastAPI()

@app.get("/reversed")
def greet(name: str = "Guest"):
    greeting = name[::-1]
    return JSONResponse(content={"greeting": greeting})


if __name__ == "__main__":
    uvicorn.run("reversed:app", host="127.0.0.1", port=8000, reload=True)
