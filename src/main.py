from fastapi import FastAPI, Depends
from src.middleware.rate_limiter import rate_limit_dependency

app = FastAPI()

@app.get("/", dependencies=[Depends(rate_limit_dependency)])
async def hello():
    return {"message": "Hello World - Acesso liberado"}
