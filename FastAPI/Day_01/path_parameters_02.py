from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "IC"}

@app.get("/users/{user_id}", response_class=HTMLResponse)
async def read_user(user_id: str):
    return f'''
    <html>
        <body>
            <h2>user_id: {user_id}</h2>
            <a href="http://127.0.0.1:8000/users/me"> ME </a>
        </body>
    </html>
    '''