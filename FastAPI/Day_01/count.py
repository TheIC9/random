from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.get("/count")
def count_words(name: str = "Guest"):
    words = name.strip().split()
    word_count = len(words)
    return JSONResponse(content={"word_count": word_count})

if __name__ == "__main__":
    uvicorn.run("count:app", host="127.0.0.1", port=8000, reload=True)
    