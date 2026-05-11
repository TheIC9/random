from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.get("/")
def calc(a: int = 0, b: int = 0, c: str = ''):
    try:
        if c == "+":
            value = "sum"
            result = a + b
        elif c == "-":
            value = "sub"
            result = a - b
        elif c == "*":
            value = "mul"
            result = a * b
        elif c == "/":
            if b == 0:
                return JSONResponse(content={"error": "Division by zero not allowed"}, status_code=400)
            value = "div"
            result = a / b
        else:
            return JSONResponse(content={"error": "Invalid operator. Use +, -, *, /"}, status_code=400)

        return JSONResponse(content={
            "a": a,
            "b": b,
            "c": value,
            "result": result
        })
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("calc:app", host="127.0.0.1", port=8000, reload=True)
