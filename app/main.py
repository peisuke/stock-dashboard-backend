from fastapi import FastAPI
from app.api.routes import search, stocks

app = FastAPI()

# ルーターの登録
app.include_router(search.router)
app.include_router(stocks.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
