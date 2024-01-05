from fastapi import FastAPI, Depends, HTTPException, Form, Query
from fastapi.responses import JSONResponse

app = FastAPI()

valid_username = "user123"
valid_password = "password123"

@app.get("/")
def read_hello():
    content = {"message": "Hello, World!"}
    return JSONResponse(content=content)

@app.post("/login/")
async def login(
    username: str = Query(None, title="User Name"),
    password: str = Query(None, title="Password")
):
    # Check if provided credentials match the valid ones
    if username == valid_username and password == valid_password:
        content = {"response": "1"}
        return JSONResponse(content=content)
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")