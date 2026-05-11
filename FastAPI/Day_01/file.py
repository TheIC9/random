from fastapi import FastAPI

app = FastAPI()


# @app.get("/files/{file_path:path}")
# async def read_file(file_path: str):
#     return {"file_path": file_path}
@app.get("/files/{file_content:path}")
async def read_file(file_content: str):
    with open("file.txt") as f:
        file_content = f.read()
    return {"file_path": file_content}
