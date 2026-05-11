from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
app = FastAPI()
@router.get()
@app.get("/greet")
def greet(name: str = "Guest"):
    greeting = f"Hello {name}!"
    return JSONResponse(content={"greeting": greeting})


if __name__ == "__main__":
    uvicorn.run("main_01:app", host="127.0.0.1", port=8000, reload=True)
