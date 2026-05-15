from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter

@app.get("/hello")
@limiter.limit("10/minute")
async def hello(request: Request):
    return {"message": "Hello World"}